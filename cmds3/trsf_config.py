class trsf_config:

    __STRUCT = {'trsf_config': ['config', 'last_config_version']}
    __VERSION = '0.01'

    def read_cmd(self, **dico):
        return dico['last_config_version'], dico['config']

    def write_cmd(self, chaine):
        msg = {
            'command': 'trsf_config',
            'version_cmd': self.__VERSION,
        }
        if chaine is not None:
            conf, conf_vers = eval(chaine)
            msg.update({
                'config': conf,
                'last_config_version': conf_vers,
            })
        else:
            msg.update({
                'config': '',
                'last_config_version': '',
            })
        return msg

    def get_STRUCT(self):
        return self.__STRUCT

    @classmethod
    def get_VERSION(self):
        return self.__VERSION
