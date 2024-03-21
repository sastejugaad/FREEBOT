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
import socket
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define UDP host and port
udp_host = '0.0.0.0'  # Listen on all available network interfaces
udp_port = 12345  # Should be the same as the port in the robot program
BUFFER_SIZE = 1024
sock.bind((udp_host, udp_port))  # Bind the socket to the host and port

url = 'http://192.168.1.27:8080/video' #Replace with your own video url and add /video to the link

# Initialize robot_speed with a default value
robot_speed = 40

# Initialize lower and upper bounds for green color in HSV
lower_green = np.array([40, 40, 40])
upper_green = np.array([70, 255, 255])

# Create a buffer to store past positions of the detected ball
trail_buffer = []

# Rectangle parameters
# Adjust these to change the detection area
rect_width = 400
rect_height = 200
rect_color = (0, 0, 255)  # Red color
rect_thickness = 2

def detect_green_ball(frame):
    """Function to detect a green ball in the frame."""
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Check if any contour is found
    if contours:
        # Get the largest contour (assumed to be the green ball)
        max_contour = max(contours, key=cv2.contourArea)
        
        # Calculate the centroid of the contour
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Return the centroid coordinates and contour area
            return cx, cy, max_contour

    return None, None, None

def show_live_camera_feed():
    """Function to display live camera feed, detect green ball, and control the robot."""
    global robot_speed, lower_green, upper_green, trail_buffer  # Declare global variables
    
    cap = cv2.VideoCapture(0)  # Open the camera (use 0 for webcam)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
       # Set capture properties to 1280x720 resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Create trackbars for adjusting robot_speed and green color threshold
    cv2.namedWindow('Ball Chasing',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Ball Chasing', 1280, 720)  # Resize the window
    cv2.createTrackbar('Speed', 'Ball Chasing', robot_speed, 255, lambda x: None)
    cv2.createTrackbar('Hue', 'Ball Chasing', lower_green[0], 255, lambda x: None)

    while True:
        ret, frame = cap.read()  # Read a frame from the camera

        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Get current values from the trackbars
        robot_speed = cv2.getTrackbarPos('Speed', 'Ball Chasing')
        lower_green[0] = cv2.getTrackbarPos('Hue', 'Ball Chasing')

        # Detect green ball in the frame
        ball_x, ball_y, max_contour = detect_green_ball(frame)
        
        # Create a mask only around the detected green ball
        mask = np.zeros_like(frame)
        if max_contour is not None:
            cv2.drawContours(mask, [max_contour], -1, (255, 255, 255), -1)  # Draw filled contour
            frame = cv2.bitwise_and(frame, mask)

            # Add current position to the trail buffer
            if len(trail_buffer) < 10:
                trail_buffer.append((ball_x, ball_y))
            else:
                trail_buffer.pop(0)
                trail_buffer.append((ball_x, ball_y))

            # Draw trail using past positions from the buffer
            for i in range(1, len(trail_buffer)):
                if trail_buffer[i - 1] is not None and trail_buffer[i] is not None:
                    cv2.line(frame, trail_buffer[i - 1], trail_buffer[i], (0, 255, 0), 2)

        # Draw a bounding box around the detected ball
        if ball_x is not None and ball_y is not None:
            cv2.circle(frame, (ball_x, ball_y), 20, (0, 255, 0), 2)  # Draw a green circle around the ball

            # Calculate diameter of the circle
            diameter = cv2.contourArea(max_contour)
            diameter_text = f"Diameter: {diameter:.2f}"
            
            # Display diameter of the circle
            cv2.putText(frame, diameter_text, (ball_x - 100, ball_y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Display X and Y coordinates of the tracked ball
            cv2.putText(frame, f"X: {ball_x}, Y: {ball_y}", (ball_x - 100, ball_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Draw rectangle in the middle of the screen
        screen_center_x = frame.shape[1] // 2
        screen_center_y = frame.shape[0] // 2
        rect_x1 = screen_center_x - rect_width // 2
        rect_y1 = screen_center_y - rect_height // 2
        rect_x2 = screen_center_x + rect_width // 2
        rect_y2 = screen_center_y + rect_height // 2
        cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), rect_color, rect_thickness)

        # Update robot_command based on ball position
        if ball_x is not None and ball_y is not None:
                # Check if the ball is above the top of the rectangle
            if ball_y < rect_y1:
                 robot_command = f"f,{robot_speed}"  # Move forward
    # Check if the ball is below the bottom of the rectangle
            elif ball_y > rect_y2:
                    robot_command = f"b,{robot_speed}"  # Move backward
    # Check if the ball is inside the rectangle
            else:
                if rect_x1 <= ball_x <= rect_x2:
                 robot_command = "s,0"  # Stop the robot
                elif ball_x < screen_center_x:
                    robot_command = f"l,{(robot_speed+30)}"  # Move left
                else:
                    robot_command = f"r,{(robot_speed+30)}"  # Move right
        else:
            robot_command = "s,0"  # Stop the robot if no ball is detected

        # Print and display robot command
        print("Robot Command:", robot_command)
        cv2.putText(frame, "Robot Command: " + robot_command, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Ball Chasing', frame)  # Display the frame

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

