
class you_have_cmd:

    __STRUCT = {'you_have_cmd': ['cmd','reponse']}
    __VERSION = '0.01'

    def read_cmd(self, **dico):
        if dico['reponse'] == 'no':
            if dico['cmd'] == "get_struct_cmd":
                send_cmd()
#METTRE IP DANS LES MSG !!!

    def write_cmd(self, cmd, rep):
        msg = {}
        msg['command'] = 'you_have_cmd'
        msg['cmd'] = cmd
        msg['reponse'] = rep

    def get_STRUCT(self):
        return self.__STRUCT

    @classmethod
    def get_VERSION(self):
        return self.__VERSION
