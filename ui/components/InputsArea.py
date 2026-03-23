from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class InputsArea(QWidget):
    input_values = {}

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addWidget(self.create_field('URL 1'))
        self.setLayout(layout)


    def create_field(self, label_txt: str):

        field_container = QWidget()
        field_layout = QVBoxLayout(field_container)
        field_layout.setContentsMargins(0,0,0,0)
        field_layout.setSpacing(0)

        # label
        label = QLabel(label_txt)
        label.setContentsMargins(10,0,0,0)
        
        # input
        input_ = QLineEdit()
        input_name = f'input-{self.layout().count() + 1}'
        input_.setObjectName(input_name)

        # remove button for delete the input
        remove_btn = QPushButton()
        remove_btn.setIcon(QIcon('ui/icons/remove-icon.png'))
        remove_btn.setFixedSize(20, 20)
        remove_btn.setObjectName('remove-input-btn')

        input_widget = QWidget()
        input_layout = QHBoxLayout()
        input_layout.addWidget(input_)

        # add remove btn only if there's more than 1 input
        if self.layout().count() > 0:
            input_layout.addWidget(remove_btn)

        input_widget.setLayout(input_layout)

        # add widgets
        field_layout.addWidget(label)
        field_layout.addWidget(input_widget)
        field_container.setObjectName(f'{input_name}')

        # events
        input_.textChanged.connect(lambda texto: self.input_handler(texto, input_.objectName()))
        remove_btn.clicked.connect(lambda texto: self.remove_input_handler(input_.objectName()))

        return field_container
    

    def input_handler(self, value: str, input_name: str):
        self.input_values[input_name] = value
        print(self.input_values)

    
    def add_field(self):
        layout = self.layout()
        num_field = layout.count()
        campo = self.create_field(f'URL {num_field + 1}')
        layout.addWidget(campo)


    def get_input_values(self):
        return self.input_values


    def remove_input_handler(self, input_name: str):
        layout = self.layout()

        for i in range(0, layout.count()):

            input = layout.itemAt(i)

            if input is not None and input.widget().objectName() == input_name:

                widget = input.widget()
                layout.removeWidget(widget)

                if input_name in self.input_values:
                    self.input_values.pop(input_name)
                widget.deleteLater()
            
        self.layout().invalidate()
        self.adjustSize()
        self.parentWidget().adjustSize()
        