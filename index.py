#! /usr/bin/env python

import logging
import urlparse
import json
import os
logging.basicConfig(filename='/var/www/my.hackerspace.com/spaceapi.log',level=logging.DEBUG)

def spaceapi_app(environ, start_response):

    Router.set_environ(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    return {
        'sensor' : SensorController.execute #Other possible commands in this dict
    }.get(Router.get_controller(), StatusController.execute)()



class SensorController:

    key = '86f7896f97asdf89u0a9s7d7fdasgsda88af'
    @classmethod
    def execute(cls):
        #return Router.get_action()
        return {
            'set' : cls.setAction
        }.get(Router.get_action(), cls.noneAction)()

    @classmethod
    def noneAction(cls):
        return ''
    @classmethod
    def setAction(cls):
        logging.debug(Router.get_post('key')[0])
        if any(p == cls.key for p in Router.get_post('key')):
            try:
                js = json.loads(Router.get_post('sensors')[0]) #hack
            except:
                logging.warn(Router.get_post('sensors'))
                return 'Invalid JSON'
            for sensor in js:
                file = open(Router.environ['CONTEXT_DOCUMENT_ROOT']+os.sep+'data'+os.sep+sensor,'w')
                file.write(json.dumps(js[sensor])) #convert to a neat format to read back later
                file.close()
            return 'SensorController::set'
        else:
            return 'Not allowed'


class StatusController:

    @classmethod
    def execute(cls):
        return {
            'json' : cls.jsonAction
        }.get(Router.get_action(), cls.htmlAction)()

    @classmethod
    def jsonAction(cls):
        return 'StatusController::json'

    @classmethod
    def htmlAction(cls):
        return 'StatusController::html'

class Router:

    environ = None

    @classmethod
    def set_environ(cls, environ):
        cls.environ = environ

    @classmethod
    def get_segment(cls, index):
        request_uri = cls.environ['PATH_INFO']
        segments = request_uri.lower().strip('/').split('/')
        if len(segments)-1 >= index:
            return segments[index]
        else:
            return ''

    @classmethod
    def get_post(cls, value):
        postdata = urlparse.parse_qs(cls.environ['QUERY_STRING']) #lowercase this
        logging.debug(postdata['key'][0])
        if value in postdata:
            return postdata[value]
        else:
            return ''

    @classmethod
    def get_controller(cls):
        return cls.get_segment(0)

    @classmethod
    def get_action(cls):
        return cls.get_segment(1)


class Output():

    @staticmethod
    def html():
        return ''

    @staticmethod
    def json():
        return ''


######################################################################

## use this line to use the script with mod_wsgi or
## other wsgi-compliant web servers/modules
application = spaceapi_app

## use the following lines to run the script as built-in web server
#from wsgiref.simple_server import make_server
#httpd = make_server('', 8052, spaceapi_app)
#print("Serving on port 8052...")
#httpd.serve_forever()

######################################################################

# http://docs.python.org/3.3/library/wsgiref.html
# https://wiki.archlinux.org/index.php/Mod_wsgi
# https://code.google.com/p/modwsgi/wiki/DebuggingTechniques
