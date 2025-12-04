from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt6.QtCore import pyqtSignal
from blogging.blog import Blog

class Dashboard(QWidget):

    clicked_logout = pyqtSignal()

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("BLOG DASHBOARD"))

        #Search for blog operations
        search_blog_button = QPushButton("Search For Blog")
        layout.addWidget(search_blog_button)
        search_blog_button.clicked.connect(self.open_search_blog)

        #Create new blog operations
        create_blog_button = QPushButton("Create New Blog")
        layout.addWidget(create_blog_button)
        create_blog_button.clicked.connect(self.open_create_blog)

        #Retrieve blog operations
        retrieve_blog_button = QPushButton("Retrieve Blog")
        layout.addWidget(retrieve_blog_button)
        retrieve_blog_button.clicked.connect(self.open_retrieve_blog)




        #LOGOUT OPERATIONS
        logout_button = QPushButton("Logout")
        layout.addWidget(logout_button)
        logout_button.clicked.connect(self.clicked_logout.emit)

        #CONTENT
        self.content = QWidget()
        self.content_layout = QVBoxLayout()
        self.content.setLayout(self.content_layout)
        layout.addWidget(self.content)



    def open_search_blog(self):
        self.clear_content()

        search_label = QLabel("Search For Blog")
        key_label = QLabel("Search Key:")
        key_input = QLineEdit()
        search_button = QPushButton("Search")

        self.content_layout.addWidget(search_label)
        self.content_layout.addWidget(key_label)
        self.content_layout.addWidget(key_input)
        self.content_layout.addWidget(search_button)

        search_button.clicked.connect(lambda: self.do_search_blog(key_input.text()))

    def do_search_blog(self, key):
        self.clear_content()

        try:
            blog = self.controller.search_blog(key)

            if blog is not None:
                self.content_layout.addWidget(QLabel(f"ID: {blog.id}"))
                self.content_layout.addWidget(QLabel(f"Name: {blog.name}"))
                self.content_layout.addWidget(QLabel(f"URL: {blog.url}"))
                self.content_layout.addWidget(QLabel(f"Email: {blog.email}"))

            else:
                self.content_layout.addWidget(QLabel(f"No blog found"))

        except Exception as e:
            self.content_layout.addWidget(QLabel(str(e)))

    def open_retrieve_blog(self):
        self.clear_content()

        search_label = QLabel("Retrieve Blog")
        search_string = QLabel("Search string:")
        string_input = QLineEdit()
        retrieve_button = QPushButton("Retrieve")

        self.content_layout.addWidget(search_label)
        self.content_layout.addWidget(search_string)
        self.content_layout.addWidget(string_input)
        self.content_layout.addWidget(retrieve_button)


    def open_create_blog(self):
        self.clear_content()

        create_label = QLabel("Create Blog")

        id_label = QLabel("Blog ID:")
        self.id_input = QLineEdit()

        name_label = QLabel("Blog Name:")
        self.name_input = QLineEdit()

        url_label = QLabel("Blog URL:")
        self.url_input = QLineEdit()

        email_label = QLabel("Blog Email:")
        self.email_input = QLineEdit()

        create_button = QPushButton("Create")

        self.content_layout.addWidget(create_label)
        self.content_layout.addWidget(id_label)
        self.content_layout.addWidget(self.id_input)
        self.content_layout.addWidget(name_label)
        self.content_layout.addWidget(self.name_input)
        self.content_layout.addWidget(url_label)
        self.content_layout.addWidget(self.url_input)
        self.content_layout.addWidget(email_label)
        self.content_layout.addWidget(self.email_input)
        self.content_layout.addWidget(create_button)

        create_button.clicked.connect(lambda: self.do_create_blog())

    def do_create_blog(self):
        self.clear_content()

        try:
            blog = self.controller.create_blog(self.id_input.text(), self.name_input.text(), self.url_input.text(), self.email_input.text())

            self.content_layout.addWidget(QLabel(f"Blog Created"))
            self.content_layout.addWidget(QLabel(f"ID: {blog.id}"))
            self.content_layout.addWidget(QLabel(f"Name: {blog.name}"))
            self.content_layout.addWidget(QLabel(f"URL: {blog.url}"))
            self.content_layout.addWidget(QLabel(f"Email: {blog.email}"))

        except Exception as e:
            self.content_layout.addWidget(QLabel(str(e)))


    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
