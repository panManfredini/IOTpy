import os
from twisted.web import server
from twisted.internet import reactor
from twisted.application.internet import TCPServer
from twisted.web.resource import Resource
from twisted.web.static import File

from prometheus_client.twisted import MetricsResource
from .loadDevices import loadDevices
from .routes import NodeValues, ShutDown, WriteValue
from .splashscreen import printSplashScreen

printSplashScreen()
loadDevices()
dir_path = os.path.abspath(os.path.dirname(__file__))

root = Resource()

variablesRoute = NodeValues()
variablesRoute.putChild(b"", NodeValues())
root.putChild(b"variables", variablesRoute)
root.putChild(b"restart", ShutDown())
root.putChild(b'metrics', MetricsResource())
root.putChild(b'write',   WriteValue())

root.putChild(b"", File(dir_path + "/html/index.html" ) )
root.putChild(b"main.js",  File( dir_path + "/html/main.js" ) )
root.putChild(b"main.css", File( dir_path + "/html/main.css" ))

def run():
    site = server.Site(root)
    reactor.listenTCP(8085, site)
    print("Listening on 8085")
    reactor.run()
