from os import path
import base64
from lib import couleurs

class lower_version:

    __STRUCT = {'lower_version': ['cmd_name', 'file_name', 'file_content']}
    __VERSION = '0.01'

    def read_cmd(self):
        def read_cmd(self, obj, **dico):
            with open(path.join(obj.moduleManager.path, dico['file_name']), 'wb') as fic:
                fic.write(base64.b64decode(dico['file_content']))
            couleurs.AffichageColor().msg_WARNING(f"Reload the command '{dico['cmd_name']}' in version : {obj.moduleManager.reload_one_by_name_cmd(dico['cmd_name'])}")

    def write_cmd(self, obj, cmd):
        chem = obj.moduleManager.get_cmd_path_file(cmd)
        if path.exists(chem):
            dico = {
                'command': 'lower_version',
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

    def get_VERSION(self):
        return self.__VERSION
