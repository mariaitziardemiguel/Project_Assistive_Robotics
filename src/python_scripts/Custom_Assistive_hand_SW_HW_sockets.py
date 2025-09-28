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
tool = RDK.Item('Hand')

Init_target = RDK.Item('Init')
App_wave_target = RDK.Item('App_wave')
Wave_target = RDK.Item('Wave')
Bajada_target = RDK.Item('Bajada')
Subida_target = RDK.Item('Subida')
Bajada2_target = RDK.Item('Bajada2')
Dab1_target = RDK.Item('Dab1')
Dab2_target = RDK.Item('Dab2')
Dab3_target = RDK.Item('Dab3')
Dab4_target = RDK.Item('Dab4')
Dab5_target = RDK.Item('Dab5')
Stop_target = RDK.Item('Stop')
Go1_target = RDK.Item('Go1')
Go2_target = RDK.Item('Go2')
Go3_target = RDK.Item('Go3')
Emergency1_target = RDK.Item('Emergency1')
Emergency2_target = RDK.Item('Emergency2')
Emergency3_target = RDK.Item('Emergency3')
RCP_up_target = RDK.Item('RCP_up')
RCP_down_target = RDK.Item('RCP_down')
Out_target = RDK.Item('Out')
In_target = RDK.Item('In')

robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(20)

# Robot Constants setup
ROBOT_IP = '192.168.1.5'
ROBOT_PORT = 30002 # Default port for UR robots
accel_mss = 1.2
speed_ms = 0.75
blend_r = 0.0
timej = 6 # seconds to finish movej
timel = 4 # seconds to finish movel

# Define robot movement commands as URScript strings
set_tcp="set_tcp(p[0.000000, 0.000000, 0.050000, 0.000000, 0.000000, 0.000000])"
movej_init = f"movej([0, -0.4, 0.5, 1.571, 0, 0.000000],1.20000,0.75000,{timel},0.0000)"
movel_app_wave = f"movel([0, -0.68, 0.5, 1.571, 0.000000, 0.000000],{accel_mss},{speed_ms},{timel},0.000)"
movel_wave = f"movel([0, -0.68, 0.5, -2.182, 0, -1.993],{accel_mss},{speed_ms},{timel/2},0.000)"
movel_bajada = f"movel([0.2, -0.68, 0.3, 2.819, 0, 0.940],{accel_mss},{speed_ms},{timel},0.000)"
movel_subida = f"movel([0.4, -0.68, 0.3, 1.366, 0.180, 2.688],{accel_mss},{speed_ms},{timel},0.000)"
movel_bajada2 = f"movel([0.6, -0.68, 0.3, 2.514, 0.061, 1.593],{accel_mss},{speed_ms},{timel},0.000)"

# Initialize UR5e socket communication
def check_robot_port(ROBOT_IP, ROBOT_PORT):
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(1)  # Tiempo de espera de 1 segundo
        robot_socket.connect((ROBOT_IP, ROBOT_PORT)) 
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
# Send commands to the UR5e robot using socket communication
def send_ur_script(command):
    robot_socket.send(("{}\n".format(command)).encode())

# Wait for robot response
def receive_response(t):
    try:
        print("Waiting time: " + str(t))
        time.sleep(t)       
    except socket.error as e:
        print(f"Error receiving data from the robot: {e}")
        exit(1) #Non-zero exit status code to indicate the error

# Movements
def Init():
    print("Init")
    robot.setSpeed(20)
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")
    if robot_is_connected:
        # Set the TCP pose
        print("Init REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movej_init)
        receive_response(timej)
    else:
        print("UR5e is not connected. Only simulation will take place")

def Hand_wave():
    print("Hand Wave")
    robot.setSpeed(40)
    robot.MoveL(App_wave_target, True)
    robot.setSpeed(10)
    robot.MoveL(Wave_target, True)
    robot.setSpeed(30)
    robot.MoveL(Bajada_target, True)
    robot.MoveL(Subida_target, True)
    robot.MoveL(Bajada2_target, True)
    print("Hand Wave FINISHED")
    if robot_is_connected:
        # Set the TCP pose
        print("App_shake REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movel_app_wave)
        receive_response(timel)
        send_ur_script(movel_wave)
        receive_response(timel)
        send_ur_script(movel_bajada)
        receive_response(timel)
        send_ur_script(movel_subida)
        receive_response(timel)
        send_ur_script(movel_bajada2)
        receive_response(timel)
    else:
        print("UR5e is not connected. Only simulation will take place")

def Dab():
    print("Dab!")
    robot.MoveL(Dab1_target, True)
    robot.MoveL(Dab2_target, True)
    robot.MoveL(Dab3_target, True)
    robot.MoveL(Dab4_target, True)
    robot.setSpeed(30)
    robot.MoveL(Dab5_target, True)
    print("Dab! FINISHED")

def Stop_and_go():
    print("Stop and go")
    robot.MoveL(Stop_target, True)
    time.sleep(2)
    robot.MoveL(Go1_target, True)
    robot.setSpeed(50)
    robot.MoveL(Go2_target, True)
    robot.MoveL(Go3_target, True)
    robot.MoveL(Go2_target, True)
    robot.MoveL(Go3_target, True)
    print("Stop and go FINISHED")

def Emergency():
    print("Emergency")
    robot.setSpeed(40)
    robot.MoveL(Emergency1_target, True)
    robot.setSpeed(90)
    robot.MoveL(Emergency2_target, True)
    robot.MoveL(Emergency3_target, True)
    robot.MoveL(Emergency2_target, True)
    robot.MoveL(Emergency1_target, True)
    print("Emergency FINISHED")

def RCP():
    print("Starting RCP...")
    robot.setSpeed(20)
    robot.MoveL(RCP_up_target, True)
    robot.setSpeed(100)
    cycles = 6
    for i in range(cycles):
        print(f"Compression {i+1}")
        robot.MoveL(RCP_down_target, True)
        robot.MoveL(RCP_up_target, True)
    print("RCP FINISHED")

#def Heimlich():
    #print("Heimlich")
    #robot.setSpeed(20)
    #robot.MoveL(Out_target, True)
    #robot.setSpeed(100)
    #robot.MoveL(In_target, True)
    #robot.setSpeed(20)
    #robot.MoveL(Out_target, True)
    #robot.setSpeed(100)
    #robot.MoveL(In_target, True)
    #robot.setSpeed(20)
    #robot.MoveL(Out_target, True)
    #print("Heimlich FINISHED")

# Main function
def main():
    global robot_is_connected
    robot_is_connected=check_robot_port(ROBOT_IP, ROBOT_PORT)
    Init()
    Hand_wave()
    Dab()
    time.sleep(1)
    Init()
    time.sleep(1)
    Stop_and_go()
    time.sleep(1)
    Init()
    time.sleep(1)
    Emergency()
    time.sleep(1)
    RCP()
    time.sleep(1)
    Init()
    #time.sleep(1)
    #Heimlich()
    #time.sleep(1)
    #Init()
    if robot_is_connected:
        robot_socket.close()   

# Run and close
if __name__ == "__main__":
    main()
    #confirm_close()