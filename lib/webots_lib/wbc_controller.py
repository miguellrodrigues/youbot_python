#  * Copyright (c) 10/02/2021 22:04
#  *
#  * Last modified 10/02/2021 15:56
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.webots_lib.controller import Supervisor, Node, Device, PositionSensor, DistanceSensor, LightSensor, TouchSensor, Motor
from typing import List, cast


class Controller:
    def __init__(self, sampling_rate: int, setup_sensors: bool):
        self.supervisor = Supervisor()
        self.sampling_rate = sampling_rate

        if setup_sensors:
            self.setup_sensors()

    def step(self):
        return self.supervisor.step(self.sampling_rate)

    def get_supervisor(self) -> Supervisor:
        return self.supervisor

    def get_all_devices(self) -> List[Device]:
        count = self.supervisor.getNumberOfDevices()

        devices = []

        for i in range(count):
            devices.append(self.supervisor.getDeviceByIndex(i))

        return devices

    def _cast_devices(self, node_type, clazz):
        return [cast(clazz, x) for x in self.get_devices_by_type(node_type)]

    def get_devices_by_type(self, node_type: int) -> List[Device]:
        return [x for x in self.get_all_devices() if x.getNodeType() == node_type]

    def get_device_by_name(self, name) -> Device:
        return [x for x in self.get_all_devices() if x.getName() == name][0]

    def get_devices_by_type_list(self, list_type) -> List[Device]:
        return [x for x in self.get_all_devices() if list_type.__contains__(x.getNodeType())]

    def get_position_sensors(self) -> List[PositionSensor]:
        return self._cast_devices(Node.POSITION_SENSOR, PositionSensor)

    def get_distance_sensors(self) -> List[DistanceSensor]:
        return self._cast_devices(Node.DISTANCE_SENSOR, DistanceSensor)

    def get_light_sensors(self) -> List[LightSensor]:
        return self._cast_devices(Node.LIGHT_SENSOR, LightSensor)

    def get_touch_sensors(self) -> List[TouchSensor]:
        return self._cast_devices(Node.TOUCH_SENSOR, TouchSensor)

    def get_motors(self) -> List[Motor]:
        return self._cast_devices(Node.ROTATIONAL_MOTOR, Motor)

    def get_object_orientation(self, node_def: str) -> List[float]:
        object_node = self.supervisor.getFromDef(node_def)

        return object_node.getOrientation()

    def get_object_position(self, node_def: str) -> List[float]:
        object_node = self.supervisor.getFromDef(node_def)

        translation_field = object_node.getField("translation")

        return translation_field.getSFVec3f()

    def get_object_rotation(self, node_def: str) -> List[float]:
        object_node = self.supervisor.getFromDef(node_def)

        rotation_field = object_node.getField("rotation")

        return rotation_field.getSFRotation()

    def set_object_position(self, node_def: str, position: List[float]):
        object_node = self.supervisor.getFromDef(node_def)

        translation_field = object_node.getField("translation")

        translation_field.setSFVec3f(position)

    def set_object_rotation(self, node_def: str, rotation: List[float]):
        object_node = self.supervisor.getFromDef(node_def)

        rotation_field = object_node.getField("rotation")

        rotation_field.setSFRotation(rotation)

    def get_object_velocity(self, node_def: str) -> List[float]:
        return self.supervisor.getFromDef(node_def).getVelocity()

    def setup_sensors(self):
        sensors = self.get_devices_by_type_list(
            [Node.POSITION_SENSOR, Node.DISTANCE_SENSOR, Node.LIGHT_SENSOR, Node.TOUCH_SENSOR])

        for sensor in sensors:
            sensor.enable(self.sampling_rate)

    def setup_motors(self, index_list: List[int], pos: float):
        motors = self.get_motors()

        for index in index_list:
            motors[index].setPosition(pos)

    def set_motor_velocity(self, index: int, velocity: float):
        self.get_motors()[index].setVelocity(velocity)

    def get_sensor_value(self, node_type: int, index: int) -> float:
        sensors = self.get_devices_by_type(node_type)

        return sensors[index].getValue()

    def get_position_sensor_value(self, index: int) -> float:
        return self.get_sensor_value(Node.POSITION_SENSOR, index)

    def get_distance_sensor_value(self, index: int) -> float:
        return self.get_sensor_value(Node.DISTANCE_SENSOR, index)

    def get_light_sensor_value(self, index: int) -> float:
        return self.get_sensor_value(Node.LIGHT_SENSOR, index)

    def get_touch_sensor_value(self, index: int) -> float:
        return self.get_sensor_value(Node.TOUCH_SENSOR, index)
