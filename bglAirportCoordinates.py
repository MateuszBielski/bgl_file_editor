import bglTested
from struct import unpack

fileName = "cvx9247.bgl"

fileCVX = open(fileName,"rb")
rawData = fileCVX.read()
fileCVX.close()

BGLStructure = bglTested.parse(rawData)
segments =  BGLStructure.subsectionData[248].entities[49].segments
for seg in segments:
    print( 'altitude',seg.altitude)
    print('final coordinates')
    finCoord = seg.CalculateFinalCoordinates()
    for fC in finCoord:
        print(fC[0],fC[1])




"""


Use a bytearray:

>>> frame = bytearray()
>>> frame.append(0xA2)
>>> frame.append(0x01)
>>> frame.append(0x02)
>>> frame.append(0x03)
>>> frame.append(0x04)
>>> frame
bytearray(b'\xa2\x01\x02\x03\x04')

or, using your code but fixing the errors:

frame = b""
frame += b'\xA2' 
frame += b'\x01' 
frame += b'\x02' 
frame += b'\x03'
frame += b'\x04'

"""

