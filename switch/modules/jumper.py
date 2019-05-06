from itertools import count
from utils import *
from structs import TABLE
from base import *

# import bnry.write

class JUMPER(BASE):
    def __init__(self, _inst, code):
        BASE.__init__(self, _inst, code)
        # # self.inst = INST(_inst)
        # self.inst = _inst
        # self.code = code
        # self.stub_rva = len(code) + constants.code_section_base


        self.update()

    #
    # def update(self):
    #     self.table_rva = self._update_table_rva()
    #     self.table = self._update_table()
    #     self.reg_in = self._update_reg()
    #     return True

    # def _update_table_rva(self):
    #     ree = re.search('(0x[0123456789abcdef]*)', self.inst.op_str)
    #     addr = int(ree.group(1), 16) - constants.module_base
    #     a = len(self.code)
    #     if addr not in xrange(constants.code_section_base, a + constants.code_section_base):
    #         # la jt no esta en la seccion codigo, lo cual es algo raro.
    #         raise Exception
    #     return addr
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
    # def _update_reg(self):
    #     for reg in constants.reg_list:
    #         if reg in self.inst.op_str[4:]:
    #             return reg
    #     raise Exception

    # def patch(self, code, binary):
    #     code = self._patch_inst(code, binary)
    #     code = self._patch_table(code, binary)
    #     return code

    def _patch_table(self, code, relocs):
        for entry in self.table:
            code = bnry.write.dword(code, entry.rva, '\x40\x40\x40\x40')
            self.del_reloc(relocs, entry.rva)
        return code

    # def _patch_inst(self, code, binary):
    #     for i, a in enumerate(self.inst.bytes):
    #         # bnry.write.dword(code, )
    #         # pass
    #         code = bnry.write.bytet(code, self.inst.rva + i, '\x90')
    #     self.del_reloc(binary, self.inst.rva+3)
    #     return code


    # def del_reloc(self, binary, rva):
    #     for relocs in binary.relocations:
    #         for reloc in relocs.entries:
    #             if reloc.type == constants.HIGHLOW:
    #                 if reloc.address == rva:
    #                     pass
    #                     del reloc
    #
    #     return True

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
