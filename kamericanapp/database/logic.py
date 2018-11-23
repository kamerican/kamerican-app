import glob
import os


class DatabaseManager(object):
    """Class controlling images in linked to the database."""
    def __init__(self):
        current_directory = os.path.abspath(os.path.dirname(__file__))
        images_directory = os.path.join(current_directory, 'images')
        self.download_directory = os.path.join(images_directory, 'download')
        self.load_directory = os.path.join(images_directory, 'load')
        self.original_directory = os.path.join(images_directory, 'original')
        self.resize_directory = os.path.join(images_directory, 'resize')
        self.face_directory = os.path.join(images_directory, 'face')
        return
    ### Public methods
    def get_n_load_images(self):
        """Return number of images in the load directory."""
        load_image_list = self._get_image_glob_list(self.load_directory)
        return len(load_image_list)
    ### Private methods
    def _get_image_glob_list(self, directory):
        jpg_pattern = os.path.join(directory, '*.jpg')
        jpg_list = glob.glob(pathname=jpg_pattern)
        png_pattern = os.path.join(directory, '*.png')
        png_list = glob.glob(pathname=png_pattern)
        #print("jpg:", len(jpg_list))
        #print("png:", len(png_list))

        return [*jpg_list, *png_list]
        


