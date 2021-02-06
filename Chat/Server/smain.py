from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import sys
import socket
from server import Server

class Form(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('form.ui', self)

        self.setWindowTitle('서버')
        self.ip.setInputMask('000.000.000.000; ')

        # ip, port 초기값 설정
        pcname = socket.gethostname()
        ip = socket.gethostbyname(pcname)
        self.ip.setText(ip)
        self.port.setText('6666')

        # toggle 버튼으로 만들기
        self.btn_open.setCheckable(True)

        # 서버 생성
        self.server = Server(self)

        # 시그널
        self.btn_open.clicked.connect(self.OnOpen)

    def OnOpen(self):
        if self.btn_open.isChecked():
            self.btn_open.setText('서버 닫기')
            ip = self.ip.text()
            port = self.port.text()

            if not self.server.startServer(ip, port):
                self.btn_open.setChecked(False)
                self.btn_open.setText('서버 열기')
        else:
            self.btn_open.setText('서버 열기')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())