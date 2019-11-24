from struct import unpack,pack
#~ import struct

class Offset:
    def __init__(self,val):
        self.val = val
class AirportSubrecord:
    def __init__(self):
        self.as_name = None
        self.as_id = None
        self.as_size = None
        self.address = 0x0
        self.dataToRead = None
    def setElevation(self,newAltitude,rData):
        pass
    def ReadData(self,rData):
        pass
    def GiveDataTo(self,record):
        pass

class AirportName(AirportSubrecord):
    def ReadData(self,rData):
        self.name = rData.decode('utf-8').rstrip('\x00')
        #~ print('Name subrecord',hex(self.as_id),self.as_size,self.name)
    def GiveDataTo(self,record):
        record.name = self.name
        
class AirportRunway(AirportSubrecord):
    def ReadData(self,rData):    
        surfaceType = None #H
        primaryRunwayNumber = None #B
        primaryRunwayDesignator = None  #B
        secondaryRunwayNumber = None #B
        secondaryRunwayDesignator = None #B
        icaoPrimIls = None #I
        icaoSeconIls = None #I
        rData = rData[0x14 - 6:0x2c - 6]
        #~ longtitude = None #I
        #~ latitude = None #I
        #~ elevation = None #I x 1000 m
        #~ length = None #f m
        #~ width = None #f m
        #~ heading = None #f deg 0x28
        self.longtitude,self.latitude,elevation,self.length,self.width,self.heading = unpack('IIIfff',rData)
        self.elevation = elevation/1000
        #~ print('runway elevation',elevation/1000,'heading',heading)
        
    def setElevation(self,newAltitude,rData):
        #~ print('runway setElevation address',hex(self.address + 0x1c))
        adr = self.address + 0x1c
        rData[adr:adr + 4] = pack('I',int(newAltitude*1000))

class AirportStart(AirportSubrecord):
    def ReadData(self,rData):
        start_u = unpack('<BBIIIf',rData)
        runwayNumber,runwayDesignator,longtitude,latitude,elevation,heading = unpack('<BBIIIf',rData)
        self.elevation = elevation/1000
        
    def setElevation(self,newAltitude,rData):
        #~ print('airport setElevation address',hex(self.address + 0x10))   
        adr = self.address + 0x10
        rData[adr:adr + 4] = pack('I',int(newAltitude*1000))
        
class AirportCom(AirportSubrecord):
    def ReadData(self,rData):
        com_u = unpack('I',rData[0x8 - 6:0x8 - 2])[0]
        name = rData[0x0c:].decode('utf-8')
        self.as_name = 'com'+str(com_u/1000000)+name
        
class AirportApproach(AirportSubrecord):
    def ReadData(self,rData):
        self.as_name = 'approach'
class Airport3B(AirportSubrecord):
    pass
class TaxiwayPoint(AirportSubrecord):
    def ReadData(self,rData):
        self.as_name = 'TaxiwayPoint'
class TaxiwayParking(AirportSubrecord):
    def ReadData(self,rData):
        self.as_name = 'TaxiwayParking'
class TaxiwayPath(AirportSubrecord):
    def ReadData(self,rData):
        self.as_name = 'TaxiwayPath'
class TaxiName(AirportSubrecord):
    def ReadData(self,rData):
        self.as_name = 'TaxiName'
class Apron(AirportSubrecord):
    def ReadData(self,rData):
        self.as_name = 'Apron'
class Approach(AirportSubrecord):
    def ReadData(self,rData):
        self.as_name = 'Approach'
class ApronEdgeLights(AirportSubrecord):
    def ReadData(self,rData):
        self.as_name = 'ApronEdgeLights'
