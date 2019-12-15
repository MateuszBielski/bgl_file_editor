from struct import unpack,pack
from bglSectionClass import Section
from bglAirportClasses_Functions import AirportSection
from bglIlsClass import IlsSection

posNumberOfSections = 0x14
posSectionData = 0x38
posNumberOfSubsections = posSectionData + 0x08
posStartOfFirstSubsection = posSectionData + 0x0C

class Offset:
    val = 0
    
class BGLStructue:
    def __init__(self):
        self.status = True
        self.numberOfSubsections = 0
        self.subsectionsDataOffsets = []
        self.subsections = []
        self.subsectionData = []
        self.allSegments = []
        self.SelectClosestAirportTo = None
        self.numberOfSections = 0
    def getSectionIds(self):
        return [sec.kindOfSection for sec in self.sections ]
        
class VectorTerrainDbSection(Section):
    def readSubsectionDataFrom(self,rData,offset,i,bglStructure):#bglStructure - potrzebne np dla Airport
        subsectionData = SubsectionData()
        subsectionData.owner_structure = bglStructure
        subsectionData.nr_id = i
        subsectionData.qmid = unpack('I',rData[offset + 4 : offset + 8])[0]
        subsectionData.boundingCoordinates = GetBoundingCoordinates(subsectionData.qmid)
        subsectionData.numberOfEntities = unpack('I',rData[offset + 12 : offset + 12 + 4])[0]
        dataSize = unpack('I',rData[offset + 16 : offset + 16 + 4])[0]
        subsectionData.dataSize = dataSize
        offset += 32
        subsectionData.startSignature = offset
        #~ print(str(num),'\t','start signature ',hex(offset))
        end = offset + dataSize
        read = 1
        countGUID = 0
        signatures = []
        while read:
            #~ print(countGUID,'\t',getGUID(rawData[offset: offset + 16]))
            signat = Signature()
            signat.address = offset
            signat.name = getGUID(rData[offset: offset + 16])
            countGUID += 1
            offset += 16
            sizeAdditionalData = unpack('I',rData[offset :offset + 4])[0]
            offset0 = offset + 4
            offset = offset0 + sizeAdditionalData
            dataToRead = bytearray(rData[offset0:offset])
            for i in range(len(dataToRead)%4):
                dataToRead.append(0x0)
            if len(dataToRead)%4 == 0:
                numbIntegers = int(len(dataToRead)/4)
                signat.additionalData = unpack('I'*numbIntegers,dataToRead)
                #~ for i in range(numbIntegers):
                    #~ print(additionalData[i])
            else:
                print('nieprawidłowo addData po sygnaturach, adres:',offset0)
            if offset >= end:
                read = 0
            #~ signatures.append(signat)
            signatures += [signat]
        subsectionData.signatures =  signatures   
        subsectionData.offsetStartEntities = offset
        subsectionData.numberOfSignatures = countGUID

        offOb = Offset()
        offOb.val = offset
        subsectionData.entities = [Entity(rData,offOb,i,subsectionData) for i in range(subsectionData.numberOfEntities)]
        return subsectionData
    def SelectClosestAirportTo(self,coordinates):
        result = None
        yb,xb = coordinates #lat, lon
        d_min = 259200 # przykładowa duża wartość
        for ap in FindAirportSegments(self):
            xa,ya = GetMeanCoordinates(ap.CalculateFinalCoordinates())
            #~ print(xa,ya)
            d = (xb - xa)**2 + (yb - ya)**2
            if d < d_min:
                d_min = d
                result = ap
        #~ print('wybrano',GetMeanCoordinates(result.CalculateFinalCoordinates()))
        #~ print('w porównaniu do',
        return result

class SubsectionData:
    def __init__(self):
        self.nr_id = -1
        self.qmid = 0
        self.boundingCoordinates = (0,0,0,0)
        self.numberOfEntities = 0
        self.dataSize = 0
        self.signatures = []
        self.entities = []
        self.startSignature = 0x0
        self.offsetStartEntities = 0x0
        self.numberOfSignatures = 0 
        self.owner_structure = None
        
