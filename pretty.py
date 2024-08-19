import os
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QFileDialog, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class CSVSplitTool(QWidget):
    """
    A tool for splitting large CSV files into smaller ones using a GUI built with PyQt5.
    """
    
    def __init__(self):
        """
        Initialize the CSVSplitTool class.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initialize the user interface of the application.
        """
        self.setWindowTitle('CSV Split Tool')
        self.setGeometry(100, 100, 600, 400)  # Increased height to accommodate the image

        layout = QVBoxLayout()

        # Add the image at the top of the GUI
        logo_layout = QHBoxLayout()
        self.logo_label = QLabel(self)
        pixmap = QPixmap('knowbe4logo.svg')
        self.logo_label.setPixmap(pixmap)
        logo_layout.addStretch()
        logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        logo_layout.addStretch()
        layout.addLayout(logo_layout)

        self.source_file_button = QPushButton('Select Source File', self)
        self.source_file_button.clicked.connect(self.find_source_files)
        layout.addWidget(self.source_file_button)

        self.source_file_label = QLabel('Selected File: None', self)
        layout.addWidget(self.source_file_label)

        self.dest_folder_button = QPushButton('Select Destination Folder', self)
        self.dest_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.dest_folder_button)

        self.dest_folder_label = QLabel('Destination Folder: None', self)
        layout.addWidget(self.dest_folder_label)

        self.new_file_name_label = QLabel('File Name Prefix', self)
        layout.addWidget(self.new_file_name_label)

        self.new_file_name_input = QLineEdit(self)
        layout.addWidget(self.new_file_name_input)

        self.record_per_label = QLabel('Entries Per CSV File', self)
        layout.addWidget(self.record_per_label)

        self.record_per_input = QLineEdit(self)
        layout.addWidget(self.record_per_input)

        self.split_csv_button = QPushButton('Split CSV', self)
        self.split_csv_button.clicked.connect(self.split_csv)
        layout.addWidget(self.split_csv_button)

        self.reset_button = QPushButton('RESET', self)
        self.reset_button.clicked.connect(self.reset_fields)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def find_source_files(self):
        """
        Open a file dialog to select a CSV file and update the label with the selected file path.
        """
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select a CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file:
            self.source_file_label.setText(f'Selected File: {file}')

    def select_folder(self):
        """
        Open a directory dialog to select a destination folder and update the label with the selected folder path.
        """
        options = QFileDialog.Options()
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder", options=options)
        if folder:
            self.dest_folder_label.setText(f'Destination Folder: {folder}')

    def split_csv(self):
        """
        Validate inputs and call the method to split the CSV file into smaller files.
        """
        source_filepath = self.source_file_label.text().replace('Selected File: ', '')
        dest_folder = self.dest_folder_label.text().replace('Destination Folder: ', '')
        new_file_prefix = self.new_file_name_input.text()
        try:
            entries_per_file = int(self.record_per_input.text())
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Entries Per CSV File must be an integer.')
            return

        if not source_filepath or not dest_folder or not new_file_prefix:
            QMessageBox.warning(self, 'Error', 'All fields must be filled out.')
            return

        try:
            self.csv_split(source_filepath, dest_folder, new_file_prefix, entries_per_file)
            QMessageBox.information(self, 'Success', 'CSV files split successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def csv_split(self, source_filepath, dest_folder, new_file_prefix, entries_per_file):
        """
        Split the source CSV file into smaller files with the specified number of entries per file.
        
        Parameters:
        source_filepath (str): The path of the source CSV file.
        dest_folder (str): The destination folder to save the smaller CSV files.
        new_file_prefix (str): The prefix for the new smaller CSV files.
        entries_per_file (int): The number of entries per smaller CSV file.
        """
        if entries_per_file <= 0:
            raise ValueError('The file must have one or more entries')

        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)

        with open(source_filepath, 'r') as source:
            reader = csv.reader(source)
            headers = next(reader)

            file_idx = 0
            records_exist = True

            while records_exist:
                i = 0
                target_filename = f'{new_file_prefix}_{file_idx}.csv'
                target_filepath = os.path.join(dest_folder, target_filename)

                with open(target_filepath, 'w', newline='') as target:
                    writer = csv.writer(target)
                    if headers:
                        writer.writerow(headers)

                    while i < entries_per_file:
                        try:
                            writer.writerow(next(reader))
                            i += 1
                        except StopIteration:
                            records_exist = False
                            break

                if i == 0:
                    os.remove(target_filepath)

                file_idx += 1

    def reset_fields(self):
        """
        Reset all input fields and labels to their default state.
        """
        self.source_file_label.setText('Selected File: None')
        self.dest_folder_label.setText('Destination Folder: None')
        self.new_file_name_input.clear()
        self.record_per_input.clear()

if __name__ == '__main__':
    app = QApplication([])
    ex = CSVSplitTool()
    ex.show()
    app.exec_()