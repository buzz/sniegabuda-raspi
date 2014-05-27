from math import ceil

class LPD8806(object):
    """Main driver for LPD8806 based LED strips"""
    
    def __init__(self, leds, use_py_spi = False, dev="/dev/spidev0.0"):
        self.leds = leds
        self.dev = dev
        self.use_py_spi = use_py_spi

        if self.use_py_spi:
            import spidev
            self.spi = spidev.SpiDev()
            self.spi.open(0,0)
            self.spi.max_speed_hz = 2000000
            print 'py-spidev MHz: %d' % (self.spi.max_speed_hz / 1000000.0 )
        else:
            self.spi = open(self.dev, "wb")

    #Push new data to strand
    def update(self, buffer):
        if self.use_py_spi:

            # optimization taken from:
            # http://www.instructables.com/id/Raspberry-Pi-Spectrum-Analyzer-with-RGB-LED-Strip-/step1/Connect-LED-strip-and-setup-RGB-LED-software/
            # temp_buffer = []
            # for x in xrange(self.leds):
            #     temp_buffer = temp_buffer + [i for i in buffer[x]]
            #     temp_buffer = temp_buffer + [i for i in buffer[x]]
            # self.spi.xfer2(temp_buffer)

            for x in xrange(self.leds):
                self.spi.xfer2([i for i in buffer[x]]) # SLOW!?

            # we have to send one 0 octet for every 32 LED to reset
            # for x in xrange(int(ceil(self.leds/32.))):
                # self.spi.xfer2([0x00])
    
            self.spi.xfer2([0x00,0x00,0x00]) #zero fill the last to prevent stray colors at the end
            self.spi.xfer2([0x00]) #once more with feeling - this helps :)
        else:
            for x in xrange(self.leds):
                self.spi.write(buffer[x])
                self.spi.write(buffer[x])
                self.spi.flush()
            #seems that the more lights we have the more you have to push zeros
            #not 100% sure why this is yet, but it seems to work
            self.spi.write(bytearray(b'\x00\x00\x00')) #zero fill the last to prevent stray colors at the end
            self.spi.flush()
            self.spi.write(bytearray(b'\x00\x00\x00'))
            self.spi.flush()
            self.spi.write(bytearray(b'\x00\x00\x00'))
            self.spi.flush()
            self.spi.write(bytearray(b'\x00\x00\x00'))
            self.spi.flush()
