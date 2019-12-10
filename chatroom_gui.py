import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, 
    QPushButton, QLabel, QLineEdit, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)
        
        label_username = QLabel('username:')
        label_password = QLabel('password:')
        edit_username = QLineEdit()
        edit_password = QLineEdit()
        button_login = QPushButton('login')
        button_register = QPushButton('register')

        # button_login.clicked.connect(self.login)
        # button_register.clicked.connect(self.register)

        # button_login.resize(button_login.sizeHint())
        # button_register.resize(button_register.sizeHint())

        grid.addWidget(label_username, 0, 0)
        grid.addWidget(edit_username, 0, 1)
        grid.addWidget(label_password, 1, 0)
        grid.addWidget(edit_password, 1, 1)
        grid.addWidget(button_login, 2, 0)
        grid.addWidget(button_register, 2, 1)
        
        self.move(300, 150)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Chat')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())