import socket
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal
import datetime

class Server(QObject):

    conn_signal = pyqtSignal(str, str)
    disconn_signal = pyqtSignal(str, str)
    recv_signal = pyqtSignal(str)
    name_signal = pyqtSignal(str)

    def __init__(self, w):
        super().__init__()
        self.parent = w

        self.clients = []

        # 시그널
        self.conn_signal.connect(self.parent.OnConnClient)
        self.disconn_signal.connect(self.parent.OnDisconnClient)
        self.recv_signal.connect(self.parent.OnRecv)
        self.name_signal.connect(self.parent.SetName)

    def openServer(self, ip, port):
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
        # listen 소켓 종료
        print('close server')
        self.run = False
        self.socket.close()

        # 접속한 클라이언트 소켓도 종료
        for c in self.clients:
            c[0].close()

    def closeClient(self, sock):
        for n, c in enumerate(self.clients):
            if c[0] == sock:
                sock.close()
                del(self.clients[n])
                break

    def broadcast(self, msg):
        for c in self.clients:
            c[0].send(msg)

    # 서버 listen 처리용
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

                #print(buf)
                txt = buf.decode(encoding='utf-8')
                idx = txt.find('[name]')
                if not idx == -1:
                    self.name_signal.emit(txt[:idx])
                else:
                    t = datetime.datetime.now()
                    time = t.strftime('%H:%M:%S')
                    txt = f'{time} {txt}'

                    self.recv_signal.emit(txt)
                    self.broadcast(txt.encode(encoding='utf-8'))

        print('disconnect client', addr)
        self.closeClient(client)
        self.disconn_signal.emit(addr[0], str(addr[1]))