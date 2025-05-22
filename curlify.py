# coding: utf-8
import sys

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
            flat_parts.append(quote(str(k)))
        if v:
            flat_parts.append(quote(str(v)))

    return ' '.join(flat_parts)
