from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QRadioButton
from PyQt6.QtGui import QIntValidator
from pathlib import Path
from binder_jet_convertor import StackConvertor

class ImageConverterController:
    def __init__(self, view):
        self.view = view
        self.view.convert_button.clicked.connect(self.convert_images)

    def convert_images(self):
        path = self.view.selected_directory
        format_name = self.view.format_edit.text()
        extension = self.view.extension_edit.text()
        rename_file_style = self.view.rename_style

        stack_converter = StackConvertor(path, new_file_name_format=format_name,
                                         new_file_extension=extension)
        stack_converter.convert_image_stack()

class ImageConverterView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.controller = ImageConverterController(self)

    def init_ui(self):
        self.setWindowTitle('Image Converter')
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.path_label = QLabel('Path:')
        # self.path_edit = QLineEdit()

        # Directory selection button
        directory_button = QPushButton('Select Directory')
        directory_button.clicked.connect(self.select_directory)

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
        self.bit_depth_1 = QRadioButton('1 Bit')
        self.bit_depth_8 = QRadioButton('8 Bit')
        self.bit_depth_24 = QRadioButton('24 Bit')
        self.bit_depth_32 = QRadioButton('32 Bit')
        self.bit_depth_default = QRadioButton('Keep Original Bit Depth')
        bit_depth_layout.addWidget(self.bit_depth_1)
        bit_depth_layout.addWidget(self.bit_depth_8)
        bit_depth_layout.addWidget(self.bit_depth_24)
        bit_depth_layout.addWidget(self.bit_depth_32)
        bit_depth_layout.addWidget(self.bit_depth_default)
        self.bit_depth_default.setChecked(True)

        # Numerical entry boxes for setting the numbe of copies of each image
        copies_layout = QHBoxLayout()
        self.copy_number_label = QLabel('Number of Copies of Each Image:')
        self.copy_number_entry = QLineEdit()
        self.copy_number_entry.setValidator(QIntValidator())
        self.copy_number_entry.setPlaceholderText('1')
        copies_layout.addWidget(self.copy_number_label)
        copies_layout.addWidget(self.copy_number_entry)

        self.convert_button = QPushButton('Convert')
        self.convert_button.clicked.connect(self.process_selections)

        layout.addWidget(self.path_label)
        layout.addWidget(directory_button)
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

        self.selected_directory = None
        central_widget.setLayout(layout)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.selected_directory = directory

    def process_selections(self):
        directory = self.selected_directory
        if not directory:
            print('Please select a directory first.')
            return

        if self.layer_radio.isChecked():
            self.rename_style = 'Layer'
        elif self.slice_radio.isChecked():
            self.rename_style = 'Slice'
        elif self.default_rename_radio.isChecked():
            self.rename_style = None
        else:
            print('Please select a rename style (Layer, Slice, or keep same name).')
            return

        self.controller.convert_images()


def run_gui():
    app = QApplication([])
    window = ImageConverterView()
    window.show()
    app.exec()

if __name__ == '__main__':
    run_gui()
