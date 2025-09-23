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


def check_robot_port(ROBOT_IP, ROBOT_PORT):
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(1)
        robot_socket.connect((ROBOT_IP, ROBOT_PORT)) 
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def send_ur_script(command):
    robot_socket.send(("{}\n".format(command)).encode())

def receive_response(t):
    try:
        print("Waiting time: " + str(t))
        time.sleep(t)       
    except socket.error as e:
        print(f"Error receiving data from the robot: {e}")
        exit(1)

def Init():
    print("Init")
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")

def Pick_food():
    print("Picking food")
    robot.MoveL(Pick_food_target, True)
    print("Food picked")

def Move_to_mouth():
    print("Moving to mouth")
    robot.MoveL(Move_to_mouth_target, True)
    print("At mouth position")

def Feed():
    print("Feeding")
    robot.MoveL(Feed_target, True)
    print("Feeding done")

def main():
    global robot_is_connected
    robot_is_connected = check_robot_port(ROBOT_IP, ROBOT_PORT)
    Init()
    Pick_food()
    Move_to_mouth()
    Feed()
    if robot_is_connected:
        robot_socket.close()

if __name__ == "__main__":
    main()