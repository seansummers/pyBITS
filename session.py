reason_codes = {
	'200': 'OK',		# The request was successful
	'201': 'Created',	# The session was created
	'403': 'Forbidden',	# The user is not allowed to upload to the specified URL
	'404': 'Not Found',	# The specified URL does not exist
	'409': 'Conflict',	# The file exists on the server and cannot be overwritten
}
headers = {
	'Content-Length': 0,
	'BITS-Packet-Type: 'Ack',
}
class Session(object):
	''' Resumable session '''

	def get_session_id(seed):
		''' using a seed, retrieve a valid, stable session_id '''
		import urllib
		return urllib.quote(seed, '-{}')[:99]

	def __init__(self, base_path, file_path = None, session_id = None):
		''' initialize or resume a session '''
		base_path: file storage for all state (trusted)
		file_path: file being uploaded (from client)
		session_id: existing session_id for resuming (from client)
		'''
		import os
		self.base_path = base_path
		self.file_path = os.relpath(os.normpath(os.path.join(base_path, file_path)), base_path)
		self.session_id = session_id or produce_session_id(file_path)

		if os.pardir in file_path:
			raise ValueError, 'No relative links allowed in file_path'
		if not session_id:
			session_id = generate_session_id(seed)
		self.session_id = session_id
		self.file_path = basepath
		self.file_name = filename
		self.storage
		if os.path.isfile('{0}.state'.format(session_id)): # existing session
