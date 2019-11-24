import bglTested
from struct import unpack

fileName = "cvx5828.bgl"

fileCVX = open(fileName,"rb")
rawData = fileCVX.read()
fileCVX.close()

BGLStructure = bglTested.parse(rawData)

#~ segment = BGLStructure.subsectionData[245].entities[1008].segments[0]
#~ maskRoot = segment.maskRoot
#~ dataBuffer = segment.dataBuffer
#~ nbPoints = segment.numberOfPoints

signatures = {}

signTypes = {
'91CB4A9B-9398-48E6-81DA-70AEA3295914':'Parks',
'1B6A15BB-05FB-4401-A8D1-BB520E84904C':'Water Polygons Slope',
'CEB07D86-3605-44BE-B48A-97F8D01B74DE':'Water Polygons Slope',
'359C73E8-06BE-4FB2-ABCB-EC942F7761D0':'Airport Bounds',
'33239EB4-D2B8-46F5-98AB-47B3D0922E2A':'Railways',
'EA0C44F7-01DE-4D10-97EB-FB5510EB7B72':'Water Polygons (GPS)',
'54B91ED8-BC02-41B7-8C3B-2B8449FF85EC':'Freeway Traffic Roads',
'560FA8E6-723D-407D-B730-AE08039102A5':'Roads',
'C7ACE4AE-871D-4938-8BDC-BB29C4BBF4E3':'Utilities',
'0CBC8FAD-DF73-40A1-AD2B-FE62F8004F6F':'Shorelines',
'956A42AD-EC8A-41BE-B7CB-C68B5FF1727E':'Water Polygons',
'46BFB38D-CE68-418E-8112-FEBA17428ACE':'Airport Bounds Addis Abeba'}
     

i_subs = 0
for subs in BGLStructure.subsectionData:
    i_sign = 0
    for sign in subs.signatures:
        signatures[' '+str(i_subs)+'_'+str(i_sign)] = sign.name
        i_sign += 1
    i_subs += 1

    
signatures_l = sorted(signatures.values())
signatures_d = {}
for sign in signatures_l:
    if sign in signatures_d:
        signatures_d[sign] += 1
    else:
        signatures_d[sign] = 1
print(fileName)
for key,sign in signatures_d.items():
    try:
        print(key,sign,'\t',signTypes[key])
    except:
        print(key,sign)





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

