import os
import time
import tkinter as tk
from tkinter import messagebox
from robodk.robolink import *
from robodk.robomath import *

# Define relative path to the .rdk file
relative_path = "src/roboDK/Assistive_UR5e.rdk"
absolute_path = os.path.abspath(relative_path)

# Start RoboDK with the project file
RDK = Robolink()
RDK.AddFile(absolute_path)

# Retrieve items from the RoboDK station
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


# Set robot frame, tool and speed
robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(50)

# Connect to real robot or simulate
def robot_online(online):
    if online:
        robot.setConnectionParams('192.168.1.5', 30000, '/', 'anonymous', '')
        time.sleep(5)
        success = robot.ConnectSafe('192.168.1.5')
        time.sleep(5)
        status, status_msg = robot.ConnectedState()
        if status != ROBOTCOM_READY:
            raise Exception("Failed to connect: " + status_msg)
        RDK.setRunMode(RUNMODE_RUN_ROBOT)
        print("Connection to UR5e Successful!")
    else:
        RDK.setRunMode(RUNMODE_SIMULATE)
        print("Simulation mode activated.")

# Robot movements
def Init():
    print("Init")
    robot.setSpeed(20)
    robot.MoveL(Init_target, True)
    print("Init_target REACHED")
    

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

# Confirmation dialog to close RoboDK
def confirm_close():
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askquestion(
        "Close RoboDK",
        "Do you want to save changes before closing RoboDK?",
        icon='question'
    )
    if response == 'yes':
        RDK.Save()
        RDK.CloseRoboDK()
        print("RoboDK saved and closed.")
    else:
        RDK.CloseRoboDK()
        print("RoboDK closed without saving.")

# Main function
def main():
    robot_online(False)  # True for real robot, False for simulation
    move_to_init()
    hand_shake()
    give_me_5()

# Run main and handle closing
if __name__ == "__main__":
    main()
    #confirm_close()
