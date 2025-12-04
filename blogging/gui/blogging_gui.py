import sys
from blogging.configuration import Configuration
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLabel, QLineEdit
from blogging.gui.login_gui import LoginGUI
from blogging.gui.dashboard_gui import Dashboard
from blogging.controller import Controller
from blogging.blog import Blog


class BloggingGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # set autosave to True to ensure persistence is working
        self.configuration = Configuration()
        self.configuration.__class__.autosave = True
        # Continue here with your code!

        self.setWindowTitle("Gabriel and Michael's Blogging App")
        self.setMaximumSize(1920, 1080)

        middle = QWidget()
        self.setCentralWidget(middle)
        self.layout = QVBoxLayout()
        middle.setLayout(self.layout)

        self.controller = Controller()
        self.current_user = None

        self.login_widget = LoginGUI(self.controller)
        self.login_widget.setFixedSize(300,300)
        self.layout.addWidget(self.login_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.login_widget.login_success.connect(self.when_login_successful)
        self.login_widget.login_fail.connect(self.when_login_failed)

        self.user_login_log = None
        self.user_failed_login_log = None

    #Successful Login Prompt
    def when_login_successful(self, username):
        self.current_user = username

        #Removing current user prompt if logged out
        if self.user_login_log is not None:
            self.user_login_log.setParent(None)
            self.user_login_log = None

        #Removing failed login prompt if logged in
        if self.user_failed_login_log is not None:
            self.user_failed_login_log.setParent(None)
            self.user_failed_login_log = None

        self.user_login_log = QLabel(f"Logged in as {self.current_user}")
        self.layout.addWidget(self.user_login_log, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.login_widget.setParent(None)

        self.dashboard = Dashboard(self.controller)
        self.dashboard.clicked_logout.connect(self.logout_gui)

        self.layout.addWidget(self.dashboard, alignment=Qt.AlignmentFlag.AlignHCenter)

    # Failed Login Prompt
    def when_login_failed(self):
        if self.user_failed_login_log is not None:
            self.user_failed_login_log.setParent(None)

        self.user_failed_login_log = QLabel(f"Failed to login. Invalid username or password.")
        self.layout.addWidget(self.user_failed_login_log, alignment=Qt.AlignmentFlag.AlignHCenter)

    #Logs out current user and opens log in menu
    def logout_gui(self):
        self.controller.logout()
        self.current_user = None

        if hasattr(self, "dashboard"):
            self.dashboard.setParent(None)
            del self.dashboard

        if self.user_login_log is not None:
            self.user_login_log.setParent(None)
            self.user_failed_login_log = None

        self.layout.addWidget(self.login_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

def main():
    app = QApplication(sys.argv)
    window = BloggingGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
