import sys
sys.path.append('..')
import Display
from datetime import datetime
import time

d = Display.Display()
d.clear()

for i in range(3):
    d.new_canvas(d.DISP_LAYOUT_PORTRAIT)
    d.draw.text((10,0), 'Weather at', font=d.font24, fill=0)
    d.draw.text((10,26), datetime.now().strftime('%Y-%m-%d'), font=d.font24, fill=0)
    d.draw.text((10,52), datetime.now().strftime('%H:%M:%S'), font=d.font24, fill=0)
    d.draw.text((10,90), 'temp 24.5 °C', font=d.font24, fill=0)
    d.draw.text((10,116), 'hum. 40.0 %', font=d.font24, fill=0)
    d.draw.text((10,142), 'bp 1014 hPa', font=d.font24, fill=0)
    d.draw.text((10,174), 'wind WNW', font=d.font24, fill=0)
    d.draw.text((10,200), ' 10/25g mph', font=d.font24, fill=0)
    d.draw.text((10,226), 'rain 0.00 in', font=d.font24, fill=0)
    d.finish_drawing()
    time.sleep(10)
