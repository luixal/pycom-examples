from serial import Serial

class ModbusReader:

    def __init__(self, pinRX, pinTX):
        self.modbus_obj = Serial(uart_id=1, baudrate=19200, data_bits=8, stop_bits=1, pins=(pinRX, pinTX))
        # slave serial device address:
        self.SLAVE_ADDRESS = 1
        # sending all command as signed:
        self.SIGNED = False
        # function codes/addresses for values:
        self.OZONE_FC = 0
        self.TEMPERATURE_FC = 2
        self.HUMIDITY_FC = 4
        # default record length:
        self.RECORD_LENGTH = 2

    def readOzone(self):
        try:
            value = self.modbus_obj.read_float_registers(self.SLAVE_ADDRESS, self.OZONE_FC, self.RECORD_LENGTH, self.SIGNED)
            return value
        except Exception:
            return False

    def readTemperature(self):
        try:
            value = self.modbus_obj.read_float_registers(self.SLAVE_ADDRESS, self.TEMPERATURE_FC, self.RECORD_LENGTH, self.SIGNED)
            return value
        except Exception:
            return False

    def readHumidity(self):
        try:
            value = self.modbus_obj.read_float_registers(self.SLAVE_ADDRESS, self.HUMIDITY_FC, self.RECORD_LENGTH, self.SIGNED)
            return value
        except Exception:
            return False
