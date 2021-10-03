import asyncio
import os
from collections import deque
from lib import couleurs, tools
from lib.logs import Log
from lib.alphaserver import AlphaServer


class alphaservervalidator:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class AlphaServerValidator(AlphaServer):

    __VERSION = '0.01'

    def __init__(self, host, port, pwd=None, debug=False):
        super().__init__(host, port, pwd, debug)
        self.services = [{'validator': [self.listener.address[0], self.listener.address[1]]}, ] # TODO supprimer la notion de list
        self.currentblock = None
        self.node = None
        self.blocks = deque()
        self.log = Log('validator', os.path.join(tools.find_root(), 'log', 'validator.log'))



    def msg_welcome(self):
        couleurs.AffichageColor().msg_INFO(msg=f"""

   _____                                 __      __     _      _____ _____       _______ ____  _____                           
  / ____|                                \ \    / /\   | |    |_   _|  __ \   /\|__   __/ __ \|  __ \                          
 | (___   ___ _ ____   _____ _   _ _ __   \ \  / /  \  | |      | | | |  | | /  \  | | | |  | | |__) |   ___  _ __   ___ _ __  
  \___ \ / _ \ '__\ \ / / _ \ | | | '__|   \ \/ / /\ \ | |      | | | |  | |/ /\ \ | | | |  | |  _  /   / _ \| '_ \ / _ \ '_ \ 
  ____) |  __/ |   \ V /  __/ |_| | |       \  / ____ \| |____ _| |_| |__| / ____ \| | | |__| | | \ \  | (_) | |_) |  __/ | | |
 |_____/ \___|_|    \_/ \___|\__,_|_|        \/_/    \_\______|_____|_____/_/    \_\_|  \____/|_|  \_\  \___/| .__/ \___|_| |_|
                                                                                                             | |               
                                                                                                             |_|               
                 serveur : {self.listener.address[0]} 
                 Port: {self.listener.address[1]}      
                 """, log=self.log.logger)

    async def start(self):
        super().start()
        #self.ordo_thread = Thread(target=self.ordo.start, daemon=True)
        #self.ordo_thread.start()
        while self.is_start():
            print(f"boucle n°{self.boucle}")
            self.init_tx()
            await asyncio.create_task(self.recv_msg())
            self.boucle += 1

    async def stop(self):
        await super().stop()

    async def trt_cmd(self, **msg):
        from lib.block import Block
        if msg['command'] == 'get_services':
            await self.send_msg_common_rep('get_services')
            self.node = msg['node']
        elif msg['command'] == 'trsf_bloc':
            ori, blc = await self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg)
            await self.send_msg_ctrl('done')
            self.currentblock = Block(blc,"0.1.0")
            await self.sign_block()
            await self.send_block()
        else:
            await super().trt_cmd(**msg)

    async def sign_block(self):
        import hashlib
        import datetime
        self.currentblock.bloc['blk_signature'] = hashlib.sha512(f"{self.listener.address[0]}:{datetime.datetime.now().timestamp() * 1000000}".encode()).hexdigest()
        self.currentblock.bloc['blk_signature_timestamp'] = int(datetime.datetime.now().timestamp() * 1000000)

    async def send_block(self):
        from lib.AlphaClient import AlphaClientValidator
        AlphaClientValidator.send_cmd(self.node[0], self.node[1], self.boucle, 'trsf_bloc', 'AlphaClientValidator', debug=False, chaine=(list(self.services[0].keys())[0], self.currentblock.bloc))

    def load_config(self):
        return '0', {'PORT_VALIDATOR': '8030'}

