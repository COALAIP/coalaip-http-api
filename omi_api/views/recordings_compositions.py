# Note: this module doesn't use CoalaIP because the current implementation
# doesn't allow to register a work, a manifestation, and connect them
# *afterwards*. This feature is not supported by the OMI API 1.0 as well.
# The correct way to fix this issue would be to:
# - add a new endpoint to the OMI spec
# - add a new model to CoalaIP spec
# - change the code in our Python compatible CoalaIP module
# - reconciliate everything here
#
# Since we are time bounded, we will just do a quick'n'drty™ implementation.

from flask import Blueprint, request
from flask_restful import reqparse, Resource, Api

from bigchaindb_driver import BigchainDB

from omi_api import config
from omi_api.transformers import transform
from omi_api.utils import get_bigchaindb_api_url, queryparams_to_dict
from omi_api.queries import bdb_find, unpack


bdb = BigchainDB(get_bigchaindb_api_url())

recordings_compositions_views = Blueprint('recordings_compositions_views',

                                          __name__)
recordings_compositions_api = Api(recordings_compositions_views)


class RecordingsCompositionsAPI(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('isrc', type=str)
        parser.add_argument('iswc', type=str)

        args = queryparams_to_dict(request.args)
        results = []

        # First we need to look for all the recordings connected
        # to the composition (or the other way around, depending
        # on the user's query)
        match = map(unpack, bdb_find(query=args, _type='LinkToWork'))

        # If the user searched by `isrc` (aka recording)
        # then we need to return all the linked compositions.
        if 'isrc' in args:
            queries = [{'iswc': x['iswc']} for x in match]
            transformation = 'AbstractWork->Composition'
            _type = 'AbstractWork'
            key = 'composition'
        # otherwise we return the linked recordings.
        else:
            queries = [{'isrc': x['isrc']} for x in match]
            transformation = 'CreativeWork->Recording'
            _type = 'CreativeWork'
            key = 'recording'

        for query in queries:
            for result in bdb_find(query=query, _type=_type):
                result = transform(unpack(result), transformation)
                results.append({key: result})

        return {
            'count': len(results),
            'total': len(results),
            'offset': 0,
            'results': results
        }

    def post(self):
        parser = reqparse.RequestParser()

        # These are the required parameters
        parser.add_argument('isrc', type=str, required=True, location='json')
        parser.add_argument('iswc', type=str, required=True, location='json')
        args = parser.parse_args()

        # Here we're creating the payload for the tx mimicking
        # a CoalaIP type using `@type: LinkToWork`.
        # This is *not* part of the specification yet.
        link = {'@type': 'LinkToWork',
                'isrc': args['isrc'],
                'iswc': args['iswc']}

        tx = bdb.transactions.prepare(
                operation='CREATE',
                signers=config.PUBLIC_KEY,
                asset={'data': link})

        signed_tx = bdb.transactions.fulfill(tx, private_keys=config.PRIVATE_KEY)
        bdb.transactions.send(signed_tx)

        return 'Composition and Recording were successfully connected.', 200


recordings_compositions_api.add_resource(
    RecordingsCompositionsAPI,
    '/recordings/compositions',
    strict_slashes=False)
