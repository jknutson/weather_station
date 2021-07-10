from gpiozero import Button

rain_speed_sensor = Button(6)
rain_count = 0

def rain():
    global rain_count
    rain_count = rain_count + 1

def rain_gauge_data():
    global rain_count
    rain = rain_count * 0.011 # inches per bucket tip
    rain_count = 0
    return rain

rain_speed_sensor.when_pressed = rain
