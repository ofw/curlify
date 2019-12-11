# coding: utf-8
"""
A library to convert python requests request object to curl command.

Usage:

    >>> curlify.to_curl(preparedRequest)
"""
import os
import sys
import tempfile
from _md5 import md5

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

    for k, value in sorted(request.headers.items()):
        parts += [('-H', '{0}: {1}'.format(k, value))]

    if request.body:
        body = request.body
        data_arg = '-d'
        if isinstance(body, bytes):
            try:
                body = body.decode('utf-8')
            # handle binary files
            except UnicodeDecodeError:
                data_file = os.path.join(
                    tempfile.tempdir,
                    'curlify.{}.data'.format(md5(body).hexdigest())
                )
                with open(data_file, 'wb') as file:
                    file.write(body)
                body = f'@{data_file}'
                data_arg = '--data-binary'
        parts += [(data_arg, body)]

    if compressed:
        parts += [('--compressed', None)]

    if not verify:
        parts += [('--insecure', None)]

    parts += [(None, request.url)]

    flat_parts = []
    for k, value in parts:
        if k:
            flat_parts.append(quote(k))
        if value:
            flat_parts.append(quote(value))

    return ' '.join(flat_parts)
