from robodk import robolink, robomath
import time, socket

# --- Connect to RoboDK ---
RDK = robolink.Robolink()
robot = RDK.Item('UR5e')
tool = RDK.Item('Hand')
base = RDK.Item('UR5e Base')
robot.setPoseFrame(base)
robot.setTool(tool)

# --- Targets ---
init = RDK.Item('Init')
app_plate = RDK.Item('App_plate')
pick_food = RDK.Item('Pick_Food')
out_plate = RDK.Item('Out_plate')
app_mouth = RDK.Item('App_mouth')
in_mouth = RDK.Item('In_mouth')

# --- UR5e real robot connection ---
ROBOT_IP = "192.168.1.5"
ROBOT_PORT = 30002
robot_socket = None

# Motion params
accel_mss = 1.2
speed_ms = 0.25
timel = 4
timej = 6

# --- URScript commands ---
set_tcp = "set_tcp(p[0.000000,0.000000,0.050000,0.000000,0.000000,0.000000])"

# Define positions (joint values or p[] depending on your needs)
movej_init = f"movej([-1.57, -1.2, -1.8, 2.9, -1.57, 0], {accel_mss}, {speed_ms}, {timej}, 0.0)"
movel_app_plate = f"movel(p[0.3, -0.2, 0.15, 0, 3.14, 0], {accel_mss}, {speed_ms}, {timel}, 0.0)"
movel_pick_food = f"movel(p[0.3, -0.2, 0.05, 0, 3.14, 0], {accel_mss}, {speed_ms}, {timel}, 0.0)"
movel_out_plate = f"movel(p[0.3, -0.1, 0.15, 0, 3.14, 0], {accel_mss}, {speed_ms}, {timel}, 0.0)"
movel_app_mouth = f"movel(p[0.4, 0.0, 0.15, 0, 3.14, 0], {accel_mss}, {speed_ms}, {timel}, 0.0)"
movel_in_mouth = f"movel(p[0.4, 0.0, 0.05, 0, 3.14, 0], {accel_mss}, {speed_ms}, {timel}, 0.0)"

# --- Socket helpers ---
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

# --- Feeding sequence ---
def Feeding():
    print("Feeding sequence...")
    # --- Simulation ---
    robot.MoveJ(init)
    robot.MoveJ(app_plate)
    robot.MoveL(pick_food)
    time.sleep(1.0)
    robot.MoveL(out_plate)
    robot.MoveL(app_mouth)
    robot.MoveL(in_mouth)
    time.sleep(3.0)
    robot.MoveL(app_mouth)
    robot.MoveJ(app_plate)

    # --- Real robot ---
    if robot_is_connected:
        send_ur_script(set_tcp)
        wait_robot(1)
        send_ur_script(movej_init)
        wait_robot(timej)

        send_ur_script(movel_app_plate)
        wait_robot(timel)
        send_ur_script(movel_pick_food)
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

# --- Main ---
def main():
    global robot_is_connected
    robot_is_connected = check_robot_port(ROBOT_IP, ROBOT_PORT)

    Feeding()

    if robot_is_connected:
        robot_socket.close()

if __name__ == "__main__":
    main()

