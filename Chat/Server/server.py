import socket
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal

class Server(QObject):

    conn_signal = pyqtSignal(str, str)
    disconn_signal = pyqtSignal(str, str)

    def __init__(self, w):
        super().__init__()
        self.parent = w

        self.clients = []

        # 시그널
        self.conn_signal.connect(self.parent.OnConnClient)
        self.disconn_signal.connect(self.parent.OnDisconnClient)

    def startServer(self, ip, port):
        # 소켓 생성 IPV4, TCP (연결 지향형)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 소켓 묶음(bind) ip, port
        try:
            self.socket.bind((ip, int(port)))
        except Exception as e:
            print(e)
            return False
        else:
            # listen thread 생성
            self.run = True
            self.lt = Thread(target=self.threadListen, args=(self.socket,))
            self.lt.start()

        return True

    def closeServer(self):
        print('close server')
        self.run = False
        self.socket.close()

    # sever listen 처리용
    def threadListen(self, sock):
        print('listen start')
        sock.listen(5)

        while self.run:
            # 클라이언트가 접속할 때 까지 blocking
            try:
                client, addr = sock.accept()
            except Exception as e:
                print(e)
                break
            else:
                #print(client, addr)
                self.conn_signal.emit(addr[0], str(addr[1]))
                self.clients.append( (client, addr) )
                t = Thread(target=self.threadClient, args=(client, addr))
                t.start()

    # 서버가 클라이언트 처리용
    def threadClient(self, client, addr):
        while self.run:
            try:
                # 받을 때 까지 blocking
                buf = client.recv(1024)
            except Exception as e:
                print(e)
                break
            else:
                if buf == b'':
                    break

                print(buf)
                print(buf.decode(encoding='utf-8'))

        self.disconn_signal.emit(addr[0], str(addr[1]))
        print('client disconnect', addr)