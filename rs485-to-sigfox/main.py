from serial import Serial
import time
import struct
from sigfoxSender import SigFoxSender
from modbusReader import ModbusReader
from pycom import heartbeat
from pycom import rgbled

# disable LED's heartbeat:
heartbeat(False)
# LED color values:
LED_OFF = 00000000
LED_COLOR_RED = 0x7f0000
LED_COLOR_GREEN = 0x007f00
LED_COLOR_YELLOW = 0x7f7f00

# serial modbus reader:
PIN_RX = 'P3'
PIN_TX = 'P4'
modbusReader = ModbusReader(PIN_RX, PIN_TX)

# interval between each reading:
READING_INTERVAL = 60
# error interval between each trying:
READING_INTERVAL_ERROR = 5
# how many values to read before sending:
READING_LIMIT = 10
# array for keeping ozone values:
ozoneValues = []

# sigfox class for packing and sending messages:
sigfoxSender = SigFoxSender()

def get_device_details():
    # TODO: get serial, firmware version, script version...
    return ''

while True:
    # temperature = read_temperature()
    # humidity = read_humidity()
    ozone = modbusReader.readOzone()
    if (ozone):
        # turn LED off (in case it was on):
        rgbled(LED_OFF)
        ozoneValues.append(ozone)
        print('{} :: Ozone level: {} ppb'.format(len(ozoneValues), ozone))
        if (len(ozoneValues) == READING_LIMIT):
            # TODO: read temperature and humidity and pack message:
            temperature = modbusReader.readTemperature()
            humidity = modbusReader.readHumidity()
            print('\nSending values: \n\t-Ozone: {}\n\t-Temperature: {}\n\tHumidity: {}\n'.format(ozoneValues, temperature, humidity))
            # set LED to yello color while sending:
            rgbled(LED_COLOR_YELLOW)
            result = sigfoxSender.sendValues(ozoneValues, temperature, humidity)
            print('Message sent: {} - Signal Strength: {}'.format(result, sigfoxSender.getSignalStrength()))
            # if sent, set LED to green color for a second and power it off:
            rgbled(LED_COLOR_GREEN)
            time.sleep(1)
            rgbled(LED_OFF)
            # reset values array:
            ozoneValues = []
        # wait interval
        time.sleep(READING_INTERVAL)
    else:
        # if error, set LED to red color and print message:
        rgbled(LED_COLOR_RED)
        print('Could NOT read value from modbus')
        # wait interval
        time.sleep(READING_INTERVAL_ERROR)
