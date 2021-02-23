from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi
import sys
import socket
from client import Client

class Form(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('form.ui', self)

        self.setWindowTitle('클라이언트')
        self.ip.setInputMask('000.000.000.000; ')

        # ip, port 초기값 설정
        pcname = socket.gethostname()
        ip = socket.gethostbyname(pcname)
        self.ip.setText(ip)
        self.port.setText('6666')

        self.nick.setText('익명')

        # toggle 버튼으로 만들기
        self.btn_conn.setCheckable(True)

        # 클라이언트 생성
        self.client = Client(self)

        # 시그널
        self.btn_conn.clicked.connect(self.OnConn)
        self.btn_send.clicked.connect(self.OnSend)

        # 전역 시그널 처리
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj == self.msg and e.type() == QEvent.KeyPress and e.key() == Qt.Key_Return:
            self.OnSend()
            return True
        return super().eventFilter(obj, e)

    def OnConn(self):
        if self.btn_conn.isChecked():
            self.btn_conn.setText('접속 해제')
            ip = self.ip.text()
            port = self.port.text()

            if not self.client.connectServer(ip, port):
                self.btn_conn.setChecked(False)
                self.btn_conn.setText('서버 접속')
        else:
            self.btn_conn.setText('서버 접속')
            self.client.disconnServer()

    def OnSend(self):
        txt = self.msg.text()
        nick = self.nick.text()
        txt = f'[{nick}] {txt}'
        self.client.sendMsg(txt)
        self.msg.setText('')

    def OnRecv(self, txt):
        self.lw.addItem(txt)

    def OnDisconn(self):
        self.btn_conn.setChecked(False)
        self.btn_conn.setText('서버 접속')

    def closeEvent(self, e):
        self.client.disconnServer()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())