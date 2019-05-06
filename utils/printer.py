


def bytearray(barray, size = 64):
    cycles = len(barray) // size
    for i in xrange(cycles):
        s = ""
        for a in xrange(size):
            s += "%02x " % ord(barray[i*size+a])
        print s

    rest = len(barray) % size
    s = ""
    for i in xrange(rest):
        s += "%02x " % ord(barray[cycles * size + i])
    print s
    return True