from modules import *
from keystone import *


class SWITCH():
    # switch es una clase disenada para detectar cnstrucciones de switch y parchearlas a if
    # lo hace mutando la seccion code del binario
    def __init__(self, disasm, code):
        self.disasm = disasm
        self.code = code

        self.jmpr = None
        self.indxr = None

        pass

    def decompile_switch(self):
        # como sabemos que en el desensamblado viene un switch, enocnes podemos obviar varios chequeos
        self.jmpr = JUMPER(self.disasm[-1], self.code)
        if is_indexer(self.disasm[-2]):
            self.indxr = INDEXER(self.disasm[-2], self.code, self.jmpr)
        return True


    def patch(self, code, binary):
        # print 'LEN DE CODE luego del patch 0x%x' % len(code)
        code = self.jmpr.patch(code, binary)
        if self.indxr:
            code = self.indxr.patch(code, binary)

        return code


    def resemble(self, code):
        # partiendo de la data del jumper y del indexer si existe, arma la tabla de transferencia
        # esta es la tabla de verdad del switch, que como dominio tiene al valor de entrada y al codomnio la addr
        # donde debe saltar
        if not self.jmpr.table:
            return code

        trnsfr_table = []
        reg_in = ""
        if not self.indxr:
            trnsfr_table = self.jmpr.table
            reg_in = self.jmpr.reg_in
        else:
            for entry in self.indxr.table:
                trnsfr_table.append(self.jmpr.table[entry.pointer])
            reg_in = self.indxr.reg_in



        if len(trnsfr_table) > 0x7f:
            stub_len = 12*len(trnsfr_table)
        else:
            stub_len = 9 * len(trnsfr_table)

        self.stub_rva = self.find_space(code, stub_len)


        # jump de hookeo
        hook_jmp_asm = 'jmp 0x%x' % self.stub_rva
        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        hook_jmp_opcode = ks.asm(hook_jmp_asm, self.jmpr.inst.rva)[0]

        for i, opcode in enumerate(hook_jmp_opcode):
            code = bnry.write.byte(code, self.jmpr.inst.rva + i, chr(opcode))

        # if-switch table
        stub_asm = ''
        for i, entry in enumerate(trnsfr_table):
            stub_asm += 'cmp %s, 0x%08x\n ' % (reg_in, i)
            stub_asm += 'je 0x%08x\n ' % entry.pointer

        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        stub_opcode = ks.asm(stub_asm, self.stub_rva)[0]


        for i, opcode in enumerate(stub_opcode):
            code = bnry.write.byte(code, self.stub_rva + i, chr(opcode))

        return code

    def find_space(self, code, size):
        filler = ["\xcc", "\x40"]
        for ftype in filler:
            pos = bnry.search.bytes(code, ftype * size)
            if pos != 0:
                return pos + constants.code_section_base
        # si t-odo falla lo ponemos al final
        return len(code) + constants.code_section_base



def is_switch(self, inst):
    if is_jumper(inst):
        return True
    return False
