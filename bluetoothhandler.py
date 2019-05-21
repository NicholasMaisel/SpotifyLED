import bluepy
from config import *

class LEDController():
    def __init__(self):
        self.peripheral = bluepy.btle.Peripheral(bluetooth_mac)
        self.chars = [x for x in self.peripheral.getDescriptors()]
        self.red = self.chars[36]
        self.green = self.chars[39]
        self.blue = self.chars[42]
