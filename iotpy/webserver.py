#from twisted.application.internet import TCPServer
#from twisted.application.service import Application
#from twisted.web.resource import Resource
#from twisted.web.server import Site
import os
from twisted.web import server
from twisted.internet import reactor
from twisted.application.internet import TCPServer
from twisted.web.resource import Resource
from twisted.web.static import File

from prometheus_client.twisted import MetricsResource
from threading import Thread
import time
import json
from . import loadDevices
from .Device import listOfDevices


class Index(Resource):
    isLeaf = True
    def render_GET(self, request):
        return b'<html><h1>IOTpy</h1></html>'


class NodeValues(Resource):
    isLeaf = False
    def render_GET(self, request):
        request.responseHeaders.addRawHeader(b"Content-Type", b"application/json")
        overall_dict_of_values = dict()
        for x in listOfDevices:
            dev_dict = x.getAllVariablesValues()
            if bool(dev_dict):
                overall_dict_of_values = {**overall_dict_of_values, **dev_dict}
        return json.dumps(overall_dict_of_values).encode("utf8")


class WriteValue(Resource):
    isLeaf = False
    def render_POST(self, request):
        request.responseHeaders.addRawHeader(b"Content-Type", b"application/json")
        content_type = request.responseHeaders.getRawHeaders(b"Content-Type")
        if b"application/json" in content_type:
            obj = dict()
            try:
                obj = json.load(request.content)
            except:
                return self.returnFail(request, 400)

            if "name" not in obj or "value" not in obj:
                return self.returnFail(request, 400)

            success = False
            var_found = False
            for device in listOfDevices:
                if device.hasVar(obj["name"]):
                    var_found = True
                    success = device.write(obj["name"], obj["value"])
                    break

            if success and var_found:
                # return ok
                response_obj = self.buildReturnObject(200)
                response_obj = {**response_obj, **obj}
                return json.dumps(response_obj).encode("utf8")

            elif var_found :
                # return bad value
                return self.returnFail(request,400)
            else :
                # return not found
                return self.returnFail(request, 404)

        return self.returnFail(request,400)


    def buildReturnObject(self, code):
        obj = dict()
        obj["success"] = (code == 200)
        if code == 200:
            obj["error"] = ""
        elif code == 404 :
            obj["error"] = "Not Found"
        elif code == 400:
            obj["error"] = "Bad Request"
        else:
            obj["error"] = "Uknown Error"
        return obj

    def returnFail(self, request, code):
        request.setResponseCode(code)
        return json.dumps(self.buildReturnObject(code)).encode("utf8")




class ShutDown(Resource):
    isLeaf = False

    def render_GET(self, request):
        for device in listOfDevices:
            device.stop()
        t = Thread(target=shutdown)
        t.start()
        return b"""
        <h1>Shutting down... </h1> <p>Restart will only happen if you configure it as deamon.</p>
        <script>
            setTimeout(()=>{ window.location.pathname = '/'; }, 3000);
        </script>
        """



root = Resource()
#root.putChild(b"", Index())
variablesRoute = NodeValues()
variablesRoute.putChild(b"", NodeValues())
root.putChild(b"variables", variablesRoute)
root.putChild(b"restart", ShutDown())
root.putChild(b'metrics', MetricsResource())
root.putChild(b'write', WriteValue())
file_path = os.path.abspath(os.path.dirname(__file__)) + "/html/index.html"
print(file_path)
root.putChild(b"",File(file_path))

#application = Application("My Web Service")
#TCPServer(8880, Site(root)).setServiceParent(application)


def shutdown():
    time.sleep(0.3)
    reactor.stop()

def run():
    site = server.Site(root)
    reactor.listenTCP(8085, site)
    print("Listening on 8085")
    reactor.run()


