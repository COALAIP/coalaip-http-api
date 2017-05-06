import os

def get(key, default=None):
    # Double check in case the environment variable is sent via Docker,
    # which will send empty strings for missing environment variables
    value = os.environ.get(key)
    if not value:
        return default
    return value


ORG_NAME = get('OMI_ORG_NAME')
PUBLIC_KEY = get('OMI_PUBLIC_KEY')
PRIVATE_KEY = get('OMI_PRIVATE_KEY')
BDB_HOST = get('BDB_NODE_HOST', 'localhost')
BDB_PORT = get('BDB_NODE_PORT', '9984')
MDB_HOST = get('MONGODB_HOST', 'localhost')
MDB_PORT = get('MONGODB_PORT', '27017')
