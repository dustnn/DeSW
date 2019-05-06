from itertools import count
from structs import TABLE
from base import *


class INDEXER(BASE):
    def __init__(self, _inst, code, jmpr):
        BASE.__init__(self, _inst, code)
        # self.inst = INST(_inst)
        # self.inst = _inst
        # self.code = code
        # al objeto jmpr solo lo uso para obtener la adrr de la jt, ya que la it va desde donde indica table_rva hasta
        # table_rva del jmpr
        self.jmpr = jmpr


        self.update()


    # def inst_rva(self):
    #     return self.inst.rva

    # def update(self):
    #     self.table_rva = self._update_table_rva()
    #     self.table = self._update_table()
    #     self.reg_in = self._update_reg()
    #     return True


    # def _update_table_rva(self):
    #     ree = re.search('(0x[0123456789abcdef]*)', self.inst.op_str)
    #     return int(ree.group(1), 16) - constants.module_base

    def _update_table(self):
        it_list = []
        for it_index in count():
            entry = TABLE()

            entry.rva = self.table_rva + it_index
            entry.pointer = bnry.read.byte(self.code, entry.rva)
            if entry.pointer < len(self.jmpr.table):
                it_list.append(entry)
                continue

            break
        return it_list
    # def _update_reg(self):
    #     for reg in constants.reg_list:
    #         if reg in self.inst.op_str[4:]:
    #             return reg
    #     raise Exception

    # def patch(self, code, binary):
    #     code = self._patch_inst(code, binary)
    #     code = self._patch_table(code, binary)
    #     return code

    def _patch_table(self, code, binary):
        jt = self.table
        for entry in jt:
            code = bnry.write.byte(code, entry.rva, '\x40')
            self.del_reloc(binary, entry.rva)
        return code
    # def _patch_inst(self, code, binary):
    #     for i, a in enumerate(self.inst.bytes):
    #         code = bnry.write.bytet(code, self.inst.rva + i, '\x90')
    #     self.del_reloc(binary, self.inst.rva + 3)
    #     return code

    # def del_reloc(self, binary, rva):
    #     for relocs in binary.relocations:
    #         for reloc in relocs.entries:
    #             if reloc.type == constants.HIGHLOW:
    #                 if reloc.address == rva:
    #                     pass
    #                     del reloc


def is_indexer(inst):
    if 'movzx' in inst.mnemonic and '0x' in inst.op_str:
        return True
    return False