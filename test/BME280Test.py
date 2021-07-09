import sys
sys.path.append('..')
import BME280
from datetime import datetime
import time

sensor = BME280.BME280Monitor()
for i in range(10):
    p = sensor.get_all_data()
    print('Data at {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print(p)
    time.sleep(5)
