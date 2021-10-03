import asyncio
import datetime
import hashlib
import os
from collections import deque
from multiprocessing.connection import Listener
from operator import itemgetter
from threading import *
from etc.contants import PATH_CMDS
from lib import couleurs, tools
from lib.ordonnanceur import OrdoNode, OrdoCache, OrdoFabrik
from lib.logs import Log


class alphaserver:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class AlphaServer:

    __VERSION = '0.01'

    def __init__(self, host, port, pwd=None, debug=False):
        self.listener = Listener((host, port), pwd)
        self.conn = None
        self._debug = debug
        self.moduleManager = tools.ManagerClass(PATH_CMDS)
        self.pre_cmds = tools.ManagerClassPreCMDS(True)
        self.__is_start = False
        self.index = self.init_index()
        self.boucle = 0
        self.last_config_version, self.config = self.load_config()
        self.log = None
        if self.moduleManager.isempty: couleurs.AffichageColor().msg_WARNING("I have no command vocabulary. I'm a baby !")
        if self._debug: couleurs.AffichageColor().msg_DEBUG(f"get_structCmds {type(self)} {repr(self.moduleManager.get_structCmds())}")


    @classmethod
    def get_VERSION(self):
        return self.__VERSION

    async def send_msg(self, **dico):
            if self._debug: couleurs.AffichageColor().msg_DEBUG(f'dico {type(self)} {repr(dico)}', self.log.logger)
            if self._debug: couleurs.AffichageColor().msg_DEBUG(f"listener.last_accepted {type(self)} {repr(self.listener.last_accepted)}", self.log.logger)
            try:
                self.conn.send(dico)
            except:
                couleurs.AffichageColor().msg_FAIL(f'send error "send_msg" on {self.listener.last_accepted}', self.log.logger)
                pass
    # findef

    def msg_welcome(self):
        couleurs.AffichageColor().msg_INFO(msg="""
           _____                                         _   __  __                  _              __      ___      _                           _ 
          / ____|                                       | | |  \/  |                (_)             \ \    / (_)    | |                         | |
         | |  __  ___   ___   ___   ___   ___   ___   __| | | \  / | ___  _ __ _ __  _ _ __   __ _   \ \  / / _  ___| |_ _ __ ___   __ _ _ __   | |
         | | |_ |/ _ \ / _ \ / _ \ / _ \ / _ \ / _ \ / _` | | |\/| |/ _ \| '__| '_ \| | '_ \ / _` |   \ \/ / | |/ _ \ __| '_ ` _ \ / _` | '_ \  | |
         | |__| | (_) | (_) | (_) | (_) | (_) | (_) | (_| | | |  | | (_) | |  | | | | | | | | (_| |    \  /  | |  __/ |_| | | | | | (_| | | | | |_|
          \_____|\___/ \___/ \___/ \___/ \___/ \___/ \__,_| |_|  |_|\___/|_|  |_| |_|_|_| |_|\__, |     \/   |_|\___|\__|_| |_| |_|\__,_|_| |_| (_)
                                                                                              __/ |                                                
                                                                                             |___/                                                 

         It's gonna be hot and wet! That's nice if you're with a lady, but it ain't no good if you're in the jungle.
         What does three up and three down mean to you Airman? une pub Citroën ? (End of an inning?)""", bold=True)

    def msg_goodbye(self):
        couleurs.AffichageColor().msg_INFO(msg="""
          _____  ____   ____  _____  ______     ________   _ _ _ 
         / ____|/ __ \ / __ \|  __ \|  _ \ \   / /  ____| | | | |
        | |  __| |  | | |  | | |  | | |_) \ \_/ /| |__    | | | |
        | | |_ | |  | | |  | | |  | |  _ < \   / |  __|   | | | |
        | |__| | |__| | |__| | |__| | |_) | | |  | |____  |_|_|_|
         \_____|\____/ \____/|_____/|____/  |_|  |______| (_|_|_)
               """, log=self.log.logger)

    def start(self):
        self.__is_start = True
        self.msg_welcome()

    async def stop(self):
        self.__is_start = False
        self.msg_goodbye()

    def is_start(self):
        return self.__is_start

    async def recv_msg(self):
        try:
            msg = self.conn.recv()
            return await asyncio.wait([self.trt_msg(msg)])
        except EOFError:
            couleurs.AffichageColor().msg_FAIL(f"message error in 'recv_msg' with {self.listener.last_accepted}", self.log.logger)
            pass
        except ConnectionResetError:
            couleurs.AffichageColor().msg_FAIL(f"Connection client error in 'recv_msg' from {self.listener.last_accepted}", self.log.logger)
            pass
    # findef

    def init_tx(self):
        self.conn = self.listener.accept()
        couleurs.AffichageColor().msg_OK(f'Connected by {self.listener.last_accepted}', self.log.logger)
    # findef

    def close(self):
            if self.listener is not None:
                self.listener.close()
    # findef

    async def trt_msg(self, msg: dict):
        if self._debug: couleurs.AffichageColor().msg_DEBUG(f"trt_msg {type(self)} {repr(msg)}", self.log.logger)

        #Le Client ne connait pas la commande donc envoie de la commande

        if msg['command'] is 'misunderstood':
            couleurs.AffichageColor().msg_FAIL('message incompris', self.log.logger)
            couleurs.AffichageColor().msg_FAIL(msg, self.log.logger, True)
            return 1

        # Ajout / MAJ d'une commande pour le serveur
        elif msg['command'] == 'get_struct_cmd':
            if self.moduleManager.isempty: # le serveur ne connait pas la commande get_struct_cmd
                if msg['cmd_name'] == msg['command']:
                    # Pour amorcer la commande c'est le read_cmd V0.01 de la class get_struct_cmd
                    from os import path
                    from base64 import b64decode
                    with open(path.join('..', self.moduleManager.path, msg['file_name']), 'wb') as fic:
                        fic.write(b64decode(msg['file_content']))
                    self.moduleManager.add_cmd(msg['cmd_name'])
                    couleurs.AffichageColor().msg_WARNING(f"I just learned the command '{msg['cmd_name']}' it's COOL ! :)", self.log.logger)
                else:
                    couleurs.AffichageColor().msg_FAIL(f"Je pratique couramment six millions de formes de communication... pour le moment il me faudrait connaitre la commande '{msg['command']}'", self.log.logger)
                    await self.send_msg_ctrl_legacy('done')
            else: # utilisation de la dernière version get_struct_cmd si le serveur l'a
                if msg['version_cmd'] == self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION():
                    self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).read_cmd(self, **msg)
                    await self.send_msg_ctrl('done')
                else:
                    if msg['version_cmd'] > self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION():
                        if msg['cmd_name'] == msg['command']:
                            self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).read_cmd(self, **msg)
                            await self.send_msg_ctrl('done')
                        else:
                            couleurs.AffichageColor().msg_WARNING(f"wrong version of '{msg['command']}' from {msg['version_cmd']} to {self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION()}", self.log.logger)
                            await self.send_msg_ctrl('misunderstood')
                    else:
                        couleurs.AffichageColor().msg_WARNING(f"the client version of command '{msg['command']}' is lower then me from {msg['version_cmd']} to {self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION()}.", self.log.logger)
                        await self.send_update_msg(msg['command'])
            return 0


        # Execution d'une commande en vérifiant sa version
        elif msg['command'] in self.moduleManager.get_structCmds().keys():
            if msg['version_cmd'] == self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION():
                if 'get_entete_msg' in self.moduleManager.get_structCmds().keys():
                    self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class('get_entete_msg')).read_cmd(**msg)
                #await self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg)
                await self.trt_cmd(**msg)
                await self.send_msg_ctrl('done')
                print('~' * 79)
            else:
                if msg['version_cmd'] > self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION():
                    couleurs.AffichageColor().msg_WARNING(f"wrong version of '{msg['command']}' from {msg['version_cmd']} to {self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION()}", self.log.logger)
                    await self.send_msg_ctrl('misunderstood')
                else:
                    couleurs.AffichageColor().msg_WARNING(f"the client version of command '{msg['command']}' is lower then me from {msg['version_cmd']} to {self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION()}.", self.log.logger)
                    await self.send_update_msg(msg['command'])


        else:
            couleurs.AffichageColor().msg_WARNING(f"I did not understand the command '{msg['command']}'", self.log.logger)
            await self.send_msg_ctrl('misunderstood')
        # self._debug: couleurs.AffichageColor().msg_DEBUG(repr(self.moduleManager.get_structCmds()))
        return 0
    # findef

    async def trt_cmd(self, **msg):
        if msg['command'] == 'stop':
            await self.send_msg_ctrl('done')
            await self.stop()
        elif msg['command'] == 'trsf_config':
            v, r = await self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg)
            old_vers = self.last_config_version
            if int(self.last_config_version) < int(v):
                self.last_config_version = v
                self.config = r
                couleurs.AffichageColor().msg_WARNING(f"Changement de configuration. \n"
                                                      f"Passage de la version : {old_vers} à la version : {self.last_config_version}")
                await self.trt_maj_conf()
        else:
            await self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg)

    async def trt_maj_conf(self):
        pass

    async def send_msg_ctrl_legacy(self, cmd):
        msg = {
            'numero': '-1',
            'nom': tools.get_name(),
            'signature': hashlib.sha512("ns".encode()).hexdigest(),
            'version_cmd': '0',
            'command': cmd,
        }
        try:
            await self.send_msg(**msg)
        except:
            couleurs.AffichageColor().msg_FAIL(f"send error 'send_msg_ctrl_legacy' on {self.listener.last_accepted}", self.log.logger)
            pass

    # findef

    async def send_msg_ctrl(self, cmd):
        msg = {
            'numero': self.boucle,
            'nom': tools.get_name(),
            'signature': hashlib.sha512("ns".encode()).hexdigest(),
        }
        msg.update(self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(cmd)).write_cmd())
        try:
            await self.send_msg(**msg)
        except:
            couleurs.AffichageColor().msg_FAIL(f"send error 'send_msg_ctrl' on {self.listener.last_accepted}", self.log.logger)
            pass
    # findef

    async def send_msg_common(self, cmd):
        msg = {
            'numero': self.boucle,
            'nom': tools.get_name(),
            'signature': hashlib.sha512("ns".encode()).hexdigest(),
        }
        msg.update(self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(cmd)).write_cmd())
        try:
            await self.send_msg(**msg)
        except:
            couleurs.AffichageColor().msg_FAIL(f"send error 'send_msg_common' on {self.listener.last_accepted}", self.log.logger)
            pass

    async def send_msg_common_rep(self, cmd, chaine=None):
        msg = {
            'numero': self.boucle,
            'nom': tools.get_name(),
            'signature': hashlib.sha512("ns".encode()).hexdigest(),
        }
        msg.update(await self.pre_cmds.get_func_throught_module('pre_write_cmd')(self, cmd, chaine))
        msg.update(await self.pre_cmds.get_func_throught_module('pre_write_cmd_rep')(self, cmd))
        try:
            await self.send_msg(**msg)
        except:
            couleurs.AffichageColor().msg_FAIL(f"send error 'send_msg_common' on {self.listener.last_accepted}", self.log.logger)
            pass

    async def send_update_msg(self, cmd):
        if cmd in self.moduleManager.get_structCmds().keys():
            dico = {
                'numero':self.boucle,
                'nom': tools.get_name(),
                'signature': hashlib.sha512("ns".encode()).hexdigest(),
            }
            dico.update(self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class('lower_version')).write_cmd(self, cmd))
            if self._debug: couleurs.AffichageColor().msg_DEBUG(f"send_update_msg {type(self)} {repr(dico)}", self.log.logger)
            try:
                await self.send_msg(**dico)
            except:
                couleurs.AffichageColor().msg_FAIL(f"send error 'send_update_msg' on {self.listener.last_accepted}", self.log.logger)
                pass
        else:
            print("commande inconnue")
            exit()

    def init_index(self):
        pass

    def load_config(self):
        return 0, {}


async def main():
    from lib.parametres import Params
    from lib.alphaservernode import AlphaServerNode
    port = int(Params().PARAMS['PORT_NODE'])
    host = tools.get_ip()
    loop = asyncio.get_running_loop()

    l = AlphaServerNode(host, port, debug=False)
    i = 0
    await l.start()


if __name__ == "__main__": asyncio.run(main())