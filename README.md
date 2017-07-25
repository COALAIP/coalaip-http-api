# OMI MVI 1.0

[Open Music Initiative (OMI)](http://open-music.org/) has developed a first cut HTTP API specification for linking composition and recordings of musical works. This spec is called the "OMI MVI 1.0 Specification", where MVI = Minimum Viable Interopability.

This repo is an implementation of OMI MVI 1.0, using [BigchainDB](https://www.bigchaindb.com) and [COALA IP](https://coalaip.org).

We thought that COALA IP + BigchainDB might be a perfect data model + storage layer to implement
the OMI MVI 1.0. We guessed right! [We only had to make little modifications to the data
models](https://github.com/COALAIP/omi-mvi-1.0/blob/master/omi_api/transformers.py#L3).

The rest of this doc contains:

- The architecture
- How to set up this server
- About the OMI MVI API we implemented
- What we didn't get to implement (yet..)

Have fun!

Yours,

Alberto and Tim at BigchainDB (the authors); and Trent at BigchainDB, George at OMI (the encouragers:)

Contact: {alberto, tim, trent}@bigchaindb.com

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
# This will generate a new keypair you can use to sign POST requests.
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

Depending on your configuration though. See your `.env` file or if you haven't
created it yet, checkout and copy our [.env_template](./.env_template).


## REST API
### Query for a Composition

`GET api/v1/compositions?name=Crystallize`

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

`POST api/v1/compositions`

```
Request
Headers
Content-Type: application/json
X-OMI-PUBLIC-KEY: your-public-key
X-OMI-PRIVATE-KEY: your-private-key

Body
{
    "title": "Crystallize",
    "iswc": "US-TEY-09-00057",
    "composers": [{
            "name": "Lindsey Stirling",
            "ipi": "I-000000229-7",
            "isni": "0000 0004 0314 2012",
            "split": 1
    }],
    "songwriters": [{
            "name": "Lindsey Stirling",
            "ipi": "I-000000229-7",
            "isni": "0000 0004 0314 2012",
            "split": 1
    }],
    "publishers": [{
            "name": "Digital Empire",
            "split": 1
    }]
}

Response

201 Created

The composition was successfully registered.
```

The server will log the transaction id which was used to store the composition
in BigchainDB. You can check if how it was persisted by going to:
http://localhost:9984/api/v1/transactions/<id>


### Query for a Recording

`GET api/v1/recordings?name=Crystallize{&isrc=US-TEY-09-00057}`

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

`POST api/v1/recordings`

```
Request
Headers
Content-Type: application/json
X-OMI-PUBLIC-KEY: your-public-key
X-OMI-PRIVATE-KEY: your-private-key

Body
{
    "title": "Crystallize",
    "isrc": "US-TEY-09-00057",
    "labels": [{
            "id": "string",
            "name": "string"
    }],
    "artists": [{
            "name": "Lindsey Stirling",
            "isni": "0000 0004 0314 2012"
    }],
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
http://localhost:9984/api/v1/transactions/your-transaction-id


## What we didn't implement

This list is likely not be complete:

- `!=` query paramter
- `X-OMI-VERSION`
- Wildcard search indexes. We just created a bunch of random indexes, this
however can easily be changed. MongoDB has really great wildcard text indexing.
- A solid check if the BigchainDB blocks we're querying against are `VALID`.
It's more work (too much for a hackathon), but easily doable.
- Pagination and sorting on all endpoints
- Generally we implemented only happy paths, this also means:
    - No tests (lol)
    - Almost no error scenarios
    - etc.
- Might be that you're even able to query for nested fields :D BTW our QUERIES
ARE NOT SANITIZED DON'T HACK PLS :D
- The status endpoints
- We added two headers for signing BigchainDB transactions: `X-OMI-PUBLIC-KEY`
and `X-OMI-PRIVATE-KEY`


## Signing BigchainDB transactions

Currently BigchainDB's transactions are created and signed on the server. We
acknowledge that this is a showstopping practise. Implementing a full-on secure
client-server transaction signing protocol wasn't possible in the timeframe we
had. We plan to make it happen though! If you have thoughts or ideas on this,
please feel free to comment in [this
ticket](https://github.com/COALAIP/omi-mvi-1.0/issues/25)


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


### Can I have this for Ethereum/Bitcoin/...?

Yes! COALA IP is designed to be ledger agnostic. In fact, only a few functions
would need to be implemented to make the registration work on e.g. Ethereum.
Specifically [these methods](https://github.com/bigchaindb/pycoalaip-bigchaindb/blob/master/coalaip_bigchaindb/plugin.py#L23). Should be fairly
simple! Dunno about querying on those ledgers though. Please reach out to
tim@bigchaindb.com if you're planning to do this. The COALA IP group would
be more than happy to hold your hand in implementing!


### I get this weird log message when registering a Recording. Is everything OK?

You're probably talking about:

```
'manifestationOfWork' must be given as a string in the 'data' parameter of a
'Model'. Given 'None'
```

If so, everything is alright! We didn't have a lot of time building this, so
we had take a few short cuts. This error message was one of them. TimDaub
pledged to fix this in pycoalaip. Call me out on it :D!
