from omi_api import config
from collections import namedtuple


BigchainDBConfiguration = namedtuple('BigchainDBConfiguration', [
    'hostname',
    'port',
])


def get_bigchaindb_configuration():
    return BigchainDBConfiguration(config.BDB_HOST, config.BDB_PORT)


def get_bigchaindb_api_url():
    hostname, port = get_bigchaindb_configuration()
    return 'http://{hostname}:{port}'.format(hostname=hostname, port=port)

def queryparams_to_dict(queryparams):
    queryparams = dict(queryparams)
    for k, v in queryparams.items():
        queryparams[k] = v[0]
    return queryparams
