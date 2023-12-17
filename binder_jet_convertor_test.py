import os
import pytest
from pathlib import Path
from PIL import Image
from binder_jet_convertor import ImageConvertor, StackConvertor 

TEST_IMAGES_DIR = Path("test_image_directory")

class TestImageConvertor:

    def test_init_with_valid_path(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        assert image_convertor.path == image_path

    def test_init_with_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            ImageConvertor(Path("nonexistent_path"))

    def test_open_jpg_image(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        assert isinstance(image_convertor.image, Image.Image)

    def test_open_jpeg_image(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpeg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        assert isinstance(image_convertor.image, Image.Image)

    def test_open_bmp_image(self):
        image_path = TEST_IMAGES_DIR / "test_image.bmp"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        assert isinstance(image_convertor.image, Image.Image)

    def test_open_png_image(self):
        image_path = TEST_IMAGES_DIR / "test_image.png"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        assert isinstance(image_convertor.image, Image.Image)

    def test_open_tiff_image(self):
        image_path = TEST_IMAGES_DIR / "test_image.tiff"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        assert isinstance(image_convertor.image, Image.Image)

    def test_open_tif_image(self):
        image_path = TEST_IMAGES_DIR / "test_image.tif"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        assert isinstance(image_convertor.image, Image.Image)

    def test_resize(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_width, new_height = 50, 75
        image_convertor.resize(new_width, new_height)
        assert image_convertor.image.size == (new_width, new_height)

    def test_resize_invalid_str(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_width, new_height = "a", "b"
        with pytest.raises(TypeError):
            image_convertor.resize(new_width, new_height)

    def test_resize_invalid_negative(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_width, new_height = -50, -50
        width, height = image_convertor.image.size
        with pytest.raises(TypeError):
            image_convertor.resize(new_width, new_height)

    def test_resize_default(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        width, height = image_convertor.image.size
        image_convertor.resize()
        assert image_convertor.image.size == (width, height)
        
    def test_bit_depth_1(self):
        bit_dict = {1: '1', 8:'L', 24:'RGB', 32:'RGBA'}
        new_depth = 1
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.convert_image_depth(new_depth)
        assert image_convertor.image.mode == (bit_dict[new_depth])

    def test_bit_depth_8(self):
        bit_dict = {1: '1', 8:'L', 24:'RGB', 32:'RGBA'}
        new_depth = 8
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.convert_image_depth(new_depth)
        assert image_convertor.image.mode == (bit_dict[new_depth])

    def test_bit_depth_24(self):
        bit_dict = {1: '1', 8:'L', 24:'RGB', 32:'RGBA'}
        new_depth = 24
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.convert_image_depth(new_depth)
        assert image_convertor.image.mode == (bit_dict[new_depth])

    def test_bit_depth_32(self):
        bit_dict = {1: '1', 8:'L', 24:'RGB', 32:'RGBA'}
        new_depth = 32
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.convert_image_depth(new_depth)
        assert image_convertor.image.mode == (bit_dict[new_depth])

    def test_bit_depth_invalid_str(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_depth = 'a'
        with pytest.raises(TypeError):
            image_convertor.convert_image_depth(new_depth)

    def test_bit_depth_invalid_negative(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_depth = 50
        with pytest.raises(TypeError):
            image_convertor.convert_image_depth(new_depth)

    def test_bit_depth_default(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        original_mode = image_convertor.image.mode
        image_convertor.convert_image_depth()
        assert image_convertor.image.mode == original_mode

    def test_file_rename(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_filename = "renamed"
        image_convertor.get_new_file_name(new_filename)
        assert image_convertor.new_file_name == new_filename

    def test_file_rename_invalid_int(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_filename = 2
        with pytest.raises(TypeError):
            image_convertor.get_new_file_name(new_filename)

    def test_file_rename_default(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.get_new_file_name()
        assert image_convertor.new_file_name == "test_image"

    def test_file_extension_change(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_extension = ".tiff"
        image_convertor.get_new_file_extension(new_extension)
        assert image_convertor.new_file_extension == new_extension

    def test_file_extension_change_invalid_int(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_extension = 2
        with pytest.raises(TypeError):
            image_convertor.get_new_file_extension(new_extension)

    def test_file_extension_change_default(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.get_new_file_extension()
        assert image_convertor.new_file_extension == ".jpg"

    def test_save_image(self):
        image_path = TEST_IMAGES_DIR / "test_image.jpg"
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.save_file()
        expected_output_path = TEST_IMAGES_DIR.parent.parent / 'output' / 'test_image.jpg'
        assert expected_output_path.is_file()
        os.remove(expected_output_path)

class TestStackConvertor:

    def test_init_with_valid_path(self):
        stack_convertor = StackConvertor(TEST_IMAGES_DIR, ".jpg", "output_image")
        assert stack_convertor.path == TEST_IMAGES_DIR

    def test_init_with_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            StackConvertor(Path("nonexistent_path"), ".jpg", "output_image")
