import asyncio
from lib.parametres import Params
from lib.tools import get_ip
from importlib import import_module

async def main():
    p = Params()
    services = ['CACHE', 'WALLET', 'FABRIK', 'VALIDATOR', 'NODE', ]
    port_s = "_S"
    ip_service = "IP_"
    ports_services = [f"PORT_{e}" for e in services]
    ports_services += [f"PORT_{e}{port_s}" for e in services]

    for elem in ports_services:
        if elem in p.PARAMS.keys() and p.PARAMS[elem] != '':
            port = int(p.PARAMS[elem])
            if f"{ip_service}{elem.split('_')[1]}" in p.PARAMS.keys() and p.PARAMS[f"{ip_service}{elem.split('_')[1]}"] != '':
                host = p.PARAMS[f"{ip_service}{elem.split('_')[1]}"]
            else:
                host = get_ip()
            fonc = getattr(import_module(f"services.{elem.split('_')[1].casefold()}"), "start")
            asyncio.ensure_future(fonc(host, port))


if __name__ == "__main__": asyncio.run(main())

