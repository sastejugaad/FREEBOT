""" 
This program is part of FREEBOT project.
https://github.com/sastejugaad/FREEBOT/
Part-1 https://www.youtube.com/watch?v=ymNAXm_j8do&t=3s
Part-2 https://www.youtube.com/watch?v=j49aA8wwWxY&ab_channel=SasteJugaad
Part-3 https://www.youtube.com/watch?v=SvNt3h0w55A&ab_channel=SasteJugaad
Ask Help on discord
https://discord.com/invite/fMXvGty
Instagram
https://www.instagram.com/shub_bhatt/
"""

import cv2
import keyboard  # Library for detecting keyboard events
import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define UDP host and port
udp_host = '0.0.0.0'  # Listen on all available network interfaces
udp_port = 12345  # Should be the same as the port in the robot program
BUFFER_SIZE = 1024
sock.bind((udp_host, udp_port))  # Bind the socket to the host and port

# URL for the video stream from the camera (replace with your camera's URL)
url = 'http://192.168.1.27:8080/video'

def on_speed_change(val):
    """Callback function for trackbar change."""
    global robot_speed
    robot_speed = val

# Create a window to display robot control interface
cv2.namedWindow('Robot Control', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Robot Control', 1280, 720)

# Initialize robot_speed with a default value
robot_speed = 40

# Create a trackbar for adjusting robot_speed
cv2.createTrackbar('Speed', 'Robot Control', robot_speed, 255, on_speed_change)

def show_live_camera_feed():
    """Function to display live camera feed and control the robot."""
    global robot_speed  # Declare robot_speed as a global variable
    cap = cv2.VideoCapture(url)  # Open the camera (use 0 for webcam)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Variable to track robot state
    robot_command = "s,0"  # Default command: stop the robot

    while True:
        ret, frame = cap.read()  # Read a frame from the camera

        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Display control instructions on the frame
        text = f"Press 'W' for Forward, 'S' for Backward, 'A' for Left, 'D' for Right | Robot Speed: {robot_speed}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Robot Control', frame)  # Display the frame

        # Update robot_command based on keyboard input
        if keyboard.is_pressed('w'):
            robot_command = f"f,{robot_speed}"  # Move forward
            print(robot_command)
        elif keyboard.is_pressed('s'):
            robot_command = f"b,{robot_speed}"  # Move backward
            print(robot_command)
        elif keyboard.is_pressed('a'):
            robot_command = f"l,{robot_speed}"  # Move left
            print(robot_command)
        elif keyboard.is_pressed('d'):
            robot_command = f"r,{robot_speed}"  # Move right
            print(robot_command)
        elif not any(keyboard._pressed_events):
            robot_command = "s,0"  # Stop the robot if no key is pressed
            print(robot_command)

        # Check for the 'q' key press to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Send the robot command over UDP
        response_message = robot_command
        sock.sendto(response_message.encode("utf-8"), ('192.168.1.37', 12345))  # Send the command to the robot

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function to show the live camera feed and control the robot
show_live_camera_feed()
