# -*- coding: utf-8 -*-

import ujson

from starlette.responses import Response


def jsonify(content, status):
    return Response(
        content=ujson.dumps(content),
        status_code=status,
        headers={'content-type': 'application/json'}
    )


def request_ip(request):
    return request.client.host
    # return request.remote_addr or request.ip

