import unittest
import bglTested
from bglFunctions import getIcaoCode

fileCVX = open("cvx9247.bgl","rb")
rawData = fileCVX.read()
fileCVX.close()

fileApx = open("APX92470.bgl","rb")
rawApxData = fileApx.read()
fileApx.close()

fileCVX5828 = open("cvx5828.bgl","rb")
rawDataCVX5828 = fileCVX5828.read()
fileCVX5828.close()

fileAPX5828 = open("APX58280.bgl","rb")
rawDataAPX5828 = fileAPX5828.read()
fileAPX5828.close()


subsections = bglTested.getSubsections(rawData)
BGLStructure = bglTested.parse(rawData)
BGLStructure_apx = bglTested.parse(rawApxData)
BGLStructureCVX5828 = bglTested.parse(rawDataCVX5828)
BGLStructureAPX_5828 = bglTested.parse(rawDataAPX5828)


chain = '84 3E 56 37 65 10 74 1D 3C 44 5B 9F 11 C5 D0 05 C9 2C F3 D5 B2 3A 8D 8A 8D 9D 9B 67 8B ED 52 59 B3 BC 0B 36 35 5F 54 25 B5 33 30 6D E2 64 4B EB 36 A1 8F D5 0D'
chain = chain.split()
chain = bytes([int('0x'+chain[i],16) for i in range(len(chain))])

result = '3E84 6EAC 4194 6BA0 43C1 6B68 4467 6862 4905 6659 4B57 69D5 58A8 73B1 59E6 76C5 5952 7966 582E 79A9 5545 76A4 4C0C 7136 4B64 6DD6 3E84 6EAC'
result = result.split()
result = [int('0x'+result[i],16) for i in range(len(result))]

maskRoot = 0xf
nbPoints = 14

