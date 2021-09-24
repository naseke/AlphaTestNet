import asyncio


class node:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


async def start(host, port):
    # from tx.AlphaServer_wo_coro import AlphaServerNode
    from lib.AlphaServer import AlphaServerNode

    loop = asyncio.get_running_loop()

    l = AlphaServerNode(host, port, debug=False)
    await l.start()

async def main():
    from lib.parametres import Params
    from lib.tools import get_ip

    port = int(Params().PARAMS['PORT_NODE'])
    host = get_ip()
    await start(host, port)




if __name__ == "__main__": asyncio.run(main())