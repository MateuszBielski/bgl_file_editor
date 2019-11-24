import bglTested
from struct import unpack
#~ from copy import copy
lat = float(input('szerokość geograficzna:'))
lon = float(input('długość geograficzna:'))

fileName_0 = bglTested.PathCreate(lat,lon)
fileName_ext = ".bgl"
fileName = fileName_0+fileName_ext
fileNameCopy = fileName_0+'_bak'+fileName_ext

question = 'czy pracujemy nad plikiem '+fileName+' ? (t/n)'
decision = input(question)
if decision == 'n':
    exit()

fileSource = open(fileName,"rb")
rawData = fileSource.read()
fileSource.close()

fileCopy = open(fileNameCopy,"wb")
fileCopy.write(rawData)
fileCopy.close()

copyRawData = bytearray(rawData)
airportSegments = []

i = 0
for a_seg in bglTested.FindAirportSegments(bglTested.parse(rawData)):
    airportSegments.append(a_seg)
    entity = a_seg.owner_entity
    subsection = entity.owner_subsection
    coords = bglTested.GetMeanCoordinates(a_seg.CalculateFinalCoordinates())
    print('[',i,']',subsection.nr_id,entity.nr_id,a_seg.altitude[0],coords[0],coords[1])
    i += 1

inp = None
while inp != 'q': 
    inp = input('którą wysokość zmieniamy (q - koniec):')
    if inp == 'q':
        break
    inp = int(inp)
    if inp < len(airportSegments):
        changeAltitude = float(input("zmiana wysokości o:"))
    bglTested.AddValueToAltitude(changeAltitude,copyRawData,airportSegments[inp])
    print('nowa wysokość:',airportSegments[inp].altitude[0]+changeAltitude)

newFile = open(fileName,"wb")
newFile.write(copyRawData)
newFile.close()



