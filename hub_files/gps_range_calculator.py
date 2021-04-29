import mock_config.default_variables as dv
import math

# meaturements in feet
radius_of_earth = 20902000
bluetooth_range = 30
range_tolerance = bluetooth_range * 0.75
hub_lat = dv.mock_latitude
hub_long = dv.mock_longitude


def translate_gps(gps_coords):
    #print("Calculating range from hub")
    message = calculate_with_real_gps(gps_coords)
    #message = calculate_with_fake_gps(gps_coords)
    return message

def calculate_with_fake_gps(gps_coords):
    return gps_coords

def calculate_with_real_gps(gps_coords):
    # assumes gps_coords is a list of two floats
    if type(gps_coords) is not list:
        gps_coords = gps_coords.split(", ")
        for i in range(0,len(gps_coords)):
            gps_coords[i] = float(gps_coords[i])
    #print("GPS coords: " + str(gps_coords))
    #print("GPS coords type: " + str(type(gps_coords)))
    collar_lat = gps_coords[0]
    collar_long = gps_coords[1]
    dlat = degrees_to_radians(hub_lat - collar_lat)
    dlon = degrees_to_radians(hub_long - collar_long)
    lat1 = degrees_to_radians(collar_lat)
    lat2 = degrees_to_radians(hub_lat)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.sin(dlon/2) * math.sin(dlon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius_of_earth * c
    if distance <= range_tolerance:
        return 'OK'
    elif distance <= bluetooth_range:
        print("Pet is almost out of range of home hub")
        return 'AT BOUNDARY'
    elif distance > bluetooth_range:
        print("Pet is not in range")
        return 'EXCEEDED RANGE'
    
def degrees_to_radians(deg):
    return deg * math.pi / 180
