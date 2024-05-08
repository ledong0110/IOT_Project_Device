from typing import List
from serial import Serial
from ..utils import calculate_crc16

class Rs485Device:
    def __init__(self, serial: Serial, id: int):
        self.serial = serial
        self.id = id
    
    def _generate_bytearray(self, operation: int, register_address: int, data: int):
        array_data = [self.id, operation, register_address >> 8, register_address & 0xFF, data >> 8, data & 0xFF]
        return  array_data + calculate_crc16(array_data)
        
    def _send(self, data: List):
        if len(data) != 7:
            raise ValueError("Data must be 7 bytes long")
        self.serial.write(data)

    def _read(self):
        bytesToRead = self.serial.inWaiting()
        if bytesToRead == 0:
            return 0
        data = self.serial.read(bytesToRead)
        dataArray = list(data)
        if len(dataArray) >= 7:
            array_size = len(dataArray)
            value = dataArray[array_size - 4] * 256 + dataArray[array_size - 3]
            return value
        else:
            return -1
   