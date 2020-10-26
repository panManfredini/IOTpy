from twisted.web import server
from twisted.internet import reactor
from twisted.web.resource import Resource
from prometheus_client.twisted import MetricsResource
import json
#import loadDevices

class Index(Resource):
    isLeaf = True

    def render_GET(self, request):
        return b'<html><h1>IOTpy</h1></html>'


class NodeValues(Resource):
    isLeaf = False

    def render_GET(self, request):
        request.responseHeaders.addRawHeader(b"content-type", b"application/json")
        x = dict()
        x["ciao"] = 89
        x["boo"] = "boo"
        return json.dumps(x).encode("utf8")


class ShutDown(Resource):
    isLeaf = False

    def render_GET(self, request):
        reactor.stop()
        return b'Shutting down'


root = Resource()
root.putChild(b"", Index())
variablesRoute = NodeValues()
variablesRoute.putChild(b"", NodeValues())
root.putChild(b"variables", variablesRoute)
root.putChild(b"restart", ShutDown())
root.putChild(b'metrics', MetricsResource())

site = server.Site(root)
reactor.listenTCP(8085, site)
print("Listening on 8085")
reactor.run()
