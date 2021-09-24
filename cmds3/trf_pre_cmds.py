from os import path
import base64
from lib import couleurs
from lib.tools import find_root, ManagerClassPreCMDS



class trf_pre_cmds:

    __STRUCT = {'trf_pre_cmds': ['file_name', 'file_content']}
    __VERSION = '0.01'

    def read_cmd(self, obj, **dico):
        with open(path.join(find_root(), 'lib', dico['file_name']), 'wb') as fic:
            fic.write(base64.b64decode(dico['file_content']))
        if obj.pre_cmds.isempty:
            obj.pre_cmds = ManagerClassPreCMDS()
        else:
            couleurs.AffichageColor().msg_WARNING(f"Reload the interface '{dico['file_name'].split('.')[0]}' in version : {obj.pre_cmds.reload()}")
        return 0

    def write_cmd(self):
        chem = path.join(find_root(), 'lib', 'pre_cmds.py')
        if path.exists(chem):
            dico = {
                'command': 'trf_pre_cmds',
                'version_cmd': self.__VERSION,
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
