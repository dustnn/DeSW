from utils import constants
import struct

def _read_data(data, position, size):
    return data[position - constants.code_section_base:position - constants.code_section_base + size]


def dword(data, position):
    return struct.unpack('<L', _read_data(data, position, constants.dword_size))[0]


def byte(data, position):
    return struct.unpack('<B', _read_data(data, position, constants.byte_size))[0]




