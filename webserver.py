from twisted.web import server
from twisted.internet import reactor
from twisted.web.resource import Resource
from prometheus_client.twisted import MetricsResource
import json

class Simple(Resource):
    isLeaf = True 
    def render_GET(self, request):
        return b'<html>Hello, world!</html>'

class NodeValues(Resource):
    isLeaf = False 
    def render_GET(self, request):
        request.responseHeaders.addRawHeader(b"content-type", b"application/json")
        x = dict()
        x["ciao"] = 89
        x["booo"] = "booo"
        return json.dumps(x).encode("utf8")

class ShutDown(Resource):
    isLeaf = False 
    def render_GET(self, request):
        reactor.stop()
        return b'Shutting down'


root = Resource()
root.putChild(b"", Simple())
variablesRoute = NodeValues()
variablesRoute.putChild(b"", NodeValues())
root.putChild(b"variables", variablesRoute)
root.putChild(b"restart", ShutDown())
root.putChild(b'metrics', MetricsResource())

site = server.Site(root)
reactor.listenTCP(8085, site)
reactor.run()
