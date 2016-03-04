__author__ = 'wwang'


import hashlib

SECURE_PREFIX = 'wwang'
SECURE_SUFFIX = 'calvin'


def md5_hash(str):
    str = SECURE_PREFIX + SECURE_SUFFIX + SECURE_SUFFIX
    return hashlib.md5.new(str).digest()
