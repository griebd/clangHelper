from ctypes import CDLL, c_char_p
from platform import system
from re import compile

clang_version = None

def get_libclang_version():
    global clang_version
    if clang_version:
        return clang_version

    if system() == 'Darwin':
        lib_file = 'libclang.dylib'
    elif system() == 'Windows':
        lib_file = 'libclang.dll'
    else:
        lib_file = 'libclang.so'

    lib = CDLL(lib_file)
    version = lib.clang_getClangVersion
    version.restype = c_char_p

    v = compile('(?<=RELEASE\_)[\d+#]+').search(version().decode())
    clang_version = v.group(0)

    return clang_version
