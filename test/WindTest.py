import sys
sys.path.append('..')
import Wind
import time

wind_speed = Wind.WindSpeed()
wind_dir = Wind.WindDirection()
for i in range(10):
    time.sleep(5)
    data = wind_speed.get_all_data()
    units = data['units']
    ispeed = data['speed']
    aspeed = data['average']
    gust = data['gust']
    print('Current speed: {0:6.2f} {1}'.format(ispeed, units))
    print('Average speed: {0:6.2f} {1}'.format(aspeed, units))
    print('Gust: {0:6.2f} {1}'.format(gust, units))

    data = wind_dir.get_wind_direction()
    print('Direction {0:5.1f}°, {1}'.format(data[0], data[1]))
