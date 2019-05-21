import bluepy
from config import *

class LEDController():
    def __init__(self):
        self.peripheral = bluepy.btle.Peripheral(bluetooth_mac)
        self.chars = [x for x in self.peripheral.getDescriptors()]
        self.red = chars[36]
        self.green = chars[39]
        self.blue = chars[42]
