import bglTested
from struct import unpack
from bglFunctions import AssignRecordsFromOtherSectionByIcaoTo
#~ from copy import copy
lat = None
lon = None
decision = 'n'
while decision != 't':
    signature = input('numer pliku lub współrzędne (c):')
    if signature == 'c':
        lat = float(input('szerokość geograficzna:'))
        lon = float(input('długość geograficzna:'))
        try:
            file_cvx_Name_0 = bglTested.CreatePathFromCoordinates(lat,lon,'cvx')
            file_APX_Name_0 = bglTested.CreatePathFromCoordinates(lat,lon,'apx')
        except:
            print('błąd wprowadzonych współrzędnych')
            continue
    else:
        try:
            file_cvx_Name_0 = bglTested.CreatePathFromSignature(signature,'cvx')
            file_APX_Name_0 = bglTested.CreatePathFromSignature(signature,'apx')
        except:
            print('błąd wprowadzonej nazwy pliku')
            continue
    fileName_ext = ".bgl"
    file_cvx_Name = file_cvx_Name_0 + fileName_ext
    file_APX_Name = file_APX_Name_0 + fileName_ext
    
    question = 'czy pracujemy nad plikiem \n'+file_cvx_Name+'\n'+file_APX_Name+' ? (t/n), koniec (q):'
    decision = input(question)
    if decision == 'q':
        exit()
    if decision == 'n':
        lat = None
        lon = None
        
file_cvx_NameCopy = file_cvx_Name_0+'_bak'+fileName_ext
file_APX_NameCopy = file_APX_Name_0+'_bak'+fileName_ext
        
file_cvx_Source = open(file_cvx_Name,"rb")
raw_cvx_Data = file_cvx_Source.read()
file_cvx_Source.close()  
    
file_APX_Source = open(file_APX_Name,"rb")
raw_APX_Data = file_APX_Source.read()
file_APX_Source.close()      

if lat != None and lon != None:
    print('wyszukać z obu plików lotnisko najbliższe współrzędnym')
#~ else:

bgl_APX_Structure = bglTested.parse(raw_APX_Data)
bgl_cvx_Structure = bglTested.parse(raw_cvx_Data)
airports = []
for subs in bgl_APX_Structure.subsectionData:
    for rec in subs.records:
        airports += [rec]
a_numb = 0
for apt in airports:
    toPrint = '['+str(a_numb) + ']'+' '+ str(apt.getICAO())+' '+str(apt.name)+' '+str(apt.latitude)+' '+str(apt.longtitude)+' '+str(apt.altitude)
    print(toPrint)
    a_numb += 1

which_airport = int(input('w którym lotnisku zmieniamy wysokość?:'))
newAltitude  = input('podaj nową wysokość koniec(q)')
if newAltitude == 'q':
    exit()
newAltitude = float(newAltitude)
raw_APX_DataCopy = bytearray(raw_APX_Data)
raw_cvx_DataCopy = bytearray(raw_cvx_Data)
airportAPX = airports[which_airport]
airportCoordinates = (airportAPX.latitude,airportAPX.longtitude)
airportCVX = bgl_cvx_Structure.SelectClosestAirportTo(airportCoordinates)

AssignRecordsFromOtherSectionByIcaoTo(airportAPX)

airportAPX.setAltitude(newAltitude,raw_APX_DataCopy)
airportCVX.setAltitude(newAltitude,raw_cvx_DataCopy)

file_cvx_Copy = open(file_cvx_NameCopy,"wb")
file_cvx_Copy.write(raw_cvx_Data)
file_cvx_Copy.close()
file_APX_Copy = open(file_APX_NameCopy,"wb")
file_APX_Copy.write(raw_APX_Data)
file_APX_Copy.close()

new_cvx_File = open(file_cvx_Name,"wb")
new_cvx_File.write(raw_cvx_DataCopy)
new_cvx_File.close()
new_APX_File = open(file_APX_Name,"wb")
new_APX_File.write(raw_APX_DataCopy)
new_APX_File.close()
