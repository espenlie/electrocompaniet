import serial, time


class ECI6D(object):
    def __init__(self):
        self.dev = serial.Serial(
                    port='/dev/ttyUSB0',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1
                    )
        self.eol = b'\r'
        self.channels = {'USB'      :   'USB',
                        'TOSLink1'  :   'TL1',
                        'TOSLink2'  :   'TL2',
                        'COAX1'     :   'CX1',
                        'COAX2'     :   'CX2',
                        'CD'        :   'CDP',
                        'DVD'       :   'DVD',
                        'AUX'       :   'AUX'
                        }


    def ismuted(self):
        self.dev.write('#QMU\r')
        if self.read_response() == '@OK OFF\r':
            return False
        else:
            return True

    def mute(self):
        self.dev.write('#MUT\r')
        if self.read_response() == '@OK OFF\r':
            return False
        else:
            return True

    def read_response(self):
        leneol = len(self.eol)
        line = bytearray()
        while True:
            c = self.dev.read(1)
            if c:
                line += c
                if line[-leneol:] == self.eol:
                    break
            else:
                break
        return line
    
    def volume_up(self, lvls=1):
        if lvls > 10:
            lvls = 4
        for i in range(lvls):
            self.dev.write('#VUP\r')
            if self.read_response() != '@OK\r':
                break

    def volume_down(self, lvls=1):
        if lvls > 10:
            lvls = 4
        for i in range(lvls):
            self.dev.write('#VDN\r')
            if self.read_response() != '@OK\r':
                break

    def set_input(self, channel):
        if not channel in self.channels.keys():
            print "Invalid channel."
            return
        self.dev.write('#QIN\r')
        if self.read_response() == '@OK %s\r' % channel:
            print 'Already at that channel.'
            return

        self.dev.write('#%s\r' % self.channels[channel])
        if not self.read_response() == '@OK %s\r' % self.channels[channel]:
            print 'Something wrong happend.'
            
    def close(self):
        self.dev.close()

    def power_off(self):
        self.dev.write('#POF\r')
        if not self.read_response() == '@OK OFF\r':
            print 'Something wrong happened. Could not turn off amp.'

    def power_on(self):
        self.dev.write('#PON\r')
        if not self.read_response() == '@OK ON\r':
            print 'Something wrong happened. Could not turn on amp.'



if __name__ == '__main__':
    electro = ECI6D()
#   print electro.mute()
#   print electro.ismuted()
#   electro.volume_up(lvls=10)
#   electro.volume_down(lvls=10)
    electro.set_input('USB')
#   electro.power_off()
#   time.sleep(5)
#   electro.power_on()
    electro.close()
