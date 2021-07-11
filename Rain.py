
from gpiozero import Button
import time
from datetime import datetime

RAIN_HOUR = 'in/hr'
RAIN_DAY = 'in/day'
RAIN_WEEK = 'in/wk'
RAIN_MONTH = 'in/mo'
RAIN_YEAR = 'in/yr'

class RainGauge:
    def __init__(self):
        self.reset()
        self.rain_speed_sensor = Button(6)
        self.rain_speed_sensor.when_pressed = self.rain_count
        
    def reset(self):
        self.count = []
    
    def rain_count(self):
        self.count.append(time.time())

    def get_recent(self, since=RAIN_HOUR):
        if since == RAIN_HOUR:
            s = datetime.now().strftime('%Y-%m-%d %H:00')
            limit = datetime.strptime(s, "%Y-%m-%d %H:%M").timestamp()
        elif since == RAIN_DAY:
            s = datetime.now().strftime('%Y-%m-%d 00:00')
            limit = datetime.strptime(s, "%Y-%m-%d %H:%M").timestamp()
        elif since == RAIN_MONTH:
            s = datetime.now().strftime('%Y-%m-01 00:00')
            limit = datetime.strptime(s, "%Y-%m-%d %H:%M").timestamp()
        else: # if since == RAIN_YEAR
            s = datetime.now().strftime('%Y-01-01 00:00')
            limit = datetime.strptime(s, "%Y-%m-%d %H:%M").timestamp()
        
        clicks = filter(lambda x: x >= limit, self.count)
        val = len(list(clicks)) * 0.011 # inches rain per click
        data = {'rain': {'measurement': val, 'units': since}}
        return data
