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
    print(hex(rec.r_id),rec.size,rec.Icao,rec.latitude,rec.longtitude,rec.altitude,rec.airportID)
    
airports = []
for subs in BGLStructure.sections[0].subsectionData:
    for rec in subs.records:
        airports += [rec]
    
a_numb = 0
for apt in airports:
    toPrint = '['+str(a_numb) + ']'+' '+ str(apt.getICAO())+' '+str(apt.name)+' '+str(apt.latitude)+' '+str(apt.longtitude)+' '+str(apt.altitude)
    print(toPrint)
    a_numb += 1    

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

