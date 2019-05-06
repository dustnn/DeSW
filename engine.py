from _testcapi import code_newempty

from capstone import *
from lief import PE
from switch.switch import *
from switch.modules.structs import INST
from utils import *
from collections import deque

# def disassemble(code, debug=False):
#     # desensambla el codigo de self.code y retorna una lista con el desensamblado
#     disasm_list = []
#
#     md = Cs(CS_ARCH_X86, CS_MODE_32)
#     md.skipdata = True
#     md.detail = False
#
#     for instruction in md.disasm(code, 0x1000):
#         custom_inst = INST(instruction)
#         disasm_list.append(custom_inst)
#
#
#     return disasm_list

def detect(code):

    disasm_stack = deque()

    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.skipdata = True
    md.detail = False

    for instruction in md.disasm(code, constants.code_section_base):
        custom_inst = INST(instruction)
        disasm_stack.append(custom_inst)
        if len(disasm_stack) < 6:
            continue

        disasm_stack.popleft()
        if is_jumper(disasm_stack[-1]):
            return disasm_stack

    return False

def run(code, relocs, verbose=False):

    while True:
        disasm = detect(code)
        if not disasm:
            break

        sw = SWITCH(disasm, code)
        if sw.decompile_switch():
            if verbose:
                print 'largo %x' % len(code)
            code = sw.patch(code, relocs)
            code = sw.resemble(code)

        else:
            break

    if verbose:
        printer.bytearray(code, size=64)

    return [code, relocs]
