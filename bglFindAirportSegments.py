import bglTested
from struct import unpack

#~ fileName = "cvx9247_n.bgl"
fileName = "cvx5828.bgl"
#~ fileName = "cvx9247.bgl"

fileCVX = open(fileName,"rb")
rawData = fileCVX.read()
fileCVX.close()

for a_seg in bglTested.FindAirportSegments(bglTested.parse(rawData)):
    
    entity = a_seg.owner_entity
    subsection = entity.owner_subsection
    print(subsection.nr_id,entity.nr_id,a_seg.altitude[0])
    
#~ for a_ent in bglTested.FindAirportEntities(bglTested.parse(rawData)):
    #~ print(a_ent.owner_subsection.nr_id,a_ent.nr_id)
    
    
"""

70 195 4.267199993133545
73 67 44.50080108642578
75 209 44.50080108642578
145 741 656.234375
147 932 656.234375
155 564 480.05999755859375
172 29 348.08160400390625
179 236 420.6239929199219
206 480 27.127199172973633
210 311 90.83039855957031
211 90 90.83039855957031
228 445 27.127199172973633
233 202 24.384000778198242
235 348 30.175199508666992
236 98 24.384000778198242

"""


