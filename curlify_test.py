# coding: utf-8

import curlify
import requests


def test_empty_data():
    r = requests.post(
        "http://google.ru",
        headers={"user-agent": "mytest"},
    )
    assert curlify.to_curl(r.request) == (
        "curl -X 'POST' "
        "-H 'Accept: */*' "
        "-H 'Accept-Encoding: gzip, deflate' "
        "-H 'Connection: keep-alive' "
        "-H 'Content-Length: 0' "
        "-H 'user-agent: mytest' "
        "'http://google.ru/'"
    )


def test_ok():
    r = requests.get(
        "http://google.ru",
        data={"a": "b"},
        cookies={"foo": "bar"},
        headers={"user-agent": "mytest"},
    )
    assert curlify.to_curl(r.request) == (
        "curl -X 'GET' "
        "-H 'Accept: */*' "
        "-H 'Accept-Encoding: gzip, deflate' "
        "-H 'Connection: keep-alive' "
        "-H 'Content-Length: 3' "
        "-H 'Content-Type: application/x-www-form-urlencoded' "
        "-H 'Cookie: foo=bar' "
        "-H 'user-agent: mytest' "
        "-d 'a=b' 'http://google.ru/'"
    )
