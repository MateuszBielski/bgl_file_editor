import bglTested

#~ fileAPX = open("APX58280.bgl","rb")
fileAPX = open("APX92470.bgl","rb")
rawData = fileAPX.read()
fileAPX.close()

bglStructure = bglTested.parse(rawData)
print('number of subsections',bglStructure.numberOfSubsections)
airports = []
for subs in bglStructure.subsectionData:
    for rec in subs.records:
        airports += [rec]


for apt in airports:
    toPrint = (apt.getICAO(),apt.name,apt.latitude,apt.longtitude, apt.altitude,)
    print(toPrint)
