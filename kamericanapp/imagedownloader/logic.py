import bs4
import requests
from requests_html import HTMLSession
import re
import os
import time

from redis import Redis
from rq import get_current_job

class ImageDownloader(object):
    """Class handling downloading images from URLs."""
    def __init__(self, chunk_size=1024):
        #working_directory = os.getcwd()
        #print(working_directory)
        #dirname = os.path.dirname(__file__)
        #print(dirname, __file__)
        #self.download_path = os.path.join(working_directory, 'kamericanapp', 'database', 'images', 'download')
        
        current_directory = os.path.abspath(os.path.dirname(__file__))
        self.download_path = os.path.join(current_directory, '..', 'database', 'images', 'download')
        #print(os.listdir(self.download_path))
        
        self.chunk_size = chunk_size
        self.html_session = HTMLSession()
        return
    ### Public methods
    def download_from_list_of_twitter_urls(self, twitter_URL_list):
        """Async method downloading images from twitter URLs."""
        redis = Redis()
        current_job = get_current_job(connection=redis)
        if current_job is None:
            print("@@@ Issue getting current job @@@")
            return "No result"
        else:
            current_job.meta['process'] = "Download images"
            current_job.save_meta()

            n_downloaded_image_total = 0
            n_twitter_link = len(twitter_URL_list)
            i_twitter_link = 0
            for twitter_URL in twitter_URL_list:
                print("Saving images from: " + twitter_URL)

                progress = "Downloaded {0} images from {1}/{2} URLs ({3}%)".format(
                    n_downloaded_image_total,
                    i_twitter_link,
                    n_twitter_link,
                    int(i_twitter_link/n_twitter_link*100),
                )
                print(progress)
                current_job.meta['progress'] = progress
                current_job.save_meta()
                
                n_downloaded_image_total += self._download_from_twitter_url(twitter_URL)
                i_twitter_link += 1

            result = "Downloaded {0} images from {1} URLs".format(
                n_downloaded_image_total,
                n_twitter_link,
            )
            return result
    ### Private methods
    def _download_from_twitter_url(self, twitter_URL):
        """Private main method.""" 
        twitter_URL = self._process_twitter_url(twitter_URL)
        meta_tag_list, code = self._get_meta_tags_from_url_html(twitter_URL)
        if meta_tag_list is None:
            print("Error: no meta tags for " + twitter_URL)
            print("HTML response status code = " + str(code))
            return
        image_URL_list = self._get_image_urls_from_tags(meta_tag_list)
        if len(image_URL_list) == 0:
            print("Tweet has no images: " + twitter_URL)
        else:
            n_downloaded_image = self._download_images_from_image_urls(image_URL_list)
        return n_downloaded_image
    def _process_twitter_url(self, twitter_URL):
        """Method preprocessing the URL string."""
        # Strip whitespace (mainly the \n newline)
        twitter_URL = twitter_URL.rstrip()
        # Transform mobile version of links
        twitter_URL = twitter_URL.replace("mobile.", "")
        return twitter_URL
    def _get_meta_tags_from_url_html(self, twitter_URL):
        """Method getting reponse from URL - using requests which is broken because javascript."""
        #response = requests.get(twitter_URL)

        # Get reponse from URL - using html-requests
        response = self.html_session.get(twitter_URL)

        # Break for this URL because error in request/response
        if response.status_code != 200:
            return None, response.status_code
        # Process HTML from reponse.content
        html_soup = bs4.BeautifulSoup(response.content, 'lxml')
        ### CHANGE TO RETURN HTML SOUP AND RESPONSE ONLY, CAN GET THE TAGS IN ANOTHER METHOD
        meta_tag_list = html_soup.find_all('meta')
        return meta_tag_list, response.status_code
    def _get_image_urls_from_tags(self, meta_tag_list):
        """Method getting the image URL strings."""
        image_URL_list = []
        for tag in meta_tag_list:
            attribute_dict = tag.attrs
            keys = attribute_dict.keys()
            if 'property' in keys:
                property_value = attribute_dict['property']
                if property_value == 'og:image' and 'content' in keys:
                    image_url = attribute_dict['content']
                    if 'jpg:large' in image_url:
                        image_URL_list.append(image_url)
        return image_URL_list
    def _download_images_from_image_urls(self, image_URL_list):
        """Method doing the actual downloading."""
        n_downloaded_image = 0
        for url in image_URL_list:
            # Split URL using / and get image file name
            match_list = re.split('/', url)
            for match in match_list:
                if 'jpg:large' in match:
                    # Leave ':large' out of the file name
                    file_name = match.replace("jpg:large", "jpg")
                    destination_file_name = os.path.join(self.download_path, file_name)
            
            # Check that image file name is not already in destination folder
            if os.path.isfile(destination_file_name):
                print(file_name, "already downloaded")
            else:
                # Get image from URL
                image_response = requests.get(url, stream=True)
                if image_response.status_code != 200:
                    print("Error: response status code = " + str(image_response.status_code) + " for " + url)
                    break
                #print("Downloading", destination_file_name)

                # Write image data to disk
                with open(destination_file_name, 'wb') as f:
                    # Download using the set download chunk size
                    for chunk in image_response.iter_content(self.chunk_size):
                        f.write(chunk)
                n_downloaded_image += 1
        return n_downloaded_image