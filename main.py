from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             QPlainTextEdit,
                             QPushButton,
                             QLineEdit,
                             QWidget,
                             QLabel)
from PyQt5.QtCore import (QPropertyAnimation,
                          QParallelAnimationGroup,
                          QPoint,
                          QTimer,
                          QEventLoop)
from PyQt5.QtGui import (QMouseEvent,
                         QIcon,
                         QPixmap)

from bs4 import BeautifulSoup
import sys, requests, webbrowser, resources
from data import DataBase

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Scrambler Phone Info")
        self.setStyleSheet("background-color: #262626")
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(":/icons/logo.png"), QIcon.Selected, QIcon.On)
        self.setWindowIcon(self.icon)

        self.db = DataBase()
        self.Style = """
            QPushButton {
                font-size: 20px;
                color: white;
                border-radius: 10px;
                border: 1px solid #3A3A3A;
            }
            QPushButton#get_history_number {
                background-color: purple;
                color: white
            }
            QPushButton#Open_Panel_Menu {
                border-radius: 10px;
                border: 1px solid #3A3A3A;
                font-size: 15px;
            }
            QPushButton#Open_Panel_Menu:hover {
                border: 1px solid purple;
            }
            QPushButton#Open_Panel_Menu:pressed {
                border: 1px solid #3A3A3A;
            }
            QPushButton#TelegramButton {
                color: #fff;
                background-color: #208FFF;
                font-size: 18px;
                border-radius: 5px;
            }

            QPushButton#TelegramButton:hover {
                background-color: #46A0FC;
                font-size: 19px;
            }

            QPushButton#TelegramButton:pressed {
                background-color: #208FFF
            }
            QPushButton#GitHubButton {
                color: #fff;
                background-color: #080B0F;
                font-size: 16px;
                font: bold;
                border-radius: 5px;
            }
            QPushButton#GitHubButton:hover {
                background-color: #12151A;
                font-size: 17px;
                color: purple
            }
            QPushButton#GitHubButton:pressed {
                background-color: #080B0F
            }
            QPushButton#CloseButton {
                color: #3A3A3A;
                font-size: 20px;
                border-radius: 10;
            }
            QPushButton#CloseButton:hover {
                background-color: #2F2F32;
                color: #D800CB
            }
            QPushButton#information_service {
                color: #545454;
                font-size: 13px;
                border: none;
            }
            QPushButton#information_service:hover {
                color: #00E0FF
            }
            QLineEdit {
                border: 1px solid #3A3A3A;
                font-size: 25px;
                color: silver;
                padding: 10px;
                border-radius: 10px;
            }
            QPlainTextEdit {
                border: 1px solid #3A3A3A;
                font-size: 20px;
                color: white;
                padding: 10px
            }
            QWidget#panel_menu {
                background-color: #202020
            }
            QLabel {
                color: #545454;
                background-color: none;
                font-size: 17px; 
            }
        """
        self.information_plain = QPlainTextEdit(self)
        self.information_plain.setGeometry(50, 100, 500, 600)
        self.information_plain.setStyleSheet(self.Style)
        self.information_plain.setReadOnly(True)

        self.input_number = QLineEdit(self)
        self.input_number.setGeometry(700, 200, 400, 100)
        self.input_number.setStyleSheet(self.Style)
        self.input_number.setMaxLength(10)
        self.input_number.setPlaceholderText("Введите номер после +7")
        self.input_number.textChanged.connect(self.input_text)

        self.push_number = QPushButton("Поиск", self)
        self.push_number.setGeometry(700, 320, 400, 100)
        self.push_number.setStyleSheet(self.Style)
        self.push_number.setEnabled(False)
        self.push_number.clicked.connect(self.get_status_code)
        
        self.get_history_number = QPushButton("История", self)
        self.get_history_number.setGeometry(700, 440, 400, 100)
        self.get_history_number.setObjectName("get_history_number")
        self.get_history_number.setStyleSheet(self.Style)
        self.get_history_number.clicked.connect(self.get_history_numbers)

        self.clear_history_number = QPushButton("Очистить Историю", self)
        self.clear_history_number.setGeometry(700, 560, 400, 100)
        self.clear_history_number.setObjectName("get_history_number")
        self.clear_history_number.setStyleSheet(self.Style)
        self.clear_history_number.clicked.connect(self.clear_database_history_numbers)

        self.Open_Panel_Menu = QPushButton("Меню", self)
        self.Open_Panel_Menu.setGeometry(1000, 50, 100, 50)
        self.Open_Panel_Menu.setObjectName("Open_Panel_Menu")
        self.Open_Panel_Menu.setStyleSheet(self.Style)
        self.Open_Panel_Menu.clicked.connect(self.OpenPanel)

        self.information_service = QPushButton("Service https://phoneradar.ru/ 2023г", self)
        self.information_service.setObjectName("information_service")
        self.information_service.setStyleSheet(self.Style)
        self.information_service.setGeometry(820, 750, 350, 15)
        self.information_service.clicked.connect(self.openServicePhonesBrowser)

        self.panel_menu = QWidget(self)
        self.panel_menu.setGeometry(0, -200, 1200, 100)
        self.panel_menu.setObjectName("panel_menu")
        self.panel_menu.setStyleSheet(self.Style)

        self.TelegramButton = QPushButton("Telegram", self)
        self.TelegramButton.setObjectName("TelegramButton")
        self.TelegramButton.setStyleSheet(self.Style)
        self.TelegramButton.setGeometry(100, -35, 200, 30)
        self.TelegramButton.clicked.connect(self.openTelegramWebBrowser)

        self.GitHubButton = QPushButton("GitHub", self)
        self.GitHubButton.setObjectName("GitHubButton")
        self.GitHubButton.setStyleSheet(self.Style)
        self.GitHubButton.setGeometry(320, -35, 200, 30)
        self.GitHubButton.clicked.connect(self.openGitHubWebBrowser)
        
        self.label_menu_text = QLabel("Thank you for using: Scrambler Phone Info :)", self)
        self.label_menu_text.setGeometry(550, -35, 410, 50)
        self.label_menu_text.setStyleSheet(self.Style)

        self.CloseButton = QPushButton("✕", self)
        self.CloseButton.setObjectName("CloseButton")
        self.CloseButton.setStyleSheet(self.Style)
        self.CloseButton.setGeometry(1100, -35, 30, 30)
        self.CloseButton.clicked.connect(self.ClosePanel)

        self.GroupAnimation = QParallelAnimationGroup()
        self.AnimationPanelMenu = QPropertyAnimation(self.panel_menu, b"pos")
        self.AnimationTelegramButton = QPropertyAnimation(self.TelegramButton, b"pos")
        self.AnimationGitHubButton = QPropertyAnimation(self.GitHubButton, b"pos")
        self.AnimationLabelText = QPropertyAnimation(self.label_menu_text, b"pos")
        self.AnimationCloseButton = QPropertyAnimation(self.CloseButton, b"pos")
    
    def input_text(self):
        try:
            int(self.input_number.text())
            if len(self.input_number.text()) == 10:
                self.push_number.setStyleSheet("background-color: purple; font-size: 20px; color: white; border-radius: 10px;")
                self.push_number.setEnabled(True)
            else:
                self.is_active_button()
        except:
            self.is_active_button()

    def is_active_button(self):
        self.push_number.setStyleSheet(self.Style)
        self.push_number.setEnabled(False)

    def get_status_code(self):
        try:
            service = f"https://phoneradar.ru/phone/"
            number = self.input_number.text()
            absolute = service+number
            self.loop = QEventLoop()
            QTimer.singleShot(3000, self.loop.quit)
            self.loop.exec()
            response = requests.get(url=absolute, params=None)
            if response.status_code == 200:
                bs = BeautifulSoup(response.text, "lxml")
                title = bs.find('div', 'card-body')
                all_info = title.find('table', 'table')
                self.information_plain.setPlainText(all_info.text)
                self.db.add_numbers(self.input_number.text())
            else:
                self.information_plain.setPlainText(f"Сайт вернул ответ, ощибка подключения {response.status_code}")
        except Exception as Exp:
            self.information_plain.setPlainText(f"Упс, что-то пошло не так :( {Exp}\n\nЕсли что: Перезапустите программу")

    def get_history_numbers(self):
        get_history = self.db.get_history_numbers()
        self.information_plain.setPlainText(f"{get_history}")

    def clear_database_history_numbers(self):
        self.db.clear_database_history()
        self.information_plain.setPlainText("История очищена!")
    
    def OpenPanel(self):
        self.AnimationPanelMenu.setEndValue(QPoint(0, 0))  # Geometry Animation PanelOpen
        self.AnimationPanelMenu.setDuration(200)

        self.AnimationTelegramButton.setEndValue(QPoint(100, 35))  # Geometry Animation PanelOpen
        self.AnimationTelegramButton.setDuration(200)

        self.AnimationGitHubButton.setEndValue(QPoint(320, 35))  # Geometry Animation PanelOpen
        self.AnimationGitHubButton.setDuration(200)

        self.AnimationLabelText.setEndValue(QPoint(550, 25))  # Geometry Animation PanelOpen
        self.AnimationLabelText.setDuration(200)
        
        self.AnimationCloseButton.setEndValue(QPoint(1100, 35))  # Geometry Animation PanelOpen
        self.AnimationCloseButton.setDuration(200)

        self.start_anim()

    def ClosePanel(self):
        self.AnimationPanelMenu.setEndValue(QPoint(0, -200))  # Geometry Animation PanelOpen
        self.AnimationPanelMenu.setDuration(200)

        self.AnimationTelegramButton.setEndValue(QPoint(100, -35))  # Geometry Animation PanelOpen
        self.AnimationTelegramButton.setDuration(200)

        self.AnimationGitHubButton.setEndValue(QPoint(320, -35))  # Geometry Animation PanelOpen
        self.AnimationGitHubButton.setDuration(200)

        self.AnimationLabelText.setEndValue(QPoint(550, -35))  # Geometry Animation PanelOpen
        self.AnimationLabelText.setDuration(200)
        
        self.AnimationCloseButton.setEndValue(QPoint(1100, -35))  # Geometry Animation PanelOpen
        self.AnimationCloseButton.setDuration(200)

        self.start_anim()

    def start_anim(self):
        self.GroupAnimation.addAnimation(self.AnimationPanelMenu)
        self.GroupAnimation.addAnimation(self.AnimationTelegramButton)
        self.GroupAnimation.addAnimation(self.AnimationGitHubButton)
        self.GroupAnimation.addAnimation(self.AnimationLabelText)
        self.GroupAnimation.addAnimation(self.AnimationCloseButton)
        self.GroupAnimation.start()

    def openTelegramWebBrowser(self):
        webbrowser.open('https://t.me/ProgramsCreator/')

    def openGitHubWebBrowser(self):
        webbrowser.open('https://github.com/Shedrjoinzz')

    def openServicePhonesBrowser(self, envent: QMouseEvent):
        webbrowser.open("https://phoneradar.ru/")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setFixedSize(1200, 800)
    window.show()
    sys.exit(app.exec_())
