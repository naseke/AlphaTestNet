import asyncio


class node:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


async def commande(cmd):
    # from tx.AlphaServer_wo_coro import AlphaServerNode
    from lib.parametres import Params
    from lib.tools import get_ip

    port = int(Params().PARAMS['PORT_NODE'])
    host = get_ip()
    if cmd == 'start':
        from lib.AlphaServer import AlphaServerNode
        l = AlphaServerNode(host, port, debug=False)
        await l.start()
    elif cmd == 'stop':
        from lib.AlphaClient import AlphaClientNode
        AlphaClientNode.send_cmd(host, port, -1, 'stop', 'AlphaClientNode', debug=False)
    else:
        print("erreur de commande !")


async def main():

    await commande('start')


if __name__ == "__main__": asyncio.run(main())