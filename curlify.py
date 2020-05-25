# coding: utf-8
import sys

if sys.version_info.major >= 3:
    from shlex import quote
else:  # pragma: no cover, 2.7 flavor is not tested
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
        parts += [('-H', '{0}: {1}'.format(k.lower(), v))]

    body_content = request.body if hasattr(request, "body") else request.read()
    if body_content:
        if isinstance(body_content, bytes):
            body_content = body_content.decode('utf-8')
        parts += [('-d', body_content)]

    if compressed:
        parts += [('--compressed', None)]

    if not verify:
        parts += [('--insecure', None)]

    parts += [(None, str(request.url))]

    flat_parts = []
    for k, v in parts:
        if k:
            flat_parts.append(quote(k))
        if v:
            flat_parts.append(quote(v))

    return ' '.join(flat_parts)
