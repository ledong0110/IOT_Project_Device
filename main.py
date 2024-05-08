import time
import serial
import serial.tools.list_ports
from device_wrapper import Relay, Sensor

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort
    # return "/dev/ttyUSB1"

portName = "/dev/ttyUSB0"
print(portName)



try:
    ser = serial.Serial(port=portName, baudrate=9600)
    print("Open successfully")
except:
    print("Can not open the port")

relay1 = Relay(serial=ser, id=2, register_address=0, on_value=255, off_value=0)

# while True:
#     relay1.on()
#     print("Is on: ", relay1.get_state())
#     time.sleep(2)
#     relay1.off()
#     print("Is off: ", relay1.get_state() == 0)
#     time.sleep(2)

soil_temperature_sensor = Sensor(serial=ser, id=3, register_address=6)
soil_moisture_sensor = Sensor(serial=ser, id=3, register_address=7)


while True:
    print("TEST SENSOR")
    print("Soil temperature: ", soil_temperature_sensor.read())
    time.sleep(1)
    print("Soil moisture: ", soil_moisture_sensor.read())
    time.sleep(1)