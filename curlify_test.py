# coding: utf-8

import requests

import curlify


def test_ok():
    response = requests.get(
        "http://google.ru",
        data={"a": "b"},
        cookies={"foo": "bar"},
        headers={"user-agent": "mytest"}
    )
    assert curlify.to_curl(response.request) == (
        "curl -X GET "
        "-H 'Accept-Encoding: gzip, deflate' "
        "-H 'Accept: */*' "
        "-H 'Connection: keep-alive' "
        "-H 'Content-Length: 3' "
        "-H 'Content-Type: application/x-www-form-urlencoded' "
        "-H 'Cookie: foo=bar' "
        "-H 'user-agent: mytest' "
        "-d 'a=b' 'http://google.ru/'"
        " --compressed"
    )


def test_prepare_request():
    response = requests.Request('GET', "http://google.ru", data={"a": "b"}, cookies={"foo": "bar"},
                                headers={"user-agent": "UA"})

    assert curlify.to_curl(response.prepare()) == (
        "curl -X GET "
        "-H 'Content-Length: 3' "
        "-H 'Content-Type: application/x-www-form-urlencoded' "
        "-H 'Cookie: foo=bar' "
        "-H 'user-agent: UA' "
        "-d 'a=b' 'http://google.ru/' "
        "--compressed"
    )
