from flask import jsonify


def jsonapiify(*args, **kwargs):
    """ jsonify wrapper that sets content-type"""
    response = jsonify(*args, **kwargs)
    response.mimetype = 'application/vnd.api+json'
    return response

def ok(data):
    return jsonapiify(data), 200

def created(data):
    return jsonapiify(data), 201

def not_found(id):
    payload = jsonapiify({
        'errors': [{'status': 'Not Found',
                    'detail': f'id=({id}) does not exist'}]
    })
    return payload, 404

def no_content():
    return '', 204

def cant_process(data):
    """ Note that some folks are split on this one.
    It's being used in this api specifically for malformed
    payloads or query params.  I've also used 400 for that.
    Style thing I think.
    """
    return jsonapiify(data), 422

def conflict(msg):
    payload = jsonapiify({
        'errors': [{'status': 'Conflict',
                    'detail': msg}]
    })
    return payload, 409
