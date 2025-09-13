from robodk.robolink import *
from robodk.robomath import *

# Robot setup
RDK = Robolink()
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item('Hand')
Init_target = RDK.Item('Init')
App_shake_target = RDK.Item('App_shake')
Shake_target = RDK.Item('Shake')
App_give5_target = RDK.Item('App_give5')
Give5_target = RDK.Item('Give5')

robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(50)

def Robot_online(online):
    RUN_ON_ROBOT = online
    if RUN_ON_ROBOT:
        robot.setConnectionParams('192.168.1.5',30000,'/', 'anonymous','')
        time.sleep(5)
        success = robot.ConnectSafe('192.168.1.5') # Try to connect once
        time.sleep(5)
        status, status_msg = robot.ConnectedState()
        if status != ROBOTCOM_READY: # Stop if the connection did not succeed
            #print(status_msg)
            raise Exception("Failed to connect: " + status_msg)
        RDK.setRunMode(RUNMODE_RUN_ROBOT)
        print("Connection to UR5e Successful!")
        # This will set to run the API programs on the robot and the simulator (online programming)
    else:
        RDK.setRunMode(RUNMODE_SIMULATE) 
        print("Simulation!")
        # This will run the API program on the simulator (offline programming)  
def Init():
    print("Init")
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")
def Hand_shake():
    print("Hand Shake")
    robot.setSpeed(50)
    robot.MoveL(App_shake_target, True)
    robot.setSpeed(100)
    robot.MoveL(Shake_target, True)
    robot.MoveL(App_shake_target, True)
    print("Hand Shake FINISHED")
def Give_me_5():
    print("Give me 5!")
    robot.setSpeed(50)
    robot.MoveL(App_give5_target, True)
    robot.setSpeed(100)
    robot.MoveL(Give5_target, True)
    robot.MoveL(App_give5_target, True)
    print("Give me 5! FINISHED")
# Main function
def main():
    Robot_online(False) # True for real robot, False for simulation
    Init()
    Hand_shake()
    Give_me_5()  
if __name__ == "__main__":
    main()
