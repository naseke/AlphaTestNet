from multiprocessing.connection import Client
import hashlib
import random
from lib import couleurs, tools
from etc.contants import PATH_CMDS

class AlphaClient:

    __VERSION = '0.01'

    def __init__(self, host, port, pwd=None, debug=False):
        self.conn = Client((host, port), pwd)
        self._debug = debug
        self.moduleManager = tools.ManagerClass(PATH_CMDS)
        self.pre_cmds = tools.ManagerClassPreCMDS()
        self.lastReply = ''
        self.lastCmdSend = ''
        # if self._debug: couleurs.AffichageColor().msg_DEBUG(self.moduleManager.get_structCmds())

    # findef

    @classmethod
    def get_VERSION(self):
        return self.__VERSION

    def send_msg(self, i, **dico):
        dico['nom'] = tools.get_name()
        dico['numero'] = i
        dico['signature'] = hashlib.sha512("ns".encode()).hexdigest()
        #couleurs.AffichageColor().msg_DEBUG(f"dico {type(self)} {dico}")
        self.conn.send(dico)
        self.lastCmdSend = dico['command']
    # findef

    def send_first_msg(self, cmd):
        if cmd in self.moduleManager.get_structCmds().keys():
            dico = {
                'numero': -1,
                'nom': tools.get_name(),
                'signature': hashlib.sha512("ns".encode()).hexdigest(),
            }
            dico.update(self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class('get_struct_cmd')).write_cmd(self, cmd))
            if self._debug: couleurs.AffichageColor().msg_DEBUG(repr(dico))
            self.conn.send(dico)
        else:
            print("commande inconue")
            exit()

    def create_msg(self, i=0, cmd_s='', cmd_c='', **msg):
        dico = {
            'numero': i,
            'nom': tools.get_name(),
            'signature': hashlib.sha512("ns".encode()).hexdigest(),
        }
        dico.update(self.pre_cmds.get_func_throught_module('pre_write_cmd')(self, cmd_s, cmd_c, **msg))
        if self._debug: couleurs.AffichageColor().msg_DEBUG(f"create_msg {type(self)} {repr(dico)}")
        return dico

    def recv_msg(self):
         msg = self.conn.recv()
         self.lastReply = msg['command']
         return msg 
    # findef

    def trt_cmd_other(self, obj, msg, msg2):
        pass

    @classmethod
    def send_cmd(cls, host, port, i, cmd, obj_name='AlphaClient', debug=False, chaine=None):
        from importlib import import_module
        r = None
        class_ = getattr(import_module('lib.AlphaClient'), obj_name)
        c = class_(host, port, debug)
        msg = [c.create_msg(i, cmd, chaine)]
        c.send_msg(i, **msg[0])
        if debug: couleurs.AffichageColor().msg_DEBUG(f'emission {msg[0]}')
        msg2 = c.recv_msg()
        #msg2 = {'command' : 'done'}
        while msg:
            if debug: couleurs.AffichageColor().msg_DEBUG(f"msg {type(c)} {repr(msg)}")
            if debug: couleurs.AffichageColor().msg_DEBUG(f"msg2 {type(c)} {repr(msg2)}")
            if msg2['command'] == 'misunderstood':
                c.conn.close()
                # envoie du get_struc_cmd
                if msg[len(msg)-1]['command'] == 'get_struct_cmd':
                    c = class_(host, port, debug)
                    c.send_first_msg('get_struct_cmd')
                    msg2 = c.recv_msg()
                elif msg[len(msg)-1]['command'] == 'trf_pre_cmds':
                    c = class_(host, port, debug)
                    c.send_first_msg('trf_pre_cmds')
                    msg2 = c.recv_msg()
                else:
                    c = class_(host, port, debug)
                    c.send_first_msg(msg[len(msg) - 1]['command'])
                    msg.append({'command': 'trf_pre_cmds'})
                    msg.append({'command': 'get_struct_cmd'})
                    msg2 = c.recv_msg()
            elif msg2['command'] == 'done':
                c.conn.close()
                msg.pop()
                r = True
                msg2 = {'command': 'None'}
            elif msg2['command'] == 'lower_version':
                c.conn.close()
                c.pre_cmds.get_func_throught_module('pre_read_cmd')(c, **msg2)
                msg2 = {'command': 'None'}
            elif msg[len(msg) - 1]['command'] == 'trf_pre_cmds':
                msg.pop()
                c.conn.close()
                c = class_(host, port, debug)
                msg.append(c.pre_cmds.get_func_throught_module('pre_write_cmd')(c, 'trf_pre_cmds'))
                c.send_msg(i, **msg[len(msg) - 1])
                msg2 = c.recv_msg()
            elif len(msg) == 1:
                if msg[len(msg) - 1]['command'] == msg2['command']:
                   r = c.trt_cmd_other(c, msg, msg2)
                else:
                    c = class_(host, port, debug)
                    c.send_msg(i + 0.5, **msg[len(msg) - 1])
                    msg2 = c.recv_msg()
        return r



    def init_cmd_srv (host, port, debug=0 ):
        cmd_init = [
            'get_struct_cmd',
            'done',
            'wrong',
            'misunderstood',
            'get_entete_msg',
            'lower_version',
        ]
        for cmd in cmd_init:
            c = AlphaClient(host, port, debug)
            c.send_first_msg(cmd)
            c.conn.close()
