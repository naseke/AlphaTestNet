from multiprocessing.connection import Client
import hashlib
import random
from lib import couleurs, tools
from etc.contants import PATH_CMDS

class AlphaClient:

    #list_cmd = {
    #    'get_struct_cmd': ['cmd_name', 'keys_param'],
    #    'get_entete_msg': ['numero', 'nom', 'signature'],
    #    'misunderstood': [],
    #    'done': [],
    #    'cmd_test': ['parametres'],
    #    'trsf_file': ['file_name', 'file_path', 'file_content'],
    #}

    def __init__(self, host, port, pwd=None, debug=0):
        self.conn = Client((host, port), pwd)
        self._debug = debug
        self.moduleManager = tools.ManagerClass(PATH_CMDS)
        self.pre_cmds = tools.ManagerClassPreCMDS()
        self.lastReply = ''
        self.lastCmdSend = ''
        if self._debug > 1: couleurs.AffichageColor().msg_DEBUG(self.moduleManager.get_structCmds())

    # findef

    def send_msg(self, i, **dico):
        dico['nom'] = tools.get_name()
        dico['numero'] = i
        dico['signature'] = hashlib.sha512("ns".encode()).hexdigest()
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
            if self._debug > 0: couleurs.AffichageColor().msg_DEBUG(repr(dico))
            self.conn.send(dico)
        else:
            print("commande inconue")
            exit()


    # findef

    def create_msg(self, cmd_s='', cmd_c='' , **msg):
        # A FAIRE : faire l'entete des msg (plus tard)
        msg = self.pre_cmds.get_func_throught_module('pre_write_cmd')(self, cmd_s, cmd_c, **msg)
        if self._debug > 1: couleurs.AffichageColor().msg_DEBUG(repr(msg))
        return msg

    def recv_msg(self):
         msg = self.conn.recv()
         self.lastReply = msg['command']
         return msg 
    # findef

    def trt_cmd_other(self, obj, msg, msg2):
        if msg2['command'] == 'get_net_conf':
            obj.pre_cmds.get_func_throught_module('pre_read_cmd')(obj, **msg2)
            msg.pop()
        elif msg2['command'] == 'get_services':
            obj.pre_cmds.get_func_throught_module('pre_read_cmd')(obj, **msg2)
            msg.pop()

    def send_cmd(self, host, port, i, cmd, obj_name='AlphaClient', debug=0):
        from importlib import import_module
        class_ = getattr(import_module('lib.AlphaClient'), obj_name)
        c = class_(host, port, debug)
        msg = [c.create_msg(cmd)]
        c.send_msg(i, **msg[0])
        msg2 = c.recv_msg()
        while msg:
            if msg2['command'] == 'misunderstood':
                c.conn.close()
                # envoie du get_struc_cmd
                if msg[len(msg) - 1]['command'] == 'get_struct_cmd':
                    c = class_(host, port, debug)
                    c.send_first_msg('get_struct_cmd')
                    msg2 = c.recv_msg()
                elif msg[len(msg) - 1]['command'] == 'trf_pre_cmds':
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
                if msg[len(msg) - 1]['command'] == 'get_net_conf':
                    c.trt_cmd_other(c, msg, msg2)
                else:
                    c = class_(host, port, debug)
                    c.send_msg(i + 0.5, **msg[len(msg) - 1])
                    msg2 = c.recv_msg()

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

def just_one_cmd(host, port, cmd, debug=0):
    #c = AlphaClient(host, port, debug)
    #c.send_first_msg(cmd)
    AlphaClient.send_cmd(host, port, 0, cmd, debug)
    #c.conn.close()
    exit()

def just_one_maj(host, port, cmd, debug=0):
    c = AlphaClient(host, port, debug)
    c.send_first_msg(cmd)
    #tools.send_cmd(host, port, 0, cmd)
    c.conn.close()
    exit()

def main():
    port = 8010
    host = '192.168.1.9'
    #host = '192.168.1.3'

    just_one_cmd(host, port, 'get_services', 2)
    #just_one_maj(host, port, 'lower_version')
    #tools.init_cmd_srv(host, port)

    for i in range(2):
        print("boucle n°{}".format(i))
        tools.send_cmd(host, port, i,'cmd_test')
    #for j in range(2):
    #    t = i+j+1
    #    print("boucle n°{}".format(t))
    #    tools.send_cmd(host, port, t, 'trsf_file')
    #    tools.send_cmd(host, port, t, 'cmd_test')

# findef


if __name__ == "__main__": main()