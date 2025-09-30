from robodk import robolink, robomath
import time

# Conectar con RoboDK
RDK = robolink.Robolink()

# Obtener referencias al robot y la herramienta
robot = RDK.Item('UR5e')
tool = RDK.Item('Hand')
robot.setTool(tool)

# Obtener targets
init = RDK.Item('Init')
app_plate = RDK.Item('App_plate')
pick_food = RDK.Item('Pick_Food')
out_plate = RDK.Item('Out_plate')
app_mouth = RDK.Item('App_mouth')
in_mouth = RDK.Item('In_mouth')

# --- PROGRAMA FEEDING ---
def Feeding():
    robot.setPoseFrame(RDK.Item('UR5e Base'))   # Sistema de referencia
    robot.setTool(tool)                         # Herramienta activa
    
    robot.MoveJ(init)
    robot.MoveJ(app_plate)
    robot.MoveL(pick_food)
    time.sleep(1.0)  # Pausa 1 s
    
    robot.MoveL(out_plate)
    robot.MoveL(app_mouth)
    robot.MoveL(in_mouth)
    time.sleep(3.0)  # Pausa 3 s
    
    robot.MoveL(app_mouth)
    robot.MoveJ(app_plate)

# --- PROGRAMA PRINCIPAL ---
def MainProgram():
    robot.setSpeed(600)     # Velocidad en mm/s
    Feeding()
    time.sleep(4.0)         # Pausa 4 s
    robot.MoveJ(init)

# Ejecutar el programa principal
MainProgram()
