import uuid
import hashlib
import datetime


class trsf_ligne:

    __STRUCT = {'trsf_ligne': ['ligne']}
    __VERSION = '0.01'

    def read_cmd(self, **dico):
        return dico['ligne']

    def write_cmd(self, chaine):
        eval(chaine)
        msg = {
            'command': 'trsf_ligne',
            'version_cmd': self.__VERSION,


        }
        if chaine is not None:
            msg.update({'ligne': chaine})
        else:
            msg.update({'ligne': {}})
        return msg

    def get_STRUCT(self):
        return self.__STRUCT

    @classmethod
    def get_VERSION(self):
        return self.__VERSION
