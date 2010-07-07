import urllib, urllib2
from pprint import pprint

try:
    import simplejson as json
except ImportError:
    import json

response = urllib2.urlopen(
  url  = "http://dbrelay.net:1433/sql",
  data = urllib.urlencode({
    'connection_name' : 'dbrelay@oscon',
    'sql_server'      : 'sqlserver',
    'sql_database'    : 'AdventureWorks',
    'sql_user'        : 'demo',
    'sql_password'    : 'demo',
    'http_keepalive'  : 0,
    'sql' : 'select count(*) as employees from HumanResources.vEmployee'
}))
parsed = json.load( response )

pprint( parsed )