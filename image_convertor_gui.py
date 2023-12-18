'''
GUI and controller for the binder jet convertor program
'''

from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QRadioButton, QButtonGroup, QListWidget, QListWidgetItem, QScrollArea
from PyQt6.QtGui import QIntValidator, QPixmap
from PyQt6.QtCore import Qt
from binder_jet_convertor import StackConvertor

class ImageConverterController:
    '''Controller that passes information between the view and model for the 
    image conversion'''
    def __init__(self, view):
        self.view = view

    def convert_images(self):
        '''Passes the variables that are set in the view through to the 
        model function to start converting images'''
        path = self.view.selected_directory
        rename_file_style = self.view.rename_style
        new_file_extension = self.view.file_extension
        x_dim_resize = self.view.x_dimension_resize
        y_dim_resize = self.view.y_dimension_resize
        bit_depth = self.view.bit_depth
        copies = self.view.copies

        stack_converter = StackConvertor(path, new_file_name_format=rename_file_style,
                                         new_file_extension=new_file_extension,
                                         x_dim=x_dim_resize, y_dim=y_dim_resize,
                                         bit_depth=bit_depth, copies=copies)
        stack_converter.convert_image_stack()

class ImageConverterView(QMainWindow):
    '''PyQt GUI class for displaying the main conversion window
    Stores the entered user information, and allows the user to change the
    directory and converstion settings'''
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.controller = ImageConverterController(self)        

    def init_ui(self):
        '''GUI layout'''
        self.setWindowTitle('Image Converter')
        self.setGeometry(100, 100, 700, 500)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.path_label = QLabel('Path:')

        # Directory selection button
        directory_button = QPushButton('Select Directory')
        directory_button.clicked.connect(self.select_directory)

        # Buttons to autofill presets for Xaar and Meteor systems
        self.preset_label = QLabel('Presets')
        xaar_preset_button = QPushButton('Xaar XPM')
        xaar_preset_button.clicked.connect(self.load_xaar_presets)
        meteor_preset_button = QPushButton('Meteor HDC')
        meteor_preset_button.clicked.connect(self.load_meteor_presets)

        self.name_format_label = QLabel('File Name Style:')
        # Radio buttons for selecting layer rename format
        rename_button_layout = QHBoxLayout()
        self.layer_radio = QRadioButton('Layer')
        self.slice_radio = QRadioButton('Slice')
        self.default_rename_radio = QRadioButton('Keep Original Name Style')
        rename_button_layout.addWidget(self.layer_radio)
        rename_button_layout.addWidget(self.slice_radio)
        rename_button_layout.addWidget(self.default_rename_radio)
        self.default_rename_radio.setChecked(True)
        # Add radio buttons to their button group
        self.rename_radio_group = QButtonGroup(self)
        self.rename_radio_group.addButton(self.layer_radio)
        self.rename_radio_group.addButton(self.slice_radio)
        self.rename_radio_group.addButton(self.default_rename_radio)
        self.process_file_rename_style(self.default_rename_radio)  # Run to set default value
        self.rename_radio_group.buttonClicked.connect(self.process_file_rename_style)

        self.extension_label = QLabel('File Extension:')
        # Radio buttons for selecting file extension
        extension_button_layout = QHBoxLayout()
        self.png_radio = QRadioButton('.png')
        self.bmp_radio = QRadioButton('.bmp')
        self.tif_radio = QRadioButton('.tif')
        self.default_extension_radio = QRadioButton('Keep Original Extension')
        extension_button_layout.addWidget(self.png_radio)
        extension_button_layout.addWidget(self.bmp_radio)
        extension_button_layout.addWidget(self.tif_radio)
        extension_button_layout.addWidget(self.default_extension_radio)
        self.default_extension_radio.setChecked(True)
        # Add radio buttons to their button group
        self.format_radio_group = QButtonGroup(self)
        self.format_radio_group.addButton(self.png_radio)
        self.format_radio_group.addButton(self.bmp_radio)
        self.format_radio_group.addButton(self.tif_radio)
        self.format_radio_group.addButton(self.default_extension_radio)
        self.process_file_extension(self.default_extension_radio)  # Run to set default value
        self.format_radio_group.buttonClicked.connect(self.process_file_extension)

        self.resize_label = QLabel('Resize')
        # Numerical entry boxes for resizing the images
        resize_entry_layout = QHBoxLayout()
        self.x_dim_label = QLabel('X Dimension (px):')
        self.x_dim_entry = QLineEdit()
        self.x_dim_entry.setValidator(QIntValidator())
        self.y_dim_label = QLabel('Y Dimension (px):')
        self.y_dim_entry = QLineEdit()
        self.y_dim_entry.setValidator(QIntValidator())
        resize_entry_layout.addWidget(self.x_dim_label)
        resize_entry_layout.addWidget(self.x_dim_entry)
        resize_entry_layout.addWidget(self.y_dim_label)
        resize_entry_layout.addWidget(self.y_dim_entry)

        self.bit_depth_label = QLabel('Bit Depth:')
        # Radio buttons for selecting bit depth
        bit_depth_layout = QHBoxLayout()
        self.bit_depth_1 = QRadioButton('1')
        self.bit_depth_8 = QRadioButton('8')
        self.bit_depth_24 = QRadioButton('24')
        self.bit_depth_32 = QRadioButton('32')
        bit_depth_default = QRadioButton('Keep Original Bit Depth')
        bit_depth_layout.addWidget(self.bit_depth_1)
        bit_depth_layout.addWidget(self.bit_depth_8)
        bit_depth_layout.addWidget(self.bit_depth_24)
        bit_depth_layout.addWidget(self.bit_depth_32)
        bit_depth_layout.addWidget(bit_depth_default)
        bit_depth_default.setChecked(True)
        # Add radio buttons to their button group
        self.bit_depth_radio_group = QButtonGroup(self)
        self.bit_depth_radio_group.addButton(self.bit_depth_1)
        self.bit_depth_radio_group.addButton(self.bit_depth_8)
        self.bit_depth_radio_group.addButton(self.bit_depth_24)
        self.bit_depth_radio_group.addButton(self.bit_depth_32)
        self.bit_depth_radio_group.addButton(bit_depth_default)
        self.process_bit_depth(bit_depth_default)  # Run to set default value
        self.bit_depth_radio_group.buttonClicked.connect(self.process_bit_depth)

        # Numerical entry box for setting the number of copies of each image
        copies_layout = QHBoxLayout()
        self.copy_number_label = QLabel('Number of Copies of Each Image:')
        self.copy_number_entry = QLineEdit()
        self.copy_number_entry.setValidator(QIntValidator())
        self.copy_number_entry.setPlaceholderText('1')
        copies_layout.addWidget(self.copy_number_label)
        copies_layout.addWidget(self.copy_number_entry)

        # Button to run the conversion with the selected settings
        self.convert_button = QPushButton('Convert')
        self.convert_button.clicked.connect(self.process_selections)

        layout.addWidget(self.path_label)
        layout.addWidget(directory_button)
        layout.addWidget(self.preset_label)
        layout.addWidget(xaar_preset_button)
        layout.addWidget(meteor_preset_button)
        layout.addWidget(self.name_format_label)
        layout.addLayout(rename_button_layout)
        layout.addWidget(self.extension_label)
        layout.addLayout(extension_button_layout)
        layout.addWidget(self.resize_label)
        layout.addLayout(resize_entry_layout)
        layout.addWidget(self.bit_depth_label)
        layout.addLayout(bit_depth_layout)
        layout.addLayout(copies_layout)

        layout.addWidget(self.convert_button)

        # Create a scrollable area for showing the thumbnails of the images
        thumbnail_layout = QVBoxLayout()
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.thumbnail_list = QListWidget()
        scroll_area.setWidget(self.thumbnail_list)
        thumbnail_layout.addWidget(scroll_area)
        self.selected_directory = None

        central_layout = QHBoxLayout()
        central_layout.addLayout(layout)
        central_layout.addLayout(thumbnail_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)


    def select_directory(self):
        '''Asks ths user to select a directory, and then sets the variable 
        self.selected_directory the chosen string
        Runs updated_thumbnail_list() to populate the stack display on the right
        of the interface'''
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.selected_directory = directory
        self.path_label.setText(f'Path: {directory}')
        self.update_thumbnail_list()

    def update_thumbnail_list(self):
        '''Updates the list of thumbnails from the selected folder,
        accepts png, bmp, tif, tiff, jpg, and jpeg images'''
        self.thumbnail_list.clear()

        if self.selected_directory:
            image_files = list(Path(self.selected_directory).glob('*.png')) + \
                            list(Path(self.selected_directory).glob('*.bmp')) + \
                            list(Path(self.selected_directory).glob('*.tif')) + \
                            list(Path(self.selected_directory).glob('*.tiff')) + \
                            list(Path(self.selected_directory).glob('*.jpg')) + \
                            list(Path(self.selected_directory).glob('*.jpeg'))

            for image_file in image_files:
                pixmap = QPixmap(str(image_file))
                thumbnail = QLabel(self)
                thumbnail.setPixmap(pixmap.scaled(100, 200,
                                                  aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))

                # Create a new widget for each thumbnail and add it to the list widget
                item = QListWidgetItem(self.thumbnail_list)
                item.setSizeHint(thumbnail.sizeHint())
                self.thumbnail_list.addItem(item)
                self.thumbnail_list.setItemWidget(item, thumbnail)

    def load_xaar_presets(self):
        '''Automatically selects the correct parameters for the Xaar XPM system'''
        self.layer_radio.setChecked(True)
        self.bmp_radio.setChecked(True)
        self.bit_depth_8.setChecked(True)

    def load_meteor_presets(self):
        '''Automatically selects the correct parameters for the Meteor HDC system
        Currently picks 1 bit depth.'''
        self.layer_radio.setChecked(True)
        self.tif_radio.setChecked(True)
        self.bit_depth_1.setChecked(True)

    def process_selections(self):
        '''Processes each of the selections in turn, setting the variables to the 
        users choice, then calls the controll '''
        directory = self.selected_directory
        if not directory:
            print('Please select a directory first.')
            return

        self.x_dimension_resize = self.process_x_dim()
        self.y_dimension_resize = self.process_y_dim()
        self.copies = self.process_copy_entry()
        self.controller.convert_images()

    def process_file_rename_style(self, button: QPushButton):
        '''Determines what radio button the user has checked, and sets the
        variable self.rename_style equal to the button text
        This will be the image naming style
        Called when the user changes the radio button selection'''
        if button.text() == 'Keep Original Name Style':
            self.rename_style = None
            return
        self.rename_style = button.text()

    def process_file_extension(self, button: QPushButton):
        '''Determines what radio button the user has checked, and sets the
        variable self.file_extension equal to the button text
        This will be the image extension
        Called when the user changes the radio button selection'''
        if button.text() == 'Keep Original Extension':
            self.file_extension = None
            return
        self.file_extension = button.text()

    def process_x_dim(self) -> int | None:
        '''Gets the user entry for the X resize dimension from the text entry box
        Converts the input to an int
        If empty, passes None'''
        if self.x_dim_entry.text():
            x_dim = int(self.x_dim_entry.text())
        else:
            x_dim = None
        return x_dim

    def process_y_dim(self) -> int | None:
        '''Gets the user entry for the Y resize dimension from the text entry box
        Converts the input to an int
        If empty, passes None'''
        if self.y_dim_entry.text():
            y_dim = int(self.y_dim_entry.text())
        else:
            y_dim = None
        return y_dim

    def process_bit_depth(self, button: QPushButton):
        '''Determines what radio button the user has checked, and sets the
        variable self.bit_depth equal to the button text
        This will be the bit depth of the image
        Called when the user changes the radio button selection'''
        if button.text() == 'Keep Original Bit Depth':
            self.bit_depth = None
            return
        self.bit_depth = int(button.text())

    def process_copy_entry(self) -> int:
        '''Gets the user entry for the number of copies from the text entry box
        Converts the input to an int
        If empty, passes None'''
        if self.copy_number_entry.text():
            copies = int(self.copy_number_entry.text())
        else:
            copies = 1
        return copies


def run_gui():
    '''Main function to run the program'''
    app = QApplication([])
    window = ImageConverterView()
    window.show()
    app.exec()

if __name__ == '__main__':
    run_gui()
