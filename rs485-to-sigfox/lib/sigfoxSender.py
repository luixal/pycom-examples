from network import Sigfox
import socket
from ubinascii import hexlify
import struct

class SigFoxSender:

    def __init__(self):
        # init Sigfox for RCZ1 (Europe)
        self.sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
        # create a Sigfox socket
        self.socket = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
        # make the socket blocking
        self.socket.setblocking(True)
        # configure it as uplink only
        self.socket.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
        print('SigFox socket created')
        print(
            'MAC: {} - ID: {} - RSSI: {} - PAC: {}'
            .format(
                hexlify(self.sigfox.mac()).decode(),
                hexlify(self.sigfox.id()).decode(),
                self.sigfox.rssi(),
                hexlify(self.sigfox.pac()).decode()
            )
        )

    def getSignalStrength(self):
        return self.sigfox.rssi()

    def transformValue(self, value):
        # divide by 10 (convention as high values are expected at some point):
        transformed = value / 10
        # cast value to int:
        transformed = int(transformed)
        # avoid negative values:
        transformed = 0 if (transformed < 0) else transformed
        # as we are packing the value in a single byte, make it 255 as max value:
        transformed = 255 if (transformed > 255) else transformed
        # return transformed value:
        return transformed

    def packMesageForSigFox(self, ozone, temperature, humidity):
        # casting floats to ints in values array (only ozone values):
        values = [ self.transformValue(x) for x in ozone ]
        # adding temperature and humidity to values array (casted to ints):
        values.append( int(temperature) )
        values.append( int(humidity) )
        # returning array packed for sigfox
        # sigfox custom grammar to use: ozone1::uint:8 ozone2::uint:8 ozone3::uint:8 ozone4::uint:8 ozone5::uint:8 ozone6::uint:8 ozone7::uint:8 ozone8::uint:8 ozone9::uint:8 ozone10::uint:8 temperature::uint:8 humidity::uint:8
        return struct.pack('B'*len(values), *values);
        # return struct.pack('>BBBBBBBBBB', ozone..., int(temperature), int(humidity))

    def sendMessage(self, message):
        return self.socket.send(message)

    def sendValues(self, ozone, temperature, humidity):
        res = self.sendMessage( self.packMesageForSigFox(ozone, temperature, humidity) )
        return res
