# Curlify - convert python requests request object to cURL command

## Installation
```sh
pip install curlify
```

## Changes

### v.1.2
   * Order of headers is deterministic (thanks to @tomviner)

## Example

```py
import curlify
import requests

response = requests.get("http://google.ru")
print(curlify.to_curl(response.request))
# curl -X GET -H 'Connection: keep-alive' -H 'Accept-Encoding: gzip, deflate' -H 'Accept: */*' -H 'User-Agent: python-requests/2.7.0 CPython/2.7.11 Darwin/15.6.0' -d '' 'http://www.google.ru/'
```
