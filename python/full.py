from dbrelay import DBRelay     # Main class to be subclassed

from itertools import cycle     # A cycle function to round-robin through DB Relay instances
from os        import getpid    # Current process ID to construct a connection name
from socket    import getfqdn   # Full system name to construct a connection name
from random    import randrange # Random numbers generator to construct a connection name

class AW_Department( DBRelay ):
    name = ''

    dbrelays = cycle([
        'http://dbrelay.net:1433/sql',
        'http://dbrelay.org:1433/sql'
    ]).next

    connection_name_prefix = getfqdn() + ':' + repr(getpid())

    def connection_name(self):
        return self.connection_name_prefix + ',' + str(randrange(0,5))

    def __init__( self, department, debug = False ):
        self.name = department
        conn = {
         'sql_server'      : 'sqlserver',
         'sql_database'    : 'AdventureWorks',
         'sql_user'        : 'demo',
         'sql_password'    : 'demo',
         'connection_name' : self.connection_name
        }
        DBRelay.__init__( self, "SystemConfig", self.dbrelays, conn, debug )

    def employee_list(self):
        return self.select("""
            select BusinessEntityID
            from HumanResources.vEmployeeDepartmentHistory
            where EndDate is null
              and Department = '%s'
        """ % (self.name)
        )

    def employee_count(self):
        return self.select("""
            select count(BusinessEntityID) as num_employees
            from HumanResources.vEmployeeDepartmentHistory
            where EndDate is null
              and Department = '%s'
        """ % (self.name)
        )[0]['num_employees']

    def shift_coverage(self):
        return self.sql("""
            select Shift, count(BusinessEntityID) as Employees
            from HumanResources.vEmployeeDepartmentHistory
            where EndDate is null
              and Department = '%s'
            group by Shift
            order by Shift
        """ % (self.name)
        )['data'][0]['rows']