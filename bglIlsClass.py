from bglSectionClass import Section
from OffsetClass import Offset
from bglFunctions import LatFromDword,LonFromDword,getIcaoCode
from struct import unpack

class IlsSection(Section):
    def readSubsectionDataFrom(self,rData,offset,i,bglStructure):
        offOb = Offset(offset)
        subsectionData = SubsectionIlsData()
        subsectionData.nr_id = i
        numberOfRecords = self.subsections[i][1]
        subsectionData.numberOfRecords = numberOfRecords
        subsectionData.records = [IlsRecord(subsectionData,i,offOb,rData) for i in range(numberOfRecords)]
        return subsectionData
    def SelectClosestAirportTo(self,coordinates):
        pass
        

class SubsectionIlsData:
    def __init__(self):
        self.nr_id = None
        self.numberOfRecords = 0
        self.records = []

class IlsRecord:
    def __init__(self,owner_subsection,i,offOb,rData):
        self.owner_subsection = owner_subsection
        self.nr_id = i
        record_u = unpack('<HIBBIIIIffII',rData[offOb.val:offOb.val+0x28])
        self.r_id = record_u[0]
        self.size = record_u[1]
        self.longtitude = LonFromDword(record_u[4])
        self.latitude = LatFromDword(record_u[5])
        self.altitude = record_u[6]/1000
        self.altitudeAddress = offOb.val + 0x10
        self.Icao = getIcaoCode(record_u[10])
        offOb.val += self.size
    """
        
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
        """
