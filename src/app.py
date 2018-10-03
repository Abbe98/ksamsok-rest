import configparser
import sys

import requests

from ksamsok import KSamsok

from flask import Flask, request, Response
from flask_restful import Api, Resource, abort

# http://www.ianbicking.org/illusive-setdefaultencoding.html
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding('utf-8')

app = Flask(__name__)
api = Api(app)
soch = KSamsok('test')

# CORS headers
@app.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
    resp.headers.add('X-Powered-By', 'K-Samsök REST Version 1.1.0')
    return resp

class Record(Resource):
    def get(self, uri):
        if 'application/json+ld' in request.headers.get('Accept'):
            url = soch.formatUri(uri, 'jsonldurl')
            if not url:
                return abort(404, message='Record {} doesn\'t exist'.format(uri))

            r = requests.get(url)
            if r.status_code is not 200:
                return abort(404, message='Record {} doesn\'t exist'.format(uri))

            resp = Response(r.text)
            resp.headers.add('Link', '<http://json-ld.org/contexts/person.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"')
            return resp

        elif 'application/rdf+xml' in request.headers.get('Accept'):
            url = soch.formatUri(uri, 'rawurl')
            if not url:
                return abort(404, message='Record {} doesn\'t exist'.format(uri))

            r = requests.get(url)
            if r.status_code is not 200:
                return abort(404, message='Record {} doesn\'t exist'.format(uri))

            resp = Response(r.text)
            resp.headers.add('Content-Type', 'application/rdf+xml')
            return resp

        else:
            record = soch.getObject(uri)

            if record:
                return record

            return abort(404, message='Record {} doesn\'t exist'.format(uri))

api.add_resource(Record, '/records/<path:uri>')

class RecordRelations(Resource):
    def get(self, uri):
        relations = soch.getRelations(uri)

        if relations:
            return relations

        return abort(404, message='Record {} doesn\'t exist'.format(uri))

api.add_resource(RecordRelations, '/records/<path:uri>/relations')

class Records(Resource):
    def get(self):
        args = request.args

        if 'action' in args and args['action'] == 'bbox':

            if all(i in args for i in ['west', 'south', 'east', 'north']):
                start = args['start'] if 'start' in args else 0
                hits = args['hits'] if 'hits' in args else 50

                return soch.geoSearch(args['west'], args['south'], args['east'], args['north'], start, hits)

            return abort(400, message='One or multiple parameters are missing.')

        if 'action' in args and args['action'] == 'search':
            if 'text' in args:
                start = args['start'] if 'start' in args else 0
                hits = args['hits'] if 'hits' in args else 50
                images = True if 'image' in args else False

                return soch.search(request.args['text'], start, hits, images)

            return abort(400, message='The text parameter is missing.')

        return abort(400, message='The action parameter is missing or has a invalid value.')

api.add_resource(Records, '/records')

class Hints(Resource):
    def get(self, text):
        return soch.getHints(text)

api.add_resource(Hints, '/hints/<string:text>')

if __name__ == '__main__':
    app.run()
