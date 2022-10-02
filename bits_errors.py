class BITSError(Exception):
    pass

class BITSServerError(BITSError):
    result = '400 Error'
    error = '0x80070057'
    context = '0x5'

class ParseError(BITSServerError):
    result = '400 Parse Error'

class UnsupportedBITSProtocol(BITSServerError):
    result = '400 Unsupported BITS-Protocol'

class PermissionDenied(BITSServerError):
    result = '403 Permission Denied'

class SessionAlreadyClosed(BITSServerError):
    result = '404 No Such Session'

class ContentLengthMissing(BITSServerError):
    result = '411 Missing or Bad Content-Length'

class IncorrectStartOffset(BITSError):
    #BITS-Received-Content-Range set correctly
    result = '416 Incorrect Content-Range'

class UnknownSession(BITSServerError):
    result = '500 Unknown BITS-Session-Id'
    error = '0x8020001F'

class FragmentError(BITSServerError):
    result = '501 Fragment Error' # 501?
    context = '0x7'
