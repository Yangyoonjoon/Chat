import socket
from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread

class Client(QObject):
    recv_signal = pyqtSignal(str)
    disconn_signal = pyqtSignal()

    def __init__(self, w):
        super().__init__()
        self.parent = w

        # 시그널
        self.recv_signal.connect(self.parent.OnRecv)
        self.disconn_signal.connect(self.parent.OnDisconn)

    def connectServer(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect( (ip, int(port)) )
        except Exception as e:
            print(e)
            return False
        else:
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
                self.recv_signal.emit(txt)

        self.disconn_signal.emit()