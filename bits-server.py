'BITS 1.5 Upload Protocol'

BITS_PROTOCOL = '{7df0354d-249b-430f-820d-3d2a9bef4931}'
BITS_CONTEXT_SERVER = '0x5'
BITS_CONTEXT_REMOTE_APPLICATION	= '0x7'
BITS_E_INVALIDARG = '0x80070057'
error_headers = {
	'Content-Length': 0,
	'BITS-Packet-Type': 'Ack',
	'BITS-Error-Code': BITS_E_INVALIDARG,
	'BITS-Error-Context': BITS_CONTEXT_REMOTE_APPLICATION,
}
ack_headers = {
	'Content-Length': 0,
	'BITS-Packet-Type': 'Ack',
}
import urllib
def session_id(file_path, sid = None):
	xsid = urllib.quote(file_path, '/-{}')[:99]
	if sid and sid != xsid:
		raise ValueError, 'Session-Id is invalid'
	return {'BITS-Session-Id': xsid}
def PING():
	return ack_headers
def FRAGMENT(file_path, sid, content_range, content_length, rfile):
	headers = ack_headers.copy()
	headers.update(session_id(file_path, sid))
	range, length = content_range[6:].split('/')
	first, last = range.split('-')
        rfile.read(int(content_length)) # TODO: save some data
	headers['BITS-Received-Content-Range'] = 1 + int(last) # TODO: os.stat file, maybe?
	#if (int(length) - 1) == int(last): # TODO: this is for UploadReply
	#	headers['BITS-Reply-URL'] = '[some url]'
	return headers
def CLOSE_SESSION(file_path, sid):
	headers = ack_headers.copy()
	headers.update(session_id(file_path, sid))
	headers['Connection'] = 'Close'
	return headers
CANCEL_SESSION = CLOSE_SESSION
def CREATE_SESSION(file_path, BITS_supported_protocols):
	if BITS_PROTOCOL not in BITS_supported_protocols:
		raise ValueError, 'BITS Protocol not supported'
	headers = ack_headers.copy()
	headers.update(session_id(file_path))
	headers.update({
		'Accept-Encoding': 'Identity',
		'BITS-Protocol': BITS_PROTOCOL,
		#('BITS-Host-Id', 'e6400'), # http://blabhlab:8080/whateer
		#('BITS-Host-Fallback-Timeout', 6), # time in seconds
	})
	return headers

import BaseHTTPServer
import itertools
class BITSRequest(BaseHTTPServer.BaseHTTPRequestHandler):
	server_version = ' '.join((BaseHTTPServer.BaseHTTPRequestHandler.server_version, 'BITS-server/0.1'))
	protocol_version = 'HTTP/1.1' # required, or 'Microsoft BITS/7.5' refuses to work
        def send_header(s, a, b):
                print('SENT {a}: {b}'.format(a=a, b=b))
                BaseHTTPServer.BaseHTTPRequestHandler.send_header(s, a, b)
	def do_BITS_POST(self):
                print('\nINCOMING\n{0}'.format(str(self.headers)))
		self.close_connection = False
		request = self.headers['BITS-Packet-Type'].upper()
		client = ':'.join(map(str, self.client_address))
		path = self.path
		print('SENDING RESPONSE {0}'.format('BITS {request}://{client}{path}'.format(request=request,client=client,path=path)))
		response_code = 200
		response = 'OK BITS'
		try:
			if request == 'PING':
				h = PING()
			elif request == 'CREATE-SESSION':
				h = CREATE_SESSION(path, self.headers['BITS-Supported-Protocols'].split())
			elif request == 'FRAGMENT':
				h = FRAGMENT(path, self.headers['BITS-Session-Id'], self.headers['Content-Range'], self.headers['Content-Length'], self.rfile)
			elif request in ('CLOSE-SESSION', 'CANCEL-SESSION'):
				h = CLOSE_SESSION(path, self.headers['BITS-Session-Id'])
		except:
			response_code = 500
			h = error_headers.copy()
			h.update(session_id(path, self.headers['BITS-Session-Id']))
		finally:
			self.send_response(response_code, response)
			tuple(itertools.starmap(self.send_header, h.iteritems()))
			#tuple(itertools.starmap(self.send_header, headers))
			self.end_headers()
			if 'Connection' in self.headers:
				self.close_connection = True

def run_while_true(server_class=BaseHTTPServer.HTTPServer,
                   handler_class=BITSRequest):
	server_address = ('', 9999)
	httpd = server_class(server_address, handler_class)
	httpd.serve_forever()

if __name__ == '__main__':
	run_while_true()
