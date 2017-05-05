import os

from flask import Blueprint
from flask_restful import reqparse, Resource, Api

from coalaip import CoalaIp, entities
from coalaip_bigchaindb.plugin import Plugin
from omi_api.models import recording_model
from omi_api.utils import get_bigchaindb_api_url


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

recording_views = Blueprint('recording_views', __name__)
recording_api = Api(recording_views)


class RecordingListApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        # These are the required parameters
        parser.add_argument('title', type=str, required=True, location='json')
        parser.add_argument('composers', type=list, required=True,
                            location='json')
        parser.add_argument('songwriters', type=list, required=True,
                            location='json')
        parser.add_argument('publishers', type=list, required=True,
                            location='json')
        args = parser.parse_args()

        # Here we're transforming from OMI to COALA
        work = {
            'name': args['title'],
            'composers': args['composers'],
            'songwriters': args['songwriters'],
            'publishers': args['publishers'],
        }

        copyright_holder = {
            "public_key": os.environ.get('OMI_PUBLIC_KEY', None),
            "private_key": os.environ.get('OMI_PRIVATE_KEY', None)
        }

        # TODO: Do a mongodb query to extract the id of the work

        copyright_, manifestation, work = coalaip.register_manifestation(
            manifestation_data=manifestation,
            copyright_holder=copyright_holder,
            work_data=work
        )

        return 'The recording was successfully registered.', 200


recording_api.add_resource(RecordingListApi, '/recordings',
                           strict_slashes=False)
