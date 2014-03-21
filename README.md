LR-Lite
=======


To get data from a Learning Registry Lite node, you issue an HTTP GET request to the /v1/lr endpoint

``` 
curl http://domain/v1/lr
```

This will return JSON 


``` JSON
{
    "response":[...]
}
```

This request can be augmented with the following query string paramaters

paramater | type | effect
----------|-------|--------
include_docs | boolean | true: entire envelope false: only IDs
from | ISO8601 Timestamp | Earliest node_timestamp returned
until | ISO8601 Timestamp | Latest node_timestamp returned
page | Integer | results page, starting at 0

To submit data submit a PUT request to the /v1/lr endpoint 

```
curl -XPOST http://domain/v1/lr -H "Content-Type: applicaiton/json" -d @envelope.json -u username
```


Submission uses HTTP Basic Auth and requires a user account to be able to publish

You can signup for an account on the node by going to 

```
http://domain/signup
```
and filling in the form for an account.
