# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.9 (tags/v3.8.9:a743f81, Apr  2 2021, 10:59:45) [MSC v.1928 32 bit (Intel)]
# Embedded file name: singleton.py
import atexit
import os


def _handler():
    pass


def _uid():
    import hashlib, sys
    with open(sys.argv[0], 'rb') as (file):
        data = file.read()
    hash_ = hashlib.md5(data)
    return hash_.hexdigest()


def init(uid=_uid(), crash_handler=_handler, crash_handler_args=(), exit_handler=_handler, exit_handler_args=()):
    temp_path = os.environ['TEMP']
    _path = os.path.join(temp_path, uid)
    flags = os.O_CREAT | os.O_EXCL
    os.makedirs(temp_path, exist_ok=True)
    try:
        _descriptor = os.open(_path, flags)
    except FileExistsError:
        try:
            os.remove(_path)
        except PermissionError:
            exit_handler(*exit_handler_args)
            raise SystemExit
        else:
            crash_handler(*crash_handler_args)
            _descriptor = os.open(_path, flags)
    else:
        atexit.register(os.remove, _path)
        atexit.register(os.close, _descriptor)
