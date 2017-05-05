from flask import Blueprint
from flask_restful import Resource, Api

from coalaip import CoalaIp, entities
from coalaip_bigchaindb.plugin import Plugin
from omi_api.utils import get_bigchaindb_api_url


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

composition_views = Blueprint('composition_views', __name__)
composition_api = Api(composition_views)


class CompositionApi(Resource):
    def get(self, entity_id):
        composition = entities.Work.from_persist_id(
            entity_id, plugin=coalaip.plugin, force_load=True)
        return composition.to_jsonld()


composition_api.add_resource(CompositionApi, '/compositions/<entity_id>',
                             strict_slashes=False)
