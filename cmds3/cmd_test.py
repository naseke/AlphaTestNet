import random

class cmd_test:

    __STRUCT = {'cmd_test': ['parametres']}
    __VERSION = '0.01'

    def read_cmd(self, **msg):
        print(msg['command'])
        print(msg['version_cmd'])
        print(msg['parametres'])
        return 0

    def write_cmd(self):
        msg = {
            'command': 'cmd_test',
            'version_cmd': self.__VERSION,
            'parametres': ["var_" + str(u) for u in range(random.choice(range(10)))]
        }
        return msg

    def get_STRUCT(self):
        return self.__STRUCT

    def get_VERSION(self):
        return self.__VERSION