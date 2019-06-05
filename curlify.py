# coding: utf-8
import sys

PY2 = sys.version_info[0] == 2

if not PY2:  
    from pipes import quote

    # From https://github.com/flask-admin/flask-admin/blob/master/flask_admin/_compat.py (License BSD) 
    def as_unicode(s):
        if isinstance(s, bytes):
            return s.decode('utf-8')
        return s

else:
    from shlex import quote

    def as_unicode(s):
        if isinstance(s, str):
            return s.decode('utf-8')

        return unicode(s)  # NOQA: F82


def to_curl(request, compressed=False, verify=True):
    """
    Returns string with curl command by provided request object

    Parameters
    ----------
    compressed : bool
        If `True` then `--compressed` argument will be added to result
    """
    parts = [('curl', None), ('-X', request.method)]

    for k, v in sorted(request.headers.items()):
        parts += [('-H', '{0}: {1}'.format(as_unicode(k), as_unicode(v)))]

    if request.body:
        body = as_unicode(request.body)
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
