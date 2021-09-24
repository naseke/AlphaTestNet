class get_services:

    __STRUCT = {'get_services': ['node', 'liste']}
    __VERSION = '0.01'

    def read_cmd(self, **msg):
        return msg['liste']

    def write_cmd(self, chaine):
        msg = {
            'command': 'get_services',
            'version_cmd': self.__VERSION,
         }
        if chaine is not None:
            msg.update({'node': eval(chaine)})
        else:
            msg.update({'node': ()})
        return msg

    def write_cmd_rep(self, obj):
        dico = {
                'liste': obj.services
            }
        return dico


    def get_STRUCT(self):
        return self.__STRUCT

    @classmethod
    def get_VERSION(self):
        return self.__VERSION
