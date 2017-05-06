import os

from flask import Blueprint, request
from flask_restful import reqparse, Resource, Api

from coalaip import CoalaIp, entities
from coalaip_bigchaindb.plugin import Plugin
from omi_api.utils import get_bigchaindb_api_url, queryparams_to_dict
from omi_api.queries import bdb_find
from omi_api.transformers import transform


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

recording_views = Blueprint('recording_views', __name__)
recording_api = Api(recording_views)


class RecordingListApi(Resource):
    def get(self):
        args = queryparams_to_dict(request.args)
        res = bdb_find(query=args, _type='CreativeWork')
        resp = []
        for doc in res:
            doc = doc['block']['transactions']['asset']['data']
            doc = transform(doc, 'CreativeWork->Recording')
            resp.append(doc)
        return resp

    def post(self):
        parser = reqparse.RequestParser()

        # These are the required parameters
        parser.add_argument('title', type=str, required=True, location='json')
        parser.add_argument('labels', type=list, required=True,
                            location='json')
        parser.add_argument('artists', type=list, required=True,
                            location='json')
        parser.add_argument('isrc', type=str, required=False,
                            location='json')
        args = parser.parse_args()

        manifestation = transform(args, 'Recording->CreativeWork')
        copyright_holder = {
            "public_key": os.environ.get('OMI_PUBLIC_KEY', None),
            "private_key": os.environ.get('OMI_PRIVATE_KEY', None)
        }

        # TODO: Do a mongodb query to extract the id of the work
        # OR: Maybe we just register the manifestation without the work for now
        # ?

        #copyright_, manifestation, work = coalaip.register_manifestation(
        #    manifestation_data=manifestation,
        #    copyright_holder=copyright_holder,
        #    work_data=work
        #)
        return 'The recording was successfully registered.', 200


recording_api.add_resource(RecordingListApi, '/recordings',
                           strict_slashes=False)
