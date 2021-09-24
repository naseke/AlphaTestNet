import base64
import os.path

class trsf_fic:

    """test de doc"""

    __STRUCT = {'trsf_fic': ['file_name', 'file_path', 'file_content']}
    __VERSION = '0.01'

    def read_cmd(self, **dico):
        if os.path.exists(dico['file_path']):
            with open(os.path.join(dico['file_path'], dico['file_name']), 'wb') as fic:
                fic.write(base64.b64decode(dico['file_content']))
        return 0

    def write_cmd(self, chem):
        chem = f'..\\{chem}'
        if os.path.exists(chem):
            dico = {
                'command': 'trsf_file',
                'version_cmd': self.__VERSION,
                'file_path': os.path.dirname(chem),
                'file_name': os.path.basename(chem),
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


# test unitaire
def __main():
    msg = trsf_fic_sys().write_cmd('trsf_file.py')
    msg['file_path'] = "../Gaia"
    trsf_fic_sys().read_cmd( **msg)

if __name__ == "__main__": __main()