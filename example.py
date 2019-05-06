from utils import constants
from lief import PE
from engine import run




def main():

    # path = "C:\Users\GG\Desktop/spacesniffer.exe"
    # path = "C:\Users\GG\Desktop/keygenme2.exe"
    # path = 'C:\Users\GG\Desktop/Crackme-4-switch-x86.exe'
    # path = 'C:\Users\GG\Desktop/Crackme-4.exe'
    path = 'C:\Users\GG\Desktop/Crackme-4_minimalswitch.exe'


    binary = PE.parse(path)
    text_section = binary.get_section('.text')
    code = "".join(map(chr, text_section.content))

    relocs = []
    for _rlcs in binary.relocations:
        for _rlc in _rlcs.entries:
            if _rlc.type == constants.HIGHLOW:
                relocs.append(_rlc.address)

    run(code, relocs, True)


    return True

if __name__ == "__main__":
    main()
