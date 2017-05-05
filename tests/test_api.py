import json

from flask import url_for


def test_create_user(client):
    resp = client.post(url_for('user_views.userapi'))
    assert resp.status_code == 200
    assert resp.json['publicKey']
    assert resp.json['privateKey']


def test_create_manifestation(client, alice):
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

    expected = {
        'work': {
            '@context': ['<coalaip placeholder>', 'http://schema.org/'],
            '@type': 'AbstractWork',
            'name': 'The Lord of the Rings Triology',
            'author': 'J. R. R. Tolkien',
        },
        'manifestation': {
            '@context': ['<coalaip placeholder>', 'http://schema.org/'],
            '@type': 'CreativeWork',
            'name': 'The Fellowship of the Ring',
            'datePublished': '29-07-1954',
            'url': 'http://localhost/lordoftherings.txt',
        },
        'copyright': {
            '@context': ['<coalaip placeholder>', 'http://schema.org/'],
            '@type': 'Copyright',
        },
    }
    resp = client.post(url_for('manifestation_views.manifestationlistapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})
    resp_dict = resp.json
    copyright_ = resp_dict['copyright']
    manifestation = resp_dict['manifestation']
    work = resp_dict['work']

    assert bool(copyright_['rightsOf']) is True
    assert bool(manifestation['manifestationOfWork']) is True

    # Check @ids
    assert copyright_['@id'].startswith('../rights/')
    assert bool(copyright_['@id'].strip('../rights/')) is True
    assert bool(manifestation['@id']) is True
    assert work['@id'].startswith('../works/')
    assert bool(work['@id'].strip('../works/')) is True

    resp_dict['copyright'].pop('rightsOf')
    resp_dict['manifestation'].pop('manifestationOfWork')
    resp_dict['copyright'].pop('@id')
    resp_dict['manifestation'].pop('@id')
    resp_dict['work'].pop('@id')
    assert resp_dict == expected
    assert resp.status_code == 200


def test_create_manifestation_missing_single_attribute(client, alice):
    payload = {
        'manifestation': {
            'name': 'The Fellowship of the Ring',
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
    # TODO: I really don't know why flask_restful includes the extra '' in the
    #       error message's response.
    assert resp.status_code == 400
    assert resp.json['message']['manifestation'] == \
        "'`datePublished` must be provided'"


def test_create_manifestation_missing_argument_in_body(client):
    payload = {
        'manifestation': {
            'name': 'The Fellowship of the Ring',
            'url': 'http://localhost/lordoftherings.txt',
            'datePublished': '29-07-1954',
        },
    }
    resp = client.post(url_for('manifestation_views.manifestationlistapi'),
                       data=json.dumps(payload),
                       headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400
    assert resp.json['message']['work'] == \
        'Missing required parameter in the JSON body'


def test_get_manifestation(client, alice, created_manifestation_resp):
    manifestation = created_manifestation_resp['manifestation']
    resp = client.get(
        url_for('manifestation_views.manifestationapi',
                entity_id=manifestation['@id']))

    assert resp.status_code == 200

    resp_manifestation = resp.json
    # The Manifestation we get back has its @id set to "" as it could be found
    # at that location
    resp_manifestation.pop('@id')
    manifestation.pop('@id')

    assert resp_manifestation == manifestation


def test_get_work(client, alice, created_manifestation_resp):
    work = created_manifestation_resp['work']
    work_id = work['@id'].split('../works/')[1]
    resp = client.get(url_for('work_views.workapi', entity_id=work_id))

    assert resp.status_code == 200

    resp_work = resp.json
    # The Work we get back has its @id set to "" as it could be found
    # at that location
    resp_work.pop('@id')
    work.pop('@id')

    assert resp_work == work
