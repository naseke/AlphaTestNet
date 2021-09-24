from multiprocessing.connection import Listener
import lib.couleurs

class AlphaServer():

    MSG_DEB = "txtxtx"
    MSG_FIN = "rxrxrx"
    TAILLE_LONG_CHIFFRE = 6
    TAILLE_BUFFER = 1000

    def __init__(self, host, port, pwd=None):
        self.listener = Listener((host, port), pwd)
    # findef

    def send_msg(self, msg=""):
        #tmp = ("txtxtx" + str(len(msg)).rjust(self.TAILLE_LONG_CHIFFRE, "0") + msg + "rxrxrx").encode()
        self.conn.send(msg)
    # findef

    def recv_msg(self):
        return self.conn.recv()
    # findef

    def init_tx (self):
        self.conn = self.listener.accept()
        print(f'{lib.couleurs.bcolors.OK}-' * 79)
        print('Connected by ', self.listener.last_accepted)
        print('-' * 79, f'{lib.couleurs.bcolors.RESET}')
    # findef

    def __del__(self):
        self.listener.close()
    # findef

    def close(self):
        if self.listener is not None:
            self.listener.close()
    # findef

    def trt_msg(self,msg: dict):
        print(msg['numero'])
        print(msg['command'])
        print(msg['parametres'])
        print(msg['signature'])
    # findef

# finclass


def main():
    port = 8000

    s = AlphaServer('192.168.1.9', port)
    while True:
        s.init_tx()
        try:
            s.trt_msg(s.recv_msg())
        except EOFError:
            print(f'{lib.couleurs.bcolors.FAIL}-' * 79)
            print('Connexion error with :', s.listener.last_accepted)
            print('-' * 79, f'{lib.couleurs.bcolors.RESET}')
            pass
    # s.close()
# findef

if __name__ == "__main__": main()