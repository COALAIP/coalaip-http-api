from flask import Blueprint, request
from flask_restful import reqparse, Resource, Api

from coalaip import CoalaIp, entities
from coalaip_bigchaindb.plugin import Plugin

from omi_api import config
from omi_api.utils import get_bigchaindb_api_url, queryparams_to_dict
from omi_api.transformers import transform
from omi_api.queries import bdb_find


coalaip = CoalaIp(Plugin(get_bigchaindb_api_url()))

composition_views = Blueprint('composition_views', __name__)
composition_api = Api(composition_views)


class CompositionListApi(Resource):
    def get(self):
        args = queryparams_to_dict(request.args)
        res = bdb_find(query=args, _type='AbstractWork')
        resp = []
        for doc in res:
            doc = doc['block']['transactions']['asset']['data']
            doc = transform(doc, 'AbstractWork->Composition')

            resp.append(doc)
        return resp

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

        work = transform(args, 'Composition->AbstractWork')
        copyright_holder = {
            'public_key': config.PUBLIC_KEY,
            'private_key': config.PRIVATE_KEY
        }

        work = coalaip.register_work(
            work_data=work,
            copyright_holder=copyright_holder
        )

        print('Work/Composition registered under: ', work.persist_id)

        return 'The composition was successfully registered.', 200


composition_api.add_resource(CompositionListApi, '/compositions',
                             strict_slashes=False)
