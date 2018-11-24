import glob
import os
from pathlib import Path



class DatabaseManager(object):
    """Class controlling images in linked to the database."""
    def __init__(self, image_extension_list=['jpg', 'png']):
        self.image_extension_list = image_extension_list
        base_dir_path = Path(__file__)
        image_dir_path = base_dir_path.joinpath('..', 'images').resolve(strict=True)
        #self.download_dir_path = image_dir_path / 'download'
        #self.load_dir_path = image_dir_path / 'load'
        self.original_dir_path = image_dir_path / 'original'
        self.duplicate_dir_path = image_dir_path / 'duplicate'
        self.resize_dir_path = image_dir_path / 'resize'
        self.face_dir_path = image_dir_path / 'face'
        return
    ### Public methods
    def get_image_glob_list(self, dir_path):
        """Returns a list of images in a given image directory"""
        image_path_list = []
        for image_extension in self.image_extension_list:
            pattern = '*.' + image_extension
            image_path_list.extend(dir_path.glob(pattern))
        return image_path_list
    ### Private methods
    def _asdf(self):
        return


