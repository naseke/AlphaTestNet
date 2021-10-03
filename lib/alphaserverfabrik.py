import asyncio
import os
from collections import deque
from threading import *
from lib import couleurs, tools
from lib.ordonnanceur import OrdoFabrik
from lib.logs import Log
from lib.alphaserver import AlphaServer


class alphaserverfabrik:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class AlphaServerFabrik(AlphaServer):

    __VERSION = '0.01'

    def __init__(self, host, port, pwd=None, debug=False):
        super().__init__(host, port, pwd, debug)
        self.services = [{'fabrik': [self.listener.address[0], self.listener.address[1]]}, ]
        self.ordo = OrdoFabrik()
        self.ordo_thread = None
        self.currentblock = None
        self.blk_id_prev = None
        self.node = None
        self.lignes = deque()
        self.blocks = deque()
        self.blk_vers = "0.1.0" # TODO pour le turfu
        self.log = Log('fabrik', os.path.join(tools.find_root(), 'log', 'fabrik.log'))


    def msg_welcome(self):
        couleurs.AffichageColor().msg_INFO(msg=f"""

   _____                                  ______      ____  _____  _____ _  __                         
  / ____|                                |  ____/\   |  _ \|  __ \|_   _| |/ /                         
 | (___   ___ _ ____   _____ _   _ _ __  | |__ /  \  | |_) | |__) | | | | ' /    ___  _ __   ___ _ __  
  \___ \ / _ \ '__\ \ / / _ \ | | | '__| |  __/ /\ \ |  _ <|  _  /  | | |  <    / _ \| '_ \ / _ \ '_ \ 
  ____) |  __/ |   \ V /  __/ |_| | |    | | / ____ \| |_) | | \ \ _| |_| . \  | (_) | |_) |  __/ | | |
 |_____/ \___|_|    \_/ \___|\__,_|_|    |_|/_/    \_\____/|_|  \_\_____|_|\_\  \___/| .__/ \___|_| |_|
                                                                                     | |               
                                                                                     |_|               
              serveur : {self.listener.address[0]} 
              Port: {self.listener.address[1]}      
              """, log=self.log.logger)

    async def start(self):
        super().start()
        self.ordo_thread = Thread(target=self.ordo.start, daemon=True)
        self.ordo_thread.start()
        await self.init_block()
        while self.is_start():
            print(f"boucle n°{self.boucle}")
            self.init_tx()
            await asyncio.create_task(self.recv_msg())
            self.boucle += 1

    async def stop(self):
        self.ordo.stop()
        await super().stop()

    async def trt_cmd(self, **msg):
        from time import sleep
        if msg['command'] == 'get_services':
            await self.send_msg_common_rep('get_services')
            self.node = msg['node']
            await self.init_block()
        elif msg['command'] == 'trsf_ligne':
            self.lignes.append(await self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg))
            await self.send_msg_ctrl('done')
            await self.ins_ligne()
        elif msg['command'] == 'get_blk_id_prev_fabrik':
            self.blk_id_prev = await self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg)
            await self.init_block()
        else:
            await super().trt_cmd(**msg)

    async def trt_maj_conf(self):
        if self.ordo.execute('trt_blk'):
            self.ordo.del_task('trt_blk')
        await self.close_block()
        await self.send_block()
        await self.init_block()

    async def init_block(self):
        from lib.AlphaClient import AlphaClientFabrik
        from lib.block import Block
        if self.blk_id_prev is None:
            if self.node:
                AlphaClientFabrik.send_cmd(self.node[0], self.node[1], self.boucle, 'get_blk_id_prev_fabrik', 'AlphaClientFabrik', debug=False)
            else:
                couleurs.AffichageColor().msg_WARNING( "Attention pas de node encore connecté ! donc pas d'init block", self.log.logger)
        else:
            bloc = Block()
            bloc.bloc['blk_config'] = self.config
            bloc.bloc['blk_id_prev'] = self.blk_id_prev
            self.currentblock = bloc
            if not self.ordo.execute('trt_blk'):
                # self.ordo.add_task('trt_blk', True, self, minutes=1)
                self.ordo.add_task('trt_blk', True, self, seconds=15)

    async def close_block(self):
        bloc = self.currentblock
        self.currentblock = None
        bloc.set_hash()
        self.blk_id_prev = bloc.bloc['blk_id']
        self.blocks.append(bloc)

    async def send_block(self):
        from lib.AlphaClient import AlphaClientFabrik
        # AlphaClientFabrik.send_cmd(self.node[0], self.node[1], self.boucle, 'trsf_bloc', 'AlphaClientFabrik', debug=False, chaine=(list(self.services[0].keys())[0], repr(self.blocks.popleft().bloc)))
        AlphaClientFabrik.send_cmd(self.node[0], self.node[1], self.boucle, 'trsf_bloc', 'AlphaClientFabrik', debug=False, chaine=(list(self.services[0].keys())[0], self.blocks.popleft().bloc))

    async def ins_ligne(self): # TODO A voir !!!!
        from base64 import standard_b64decode
        if not self.ordo.execute('ins_ligne'):
            if len(self.lignes) > 0:
                secondes = 1 / len(self.lignes)
                if self.currentblock is not None:
                    self.currentblock.add_line(self.lignes.popleft())
            else:
                secondes = 1
            self.ordo.add_task('ins_ligne', True, self, seconds=secondes)
        else:
            if len(self.lignes) > 0:
                if self.currentblock is not None:
                    self.currentblock.add_line(self.lignes.popleft())
            else:
                self.ordo.del_task('ins_ligne')

    def load_config(self):
        return '0', {'PORT_FABRIK': '8020'}

