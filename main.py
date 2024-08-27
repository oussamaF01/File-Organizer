import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt ,QSize

import webbrowser

class FileOrganizerUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 800, 600)

        # Main widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Main layout
        main_layout = QHBoxLayout()
        self.main_widget.setLayout(main_layout)

        # Sidebar layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)
        self.setWindowIcon(QIcon("icon/pngegg.ico"))
        self.select_folder_path = None

        # Profile picture and user info
        profile_pic = QLabel(self)
        icon_path = "img/avataaars.png"
        if os.path.isfile(icon_path):
            profile_pic.setPixmap(QPixmap(icon_path).scaled(100, 100, Qt.KeepAspectRatio))
        else:
            profile_pic.setText("Profile Pic Missing")
        profile_name = QLabel("Oussama Farhani")
        profile_username = QLabel("@Oussama_Farhani")

        # Social media buttons
        self.btn_linkedin = QPushButton("LinkedIn")
        self.btn_git = QPushButton("GitHub")
        self.btn_linkedin.setIcon(QIcon("img/linkedin.png"))
        self.btn_git.setIcon(QIcon("img/github.png"))
        self.btn_linkedin.clicked.connect(self.open_linkedin)
        self.btn_git.clicked.connect(self.open_github)
        self.btn_git.setStyleSheet("""
            QPushButton {
        background-color: #333;
        color: white;
        border-radius: 5px;
        padding: 5px 10px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #24292e;
    }
    QPushButton:pressed {
        background-color: #1b1f23;
    }
        """)
        self.btn_linkedin.setStyleSheet("""
            QPushButton {
                background-color: #0e76a8;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b5c82;
            }
            QPushButton:pressed {
                background-color: #083c54;
            }
        """)
        sidebar_layout.addWidget(profile_pic, alignment=Qt.AlignCenter)
        sidebar_layout.addWidget(profile_name, alignment=Qt.AlignCenter)
        sidebar_layout.addWidget(profile_username, alignment=Qt.AlignCenter)
        sidebar_layout.addWidget(self.btn_linkedin, alignment=Qt.AlignCenter)
        sidebar_layout.addWidget(self.btn_git, alignment=Qt.AlignCenter)
        sidebar_layout.addStretch(1)  # Pushes profile info and buttons to the top

        # Adding Sidebar title
        sidebar_layout.addWidget(QLabel("FILE MANAGER"), alignment=Qt.AlignCenter)

        # Create a layout for buttons
        button_layout = QVBoxLayout()
        button_width = 150
        self.btn_select = QPushButton("Select Folder")
        self.btn_organize = QPushButton("Organize")
        self.btn_select.setFixedWidth(button_width)
        self.btn_organize.setFixedWidth(button_width)
        self.btn_select.setIcon(QIcon("img/file-and-folder.png"))
        self.btn_organize.setIcon(QIcon("img/organiser.png"))

        self.btn_select.clicked.connect(self.select_folder)
        self.btn_organize.clicked.connect(self.organize_files)
        # Style the Select Folder and Organize buttons
        self.btn_select.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #397d3a;
            }
        """)
        self.btn_organize.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #007bb5;
            }
            QPushButton:pressed {
                background-color: #005f87;
            }
        """)
        button_layout.addWidget(self.btn_select, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.btn_organize, alignment=Qt.AlignCenter)

        sidebar_layout.addLayout(button_layout)

        main_layout.addLayout(sidebar_layout, 1)

        # Folders and Storage details layout
        self.folders_layout = QVBoxLayout()

        # Header for Folders
        header_label = QLabel("Your Folders Stats")
        header_label.setFixedHeight(100)
        self.folders_layout.addWidget(header_label, alignment=Qt.AlignCenter)

        # Add folder buttons
        self.folders_grid_layout = QHBoxLayout()  # Use QHBoxLayout for horizontal alignment

        self.folder_buttons = {}
        folder_names = ["Images", "Video", "Documents", "Audio", "Archives", "Others"]
        icon_paths = {
            "Images": "img/images.png",
            "Video": "img/marketing-video.png",
            "Documents": "img/fichier-pdf.png",
            "Audio": "img/lecteur-de-musique.png",
            "Archives": "img/format-rar.png",
            "Others": "img/pensez-autrement.png"
        }

        for name in folder_names:
            folder_button = QPushButton(f"{name}\n0 Items")
            folder_button.setFixedSize(120, 80)
            folder_button.setStyleSheet("""
                QPushButton {
                    background-color: #f5f5f5;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 14px;
                    font-weight: bold;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)

            # Set the icon for the folder button
            if name in icon_paths:
                folder_button.setIcon(QIcon(icon_paths[name]))
                folder_button.setIconSize(QSize(32, 32))  # Adjust the size as needed

            self.folder_buttons[name] = folder_button
            self.folders_grid_layout.addWidget(folder_button, alignment=Qt.AlignCenter)

        self.folders_layout.addLayout(self.folders_grid_layout)
        self.folders_layout.addStretch(1)  # Pushes folder buttons to the top

        # Adding to the main layout
        main_layout.addLayout(self.folders_layout, 2)

        self.show()

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.select_folder_path = folder_path
            self.update_folder_stats()

    def update_folder_stats(self):
        if self.select_folder_path:
            file_types = {
                'Video': ['.mp4', '.mkv', '.avi'],
                'Audio': ['.mp3', '.wav', '.aac'],
                'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
                'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
                'Archives': ['.zip', '.rar', '.tar', '.gz'],
                'Scripts': ['.py', '.js', '.html', '.css'],
                'Executables': ['.exe', '.bat', '.sh'],
                'Others': []
            }

            # Initialize counts
            counts = {key: 0 for key in file_types.keys()}

            # Scan directory
            for filename in os.listdir(self.select_folder_path):
                file_path = os.path.join(self.select_folder_path, filename)
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)
                    ext = ext.lower()  # Convert extension to lowercase

                    found = False
                    for folder, extensions in file_types.items():
                        if ext in extensions:
                            counts[folder] += 1
                            found = True
                            break

                    if not found:
                        counts['Others'] += 1

            # Update button texts
            for folder, count in counts.items():
                button = self.folder_buttons.get(folder)
                if button:
                    button.setText(f"{folder}\n{count} Items")

    def organize_files(self):
        file_types = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
            'Audio': ['.mp3', '.wav', '.aac'],
            'Video': ['.mp4', '.mkv', '.avi'],
            'Archives': ['.zip', '.rar', '.tar', '.gz'],
            'Scripts': ['.py', '.js', '.html', '.css'],
            'Executables': ['.exe', '.bat', '.sh'],
            'Others': []
        }

        if self.select_folder_path:
            directory = self.select_folder_path

            # Create folders if they don't exist
            for folder in file_types.keys():
                folder_path = os.path.join(directory, folder)
                if not os.path.exists(folder_path):
                    try:
                        os.makedirs(folder_path)
                    except Exception as e:
                        self.show_message(f"Error creating folder {folder}: {e}")
                        return

            # Organize files
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)

                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)
                    moved = False

                    for folder, extensions in file_types.items():
                        if ext.lower() in extensions:
                            try:
                                shutil.move(file_path, os.path.join(directory, folder, filename))
                                moved = True
                                break
                            except Exception as e:
                                self.show_message(f"Error moving file {filename}: {e}")
                                return

                    if not moved:
                        try:
                            shutil.move(file_path, os.path.join(directory, 'Others', filename))
                        except Exception as e:
                            self.show_message(f"Error moving file {filename} to 'Others': {e}")

            self.show_message("Files have been organized")
        else:
            self.show_message("No folder selected")

    def show_message(self, message):
        QMessageBox.information(self, "Information", message)

    def open_linkedin(self):
        webbrowser.open("https://www.linkedin.com/in/oussama-farhani-23ba13306/")

    def open_github(self):
        webbrowser.open("https://github.com/oussamaF01")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerUI()
    sys.exit(app.exec_())
