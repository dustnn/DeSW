from itertools import count
from utils import *
from structs import TABLE
from base import *

# import bnry.write

class JUMPER(BASE):
    def __init__(self, _inst, code):
        BASE.__init__(self, _inst, code)

        self.update()


    def _update_table(self):
        jt_list = []
        for jt_index in count():
            entry = TABLE()
            entry.rva = self.table_rva + jt_index*4
            entry.pointer = bnry.read.dword(self.code, entry.rva) - constants.module_base
            if entry.pointer in srange(constants.code_section_base, len(self.code)):
                jt_list.append(entry)
                continue
            break

        return jt_list


    def _patch_table(self, code, relocs):
        for entry in self.table:
            code = bnry.write.dword(code, entry.rva, '\x40\x40\x40\x40')
            self.del_reloc(relocs, entry.rva)
        return code



def is_jumper(inst):
    if _check_generic(inst):
        if _check_reg(inst):
            return True
    return False

def _check_generic(inst):
    if 'jmp' in inst.mnemonic and 'dword' in inst.op_str and '*4' in inst.op_str and '0x' in inst.op_str:
        return True
    return False

def _check_reg(inst):
    reg_count = 0
    for reg in constants.reg_list:
        reg_count += inst.op_str.count(reg)
    if reg_count == 1:
        return True
    return False
