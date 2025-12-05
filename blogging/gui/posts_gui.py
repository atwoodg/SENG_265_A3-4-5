from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTableView, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import pyqtSignal
from blogging.blog import Blog

class PostGUI(QWidget):
    back_signal = pyqtSignal()

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("POST DASHBOARD"))

        create_button = QPushButton("Create Post")
        layout.addWidget(create_button)

        retrieve_button = QPushButton("Retrieve Post")
        layout.addWidget(retrieve_button)

        update_button = QPushButton("Update Post")
        layout.addWidget(update_button)

        delete_button = QPushButton("Delete Post")
        layout.addWidget(delete_button)

        list_button = QPushButton("List Posts")
        layout.addWidget(list_button)

        back_button = QPushButton("Back To Blogs")
        layout.addWidget(back_button)
        back_button.clicked.connect(self.back_signal.emit)

    #POST OPERATIONS GO HERE#