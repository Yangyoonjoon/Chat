import socket
from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread

class Client(QObject):
    recv_signal = pyqtSignal(str)
    disconn_signal = pyqtSignal()
    delete_signal = pyqtSignal(str)
    deleteAll_signal = pyqtSignal()

    def __init__(self, w):
        super().__init__()
        self.parent = w

        # 시그널
        self.recv_signal.connect(self.parent.OnRecv)
        self.disconn_signal.connect(self.parent.OnDisconn)
        self.delete_signal.connect(self.parent.OnDelete)
        self.deleteAll_signal.connect(self.parent.OnDeleteAll)

    def connectServer(self, ip, port, name):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect( (ip, int(port)) )
        except Exception as e:
            print(e)
            return False
        else:
            # 이름인지 판별하는 문자열
            name += '[name]'
            self.name = name
            self.socket.send(name.encode('utf-8'))

            self.bRun = True
            self.t = Thread(target=self.clientThread, args=(self.socket,))
            self.t.start()
            return True

    def disconnServer(self):
        self.bRun = False
        self.socket.close()

    def sendMsg(self, txt):
        if hasattr(self, 'socket'):
            self.socket.send(txt.encode('utf-8'))
    
    def clientThread(self, sock):
        while self.bRun:
            try:
                buf = sock.recv(1024)
            except Exception as e:
                print(e)
                break
            else:
                if buf == b'':
                    break
                
                #print(buf)
                txt = buf.decode('utf-8')
                idx = txt.find('[del]')

                if not idx == -1:
                    self.delete_signal.emit(txt[:idx])
                elif not txt.find('[delall]') == -1:
                    self.deleteAll_signal.emit()
                else:
                    self.recv_signal.emit(txt)

        self.disconn_signal.emit()