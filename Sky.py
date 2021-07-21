from astral import LocationInfo
from astral.sun import sun
from astral import moon
import datetime

phases = {
    (0, 0.5): 'New Moon',
    (0.5, 6.5): 'Waxing Crescent',
    (6.5, 7.5): 'First Quarter',
    (7.5, 13.5): 'Waxing Gibbous',
    (13.5, 14.5): 'Full Moon',
    (14.5, 20.5): 'Waining Gibbous',
    (20.5, 21.5): 'Last Quarter',
    (21.5, 27.5): 'Waining Crescent',
    (27.5, 29): 'New Moon'
}

location = LocationInfo("Santa Cruz", "United States", "America/Los_Angeles", 37.014835, -121.979731)
sun_state = sun(location.observer, date=datetime.date.today(), tzinfo=location.timezone)
sunrise = sun_state["sunrise"].strftime("%H:%M:%S")
sunset = sun_state["sunset"].strftime("%H:%M:%S")
phase = moon.phase(datetime.date.today())
for k, name in phases.items():
    s,e = k
    if phase >= s and phase <= e:
        pom = name
        break
print('sunrise: '+sunrise+', sunset: '+sunset+', POM: '+pom+', Moon Day: '+str(phase))
