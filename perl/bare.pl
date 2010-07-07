# Early in your program:
  
use LWP 5.64; 
use JSON;

my $browser = LWP::UserAgent->new;
my $json = new JSON;
 
my $url = 'http://dbrelay.com:1433/sql';
my $resp = $browser->post( $url, [
    'sql_server' => 'sqlserver',
    'sql_database' => 'AdventureWorks',
    'sql_user' => 'demo',
    'sql_password' => 'demo',
    'connection_name' => 'bare test',
    'http_keepalive' => 0,
    'sql' => "
        select \@\@version as ver

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
        where CountryRegionName = 'Canada'"
]);

die "Can't get $url -- ", $resp->status_line unless $resp->is_success;

print $resp->content;

print to_json($json->decode($resp->content), {pretty=>1});
