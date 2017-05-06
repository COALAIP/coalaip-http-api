# OMI MVI 1.0

> An implementation of the OMI MVI 1.0 specification implemented with
> BigchainDB and COALA IP.

### Wat?

We though using COALA IP and BigchainDB as respecivetly data model and storage
layer would be perfect to implement the OMI MVI 1.0. In fact, our hypothesis
turned out to be right. [We only had to make little modifications to the data
models](https://github.com/COALAIP/omi-mvi-1.0/blob/master/omi_api/transformers.py#L3).
To learn more about:
    - the architecture
    - how to setup this server
    - about the OMI MVI API we implemented
    - what we didn't get to implement

read further!

Have fun!

- the authors, Alberto, Tim and Trent from @bigchaindb.com (this is also how
  you can contact us :))

## Architecture
![img_20170505_171428](https://cloud.githubusercontent.com/assets/2758453/25767726/42b21a66-31fc-11e7-8816-5e00f0bd178b.jpg)


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

then do:

```
$ cp .env_template .env
$ vim .env
# configure your setup (e.g. under which port BigchainDB is running)
$ set -a
$ source .env
$ source path to your virtal env
```

### Servers

- OMI API: http://localhost:3000/api/v1
- BigchainDB: http://localhost:9984/api/v1
- MongoDB: localhost:27017

Depending on your configuration though. See your `.env` file.


### Settings

The API server can be configured with a number of environment variables [see
.env_template](./.env_template).


## REST API
### Query for a Composition

GET api/v1/compositions?name=Crystallize

NOTE: You can use all sorts of query strings and mix them up.

```
Request
Headers
Content-Type: application/json

Response

Body

[{
    "composers": [{
        "ipi": "I-000000229-7",
            "isni": "0000 0004 0314 2012",
            "name": "Lindsey Stirling",
            "split": 1
        }],
        "publishers": [{
            "name": "Digital Empire",
            "split": 1
        }],
        "songwriters": [{
            "ipi": "I-000000229-7",
            "isni": "0000 0004 0314 2012",
            "name": "Lindsey Stirling",
            "split": 1
        }],
        "title": "Crystallize"
}]

200 OK
```


### Register a Composition

POST api/v1/compositions

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

The server will log the transaction id which was used to store the composition
in BigchainDB. You can check if how it was persisted by going to:
http://localhost:9984/api/v1/transactions/<id>


### Query for a Recording

GET api/v1/recordings?name=Crystallize{&isrc=US-TEY-09-00057}

NOTE: You can use all sorts of query strings and mix them up.

```
Request
Headers
Content-Type: application/json

Response

Body

[{
    "artists": [{
        "isni": "0000 0004 0314 2012",
        "name": "Lindsey Stirling"
    }],
    "isrc": "US-TEY-09-00057",
    "labels": [{
        "id": "string",
        "name": "string"
    }],
    "title": "Crystallize"
}]

200 OK
```


### Register a Recording

POST api/v1/recordings

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

The server will log the transaction id which was used to store the recording
in BigchainDB. You can check if how it was persisted by going to:
http://localhost:9984/api/v1/transactions/<id>


## What we didn't implement

This list is likely not be complete:

- `!=` query paramter
- `X-OMI-VERSION`
- Wildcard search indexes. We just created a bunch of random indexes, this
however can easily be changed. MongoDB has really great wildcard text indexing.
- A solid check if the BigchainDB blocks we're querying against are `VALID`.
It's more work (too much for a hackathon), but easily doable.
- Pagination and sorting on all endpoints
- Generally we only implemented only happy paths, this also means:
    - No tests (lol)
    - Almost no error scenarios
    - etc.
- Might be that you're even able to query for nested fields :D BTW our QUERIES
ARE NOT SANITIZED DON'T HACK PLS :D


## FAQ

### DOCKER DOESN'T WORK AT THIS POINT??!

[There is a ticket. Pls fix.](https://github.com/COALAIP/omi-mvi-1.0/issues/15)


### Should I expose this server to the internet?

The OMI API isn't concerned with Authentication at this point. So weren't we
when hacking this in 2 days. Don't store mission-critical data on this
application or run it in production. It's just a MVP.


### Can I just have a shell-command for this?

Yes, [curl](https://curl.haxx.se/).


### Why does Github say this repository is forked?

We implemented coalaip-http-api already. It's extremely similar to this repo.
To move fast, we just forked and refactored.
