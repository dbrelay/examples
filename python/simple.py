from dbrelay import DBRelay # Main class to be used directly or subclassed
from pprint  import pprint  # For pretty-printing the results

import os, pwd, socket
db = DBRelay( "Simple example instance", "http://dbrelay.net:1433/sql", {
    'sql_server'      : 'sqlserver',
    'sql_database'    : 'AdventureWorks',
    'sql_user'        : 'demo',
    'sql_password'    : 'demo',
    'connection_name' : pwd.getpwuid(os.getuid())[0] + '@' + socket.gethostbyaddr(socket.gethostname())[0]
})

response = db.sql("""
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
""")

pprint( response )