import json
import time

from bases.FrameworkServices.UrlService import UrlService

update_every = 30

ORDER = [
    'blockindex',
    'difficulty',
    'mempool',
    'secmem',
    'network_connections',
    'unconfirmed_transactions',
    'last_block_t',
    'uptime',
]

CHARTS = {
    'blockindex': {
        'options': [None, 'Blockchain Index', 'count', 'blockchain', 'bitcoind.blockindex', 'area'],
        'lines': [
            ['blockchain_blocks', 'blocks', 'absolute'],
        ]
    },
    'difficulty': {
        'options': [None, 'Blockchain Difficulty', 'difficulty', 'blockchain', 'bitcoind.difficulty', 'line'],
        'lines': [
            ['blockchain_difficulty', '', 'absolute'],
        ],
    },
    'mempool': {
        'options': [None, 'MemPool', 'MiB', 'memory', 'bitcoind.mempool', 'area'],
        'lines': [
            ['mempool_max', 'Max', 'absolute', None, 1024*1024],
            ['mempool_current', 'Usage', 'absolute', None, 1024*1024],
        ],
    },
    'secmem': {
        'options': [None, 'Memory Usage', 'KiB', 'memory', 'bitcoind.secmem', 'area'],
        'lines': [
            ['secmem_total', 'Total', 'absolute', None, 1024],
            ['secmem_locked', 'Locked', 'absolute', None, 1024],
            ['secmem_used', 'Used', 'absolute', None, 1024],
        ],
    },
    'network_connections': {
        'options': [None, 'Network Connections', 'count', 'network', 'bitcoind.network_connections', 'line'],
        'lines': [
            ['network_connections', 'Connections', 'absolute'],
        ],
    },
    'unconfirmed_transactions': {
        'options': [None, 'Unconfirmed Transactions', 'count', 'network', 'bitcoind.unconfirmed_transactions', 'line'],
        'lines': [
            ['mempool_txcount', 'TX Count', 'absolute'],
        ],
    },
    'last_block_t': {
        'options': [None, 'Time since last block', 'minutes', 'last_block_time', 'bitcoind.last_block_t', 'line'],
        'lines': [
            ['last_block_unix_time', 'last_block', 'absolute', None, 60],
        ],
    },
    'uptime': {
        'options': [None, 'Uptime in seconds', 'seconds', 'uptime', 'bitcoind.uptime', 'line'],
        'lines': [
            ['node_uptime', 'uptime', 'absolute'],
        ],
    },
}

METHODS = {
    'getblockchaininfo': lambda r: {
        'blockchain_blocks': r['blocks'],
        'blockchain_headers': r['headers'],
        'blockchain_difficulty': r['difficulty'],
    },
    'getmempoolinfo': lambda r: {
        'mempool_txcount': r['size'],
        'mempool_txsize': r['bytes'],
        'mempool_current': r['usage'],
        'mempool_max': r['maxmempool'],
    },
    'getmemoryinfo': lambda r: dict([
        ('secmem_' + k, v) for (k,v) in r['locked'].items()
    ]),
    'getnetworkinfo': lambda r: {
        'network_timeoffset' : r['timeoffset'],
        'network_connections': r['connections'],
    },
    'getchaintxstats': lambda r: {
        'last_block_unix_time' : r['time'],
    },
    'uptime': lambda r: {
        'node_uptime' : r,
    },
}

JSON_RPC_VERSION = '1.0'

class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.host = self.configuration.get('host', '127.0.0.1')
        self.port = self.configuration.get('port', 8332)
        self.url = '{scheme}://{host}:{port}'.format(
            scheme=self.configuration.get('scheme', 'http'),
            host=self.host,
            port=self.port,
        )
        self.method = 'POST'
        self.header = {
            'Content-Type': 'application/json',
        }

    def _get_data(self):
        batch = []

        for i, method in enumerate(METHODS):
            batch.append({
                'jsonrpc': JSON_RPC_VERSION,
                'id': i,
                'method': method,
                'params': [],
            })

        result = self._get_raw_data(body=json.dumps(batch))

        if not result:
            return None

        result = json.loads(result.decode('utf-8'))
        data = dict()

        for i, (_, handler) in enumerate(METHODS.items()):
            r = result[i]
            data.update(handler(r['result']))

        data["last_block_unix_time"] = time.time() - data["last_block_unix_time"]

        return data
