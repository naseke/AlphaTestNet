import asyncio
import os
from collections import deque
from threading import *
from lib import couleurs, tools
from lib.ordonnanceur import OrdoNode
from lib.logs import Log
from lib.alphaserver import AlphaServer


class alphaservernode:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class AlphaServerNode(AlphaServer):

    __VERSION = '0.01'

    def __init__(self, host, port, pwd=None, debug=False):
        super().__init__(host, port, pwd, debug)
        self.assembly = Assembly()
        self.parametres = {}
        self.clts = {}
        self.services = {'node': [self.listener.address[0], self.listener.address[1]], }
        self.ordo = OrdoNode()
        self.ordo_thread = None
        self.lignes = deque()
        self.blocs_f = deque()
        self.blocs_v = deque()
        self.servicesOK = False
        self.blk_id_prev = None
        self.log = Log('node', os.path.join(tools.find_root(), 'log', 'node.log'))

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
        """, log=self.log.logger)

    async def start(self):
        super().start()
        self.ordo_thread = Thread(target=self.ordo.start, daemon=True)
        self.ordo_thread.start()
        while self.is_start():
            print(f"boucle n°{self.boucle}")
            if not self.servicesOK: await asyncio.create_task(self.find_service())
            self.init_tx()
            await asyncio.create_task(self.recv_msg())
            self.boucle += 1

    async def stop(self):
        self.ordo.stop()
        await super().stop()

    async def trt_cmd(self, **msg):
        from lib.AlphaClient import AlphaClientNode
        if msg['command'] == 'get_net_conf':
            await self.send_msg_common_rep('get_net_conf')
            couleurs.AffichageColor().msg_INFO(f"{msg['nom']} demande les information réseaux du serveur. Elles ont été transmises.", self.log.logger)
        elif msg['command'] == 'get_services':
            if 'liste' in msg.keys() and msg['liste'] != "":
                r = self.pre_cmds.get_func_throught_module('pre_read_cmd')(**msg)
                self.services.update(r)
                couleurs.AffichageColor().msg_INFO(f"{msg['nom']} a comme service {await self.pre_cmds.get_func_throught_module('pre_read_cmd')(**msg)}", self.log.logger)
            else:
                await self.send_msg_common_rep('get_services')

        elif msg['command'] == 'trsf_ligne':
            if 'fabrik' in self.services.keys():
                AlphaClientNode.send_cmd(self.services['fabrik'][0], self.services['fabrik'][1], self.boucle, 'trsf_ligne', 'AlphaClientNode', debug=False, chaine=str(msg['ligne']))
            else:
                self.lignes.append(msg['ligne'])
                couleurs.AffichageColor().msg_WARNING(f"ATTENTION ! node non connecté à un service Fabrik ou ne connaissant pas un node avec le service. \n"
                                                      f"Stockage de la ligne. Nombre de ligne stockées : {len(self.lignes)}", self.log.logger)
        elif msg['command'] == 'get_blk_id_prev_fabrik':
            if self.blk_id_prev is not None:
                r = AlphaClientNode.send_cmd(self.services['fabrik'][0], self.services['fabrik'][1], self.boucle, 'get_blk_id_prev_fabrik', 'AlphaClientNode', debug=False, chaine=self.blk_id_prev)
            else:
                r = AlphaClientNode.send_cmd(self.services['cache'][0], self.services['cache'][1], self.boucle, 'get_blk_id_prev', 'AlphaClientNode', debug=False)

        elif msg['command'] == 'get_blk_id_prev':
            if 'blk_id_prev' in msg.keys() and msg['blk_id_prev'] != "":
                self.blk_id_prev = msg['blk_id_prev']
                r = AlphaClientNode.send_cmd(self.services['fabrik'][0], self.services['fabrik'][1], self.boucle, 'get_blk_id_prev_fabrik', 'AlphaClientNode', debug=False, chaine=self.blk_id_prev)

        elif msg['command'] == 'trsf_bloc': # workflow fabik -> validator -> cache
            ori, blc = await self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg)
            print("ori", ori)
            print("blc", blc)
            if ori == 'fabrik':
                await self.send_msg_ctrl('done')
                if 'validator' in self.services.keys():
                    AlphaClientNode.send_cmd(self.services['validator'][0], self.services['validator'][1], self.boucle, 'trsf_bloc', 'AlphaClientNode', debug=False, chaine=(list(self.services.keys())[0], blc))
                else:
                    self.blocs_f.append(blc)
                    couleurs.AffichageColor().msg_WARNING(f"ATTENTION ! node non connecté à un service validator ou ne connaissant pas un node avec le service. \n"
                                                          f"Stockage du bloc. Nombre de Blocs stockées : {len(self.blocs_f)}", self.log.logger)
            elif ori == 'validator':
                if 'cache' in self.services.keys():
                    AlphaClientNode.send_cmd(self.services['cache'][0], self.services['cache'][1], self.boucle, 'trsf_bloc', 'AlphaClientNode', debug=False, chaine=(list(self.services.keys())[0], blc))
                else:
                    self.blocs_v.append(blc)
                    couleurs.AffichageColor().msg_WARNING(f"ATTENTION ! node non connecté à un service cache ou ne connaissant pas un node avec le service. \n"
                                                          f"Stockage du bloc. Nombre de Blocs stockées : {len(self.blocs_v)}", self.log.logger)
            elif ori == 'cache':
                pass # le turfu !!!

        else:
            await super().trt_cmd(**msg)

    async def find_node(self):
        if self.assembly:
            pass

    async def add_service_lst(self):
        pass

    async def init_assembly(self, ip, port):
        from lib.AlphaClient import AlphaClientNode
        ip, port = self.first_contact
        c = AlphaClientNode(ip, port)
        # A FINIR

    async def find_service(self):
        from lib.parametres import Params
        p = Params()
        services = ['CACHE', 'WALLET', 'FABRIK', 'VALIDATOR']
        services_actifs = []
        port_s = "_S"
        ip_service = "IP_"
        ports_services = [f"PORT_{e}" for e in services]
        ports_services += [f"PORT_{e}{port_s}" for e in services]
        for elem in ports_services :
            if elem in p.PARAMS.keys() and p.PARAMS[elem] != '':
                port = int(p.PARAMS[elem])
                services_actifs.append(elem.split('_')[1])
                if f"{ip_service}{elem.split('_')[1]}" in p.PARAMS.keys() and p.PARAMS[f"{ip_service}{elem.split('_')[1]}"] != '':
                    host = p.PARAMS[f"{ip_service}{elem.split('_')[1]}"]
                else:
                    host = self.listener.address[0]
                await self.test_service(elem.split('_')[1], host, port)
        self.servicesOK = not tools.lst2bool(list(map(self.ordo.execute, [f"test_service_{x}" for x in services_actifs])))

    async def test_service(self, service, host, port):
        result = await self._send_get_services(host, port)
        if self._debug: couleurs.AffichageColor().msg_DEBUG(f"result _send_get_services {result}", self.log.logger)
        if result < 0:
            couleurs.AffichageColor().msg_WARNING(
                f"Le service {service} déclaré ({host}:{port}) dans le paramétrage ne répond pas \n"
                f"Reprogrammation du test...", self.log.logger)
            if not self.ordo.execute(f'test_service_{service}'):
                self.ordo.add_task(f'test_service_{service}', True, self, service, host, port, seconds=10)
        else:
            couleurs.AffichageColor().msg_INFO(f"Le service {service} est ouvert ", self.log.logger)
            if self._debug: couleurs.AffichageColor().msg_DEBUG(f"ordo.tasks {self.ordo.tasks}", self.log.logger)
            if self.ordo.execute(f'test_service_{service}'):
                self.ordo.del_task(f'test_service_{service}')

    async def _send_get_services(self, ip, port):
        from lib.AlphaClient import AlphaClientNode
        try:
            r = AlphaClientNode(ip, port, debug=1).send_cmd(ip, port, self.boucle, 'get_services', 'AlphaClientNode', debug=False, chaine=str(self.listener.address))
            if r is not None:
                if type(r) is str or type(r) is list:
                    self.services.update(r[0])
                    couleurs.AffichageColor().msg_INFO(f"le serveur {ip} a comme service {repr(r)}", self.log.logger)
                    await self.trt_services()
        except ConnectionRefusedError:
            return -1
        return 0

    async def trt_services(self):
        if 'fabrik' in self.services.keys():
            if int(self.last_config_version) > 0:
                await self.trt_config('fabrik'.upper())
            else:
                if not self.ordo.execute('trt_config_FABRIK'):
                    self.ordo.add_task('trt_config_FABRIK', True, self, 'fabrik'.upper(), seconds=5)
        elif 'validator' in self.services.keys():
            if int(self.last_config_version) > 0:
                await self.trt_config('validator'.upper())
            else:
                if not self.ordo.execute('trt_config_VALIDATOR'):
                    self.ordo.add_task('trt_config_VALIDATOR', True, self, 'validator'.upper(), seconds=5)

    async def trt_config(self, service):
        from lib.AlphaClient import AlphaClientNode
        if int(self.last_config_version) > 0:
            if self._debug: couleurs.AffichageColor().msg_DEBUG(f"self.last_config_version {self.last_config_version}", self.log.logger)
            r = AlphaClientNode.send_cmd(self.services[service.casefold()][0], self.services[service.casefold()][1], self.boucle, 'trsf_config', 'AlphaClientNode', chaine=str((self.config, self.last_config_version)))
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

    # A FAIRE Rendre plus autonome la class Assembly en s'initialisant elle même et gérant les time out des participants


    def add_node(self, ip, port, name='', services='', security='', public_key=''):
        if len(self.participants) < self.max_participants:
            self.participants.append(Assembly.Node(ip,port,name,services,security,public_key))
            # A FAIRE : Indexation du node
        else:
            # if len(self.cache.candidats) < self.cache.max_candidats: plus tard
            self.cache.candidats.append(Assembly.Node(ip,port,name,services,security,public_key))
            # A FAIRE : Indexation du node

    def get_listes(self):
        return {'participants':self.participants, 'candidats': self.cache.candidats}

