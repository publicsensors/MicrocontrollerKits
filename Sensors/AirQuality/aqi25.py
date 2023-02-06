# A simple wrapper for api.py to simplify usage when only PM2.5 is available
from AirQuality.aqi import AQI
def AQI25(pm25):
    return AQI.aqi(pm25,0.)
