# Curlify - convert python requests request object to cURL command

## Installation
```sh
pip install curlify
```

## Changes

### v.2.0.1
    * Added `compressed` parameter to `to_curl` function, if it is needed to add `--compressed` option to generated cURL command.

### v.2.0
   * Skip `-d` option if request body is empty https://github.com/ofw/curlify/issues/6
   * Minor changes to header sorting

### v.1.2
   * Order of headers is deterministic (thanks to @tomviner)

## Example

```py
import curlify
import requests

response = requests.get("http://google.ru")
print(curlify.to_curl(response.request))
# curl -X 'GET' -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'User-Agent: python-requests/2.18.4' 'http://www.google.ru/'

print(curlify.to_curl(response.request), compressed=True)
# curl -X 'GET' -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'User-Agent: python-requests/2.18.4' --compressed 'http://www.google.ru/'
```
