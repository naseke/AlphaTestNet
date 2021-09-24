class toto:
    def __init__(self):
        self.dico = {'cmd': 'a'}
        self.nom = 'toto'
        self.rep = trt_rep()

    def trt_o(self, obj):
        pass

    def trt_rep(self):
        pass

    def trt(self, obj_name='toto'):
        from importlib import import_module
        class_ = getattr(import_module('tests.test'), obj_name)
        #class_ = getattr(None, obj_name)
        obj = class_()
        if obj.dico['cmd'] == 'a':
            print(obj.nom)
        else:
            obj.trt_o(obj)


class tutu(toto):

    def __init__(self):
        self.dico = {'cmd': 'b'}
        self.nom = 'tutu'
        self.index = 'foo'

    def trt_o(self, obj):
        print(obj.nom)



class tata(tutu):

    def __init__(self):
        self.dico = {'cmd': 'c'}
        self.nom = 'tata'

    def trt_o(self, obj):
        print(obj, obj.nom)

    def trt_rep(self):
        return self.index[1:2]


class A:

    def __init__(self):
        self.A = self.trt()

    def trt(self):
        pass


class B(A):

    def __init__(self):
        super().__init__()
        self.B = 'B'


class C(B):

    def trt(self):
        return 'C'


def main():
    t = A()

    print(t.A)


def verif_blk_content(bloc):
    from pickle import loads
    print(type(bloc.blk_content))
    for elem in bloc.blk_content:
        print(loads(elem).lne_content['fic_nom'], loads(elem).lne_id)

def main2():
    from lib.tools import affichage_block,find_root
    from etc.structure import block
    from lib.stock_hdd import hdd

    import os

    b = hdd().read_block(os.path.join(find_root(), 'cache', 'a0f50501-ad56-54c4-a90f-8778844e8adf'.replace("-", "")))
    #verif_blk_content(b)
    affichage_block(b, block)


if __name__ == "__main__":main()