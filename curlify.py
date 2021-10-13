# coding: utf-8
import sys

if sys.version_info.major >= 3:
    from shlex import quote
else:
    from pipes import quote


def to_curl(request, compressed=False, verify=True, skip_headers=False):
    """
    Returns string with curl command by provided request object

    Parameters
    ----------
    compressed : bool
        If `True` then `--compressed` argument will be added to result
    verify: bool
        If `True` then `--insecure` argument will be added to result
    skip_headers: bool
        If 'True' then headers [Accept, Accept-Encoding, Connection, User-Agent, Content-Length] will be skipped
    """
    parts = [
        ('curl', None),
        ('-X', request.method),
    ]

    sys_headers = ['accept', 'accept-encoding', 'connection', 'user-agent', 'content-length']
    for k, v in sorted(request.headers.items()):
        if skip_headers and k.lower() in sys_headers:
            continue
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
