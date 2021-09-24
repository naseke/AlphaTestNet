class structure:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION

block = {
    'doc': 'Block Structure.',
    'name': 'block',
    'namespace': 'Alphatestnet',
    'type': 'record',
    'fields': [
        # {'name': 'blk_id', 'type': {'type': 'string', 'logicalType': 'uuid', }},
        {'name': 'blk_id', 'type': 'string'},
        {'name': 'blk_version', 'type': 'string'},
        # {'name': 'blk_timestamp', 'type': {'type': 'long', 'logicalType': 'timestamp-micros', }},
        {'name': 'blk_timestamp', 'type': 'long', },
        # {'name': 'blk_id_prev', 'type': {'type': 'string', 'logicalType': 'uuid', }},
        {'name': 'blk_id_prev', 'type': 'string'},
        # {'name': 'blk_id_snap_prev', 'type': {'type': 'string', 'logicalType': 'uuid', }},
        {'name': 'blk_id_snap_prev', 'type': 'string'},
        {'name': 'blk_hash', 'type': 'string', 'default': ''},
        {'name': 'blk_signature', 'type': 'string', 'default': ''},
        {'name': 'blk_signature_timestamp', 'type': 'long', },
        {'name': 'blk_config', 'type': {'type': 'map', 'values': 'string', 'default': {}, }},
        {'name': 'blk_content', 'type': {'type': 'array', 'items': 'string', 'default': [], }},
    ],
}

line = {
    'doc': 'line Structure.',
    'name': 'line',
    'namespace': 'Alphatestnet',
    'type': 'record',
    'fields': [
        # {'name': 'lne_id', 'type': {'type': 'string', 'logicalType': 'uuid', }},
        {'name': 'lne_id', 'type': 'string'},
        {'name': 'lne_version', 'type': 'float'},
        # {'name': 'lne_timestamp', 'type': {'type': 'long', 'logicalType': 'timestamp-micros', }},
        {'name': 'lne_timestamp', 'type': 'long', },
        {'name': 'lne_hash', 'type': 'string'},
        # {'name': 'lne_signature', 'type': 'string'},
        {'name': 'lne_config', 'type': {'type': 'map', 'values': 'string', 'default': {}}},
        {'name': 'lne_content', 'type': {'type': 'map', 'values': 'string', 'default': {}}},
    ],
}
