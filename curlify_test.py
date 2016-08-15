# coding: utf-8

import curlify
import requests

def test_ok():
    r = requests.get("http://google.ru", data={"a": "b"}, cookies={"foo": "bar"}, headers={"user-agent": "mytest"})
    assert curlify.to_curl(r.request) == (
        "curl -X GET -H 'Content-Length: 3' -H 'Accept-Encoding: gzip, deflate' "
        "-H 'Accept: */*' -H 'user-agent: mytest' -H 'Connection: keep-alive' "
        "-H 'Cookie: foo=bar' -H 'Content-Type: application/x-www-form-urlencoded' "
        "-d 'a=b' 'http://google.ru/'"
    )
