import sys
sys.path.append('..')
import Rain
import time

rain = Rain.RainGauge()
for i in range(10):
    time.sleep(5)
    print('{} inches in last hour'.format(rain.get_recent() * 0.011))
    print('{} inches in last day'.format(rain.get_recent(Rain.RAIN_DAY) * 0.011))