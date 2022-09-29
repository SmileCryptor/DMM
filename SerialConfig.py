import serial

class SerialConfig:

    def __init__(self):
        self.port = "/dev/ttyUSB0"
        #self.port = "COM6"
        # self.port = "/dev/ttyS2"
        self.baudrate = 9600
        self.bytesize = serial.EIGHTBITS        # number of bits per bytes
        self.parity = serial.PARITY_NONE        # set parity check: no parity
        self.stopbits = serial.STOPBITS_ONE     # number of stop bits
        # self.timeout = None                   # block read
        self.timeout = 1                        # non-block read
        # self.timeout = 2                      #timeout block read
        self.xonxoff = False                    # disable software flow control
        self.rtscts = False                     # disable hardware (RTS/CTS) flow control
        self.dsrdtr = False                     # disable hardware (DSR/DTR) flow control
        self.writeTimeout = 0                   # timeout for write


        self.interval = 0.1                     # Assign Query Time in Second to Read Serial Data
        self.weightChecking = 2                 # Check similar weight values

        ## Hx711 Configuration
        self.doutpin = 21
        self.pdsckpin = 20
        self.gain = 32                          # 32, 128, 64
        self.channel = 'B'
        self.roundoff = 1                       # 1, 2, 3, 4, 5, ...

