import time
from typing import List
from serial import Serial
from utils import calculate_crc16

class RS485:
    def __init__(self, serial: Serial, id: int):
        self.serial = serial
        self.id = id
    
    def _generate_bytearray(self, operation: int, register_address: int, data: int):
        array_data = [self.id, operation, register_address >> 8, register_address & 0xFF, data >> 8, data & 0xFF]
        return  calculate_crc16(array_data)
        
    def _send(self, data: List):
        if len(data) < 7:
            raise ValueError("Data must be 7 bytes long")
        self.serial.write(data)
        time.sleep(1)

    def _read(self):
        bytesToRead = self.serial.inWaiting()
        if bytesToRead > 0:
            out = self.serial.read(bytesToRead)
            data_array = [b for b in out]
            print(data_array)
            if len(data_array) >= 7:
                array_size = len(data_array)
                value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
                return value
            else:
                return -1
        print("No data to read")
        return 0
   