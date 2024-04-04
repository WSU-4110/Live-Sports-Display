#==========================================================
#
# Title:      RemoteDesktop
# Author:     Timothy Kosinski
# Date:       04APR2024
# Description:
#
# Testing the Remote Desktop via Python remote login. This script logs into a
# Raspberry Pi via SSH and runs a Python script to control an LED matrix display.
# The user can interrupt the display script by entering '1'.
# Creating a secure tunnel using PiTunnel services
#==========================================================

import paramiko
import time

# SSH connection parameters adjusted for PiTunnel access
hostname = 'us2.pitunnel.com'  # Updated to the PiTunnel domain
username = 'timkosinski'  # Raspberry Pi username remains the same
password = '20010972'  # Raspberry Pi password remains the same
port = 56019  # Updated to the custom tunnel port provided by PiTunnel

# Command to run on the Raspberry Pi remains unchanged
execute_command = (
    "cd /home/timkosinski/rpi-rgb-led-matrix/bindings/python/samples/ && "
    "sudo python3 Sports.py --led-gpio-mapping=adafruit-hat --led-rows=64 "
    "--led-cols=64 -c 2 -P 1 -b 100 --led-scan-mode=1 --led-slowdown-gpio 2"
)

try:
    # Initialize the SSH client with updated settings for PiTunnel access
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=username, password=password)

    # Execute the Python script with TTY, the rest of the execution flow remains unchanged
    stdin, stdout, stderr = client.exec_command(execute_command, get_pty=True)

    # Wait for user input to end the program
    interrupt = input("Press '1' then 'Enter' to end the program: ")

    # Check if user wants to send Ctrl+C
    if interrupt.strip() == '1':
        stdin.write('\x03')  # Send Ctrl+C (SIGINT)
        stdin.flush()
        time.sleep(1)

    # Read the output and error if needed
    print(stdout.read().decode())
    print(stderr.read().decode())

finally:
    # Close SSH Session
    client.close()

print("Done")