class Signature:
    def __init__(self):
        self.address = 0x0
        self.name = 'no signature'
        self.additionalData = []

class Entity:
    def __init__(self,rawData,offOb,nr_id,owner_subsection):#,subsectionData
        self.nr_id = nr_id
        self.owner_subsection = owner_subsection
        entity_u = unpack('I'*2+'H',rawData[offOb.val:offOb.val + 10])
        self.numberOfSegments = entity_u[0]
        self.segmentsType = entity_u[1]
        self.numberOfSignaturesOffsets = entity_u[2]
        offOb.val += 10
        self.signaturesOffsets = unpack('I'*entity_u[2],rawData[offOb.val:offOb.val + 4*entity_u[2]])
        offOb.val += 4*entity_u[2]
        self.segments = [Segment(rawData,offOb,self,j) for j in range(entity_u[0])]

class Segment:
    def __init__(self,rawData,offOb,owner_entity,nr_id):
        self.maskRoot = None
        self.coordinatesCalculated = None
        self.dataBuffer = None
        self.owner_entity = owner_entity
        self.nr_id = nr_id
        self.altitude = []
        owner_entity.owner_subsection.owner_structure.allSegments += [self]
        try:
            segment_u = unpack('I'+'B'*2,rawData[offOb.val:offOb.val + 6])
        except:
            print('except at offset: ',offOb.val)
        else:
            offOb.val += 6
            processBufferData(self,rawData,offOb,segment_u)
            N = getNvalue(segment_u[1],segment_u[0])
            if N > 0:
                self.altitudeAddress = offOb.val
                self.altitude = unpack('f'*N,rawData[offOb.val:offOb.val + 4*N])
                    
                #~ for k in range(N):
                    #~ print('altitude',altitude[k])
                offOb.val += 4*N
            self.numberOfPoints = segment_u[0]
            self.altitudeInfo = segment_u[1]
            self.method = segment_u[2]
    def CalculateRawCoordinates(self):
        if self.method == 1:
            print('method 1')
            return (0,0)
        return CalculateRawCoordinates(self.maskRoot,self.dataBuffer,self.numberOfPoints)
    def CalculateFinalCoordinates(self):
        rawCoordinates = self.CalculateRawCoordinates()
        boundingCoordinates = self.owner_entity.owner_subsection.boundingCoordinates
        return [GetFinalCoordinatesFrom(rawCoordinates[i],rawCoordinates[i+1],boundingCoordinates) for i in range(0,len(rawCoordinates),2)]
    def setAltitude(self,destValue,rDataCopy):
        #~ newAltitudes = [*segment.altitude]
        adr = self.altitudeAddress
        for alt in self.altitude:
            rDataCopy[adr : adr + 4] = pack('f',destValue)
            adr += 4

def parse(rawData):
    bglStructure = BGLStructue()
    bglStructure.numberOfSections = unpack('I',rawData[posNumberOfSections:posNumberOfSections+4])[0]
    SectionDataOffsets = [posSectionData + i*20 for i in range(bglStructure.numberOfSections)]
    bglStructure.sections = [createSection(rawData,adr,bglStructure) for adr in SectionDataOffsets]
    
    #poniższe dotyczy pierwszej sekcji
    bglStructure.SelectClosestAirportTo = bglStructure.sections[0].SelectClosestAirportTo
    bglStructure.numberOfSubsections = bglStructure.sections[0].numberOfSubsections
    bglStructure.subsectionData = bglStructure.sections[0].subsectionData
    return bglStructure

