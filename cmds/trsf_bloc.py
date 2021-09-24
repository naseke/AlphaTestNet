class trsf_bloc:

    __STRUCT = {'trsf_bloc': ['ligne']}
    __VERSION = '0.01'

    def read_cmd(self, **dico):
        return dico['from'], dico['bloc']

    def write_cmd(self, chaine):
        ori, blc = chaine
        msg = {
            'command': 'trsf_bloc',
            'version_cmd': self.__VERSION,
        }
        if chaine is not None:
            msg.update({'bloc': blc})
            msg.update({'from': ori})
        else:
            msg.update({'bloc': {}})
            msg.update({'from': ori})
        print(msg)
        return msg

    def get_STRUCT(self):
        return self.__STRUCT

    @classmethod
    def get_VERSION(self):
        return self.__VERSION
