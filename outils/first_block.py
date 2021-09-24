import os
from etc.structure import block,line
from lib.block import Block
from lib.line import Line
import base64
from hashlib import sha512
from lib.tools import find_root, get_name, affichage_block
from lib.stock_hdd import hdd
from lib.couleurs import bcolors


def init_list_vers_prg(list_fic, id):
    from importlib import import_module

    resultat = []

    for rep in list_fic:
        if list_fic[rep]:
            lst = list_fic[rep].copy()
            lst = list(map(lambda v: getattr(v, v.__name__.split('.')[1]).get_VERSION(), list(map(lambda m: import_module(m), list(map(lambda e: f"{rep}.{e.replace('.py', '')}", lst))))))
            lst2 = [id] * len(lst)
            resultat.extend(tuple(zip(list_fic[rep], lst, lst2)))
    return resultat


def main():

    bloc = Block()

    list_fic_prg = {
        'cache': [],
        'cmds': ['done.py', 'get_entete_msg.py', 'get_net_conf.py', 'get_struct_cmd.py', 'lower_version.py', 'misunderstood.py', 'trf_pre_cmds.py', 'trsf_bloc.py', 'trsf_ligne.py', 'wrong.py'],
        'etc': ['structure.py'],
        'lib': ['AlphaClient.py', 'AlphaServer.py', 'apibinance.py', 'block.py', 'couleurs.py', 'gas.py', 'line.py', 'ordonnanceur.py', 'parametres.py', 'pre_cmds.py', 'Singleton.py', 'stock_hdd.py', 'tools.py',],
        'services': ['node.py', 'cache.py', 'fabrik.py'],
    }

    list_vers_prg = init_list_vers_prg(list_fic_prg, bloc.blk_id)

    bloc.set_config_version()
    bloc.set_config('blk_prg_fic', list_fic_prg)
    bloc.set_config('blk_prg_vers', list_vers_prg)
    bloc.set_config('BLK_VERSION', '0.1.0')
    bloc.set_config('LNE_VERSION', '0.1.0')
    bloc.set_config('PORT_NODE', '8000', True)
    bloc.set_config('PORT_CACHE', '8010', True)
    bloc.set_config('PORT_FABRIK', '8020', True)
    bloc.set_config('PORT_VALIDATOR', '8030', True)

    # lne_config = {'lne_config_keys': ['lne_content_keys', 'lne_type', 'lne_namespace'], 'lne_content_keys': ['fic_nom', 'fic_hash', 'fic_sign', 'fic_content'], 'lne_type': 'prg_core', 'lne_namespace': 'Alphatestnet'}

    for rep in list_fic_prg:
        if list_fic_prg[rep]:
            ligne = Line('Alphatestnet_Landean_area', '0.01', 'prg_core')
            for fichier in list_fic_prg[rep]:
                ligne.set_content('fic_nom', fichier)
                with open(os.path.join(find_root(), rep, fichier),'rb') as fic:
                    ligne.set_content('file_content', base64.b64encode(fic.read()))
                ligne.set_content('fic_sign', sha512(get_name().encode()).hexdigest())
                ligne.set_content('fic_hash', sha512(ligne.lne_content['file_content']).hexdigest())
                bloc.add_line(ligne)
                ligne = Line('Alphatestnet_Landean_area', '0.01', 'prg_core')
    bloc.set_hash()
    #affichage_block(0,'d',[e['name'] for e in block['fields']], bloc.bloc[0])
    affichage_block(bloc, block)
    hdd().write_block(bloc)
    b = bloc.blk_id
    print(b)



    #bloc2 = {'blk_content': ["[{'lne_id': '371e4b7e5a3f57bca131d97e4050ba34', 'lne_timestamp': 1629770129285834, 'lne_version': '0.1.0', 'lne_hash': '', 'lne_config': {'lne_config_key': ['lne_content_key'], 'lne_content_key': []}, 'lne_content': {'fic_nom': 'done.py', 'file_content': b'Y2xhc3MgZG9uZToNCg0KICAgIF9fU1RSVUNUID0geydkb25lJzogW119DQogICAgX19WRVJTSU9OID0gJzAuMDEnDQoNCiAgICBkZWYgcmVhZF9jbWQoc2VsZik6DQogICAgICAgIHBhc3MNCg0KICAgIGRlZiB3cml0ZV9jbWQoc2VsZik6DQogICAgICAgIG1zZyA9IHsNCiAgICAgICAgICAgICdjb21tYW5kJzogJ2RvbmUnLA0KICAgICAgICAgICAgJ3ZlcnNpb25fY21kJzogc2VsZi5fX1ZFUlNJT04sDQogICAgICAgIH0NCiAgICAgICAgcmV0dXJuIG1zZw0KDQogICAgZGVmIGdldF9TVFJVQ1Qoc2VsZik6DQogICAgICAgIHJldHVybiBzZWxmLl9fU1RSVUNUDQoNCiAgICBAY2xhc3NtZXRob2QNCiAgICBkZWYgZ2V0X1ZFUlNJT04oc2VsZik6DQogICAgICAgIHJldHVybiBzZWxmLl9fVkVSU0lPTg0K', 'fic_sign': '7855d5a191b8f748a78334ac5e2ec1bd24018ef0b45e3fa478e5cb5c696ea4dd8f92e18d675ad808d24b54976bb394e83ff6f60c5e1e49353feee54b2caa0053', 'fic_hash': '145f35fb48a2ef21f3fe3f823f244fd7629b19a78b35576b9b479076a2297f2d8a2a85775a6f869ee18297cc758831b99d68c0cbc2a5947c0f13ecb038dd274a'}}]"]}
    #affichage_block(0,'d',bloc2.keys(), bloc2)



if __name__ == "__main__": main()

