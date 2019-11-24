import bglTested
from struct import unpack

fileName = "APX58280.bgl"

fileAPX = open(fileName,"rb")
rawData = fileAPX.read()
fileAPX.close()

BGLStructure = bglTested.parse(rawData)

IlsSubsection = BGLStructure.sections[2].subsectionData[0]
print(IlsSubsection.numberOfRecords)

for rec in IlsSubsection.records:
    print(hex(rec.r_id),rec.size,rec.Icao,rec.latitude,rec.longtitude,rec.altitude)

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