class AirportRecord:
    
    def __init__(self,owner_subsection,i,offOb,rData):
        self.subrecords = []
        self.owner_subsection = owner_subsection
        self.nr_id = i
        self.name = None
        #~ print('offOb.val',hex(offOb.val))
        record_u = unpack('<HIBBBBBBIIIIIIII',rData[offOb.val:offOb.val+0x2c])# musi być znaczek < bo inaczej nie rozumie i żąda więcej bajtów
        self.ar_id = record_u[0]
        self.size = record_u[1]
        endOffset = offOb.val + self.size 
        self.longtitude = LonFromDword(record_u[8])
        self.latitude = LatFromDword(record_u[9])
        self.altitude = record_u[10]/1000
        self.altitudeAddress = offOb.val + 0x14
        self.icaoRaw = record_u[15]
        offOb.val += 0x38
        
        while offOb.val < endOffset:
            self.subrecords.append(readSubrecord(offOb,rData))
            #~ pass
        offOb.val = endOffset
        for subr in self.subrecords:
            subr.GiveDataTo(self)
        #~ print('altitude',self.altitude,'longitude',self.longitude,'latitude',self.latitude)
    def setAltitude(self,newAltitude,rData):
        adr = self.altitudeAddress
        rData[adr:adr + 4] = pack('I',int(newAltitude*1000))
        for subr in self.subrecords:
            #~ pass
            #~ print(subr.as_name)
            subr.setElevation(newAltitude,rData)
    def getICAO(self):
        return getIcaoCode(self.icaoRaw)
        
    
class SubsectionAirportData:
    records = []
    numberOfRecords = 0
    
def LatFromDword(var):
    return 90.0 - var * (180.0 / (2 * 0x10000000))
def LonFromDword(var):
    return var * (360.0 / (3 * 0x10000000)) - 180.0
    
def readAirportSubsectionDataFrom(rData,offset,i,bglStructure):
    offOb = Offset(offset)
    subsectionData = SubsectionAirportData()
    subsectionData.nr_id = i
    numberOfRecords = bglStructure.subsections[i][1]
    subsectionData.numberOfRecords = numberOfRecords
    subsectionData.records = [AirportRecord(subsectionData,i,offOb,rData) for i in range(numberOfRecords)]
    return subsectionData
    
def readSubrecord(offOb,rData):
    as_id,as_size = unpack('<HI',rData[offOb.val:offOb.val+6])
    endOffset = offOb.val + as_size
    #~ print('readSubrecord as_id',hex(as_id))
    dataForSubrecord = rData[offOb.val+6:endOffset]
    subrecord = AirportSubrecord()
    if as_id == 0x19:
        subrecord = AirportName()
    if as_id == 0x4:
        subrecord = AirportRunway()
    if as_id == 0x11:
        subrecord = AirportStart()
    if as_id == 0x12:
        subrecord = AirportCom()
    if as_id == 0x3b:
        subrecord = Airport3B()
    if as_id == 0x1a:
        subrecord = TaxiwayPoint()
    if as_id == 0x3d: 
        subrecord = TaxiwayParking()
    if as_id == 0x1c:
        subrecord = TaxiwayPath()
    if as_id == 0x1d:
        subrecord = TaxiName()
    if as_id == 0x37 or as_id == 0x30:
        subrecord = Apron()
    if as_id == 0x24:
        subrecord = Approach()
    if as_id == 0x31:
        subrecord = ApronEdgeLights()
    subrecord.address = offOb.val
    subrecord.as_id = as_id
    subrecord.as_size = as_size
    subrecord.ReadData(dataForSubrecord)
    offOb.val = endOffset
    return subrecord

def getIcaoCode(rawICAO):
    value = rawICAO >> 5
    codedChars = []
    
    while (value >= 0):
        if (value < 38):
            oneCodedChar = value
            value = -1
        else:
            oneCodedChar = value % 38
            value = (value - oneCodedChar) / 38
        codedChars += [int(oneCodedChar)]
    codedChars.reverse()
    result = ''
    for codedChar in codedChars:
        if codedChar == 0:
            output =' '
        elif codedChar > 1 and codedChar < 12:
            output = chr(ord('0') + codedChar - 2)
        else:
            output = chr(ord('A') + codedChar - 12)
        result += output
    return result
 