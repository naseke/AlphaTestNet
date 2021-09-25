from etc import contants, structure
import uuid
import datetime
import hashlib


class line:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class Line:

    def __init__(self, lne_namespace, lne_content_version, lne_type='user', **lne):
        if lne:
            # validation de la ligne avant de créer l'instance
            lne2 = lne.copy()
            lne2['lne_hash'] = ''
            lne2['lne_hash'] = hashlib.sha512(str(lne2).encode()).hexdigest()
            if lne['lne_hash'] == lne2['lne_hash']:
                self.line = lne
            else:
                raise AttributeError("le hash de la ligne n'est pas bon !")
        else:
            if contants.LNE_VERSION == "0.1.0":
                self.line = self.__init_lne_0_01(lne_namespace, lne_content_version, lne_type)

    def __init_lne_0_01(self, lne_namespace, lne_content_version, lne_type) -> []:
        lne = {
            "lne_id": uuid.uuid5(uuid.uuid4(), contants.BLK_NET_NAME).hex,
            "lne_timestamp": int(datetime.datetime.now().timestamp() * 1000000),
            "lne_version": contants.LNE_VERSION,
            "lne_hash": "",
            "lne_config": {'lne_config_key': ['lne_content_keys', 'lne_type', 'lne_namespace'], 'lne_content_key': [], 'lne_type': lne_type, 'lne_namespace': lne_namespace, 'lne_version': lne_content_version},
            "lne_content": {},
        }
        return lne

    def __getattribute__(self,arg):
        cles = [e['name'] for e in structure.line['fields']]
        if arg in cles: return self.line[arg]
        else: return super().__getattribute__(arg)

    def set_hash(self):
        if self.line['lne_content'] == {}:
            raise ValueError('ligne incomplète')
        elif self.line['lne_hash'] != "":
            raise ValueError('ligne verouillée')
        else:
            self.line['lne_hash'] = hashlib.sha512(str(self.line).encode()).hexdigest()

    def set_content(self, k_c, v_c):
        if k_c not in self.line['lne_config']['lne_content_key']:
            self.line['lne_config']['lne_content_key'].append(k_c)
        self.line['lne_content'][k_c] = v_c

    def __str__(self):
        return str(self.line)


def main():

    from lib import gas

    l = Line("test","0.1")
    l.set_content('gasethdico', gas.Gas().dico)
    l.set_hash()
    l.line["lne_timestamp"] = int(datetime.datetime.now().timestamp() * 1000000)
    c = Line("test","0.1",**l.line)
    print(l)
    print(c)
    print(l.lne_hash)


if __name__ == "__main__": main()