class FromBgl(unittest.TestCase):#
    def testNumberOfSubsections(self):
        self.assertEqual(256,bglTested.getNumberOfSubsections(rawData))
        
    def testAdresToSubsectionData(self):
        self.assertEqual(0x230b47,bglTested.getAdresToSubsectionData(253,subsections))
    def testIfClassExist(self):
        self.assertTrue(BGLStructure.status)
        
    def testNumberOfSubsections_2(self):
        self.assertEqual(256,BGLStructure.numberOfSubsections)
        
    def testNumberOfEntitesIn(self):
        subsectionData = BGLStructure.subsectionData[253]
        self.assertEqual(1285,subsectionData.numberOfEntities)
        self.assertEqual(8,BGLStructure.subsectionData[186].numberOfEntities)
        
    def testAddressOfstartSignatures(self):
        self.assertEqual(0xb247,BGLStructure.subsectionData[187].startSignature)
        
    def testSignatureAddress(self):
        self.assertEqual(0xb247,BGLStructure.subsectionData[187].signatures[0].address)
        self.assertEqual(0x2329c3,BGLStructure.subsectionData[253].signatures[277].address)
        
    def testReadSignatures(self):
        self.assertEqual(0x234d33,BGLStructure.subsectionData[253].offsetStartEntities)
        self.assertEqual(2296454822,BGLStructure.subsectionData[185].signatures[1].additionalData[2])
        self.assertEqual(601,BGLStructure.subsectionData[253].numberOfSignatures)
        
    def testSignatureName(self):
        self.assertEqual('1B6A15BB-05FB-4401-A8D1-BB520E84904C',BGLStructure.subsectionData[253].signatures[300].name)
        self.assertEqual('EA0C44F7-01DE-4D10-97EB-FB5510EB7B72',BGLStructure.subsectionData[185].signatures[3].name)
        self.assertEqual('0CBC8FAD-DF73-40A1-AD2B-FE62F8004F6F',BGLStructure.subsectionData[253].signatures[277].name)
        
    def testEntityNumberOfSignatureOffsetsAndSegmentType(self):
        self.assertEqual(3,BGLStructure.subsectionData[187].entities[0].numberOfSignaturesOffsets)
        self.assertEqual(3,BGLStructure.subsectionData[187].entities[2].segmentsType)
        
    def testSegmentsAndDataBuffer(self):
        self.assertEqual(5,BGLStructure.subsectionData[187].entities[2].segments[0].numberOfPoints)
        self.assertEqual('D854BE0A3E75AA425145AC7454792B09D5EF0A3695AF02',BGLStructure.subsectionData[245].entities[1008].segments[0].dataBuffer.hex().upper())
        self.assertEqual(0xf,BGLStructure.subsectionData[245].entities[1008].segments[0].maskRoot)
        
    def testAllResultValues(self):
        calculatedResult = bglTested.CalculateRawCoordinates(maskRoot,chain,nbPoints)
        calculatedResult = [calculatedResult[i] for i in range(len(calculatedResult))]
        self.assertEqual(result,calculatedResult)
        
    def testAddValueToAltitude(self):
        rawDataCopy = bytearray(rawData)
        deltaValue = 138.31
        sourceValue = BGLStructure.subsectionData[248].entities[49].segments[0].altitude[0]
        destValue = 138.31 + sourceValue
        
        bglTested.AddValueToAltitude(deltaValue,rawDataCopy,BGLStructure.subsectionData[248].entities[49].segments[0])
        bglStructureCopy = bglTested.parse(rawDataCopy)
        
        checkedValue = bglTested.parse(rawDataCopy).subsectionData[248].entities[49].segments[0].altitude[0]
        self.assertEqual('%.3f'%(destValue),'%.3f'%(checkedValue))
    def testSetAltitudeToCvxAirportSegment(self):
        rawDataCopy = bytearray(rawData)
        destValue = 158.31
        cvxAirportSegment =  BGLStructure.subsectionData[248].entities[49].segments[0]
        cvxAirportSegment.setAltitude(destValue,rawDataCopy)
        checkedValue = bglTested.parse(rawDataCopy).subsectionData[248].entities[49].segments[0].altitude[0]
        self.assertEqual('%.3f'%(destValue),'%.3f'%(checkedValue))
        
    def testFindAirportSegments(self):
        airportSegment = BGLStructure.subsectionData[248].entities[49].segments[0]
        self.assertEqual(airportSegment,bglTested.FindAirportSegments(BGLStructure)[0])

    def testFindSceneryFolder_1(self):
        latitude = -44.6754369
        longtitude = 167.9119677
        self.assertEqual('1105',bglTested.FindSceneryFolderAndFilename(latitude,longtitude)[0])
    def testFindSceneryFolder_2(self):
        latitude = 26.5993624
        longtitude = -81.9978516
        self.assertEqual('0302',bglTested.FindSceneryFolderAndFilename(latitude,longtitude)[0])
    def testFindFileName(self):
        latitude = -44.6754369
        longtitude = 167.9119677
        self.assertEqual('9247',bglTested.FindSceneryFolderAndFilename(latitude,longtitude)[1])
    def testPathCreate(self):
        latitude = -44.6754369
        longtitude = 167.9119677
        self.assertEqual('1105/scenery/cvx9247',bglTested.PathCreate(latitude,longtitude))
    def testCalcQmidFromDwordsLevel(self):
        self.assertEqual(11,bglTested.CalcQmidFromDwords(0x0081FA00,0)[2])
        self.assertEqual(13,bglTested.CalcQmidFromDwords(0x81FAB65,0)[2])
    def testCalcQmidFromDwordsUV_1(self):
        result = bglTested.CalcQmidFromDwords(0x0081FA00,0)
        u,v = 448,240
        self.assertEqual(u,result[0])
        self.assertEqual(v,result[1])
    def testCalcQmidFromDwordsUV_2(self):
        result = bglTested.CalcQmidFromDwords(0x000207E8,0)
        u,v = 56,30
        self.assertEqual(u,result[0])
        self.assertEqual(v,result[1])
        
    def testGetBoundingCoordinates_1(self):
        dword = 0x207e8 
        boundCoord = (46.40625,47.8125,-75.0,-73.125)
        self.assertEqual(boundCoord,bglTested.GetBoundingCoordinates(dword))
    def testGetBoundingCoordinates_2(self):
        dword = 0x207e9 
        boundCoord = (46.40625,47.8125,- 73.125,-71.25)
        self.assertEqual(boundCoord,bglTested.GetBoundingCoordinates(dword))
    def testGetFinalCoordinatesFrom(self):
        rawCoordinates = (0x3E84,0x6EAC)
        boundingCoordinates = (47.63671875,47.8125,-75.0,-74.765625)
        finalCoordinates = (-74.885530471801758,47.788703441619873)
        self.assertEqual(finalCoordinates,bglTested.GetFinalCoordinatesFrom(rawCoordinates[0],rawCoordinates[1],boundingCoordinates))
    def testSectionType(self):
        self.assertEqual(0x65,bglTested.SectionType(rawData))
    def testReadAirportRecordAltitude(self):
        self.assertEqual(382.524,BGLStructure_apx.subsectionData[0].records[1].altitude)
    def testSetValueToAirport(self):
        rawDataCopy = bytearray(rawApxData)
        destValue = 114.24
        bglStruct = BGLStructure_apx
        airport = bglStruct.subsectionData[0].records[1]
        airport.setAltitude(destValue,rawDataCopy)
        bglStructCopy = bglTested.parse(rawDataCopy)
        airportFromCopy = bglStructCopy.subsectionData[0].records[1]
        
        self.assertEqual('%.3f'%(destValue),'%.3f'%(airportFromCopy.altitude))
        self.assertEqual('%.3f'%(destValue),'%.3f'%(airportFromCopy.subrecords[1].elevation)) #runway
        self.assertEqual('%.3f'%(destValue),'%.3f'%(airportFromCopy.subrecords[3].elevation)) #start
    def testReadAirportName(self):
        self.assertEqual('Glenorchy',BGLStructure_apx.subsectionData[0].records[1].subrecords[0].name)
    def testGetMeanSegmentCoordinates(self):
        coordinates = [(1.9,3),(9,6),(5,-2.2),(-4.1,3.9),(4.7,3.5)]
        self.assertEqual((3.3,2.84),bglTested.GetMeanCoordinates(coordinates))
    def testGetICAO_1(self):
        upacked = 0x0257C221
        self.assertEqual('KCLT',getIcaoCode(upacked))
    def testGetICAO_2(self):
        airport = BGLStructure_apx.subsectionData[0].records[0]
        self.assertEqual('NZMF',airport.getICAO())
    def testSubrecordGiveDataToAirport_Name(self):
        airport = BGLStructure_apx.subsectionData[0].records[0]
        self.assertEqual('Milford Sound',airport.name)
    def testSelectAirportSegmentClosestTo_cvx(self):
        airportCVXsegment = BGLStructureCVX5828.subsectionData[177].entities[31].segments[0] #HAAB
        coordinates = (8.9750, 38.7993)
        self.assertEqual(airportCVXsegment,BGLStructureCVX5828.SelectClosestAirportTo(coordinates))
    def testSelectAirportRecordClosestTo_apx(self):
        airportAPXRecord = BGLStructure_apx.subsectionData[0].records[0]
        coordinates = (-44.68, 167.91)
        self.assertEqual(airportAPXRecord,BGLStructure_apx.SelectClosestAirportTo(coordinates))
    def testGetCenterCoordinatesFromFileSignature(self):
        self.assertEqual((9.84375, 39.375),bglTested.GetCenterCoordinatesFromFileSignature('5828'))
        
    def testCreatePathFromSignature(self):
        fileSignature = '5828'
        pathCVX = bglTested.CreatePathFromSignature(fileSignature,'cvx')
        pathAPX = bglTested.CreatePathFromSignature(fileSignature,'apx')
        self.assertEqual('0703/scenery/cvx5828',pathCVX)
        self.assertEqual('0703/scenery/APX58280',pathAPX)
    def testCreatePathFromCoordinates(self):
        latitude = -44.6754369
        longtitude = 167.9119677
        pathCVX = bglTested.CreatePathFromCoordinates(-44.6754369,167.9119677,'cvx')
        pathAPX = bglTested.CreatePathFromCoordinates(-44.6754369,167.9119677,'apx')
        self.assertEqual('1105/scenery/cvx9247',pathCVX)
        self.assertEqual('1105/scenery/APX92470',pathAPX)
    def testNumberOfSections(self):
        self.assertEqual(1,BGLStructure.numberOfSections)           #cvx9247
        self.assertEqual(3,BGLStructure_apx.numberOfSections)       #APX92470
        self.assertEqual(1,BGLStructureCVX5828.numberOfSections)    #cvx5828
        self.assertEqual(9,BGLStructureAPX_5828.numberOfSections)   #APX58280
    def testIdsOfSections(self):
        sectionExpects = [0x3,0x2c,0x13,0x18,0x22,0x25,0x28,0x2a,0x27]
        sectionResults = BGLStructureAPX_5828.getSectionIds()
        self.assertEqual(sectionExpects,sectionResults)
    def testNumberOfSubsectionsInSections(self):
        self.assertEqual(256,BGLStructure.sections[0].numberOfSubsections)
class ILSAirport(unittest.TestCase):
    def testIlsTypeSection(self):
        self.assertEqual(0x13,BGLStructureAPX_5828.sections[2].kindOfSection)
    
if __name__ == "__main__":
    unittest.main()
