import bglTested
from struct import unpack

fileName = "cvx5828.bgl"

fileCVX = open(fileName,"rb")
rawData = fileCVX.read()
fileCVX.close()

BGLStructure = bglTested.parse(rawData)

i = 0

segmentsWithAltitude = []
segmentsWithAltitudes = []
for seg in BGLStructure.allSegments:
    alt = seg.altitude
    if not len(alt):
        continue
    segmentsWithAltitude += [seg]
print('number of segments with altitude',len(segmentsWithAltitude))
    
for seg in segmentsWithAltitude:
    entity = seg.owner_entity
    subsection = entity.owner_subsection
    print(seg.altitude[0],subsection.nr_id,entity.nr_id)
    
# offsety szukanej sygnatury 46...
# 0x3132  25 subsekcja 2 ent HAMA
# 0x4597  35  4 ent HADM
# 0x8ace  65 HADC
# 0x1c64e 177 ent 17 - tu jest wysokość 2361.895263671875 czyli to jest HAAL 


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

