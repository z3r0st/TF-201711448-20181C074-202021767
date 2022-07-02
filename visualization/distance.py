import math

def toRadians(valor):
  return (math.pi/180.0)*valor

def calculateDistance(intercept1, intecerpt2):
  Lat1, Lon1 = intercept1
  Lat2, Lon2 = intecerpt2
  difLat = toRadians(Lat2 - Lat1)
  difLon = toRadians(Lon2 - Lon1)

  a = math.sin(difLat/2)**2 + math.cos(toRadians(Lat1))*math.cos(toRadians(Lat2))*(math.sin(difLon/2))**2
  c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))

  return  6371000.0*c