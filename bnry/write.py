from DeSW.utils import constants


def dword(data, position, value):
    return _write_data(data, position - constants.code_section_base, value, constants.dword_size)


def byte(data, position, value):
    return _write_data(data, position - constants.code_section_base, value, constants.byte_size)


def _write_data(data, position, value, size):
    return data[:position] + value + data[position + size:]


