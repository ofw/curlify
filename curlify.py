# coding: utf-8
import sys
from copy import deepcopy

import requests

if sys.version_info.major >= 3:
    from shlex import quote
else:
    from pipes import quote


def to_curl(request, compressed=False, verify=True):
    """
    Returns string with curl command by provided request object

    Parameters
    ----------
    compressed : bool
        If `True` then `--compressed` argument will be added to result
    """
    parts = [
        ('curl', None),
        ('-X', request.method),
    ]

    for k, v in sorted(request.headers.items()):
        parts += [('-H', '{0}: {1}'.format(k, v))]

    if request.body:
        body = request.body
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        parts += [('-d', body)]

    if compressed:
        parts += [('--compressed', None)]

    if not verify:
        parts += [('--insecure', None)]

    parts += [(None, request.url)]

    flat_parts = []
    for k, v in parts:
        if k:
            flat_parts.append(quote(k))
        if v:
            flat_parts.append(quote(v))

    return ' '.join(flat_parts)


def to_raw_http_curl(response, *args, **kwargs):
    """
    Returns string with curl command by provided response object.

    If you use a custom http scheme (like `http-custom://aaa.bbb.ccc/path`)
    and use your custom `HTTPConnectionPool` to parse it to generate a http
    connection, this method will return curl with the final http host.

    Parameters
    ----------
    response : requests.models.Response
    """
    assert isinstance(response, requests.models.Response)
    request = deepcopy(response.request)
    connection_pool = response.connection.poolmanager.connection_from_url(request.url)
    connection = connection_pool._get_conn()
    http_scheme = connection_pool.scheme
    if http_scheme not in ('http', 'https'):
        http_scheme = 'http'

    request.url = '{scheme}://{host}:{port}{path_url}'.format(
        scheme=http_scheme, host=connection.host, port=connection.port, path_url=request.path_url
    )
    return to_curl(request, *args, **kwargs)
