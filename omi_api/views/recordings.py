import os

from flask import Blueprint
from flask_restful import reqparse, Resource, Api

from coalaip import CoalaIp, entities
from coalaip_bigchaindb.plugin import Plugin
from omi_api.models import recording_model
from omi_api.utils import get_bigchaindb_api_url
from omi_api.queries import bdb_find


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

recording_views = Blueprint('recording_views', __name__)
recording_api = Api(recording_views)


class RecordingListApi(Resource):
    def get(self):
        # TODO method can be generalized to utility probably
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('name', type=str)
        #TODO add all other parameters
        args = dict(parser.parse_args())

        res = bdb_find(query=args, _type='CreativeWork')
        resp = []
        for doc in res:
            #todo this is super ugly
            doc = doc['block']['transactions']['asset']['data']
            print(doc)
            doc = {
                'title': doc['name'],
                'labels': doc['labels'],
                'artists': doc['artists'],
            }
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

        # Here we're transforming from OMI to COALA
        manifestation = {
            'name': args['title'],
            'labels': args['labels'],
            'artists': args['artists'],
        }

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
