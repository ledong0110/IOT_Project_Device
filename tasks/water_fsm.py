from typing import List, String
import random
from device_wrapper import Sensor, Relay, RS485
from connector import AdafruitConnector
from repository import TaskAction
from config.constants import IDLE, MIXER, PUMP_IN, SELECTOR, PUMP_OUT


def water_fsm(actuators: List[Relay], task: TaskAction, mqtt_client: AdafruitConnector):

    count = 0
    state = IDLE
    actuator = None
    while state == DONE:
        if state == IDLE:
            print("IDLE")
            state = MIXER1
            count = task.M1

            print("MIXER1")
            actuator = next(filter(lambda x: x.name == "Mixer1", actuators))
            actuator.on()
            print("TimeProcess: " + str(count))

        elif state == MIXER1:
            if count <= 0:
                actuator.off()
                print("MIXER2")
                state = MIXER2
                count = task.M2
                actuator = next(filter(lambda x: x.name == "Mixer2", actuators))
                actuator.on()

            print("TimeProcess: " + str(count))

        elif state == MIXER2:
            if count <= 0:
                actuator.off()
                print("MIXER3")
                state = MIXER3
                count = task.M3
                actuator = next(filter(lambda x: x.name == "Mixer3", actuators))
                actuator.on()

            print("TimeProcess: " + str(count))

        elif state == MIXER3:
            if count <= 0:
                actuator.off()
                print("PUMP_IN")
                state = PUMP_IN
                count = random.randint(4, 8)
                actuator = next(filter(lambda x: x.name == "Pump_in", actuators))
                actuator.on()

            print("TimeProcess: " + str(count))

        elif state == PUMP_IN:
            if count <= 0:
                actuator.off()
                print("SELECTOR")
                state = SELECTOR
                if task.Area1:
                    actuator = next(filter(lambda x: x.name == "Selector1", actuators))
                    actuator.on()
                if task.Area2:
                    actuator = next(filter(lambda x: x.name == "Selector2", actuators))
                    actuator.on()
                if task.Area3:
                    actuator = next(filter(lambda x: x.name == "Selector3", actuators))
                    actuator.on()

                # print("Area selected: " + str(area_selected))
                count = 3
                publish_stage(client, schedule_id, cycle, state)

            print("TimeProcess: " + str(count))
        elif state == SELECTOR:
            if count <= 0:
                print("PUMP_OUT")
                if task.Area1:
                    actuator = next(filter(lambda x: x.name == "Selector1", actuators))
                    actuator.off()
                if task.Area2:
                    actuator = next(filter(lambda x: x.name == "Selector2", actuators))
                    actuator.off()
                if task.Area3:
                    actuator = next(filter(lambda x: x.name == "Selector3", actuators))
                    actuator.off()
                state = PUMP_OUT
                count = 5
                actuator = next(filter(lambda x: x.name == "Pump_out", actuators))
                actuator.on()
            print("TimeProcess: " + str(count))

        elif state == PUMP_OUT:
            if count <= 0:
                actuator.off()
                print("DONE")
                state = DONE
        else:
            raise ValueError("Invalid state")

        count -= 1
