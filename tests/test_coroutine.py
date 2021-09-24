import asyncio
from multiprocessing.connection import Listener
import lib.couleurs

class AlphaServer():
    def __init__(self, host, port, pwd=None):
        self.listener = Listener((host, port), pwd)
    # findef

    def send_msg(self, msg=""):
        self.conn.send(msg)
    # findef

    def recv_msg(self):
        return self.conn.recv()
    # findef

    async def init_tx(self):
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

    async def trt_msg(self, msg: dict):
        print(msg['command'])
        print(msg['parametres'])
        print(msg['signature'])
    # findef

    def __await__(self):
        pass

# finclass

class coroutine():

    def __init__(self):
        pass

    async def run(self):
        print('hello')
        await asyncio.sleep(1)
        print('world')

    async def runsrv(self):
        port = 8000

        s = AlphaServer('192.168.1.9', port)
        print('-' * 79)
        print('Start node')
        print('listen to  ' + str(port))
        print('-' * 79)
        await s.init_tx()
        try:
            await s.trt_msg(s.recv_msg())
        except EOFError:
            print(f'{lib.couleurs.bcolors.FAIL}-' * 79)
            print('Connexion error with :', s.listener.last_accepted)
            print('-' * 79, f'{lib.couleurs.bcolors.RESET}')
            pass

    def __await__(self):
        return 1

def main():

    asyncio.run(coroutine().runsrv())
    asyncio.create_task(coroutine().run())

if __name__ == "__main__": main()