def createSection(rData,startOfSectionData,bglStructure):
    section = Section()
    sectionData_u = unpack('I'*5,rData[startOfSectionData:startOfSectionData+20])
    #~ sec_id,val_subsection_size,numberOfSubsections,subs_offset,subs_size = 
    startOfFirstSubsection = sectionData_u[3]
    kindOfSection = sectionData_u[0]
    
    if kindOfSection == 0x65:
        section = VectorTerrainDbSection()
    if kindOfSection == 0x3:
        section  = AirportSection()
    if kindOfSection == 0x13:
        section = IlsSection()

    section.kindOfSection = kindOfSection
    section.numberOfSubsections = sectionData_u[2]
    subsectionSize = ((sectionData_u[1] & 0x10000) | 0x40000) >> 0x0E
    if subsectionSize == 16:
        subsections = [unpack('I'*4,rData[startOfFirstSubsection + i * 16:startOfFirstSubsection + (i+1) * 16]) for i in range(sectionData_u[2])]
    section.subsections = subsections
    section.subsectionsDataOffsets = [subsections[i][2] for i in range(len(subsections))]
    section.subsectionData = [section.readSubsectionDataFrom(rData,section.subsectionsDataOffsets[i],i,bglStructure) for i in range(sectionData_u[2])]#przenieść subsectionsDataOffsets[i] do funkcji
    return section       
    
def getNumberOfSubsections(rawData):
    return unpack('I',rawData[posNumberOfSubsections:posNumberOfSubsections + 4])[0]
    
def getSubsections(rawData): #musi być do testów
    numberOfSubsections = getNumberOfSubsections(rawData)
    startOfFirstSubsection = unpack('I',rawData[posStartOfFirstSubsection:posStartOfFirstSubsection + 4])[0]
    return [unpack('I'*4,rawData[startOfFirstSubsection + i * 16:startOfFirstSubsection + (i+1) * 16]) for i in range(numberOfSubsections)]

def getAdresToSubsectionData(numberOfSubsection,subsections):
    return subsections[numberOfSubsection][2]

def processBufferData(segment,rawData,offOb,segmentInfo):
    maskRoot = 0x0
    if segmentInfo[2] == 2:
        maskRoot = unpack('B',rawData[offOb.val:offOb.val + 1])[0]
        numberOfBytes = (maskRoot*segmentInfo[0]*2 + 7) >> 3
        offOb.val += 1
        offsetEnd = offOb.val + numberOfBytes
    if segmentInfo[2] == 1:
        segmentData = unpack('I'*2+'i'*2+'I',rawData[offOb.val:offOb.val + 5 * 4])
        #~ print('First Longitude Data',segmentData[0])
        #~ print('First Latitude Data',segmentData[1])
        #~ print('LongitudeData Increment',segmentData[2])
        #~ print('LatitudeData Increment',segmentData[3])
        numberOfBytes = segmentData[4]
        offOb.val += 20
        offsetEnd = offOb.val + numberOfBytes
    segment.maskRoot = maskRoot
    segment.dataBuffer = rawData[offOb.val:offsetEnd]
    #~ if segmentInfo[2] == 2:
        #~ segment.coordinatesCalculated = CalculateRawCoordinates(maskRoot,segment.dataBuffer,segmentInfo[0])
    offOb.val = offsetEnd
    
    
def getGUID(bc):
    bc_u = unpack('I'+'H'*2,bc[:8])
    res = '{:X}'.format(bc_u[0])
    if len(res) < 8:
        res = '0'+res
    result = res + '-'
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
    #~ return 1
        
def CalculateRawCoordinates(maskRoot,dataBuffer,nbPoints):
    positionInPair = 0
    pairIndex = 0
    shiftValue = 0
    offset = 0
    listOfValues = {}
    nbBytesLeftToRead = ((maskRoot * nbPoints) * 2 + 7) >> 3;
    if nbBytesLeftToRead != len(dataBuffer):
        print(nbBytesLeftToRead,len(dataBuffer),maskRoot,nbPoints)
        
    mask = (1 << maskRoot) - 1
    if nbBytesLeftToRead > 3:
        valueFromFile = unpack('I',dataBuffer[offset:offset + 4])[0]
        nbBytesLeftToRead -= 4
        offset +=4 
    else:
        data = bytearray(dataBuffer[offset:])
        for i in range(4 - nbBytesLeftToRead):
            data.append(0x0)
        valueFromFile = unpack('I',data)[0]
        nbBytesLeftToRead = 0 
    while pairIndex < nbPoints:
        if shiftValue < 0:
            
            result = (valueFromFile << (-shiftValue)) & mask

            result += listOfValues[pairIndex * 2 + positionInPair];        
            listOfValues[pairIndex * 2 + positionInPair] = result;
        else:
            result = (valueFromFile >> shiftValue) & mask
            listOfValues[pairIndex * 2 + positionInPair] = result;

        if maskRoot + shiftValue >= 32:
            if nbBytesLeftToRead > 3:
                valueFromFile = unpack('I',dataBuffer[offset:offset + 4])[0]
                nbBytesLeftToRead -= 4
                offset +=4 
            else:
                data = bytearray(dataBuffer[offset:])
                for i in range(4 - nbBytesLeftToRead):
                    data.append(0x0)
                valueFromFile = unpack('I',data)[0]
                nbBytesLeftToRead = 0
            shiftValue -= 32
        else:
            shiftValue += maskRoot;
            positionInPair += 1;

        if positionInPair == 2:
            pairIndex += 1 
            positionInPair = 0
    return (listOfValues)



    

