from collections import namedtuple
import os


BigchainDBConfiguration = namedtuple('BigchainDBConfiguration', [
    'hostname',
    'port',
])


# Double check in case the environment variable is sent via Docker,
# which will send empty strings for missing environment variables
BDB_HOST = os.environ.get('BDB_NODE_HOST', None)
if not BDB_HOST:
    BDB_HOST = 'localhost'

BDB_PORT = os.environ.get('BDB_NODE_PORT', None)
if not BDB_PORT:
    BDB_PORT = '9984'


def get_bigchaindb_configuration():
    return BigchainDBConfiguration(BDB_HOST, BDB_PORT)


def get_bigchaindb_api_url():
    hostname, port = get_bigchaindb_configuration()
    return 'http://{hostname}:{port}'.format(hostname=hostname, port=port)

def queryparams_to_dict(queryparams):
    queryparams = dict(queryparams)
    for k, v in queryparams.items():
        queryparams[k] = v[0]
    return queryparams
