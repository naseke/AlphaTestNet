import asyncio


class cache:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


async def start(host, port):
    # from tx.AlphaServer_wo_coro import AlphaServerValidator
    from lib.AlphaServer import AlphaServerValidator

    loop = asyncio.get_running_loop()

    l = AlphaServerValidator(host, port, debug=False)
    await l.start()


async def main():
    from lib.parametres import Params
    from lib.tools import get_ip

    port = int(Params().PARAMS['PORT_VALIDATOR'])
    host = get_ip()
    await start(host, port)


if __name__ == "__main__": asyncio.run(main())