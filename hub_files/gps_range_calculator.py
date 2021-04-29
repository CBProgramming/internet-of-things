import mock_config.default_variables as dv

def translate_gps(gps_coords):
    #print("Calculating range from hub")
    #message = calculate_with_real_gps(gps_coords)
    message = calculate_with_fake_gps(gps_coords)
    return message

def calculate_with_fake_gps(gps_coords):
    return gps_coords

def calculate_with_real_gps(gps_coords):
    hub_long = dv.mock_longitute
    hub_lat = dv.mock_latitude
    
    
