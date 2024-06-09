from .rs485 import RS485
from ..config.constants import READ_HOLDING_REGISTERS, WRITE_SINGLE_REGISTER
import random


class Sensor(RS485):
    def __init__(self, serial, id, name, area, register_address=0):
        super().__init__(serial, id, name, area)
        self.register_address = register_address

    def read(self, postprocess=lambda x: x):
        self._read()
        msg = self._generate_bytearray(READ_HOLDING_REGISTERS, self.register_address, 1)
        self._send(msg)
        return postprocess(self._read())


class VirtualSensor(RS485):
    def __init__(self, serial, id, name, area, register_address=0):
        super().__init__(serial, id, name, area)
        self.register_address = register_address

    def read(self, postprocess=lambda x: x):
        sensor_value = random.randint(0, 100)
        return postprocess(sensor_value)
