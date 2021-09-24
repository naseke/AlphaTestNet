class done:

    __STRUCT = {'done': []}
    __VERSION = '0.01'

    def read_cmd(self):
        pass

    def write_cmd(self):
        msg = {
            'command': 'done',
            'version_cmd': self.__VERSION,
        }
        return msg

    def get_STRUCT(self):
        return self.__STRUCT

    @classmethod
    def get_VERSION(self):
        return self.__VERSION
