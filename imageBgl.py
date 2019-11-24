import numpy as np
from struct import unpack
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

#~ path = "/media/mateusz/New Volume/Program Files/Microsoft Games/Microsoft Flight Simulator X/Scenery/0501/scenery/cvx4308.bgl"
#~ A = plt.imread(path)
#~ fig, ax = plt.subplots()
#~ ax.imshow(A,cmap=cm.gray)
#~ ax.axis('off')

#~ plt.show()

fileCVX = open("cvx5828.bgl","rb")
rawData = fileCVX.read()
fileCVX.close()
#~ start
posNumberOfSections = 0x14
posSectionData = 0x38
posNumberOfSubsections = posSectionData + 0x08
posStartOfFirstSubsection = posSectionData + 0x0C
#~ numberOfSections = unpack('I',rawData[20:24])
numberOfSections = unpack('I',rawData[posNumberOfSections:posNumberOfSections + 4])
print("number of sections: ",numberOfSections[0])
sectionType = unpack('I',rawData[posSectionData:posSectionData + 4])[0]
print("section type",hex(sectionType))
numberOfSubsections = unpack('I',rawData[posNumberOfSubsections:posNumberOfSubsections + 4])[0]
print("number of sub sections: ",numberOfSubsections)
startOfFirstSubsection = unpack('I',rawData[posStartOfFirstSubsection:posStartOfFirstSubsection + 4])[0]
print('startOfFirstSubsection',hex(startOfFirstSubsection))
subsections = [unpack('I'*4,rawData[startOfFirstSubsection + i * 16:startOfFirstSubsection + (i+1) * 16]) for i in range(numberOfSubsections)]
subsectionsDataOffsets = [subsections[i][2] for i in range(len(subsections))]

def printSubsectionDataHeader(subsectionDataHeader,numb):
    print("subsectionDataHeader nr ",numb)
    print("identifier",subsectionDataHeader[0])
    print("QMID square",subsectionDataHeader[1])
    print("add to cells",subsectionDataHeader[2])
    print("Number of entities",subsectionDataHeader[3])
    print("Number of bytes in the attributes buffer",subsectionDataHeader[4])
    print("Number of attribute offsets used in that subsection",subsectionDataHeader[5])
    print("Number of points used in that subsection",subsectionDataHeader[6])
    print("Number of points,  that have a different altitude value",subsectionDataHeader[7])
    
def getGUID(bc):
    bc_u = unpack('I'+'H'*2,bc[:8])
    result = '{:X}'.format(bc_u[0]) + '-'
    for i in [1,2]:
        res = '{:X}'.format(bc_u[i])
        if len(res) < 4:
            res = '0'+res
        result += res + '-'
    result += bc[8:10].hex().upper() + '-'
    result += bc[10:].hex().upper()
    return result
    
def getNvalue(altInf,numOfPoints):
    if altInf == 0:
        return 0
    if altInf == 1:
        return numOfPoints
    if altInf == 2:
        return 1

def processBufferData(offset,segmentInfo):
    if segmentInfo[2] == 2:
        maskRoot = unpack('B',rawData[offset:offset + 1])[0]
        numberOfBytes = (maskRoot*segmentInfo[0]*2 + 7) >> 3
        offset += 1
        offsetEnd = offset + numberOfBytes
    if segmentInfo[2] == 1:
        segmentData = unpack('I'*2+'i'*2+'I',rawData[offset:offset + 5 * 4])
        print('First Longitude Data',segmentData[0])
        print('First Latitude Data',segmentData[1])
        print('LongitudeData Increment',segmentData[2])
        print('LatitudeData Increment',segmentData[3])
        numberOfBytes = segmentData[4]
        offset += 20
        offsetEnd = offset + numberOfBytes 
    print('numberOfBytes ',numberOfBytes)
    print(rawData[offset:offsetEnd].hex().upper())
    return offsetEnd
        
