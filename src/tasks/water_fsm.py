from typing import List
import random
from ..device_wrapper import Sensor, Relay, RS485
from ..connector import AdafruitConnector
from ..repository import TaskAction
from ..config.constants import IDLE, MIXER1, MIXER2, MIXER3, PUMP_IN, SELECTOR, PUMP_OUT, DONE
from ..config import glob_var
import json
import logging
import time
logging.basicConfig(filename='SchedulerLog.txt', level=logging.INFO)


def water_fsm(task: TaskAction):
    glob_var.mqtt_client.publish("task_result", json.dumps({"Task_id": task.task_id, "state": 1}))
    actuators = glob_var.list_actuators
    count = 0
    state = IDLE
    actuator = None
    while state == DONE:
        if state == IDLE:
            logging.info("IDLE")
            state = MIXER1
            count = task.M1

            logging.info("MIXER1")
            actuator = next(filter(lambda x: x.name == "Mixer1", actuators))
            actuator.on()
            logging.info("TimeProcess: " + str(count))

        elif state == MIXER1:
            if count <= 0:
                actuator.off()
                logging.info("MIXER2")
                state = MIXER2
                count = task.M2
                actuator = next(filter(lambda x: x.name == "Mixer2", actuators))
                actuator.on()

            logging.info("TimeProcess: " + str(count))

        elif state == MIXER2:
            if count <= 0:
                actuator.off()
                logging.info("MIXER3")
                state = MIXER3
                count = task.M3
                actuator = next(filter(lambda x: x.name == "Mixer3", actuators))
                actuator.on()

            logging.info("TimeProcess: " + str(count))

        elif state == MIXER3:
            if count <= 0:
                actuator.off()
                logging.info("PUMP_IN")
                state = PUMP_IN
                count = random.randint(4, 8)
                actuator = next(filter(lambda x: x.name == "Pump_in", actuators))
                actuator.on()

            logging.info("TimeProcess: " + str(count))

        elif state == PUMP_IN:
            if count <= 0:
                actuator.off()
                logging.info("SELECTOR")
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

                # logging.info("Area selected: " + str(area_selected))
                count = 3
                

            logging.info("TimeProcess: " + str(count))
        elif state == SELECTOR:
            if count <= 0:
                logging.info("PUMP_OUT")
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
            logging.info("TimeProcess: " + str(count))

        elif state == PUMP_OUT:
            if count <= 0:
                actuator.off()
                logging.info("DONE")
                state = DONE
        else:
            raise ValueError("Invalid state")
        time.sleep(1)
        count -= 1
    glob_var.mqtt_client.publish("task_result", json.dumps({"Task_id": task.task_id, "state": 2}))
