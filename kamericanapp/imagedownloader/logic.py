import bs4
import requests
from requests_html import HTMLSession
import re
import os
import time

from kamericanapp import db
from kamericanapp.database.models import RQJob

class ImageDownloader(object):
    def __init__(self, chunk_size=1024):
        working_directory = os.getcwd()
        #dirname = os.path.dirname(__file__)

        self.download_path = os.path.join(working_directory, 'kamericanapp', 'database', 'images', 'download')
        #self.download_path = os.path.join('..', 'database', 'images', 'download')
        #print(self.download_path)

        self.chunk_size = chunk_size
        self.html_session = HTMLSession()
        return
    ### Main methods
    def DownloadFromListOfTwitterURLs(self, twitter_URL_list):
        for twitter_URL in twitter_URL_list:
            self.DownloadFromTwitterURL(twitter_URL)

        #time_start = time.time()
        #time_end = time.time()
        #print("Wrote " + str(total_number_of_images) + " images to disk.")
        #print("Process took " + str(time_end - time_start) + " seconds.")
        return
    def DownloadFromTwitterURL(self, twitter_URL):
        twitter_URL = self._ProcessTwitterURL(twitter_URL)

        meta_tag_list, code = self._GetMetaTagsFromURLHTML(twitter_URL)
        
        if meta_tag_list is None:
            print("Error: no meta tags for " + twitter_URL)
            print("HTML response status code = " + str(code))
            return
        #print(meta_tag_list)
        image_URL_list = self._GetImageURLsFromTags(meta_tag_list)
        
        if len(image_URL_list) == 0:
            print("Tweet has no images: " + twitter_URL)
        else:
            self._DownloadImagesFromImageURLs(image_URL_list)
        return
    ### Helper methods
    def _ProcessTwitterURL(self, twitter_URL):
        # Strip whitespace (mainly the \n newline)
        twitter_URL = twitter_URL.rstrip()
        # Transform mobile version of links
        twitter_URL = twitter_URL.replace("mobile.", "")
        return twitter_URL
    def _GetMetaTagsFromURLHTML(self, twitter_URL):
        # Get reponse from URL - using requests which is broken because javascript
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
    def _GetImageURLsFromTags(self, meta_tag_list):
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
    def _DownloadImagesFromImageURLs(self, image_URL_list):
        for url in image_URL_list:
            # Split URL using / and get image file name
            match_list = re.split('/', url)
            for match in match_list:
                if 'jpg:large' in match:
                    # Leave ':large' out of the file name
                    file_name = match.replace("jpg:large", "jpg")
                    #print("Downloading: " + file_name)
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
                #self.total_number_of_images += 1
                #print("Downloading", destination_file_name)

                # Write image data to disk
                with open(destination_file_name, 'wb') as f:
                    # Download using the set download chunk size
                    for chunk in image_response.iter_content(self.chunk_size):
                        f.write(chunk)
        return

    def tempfunc(self):
        job = RQJob()
        n = 10
        for i in range(1, n + 1):
            percentage = i/n*100
            print(percentage)
            time.sleep(3)
        return