# finclass


class AlphaClientNode(AlphaClient):

    def __init__(self, host, port, server=None, pwd=None, debug=0):
        super().__init__(host, port, pwd, debug)
        self.server = server

    def trt_cmd_other(self, obj, msg, msg2):
        if msg2['command'] == 'get_net_conf':
            msg.pop()
            obj.pre_cmds.get_func_throught_module('pre_read_cmd')(obj, **msg2)
        elif msg2['command'] == 'get_services':
            msg.pop()
            return obj.pre_cmds.get_func_throught_module('pre_read_cmd')(obj, **msg2)


class AlphaClientCache(AlphaClient):

    def trt_cmd_other(self, obj, msg, msg2):
        if msg2['command'] == 'get_net_conf':
            msg.pop()
            obj.pre_cmds.get_func_throught_module('pre_read_cmd')(obj, **msg2)
        elif msg2['command'] == 'get_services':
            msg.pop()
            return obj.pre_cmds.get_func_throught_module('pre_read_cmd')(obj, **msg2)

    #@classmethod
    #async def send_cmd(cls, host, port, i, cmd, obj_name='AlphaClient', debug=0, chaine=None):
    #    super().send_cmd(host, port, i, cmd, obj_name, debug, chaine)


class AlphaClientFabrik(AlphaClient):

    def trt_cmd_other(self, obj, msg, msg2):
        if msg2['command'] == 'get_net_conf':
            msg.pop()
            obj.pre_cmds.get_func_throught_module('pre_read_cmd')(obj, **msg2)
        elif msg2['command'] == 'get_services':
            msg.pop()
            return obj.pre_cmds.get_func_throught_module('pre_read_cmd')(obj, **msg2)


class AlphaClientValidator(AlphaClient):

    def trt_cmd_other(self, obj, msg, msg2):
        if msg2['command'] == 'get_net_conf':
            msg.pop()
            obj.pre_cmds.get_func_throught_module('pre_read_cmd')(obj, **msg2)
        elif msg2['command'] == 'get_services':
            msg.pop()
            return obj.pre_cmds.get_func_throught_module('pre_read_cmd')(obj, **msg2)


class AlphaClientProdukt(AlphaClient):
    pass


class AlphaClientRequeteur(AlphaClient):
    pass


class AlphaClientWallet(AlphaClient):
    pass



"""Tests Unitaires"""


def just_one_cmd(host, port, cmd, debug=False):
    # c = AlphaClient(host, port, debug)
    # c.send_first_msg(cmd)
    r = AlphaClientNode.send_cmd(host, port, 0, cmd, 'AlphaClientNode', debug, chaine=('fabrik', "{'blk_id': '71133dc6-8dc7-5c84-ba44-9c0edf9bed82', 'blk_timestamp': 1632044531659438, 'blk_id_prev': 'f2c317c1-d9ab-5b16-b896-206da413149c', 'blk_id_snap_prev': '', 'blk_version': '0.1.0', 'blk_hash': '93d764b739eea574feeff53de5ac349a55ea086f11f4c73e605a88a7f38a1284c2af3c4ac5c4f245f24b19d5b2bfb61b157d861634b9dfe998a6d513ebcdfb42', 'blk_signature': '', 'blk_config': {'PORT_FABRIK': '8020'}, 'blk_content': []}"))
    print(r)
    if r is not None:
        if type(r) is str or type(r) is list:
            print(r)
    # c.conn.close()
    exit()


def just_one_maj(host, port, cmd, debug=0):
    c = AlphaClient(host, port, debug)
    c.send_first_msg(cmd)
    # tools.send_cmd(host, port, 0, cmd)
    c.conn.close()
    exit()


def main():
    port = 8000
    host = '192.168.1.9'
    #host = '192.168.1.3'

    just_one_cmd(host, port, 'trsf_bloc')
    #just_one_maj(host, port, 'get_net_conf')
    #tools.init_cmd_srv(host, port)

    for i in range(2):
        print("boucle n°{}".format(i))
        # tools.send_cmd(host, port, i,'cmd_test')
    #for j in range(2):
    #    t = i+j+1
    #    print("boucle n°{}".format(t))
    #    tools.send_cmd(host, port, t, 'trsf_file')
    #    tools.send_cmd(host, port, t, 'cmd_test')

# findef


if __name__ == "__main__": main()