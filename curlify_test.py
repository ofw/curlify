import curlify
import re
import requests


def test_empty_data():
    r = requests.post(
        "http://google.ru",
        headers={"user-agent": "mytest"},
    )
    assert curlify.to_curl(r.request) == (
        "curl -X POST "
        "-H 'user-agent: mytest' "
        "-H 'Accept-Encoding: gzip, deflate' "
        "-H 'Accept: */*' "
        "-H 'Connection: keep-alive' "
        "-H 'Content-Length: 0' "
        "http://google.ru/"
    )


def test_ok():
    r = requests.get(
        "http://google.ru",
        data={"a": "b"},
        cookies={"foo": "bar"},
        headers={"user-agent": "mytest"},
    )
    assert curlify.to_curl(r.request) == (
        "curl -X GET "
        "-H 'user-agent: mytest' "
        "-H 'Accept-Encoding: gzip, deflate' "
        "-H 'Accept: */*' "
        "-H 'Connection: keep-alive' "
        "-H 'Cookie: foo=bar' "
        "-H 'Content-Length: 3' "
        "-H 'Content-Type: application/x-www-form-urlencoded' "
        "-d a=b http://google.ru/"
    )


def test_prepare_request():
    request = requests.Request(
        'GET', "http://google.ru",
        headers={"user-agent": "UA"},
    )

    assert curlify.to_curl(request.prepare()) == (
        "curl "
        "-H 'user-agent: UA' "
        "http://google.ru/"
    )


def test_compressed():
    request = requests.Request(
        'GET', "http://google.ru",
        headers={"user-agent": "UA"},
    )
    assert curlify.to_curl(request.prepare(), compressed=True) == (
        "curl -H 'user-agent: UA' --compressed http://google.ru/"
    )


def test_verify():
    request = requests.Request(
        'GET', "http://google.ru",
        headers={"user-agent": "UA"},
    )
    assert curlify.to_curl(request.prepare(), verify=False) == (
        "curl -H 'user-agent: UA' --insecure http://google.ru/"
    )


def test_post_json():
    data = {'foo': 'bar'}
    url = 'https://httpbin.org/post'

    r = requests.Request('POST', url, json=data)
    curlified = curlify.to_curl(r.prepare())

    assert curlified == (
        "curl -H 'Content-Length: 14' "
        "-H 'Content-Type: application/json' "
        "-d '{\"foo\": \"bar\"}' https://httpbin.org/post"
    )


def test_post_csv_file():
    r = requests.Request(
        method='POST',
        url='https://httpbin.org/post',
        files={'file': open('data.csv', 'r')},
        headers={'User-agent': 'UA'}
    )

    curlified = curlify.to_curl(r.prepare())
    boundary = re.search(r'boundary=(\w+)', curlified).group(1)

    expected = (
        'curl'
        ' -H \'User-agent: UA\''
        ' -H \'Content-Length: 519\''
        f' -H \'Content-Type: multipart/form-data; boundary={boundary}\''
        f' -d \'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="data.csv"\r\n\r\n'
        '"Id";"Title";"Content"\n'
        '1;"Simple Test";"Ici un test d\'"\'"\'échappement de simple quote"\n'
        '2;"UTF-8 Test";"ăѣ𝔠ծềſģȟᎥ𝒋ǩľḿꞑȯ𝘱𝑞𝗋𝘴ȶ𝞄𝜈ψ𝒙𝘆𝚣1234567890!@#$%^&*()-_=+;:\'"\'"\'",[]{}<.>/?~𝘈Ḇ𝖢𝕯٤ḞԍНǏ𝙅ƘԸⲘ𝙉০Ρ𝗤Ɍ𝓢ȚЦ𝒱Ѡ𝓧ƳȤѧᖯć𝗱ễ𝑓𝙜Ⴙ𝞲𝑗𝒌ļṃŉо𝞎𝒒ᵲꜱ𝙩ừ𝗏ŵ𝒙𝒚ź"'
        f'\r\n--{boundary}--\r\n\''
        ' https://httpbin.org/post'
    )

    assert curlified == expected


def test_data_with_at():
    request = requests.Request(
        'GET', "http://google.ru",
        data='@example.com'
    )
    assert curlify.to_curl(request.prepare()) == (
        "curl -X GET -H 'Content-Length: 12' --data-raw @example.com http://google.ru/"
    )


def test_empty_header():
    request = requests.Request(
        'POST', "http://google.ru",
        headers={'User-agent': ''}
    )
    assert curlify.to_curl(request.prepare()) == (
        "curl -X POST -H 'User-agent;' -H 'Content-Length: 0' http://google.ru/"
    )


def test_pretty():
    request = requests.Request(
        'GET', "http://google.ru",
        data={'foo': 'bar'}
    )
    assert curlify.to_curl(request.prepare(), pretty=True) == '''curl -X GET \\
  -H 'Content-Length: 7' \\
  -H 'Content-Type: application/x-www-form-urlencoded' \\
  -d foo=bar \\
  http://google.ru/'''


def test_short():
    request = requests.Request(
        'GET', "http://google.ru",
    )
    assert curlify.to_curl(request.prepare(), pretty=True) == (
        "curl http://google.ru/"
    )
