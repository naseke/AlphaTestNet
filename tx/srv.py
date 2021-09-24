import re
import socket
import base64


class AlphaServer():

    MSG_DEB = "txtxtx"
    MSG_FIN = "rxrxrx"
    TAILLE_LONG_CHIFFRE = 6
    TAILLE_BUFFER = 1000

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # findef

    def bind(self, host, port):
        self.socket.bind((host, port))
    # findef

    def send_msg(self,msg=""):
        tmp = ("txtxtx" + str(len(msg)).rjust(self.TAILLE_LONG_CHIFFRE, "0") + msg + "rxrxrx").encode()
        self.socket.sendall(base64.b64encode(tmp))
    # findef

    def recv_msg(self):
        buf = ""

        tx = base64.b64decode(self.conn.recv(self.TAILLE_BUFFER)).decode()
        if tx.find(self.MSG_DEB) > -1:
            buf = tx.replace(self.MSG_DEB,"")
            p = re.compile("\d" * self.TAILLE_LONG_CHIFFRE)
            msglong = int(p.search(tx).group())
            buf = buf.replace(p.search(tx).group(),"")
            while len(buf) < msglong:
                tx = base64.b64decode(self.conn.recv(self.TAILLE_BUFFER)).decode()
                buf = buf + tx
            # fintantque
            buf = buf.replace(self.MSG_FIN, "")
            return buf
        # finsi
        #return self.conn.recv(1024)

    # findef

    def listen(self):
        self.socket.listen()
    # findef

    def init_tx (self):
        self.conn, self.addr = self.socket.accept()
        print('-' * 79)
        print('Connected by', self.addr)
        print('-' * 79)
    # findef

    def close(self):
        self.socket.close()
    # findef

    def __del__(self):
        self.socket.close()
    # findef

# finclass


def main():
    port = 8000

    s = AlphaServer()
    s.bind('0.0.0.0', port)
    while True:
        s.listen()
        s.init_tx()
        print(s.recv_msg())
    s.close()
# findef

if __name__ == "__main__": main()