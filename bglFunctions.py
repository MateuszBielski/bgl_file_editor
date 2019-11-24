def LatFromDword(var):
    return 90.0 - var * (180.0 / (2 * 0x10000000))
def LonFromDword(var):
    return var * (360.0 / (3 * 0x10000000)) - 180.0
    
def getIcaoCode(rawICAO):
    print(bin(rawICAO))
    value = rawICAO >> 5
    codedChars = []
    
    while (value >= 0):
        if (value < 38):
            oneCodedChar = value
            value = -1
        else:
            oneCodedChar = value % 38
            value = (value - oneCodedChar) / 38
        codedChars += [int(oneCodedChar)]
    codedChars.reverse()
    result = ''
    for codedChar in codedChars:
        if codedChar == 0:
            output =' '
        elif codedChar > 1 and codedChar < 12:
            output = chr(ord('0') + codedChar - 2)
        else:
            output = chr(ord('A') + codedChar - 12)
        result += output
    return result
