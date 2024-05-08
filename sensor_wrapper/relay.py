from .rs485 import RS485
from .constants import READ_HOLDING_REGISTERS, WRITE_SINGLE_REGISTER
class Relay(RS485):
    def __init__(self, serial, id, register_address=0, on_value=255, off_value=0):
        super().__init__(serial, id)
        self.on_value = on_value
        self.off_value = off_value
        self.register_address = register_address
    
    def on(self):
        msg = self._generate_bytearray(WRITE_SINGLE_REGISTER, self.register_address, self.on_value)
        self._send(msg)
        self._read()
    
    def off(self):
        msg = self._generate_bytearray(WRITE_SINGLE_REGISTER, self.register_address, self.off_value)
        self._send(msg)
        self._read()
    
    def get_state(self):
        self._read()
        msg = self._generate_bytearray(READ_HOLDING_REGISTERS, self.register_address, 1)
        self._send(msg)
        return self._read() == self.on_value