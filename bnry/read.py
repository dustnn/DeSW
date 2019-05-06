from utils import constants
import struct

def _read_data(data, position, size):
    return data[position - constants.code_section_base:position - constants.code_section_base + size]


def dword(data, position):
    b = _read_data(data, position, constants.dword_size)
    a = struct.unpack('<L', b)[0]
    return a


def byte(data, position):
    b = _read_data(data, position, constants.byte_size)
    a = struct.unpack('<B', b)[0]
    return a
    # return read_data(data, position, constants.byte_size)


