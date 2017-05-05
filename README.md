# COALA IP HTTP Wrapper



## Why?



## What's the status of this?



## Can I use this in production?



## OK, how can I start experimenting?

1. Read the installation section on how to install with Docker.
1. Get familiar with the REST API provided at the end of this document.
1. Hit against a running Docker container with a HTTP client of your choice.


## Should I expose this server to the internet?

NO! Think of this library more like a shell-command. The flask server should at
least be run behind a reverse-proxy like nginx, so that its interface is NOT
exposed to the world wide web.


## Can I just have a shell-command for this?

Yes, [curl](https://curl.haxx.se/).


## Installation and Usage


### For development on Linux

1. You'll have to [install, configure and run BigchainDB as well as
MongoDB](https://bigchaindb.readthedocs.io/en/latest/quickstart.html).

2. Install and run this library using the following commands:

```
$ git clone git@github.com:coalaip/omi-mvi-1.0.git
$ virtualenv --python=python3 venv
$ source venv/bin/activate
$ cp .env_template my_new_env
$ set -a
$ source my_new_env
$ pip install -e .
$ omi-api keypair
# This will generate a new keypair you have to copy paste
# to my_new_env
$ omi-api run
```


### Run on your Linux/Mac machine directly

```
$ cp .env_template .env
$ vim .env
# configure your setup (e.g. under which port BigchainDB is running)
$ set -a
$ source .env
$ source path to your virtal env
```

### For integration (or for non-Linux development)

Use Docker :whale:.


#### Installing Docker

You'll need to have at least the base [Docker](https://docs.docker.com/engine/installation/)
and [Docker Compose](https://docs.docker.com/compose/install/) installed, but
on some platforms (i.e. OSX and Windows), [Docker Machine](https://docs.docker.com/machine/install-machine/).
will also be necessary. As a quick primer, it may be interesting to go through
the guide to [run BigchainDB via Docker](http://bigchaindb-examples.readthedocs.io/en/latest/install.html#the-docker-way),
but we've already set up everything for you in this repo.

If you already have Docker installed, just make sure you have a recent version:

```bash
$ docker --version
Docker version 1.11.1, build 5604cbe

$ docker-compose --version
docker-compose version 1.7.0, build 0d7bf73
```

#### Running with Docker

Using the provided [docker-compose.yml](./docker-compose.yml), you can install
and start RethinkDB, BigchainDB, and the COALA IP HTTP server with just a
few commands.

First, copy the default environment settings and build the Docker containers:

```bash
$ cp .env_template .env
$ docker-compose build
```

And then start the services:

```bash
# In one terminal
# Note that BigchainDB must be started after RethinkDB has begun accepting connections (may take a few seconds)
$ docker-compose up -d rethinkdb
$ docker-compose up bigchaindb

# In another terminal
$ docker-compose up api
```

By default, the COALA IP HTTP server will now be available through
`http://localhost:3000/api/v1/`, along with the BigchainDB API
(`http://localhost:32768/api/v1/`) and the RethinkDB admin panel
(`http://localhost:58585`).

**Note**: If you are running Docker through Docker Machine, the services will
only be available through the hostname of your Docker Machine instance. Use
`docker-machine ip <machine-name>` to get this hostname, and use it to replace
the `localhost` part of the above URLs.

### Settings

The API server can be configured with a number of environment variables [see
.env_template](./.env_template).


## Quick Guide

Let's assume you have an artwork you'd like to loan to someone else. These are
the steps you'll need to follow in order to register the work and any
transactions relating to the work via COALA IP.


1.
2.
3.


## REST API


### Register a Composition

POST /v1/compositions

```
Request
Headers
Content-Type: application/json

Body
{
    "title": "Crystallize",
    "iswc": "US-TEY-09-00057",
    "composers": [
        {
            "name": "Lindsey Stirling",
            "ipi": "I-000000229-7",
            "isni": "0000 0004 0314 2012",
            "split": 1
        }
    ],
    "songwriters": [
        {
            "name": "Lindsey Stirling",
            "ipi": "I-000000229-7",
            "isni": "0000 0004 0314 2012",
            "split": 1
        }
    ],
    "publishers": [
        {
            "name": "Digital Empire",
            "split": 1
        }
    ]
}

Response

201 Created

The composition was successfully registered.
```


### Register a Recording

POST /v1/recordings

```
Request
Headers
Content-Type: application/json

Body
{
    "title": "Crystallize",
    "isrc": "US-TEY-09-00057",
    "labels": [
        {
            "id": "string",
            "name": "string"
        }
    ],
    "artists": [
        {
            "name": "Lindsey Stirling",
            "isni": "0000 0004 0314 2012"
        }
    ],
    "released": "01/01/1970",
    "duration": "00:02:16",
    "versionTitle": "Hello, world!",
    "albumTitle": "Hello, world!"
}


Response

201 Created

The recording was successfully registered.
```


### Register a Manifestation

In order to register the manifestation on BigchainDB as transactions on a
specific copyright holder's name, the copyright holder's `publicKey` and
`privateKey` must be provided here.

Note that the attributes shown for `manifestation` and `work` can be much more
diverse; for this, see their [COALA IP models definition](https://github.com/COALAIP/specs/tree/master/data-structure#rrm-creation).

```
POST /api/v1/manifestations/
HEADERS {"Content-Type": "application/json"}

PAYLOAD:
{
    "manifestation": {
        "name": "The Fellowship of the Ring",
        "datePublished": "29-07-1954",
        "url": "<URI pointing to a media blob>"
    },
    "copyrightHolder": {
        "publicKey": "<base58 string>",
        "privateKey": "<base58 string>"
    },
    "work": {
        "name": "The Lord of the Rings Triology",
        "author": "J. R. R. Tolkien"
    }
}


RETURNS:
{
    "work": {
        "@id": "<Relative URI with the ID of the entity on BigchainDB>",
        "@type": "AbstractWork",
        "name": "The Lord of the Rings Trilogy",
        "author": "J. R. R. Tolkien"
    },
    "manifestation": {
        "@id": "<Relative URI with the ID of the entity on BigchainDB>",
        "@type": "CreativeWork"
        "name": "The Fellowship of the Ring",
        "manifestationOfWork": "<URI pointing to the Work's transaction ../<txid>",
        "datePublished": "29-07-1954",
        "url": "<URI pointing to a media blob>"
    },
    "copyright": {
        "@id": "<Relative URI with the ID of the entity on BigchainDB>",
        "@type": "Copyright"
        "rightsOf": "<Relative URI pointing to the Manifestation ../<txid>"
    }
}
```

#### What are the returned `@id`s?

The returned `@id`s denote the persisted ID of the entities on BigchainDB as a
relative URI to the current document base (i.e. the route URL, or
`/manifestations` in this case). For now, these point to the `CREATE`
transaction for the entity; in the future, they will be changing to be an asset
ID instead.

In the case of the returned Work and Copyright, their `@id`s are slightly
inconvenient to process as they live under a different base URL (`/works` and
`/rights`, respectively). You should strip away the leading paths to use just
the persisted IDs of these entities.

Note that in the future, we also plan to replace the JSON-LD linking structure
with [IPLD](https://github.com/ipld/specs).

#### Was my POST to `/manifestations/` successful?

To check if your POST was successful, try validating by doing the following:

1. Check the response of your POST request: Is the return value similar to the
   example provided above?

or

1. Try to [request for the entity with a GET request](#requesting-submitted-entities)

or

1. Open your browser and go to `http://localhost:9984/api/v1` (your locally
   running BigchainDB instance - if using the default Docker settings, use port
   `32768` instead).

1. To check if your previously created entities were included in BigchainDB,
   take the string in any of the returned `@id`s and append it to the following
   link: `http://localhost:9984/api/v1/transactions/<string goes here>`.
   BigchainDB should then answer with the transaction the entity was registered
   in (if using the default Docker settings, use port `32768` instead).

**Note**: If running on Docker and/or Docker Machine, substitute the hostnames
and ports of the above URLs with your Docker settings, as necessary (see the
[running with Docker section](#how-to-run-with-docker) for more help).


### Requesting Submitted Entities

You can retrieve any submitted entities via a GET to one of the following
endpoints with the entity's ID (usually the `@id` stripped of any relative URL
artifacts):

* `/manifestations/<manifestation_id>`: Manifestations
* `/works/<work_id>`: Works
* `/rights/<right_id>`: Copyrights and Rights
