# Curlify - convert Python Requests request object to cURL command

## Installation

```sh
pip install curlify
```

## Changes

### v3.0.0
   * Remove Python 2 compatibility
   * Add `pretty` parameter to enable generating a multi-line command
   * Don't add `-X` when it's unnecessary
   * Correctly send empty headers
   * Don't generate `--data` that would read a file
   * Don't sort headers, their order is deterministic on Python 3.7+

### v2.2.0
   * Fixed shell quotes. Fixed posting CSV file. Thanks to @leNEKO

### v2.1.1
   * Add `--insecure` flag if `verify` parameter is not `True`

### v2.1.0
   * Fixed body rendering when using `json` param to request function.

### v2.0.1
   * Added `compressed` parameter to `to_curl` function, if it is needed to add `--compressed` option to generated cURL command.

### v2.0
   * Skip `-d` option if request body is empty https://github.com/ofw/curlify/issues/6
   * Minor changes to header sorting

### v1.2
   * Order of headers is deterministic (thanks to @tomviner)

## Example

```py
import curlify
import requests

response = requests.get("http://google.ru")
print(curlify.to_curl(response.request))
# curl -X 'GET' -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'User-Agent: python-requests/2.18.4' 'http://www.google.ru/'

print(curlify.to_curl(response.request, compressed=True))
# curl -X 'GET' -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'User-Agent: python-requests/2.18.4' --compressed 'http://www.google.ru/'
```