def AddValueToAltitude(deltaValue,rDataCopy,segment):
    #~ nbAltitudes = len(segment.altitude)
    newAltitudes = [*segment.altitude]
    adr = segment.altitudeAddress
    for alt in newAltitudes:
        rDataCopy[adr : adr + 4] = pack('f',alt + deltaValue)
        adr += 4
        
def FindAirportSegments(bglStructure):
    result_segments = []
    for ent in FindAirportEntities(bglStructure):
        for seg in ent.segments:
            if len(seg.altitude):
                #~ result_segments.append(seg)
                result_segments += [seg]
    return result_segments

def FindAirportEntities(bglStructure):
    result_entities = []
    i_subs = 0
    
    for subs in bglStructure.subsectionData:
        i_ent = 0
        #~ airportSignatures = []
        entitiesCopy = [*subs.entities]
        for sign in subs.signatures:
            if sign.name == '359C73E8-06BE-4FB2-ABCB-EC942F7761D0' :
                adrRelative = sign.address - subs.startSignature
                foundEntity = False
                for ent in entitiesCopy:
                    for sigOf in ent.signaturesOffsets:
                        if sigOf == adrRelative:
                            result_entities +=[ent]
                            foundEntity = True
                            break
                    if foundEntity:
                        entitiesCopy.remove(ent) 
                        #~ break
            
    return result_entities
def FindSceneryFolderAndFilename(latitude,longtitude):
    horiz = 180 + longtitude
    vert = 90 - latitude
    x_fold = 12 * horiz /360
    y_fold = 8 * vert/180
    x_file = 12*8 * horiz /360
    y_file = 8*8 * vert/180
    return ('%.02d'%(x_fold)+'%.02d'%(y_fold),'%.02d'%(x_file)+'%.02d'%(y_file))
def GetCenterCoordinatesFromFileSignature(signature):
    x_file,y_file = float(signature[:2]),float(signature[2:])
    horiz = (x_file + 0.5) * 360/(12*8)
    vert = (y_file + 0.5) * 180/(8*8)
    lon = horiz - 180
    lat = 90 - vert 
    return (lat,lon)
def PathCreate(latitude,longtitude):
    names = FindSceneryFolderAndFilename(latitude,longtitude)
    return names[0]+'/scenery/cvx'+names[1]
    
def CreatePathFromCoordinates(latitude,longtitude,type_of_file):
    names = FindSceneryFolderAndFilename(latitude,longtitude)
    if type_of_file == 'cvx':
        return names[0]+'/scenery/cvx'+names[1]
    if type_of_file == 'apx':
        return names[0]+'/scenery/APX'+names[1]+'0'
        
def CreatePathFromSignature(signature,type_of_file):
    
    names = FindSceneryFolderAndFilename(*GetCenterCoordinatesFromFileSignature(signature))
    if type_of_file == 'cvx':
        return names[0]+'/scenery/cvx'+names[1]
    if type_of_file == 'apx':
        return names[0]+'/scenery/APX'+names[1]+'0'
    
