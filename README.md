# K-Samsök REST

K-Samsök REST is an JSON REST API built as a proxy for the K-Samsök (Swedish Open Cultural Heritage) API.

## API Documentation

There is a public instance of this API at `https://tools.wmflabs.org/ksamsok-rest`. From version 1.1.0 K-Samsök REST instances provides a `X-Powered-By` header.

### Records

Retrieve a single record from K-Samsök. An ID is usually formated as `<institution>/dataset/id`. If you want the full record as JSON-LD or as XML RDF use one of the following Accept headers: `application/json+ld`, `application/rdf+xml`.

```
/records/<id>
```

Retrieve all relations for a given record.

```
/records/<id>/relations
```

Search records by text.

```
/records?action=search&text=<string>
```

There is three optional parameters available for the search action. `start` and `hits` for pagination. `image` can be set to true to only include records with images.

Search by text limited to records with images while skiping the first five results and limit the number of responses to ten:

```
/records?action=search&text=<string>&image=true&hits=10&start=5
```

Search by bounding box:

```
/records?action=bbox&west=<int|decimal>&south=<int|decimal>&east=<int|decimal>&north=<int|decimal>
```

Note that the API can handle both SWEREF 99 and WGS84. `start` and `hits` are available for bounding searches too.

Query K-samsök with CQL:

```
/records?action=cql&query=<string>
```

### Search Hints

Returns a list of five search hints for the given string. Commonly used for auto complete features.

```
/hints/<string>
```

## Setup

```bash
git clone https://github.com/Abbe98/ksamsok-rest.git
cd ksamsok-rest
pipenv install
pipenv run python3 src/app.py
```