def printEntities(offset,totalNumber):
    print('number of entities ',totalNumber)
    for i in range(totalNumber):
        entity = unpack('I'*2+'H',rawData[offset:offset + 10])
        numberOfSegments = entity[0]
        segmentsType = entity[1]
        numberOfSignaturesOffsets = entity[2]
        offset += 10
        print(i,'entity')
        print('numberOfSegments',numberOfSegments)
        print('segmentsType',segmentsType)
        print('numberOfSignaturesOffsets',numberOfSignaturesOffsets)
        signaturesOffsets = unpack('I'*numberOfSignaturesOffsets,rawData[offset:offset + 4*numberOfSignaturesOffsets])
        for j in range(numberOfSignaturesOffsets):#
            print(hex(signaturesOffsets[j]))
        offset += 4*numberOfSignaturesOffsets
        for j in range(numberOfSegments):
            print('segment ',j)
            segment = unpack('I'+'B'*2,rawData[offset:offset + 6])
            print('number of points',segment[0])
            print('altitude info',segment[1])
            print('method',segment[2])
            offset += 6
            offset = processBufferData(offset,segment)
            
            N = getNvalue(segment[1],segment[0])
            if N > 0:
                altitude = unpack('f'*N,rawData[offset:offset + 4*N])
                for k in range(N):
                    print('altitude',altitude[k])
                offset += 4*N
            print('end of entity: ',hex(offset))
        
    
def printSubsectionDatafrom(offset,num):
    numberOfEntities = unpack('I',rawData[offset + 12 : offset + 12 + 4])[0]
    dataSize = unpack('I',rawData[offset + 16 : offset + 16 + 4])[0]
    offset += 32
    print(str(num),'\t','start signature ',hex(offset))
    end = offset + dataSize
    read = 1
    countGUID = 0
    while read:
        print(countGUID,'\t',hex(offset),'\t',getGUID(rawData[offset: offset + 16]))
        countGUID += 1
        offset += 16
        #~ numbIntegers = int(unpack('I',rawData[offset :offset + 4])[0] / 4)
        #~ offset0 = offset + 4 
        #~ offset = offset0 + numbIntegers*4
        #~ if numbIntegers:
            #~ additionalData = unpack('I'*numbIntegers,rawData[offset0:offset])
            #~ for i in range(numbIntegers):
                #~ print(additionalData[i])
        sizeAdditionalData = unpack('I',rawData[offset :offset + 4])[0]
        offset0 = offset + 4
        offset = offset0 + sizeAdditionalData
        dataToRead = bytearray(rawData[offset0:offset])
        for i in range(len(dataToRead)%4):
            dataToRead.append(0x0)
        if len(dataToRead)%4 == 0:
            numbIntegers = int(len(dataToRead)/4)
            additionalData = unpack('I'*numbIntegers,dataToRead)
            for i in range(numbIntegers):
                print(additionalData[i])
        else:
            print('nieprawidłowo addData po sygnaturach, adres:',offset0)
        if offset >= end:
            read = 0
    print('offset, end, ',hex(offset),hex(end))
    printEntities(offset,numberOfEntities)
    

def printAllSubsetionDataHeader():
    for i in range(numberOfSubsections):
        #~ print("daneSubsekcji,ileEntity,daneBufora",subsections[i][3],"\t",subsectionDataHeader[i][3],"\t",subsectionDataHeader[i][4])
        text = str(i)+"\t"+str(subsections[i][3])
        for j in range(3,8):
            text += "\t" + str(subsectionDataHeader[i][j])
        text += "\t" + hex(subsectionsDataOffsets[i])
        print(text)
    

subsectionDataHeader = [unpack('I'*8,rawData[subsectionsDataOffsets[i] : subsectionsDataOffsets[i] + 4*8]) for i in range(numberOfSubsections)]
    #~ print(subsections[i][3],"\t\t",subsectionDataHeader[i][3],"\t\t",subsectionDataHeader[i][4],"\t\t",subsectionDataHeader[i][5],"\t\t",subsectionDataHeader[i][6],"\t\t",subsectionDataHeader[i][7])
#~ vectorTypes = [rawData[subsectionsDataOffsets[i] + 32 :subsectionsDataOffsets[i] + 32 +16] for i in range(numberOfSubsections)]
vectorTypes = [getGUID(rawData[subsectionsDataOffsets[i] + 32 :subsectionsDataOffsets[i] + 32 + 16]) for i in range(numberOfSubsections)]

#~ for i in range(3):
    #~ printSubsectionDataHeader(subsectionDataHeader[i],i)
#~ for i in range(numberOfSubsections):

#~ printAllSubsetionDataHeader()
for i in range(177,178):
    printSubsectionDatafrom(subsectionsDataOffsets[i],i)
