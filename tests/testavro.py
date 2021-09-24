import fastavro
import fastavro.utils
import fastavro.schema
import fastavro.validation
import uuid
import datetime
import hashlib

#from fastavro import writer
#from fastavro.utils import generate_many
#from fastavro import reader


#schema = {
#    'doc': 'A weather reading.',
#    'name': 'Weather',
#    'namespace': 'Alphanet',
#    'type': 'record',
#    'fields': [
#        {'name': 'station', 'type': 'string'},
#        {'name': 'time', 'type': 'long'},
#        {'name': 'temp', 'type': 'int'},
#    ],
#}

#schema = {
#    'doc': 'A weather reading.',
#    'name': 'Weather2',
#    'namespace': 'Alphanet',
#    'type': 'record',
#    'fields': [
#        {
#            'name': 'system-fields',
#            'doc': 'system fields',
#            'type': 'record',
#            'fields': [
#                {'name': 'champ_sys', 'type': 'string'},
#                {'name': 'blk_num', 'type': 'long'},
#            ],
#         },
#        {
#            'name': 'custom-fields',
#            'doc': 'custom fields',
#            'type': 'record',
#            'fields': [
#                {'name': 'champ_cust_s', 'type': 'string'},
#                {'name': 'champ_cust_i', 'type': 'integer'},
#            ],
#         },
#        {
#            'name': 'custom-snap-def',
#            'doc': 'custom snap def',
#            'type': 'record',
#            'fields': [
#                {'name': 'champ_snap_id', 'type': {'name': 'blk_num', 'type': 'long'},},
#                {'name': 'champ_snap', 'type': 'string'},
#            ],
#        },
#        {
#            'name': 'custom-snap-result',
#            'doc': 'custom fields',
#            'type': 'record',
#            'fields': [
#                {'name': 'snap_id_def', 'type': 'string'},
#                {'name': 'snap_id', 'type': {'type': 'string', 'logicalType': 'uuid', }},
#                {'name': 'snap_data', 'type': 'string'},
#            ],
#        },
#
#    ],
#}

schema = {
    'doc': 'A weather reading.',
    'name': 'block',
    'namespace': 'Alphanet',
    'type': 'record',
    'fields': [
        {
            'name': 'System',
            'doc': 'system fields',
            'type':
                {
                    'name': 'system-fields',
                    'type': 'record',
                    'fields': [
                        {'name': 'blk_champ_sys', 'type': 'string'},
                        {'name': 'blk_num', 'type': 'long'},
                        {'name': 'blk_id', 'type': {'type': 'string', 'logicalType': 'uuid', }},
                        {'name': 'blk_timestamp', 'type': {'type': 'long', 'logicalType': 'timestamp-micros'},},
                    ],
                }
        },
    ],
}

schema = {
    'doc': 'A weather reading.',
    'name': 'block',
    'namespace': 'Alphanet',
    'type': 'record',
    'fields': [
        {
            'name': 'System',
            'doc': 'system fields',
            'type':
                {
                    'name': 'system-fields',
                    'type': 'record',
                    'fields': [
                        {'name': 'blk_champ_sys', 'type': 'string'},
                        {'name': 'blk_num', 'type': 'long'},
                        {'name': 'blk_id', 'type': {'type': 'string', 'logicalType': 'uuid', }},
                        {'name': 'blk_timestamp', 'type': {'type': 'long', 'logicalType': 'timestamp-micros', }},
                    ],
                }
        },
        {
            'name': 'Ligne',
            'doc': 'lignes d un block',
            'fields': [
                {'name': 'blk_ligne_num', 'type': 'long'},
                {'name': 'blk_ligne_id', 'type':  {'type': 'string', 'logicalType': 'uuid', }},
                {'name': 'blk_ligne_data', 'type': 'string'},
            ],
        },
    ],
}


records = [
    {
        'System': {'blk_champ_sys': 'mTSlCieFwJ', 'blk_num': 0, 'blk_id': uuid.uuid5(uuid.uuid4(),"Alphanet"), 'blk_timestamp': int(datetime.datetime.now().timestamp()*1000000)},
        'Ligne': {'blk_ligne_num': 0, 'blk_ligne_id': uuid.uuid5(uuid.uuid4(),str(uuid.uuid5(uuid.uuid4(),"Alphanet"))), 'blk_ligne_data': hashlib.sha256().hexdigest()}
    },
    {
        'System': {'blk_champ_sys': 'fjgyPFDqOJ', 'blk_num': 1, 'blk_id': uuid.uuid5(uuid.uuid4(),"Alphanet"), 'blk_timestamp': int(datetime.datetime.now().timestamp()*1000000)},
        'Ligne': {'blk_ligne_num': 0, 'blk_ligne_id': uuid.uuid5(uuid.uuid4(),str(uuid.uuid5(uuid.uuid4(),"Alphanet"))), 'blk_ligne_data': hashlib.sha256().hexdigest()}
    },
    {
        'System': {'blk_champ_sys': 'mTSlCieFwJ', 'blk_num': 2, 'blk_id': uuid.uuid5(uuid.uuid4(),"Alphanet"), 'blk_timestamp': int(datetime.datetime.now().timestamp()*1000000)},
        'Ligne': {'blk_ligne_num': 0, 'blk_ligne_id': uuid.uuid5(uuid.uuid4(),str(uuid.uuid5(uuid.uuid4(),"Alphanet"))), 'blk_ligne_data': hashlib.sha256().hexdigest()}
    },
    {
        'System': {'blk_champ_sys': 'fjgyPFDqOJ', 'blk_num': 3, 'blk_id': uuid.uuid5(uuid.uuid4(),"Alphanet"), 'blk_timestamp': int(datetime.datetime.now().timestamp()*1000000)},
        'Ligne': {'blk_ligne_num': 0, 'blk_ligne_id': uuid.uuid5(uuid.uuid4(),str(uuid.uuid5(uuid.uuid4(),"Alphanet"))), 'blk_ligne_data': hashlib.sha256().hexdigest()}
    },
]


pschem = fastavro.schema.parse_schema(schema)

with open('weather.avro', 'wb') as out:
   #fastavro.writer(out, pschem, fastavro.utils.generate_many(schema, 5))
   fastavro.writer(out, pschem, records)

print(fastavro.schema.fullname(pschem))

with open('weather.avro', 'rb') as fic:
    avro_reader = fastavro.reader(fic, pschem)
    for record in avro_reader:
        print(fastavro.validation.validate(record, pschem))
        print(record)
