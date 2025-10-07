from robodk import robolink, robomath
import time, socket
import numpy as np

# Connection to RoboDK
RDK = robolink.Robolink()
robot = RDK.Item('UR5e')
tool = RDK.Item('Hand')
base = RDK.Item('UR5e Base')
robot.setPoseFrame(base)
robot.setTool(tool)

# Targets
init = RDK.Item('Init')
app_plate = RDK.Item('App_plate')
pick_food = RDK.Item('Pick_Food')
pick_food_2 = RDK.Item('Pick_Food_2')
pick_food_3 = RDK.Item('Pick_Food_3')
out_plate = RDK.Item('Out_plate')
app_mouth = RDK.Item('App_mouth')
in_mouth = RDK.Item('In_mouth')

# UR5e real robot connection
ROBOT_IP = "192.168.1.5"
ROBOT_PORT = 30002
robot_socket = None

# Motion parameters
accel_mss = 1.2
speed_ms = 0.25
timel = 4
timej = 6

# URScript TCP definition
set_tcp = "set_tcp(p[0.000000,0.000000,0.050000,0.000000,0.000000,0.000000])"

# Helper function to convert joint targets to URScript
def joints_to_urscript(item, move_type="movel"):
    angs = np.radians(item.Joints())
    angsr = list(angs[0])
    return f"{move_type}({angsr}, {accel_mss}, {speed_ms},{timel},0.0)"

# URScript commands for each pose
movej_init = joints_to_urscript(init, "movej")
movel_app_plate = joints_to_urscript(app_plate)
movel_pick_food = joints_to_urscript(pick_food)
movel_pick_food_2 = joints_to_urscript(pick_food_2)
movel_pick_food_3 = joints_to_urscript(pick_food_3)
movel_out_plate = joints_to_urscript(out_plate)
movel_app_mouth = joints_to_urscript(app_mouth)
movel_in_mouth = joints_to_urscript(in_mouth)

# Socket management
def check_robot_port(ip, port):
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(1)
        robot_socket.connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def send_ur_script(command):
    robot_socket.send((command + "\n").encode())

def wait_robot(t):
    time.sleep(t)

# Feeding sequence
def Feeding():
    print("Feeding sequence...")

    # --- Simulation in RoboDK ---
    robot.MoveJ(init)
    robot.MoveJ(app_plate)
    robot.MoveL(pick_food)
    robot.MoveC(pick_food_2, pick_food_3)  # circular scooping motion
    time.sleep(1.0)
    robot.MoveL(out_plate)
    robot.MoveL(app_mouth)
    robot.MoveL(in_mouth)
    time.sleep(3.0)
    robot.MoveL(app_mouth)
    robot.MoveJ(app_plate)

    # --- Real robot execution (URScript) ---
    if robot_is_connected:
        send_ur_script(set_tcp)
        wait_robot(1)
        send_ur_script(movej_init)
        wait_robot(timej)

        send_ur_script(movel_app_plate)
        wait_robot(timel)
        send_ur_script(movel_pick_food)
        wait_robot(timel)
        # Circular move simulated with two linear segments
        send_ur_script(movel_pick_food_2)
        wait_robot(timel)
        send_ur_script(movel_pick_food_3)
        wait_robot(2)
        send_ur_script(movel_out_plate)
        wait_robot(timel)
        send_ur_script(movel_app_mouth)
        wait_robot(timel)
        send_ur_script(movel_in_mouth)
        wait_robot(3)
        send_ur_script(movel_app_mouth)
        wait_robot(timel)
        send_ur_script(movel_app_plate)
        wait_robot(timel)
    else:
        print("UR5e not connected → Simulation only")

# Main
def main():
    global robot_is_connected
    robot_is_connected = check_robot_port(ROBOT_IP, ROBOT_PORT)

    Feeding()

    if robot_is_connected:
        robot_socket.close()

if __name__ == "__main__":
    main()
