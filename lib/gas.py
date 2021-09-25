from lib import parametres, apibinance
import requests
import json

from lib import outils


class gas:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION

class Gas:

    def __init__(self):
        self.__p = parametres.Params()
        self.dico = self.__get_priceGas(self.__p.PARAMS['GAS_URL'])
        self.__api = apibinance.Binance_api()

    # findef

    def __get_priceGas(self, url):

        r = requests.get(url)

        if 'json' in r.headers['content-type']:
            return r.json()
        # optimisation_gas(r.json())
        else:
            return "0"

    # finSi

    # findef

    def get_prixcours(self):
        return self.__api.apibin.get_avg_price(symbol=self.__p.PARAMS['GAS_COURS'])['price']

    # findef

    def get_prix_unitaire_gaz(self, speed):
        return self.__qte_gaz(self.dico[speed])

    # findef

    def get_gasqteeth(self, speed):
        return self.__gwei2eth(self.__qte_gaz(self.dico[speed])) * float(self.__p.PARAMS['GAS_NB'])

    # findef

    def get_prixgas(self, speed):
        return self.__gwei2eth(self.__qte_gaz(self.dico[speed])) * float(self.__p.PARAMS['GAS_NB']) * float(
            self.__api.apibin.get_avg_price(symbol=self.__p.PARAMS['GAS_COURS'])['price'])

    # findef

    def __qte_gaz(self, str):
        # afin de na pas avoir à répéter la règle
        return str / 10

    # findef

    def __gwei2eth(self, str):
        # afin de na pas avoir à répéter la règle
        return str * 0.000000001

    # findef

    def __str__(self):
        return str(self.dico)
# findef

# finClass


def main():
    gaz = Gas()
    print(gaz.get_prixcours())
    print(gaz)
    print(gaz.get_prixgas("fastest"))

# findef


if __name__ == "__main__": main()
