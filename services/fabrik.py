import asyncio


class cache:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


async def start(host, port):
    # from tx.AlphaServer_wo_coro import AlphaServerFabrik
    from lib.AlphaServer import AlphaServerFabrik

    loop = asyncio.get_running_loop()

    l = AlphaServerFabrik(host, port, debug=False)
    await l.start()


async def main():
    from lib.parametres import Params
    from lib.tools import get_ip

    port = int(Params().PARAMS['PORT_FABRIK'])
    host = get_ip()
    await start(host, port)


if __name__ == "__main__": asyncio.run(main())