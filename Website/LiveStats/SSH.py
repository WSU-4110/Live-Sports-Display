#==========================================================
#
# Title:      RemoteDesktop
# Author:     Timothy Kosinski
# Date:       05MAR2024
# Description:
#
# Testing the Remote Desktop via Python remote login. This program logs into a
# Raspberry Pi via SSH and runs a Python script to control an LED matrix display.
# The user can interrupt the display script by entering '1'.
#==========================================================


import paramiko
import time
def run_stacked_display():
    print (testing)
   # return "Stacked display command executed"
    

#    # SSH connection parameters
 #   hostname = '192.168.1.49'
  #  username = 'timkosinski'
   # password = '20010972'
#    port = 22  # SSH port default is 22
    
#    # Command to run on the Raspberry Pi
#    execute_command = (
#        "cd /home/timkosinski/rpi-rgb-led-matrix/bindings/python/samples/ && "
#        "sudo python3 Sports.py --led-gpio-mapping=adafruit-hat --led-rows=64 "
#        "--led-cols=64 -c 2 -P 1 -b 100 --led-scan-mode=1 --led-slowdown-gpio 2"
#    )
#    
#    try:
#        # Initialize the SSH client
#        client = paramiko.SSHClient()
#        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#        client.connect(hostname, port=port, username=username, password=password)
#    
##        # Execute a Python script with TTY
#        stdin, stdout, stderr = client.exec_command(execute_command, get_pty=True)
#    
#        # Wait for user input to end the program
#        interrupt = input("Press '1' then 'Enter' to end the program: ")
#    
#        # Check if user wants to send Ctrl+C
#        if interrupt.strip() == '1': 
#            stdin.write('\x03')  # Send Ctrl+C (SIGINT)
#            stdin.flush()
#            time.sleep(1)  
#    
#    
#        print(stdout.read().decode())
#        print(stderr.read().decode())
#    
#    finally:
#        # Close SSH Connection
#        client.close()
#    
#    return "Stacked display command executed successfully."
