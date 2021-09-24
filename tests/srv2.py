from multiprocessing.connection import Listener
import hashlib
from lib import couleurs, tools
from etc.contants import PATH_CMDS2
from lib.pre_cmds import pre_read_cmd




class AlphaServer():

    #list_cmd = {
    #    'get_struct_cmd': ['cmd_name', 'keys_param'],
    #    'get_entete_msg': ['numero', 'nom', 'signature'],
    #    'misunderstood': [],
    #    'done': []
    #}

    def __init__(self, host, port, pwd=None, debug=False):
        self.msg_welcome()
        self.listener = Listener((host, port), pwd)
        self.conn = None
        self._debug = debug
        self.moduleManager = tools.ManagerClass(PATH_CMDS2)
        self.pre_cmds = tools.ManagerClassPreCMDS()
        if self.moduleManager.isempty: couleurs.AffichageColor().msg_WARNING("I have no command vocabulary. I'm a baby !")
        if self._debug: couleurs.AffichageColor().msg_DEBUG(repr(self.moduleManager.get_structCmds()))

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

    def send_msg(self, **dico):
            try:
                self.conn.send(dico)
            except:
                couleurs.AffichageColor().msg_FAIL(f'send error on {self.listener.last_accepted}')
                pass
    # findef


    def recv_msg(self):
        try:
            msg = self.conn.recv()
            return self.trt_msg(msg)
        except EOFError:
            couleurs.AffichageColor().msg_FAIL(f'message error with {self.listener.last_accepted}')
            pass
        except ConnectionResetError:
            couleurs.AffichageColor().msg_FAIL(f'Connection client error from {self.listener.last_accepted}')
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
        if self._debug: couleurs.AffichageColor().msg_DEBUG(repr(msg))

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
                    couleurs.AffichageColor().msg_WARNING(
                        f"I just learned the command '{msg['cmd_name']}' it's COOL ! :)")
                else:
                    couleurs.AffichageColor().msg_FAIL(
                        f"Je pratique couramment six millions de formes de communication... pour le moment il me faudrait connaitre la commande '{msg['command']}'")
                    self.send_msg_ctrl_legacy('done')
            else:  # utilisation de la dernière version get_struct_cmd si le serveur l'a
                if msg['version_cmd'] == self.moduleManager.get_obj_throught_module(
                        self.moduleManager.get_module_by_class(msg['command'])).get_VERSION():
                    self.moduleManager.get_obj_throught_module(
                        self.moduleManager.get_module_by_class(msg['command'])).read_cmd(self, **msg)
                    self.send_msg_ctrl('done')
                else:
                    if msg['version_cmd'] > self.moduleManager.get_obj_throught_module(
                            self.moduleManager.get_module_by_class(msg['command'])).get_VERSION():
                        if msg['cmd_name'] == msg['command']:
                            self.moduleManager.get_obj_throught_module(
                                self.moduleManager.get_module_by_class(msg['command'])).read_cmd(self, **msg)
                            self.send_msg_ctrl('done')
                        else:
                            couleurs.AffichageColor().msg_WARNING(
                                f"wrong version of '{msg['command']}' from {msg['version_cmd']} to {self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION()}")
                            self.send_msg_ctrl('misunderstood')
                        # self.moduleManager.reload_one_by_name_cmd(msg['command'])
                        # self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).read_cmd(self, **msg)
                    else:
                        couleurs.AffichageColor().msg_WARNING(
                            f"the client version of command {msg['command']}is lower then me.")

            return 0


        # Execution d'une commande en vérifiant sa version
        elif msg['command'] in self.moduleManager.get_structCmds().keys():
            if msg['version_cmd'] == self.moduleManager.get_obj_throught_module(
                    self.moduleManager.get_module_by_class(msg['command'])).get_VERSION():
                if 'get_entete_msg' in self.moduleManager.get_structCmds().keys():
                    self.moduleManager.get_obj_throught_module(
                        self.moduleManager.get_module_by_class('get_entete_msg')).read_cmd(**msg)
                self.pre_cmds.get_func_throught_module('pre_read_cmd')(self, **msg)
                self.send_msg_ctrl('done')
                print('~' * 79)
            else:
                if msg['version_cmd'] > self.moduleManager.get_obj_throught_module(
                        self.moduleManager.get_module_by_class(msg['command'])).get_VERSION():
                    couleurs.AffichageColor().msg_WARNING(f"wrong version of '{msg['command']}' from {msg['version_cmd']} to {self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION()}")
                    self.send_msg_ctrl('misunderstood')
                else:
                    couleurs.AffichageColor().msg_WARNING(f"the client version of command '{msg['command']}' is lower then me from {msg['version_cmd']} to {self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(msg['command'])).get_VERSION()}.")



        else:
            couleurs.AffichageColor().msg_WARNING(f"I did not understand the command '{msg['command']}'")
            self.send_msg_ctrl('misunderstood')
        # self._debug: couleurs.AffichageColor().msg_DEBUG(repr(self.moduleManager.get_structCmds()))
        return 0

    # findef

    def send_msg_ctrl(self, cmd):
        msg = {}
        msg['numero'] = -1
        msg['command'] = cmd
        msg['nom'] = tools.get_name()
        msg['signature'] = hashlib.sha512("ns".encode()).hexdigest()
        try:
            self.send_msg(**msg)
        except:
            couleurs.AffichageColor().msg_FAIL(f'send error on {self.listener.last_accepted}')
            pass

    # findef

    def send_msg_common(self, cmd):
        msg = {
            'numero': '-1',
            'nom': tools.get_name(),
            'signature': hashlib.sha512("ns".encode()).hexdigest(),
        }
        msg.update(self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class(cmd)).write_cmd())
        try:
            self.send_msg(**msg)
        except:
            couleurs.AffichageColor().msg_FAIL(f'send error on {self.listener.last_accepted}')
            pass

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
            couleurs.AffichageColor().msg_FAIL(f'send error on {self.listener.last_accepted}')
            pass

    # findef

    def send_update_msg(self, cmd):
        if cmd in self.moduleManager.get_structCmds().keys():
            dico = {
                'numero': -1,
                'nom': tools.get_name(),
                'signature': hashlib.sha512("ns".encode()).hexdigest(),
            }
            dico.update(self.moduleManager.get_obj_throught_module(self.moduleManager.get_module_by_class('lower_version')).write_cmd(self, cmd))
            if self._debug > 0: couleurs.AffichageColor().msg_DEBUG(repr(dico))
            self.conn.send(dico)
        else:
            print("commande inconue")
            exit()



def main():
    port = 8000
    host = tools.get_ip()

    l = AlphaServer(host, port, debug=False)
    i = 0
    while True:
        print("boucle n°{}".format(i))
        i += 1
        l.init_tx()
        l.recv_msg()


if __name__ == "__main__": main()