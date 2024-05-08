def calculate_crc16(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return data+[crc & 0xFF, (crc >> 8) & 0xFF]

if __name__ == '__main__':
    # Test the function
    data = [0, 6, 0, 0, 0, 255]
    crc = calculate_crc16(data)
    print(crc)