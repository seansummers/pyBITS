#! /usr/bin/env python
''' A basic bottle app skeleton '''

root = './files'

import bottle
from bottle import Bottle, response, request, static_file
import bits_util
from wsgiref.simple_server import ServerHandler
ServerHandler.http_version = '1.1'

app = application = Bottle()

@app.route('/<filename:path>')
def static(filename):
    return static_file(filename, root=root)

@app.hook('after_request')
def bits_headers():
    response.headers['BITS-Packet-Type'] = 'Ack'
    print(request.path, request.headers.items(), response.headers.items())

@app.route('/<file_path:path>', method='BITS_POST')
def bits(file_path):
    cmd = request.headers['BITS-Packet-Type'].upper()
    session_id = request.get_header('BITS-Session-Id')
    if cmd == 'CREATE-SESSION':
        response['BITS-Protocol'] = bits_util.select_protocol_from_supported(
            request.headers['BITS-Supported-Protocols'])
        response['Accept-Encoding'] = 'Identity'
        try:
            session_id = bits_util.session_create(root, file_path)
        except:
            bottle.abort('409 Conflict')
    elif cmd == 'FRAGMENT':
        if False and int(request.headers['Content-Length']) > 168000:
            bottle.abort('406 Not') # if not contiguous
            #bottle.abort('413 Request entity too large') # if not contiguous
            #bottle.abort('416 Range-Not-Satisfiable') # if not contiguous
        response['BITS-Received-Content-Range'] = bits_util.session_fragment(
            root, session_id, file_path,
            request.headers['Content-Range'],
            request['wsgi.input'])
    elif cmd  == 'CLOSE-SESSION':
        try:
            bits_util.session_close(root, session_id, file_path)
        except:
            bottle.abort('404 invalid session')
    elif cmd  == 'CANCEL-SESSION':
        try:
            bits_util.session_close(root, session_id, file_path)
        except:
            bottle.abort('404 invalid session')
    elif cmd == 'PING':
        pass
    else:
        bottle.abort('401 invalid BITS-Packet-Type: {0}'.format(cmd))
    response['BITS-Session-Id'] = session_id

@app.error(401)
@app.error(404)
@app.error(406)
@app.error(409)
@app.error(413)
@app.error(416)
@app.error(419)
def error(error):
    pass

if __name__ == '__main__':
    bottle.debug(True)
    bottle.run(app=app,
        server='wsgiref',
        host='0.0.0.0',
        port=8080,
        debug=True,
        reloader=True)
