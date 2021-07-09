
import smbus2
import bme280

class BME280Monitor:
    def __init__(self, port=1, address=0x77) -> None:
        self.port = port
        self.address = address
        self.bus = smbus2.SMBus(self.port, self.address)
        self.compensation = bme280.load_calibration_params(self.bus, self.address)
        
    def get_all_data(self):
        data = bme280.sample(self.bus, self.address, self.compensation)
        temperature = '{0:6.2f}'.format(data.temperature).strip()
        pressure = '{0:7.2f}'.format(data.pressure).strip()
        humidity = '{0:5.1f}'.format(data.humidity).strip()

        payload = {
            'temperature': {'measurement': temperature, 'units': '°C'},
            'pressure': {'measurement': pressure, 'units': 'hPa'},
            'humidity': {'measurement': humidity, 'units': '%'},
        }
        return payload
  