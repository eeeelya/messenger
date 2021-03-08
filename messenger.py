from datetime import datetime

import requests
from PyQt6 import QtWidgets, QtCore
from clientui import Ui_MainWindow


class Messenger(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.pressed.connect(self.send_message)

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_message)
        self.timer.start(1000)

    def print_message(self, message):
        dt = datetime.fromtimestamp(message['time'])
        dt_str = dt.strftime('%d %b %H:%M:%S')
        self.textBrowser.append(dt_str + ' ' + message['name'])
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')

    def get_message(self):
        try:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': self.after}
            )
        except:
            return

        messages = response.json()['messages']
        for message in messages:
            self.print_message(message)
            after = message['time']

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()

        try:
            response = requests.post(
                'http://127.0.0.1:5000/send',
                json={'name': name, 'text': text}
            )
        except:
            self.textBrowser.append('Сервер недоступен.')
            self.textBrowser.append('Попробуйте еще раз.')
            self.textBrowser.append('')
            return

        if response.status_code != 200:
            self.textBrowser.append('Имя и текст не должно быть пустыми. Текст <= 1000 символов.')
            return

        self.textEdit.clear()


app = QtWidgets.QApplication([])
window = Messenger()
window.show()
app.exec()
