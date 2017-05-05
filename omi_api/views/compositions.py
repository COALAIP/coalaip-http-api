from flask import Blueprint
from flask_restful import reqparse, Resource, Api

from coalaip import CoalaIp, entities
from coalaip_bigchaindb.plugin import Plugin
from omi_api.utils import get_bigchaindb_api_url


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

composition_views = Blueprint('composition_views', __name__)
composition_api = Api(composition_views)


class CompositionListApi(Resource):
    #def get(self, entity_id):
    #    composition = entities.Work.from_persist_id(
    #        entity_id, plugin=coalaip.plugin, force_load=True)
    #    return composition.to_jsonld()

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
            "public_key": "Cxj6Pct7T2hLhUh455tbvDWkVDY1vW5aoRGHZCtQkNKQ",
            "private_key": "8vVgr68Cb5RzUm89nkALvVBmmSoBdC58MTAmqGr8HfYy",
        }

        work = coalaip.register_work(
            work_data=work,
            copyright_holder=copyright_holder
        )

        work_jsonld = work.to_jsonld()
        work_jsonld['@id'] = work.persist_id

        return work_jsonld, 200


composition_api.add_resource(CompositionListApi, '/compositions',
                             strict_slashes=False)
