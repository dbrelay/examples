import urllib, urllib2
from pprint import pprint
try:
    import simplejson as json
except ImportError:
    # v2.6 and 3.x
    import json

params = {
    'sql_server'      : 'sqlserver',
    'sql_database'    : 'AdventureWorks',
    'sql_user'        : 'demo',
    'sql_password'    : 'demo',
    'connection_name' : 'bare test',
    'http_keepalive'  : 0,
    'sql'             : """
        select @@version as ver

        select
            BusinessEntityID,
            FirstName + ' ' +
                coalesce( MiddleName + ' ', '' ) +
        	    LastName +
                coalesce( ' ' + Suffix, '' ) as Name,
            City,
            StateProvinceName,
    	    PostalCode
        from HumanResources.vEmployee
        where CountryRegionName = 'Canada'
    """
}

response = urllib2.urlopen( url="http://dbrelay.net:1433/sql", data=urllib.urlencode(params) )
parsed = json.load( response )

pprint( parsed )
