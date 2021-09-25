class pre_cmds:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


def version():
    return 0.01

# Version Simple
def pre_read_cmd(obj, **msg):
    from lib.couleurs import AffichageColor

    param_dict = ['cmd_test','get_services', 'trsf_config', 'trsf_ligne', 'get_blk_id_prev_fabrik', 'get_blk_id_prev_validator', 'get_blk_id_prev', 'trsf_bloc']
    param_obj_dict = ['get_struct_cmd', 'trf_pre_cmds', 'lower_version', 'get_net_conf', 'get_list_node', ]

    if msg['command'] in param_dict:
        return obj.moduleManager.get_obj_throught_module(obj.moduleManager.get_module_by_class(msg['command'])).read_cmd(**msg)
    elif msg['command'] in param_obj_dict:
        return obj.moduleManager.get_obj_throught_module(obj.moduleManager.get_module_by_class(msg['command'])).read_cmd(obj, **msg)
    else:
        AffichageColor().msg_FAIL(f"Je pratique couramment six millions de formes de communication... pour le moment il me faudrait connaitre la commande '{msg['command']}'")


def pre_write_cmd(obj, cmd, chaine='', **msg):
    from lib.couleurs import AffichageColor

    param_vide = ['trf_pre_cmds', 'cmd_test', 'get_net_conf', 'get_list_node', ]
    # param_obj = []
    param_str = ['get_services', 'trsf_config', 'trsf_ligne', 'get_blk_id_prev_fabrik', 'get_blk_id_prev_validator', 'get_blk_id_prev', 'trsf_bloc']
    param_obj_str = ['get_struct_cmd', 'lower_version', ]

    if cmd in param_vide:
        return obj.moduleManager.get_obj_throught_module(obj.moduleManager.get_module_by_class(cmd)).write_cmd()
    elif cmd in param_obj_str:
        return obj.moduleManager.get_obj_throught_module(obj.moduleManager.get_module_by_class(cmd)).write_cmd(obj, chaine)
    # elif cmd in param_obj:
    #     return obj.moduleManager.get_obj_throught_module(obj.moduleManager.get_module_by_class(cmd)).write_cmd(obj)
    elif cmd in param_str:
        return obj.moduleManager.get_obj_throught_module(obj.moduleManager.get_module_by_class(cmd)).write_cmd(chaine)
    else:
        AffichageColor().msg_FAIL(f"Je pratique couramment six millions de formes de communication... pour le moment il me faudrait connaitre la commande '{cmd}'")


def pre_write_cmd_rep(obj, cmd, chaine='', **msg):
    from lib.couleurs import AffichageColor

    param_obj = ['get_net_conf', 'get_list_node', 'get_services']

    if cmd in param_obj:
        return obj.moduleManager.get_obj_throught_module(obj.moduleManager.get_module_by_class(cmd)).write_cmd_rep(obj)
    else:
        AffichageColor().msg_FAIL(f"Je pratique couramment six millions de formes de communication... pour le moment il me faudrait connaitre la commande '{cmd}'")


# Version en Coroutine
async def pre_read_cmd_coro(obj, **msg):
    return pre_read_cmd(obj, **msg)


async def pre_write_cmd_coro(obj, cmd, chaine='', **msg):
    return pre_write_cmd(obj, cmd, chaine, **msg)


async def pre_write_cmd_rep_coro(obj, cmd, chaine='', **msg):
    return pre_write_cmd_rep(obj, cmd, chaine, **msg)
