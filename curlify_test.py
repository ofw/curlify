# coding: utf-8
import unittest

import httpx
import requests
import responses
import respx

import curlify


class TestCurlify(unittest.TestCase):
    def mock_add_get(self):
        self.request_reponses.add(
            responses.GET,
            'https://example.com/',
            body='fake_example.com',
            status=200
        )
        self.httpx_respx.get(
            "/",
            content="fake_example.com",
            status_code=200
        )

    def mock_add_post(self):
        self.request_reponses.add(
            responses.POST,
            'https://example.com/',
            body='fake_example.com',
            status=200
        )
        self.httpx_respx.post(
            "/",
            content="fake_example.com",
            status_code=201
        )

    def setUp(self):
        self.request_reponses = responses.RequestsMock()
        self.request_reponses.start()

        self.httpx_respx = respx.mock(base_url="https://example.com")
        self.httpx_respx.start()

    def tearDown(self):
        self.request_reponses.stop()
        self.httpx_respx.stop()

    def test_mocks(self):
        self.mock_add_get()
        self.mock_add_post()

        r = requests.get("https://example.com/")
        assert r.text == "fake_example.com"
        r = httpx.get("https://example.com/")
        assert r.text == "fake_example.com"
        r = requests.post("https://example.com/")
        assert r.text == "fake_example.com"
        r = httpx.post("https://example.com/")
        assert r.text == "fake_example.com"

    def assert_approx_curl(self, curl_equivalent, curlify_string):
        """
        Check that all elements of curl_equivalent are in result of to_curl
        The approximation allows for to_curl to include other flags and
        shuffle order.

        equivalency is not done as
         * requests does not set host explicitly and relies http lib to do
           it on its behalf
         * httpx does not set on empty bodycontent-length
        """
        for arg in curl_equivalent:
            assert arg in curlify_string

    def assert_all(self, curl_equivalent, method, *args, **kwargs):
        for module in requests, httpx:
            response = getattr(module, method)(*args, **kwargs)
            self.assert_approx_curl(
                curl_equivalent,
                curlify.to_curl(response.request)
            )

    def test_post_empty_data(self):
        self.mock_add_post()
        self.assert_all(
            [
                "curl -X POST ",
                "-H 'accept: */*' ",
                "-H 'accept-encoding: gzip, deflate' ",
                "-H 'connection: keep-alive' ",
                "-H 'user-agent: mytest' ",
                "https://example.com/",
            ],
            "post",
            "https://example.com/",
            headers={
                "user-agent": "mytest",
            },
        )

    def test_post(self):
        self.mock_add_post()
        self.assert_all(
            [
                "curl -X POST ",
                "-H 'accept: */*' ",
                "-H 'accept-encoding: gzip, deflate' ",
                "-H 'connection: keep-alive' ",
                "-H 'content-length: 3' ",
                "-H 'content-type: application/x-www-form-urlencoded' ",
                "-H 'cookie: foo=bar' ",
                "-H 'user-agent: mytest' ",
                "-d a=b ",
                "https://example.com/",
            ],
            "post",
            "https://example.com/",
            data={"a": "b"},
            cookies={"foo": "bar"},
            headers={"user-agent": "mytest"},
        )

    def test_prepare_request(self):
        request = requests.Request(
            'GET', "https://example.com/",
            headers={"user-agent": "UA"},
        )
        assert curlify.to_curl(request.prepare()) == (
            "curl -X GET "
            "-H 'user-agent: UA' "
            "https://example.com/"
        )

    def test_httpx_request(self):
        request = httpx.Request(
            'GET', "https://example.com",
            headers={"user-agent": "UA"},
        )
        curl_equivalent = curlify.to_curl(request)
        for substring in [
            "curl -X GET ",
            "-H 'user-agent: UA' ",
            "https://example.com",
        ]:
            assert substring in curl_equivalent

    def test_compressed_request(self):
        request = requests.Request(
            'GET', "https://example.com/",
            headers={"user-agent": "UA"},
        )
        assert curlify.to_curl(request.prepare(), compressed=True) == (
            "curl -X GET -H 'user-agent: UA' --compressed https://example.com/"
        )

    def test_verify(self):
        request = requests.Request(
            'GET', "https://example.com/",
            headers={"user-agent": "UA"},
        )
        assert curlify.to_curl(request.prepare(), verify=False) == (
            "curl -X GET -H 'user-agent: UA' --insecure https://example.com/"
        )

    def test_post_json(self):
        self.mock_add_post()
        self.assert_all(
            [
                "curl -X POST ",
                "-H 'content-length: 14' ",
                "-H 'content-type: application/json' ",
                "-d '{\"foo\": \"bar\"}' ",
                "https://example.com/",
            ],
            "post",
            'https://example.com/',
            json={'foo': 'bar'},
        )

    def test_post_csv_file(self):
        self.mock_add_post()
        with open('data.csv', 'r') as fd:
            content = fd.read()
        self.assert_all(
            [
                'curl -X POST ',
                '-H \'content-length: 543\' ',
                '-H \'content-type: multipart/form-data; boundary=',
                '-H \'user-agent: UA\'',
                '-d \'--',
                'Content-Disposition: form-data; name="file"; filename="da'
                'ta.csv"\r\nContent-Type: text/csv\r\n\r\n"Id";"Title";"Co'
                'ntent"\n1;"Simple Test";"Ici un test d\'"\'"\'échappement'
                ' de simple quote"\n2;"UTF-8 Test";"ăѣ𝔠ծềſģȟᎥ𝒋ǩľḿꞑȯ𝘱𝑞𝗋𝘴ȶ𝞄𝜈'
                'ψ𝒙𝘆𝚣1234567890!@#$%^&*()-_=+;:\'"\'"\'",[]{}<.>/?~𝘈Ḇ𝖢𝕯٤Ḟԍ'
                'НǏ𝙅ƘԸⲘ𝙉০Ρ𝗤Ɍ𝓢ȚЦ𝒱Ѡ𝓧ƳȤѧᖯć𝗱ễ𝑓𝙜Ⴙ𝞲𝑗𝒌ļṃŉо𝞎𝒒ᵲꜱ𝙩ừ𝗏ŵ𝒙𝒚ź"\r\n',
                'https://example.com'
            ],
            'post',
            'https://example.com/',
            files={'file': ('data.csv', content, 'text/csv')},
            headers={'User-agent': 'UA'}
        )
