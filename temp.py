import bs4
import requests
from requests_html import HTMLSession
import re
import time
from pathlib import Path
from redis import Redis
from rq import get_current_job

class ImageDownloader(object):
    """Class handling downloading images from URLs."""
    def __init__(self, chunk_size=1024):
        base_dir_path = Path(__file__)
        self.download_dir_path = base_dir_path.parent.resolve() / 'kamericanapp' / 'database' / 'images' / 'duplicate'
        #print(self.download_dir_path.is_dir())
        self.chunk_size = chunk_size
        self.html_session = HTMLSession()
        return
    ### Public methods
    def download_from_list_of_urls(self, url_list):
            n_downloaded_image_total = 0
            n_link = len(url_list)
            for url in url_list:
                n_downloaded_image_total += self._download_from_url(url)
            print("Downloaded:", n_downloaded_image_total)
            return
    ### Private methods
    def _download_from_url(self, url):
        """Private main method."""       
        url = self._process_url(url)
        img_tag_list, code = self._get_meta_tags_from_url_html(url)
        if img_tag_list is None:
            print("Error: no img tags for " + url)
            print("HTML response status code = " + str(code))
            return
        image_url_list, image_name_list = self._get_image_urls_from_tags(img_tag_list)
        print(len(image_url_list))

        if len(image_url_list) == 0:
            print("Link has no images: " + url)
        else:
            n_downloaded_image = self._download_images_from_image_urls(image_url_list, image_name_list)
        return n_downloaded_image
    def _process_url(self, url):
        """Method preprocessing the URL string."""
        # Strip whitespace (mainly the \n newline)
        url = url.rstrip()
        # Transform mobile version of links
        url = url.replace("mobile.", "")
        return url
    def _get_meta_tags_from_url_html(self, url):
        """Method getting reponse from URL - using requests which is broken because javascript."""
        # Get reponse from URL - using html-requests
        response = self.html_session.get(url)

        # Break for this URL because error in request/response
        if response.status_code != 200:
            return None, response.status_code

        # Process HTML from reponse.content
        html_soup = bs4.BeautifulSoup(response.content, 'lxml')
        ### CHANGE TO RETURN HTML SOUP AND RESPONSE ONLY, CAN GET THE TAGS IN ANOTHER METHOD
        img_tag_list = html_soup.find_all('img')
        return img_tag_list, response.status_code
    def _get_image_urls_from_tags(self, img_tag_list):
        """Method getting the image URL strings."""
        image_url_list = []
        image_name_list = []
        for tag in img_tag_list:
            attribute_dict = tag.attrs
            if 'onclick' in attribute_dict:
                image_string = attribute_dict['onclick']
                image_string_split = image_string.split('\'')
                #print(image_string_split[1])
                image_url_list.append(image_string_split[1])

                image_name_list.append(attribute_dict['filename'])
        return image_url_list, image_name_list
    def _download_images_from_image_urls(self, image_url_list, image_name_list):
        """Method doing the actual downloading."""
        n_downloaded_image = 0
        for index in range(len(image_url_list)):
            url = image_url_list[index]
            filename = image_name_list[index]
            download_file_path = self.download_dir_path / filename

            #print(download_file_path, type(download_file_path))
            

            # Check that image file name is not already in destination folder
            if download_file_path.is_file():
                print("Already downloaded:", download_file_path.name)
                pass
            else:
                # Get image from URL
                image_response = requests.get(url, stream=True)
                if image_response.status_code != 200:
                    print("Error: response status code = " + str(image_response.status_code) + " for " + url)
                    break
                # Write image data to disk
                with download_file_path.open(mode='wb') as f:
                    # Download using the set download chunk size
                    for chunk in image_response.iter_content(self.chunk_size):
                        f.write(chunk)
                n_downloaded_image += 1
                time.sleep(3)
        return n_downloaded_image

if __name__ == "__main__":
    obj = ImageDownloader()
    with open(file=Path('links.txt'), mode='r', newline='') as f:
        url_list = f.readlines()
    print(url_list)
    obj.download_from_list_of_urls(url_list)