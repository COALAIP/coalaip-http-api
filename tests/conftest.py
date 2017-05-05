from omi_api.server import create_app

from flask import url_for
import pytest


@pytest.fixture
def app():
    app = create_app({'debug': True})
    return app


@pytest.fixture
def alice(client):
    return client.post(url_for('user_views.userapi')).json


@pytest.fixture
def bob(client):
    return client.post(url_for('user_views.userapi')).json


@pytest.fixture
def carly(client):
    return client.post(url_for('user_views.userapi')).json


@pytest.fixture
def created_manifestation_resp(client, alice):
    import json
    from time import sleep
    payload = {
        'manifestation': {
            'name': 'The Fellowship of the Ring',
            'datePublished': '29-07-1954',
            'url': 'http://localhost/lordoftherings.txt',
        },
        'copyrightHolder': alice,
        'work': {
            'name': 'The Lord of the Rings Triology',
            'author': 'J. R. R. Tolkien',
        },
    }

    resp = client.post(url_for('manifestation_views.manifestationlistapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})

    # Sleep for a bit to let the transaction become valid
    sleep(3)
    return resp.json


@pytest.fixture
def created_derived_right(client, alice, created_manifestation_resp):
    import json
    from time import sleep

    copyright_id = created_manifestation_resp['copyright']['@id']
    copyright_id = copyright_id.split('../rights/')[1]
    payload = {
        'currentHolder': alice,
        'right': {
            'license': 'http://www.ascribe.io/terms',
        },
        'sourceRightId': copyright_id,
    }

    resp = client.post(url_for('right_views.rightlistapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})

    # Sleep for a bit to let the transaction become valid
    sleep(3)
    return resp.json['right']


@pytest.fixture
def transferred_derived_right(client, alice, bob, created_derived_right):
    import json
    from time import sleep

    payload = {
        'rightId': created_derived_right['@id'],
        'rightsAssignment': {
            'action': 'loan',
        },
        'currentHolder': alice,
        'to': {
            'publicKey': bob['publicKey'],
            'privateKey': None,
        }
    }

    client.post(url_for('right_views.righttransferapi'),
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'})

    # Sleep for a bit to let the transaction become valid
    sleep(3)
    return created_derived_right


@pytest.fixture
def retransferred_derived_right(client, bob, carly, transferred_derived_right):
    import json
    from time import sleep

    payload = {
        'rightId': transferred_derived_right['@id'],
        'rightsAssignment': {
            'action': 'loan',
        },
        'currentHolder': bob,
        'to': {
            'publicKey': carly['publicKey'],
            'privateKey': None,
        }
    }

    client.post(url_for('right_views.righttransferapi'),
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'})

    # Sleep for a bit to let the transaction become valid
    sleep(3)
    return transferred_derived_right
