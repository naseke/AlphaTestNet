import asyncio
import os
from operator import itemgetter
from threading import *
from lib import couleurs, tools
from lib.ordonnanceur import OrdoCache
from lib.logs import Log
from lib.alphaserver import AlphaServer


class alphaservercache:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class AlphaServerCache(AlphaServer):

    __VERSION = '0.01'

    def __init__(self, host, port, pwd=None, debug=False):

        super().__init__(host, port, pwd, debug)
        self.services = [{'cache': [self.listener.address[0], self.listener.address[1]]}, ]
        self.node = ()
        self.ordo = OrdoCache()
        self.ordo_thread = None
        self.last_config_version, self.config = self.load_config()
        self.blk_id_prev = self.index['id_obj_prev'][len(self.index['id_obj_prev']) - 1][0]
        self.log = Log('cache', os.path.join(tools.find_root(), 'log', 'cache.log'))

    def msg_welcome(self):
        couleurs.AffichageColor().msg_INFO(msg=f"""

   _____                                   _____          _____ _    _ ______                          
  / ____|                                 / ____|   /\   / ____| |  | |  ____|                         
 | (___   ___ _ ____   _____ _   _ _ __  | |       /  \ | |    | |__| | |__      ___  _ __   ___ _ __  
  \___ \ / _ \ '__\ \ / / _ \ | | | '__| | |      / /\ \| |    |  __  |  __|    / _ \| '_ \ / _ \ '_ \ 
  ____) |  __/ |   \ V /  __/ |_| | |    | |____ / ____ \ |____| |  | | |____  | (_) | |_) |  __/ | | |
 |_____/ \___|_|    \_/ \___|\__,_|_|     \_____/_/    \_\_____|_|  |_|______|  \___/| .__/ \___|_| |_|
                                                                                     | |               
                                                                                     |_|               
           serveur : {self.listener.address[0]} 
           Port: {self.listener.address[1]}      
           """, log=self.log.logger)

    async def start(self):
        super().start()
        self.ordo_thread = Thread(target=self.ordo.start, daemon=True)
        self.ordo_thread.start()
        couleurs.AffichageColor().msg_INFO(f"Chargement de la configuration \n"
                                           f"version : {self.last_config_version}\n"
                                           f"{repr(self.config)}", self.log.logger)
        couleurs.AffichageColor().msg_INFO(f"{len(self.index['id_obj_prev'])} blocs trouvés dans le cache", self.log.logger)
        while self.is_start():
            print(f"boucle n°{self.boucle}")
            self.init_tx()
            await asyncio.create_task(self.recv_msg())
            self.boucle += 1

    async def stop(self):
        self.ordo.stop()
        await super().stop()

    async def trt_cmd(self, **msg):
        from lib.AlphaClient import AlphaClientCache
        from lib.block import Block
        if msg['command'] == 'get_services':
            await self.send_msg_common_rep('get_services')
            self.node = msg['node']
            AlphaClientCache.send_cmd(self.node[0], self.node[1], self.boucle, 'trsf_config', 'AlphaClientCache', chaine=str((self.config, self.last_config_version)))
        elif msg['command'] == 'get_blk_id_prev':
            await self.send_msg_ctrl('done')
            AlphaClientCache.send_cmd(self.node[0], self.node[1], self.boucle, 'get_blk_id_prev', 'AlphaClientCache', debug=False, chaine=self.blk_id_prev)
        elif msg['command'] == 'trsf_bloc':
            ori, blc = await self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg)
            await self.cache_blk(Block(blc, "0.1.0"))
        else:
            await super().trt_cmd(**msg)

    async def cache_blk(self, blk):
        from lib.stock_hdd import hdd
        hdd().write_block(blk)
        self.index = self.init_index()
        self.blk_id_prev = max(self.index['id_obj_prev'], key=itemgetter(0))[0]

    def init_index(self):
        pass  # TODO A faire pour un cache normal

    def load_config(self):
        # from lib.stock_hdd import hdd # TODO future implementation (pas sure)
        tupl = self.index['id_obj_prev'][0]  # TODO A corrigé Il faut trouver une mecanique pour recuperer la dernière configuration
        return tupl[1].get_config_version(), tupl[1].blk_config

    async def _send_config(self, ip, port):
        from lib.AlphaClient import AlphaClientCache
        try:
            r = AlphaClientCache.send_cmd(ip, port, self.boucle, 'trsf_config', 'AlphaClientCache', chaine=str((self.config, self.last_config_version)))
        except ConnectionRefusedError:
            return -1
        return 0
