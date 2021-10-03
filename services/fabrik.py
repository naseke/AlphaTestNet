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

    port = int(Params().PARAMS['PORT_FABRIK'])
    host = get_ip()
    if cmd == 'start':
        from lib.alphaserverfabrik import AlphaServerFabrik
        l = AlphaServerFabrik(host, port, debug=False)
        await l.start()
    elif cmd == 'stop':
        from lib.AlphaClient import AlphaClientFabrik
        AlphaClientFabrik.send_cmd(host, port, -1, 'stop', 'AlphaClientFabrik', debug=False)
    else:
        print("erreur de commande !")


async def main():

    await commande('start')

if __name__ == "__main__": asyncio.run(main())