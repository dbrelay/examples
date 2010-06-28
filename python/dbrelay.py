import urllib, urllib2
import sys
import logging
import pprint
import copy

try:
   import simplejson as json
except ImportError:
   # v2.6 and 3.x
   import json

__doc__ = """
The drelay module provides wrapper classes to access MS SQL Servers via DB
Relay instances. Instances of the DBRelayRoundRobin class try a random
server from the supplied list. If a query to the tried server fails, the
next server in the randomized list attempted. If the list is exausted, then
the call raises an exception.
"""

class DBRelay(object):
    """
    Instances of DBRelay use a single DB Relay server url and either return
    result or raise an exception. The DBRelay class can be used directly.
    However, in all but simplest cases it is better to extend it with domain
    specific methods.
    """

    logger = logging.getLogger("dbrelay")
    logger.addHandler(logging.StreamHandler(sys.stderr))

    def __init__(self, tag, server, params, debug = False):
        """
        DBRelay constructor takes the following parameters:
        
        tag    - A string, which will be used to identify the instance in
                 log files and exceptions.
        
        server - Target DB Relay server url, e.g. "http://local:1433/sql"
                 May be provided as a function returning a server url
                 on each call.
        
        params - DB Relay connection configuration dictionary. See DB
                 Relay documentation for specifics. The only variation is
                 that 'connection_name' and 'query_tag' may be provided
                 as functions returning desired values on each call.
        
        debug  - A boolean flag. If True, sets the logger level to DEBUG.
                 Optional, defaults to False.
        """
        self.tag = tag
        self.params = params
        self.server = server

        if sys.version_info[:2] < (2, 6):
            self.params['http_keepalive'] = '0'

        if debug:
            self.params['flags']='echosql'
            self.logger.setLevel(logging.DEBUG)

    def sql(self, query ):

        conn = copy.copy( self.params )
        conn['sql'] = query
        
        if callable( self.server ):
            server = self.server()
        else:
            server = self.server

        try:
            if callable( conn['connection_name'] ):
                conn['connection_name'] = conn['connection_name']()
        except KeyError:
            pass

        try:
            if callable( conn['query_tag'] ):
                conn['query_tag'] = conn['query_tag']()
        except KeyError:
            pass

        self.logger.debug("Calling the query %s at %s with parameters:\n%s" % (self.tag, server, pprint.pformat(conn)))

        try:
            response = urllib2.urlopen( url=server, data=urllib.urlencode(conn) )
        except Exception, msg:
            raise( RuntimeError( "Failed to use the DB Relay server %s at %s. The error message was:\n%s" % (self.tag, self.server, msg)) )

        if not response:
            raise( RuntimeError("No response from server %s to the following (%s) request:\n%s" % (server, self.tag, pprint.pformat(conn))) )

        try:
            rsp = json.load( response )
        except Exception, msg:
            raise( RuntimeError("DB Relay server error at %s on %s:\n%s\non the response text:\n%s" % (self.tag, server, msg, response.read())) )

        if rsp['log'].has_key('error'):
            err = rsp['log']['error']
            raise( RuntimeError("DB Relay query error at %s on %s:\n%s" % (self.tag, server, pprint.pformat(rsp))) )

        return rsp

    def select(self, query):
        rsp = self.sql(query)
        return rsp['data'][-1]['rows']
