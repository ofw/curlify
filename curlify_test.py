# coding: utf-8
import re

import requests
import responses

import curlify


@responses.activate
def test_empty_data():
    uri = 'https://httpbin.org/post'
    responses.add(
        responses.POST,
        uri,
        json={'hello': 'world'},
        status=200
    )
    response = requests.post(
        uri,
        headers={'User-agent': 'UA'},
    )

    assert curlify.to_curl(response.request) == (
        "curl -X POST"
        " -H 'Accept: */*'"
        " -H 'Accept-Encoding: gzip, deflate'"
        " -H 'Connection: keep-alive'"
        " -H 'Content-Length: 0'"
        " -H 'User-agent: UA'"
        f" {uri}"
    )


@responses.activate
def test_ok():
    url = 'https://httpbin.org/get'
    responses.add(
        responses.GET,
        url,
        json={'hello': 'world'},
        status=200
    )
    response = requests.get(
        url,
        data={"a": "b"},
        cookies={"foo": "bar"},
        headers={"User-agent": "UA"},
    )

    assert curlify.to_curl(response.request) == (
        "curl -X GET"
        " -H 'Accept: */*'"
        " -H 'Accept-Encoding: gzip, deflate'"
        " -H 'Connection: keep-alive'"
        " -H 'Content-Length: 3'"
        " -H 'Content-Type: application/x-www-form-urlencoded'"
        " -H 'Cookie: foo=bar'"
        " -H 'User-agent: UA'"
        " -d a=b"
        f" {url}"
    )


def test_prepare_request():
    url = 'https://httpbin.org/get'
    request = requests.Request(
        'GET',
        url,
        headers={"User-agent": "UA"},
    )

    assert curlify.to_curl(request.prepare()) == (
        "curl -X GET"
        " -H 'User-agent: UA'"
        f" {url}"
    )


def test_compressed():
    url = "https://httpbin.org/get"
    request = requests.Request(
        'GET',
        url,
        headers={"User-agent": "UA"}
    )

    assert curlify.to_curl(request.prepare(), compressed=True) == (
        "curl -X GET"
        " -H 'User-agent: UA'"
        " --compressed"
        f" {url}"
    )


def test_verify():
    url = 'https://httpbin.org/get'
    request = requests.Request(
        'GET',
        url,
        headers={"user-agent": "UA"},
    )

    assert curlify.to_curl(request.prepare(), verify=False) == (
        f"curl -X GET -H 'user-agent: UA' --insecure {url}"
    )


def test_post_json():
    url = 'https://httpbin.org/post'
    data = {'foo': 'bar'}
    request = requests.Request('POST', url, json=data)

    curl_cmd = curlify.to_curl(request.prepare())

    assert curl_cmd == (
        "curl -X POST -H 'Content-Length: 14' "
        "-H 'Content-Type: application/json' "
        "-d '{\"foo\": \"bar\"}' https://httpbin.org/post"
    )


def test_post_csv_file():
    request = requests.Request(
        method='POST',
        url='https://httpbin.org/post',
        files={'file': open('data/data.csv', 'r')},
        headers={'User-agent': 'UA'}
    )

    curl_cmd = curlify.to_curl(request.prepare())
    boundary = get_boundary(curl_cmd)

    assert curl_cmd == (
        "curl -X POST -H 'Content-Length: 519'"
        f" -H 'Content-Type: multipart/form-data; boundary={boundary}'"
        " -H 'User-agent: UA'"
        f' -d \'--{boundary}\r\nContent-Disposition: form-data;'
        ' name="file"; filename="data.csv"\r\n\r\n'
        '"Id";"Title";"Content"\n'
        '1;"Simple Test";"Ici un test d\'"\'"\'échappement de simple quote"\n'
        '2;"UTF-8 Test";"ăѣ𝔠ծềſģȟᎥ𝒋ǩľḿꞑȯ𝘱𝑞𝗋𝘴ȶ𝞄𝜈ψ𝒙𝘆𝚣1234567890!@#$%^&*()'
        '-_=+;:\'"\'"\'",[]{}<.>/?~𝘈Ḇ𝖢𝕯٤ḞԍНǏ𝙅ƘԸⲘ𝙉০Ρ𝗤Ɍ𝓢ȚЦ𝒱Ѡ𝓧ƳȤѧᖯć'
        '𝗱ễ𝑓𝙜Ⴙ𝞲𝑗𝒌ļṃŉо𝞎𝒒ᵲꜱ𝙩ừ𝗏ŵ𝒙𝒚ź"'
        f'\r\n--{boundary}--\r\n\''
        ' https://httpbin.org/post'
    )


def test_post_jpg_file():
    request = requests.Request(
        method='POST',
        url='https://httpbin.org/post',
        files={'file': open('data/data.jpg', 'rb')},
        headers={'User-agent': 'UA'}
    )

    curl_cmd = curlify.to_curl(request.prepare())
    boundary = get_boundary(curl_cmd)
    filepath = re.search(
        r'--data-binary @(?P<filepath>\S+)',
        curl_cmd
    ).group('filepath')

    assert curl_cmd == (
        "curl -X POST"
        " -H 'Content-Length: 36782'"
        f" -H 'Content-Type: multipart/form-data; boundary={boundary}'"
        " -H 'User-agent: UA'"
        f" --data-binary @{filepath}"
        " https://httpbin.org/post"
    )


def get_boundary(curl_cmd):
    return re.search(
        r'boundary=(?P<boundary>\w+)',
        curl_cmd
    ).group('boundary')
