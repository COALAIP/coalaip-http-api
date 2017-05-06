import os

from pymongo import MongoClient

def bdb():
    return MongoClient(os.environ.get('MONGODB_HOST', None),
                       int(os.environ.get('MONGODB_PORT', None)),
                       ssl=False)

def bdb_coll():
    return bdb()['bigchain']['bigchain']

def bdb_find(query, _type):
    # TODO: make this a global?
    base = 'block.transactions.asset.data'

    match = []
    for key, value in query.items():
        # Filter out None values
        if value:
            match.append({'{}.{}'.format(base, key): value})
    match.append({'{}.@type'.format(base): _type})
    match = {'$and': match}

    pipeline = [
        {'$match': match},
        {'$unwind': '$block.transactions'},
        {'$match': match},
        {'$project': {
            '_id': False,
            'block.transactions.asset.data': True
        }}
    ]

    cur = bdb_coll().aggregate(pipeline)
    return cur
