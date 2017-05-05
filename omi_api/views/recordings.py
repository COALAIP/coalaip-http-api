from flask import Blueprint
from flask_restful import reqparse, Resource, Api

from coalaip import CoalaIp, entities
from coalaip_bigchaindb.plugin import Plugin
from omi_api.models import recording_model
from omi_api.utils import get_bigchaindb_api_url


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

recording_views = Blueprint('recording_views', __name__)
recording_api = Api(recording_views)


class RecordingApi(Resource):
    def get(self, entity_id):
        recording = entities.Manifestation.from_persist_id(
            entity_id, plugin=coalaip.plugin, force_load=True)
        return recording.to_jsonld()


class RecordingListApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        #TODO: Change to parse OMI body
        #parser.add_argument('manifestation', type=manifestation_model,
        #                    required=True, location='json')
        #parser.add_argument('work', type=work_model, required=True,
        #                    location='json')
        #parser.add_argument('copyrightHolder', type=user_model, required=True,
        #                    location='json')
        #args = parser.parse_args()

        #manifestation = args['manifestation']
        #work = args['work']

        #copyright_holder = args['copyrightHolder']
        #copyright_holder = {
        #    'public_key': copyright_holder.pop('publicKey'),
        #    'private_key': copyright_holder.pop('privateKey')
        #}

        #copyright_, manifestation, work = coalaip.register_manifestation(
        #    manifestation_data=manifestation,
        #    copyright_holder=copyright_holder,
        #    work_data=work)

        # Add the appropraite @id to the JSON-LD
        res = {}
        #for (entity, id_template, key) in [
        #        (copyright_, '../rights/{}', 'copyright'),
        #        (manifestation, '{}', 'manifestation'),
        #        (work, '../works/{}', 'work')]:
        #    ld_data = entity.to_jsonld()
        #    ld_data['@id'] = id_template.format(entity.persist_id)
        #    res[key] = ld_data

        return res


recording_api.add_resource(RecordingListApi, '/recordings',
                           strict_slashes=False)
