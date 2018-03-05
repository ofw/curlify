# coding: utf-8


def to_curl(request):
    headers = ["'{0}: {1}'".format(k, v) for k, v in request.headers.items()]
    headers = " -H ".join(sorted(headers))

    command = "curl -X {method} -H {headers} -d '{data}' '{uri}' --compressed".format(
        data=request.body or "",
        headers=headers,
        method=request.method,
        uri=request.url,
    )
    return command
