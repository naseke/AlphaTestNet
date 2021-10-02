"""
Usage:
  alphanet node ( start | stop ) [-p | --port] [-a | --addr]
  alphanet cache ( start | stop ) [-p | --port] [-a | --addr]
  alphanet fabrik ( start | stop ) [-p | --port] [-a | --addr]
  alphanet validator ( start | stop ) [-p | --port] [-a | --addr]
  alphanet -h | --help
  alphanet --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -p --port     port
  -a --addr     address host
"""

import asyncio
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['cache']:
        from services import cache
        if arguments['start']:
            asyncio.run(cache.main())
        else:
            asyncio.run(cache.commande('stop'))
    elif arguments['fabrik']:
        from services import fabrik
        if arguments['start']:
            asyncio.run(fabrik.main())
        else:
            asyncio.run(fabrik.commande('stop'))
    elif arguments['node']:
        from services import node
        if arguments['start']:
            asyncio.run(node.main())
        else:
            asyncio.run(node.commande('stop'))
    elif arguments['validator']:
        from services import validator

        if arguments['start']:
            asyncio.run(validator.main())
        else:
            asyncio.run(validator.commande('stop'))
