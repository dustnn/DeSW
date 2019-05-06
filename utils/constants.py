dword_size = 4
byte_size = 1


module_base = 0x400000
code_section_base = 0x1000

reg_list = ['eax','ebx','ecx','edx','esp','ebp','esi','edi']
BCC = ["je", "jne", "js", "jns", "jp", "jnp", "jo", "jno", "jl", "jle", "jg",
       "jge", "jb", "jbe", "ja", "jae", "jcxz", "jecxz", "jrcxz", "loop", "loopne",
       "loope", "call", "lcall"]
END = ["ret", "retn", "retf", "iret", "int3"]
BNC = ["jmp", "jmpf", "ljmp"]

HIGHLOW = 3