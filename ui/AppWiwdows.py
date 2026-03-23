import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from ui.components.InputsArea import InputsArea
from ui.components.Header import Header
from ui.components.ButtonsArea import ButtonsArea
from ui.components.MsgArea import MsgArea
from entities.CatalogAnalyzer import CatalogAnalyzer


class AppWindow:
    def __init__(self):

        # main app
        app = QApplication(sys.argv)
        with open("ui/style.qss", "r") as f:
            app.setStyleSheet(f.read())

        # windows principal
        windows = QWidget()
        windows.setWindowTitle("UNC: verificador de Catálogo")

        # config layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # adiciona componentes
        self.header = Header()
        self.inputs_area = InputsArea()
        self.msg_area = MsgArea()
        self.buttons_area = ButtonsArea()

        main_layout.addWidget(self.header)
        main_layout.addWidget(self.inputs_area)
        main_layout.addWidget(self.msg_area)
        main_layout.addWidget(self.buttons_area)

        # conectar sinais
        self.buttons_area.add_field_btn_clicked.connect(self.inputs_area.add_field)
        self.buttons_area.analyze_btn_clicked.connect(self.analyze)
        self.buttons_area.cancel_btn_clicked.connect(self.end_analyze)

        self.header.folder_path_selected.connect(self.set_folder_path)

        # final
        self.analyzer = CatalogAnalyzer(self.msg_area)
        windows.setLayout(main_layout)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        windows.show()
        app.exec()


    def start_analyze(self):
        self.inputs_area.setDisabled(True)
        self.buttons_area.analyze_btn.setDisabled(True)
        self.buttons_area.add_field_btn.setDisabled(True)
        self.header.select_folder_btn.setDisabled(True)

    def end_analyze(self):
        self.inputs_area.setDisabled(False)
        self.buttons_area.analyze_btn.setDisabled(False)
        self.buttons_area.add_field_btn.setDisabled(False)
        self.header.select_folder_btn.setDisabled(False)
        self.buttons_area.cancel_btn.hide()
        self.buttons_area.layout().invalidate()
        self.buttons_area.adjustSize()
        self.buttons_area.parentWidget().adjustSize()


    def set_folder_path(self, path: str):
        self.buttons_area.analyze_btn.setDisabled(False)
        self.analyzer.folder_path = path
    

    def analyze(self):
        self.start_analyze()
        inputs_values = self.inputs_area.get_input_values()
     
        if len(inputs_values) == 0:
            self.msg_area.set_msg('error', 'Os campos de URL devem estar preenchidos!', 'error')
            self.end_analyze()
        else:
            self.msg_area.hide_msg()
            self.buttons_area.cancel_btn.show()

            for key in inputs_values.keys():
                url = inputs_values[key]

                if len(url) == 0:
                    self.msg_area.set_msg('error', 'URL Iválida', 'error')

                else:
                    try:
                        self.analyzer.analyze_catalog(url)
                        self.end_analyze()
                        self.msg_area.set_msg('Análise feita com sucesso', f'Completamos a análise no catálogo: "{url}"')
                    except:
                        self.msg_area.set_msg('Error', f'Não foi possível completar a sua análise no catálogo: "{url}"', 'error')




      
    