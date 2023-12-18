import os
import pytest
from pathlib import Path
from PIL import Image
from binder_jet_convertor import ImageConvertor, StackConvertor 

TEST_IMAGES_DIR = Path('test_image_directory')
TEST_SINGLE_IMAGE_DIR = Path('test_image_single_directory')


class TestImageConvertor:

    def test_init_with_valid_path(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        assert image_convertor.path == image_path

    def test_init_with_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            ImageConvertor(Path('nonexistent_path'))

    def test_open_jpg_image(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        assert isinstance(image_convertor.image, Image.Image)

    def test_open_jpeg_image(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpeg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        assert isinstance(image_convertor.image, Image.Image)

    def test_open_bmp_image(self):
        image_path = TEST_IMAGES_DIR / 'test_image.bmp'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        assert isinstance(image_convertor.image, Image.Image)

    def test_open_png_image(self):
        image_path = TEST_IMAGES_DIR / 'test_image.png'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        assert isinstance(image_convertor.image, Image.Image)

    def test_open_tiff_image(self):
        image_path = TEST_IMAGES_DIR / 'test_image.tiff'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        assert isinstance(image_convertor.image, Image.Image)

    def test_open_tif_image(self):
        image_path = TEST_IMAGES_DIR / 'test_image.tif'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        assert isinstance(image_convertor.image, Image.Image)

    def test_resize(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_width, new_height = 50, 75
        image_convertor.resize(new_width, new_height)
        assert image_convertor.image.size == (new_width, new_height)

    def test_resize_invalid_str(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_width, new_height = 'a', 'b'
        with pytest.raises(TypeError):
            image_convertor.resize(new_width, new_height)

    def test_resize_invalid_negative(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_width, new_height = -50, -50
        width, height = image_convertor.image.size
        with pytest.raises(TypeError):
            image_convertor.resize(new_width, new_height)

    def test_resize_invalid_x(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_width, new_height = -50, 50
        width, height = image_convertor.image.size
        with pytest.raises(TypeError):
            image_convertor.resize(new_width, new_height)

    def test_resize_invalid_y(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_width, new_height = 50, -50
        width, height = image_convertor.image.size
        with pytest.raises(TypeError):
            image_convertor.resize(new_width, new_height)

    def test_resize_default(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        width, height = image_convertor.image.size
        image_convertor.resize()
        assert image_convertor.image.size == (width, height)
        
    def test_bit_depth_1(self):
        bit_dict = {1: '1', 8:'L', 24:'RGB', 32:'RGBA'}
        new_depth = 1
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.convert_image_depth(new_depth)
        assert image_convertor.image.mode == (bit_dict[new_depth])

    def test_bit_depth_8(self):
        bit_dict = {1: '1', 8:'L', 24:'RGB', 32:'RGBA'}
        new_depth = 8
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.convert_image_depth(new_depth)
        assert image_convertor.image.mode == (bit_dict[new_depth])

    def test_bit_depth_24(self):
        bit_dict = {1: '1', 8:'L', 24:'RGB', 32:'RGBA'}
        new_depth = 24
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.convert_image_depth(new_depth)
        assert image_convertor.image.mode == (bit_dict[new_depth])

    def test_bit_depth_32(self):
        bit_dict = {1: '1', 8:'L', 24:'RGB', 32:'RGBA'}
        new_depth = 32
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.convert_image_depth(new_depth)
        assert image_convertor.image.mode == (bit_dict[new_depth])

    def test_bit_depth_invalid_str(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_depth = 'a'
        with pytest.raises(TypeError):
            image_convertor.convert_image_depth(new_depth)

    def test_bit_depth_invalid_negative(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_depth = 50
        with pytest.raises(TypeError):
            image_convertor.convert_image_depth(new_depth)

    def test_bit_depth_default(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        original_mode = image_convertor.image.mode
        image_convertor.convert_image_depth()
        assert image_convertor.image.mode == original_mode

    def test_file_rename(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_filename = 'renamed'
        image_convertor.get_new_file_name(new_filename)
        assert image_convertor.new_file_name == new_filename

    def test_file_rename_invalid_int(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_filename = 2
        with pytest.raises(TypeError):
            image_convertor.get_new_file_name(new_filename)

    def test_file_rename_default(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.get_new_file_name()
        assert image_convertor.new_file_name == 'test_image'

    def test_file_extension_change(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_extension = '.tiff'
        image_convertor.get_new_file_extension(new_extension)
        assert image_convertor.new_file_extension == new_extension

    def test_file_extension_change_invalid_int(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        new_extension = 2
        with pytest.raises(TypeError):
            image_convertor.get_new_file_extension(new_extension)

    def test_file_extension_change_default(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.get_new_file_extension()
        assert image_convertor.new_file_extension == '.jpg'

    def test_save_image(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        image_convertor.open_image()
        image_convertor.save_file()
        expected_output_path = TEST_IMAGES_DIR.parent.parent / 'output' / 'test_image.jpg'
        assert expected_output_path.is_file()
        os.remove(expected_output_path)

    def test_full_converstion(self):
        image_path = TEST_IMAGES_DIR / 'test_image.jpg'
        image_convertor = ImageConvertor(image_path)
        new_width, new_height = 50, 75
        new_depth = 1
        new_filename = 'full_test'
        new_extension = '.tiff'
        expected_name = new_filename + new_extension

        image_convertor.open_image()
        image_convertor.resize(new_width, new_height)
        image_convertor.convert_image_depth(new_depth)
        image_convertor.get_new_file_name(new_filename)
        image_convertor.get_new_file_extension(new_extension)
        image_convertor.save_file()
        expected_output_path = TEST_IMAGES_DIR.parent.parent / 'output' / expected_name

        assert image_convertor.image.size == (new_width, new_height)
        assert image_convertor.image.mode == ('1')
        assert image_convertor.new_file_name == new_filename
        assert image_convertor.new_file_extension == new_extension
        assert expected_output_path.is_file()

        os.remove(expected_output_path)


class TestStackConvertor:

    def test_init_with_valid_path(self):
        stack_convertor = StackConvertor(TEST_IMAGES_DIR, '.tiff', 'output_image')
        assert stack_convertor.path == TEST_IMAGES_DIR

    def test_init_with_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            StackConvertor(Path('nonexistent_path'), '.jpg', 'output_image')

    def test_init_with_file_path(self):
        file_name = 'test_image.bmp'
        with pytest.raises(ValueError):
            StackConvertor(Path(TEST_IMAGES_DIR / file_name), '.jpg', 'output_image')

    def test_init_with_minimum_args(self):
        stack_convertor = StackConvertor(TEST_IMAGES_DIR)
        assert stack_convertor.path == TEST_IMAGES_DIR
        assert stack_convertor.new_file_name_format is None
        assert stack_convertor.new_file_extension is None
        assert stack_convertor.x_dim is None
        assert stack_convertor.y_dim is None
        assert stack_convertor.bit_depth is None
        assert stack_convertor.copies == 1

    def test_init_with_all_args(self):
        stack_convertor = StackConvertor(TEST_IMAGES_DIR, 'Layer', '.tiff', 40,
                                         50, 1, 3)
        assert stack_convertor.path == TEST_IMAGES_DIR
        assert stack_convertor.new_file_name_format == 'Layer'
        assert stack_convertor.new_file_extension == '.tiff'
        assert stack_convertor.x_dim == 40
        assert stack_convertor.y_dim == 50
        assert stack_convertor.bit_depth == 1
        assert stack_convertor.copies == 3

    def test_conv_zero_copies(self):
        with pytest.raises(ValueError):
            StackConvertor(TEST_IMAGES_DIR, copies = 0)

    def test_conv_negative_copies(self):
        with pytest.raises(ValueError):
            StackConvertor(TEST_IMAGES_DIR, copies = -1)

    def test_single_full_conv(self):
        stack_convertor = StackConvertor(TEST_SINGLE_IMAGE_DIR, 'Layer', '.tiff', 40,
                                         50, 1, 1)
        stack_convertor.convert_image_stack()
        expected_name = "Layer_00001.tiff"
        expected_output_path = TEST_IMAGES_DIR.parent.parent / 'output' / expected_name
        assert expected_output_path.is_file()

        output_image = Image.open(expected_output_path)
        assert output_image.size == (40, 50)
        assert output_image.mode == ('1')

        output_image.close()
        os.remove(expected_output_path)

    def test_single_copies_conv(self):
        stack_convertor = StackConvertor(TEST_SINGLE_IMAGE_DIR, 'Layer', '.tiff', 40,
                                         50, 1, 3)
        stack_convertor.convert_image_stack()

        expected_output_dir_path = TEST_IMAGES_DIR.parent.parent / 'output'
        directory = Path(expected_output_dir_path)
        files = [file for file in directory.rglob('*') if file.is_file()]
        assert len(files) == 3

        expected_name_1 = "Layer_00001.tiff"
        expected_name_2 = "Layer_00002.tiff"
        expected_name_3 = "Layer_00003.tiff"
        expected_output_path_1 = TEST_IMAGES_DIR.parent.parent / 'output' / expected_name_1
        expected_output_path_2 = TEST_IMAGES_DIR.parent.parent / 'output' / expected_name_2
        expected_output_path_3 = TEST_IMAGES_DIR.parent.parent / 'output' / expected_name_3
        assert expected_output_path_1.is_file()
        assert expected_output_path_2.is_file()
        assert expected_output_path_3.is_file()

        output_image_1 = Image.open(expected_output_path_1)
        assert output_image_1.size == (40, 50)
        assert output_image_1.mode == ('1')

        output_image_2 = Image.open(expected_output_path_2)
        assert output_image_2.size == (40, 50)
        assert output_image_2.mode == ('1')

        output_image_3 = Image.open(expected_output_path_3)
        assert output_image_3.size == (40, 50)
        assert output_image_3.mode == ('1')

        output_image_1.close()
        os.remove(expected_output_path_1)
        output_image_2.close()
        os.remove(expected_output_path_2)
        output_image_3.close()
        os.remove(expected_output_path_3)
    

    def test_stack_single_conv(self):
        stack_convertor = StackConvertor(TEST_IMAGES_DIR, 'Layer', '.tiff', 40,
                                         50, 1, 1)
        stack_convertor.convert_image_stack()

        expected_output_dir_path = TEST_IMAGES_DIR.parent.parent / 'output'
        directory = Path(expected_output_dir_path)
        files = [file for file in directory.rglob('*') if file.is_file()]
        assert len(files) == 6

        expected_name_1 = "Layer_00001.tiff"
        expected_name_2 = "Layer_00002.tiff"
        expected_name_3 = "Layer_00003.tiff"
        expected_name_4 = "Layer_00004.tiff"
        expected_name_5 = "Layer_00005.tiff"
        expected_name_6 = "Layer_00006.tiff"
        expected_output_path_1 = TEST_IMAGES_DIR.parent.parent / 'output' / expected_name_1
        expected_output_path_2 = TEST_IMAGES_DIR.parent.parent / 'output' / expected_name_2
        expected_output_path_3 = TEST_IMAGES_DIR.parent.parent / 'output' / expected_name_3
        expected_output_path_4 = TEST_IMAGES_DIR.parent.parent / 'output' / expected_name_4
        expected_output_path_5 = TEST_IMAGES_DIR.parent.parent / 'output' / expected_name_5
        expected_output_path_6 = TEST_IMAGES_DIR.parent.parent / 'output' / expected_name_6
        assert expected_output_path_1.is_file()
        assert expected_output_path_2.is_file()
        assert expected_output_path_3.is_file()
        assert expected_output_path_4.is_file()
        assert expected_output_path_5.is_file()
        assert expected_output_path_6.is_file()

        output_image_1 = Image.open(expected_output_path_1)
        assert output_image_1.size == (40, 50)
        assert output_image_1.mode == ('1')

        output_image_2 = Image.open(expected_output_path_2)
        assert output_image_2.size == (40, 50)
        assert output_image_2.mode == ('1')

        output_image_3 = Image.open(expected_output_path_3)
        assert output_image_3.size == (40, 50)
        assert output_image_3.mode == ('1')

        output_image_4 = Image.open(expected_output_path_4)
        assert output_image_4.size == (40, 50)
        assert output_image_4.mode == ('1')

        output_image_5 = Image.open(expected_output_path_5)
        assert output_image_5.size == (40, 50)
        assert output_image_5.mode == ('1')

        output_image_6 = Image.open(expected_output_path_6)
        assert output_image_6.size == (40, 50)
        assert output_image_6.mode == ('1')

        output_image_1.close()
        os.remove(expected_output_path_1)
        output_image_2.close()
        os.remove(expected_output_path_2)
        output_image_3.close()
        os.remove(expected_output_path_3)
        output_image_4.close()
        os.remove(expected_output_path_4)
        output_image_5.close()
        os.remove(expected_output_path_5)
        output_image_6.close()
        os.remove(expected_output_path_6)
