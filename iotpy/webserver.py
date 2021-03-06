import os
from twisted.web import server as svr
from twisted.application import service, internet
from twisted.web.resource import Resource
from twisted.web.static import File

from prometheus_client.twisted import MetricsResource
from .loadDevices import loadDevices
from .routes import NodeValues, ShutDown, WriteValue
from .splashscreen import printSplashScreen
from .readArgs import getDirAndPort
from .shutdown import SetShutdownHandler
from .Device import StartDevicesLoop

def build_application():
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

    prefix = os.getenv('IOTPY_PROXY_PREFIX') or None
    root_prefixed = root
    if prefix != None:
        root_prefixed = Resource()
        root_prefixed.putChild(prefix.encode(), root)

    modules_dir, PORT = getDirAndPort()
    site = svr.Site(root_prefixed)
    server = internet.TCPServer(PORT, site)
    application = service.Application('IoTpy')
    server.setServiceParent(application)
    SetShutdownHandler()
    StartDevicesLoop()

    return application