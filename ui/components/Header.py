from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit
import os
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

class Header(QWidget):
    folder_path = ''
    folder_path_selected = Signal(str)

    
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.setObjectName('main-header')

        # title
        self.titulo = QLabel("Verificador de Catálogo")
        self.titulo.setObjectName('header-titulo')

        # subtitlea
        self.sub_title = QLabel("Vamos analisar as URLs abaixo para gerar um relatório.")
        self.sub_title.setObjectName('header-subtitulo')

        # subtitle 2
        sub_title_2 = QLabel("Escolhe a pasta onde o relatório será salvo")
        sub_title_2.setObjectName('header-subtitulo-2')

        # directory input
        self.folder_path = QLineEdit()
        self.folder_path.setDisabled(True)
        self.sub_title.setObjectName('header-input-path')

        # select directory button
        self.select_folder_btn = QPushButton("Salvar em")
        self.select_folder_btn.setIcon(QIcon('ui/icons/folder-icon.png'))
        self.select_folder_btn.setObjectName('header-select-folder-btn')
        self.select_folder_btn.clicked.connect(self.select_folder)

        layout.addWidget(self.titulo)
        layout.addWidget(self.sub_title)
        layout.addWidget(sub_title_2)
        layout.addWidget(self.folder_path)
        layout.addWidget(self.select_folder_btn)


    def select_folder(self):
        path = QFileDialog.getExistingDirectory(
            self,
            "Selecionar pasta"
        )

        if path:
            self.folder_path.setText(path)
        self.folder_path_selected.emit(path)

        
        
