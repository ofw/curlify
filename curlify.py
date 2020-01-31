# coding: utf-8
import sys

if sys.version_info.major >= 3:
    from shlex import quote
else:
    from pipes import quote


def to_curl(request, compressed=False, verify=True, header_sep=None):
    """
    Returns string with curl command by provided request object

    Parameters
    ----------
    compressed : bool
        If `True` then `--compressed` argument will be added to result
    header_sep : str
        If not `None` then `header_sep` value will be added after each `'-H k: v'` pair
    """
    parts = [
        ('curl', None),
        ('-X', request.method),
    ]

    if header_sep is None:
        header_sep = ''

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
            temp_part = quote(v)
            if k == "-H" and header_sep:
                temp_part += header_sep
            flat_parts.append(temp_part)
    return ' '.join(flat_parts)
