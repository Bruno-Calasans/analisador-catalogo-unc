from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QIcon

class MsgArea(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.setObjectName('msg-area')

        # title
        self.title = QLabel()
        self.title.setObjectName('title')

        # msg widget
        self.msg = QLabel()
        self.msg.setObjectName('msg')

        layout.addWidget(self.title)
        layout.addWidget(self.msg)
        self.hide()


    def set_msg(self, title: str, msg: str, type: str = 'success'):
        self.show_msg()
        self.title.setText(title)
        self.msg.setText(msg)

        if type == 'error':
            self.msg.setStyleSheet("color: red")

        elif type == 'success':
            self.msg.setStyleSheet("color: green")


    def show_msg(self):
        self.show()


    def hide_msg(self):
        self.hide()
    

