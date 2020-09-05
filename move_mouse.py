import time 
  
# a module which has functions related to time.  
# It can be installed using cmd command:  
# pip install time, in the same way as pyautogui. 
import pyautogui
while True: 
    time.sleep(60)  
    
    # makes program execution pause for 10 sec 
    pyautogui.moveTo(1000, 1000, duration = 1) 
    pyautogui.moveTo(1100, 1000, duration = 1) 
    pyautogui.moveTo(1100, 900, duration = 1) 
    pyautogui.moveTo(1000, 900, duration = 1) 
  