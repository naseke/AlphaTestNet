import asyncio

class AlphaServer():

    def __init__(self, host, port, pwd=None):
        self.host = host
        self.port = port
        self.pwd = pwd
    # findef

    async def start(self):
        r, w = await asyncio.open_connection('127.0.0.1', self.port)
        c = await asyncio.start_server([r, w], host='0.0.0.0', port=self.port)
        print(c.__dict__)

# finclass


def main():
    HOST = '192.168.1.9'  # The server's hostname or IP address
    PORT = 8000  # The port used by the server

    a = AlphaServer(HOST,PORT)
    asyncio.run(a.start())
# findef


if __name__ == '__main__': main()