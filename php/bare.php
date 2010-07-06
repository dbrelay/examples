<?php

require_once 'HTTP/Client.php';
require_once 'json_format.php';

$data = array( 
    'sql_server' => 'sqlserver',
    'sql_database' => 'AdventureWorks',
    'sql_user' => 'demo',
    'sql_password' => 'demo',
    'connection_name' => 'bare test',
    'http_keepalive' => 0,
    'sql' => "select @@version as ver

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
);
$sUri = "http://dbrelay.com:1433/sql";

$client =& new HTTP_Client(); 
$code = $client->post($sUri, $data); 
$response = $client->currentResponse();

#echo $response['body']; 

$json = json_decode($response['body']);
print json_format($response['body']);

?>
