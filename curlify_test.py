# coding: utf-8

import curlify
import requests


def test_ok():
    r = requests.get(
        "http://google.ru",
        data={"a": "b"},
        cookies={"foo": "bar"},
        headers={"user-agent": "mytest"},
    )
    assert curlify.to_curl(r.request) == (
        "curl -X GET "
        "-H 'Accept-Encoding: gzip, deflate' "
        "-H 'Accept: */*' "
        "-H 'Connection: keep-alive' "
        "-H 'Content-Length: 3' "
        "-H 'Content-Type: application/x-www-form-urlencoded' "
        "-H 'Cookie: foo=bar' "
        "-H 'user-agent: mytest' "
        "-d 'a=b' 'http://google.ru/'"
    )
