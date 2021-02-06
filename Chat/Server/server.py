import socket

class Server():
    def __init__(self, w):
        self.parent = w

    def startServer(self, ip, port):
        # 소켓 생성 IPV4, TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 소켓 묶음(bind) ip, port
        try:
            self.socket.bind((ip, int(port)))
        except Exception as e:
            print(e)
            return False
        else:
            pass

        return True

    def closeServer(self):
        pass