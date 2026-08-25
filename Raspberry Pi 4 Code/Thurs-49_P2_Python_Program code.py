## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import sys
sys.path.append('../')

from Common_Libraries.p2_sim_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()
update_thread = repeating_timer(2, update_sim)

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

#Marisa Patel and Zein Deeb
#defining bin_location

def bin_location(container_ID):
    if container_ID == 1: #small red container
        bin_loc = [-0.581,0.241,0.47]
    elif container_ID == 2:#small green container
        bin_loc = [0.0,-0.629,0.47]
    elif container_ID == 3:#small blue container
        bin_loc = [0.0,0.629,0.47]
    elif container_ID == 4:#large red container
        bin_loc = [-0.4, 0.18, 0.35]
    elif container_ID == 5:#large green container
        bin_loc = [0.0, -0.44, 0.354]
    elif container_ID == 6:#large blue container
        bin_loc = [0, 0.44, 0.354]
    return bin_loc

#Jingting Su
#defining the end effector function

def move_end_effector (container_ID,location):
    while True :
        L = arm.emg_left()
        R = arm.emg_right()
                
        if L > 0.5 and R == 0  : #checking the L and R value
            arm.move_arm(0.406, 0.0, 0.483) #go to home position first
            time.sleep(0.5)
            arm.move_arm (location[0],location[1],location[2])
            break


        
#Marisa Patel, Zein Deeb and Jingting Su
# defining the function to open/close the drawer

def control_drawer(flag,container_ID):
    while True :
        L = arm.emg_left()
        R = arm.emg_right()
        if L == 0 and R > 0.5 and container_ID >= 4 : #checking the L and R value
            if container_ID == 4 :
                arm.open_red_autoclave(flag)
            elif container_ID == 5 :
                arm.open_green_autoclave(flag)
            elif container_ID == 6 :
                arm.open_blue_autoclave(flag)
            break
        elif  container_ID < 4:#checking if the drawer should open
            break


#Marisa Patel, Zein Deeb and Jingting Su
#defining the function to control gripper
        
def control_gripper(flag):
    while True:
        L = arm.emg_left()
        R = arm.emg_right()
        if L > 0.5 and R > 0.5 : #checking the L and R value
            if flag == True:
                arm.control_gripper(-40)
            elif flag == False :
                arm.control_gripper(40)
            break
    
#Marisa Patel, Zein Deeb and Jingting Su         
#calling the main function to start the task
        
def main() :
    import random
    L = arm.emg_left()
    R = arm.emg_right()
    pick_location =  [0.534, 0.0, 0.035]#container's pickup location
    home_location = [0.406, 0.0, 0.483]
    my_list = [1,2,3,4,5,6]
    i = 0
    while i < 6 : 
            ID = random.sample(my_list,1) # randomly picking one item in my_list  and put it in to ID
            container_ID = ID[0] # picking the first item in ID 
            i = i+1
            my_list.remove(ID[0])#removing the item to avoid repetition
            arm.spawn_cage(container_ID) #spawning the conatiner
            print("The container ID selected is:", container_ID)
            move_end_effector(container_ID,pick_location)
            print("Move to the pick up location:",pick_location)
            control_gripper(False) #close the gripper to pick up container
            bin_loc = bin_location(container_ID)
            move_end_effector(container_ID,bin_loc)
            print("Move to the bin location:", bin_loc)
            control_drawer(True,container_ID) #if the container is large, open the drawer
            control_gripper(True) # open the gripper to drop off container
            control_drawer(False,container_ID)#if the container is large, close the drawer
            move_end_effector(container_ID,home_location)
            print("Move to the home location:", home_location)
            time.sleep(1.5) #avoid interfacing the arm and conatiner
    print("The program will terminate.")
                       
main()
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
