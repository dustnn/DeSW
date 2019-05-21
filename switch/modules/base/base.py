from DeSW.utils import constants
import DeSW.bnry as bnry
import re


class BASE():
    def __init__(self,_inst, code):
        self.inst = _inst
        self.code = code

        self.table = []
        self.table_rva = ()
        self.reg_in = ''

        pass

    def update(self):
        self.table_rva = self._update_table_rva()
        self.table = self._update_table()
        self.reg_in = self._update_reg()
        return True
    def _update_table_rva(self):
        ree = re.search('(0x[0123456789abcdef]*)', self.inst.op_str)
        addr = int(ree.group(1), 16) - constants.module_base
        a = len(self.code)
        if addr not in xrange(constants.code_section_base, a + constants.code_section_base):
            # la jt no esta en la seccion codigo, lo cual es algo raro.
            raise Exception
        return addr

    def _update_reg(self):
        for reg in constants.reg_list:
            if reg in self.inst.op_str[4:]:
                return reg
        raise Exception

    def _update_table(self):
        # custom area
        raise Exception

    def patch(self, code, relocs):
        code = self._patch_inst(code, relocs)
        code = self._patch_table(code, relocs)
        return code

    def _patch_inst(self, code, relocs):
        for i, a in enumerate(self.inst.bytes):
            # bnry.write.dword(code, )
            # pass
            code = bnry.write.byte(code, self.inst.rva + i, '\x90')
        self.del_reloc(relocs, self.inst.rva+3)
        return code

    def _patch_table(self, code, relocs):
        # custom area
        raise Exception


    def del_reloc(self, relocs, rva):
        if rva in relocs:
            relocs.remove(rva)
        return relocs