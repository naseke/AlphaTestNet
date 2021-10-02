from lib import couleurs, tools


class toto:

    def __init__(self):
        self.moduleManager = tools.ManagerClass('../cmds')
        self.pre_cmds = tools.ManagerClassPreCMDS()

    def go(self):
        print(self.pre_cmds.get_func_throught_module('pre_write_cmd')(self, 'stop', ''))


def main():
    toto().go()


if __name__ == "__main__": main()