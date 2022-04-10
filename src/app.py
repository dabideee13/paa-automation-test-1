import sys

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QVBoxLayout
from PyQt5.QtCore import Qt

from automations import WebFrontAutomation
from tools import get_config, get_credentials
from logger import logger


class Window(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Park Ave Appliance')
        self.setGeometry(100, 100, 400, 200)

        self.UIComponents()
        self.show()

    def UIComponents(self):
        process_data_button = QPushButton('Process Data', self)
        process_data_button.setGeometry(125, 50, 150, 30)

        process_data_button_box = QVBoxLayout(self)
        process_data_button_box.setAlignment(Qt.AlignCenter)

        process_data_button_box.addWidget(process_data_button, alignment=Qt.AlignCenter)
        process_data_button.setContentsMargins(0, 20, 0, 0)

        process_data_button.clicked.connect(self.process_data)

    def process_data(self):
        logger.info('Processing data')

        webfront = WebFrontAutomation(
            config=get_config(),
            credentials=get_credentials()
        )
        webfront.run_driver()
        webfront.quit_driver()

        logger.info('DONE: Processing data')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
