from lib.tools import get_ip, get_name

class get_net_conf:

    __STRUCT = {'get_net_conf': ['ip', 'name', 'port', 'services', 'security', 'public_key']}
    __VERSION = '0.01'

    def read_cmd(self, obj, **msg):
        for i in ['ip', 'name', 'port', 'services', 'security', 'public_key']:
            print(i, msg[i])
        return 0

    def write_cmd(self):
        msg = {
            'command': 'get_net_conf',
            'version_cmd': self.__VERSION,
        }
        return msg

    def write_cmd_rep(self, obj):
        dico = {
            'ip': get_ip(),
            'name': get_name(),
            'port': obj.listener.address[1],
            'services': obj.services,
            'security': '',
            'public_key': '',
        }
        return dico

    def get_STRUCT(self):
        return self.__STRUCT

    @classmethod
    def get_VERSION(self):
        return self.__VERSION
