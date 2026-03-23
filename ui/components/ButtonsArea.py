from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon

class ButtonsArea(QWidget):
    add_field_btn_clicked = Signal()
    analyze_btn_clicked = Signal()
    cancel_btn_clicked = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.setObjectName('buttons-area')
     
        # add button
        self.add_field_btn = QPushButton('Adicionar mais URL')
        self.add_field_btn.setIcon(QIcon('ui/icons/add-icon.png'))

        # analyze button
        self.analyze_btn = QPushButton('Analisar')
        self.analyze_btn.setIcon(QIcon('ui/icons/analyze-icon.png'))
        self.analyze_btn.setDisabled(True)

        # cancel button
        self.cancel_btn = QPushButton('Cancelar')
        self.cancel_btn.setIcon(QIcon('ui/icons/cancel-icon.png'))
        self.cancel_btn.hide()

        layout.addWidget(self.add_field_btn)
        layout.addWidget(self.analyze_btn)
        layout.addWidget(self.cancel_btn)

        self.add_field_btn.clicked.connect(self.add_btn_handler)
        self.analyze_btn.clicked.connect(self.analyze_btn_handler)
        self.cancel_btn.clicked.connect(self.cancel_btn_handler)


    def add_btn_handler(self):
        self.add_field_btn_clicked.emit()


    def analyze_btn_handler(self):
        self.analyze_btn_clicked.emit()


    def cancel_btn_handler(self):
        self.cancel_btn_clicked.emit()




