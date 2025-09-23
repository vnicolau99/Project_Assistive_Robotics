import time
from math import radians, degrees, pi
import numpy as np
import socket
#from spatialmath.base import * 
from robodk.robolink import *
from robodk.robomath import *


# Robot setup
RDK = Robolink()
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item('Spoon')
Init_target = RDK.Item('Init')
Pick_food_target = RDK.Item('Pick_food')
Move_to_mouth_target = RDK.Item('Move_to_mouth')
Feed_target = RDK.Item('Feed')

robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(20)

# Robot Constants setup
ROBOT_IP = '192.168.1.5'
ROBOT_PORT = 30002
accel_mss = 1.2
speed_ms = 0.75
timel = 4