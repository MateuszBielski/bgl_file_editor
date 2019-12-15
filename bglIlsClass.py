from bglSectionClass import Section
from OffsetClass import Offset
from bglFunctions import LatFromDword,LonFromDword,getIcaoCode
from struct import unpack,pack

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
    def FindRecordsByAirportIcao(self,icao):
        return [rec for subsection in self.subsectionData for rec in subsection.records if rec.airportID == icao]

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
        self.airportID = getIcaoCode(int(bin(record_u[11])[:28],2))#[11:31] << 4
        
        offOb.val += self.size
    def setElevation(self,newAltitude,rData):
        adr = self.altitudeAddress
        rData[adr:adr + 4] = pack('I',int(newAltitude*1000))
   
