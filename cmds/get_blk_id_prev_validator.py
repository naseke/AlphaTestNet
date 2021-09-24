class get_blk_id_prev_validator:

    __STRUCT = {'get_blk_id_prev_validator': ['blk_id_prev']}
    __VERSION = '0.01'

    def read_cmd(self, **msg):
        return msg['blk_id_prev']

    def write_cmd(self, chaine):
        msg = {
            'command': 'get_blk_id_prev_validator',
            'version_cmd': self.__VERSION,
        }
        if chaine is not None:
            msg.update({'blk_id_prev': chaine})
        else:
            msg.update({'blk_id_prev': ()})
        return msg

    def get_STRUCT(self):
        return self.__STRUCT

    @classmethod
    def get_VERSION(self):
        return self.__VERSION
