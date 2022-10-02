import os
import uuid
import urllib
import urlparse
import encode

BITS_PROTOCOL = '{7df0354d-249b-430f-820d-3d2a9bef4931}'

def normalized_filepath(client_file_path):
    ''' valid, consistent file_path, starting with a single / '''
    # normpath has a weird double double-slash bug, methinks
    # so we guarantee that there will be a single leading slash here
    target_path = os.path.normpath((3 * os.path.sep) + client_file_path)
    if os.path.pardir in target_path:
        raise ValueError, 'invalid file_path'
    return target_path

def session_from_file_path(file_path):
    filepath = normalized_filepath(file_path)
    quoted_path = urllib.quote(filepath, safe="%/:=&?~#+!$,;'@()*[]|")
    url = urlparse.urljoin('file:', quoted_path)
    file_uuid = uuid.uuid5(uuid.NAMESPACE_URL, url)
    session_id = encode.encode(file_uuid)
    return (session_id, url)

def validate_session(session_id, file_uri):
    sid, uri = session_from_file_path(file_uri)
    if session_id != sid:
        raise ValueError, 'invalid session_id'
    return uri

def select_protocol_from_supported(bits_supported_protocols):
    ''' currently only support one possible protocol '''
    if BITS_PROTOCOL in bits_supported_protocols.lower():
        return BITS_PROTOCOL

def absolute_path_from_uri(uri, file_root):
    client_path = '.' + urlparse.urlsplit(uri).path
    host_path = os.path.abspath(file_root)
    return os.path.normpath(os.path.join(host_path, client_path))

def session_cancel(file_root, session_id, file_path):
    uri = validate_session(session_id, file_path)
    os.remove(absolute_path_from_uri(uri, file_root))

def session_close(file_root, session_id, file_path):
    uri = validate_session(session_id, file_path)
    open(absolute_path_from_uri(uri, file_root) + '.done', 'w').close()

def parse_content_range(http_content_range):
    first_last, total = http_content_range[6:].split('/')
    first, last = first_last.split('-')
    if last <= total: # BG_E_INVALID_RANGE
        return(int(x) for x in (first, last, total))

def session_fragment(file_root, session_id, file_path,
        content_range, fin):
    uri = validate_session(session_id, file_path)
    first, last, total = parse_content_range(content_range)
    filename = absolute_path_from_uri(uri, file_root)
    with open(filename, 'a') as fout:
        skip = max(fout.tell() - first, 0)
        if skip: fin.read(skip)
        fout.write(fin.read(1 + last - first - skip))
    return os.stat(filename).st_size

def session_create(file_root, file_path):
    session_id, url = session_from_file_path(file_path)
    filename = absolute_path_from_uri(url, file_root)
    if os.path.exists(filename):
        raise ValueError, 'file already exists'
    open(filename, 'a').close()
    return session_id
