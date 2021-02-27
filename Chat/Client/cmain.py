from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi
import sys
import socket
from client import Client

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class Form(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('form.ui', self)

        self.setWindowTitle('양윤준톡')
        self.ip.setInputMask('000.000.000.000; ')

        # ip, port 초기값 설정
        pcname = socket.gethostname()
        ip = socket.gethostbyname(pcname)
        self.ip.setText(ip)
        self.port.setText('6666')

        # 채팅 사용 불가
        self.btn_send.setDisabled(True)
        self.msg.setDisabled(True)

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
            self.name.setDisabled(True)
            name = self.name.text()
            ip = self.ip.text()
            port = self.port.text()

            if not name:
                QMessageBox.warning(self, '닉네임 오류', '닉네임을 설정해주세요.', QMessageBox.Yes)
                self.OffConnBtn()
            elif not name.find('관리자') == -1:
                QMessageBox.warning(self, '닉네임 오류', '관리자는 사용할 수 없습니다.', QMessageBox.Yes)
                self.OffConnBtn()
            elif not self.client.connectServer(ip, port, name):
                QMessageBox.warning(self, '접속 오류', 'IP, PORT가 잘못되었거나\n서버가 열리지 않았습니다.', QMessageBox.Yes)
                self.OffConnBtn()
            else:
                row = self.lw.count()
                for r in range(row):
                    self.lw.takeItem(0)

                self.btn_conn.setText('접속 해제')
                self.btn_send.setDisabled(False)
                self.msg.setDisabled(False)
                
        else:
            self.OffConnBtn()
            self.client.disconnServer()

    def OffConnBtn(self):
        self.btn_conn.setText('서버 접속')
        self.btn_conn.setChecked(False)
        self.name.setDisabled(False)
        self.btn_send.setDisabled(True)
        self.msg.setDisabled(True)

    def OnSend(self):
        txt = self.msg.text()
        name = self.name.text()
        txt = f'[{name}] {txt}'
        self.client.sendMsg(txt)
        self.msg.setText('')

    def OnDelete(self, txt):
        row = self.lw.count()
        for r in range(row):
            if self.lw.item(r).text() == txt:
                self.lw.takeItem(r)
                break

    def OnDeleteAll(self):
        cnt = self.lw.count()
        for i in range(cnt):
            self.lw.takeItem(0)

    def OnRecv(self, txt):
        self.lw.addItem(txt)
        scrollBar = self.lw.verticalScrollBar()
        if scrollBar.value() == scrollBar.maximum():
            self.lw.scrollToBottom()

    def OnDisconn(self):
        self.btn_conn.setChecked(False)
        self.name.setDisabled(False)
        self.btn_send.setDisabled(True)
        self.msg.setDisabled(True)
        self.btn_conn.setText('서버 접속')
        QMessageBox.information(self, '채팅 종료', '채팅이 종료되었습니다.', QMessageBox.Yes)

    def closeEvent(self, e):
        self.client.disconnServer()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())