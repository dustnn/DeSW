from itertools import count
from structs import TABLE
from base import *


class INDEXER(BASE):
    def __init__(self, _inst, code, jmpr):
        BASE.__init__(self, _inst, code)

        self.jmpr = jmpr

        self.update()


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

    def _patch_table(self, code, binary):
        jt = self.table
        for entry in jt:
            code = bnry.write.byte(code, entry.rva, '\x40')
            self.del_reloc(binary, entry.rva)
        return code


def is_indexer(inst):
    if 'movzx' in inst.mnemonic and '0x' in inst.op_str:
        return True
    return False