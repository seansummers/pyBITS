''' URL safe encoding
'''
import functools
# http://www.flickr.com/groups/api/discuss/72157616713786392/
FLICKR  = u'123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
# https://wiki.ripple.com/Encodings
RIPPLE  = u'rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz'
# http://www.slevenbits.com/blog/2010/07/hexahexacontadecimal.html
# assert(encode(302231454903657293676544) == u'iFsGUkO.0tsxw')
# assert(decode('iFsGUkO.0tsxw') == 302231454903657293676544)
HHCD    = u'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.~'
CHARSET = HHCD
BASE = len(CHARSET)
MAGNITUDE = functools.partial(pow, BASE)

def encode(value):
    encoded = [ ]
    value = value if isinstance(value, (int, long)) else int(value)
    while value:
        value, mod = divmod(value, BASE)
        encoded.append(mod)
    return u''.join(CHARSET[x] for x in reversed(encoded)) or u'1'

def decode(value):
    return sum(MAGNITUDE(exponent) * CHARSET.index(char)
        for exponent, char in enumerate(reversed(value)))

def decode2(value):
    n = 0
    for char in value:
        n = BASE * n + CHARSET.index(char)
    return n
