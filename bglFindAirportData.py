import bglTested
from struct import unpack

fileName = "cvx9247.bgl"

fileCVX = open(fileName,"rb")
rawData = fileCVX.read()
fileCVX.close()

BGLStructure = bglTested.parse(rawData)

airportLocalization = []

i_subs = 0
for subs in BGLStructure.subsectionData:
    i_sign = 0
    for sign in subs.signatures:
        if sign.name == '359C73E8-06BE-4FB2-ABCB-EC942F7761D0':
            airportLocalization.append(str(i_subs)+'_'+str(i_sign))
        i_sign += 1
    i_subs += 1

    
print(airportLocalization)





"""
wynik szukania:
1. '248_301' tego wpisu używa entity 43 (subsection248.txt:2775) altitude 257.8608093261719 bytes 19 
2. '254_99'  tego wpisu używa entity 166 (subsection254.txt:4896) altitude 382.52398681640625 bytes 19 



"""