def CalcQmidFromDwords(dwordA, dwordB):
    u = 0
    v = 0
    #~ level = 0
    cnt = 0x1F
    workDwordA = dwordA
    workDwordB = dwordB
    while (cnt > 0 and (workDwordB & 0x80000000) == 0):
        workDwordB <<= 2;
        workDwordB += (workDwordA & 0xC0000000) >> 30

        workDwordA += workDwordA
        workDwordA += workDwordA
        cnt -= 1

    workDwordB &= 0x7FFFFFFF
    level = cnt
    while (cnt >= 0):
        if ((workDwordB & 0x80000000) != 0):
            v += (1 << cnt)

        if ((workDwordB & 0x40000000) != 0):
            u += (1 << cnt)

        workDwordB <<= 2
        workDwordB += (workDwordA & 0xC0000000) >> 30
        workDwordA += workDwordA
        workDwordA += workDwordA
        cnt -= 1
    return (u,v,level)
def GetBoundingCoordinates(boundingValue):
    #~ list = new List<double>();
    shiftValue = 15;
    work = boundingValue;
    latitudeData = 0;
    longitudeData = 0;

    while (work < 0x80000000 and shiftValue >= 0):
        shiftValue -= 1
        work *= 4
        
    work &= 0x7FFFFFFF  #Remove negative flag, if any
    powerOfTwo = shiftValue

    while shiftValue >= 0:
        if ((work & 0x80000000) != 0):
            latitudeData += (1 << shiftValue)

        if ((work & 0x40000000) != 0):
            longitudeData += (1 << shiftValue);
        
        work *= 4
        shiftValue -= 1

    # factor = 1.0 / (2^i)
    factor = 1.0 / (1 << powerOfTwo)

    # Calc bounding coordinates
    minLatitudeDeg = 90.0 - ((latitudeData + 1.0) * factor * 360.0)
    maxLatitudeDeg = 90.0 - (latitudeData * factor * 360.0)
    minLongitude = (longitudeData * factor * 480.0) - 180.0
    maxLongitude = ((longitudeData + 1.0) * factor * 480.0) - 180.0
    
    return (minLatitudeDeg,maxLatitudeDeg,minLongitude,maxLongitude)
    
def GetFinalCoordinatesFrom(longitude_related_Value,latitude_related_Value,boundingCoordinates):
    MinLatitudeDeg, MaxLatitudeDeg, MinLongitudeDeg, MaxLongitudeDeg = boundingCoordinates
    
    deltaLongFactor = (MaxLongitudeDeg - MinLongitudeDeg) / 0x8000
    deltaLatFactor = (MaxLatitudeDeg - MinLatitudeDeg) / 0x8000
    
    LongitudeDeg = MinLongitudeDeg + (longitude_related_Value * deltaLongFactor)
    LatitudeDeg = MinLatitudeDeg + (latitude_related_Value * deltaLatFactor)
    return (LongitudeDeg,LatitudeDeg)

def SectionType(rawData):
    return unpack('I',rawData[posSectionData:posSectionData + 4])[0]

def GetMeanCoordinates(coordinates):
    a = b = 0
    l = len(coordinates)
    for p in coordinates:
        pa,pb = p
        a += pa
        b += pb
    return (a/l,b/l)
    
"""
 Algorytm na obliczenie pierwiastka z liczby X wybranej z przykładowego przedziału od 10 do 100 wyglądałby tak:
1. Pomnóż swoją liczbę X przez magiczne 0.135
2. Do tego dodaj 7.4
3. Podziel przez 2 i zapamiętaj wynik (to jest pierwsze przybliżenie)
4. Podziel pierwiastkowany X przez liczbę uzyskaną w p.3
5. Dodaj do tego liczbę z p.3
6. Podziel przez 2 (to jest drugie przybliżenie)
Tak obliczony pierwiastek wystarczył by do określenia współrzędnej piksela, a użyto do tego 1 mnożenie, 1 dzielenie, 2 dodawania i 2 przesunięcia bitowe (dzielenie przez dwa). Jeśli potrzeba dokładniej, to dochodzi kolejne powtórzenie, jeśli dla szerszego zakresu, to inne magiczna liczby w punkcie 1 i 2 :)
"""
