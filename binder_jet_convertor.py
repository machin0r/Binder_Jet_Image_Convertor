
"""
Binder Jet image convertor functions
"""


from pathlib import Path
from PIL import Image


class ImageConvertor:
    """
    A single image file that will have transformation applied
    """

    def __init__(self, path: Path):
        self.path = path

        if not self.path.exists():
            raise FileNotFoundError(f'The specified path does not exist: {self.path}')

        self.file_name = self.path.stem
        self.file_extension = self.path.suffix
        self.new_file_name = self.path.stem
        self.new_file_extension = self.path.suffix

    def open_image(self):
        """
        Creates a PIL object of the image
        """
        self.image = Image.open(self.path)

    def resize(self, x_dim: int = None, y_dim: int = None):
        """
        Resize the image to the specified x and y in pixels
        If no argument is passed, it uses the current x and y dimensions
        of the image
        """

        width, height = self.image.size
        if x_dim is None:
            x_dim = width
        if y_dim is None:
            y_dim = height

        if not isinstance(x_dim, (int)) or x_dim <= 0:
            raise TypeError('X dimension must be a positive non-zero number')

        if not isinstance(y_dim, (int)) or y_dim <= 0:
            raise TypeError('Y dimension must be a positive non-zero number')

        self.image = self.image.resize((x_dim, y_dim))

    def convert_image_depth(self, bit_depth: int = None):
        """
        Converts the image to the specified depth
        If no argument is passed, the mode of the original image is used
        """

        if bit_depth is None:
            conversion_argument = self.image.mode
            self.image = self.image.convert(conversion_argument)
            return

        bit_dict = {1: '1', 8: 'L', 24: 'RGB', 32: 'RGBA'}
        if bit_depth in bit_dict:
            conversion_argument = bit_dict[bit_depth]
        else:
            raise TypeError(
        """Invalid mode. Only 1 (B&W), 8 (8-bit pixels, B&W),
                            24 (24-bit, true colour), or 32 (32-bit,
                            true colour with transparency) is allowed.
        """
        )

        self.image = self.image.convert(conversion_argument)

    def get_new_file_name(self, file_name: str = None):
        """
        Changes the file name to the passed argument
        If blank, the file name stays the same
        """
        if file_name is None:
            file_name = self.file_name

        if not isinstance(file_name, str):
            raise TypeError('File name must be a string')

        self.new_file_name = file_name

    def get_new_file_extension(self, file_extension: str = None):
        """
        Changes the file name to the passed argument
        If blank, the file name stays the same
        """
        if file_extension is None:
            file_extension = self.file_extension

        if not isinstance(file_extension, str):
            raise TypeError('File extension must be a string')

        self.new_file_extension = file_extension

    def save_file(self):
        """
        Saves the file to the higher directory in a folder called Output
        """

        output_directory = self.path.parent.parent / 'output'

        output_directory.mkdir(parents=True, exist_ok=True)

        full_new_file_path = self.new_file_name + self. new_file_extension

        self.image.save(output_directory / full_new_file_path)


class StackConvertor:
    """
    Collects the image stack from the specified location, and then converts
    each in turn by creating an ImageConvertor object
    Default number of copies is 1, this can be increased for more images
    """
        

    def __init__(self, path: str, new_file_name_format: str = None,
                 new_file_extension: str = None, x_dim: int = None,
                 y_dim: int = None, bit_depth: int = None, copies: int = 1):
        self.path = Path(path)
        self.new_file_name_format = new_file_name_format
        self.new_file_extension = new_file_extension
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.bit_depth = bit_depth
        self.copies = copies

        if not self.path.exists():
            raise FileNotFoundError(
                f'The specified path does not exist: {
                    self.path}')

        if not self.path.is_dir():
            raise ValueError(f'{self.path} is not a valid directory.')

        if not isinstance(copies, (int)) or copies <= 0:
            raise ValueError('Copies must be a positive, non-zero integer')

    def convert_image_stack(self):
        """
        Runs through the specified folder, converting each image and saving
        it as it goes
        """

        layer_number = 1

        for file_path in self.path.iterdir():
            if file_path.is_file():
                for copy_number in range(0, self.copies):
                    if self.new_file_name_format is not None:
                        new_file_name = self.new_file_name_format + \
                            '_' + str(layer_number).zfill(5)
                    else:
                        new_file_name = None
                    image_conversion = ImageConvertor(file_path)
                    image_conversion.open_image()
                    if self.x_dim is not None or self.y_dim is not None:
                        image_conversion.resize(self.x_dim, self.y_dim)
                    if self.bit_depth is not None:
                        image_conversion.convert_image_depth(self.bit_depth)
                    image_conversion.get_new_file_name(new_file_name)
                    image_conversion.get_new_file_extension(
                        self.new_file_extension)
                    image_conversion.save_file()
                    layer_number += 1
