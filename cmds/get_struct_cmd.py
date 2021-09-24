from os import path
import base64
from lib import couleurs
# from etc.contants import PATH_CMDS2

class get_struct_cmd:

    __STRUCT = {'get_struct_cmd': ['cmd_name', 'file_name', 'file_content']}
    __VERSION = '0.02'

    def read_cmd(self, obj, **dico):
        with open(path.join(obj.moduleManager.path, dico['file_name']), 'wb') as fic:
            fic.write(base64.b64decode(dico['file_content']))
        if obj.moduleManager.isexist(dico['cmd_name']):
            couleurs.AffichageColor().msg_WARNING(f"Reload the command '{dico['cmd_name']}' in version : {obj.moduleManager.reload_one_by_name_cmd(dico['cmd_name'])}")
        else:
            obj.moduleManager.add_cmd(dico['cmd_name'])
            couleurs.AffichageColor().msg_WARNING(f"I just learned the command '{dico['cmd_name']}' it's COOL ! :)")
        return 0

    def write_cmd(self, obj, cmd):
        chem = obj.moduleManager.get_cmd_path_file(cmd)
        if path.exists(chem):
            dico = {
                'command': 'get_struct_cmd',
                'version_cmd': self.__VERSION,
                'cmd_name': cmd,
                'file_name': path.basename(chem),
            }
            with open(chem, 'rb') as fic:
                dico['file_content'] = base64.b64encode(fic.read())
            return dico
        else:
            raise Exception

    def get_STRUCT(self):
        return self.__STRUCT

    @classmethod
    def get_VERSION(self):
        return self.__VERSION
