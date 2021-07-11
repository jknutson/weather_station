from math import sin
import time
from datetime import datetime
import socket
import MQTT
import Display
import BME280
import Rain
import Wind

# Display globals
display = Display.Display()
my_font = display.font24
line_spacing = 26

# MQTT clients
station_name = 'WeatherStation'
ws_location = '37.014835,-121.979731'
topic_data = 'weather/data'
mqtt_data = MQTT.MQTTClient(station_name, ws_location, topic_data, '192.168.0.105', 1883)
topic_status = 'weather/status'
mqtt_status = MQTT.MQTTClient(station_name+'_Status', ws_location, topic_status, '192.168.0.105', 1883)


# Retreives our IP address
ip_host = ''
def get_ip():
    global ip_host
    
    if ip_host != '':
        return ip_host
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip_host = s.getsockname()[0]
    except Exception:
        ip_host = '127.0.0.1'
    finally:
        s.close()
    return ip_host

# Publish a status message to the MQTT broker
def publish_status(payload):
    global mqtt_status
    global station_name
    global ws_location
    global topic_status
    mqtt_status.publish(topic_status, payload)

# Publish WeatherStation dat to the MQTT broker
def publish_data(payload):
    global mqtt_data
    global station_name
    global ws_location
    global topic_data
    mqtt_status.publish(topic_data, payload)

# Displays booting message on screen
def boot_message(display, message):
    global my_font
    global line_spacing
    global host

    booting_date = datetime.now().strftime('%Y-%m-%d')
    booting_time = datetime.now().strftime('%H:%M:%S')
    coords = [0, 0]
    display.new_canvas(display.DISP_LAYOUT_PORTRAIT)
    display.draw.text(tuple(coords), 'WeatherStation', font=my_font, fill=0)
    coords[1] += line_spacing
    display.draw.text(tuple(coords), message, font=my_font, fill=0)
    coords[1] += line_spacing
    display.draw.text(tuple(coords), booting_date, font=my_font, fill=0)
    coords[1] += line_spacing
    display.draw.text(tuple(coords), booting_time, font=my_font, fill=0)
    coords[1] += line_spacing
    width, height = display.get_canvas_size(display.DISP_LAYOUT_PORTRAIT)
    display.draw.text((0,height - line_spacing), host, font=my_font, fill=0)
    display.finish_drawing()

def display_update(display, temp, hum, bp, wind, speed, gust, rain):
    global my_font
    global line_spacing
    global host

    coords = [0, 0]
    display.new_canvas(display.DISP_LAYOUT_PORTRAIT)
    display.draw.text(tuple(coords), 'WeatherStation', font=my_font, fill=0)
    coords[1] += line_spacing
    display.draw.text(tuple(coords), datetime.now().strftime('%Y-%m-%d'), font=my_font, fill=0)
    coords[1] += line_spacing
    display.draw.text(tuple(coords), datetime.now().strftime('%H:%M:%S'), font=my_font, fill=0)
    coords[1] += 1.5 * line_spacing
    display.draw.text(tuple(coords), 'temp {0:.1f} °F'.format(temp), font=my_font, fill=0)
    coords[1] += line_spacing
    display.draw.text(tuple(coords), 'hum. {0:.1f} %'.format(hum), font=my_font, fill=0)
    coords[1] += line_spacing
    display.draw.text(tuple(coords), 'bp {0:.2f} inhg'.format(bp), font=my_font, fill=0)
    coords[1] += 1.5 * line_spacing
    display.draw.text(tuple(coords), 'wind {}'.format(wind), font=my_font, fill=0)
    coords[1] += line_spacing
    display.draw.text(tuple(coords), ' {0:.0f}/{1:.0f}g mph'.format(speed, gust), font=my_font, fill=0)
    coords[1] += line_spacing
    display.draw.text(tuple(coords), 'rain {0:.2f} in'.format(rain), font=my_font, fill=0)
    coords[1] += line_spacing

    width, height = display.get_canvas_size(display.DISP_LAYOUT_PORTRAIT)
    display.draw.text((0,height - line_spacing), host, font=my_font, fill=0)
    display.finish_drawing()

def report_tbp(tbp, payload):
    payload.update(tbp.get_all_data())

def report_wind(speed, direction, payload):
    speed_data = speed.get_all_data()
    wind_data = {
        'wind': {
            'direction': direction.get_wind_direction()[1],
        }
    }
    wind_data['wind'].update(speed_data)
    payload.update(wind_data)

def report_rain(rain, since, payload):
    interval = since.split('/')[1]
    rpt = rain.get_recent(since)
    payload.update({'rain_'+interval: rpt['rain']})

# Boot section
host = get_ip()

boot_message(display, ' Booting...')
publish_status({
    station_name: {
        'status': 'Bootstrap',
        'hostname': host
    }
})

thp = BME280.BME280Monitor()
wind_speed = Wind.WindSpeed()
wind_direction = Wind.WindDirection()
rain = Rain.RainGauge()

publish_status({
    station_name: {
        'status': 'Online',
        'hostname': host
    }
})
boot_message(display, ' Online')

# Online
count = 0
while True:
    # MQTT report every 10s
    time.sleep(10)
    payload = {}
    report_tbp(thp, payload)
    report_wind(wind_speed, wind_direction, payload)
    report_rain(rain, Rain.RAIN_HOUR, payload)
    report_rain(rain, Rain.RAIN_DAY, payload)
    publish_data(payload)

    # Update display every minute
    if count % 6 == 0:
        temp = float(payload['temperature']['measurement']) * 1.8 + 32.0 # convert °C to °F
        hum = float(payload['humidity']['measurement'])
        bp = float(payload['pressure']['measurement']) / 33.863886666667 # convert hPa to in/hg
        wind = payload['wind']['direction']
        speed = float(payload['wind']['average']) * 0.621371 # convert km/h to mph
        gust = float(payload['wind']['gust']) * 0.621371 # convert km/h to mph
        precip = float(payload['rain_day']['measurement'])
        display_update(display, temp, hum, bp, wind, speed, gust, precip)

    count += 1
