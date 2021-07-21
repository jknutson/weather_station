from astral import LocationInfo
from astral.sun import sun
from astral import moon
import datetime

phases = ['New Moon', 'First Quarter', 'Full Moon', 'Last Quarter']

location = LocationInfo("Santa Cruz", "United States", "America/Los_Angeles", 37.014835, -121.979731)
sun_state = sun(location.observer, date=datetime.date.today(), tzinfo=location.timezone)
sunrise = sun_state["sunrise"].strftime("%H:%M:%S")
sunset = sun_state["sunset"].strftime("%H:%M:%S")
phase = round(moon.phase(datetime.date.today()) / (29.53059/4))
pom = phases[phase]
print('sunrise: '+sunrise+', sunset: '+sunset+', POM: '+pom)
