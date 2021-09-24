class get_entete_msg:

    __STRUCT = {'get_entete_msg': ['numero', 'nom', 'signature']}
    __VERSION = '0.01'

    def read_cmd(self, **dico):
        pass
        # A FAIRe le controle de l'entete

    def write_cmd(self):
        msg = {
            'command': 'get_entete_msg',
            'version_cmd': self.__VERSION,
        }
        return msg

    def get_STRUCT(self):
        return self.__STRUCT

    @classmethod
    def get_VERSION(self):
        return self.__VERSION