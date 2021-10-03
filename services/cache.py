import asyncio


class cache:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


async def commande(cmd):
    # from tx.AlphaServer_wo_coro import AlphaServerSuperCache
    from lib.parametres import Params
    from lib.tools import get_ip

    port = int(Params().PARAMS['PORT_CACHE'])
    host = get_ip()
    if cmd == 'start':
        from lib.alphaserversupercache import AlphaServerSuperCache
        l = AlphaServerSuperCache(host, port, debug=False)
        await l.start()
    elif cmd == 'stop':
        from lib.AlphaClient import AlphaClientCache
        AlphaClientCache.send_cmd(host, port, -1, 'stop', 'AlphaClientCache', debug=False)
    else:
        print("erreur de commande !")


async def main():

    await commande('start')


if __name__ == "__main__": asyncio.run(main())