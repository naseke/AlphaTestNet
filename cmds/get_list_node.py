from lib.tools import get_ip, get_name

class get_list_node:

    __STRUCT = {'get_list_node': 'liste'}
    __VERSION = '0.01'

    def read_cmd(self, obj, **msg):
        for par in msg['liste']['participants']:
            obj.assembly.add_node(par.ip, par.port, par.name, par.services, par.security, par.public_key)

        for par in msg['liste']['candidats']:
            obj.assembly.add_node(par.ip, par.port, par.name, par.services, par.security, par.public_key)

        return 0

    def write_cmd(self):
        msg = {
            'command': 'get_list_node',
            'version_cmd': self.__VERSION,
        }
        return msg

    def write_cmd_rep(self, obj):
        dico = {
            'liste': obj.assembly.get_listes()
        }
        return dico

    def get_STRUCT(self):
        return self.__STRUCT

    @classmethod
    def get_VERSION(self):
        return self.__VERSION
