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


def test_prepare_request():
    request = requests.Request(
        'GET', "http://google.ru",
        headers={"user-agent": "UA"},
    )

    assert curlify.to_curl(request.prepare()) == (
        "curl -X 'GET' "
        "-H 'user-agent: UA' "
        "'http://google.ru/'"
    )


def test_compressed():
    request = requests.Request(
        'GET', "http://google.ru",
        headers={"user-agent": "UA"},
    )
    assert curlify.to_curl(request.prepare(), compressed=True) == (
        "curl -X 'GET' -H 'user-agent: UA' --compressed 'http://google.ru/'"
    )

def test_verify():
    request = requests.Request(
        'GET', "http://google.ru",
        headers={"user-agent": "UA"},
    )
    assert curlify.to_curl(request.prepare(), verify=False) == (
        "curl -X 'GET' -H 'user-agent: UA' --insecure 'http://google.ru/'"
    )

def test_post_json():
    data = {'foo': 'bar'}
    url = 'https://httpbin.org/post'

    r = requests.Request('POST', url, json=data)
    assert curlify.to_curl(r.prepare()) == (
        "curl -X 'POST' -H 'Content-Length: 14' "
        "-H 'Content-Type: application/json' "
        "-d '{\"foo\": \"bar\"}' 'https://httpbin.org/post'"
    )
