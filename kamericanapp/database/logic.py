import cv2
from pathlib import Path, PosixPath



class DatabaseManager(object):
    """Class controlling images in linked to the database."""
    def __init__(self, image_extension_list=['jpg', 'png'], resize_factor=0.25):
        self.image_extension_list = image_extension_list
        self.resize_factor = resize_factor
        base_dir_path = Path(__file__)
        image_dir_path = base_dir_path.joinpath('..', 'images').resolve(strict=True)
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
    def resize_images(self, images_to_resize_query_list):
        for image_to_resize in images_to_resize_query_list:
            # Get original image from image path
            image_path = image_to_resize.filepath_original

            if type(image_path) is PosixPath:
                image_path = self._convert_to_posix_path(image_path)

            original_image = cv2.imread(str(image_path))
            
            # Get resized dimensions
            width = int(original_image.shape[1] * self.resize_factor)
            height = int(original_image.shape[0] * self.resize_factor)
            dim = (width, height)

            # Get resized image and save
            resized_image = cv2.resize(original_image, dim)
            resized_image_path = self.resize_dir_path / "rsz_{}".format(image_path.name)
            if resized_image_path.is_file():
                print("Resized image already exists:", resized_image_path.name)
            else:
                cv2.imwrite(str(resized_image_path), resized_image)
            break
        return 'temp'
    ### Private methods
    def _convert_to_posix_path(self, path):
        '''For non-windows rq workers, change a windows-styled path from the db to an equivalent path for the rq worker.'''        
        # Split the WindowsPath string into the parts
        #parts = path.parts
        parts = str(path).split('\\')[1:]
        return Path('/mnt/c').joinpath(*parts)