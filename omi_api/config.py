import os


def get(key, default=None):
    # Double check in case the environment variable is sent via Docker,
    # which will send empty strings for missing environment variables
    value = os.environ.get(key)
    if not value:
        return default
    return value


ORG_NAME = get('OMI_ORG_NAME')
BDB_HOST = get('OMI_BDB_NODE_HOST', 'localhost')
BDB_PORT = get('OMI_BDB_NODE_PORT', '9984')
MDB_HOST = get('OMI_MDB_NODE_HOST', 'localhost')
MDB_PORT = get('OMI_MDB_NODE_PORT', '27017')
