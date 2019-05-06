
def bytes(code, signature):
    result = code.find(signature)
    if result == -1:
        return 0
    return result
