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
from time import sleep


class AlphaServer():
    __VERSION = '0.01'

    def __init__(self, host, port, pwd=None, debug=False):
        self.listener = Listener((host, port), pwd)
        self.conn = None
        self._debug = debug
        self.moduleManager = tools.ManagerClass(PATH_CMDS)
        self.pre_cmds = tools.ManagerClassPreCMDS(False)
        self.__is_start = False
        self.index = self.init_index()
        self.boucle = 0
        self.last_config_version, self.config = self.load_config()
        if self.moduleManager.isempty: couleurs.AffichageColor().msg_WARNING("I have no command vocabulary. I'm a baby !")
        if self._debug: couleurs.AffichageColor().msg_DEBUG(f"get_structCmds {type(self)} {repr(self.moduleManager.get_structCmds())}")

    @classmethod
    def get_VERSION(self):
        return self.__VERSION

    def send_msg(self, **dico):
        if self._debug: couleurs.AffichageColor().msg_DEBUG(f'dico {type(self)} {repr(dico)}')
        if self._debug: couleurs.AffichageColor().msg_DEBUG(f"listener.last_accepted {type(self)} {repr(self.listener.last_accepted)}")
        try:
            self.conn.send(dico)
        except:
            couleurs.AffichageColor().msg_FAIL(f'send error "send_msg" on {self.listener.last_accepted}')
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
         What does three up and three down mean to you Airman? une pub Citro??n ? (End of an inning?)""", bold=True)

    def start(self):
        self.__is_start = True
        self.msg_welcome()

    def stop(self):
        self.__is_start = False

    def is_start(self):
        return self.__is_start

    def recv_msg(self):
        try:
            msg = self.conn.recv()
            return [self.trt_msg(msg)]
        except EOFError:
            couleurs.AffichageColor().msg_FAIL(f"message error in 'recv_msg' with {self.listener.last_accepted}")
            pass
        except ConnectionResetError:
            couleurs.AffichageColor().msg_FAIL(f"Connection client error in 'recv_msg' from {self.listener.last_accepted}")
            pass

    # findef

    def init_tx(self):
        self.conn = self.listener.accept()
        couleurs.AffichageColor().msg_OK(f'Connected by {self.listener.last_accepted}')

    # findef

    def close(self):
        if self.listener is not None:
            self.listener.close()

    # findef

    def trt_msg(self, msg: dict):
        if self._debug: couleurs.AffichageColor().msg_DEBUG(f"trt_msg {type(self)} {repr(msg)}")

        # Le Client ne connait pas la commande donc envoie de la commande

        if msg['command'] is 'misunderstood':
            couleurs.AffichageColor().msg_FAIL('message incompris')
            couleurs.AffichageColor().msg_FAIL(msg, True)
            return 1

        # Ajout / MAJ d'une commande pour le serveur
        elif msg['command'] == 'get_struct_cmd':
            if self.moduleManager.isempty:  # le serveur ne connait pas la commande get_struct_cmd
                if msg['cmd_name'] == msg['command']:
                    # Pour amorcer la commande c'est le read_cmd V0.01 de la class get_struct_cmd
                    from os import path
                    from base64 import b64decode
                    with open(path.join('..', self.moduleManager.path, msg['file_name']), 'wb') as fic:
                        fic.write(b64decode(msg['file_content']))
                    self.moduleManager.add_cmd(msg['cmd_name'])
                    couleurs.AffichageColor().msg_WARNING(f"I just learned the command '{msg['cmd_name']}' it's COOL ! :)")
                else:
                    couleurs.AffichageColor().msg_FAIL(f"Je pratique couramment six millions de formes de communication... pour le moment il me faudrait connaitre la commande '{msg['command']}'")
                    self.send_msg_ctrl_legacy('done')
            else:  # utilisation de la derni??re version get_struct_cmd si le serveur l'a
                if msg['version_cmd'] == self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION():
                    self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).read_cmd(self, **msg)
                    self.send_msg_ctrl('done')
                else:
                    if msg['version_cmd'] > self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION():
                        if msg['cmd_name'] == msg['command']:
                            self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).read_cmd(self, **msg)
                            self.send_msg_ctrl('done')
                        else:
                            couleurs.AffichageColor().msg_WARNING(
                                f"wrong version of '{msg['command']}' from {msg['version_cmd']} to {self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION()}")
                            self.send_msg_ctrl('misunderstood')
                    else:
                        couleurs.AffichageColor().msg_WARNING(
                            f"the client version of command '{msg['command']}' is lower then me from {msg['version_cmd']} to {self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION()}.")
                        self.send_update_msg(msg['command'])
            return 0


        # Execution d'une commande en v??rifiant sa version
        elif msg['command'] in self.moduleManager.get_structCmds().keys():
            if msg['version_cmd'] == self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION():
                if 'get_entete_msg' in self.moduleManager.get_structCmds().keys():
                    self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class('get_entete_msg')).read_cmd(**msg)
                # self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg)
                self.trt_cmd(**msg)
                self.send_msg_ctrl('done')
                print('~' * 79)
            else:
                if msg['version_cmd'] > self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION():
                    couleurs.AffichageColor().msg_WARNING(
                        f"wrong version of '{msg['command']}' from {msg['version_cmd']} to {self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION()}")
                    self.send_msg_ctrl('misunderstood')
                else:
                    couleurs.AffichageColor().msg_WARNING(
                        f"the client version of command '{msg['command']}' is lower then me from {msg['version_cmd']} to {self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION()}.")
                    self.send_update_msg(msg['command'])


        else:
            couleurs.AffichageColor().msg_WARNING(f"I did not understand the command '{msg['command']}'")
            self.send_msg_ctrl('misunderstood')
        # self._debug: couleurs.AffichageColor().msg_DEBUG(repr(self.moduleManager.get_structCmds()))
        return 0

    # findef

    def trt_cmd(self, **msg):
        self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg)

    def send_msg_ctrl_legacy(self, cmd):
        msg = {
            'numero': '-1',
            'nom': tools.get_name(),
            'signature': hashlib.sha512("ns".encode()).hexdigest(),
            'version_cmd': '0',
            'command': cmd,
        }
        try:
            self.send_msg(**msg)
        except:
            couleurs.AffichageColor().msg_FAIL(f"send error 'send_msg_ctrl_legacy' on {self.listener.last_accepted}")
            pass

    # findef

    def send_msg_ctrl(self, cmd):
        msg = {
            'numero': self.boucle,
            'nom': tools.get_name(),
            'signature': hashlib.sha512("ns".encode()).hexdigest(),
        }
        msg.update(self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(cmd)).write_cmd())
        try:
            self.send_msg(**msg)
        except:
            couleurs.AffichageColor().msg_FAIL(f"send error 'send_msg_ctrl' on {self.listener.last_accepted}")
            pass

    # findef

    def send_msg_common(self, cmd):
        msg = {
            'numero': self.boucle,
            'nom': tools.get_name(),
            'signature': hashlib.sha512("ns".encode()).hexdigest(),
        }
        msg.update(self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(cmd)).write_cmd())
        try:
            self.send_msg(**msg)
        except:
            couleurs.AffichageColor().msg_FAIL(f"send error 'send_msg_common' on {self.listener.last_accepted}")
            pass

    def send_msg_common_rep(self, cmd, chaine=None):
        msg = {
            'numero': self.boucle,
            'nom': tools.get_name(),
            'signature': hashlib.sha512("ns".encode()).hexdigest(),
        }
        msg.update(self.pre_cmds.get_func_throught_module('pre_write_cmd')(self, cmd, chaine))
        msg.update(self.pre_cmds.get_func_throught_module('pre_write_cmd_rep')(self, cmd))
        try:
            self.send_msg(**msg)
        except:
            couleurs.AffichageColor().msg_FAIL(f"send error 'send_msg_common' on {self.listener.last_accepted}")
            pass

    def send_update_msg(self, cmd):
        if cmd in self.moduleManager.get_structCmds().keys():
            dico = {
                'numero': self.boucle,
                'nom': tools.get_name(),
                'signature': hashlib.sha512("ns".encode()).hexdigest(),
            }
            dico.update(self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class('lower_version')).write_cmd(self, cmd))
            if self._debug: couleurs.AffichageColor().msg_DEBUG(f"send_update_msg {type(self)} {repr(dico)}")
            try:
                self.send_msg(**dico)
            except:
                couleurs.AffichageColor().msg_FAIL(f"send error 'send_update_msg' on {self.listener.last_accepted}")
                pass
        else:
            print("commande inconnue")
            exit()

    def init_index(self):
        pass

    def load_config(self):
        return 0, {}


class AlphaServerNode(AlphaServer):

    def __init__(self, host, port, pwd=None, debug=False):
        super().__init__(host, port, pwd, debug)
        self.assembly = Assembly()
        self.parametres = {}
        self.clts = {}
        self.services = {'node': [self.listener.address[0], self.listener.address[1]], }
        self.ordo = OrdoNode()
        self.ordo_thread = None
        self.lignes = deque()
        self.servicesOK = False
        self.blk_id_prev = None

    def msg_welcome(self):
        couleurs.AffichageColor().msg_INFO(msg=f"""
   _____                                  _   _  ____  _____  ______                          
  / ____|                                | \ | |/ __ \|  __ \|  ____|                         
 | (___   ___ _ ____   _____ _   _ _ __  |  \| | |  | | |  | | |__      ___  _ __   ___ _ __  
  \___ \ / _ \ '__\ \ / / _ \ | | | '__| | . ` | |  | | |  | |  __|    / _ \| '_ \ / _ \ '_ \ 
  ____) |  __/ |   \ V /  __/ |_| | |    | |\  | |__| | |__| | |____  | (_) | |_) |  __/ | | |
 |_____/ \___|_|    \_/ \___|\__,_|_|    |_| \_|\____/|_____/|______|  \___/| .__/ \___|_| |_|
                                                                            | |               
                                                                            |_|               
        serveur : {self.listener.address[0]} 
        Port: {self.listener.address[1]}      
        """)

    def start(self):
        super().start()
        self.ordo_thread = Thread(target=self.ordo.start, daemon=True)
        self.ordo_thread.start()
        while self.is_start():
            print(f"boucle n??{self.boucle}")
            if not self.servicesOK: self.find_service()
            self.init_tx()
            self.recv_msg()
            self.boucle += 1

    def stop(self):
        super().stop()
        self.ordo.stop()

    def trt_cmd(self, **msg):
        from lib.AlphaClient import AlphaClientNode
        if msg['command'] == 'get_net_conf':
            self.send_msg_common_rep('get_net_conf')
            couleurs.AffichageColor().msg_INFO(f"{msg['nom']} demande les information r??seaux du serveur. Elles ont ??t?? transmises.")
        elif msg['command'] == 'get_services':
            if 'liste' in msg.keys() and msg['liste'] != "":
                r = self.pre_cmds.get_func_throught_module('pre_read_cmd')(**msg)
                self.services.update(r)
                couleurs.AffichageColor().msg_INFO(f"{msg['nom']} a comme service {self.pre_cmds.get_func_throught_module('pre_read_cmd')(**msg)}")
            else:
                self.send_msg_common_rep('get_services')
        elif msg['command'] == 'trsf_config':
            v, r = self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg)
            old_vers = self.last_config_version
            if int(self.last_config_version) < int(v):
                self.last_config_version = v
                self.config = r
                couleurs.AffichageColor().msg_WARNING(f"Changement de configuration. \n"
                                                      f"Passage de la version : {old_vers} ?? la version : {self.last_config_version}")
        elif msg['command'] == 'trsf_ligne':
            if 'fabrik' in self.services.keys():
                AlphaClientNode.send_cmd(self.services['fabrik'][0], self.services['fabrik'][1], self.boucle, 'trsf_line', 'AlphaClientNode', debug=False, chaine=str(msg['ligne']))
            else:
                self.lignes.append(msg['ligne'])
                couleurs.AffichageColor().msg_WARNING(f"ATTENTION ! node non connect?? ?? un service Fabrik ou ne connaissant pas un node avec le service. \n"
                                                      f"Stockage de la ligne. Nombre de ligne stock??es : {len(self.lignes)}")
        elif msg['command'] == 'get_blk_id_prev_fabrik':
            if self.blk_id_prev is not None:
                r = AlphaClientNode.send_cmd(self.services['fabrik'][0], self.services['fabrik'][1], self.boucle, 'get_blk_id_prev_fabrik', 'AlphaClientNode', debug=False, chaine=self.blk_id_prev)
                print('pour fabik', r)
            else:
                r = AlphaClientNode.send_cmd(self.services['cache'][0], self.services['cache'][1], self.boucle, 'get_blk_id_prev', 'AlphaClientNode', debug=False)
                print('pour cache', r)
        elif msg['command'] == 'get_blk_id_prev':
            if 'blk_id_prev' in msg.keys() and msg['blk_id_prev'] != "":
                self.blk_id_prev = msg['blk_id_prev']
                r = AlphaClientNode.send_cmd(self.services['fabrik'][0], self.services['fabrik'][1], self.boucle, 'get_blk_id_prev_fabrik', 'AlphaClientNode', debug=False, chaine=self.blk_id_prev)
                print('pour fabik bis', r)
        else:
            super().trt_cmd(**msg)

    def find_node(self):
        if self.assembly:
            pass

    def add_service_lst(self):
        pass

    def init_assembly(self, ip, port):
        from lib.AlphaClient import AlphaClientNode
        ip, port = self.first_contact
        c = AlphaClientNode(ip, port)
        # A FINIR

    def find_service(self):
        from lib.parametres import Params
        p = Params()
        services = ['CACHE', 'WALLET', 'FABRIK', 'VALIDATOR']
        services_actifs = []
        port_s = "_S"
        ip_service = "IP_"
        ports_services = [f"PORT_{e}" for e in services]
        ports_services += [f"PORT_{e}{port_s}" for e in services]

        for elem in ports_services:
            if elem in p.PARAMS.keys() and p.PARAMS[elem] != '':
                port = int(p.PARAMS[elem])
                services_actifs.append(elem.split('_')[1])
                if f"{ip_service}{elem.split('_')[1]}" in p.PARAMS.keys() and p.PARAMS[f"{ip_service}{elem.split('_')[1]}"] != '':
                    host = p.PARAMS[f"{ip_service}{elem.split('_')[1]}"]
                else:
                    host = self.listener.address[0]
                self.test_service(elem.split('_')[1], host, port)
        self.servicesOK = not tools.lst2bool(list(map(self.ordo.execute, [f"test_service_{x}" for x in services_actifs])))

    def test_service(self, service, host, port):
        result = self._send_get_services(host, port)
        if self._debug: couleurs.AffichageColor().msg_DEBUG(f"result _send_get_services {result}")
        if result < 0:
            couleurs.AffichageColor().msg_WARNING(
                f"Le service {service} d??clar?? ({host}:{port}) dans le param??trage ne r??pond pas \n"
                f"Reprogrammation du test...")
            if not self.ordo.execute(f'test_service_{service}'):
                self.ordo.add_task(f'test_service_{service}', True, self, service, host, port, seconds=10)
        else:
            couleurs.AffichageColor().msg_INFO(f"Le service {service} est ouvert ")
            if self._debug: couleurs.AffichageColor().msg_DEBUG(f"ordo.tasks {self.ordo.tasks}")
            if self.ordo.execute(f'test_service_{service}'):
                self.ordo.del_task(f'test_service_{service}')

    def _send_get_services(self, ip, port):
        from lib.AlphaClient import AlphaClientNode
        try:
            r = AlphaClientNode(ip, port, debug=1).send_cmd(ip, port, self.boucle, 'get_services', 'AlphaClientNode', debug=False, chaine=str(self.listener.address))
            if r is not None:
                if type(r) is str or type(r) is list:
                    self.services.update(r[0])
                    couleurs.AffichageColor().msg_INFO(f"le serveur {ip} a comme service {repr(r)}")
                    self.trt_services()
        except ConnectionRefusedError:
            return -1
        return 0

    def trt_services(self):
        if 'fabrik' in self.services.keys():
            if int(self.last_config_version) > 0:
                self.trt_config('fabrik'.upper())
            else:
                if not self.ordo.execute('trt_config_FABRIK'):
                    self.ordo.add_task('trt_config_FABRIK', True, self, 'fabrik'.upper(), seconds=5)
        elif 'validator' in self.services.keys():
            if int(self.last_config_version) > 0:
                self.trt_config('validator'.upper())
            else:
                if not self.ordo.execute('trt_config_VALIDATOR'):
                    self.ordo.add_task('trt_config_VALIDATOR', True, 'validator'.upper(), self, seconds=5)

    def trt_config(self, service):
        from lib.AlphaClient import AlphaClientNode
        if int(self.last_config_version) > 0:
            r = AlphaClientNode.send_cmd(self.services[service.casefold()][0], self.services[service.casefold()][1], self.boucle, 'trsf_config', 'AlphaClientNode', chaine=repr((self.config, self.last_config_version)))
            if r:
                if self.ordo.execute(f'trt_config_{service}'):
                    self.ordo.del_task(f'trt_config_{service}')
        else:
            if not self.ordo.execute(f'trt_config_{service}'):
                self.ordo.add_task(f'trt_config_{service}', True, self, service, seconds=5)

    def load_config(self):
        return '0', {'PORT_NODE': '8000'}

    def __del__(self):
        self.ordo.stop()


class AlphaServerCache(AlphaServer):

    def __init__(self, host, port, pwd=None, debug=False):

        super().__init__(host, port, pwd, debug)
        self.services = [{'cache': [self.listener.address[0], self.listener.address[1]]}, ]
        self.node = ()
        self.ordo = OrdoCache()
        self.ordo_thread = None
        self.last_config_version, self.config = self.load_config()
        self.blk_id_prev = max(self.index['id_obj_prev'], key=itemgetter(0))[0]

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
           """)

    def start(self):
        super().start()
        self.ordo_thread = Thread(target=self.ordo.start, daemon=True)
        self.ordo_thread.start()
        couleurs.AffichageColor().msg_INFO(f"Chargement de la configuration \n"
                                           f"version : {self.last_config_version}\n"
                                           f"{repr(self.config)}")
        couleurs.AffichageColor().msg_INFO(f"{len(self.index)} blocs trouv??s dans le cache")
        while self.is_start():
            print(f"boucle n??{self.boucle}")
            self.init_tx()
            self.recv_msg()
            self.boucle += 1

    def trt_cmd(self, **msg):
        from lib.AlphaClient import AlphaClientCache
        if msg['command'] == 'get_services':
            self.send_msg_common_rep('get_services')
            self.node = msg['node']
            AlphaClientCache.send_cmd(self.node[0], self.node[1], self.boucle, 'trsf_config', 'AlphaClientCache', chaine=str((self.config, self.last_config_version)))
        elif msg['command'] == 'get_blk_id_prev':
            self.send_msg_ctrl('done')
            AlphaClientCache.send_cmd(self.node[0], self.node[1], self.boucle, 'get_blk_id_prev', 'AlphaClientCache', debug=False, chaine=self.blk_id_prev)
        else:
            super().trt_msg(**msg)

    def cache_blk(self, blk):
        from lib.stock_hdd import hdd
        hdd().write_block(blk)

    def init_index(self):
        pass  # A faire pour un cache normal

    def load_config(self):
        # from lib.stock_hdd import hdd # future implementation
        tupl = max(self.index['id_obj_prev'], key=itemgetter(0))
        return tupl[1].get_config_version(), tupl[1].blk_config

    def _send_config(self, ip, port):
        from lib.AlphaClient import AlphaClientCache
        try:
            r = AlphaClientCache.send_cmd(ip, port, self.boucle, 'trsf_config', 'AlphaClientCache', chaine=str((self.config, self.last_config_version)))
        except ConnectionRefusedError:
            return -1
        return 0


class AlphaServerSuperCache(AlphaServerCache):

    def __init__(self, host, port, pwd=None, debug=False):
        super().__init__(host, port, pwd, debug)
        self.services.append({'supercache': [self.listener.address[0], self.listener.address[1]]})

    def msg_welcome(self):
        couleurs.AffichageColor().msg_INFO(msg=f"""

                                           /$$$$$$  /$$   /$$ /$$$$$$$  /$$$$$$$$ /$$$$$$$ 
                                          /$$__  $$| $$  | $$| $$__  $$| $$_____/| $$__  $$
   _____                                 | $$  \__/| $$  | $$| $$  \ $$| $$      | $$  \ $$   _____          _____ _    _ ______                          
  / ____|                                |  $$$$$$ | $$  | $$| $$$$$$$/| $$$$$   | $$$$$$$/  / ____|   /\   / ____| |  | |  ____|                         
 | (___   ___ _ ____   _____ _   _ _ __   \____  $$| $$  | $$| $$____/ | $$__/   | $$__  $$ | |       /  \ | |    | |__| | |__      ___  _ __   ___ _ __  
  \___ \ / _ \ '__\ \ / / _ \ | | | '__|  /$$  \ $$| $$  | $$| $$      | $$      | $$  \ $$ | |      / /\ \| |    |  __  |  __|    / _ \| '_ \ / _ \ '_ \ 
  ____) |  __/ |   \ V /  __/ |_| | |    |  $$$$$$/|  $$$$$$/| $$      | $$$$$$$$| $$  | $$ | |____ / ____ \ |____| |  | | |____  | (_) | |_) |  __/ | | |
 |_____/ \___|_|    \_/ \___|\__,_|_|     \______/  \______/ |__/      |________/|__/  |__/  \_____/_/    \_\_____|_|  |_|______|  \___/| .__/ \___|_| |_|
                                                                                                                                        | |               
                                                                                                                                        |_|               
              serveur : {self.listener.address[0]} 
              Port: {self.listener.address[1]}      
              """)

    def init_index(self):
        from lib.stock_hdd import hdd
        from lib.tools import find_root
        index = {"id_obj_prev": hdd().liste_bloc(os.path.join(find_root(), "cache"))}
        return index


class AlphaServerFabrik(AlphaServer):

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
              """)

    def start(self):
        super().start()
        self.ordo_thread = Thread(target=self.ordo.start, daemon=True)
        self.ordo_thread.start()
        #self.init_block()
        while self.is_start():
            print(f"boucle n??{self.boucle}")
            self.init_tx()
            sleep(0.5)
            self.recv_msg()
            self.boucle += 1

    def trt_cmd(self, **msg):
        if msg['command'] == 'get_services':
            self.send_msg_common_rep('get_services')
            self.node = msg['node']
        elif msg['command'] == 'trsf_config':
            v, r = self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg)
            old_vers = self.last_config_version
            if int(self.last_config_version) < int(v):
                self.last_config_version = v
                self.config = r
                couleurs.AffichageColor().msg_WARNING(f"Changement de configuration. \n"
                                                      f"Passage de la version : {old_vers} ?? la version : {self.last_config_version}")
                self.init_block()
        elif msg['command'] == 'trsf_ligne':
            self.ins_ligne(**msg)
        elif msg['command'] == 'get_blk_id_prev_fabrik':
            self.blk_id_prev = msg['blk_id_prev']
            print(self.blk_id_prev)
            self.init_block()
        else:
            super().trt_msg(**msg)

    def init_block(self):
        from lib.AlphaClient import AlphaClientFabrik
        from lib.block import Block
        if self.blk_id_prev is None:
            if self.node:
                AlphaClientFabrik.send_cmd(self.node[0], self.node[1], self.boucle, 'get_blk_id_prev_fabrik', 'AlphaClientFabrik', debug=False)
            else:
                couleurs.AffichageColor().msg_WARNING("Attention pas de node encore connect?? ! donc pas d'init block")
        else:
            if not self.ordo.execute('trt_blk'):
                bloc = Block()
                bloc.bloc['blk_config'] = self.config
                bloc.bloc['blk_id_prev'] = self.blk_id_prev
                self.currentblock = bloc
                self.ordo.add_task('trt_blk', True, self, minutes=1)
            else:
                bloc = Block()
                bloc.bloc['blk_config'] = self.config
                bloc.bloc['blk_id_prev'] = self.blk_id_prev
                self.currentblock = bloc

    def close_block(self):
        bloc = self.currentblock
        self.currentblock = None
        bloc.set_hash()
        self.blk_id_prev = bloc.bloc['blk_id']
        self.blocks.append(bloc)

    def send_block(self):
        from lib.AlphaClient import AlphaClientFabrik
        from base64 import standard_b64encode
        from pickle import dumps
        if 'validator' in self.services.keys():
            AlphaClientFabrik.send_cmd(self.services['validator'][0], self.services['validator'][1], self.boucle, 'trsf_line', 'AlphaClientFabrik', debug=False, chaine=str(standard_b64encode(dumps(self.blocks.popleft()))))  # A voir
        else:
            # self.lignes.append(msg['ligne'])
            couleurs.AffichageColor().msg_WARNING(f"ATTENTION ! node non connect?? ?? un service Fabrik ou ne connaissant pas un node avec le service. \n"
                                                  f"Stockage de la ligne. Nombre de ligne stock??es : {len(self.lignes)}")

    def ins_ligne(self):
        from base64 import standard_b64decode
        if not self.ordo.execute('ins_ligne'):
            if len(self.lignes) > 0:
                if self.currentblock is not None:
                    self.currentblock.add_line_raw(standard_b64decode(self.lignes.popleft()))
                secondes = 1 / len(self.lignes)
                self.ordo.add_task('trt_blk', True, self, secondes=secondes)
        else:
            if len(self.lignes) > 0:
                if self.currentblock is not None:
                    self.currentblock.add_line_raw(self.lignes.popleft())
            else:
                self.ordo.del_task('ins_ligne')

    def load_config(self):
        return '0', {'PORT_FABRIK': '8020'}


class AlphaServerValidator(AlphaServer):

    def __init__(self, host, port, pwd=None, debug=False):
        super().__init__(host, port, pwd, debug)
        self.services = [{'Validator': [self.listener.address[0], self.listener.address[1]]}, ]
        self.currentblock = None
        self.queue = deque()

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
                 """)

    def recev_block(self):
        pass

    def sign_block(self):
        pass

    def load_config(self):
        return '0', {'PORT_VALIDATOR': '8030'}


class AlphaServerwallet(AlphaServer):

    def msg_welcome(self):
        couleurs.AffichageColor().msg_INFO(msg=f"""

   _____                                  __  __  ____  _    _ _                                        
  / ____|                                |  \/  |/ __ \| |  | | |        /\                             
 | (___   ___ _ ____   _____ _   _ _ __  | \  / | |  | | |  | | |       /  \      ___  _ __   ___ _ __  
  \___ \ / _ \ '__\ \ / / _ \ | | | '__| | |\/| | |  | | |  | | |      / /\ \    / _ \| '_ \ / _ \ '_ \ 
  ____) |  __/ |   \ V /  __/ |_| | |    | |  | | |__| | |__| | |____ / ____ \  | (_) | |_) |  __/ | | |
 |_____/ \___|_|    \_/ \___|\__,_|_|    |_|  |_|\____/ \____/|______/_/    \_\  \___/| .__/ \___|_| |_|
                                                                                      | |               
                                                                                      |_|               
                    serveur : {self.listener.address[0]} 
                    Port: {self.listener.address[1]}      
                    """)

    def load_config(self):
        return 0, {'PORT_WALLET': '8040'}


class Assembly:
    class Node:

        def __init__(self, ip, port, name='', services='', security='', public_key=''):
            self.ip = ip
            self.name = name
            self.port = port
            self.security = security
            self.public_key = public_key
            self.services = services
            self.timestamp = datetime.datetime.now().timestamp()

    class CacheNode:

        def __init__(self, max=3):
            self.candidats = []
            self.candidats_index = {}
            self.lasterefresh = datetime.datetime.now().timestamp()
            self.max_candidats = max

    def __init__(self, max=3):
        import datetime
        self.participants = []
        self.participants_index = {}
        self.isempty = self.participants != []
        self.last_time_action = datetime.datetime.now().timestamp()
        self.max_participants = max
        self.cache = Assembly.CacheNode()

    # A FAIRE Rendre plus autonome la class Assembly en s'initialisant elle m??me et g??rant les time out des participants

    def add_node(self, ip, port, name='', services='', security='', public_key=''):
        if len(self.participants) < self.max_participants:
            self.participants.append(Assembly.Node(ip, port, name, services, security, public_key))
            # A FAIRE : Indexation du node
        else:
            # if len(self.cache.candidats) < self.cache.max_candidats: plus tard
            self.cache.candidats.append(Assembly.Node(ip, port, name, services, security, public_key))
            # A FAIRE : Indexation du node

    def get_listes(self):
        return {'participants': self.participants, 'candidats': self.cache.candidats}


async def main():
    from lib.parametres import Params
    port = int(Params().PARAMS['PORT_NODE'])
    host = tools.get_ip()
    loop = asyncio.get_running_loop()

    l = AlphaServerNode(host, port, debug=False)
    i = 0
    l.start()


if __name__ == "__main__": asyncio.run(main())