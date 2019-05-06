
class INST():
    def __init__(self, _inst):
        self.rva = _inst.address
        self.size = _inst.size
        self.bytes = _inst.bytes
        self.mnemonic = _inst.mnemonic
        self.op_str = _inst.op_str
        # self.id = _inst.id

class TABLE():
    def __init__(self):
        self.rva = 0
        self.pointer = 0
