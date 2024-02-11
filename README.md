# FREEBOT (Frugal Robot Engineered from Efficient and Budget Optimised Technology)
Easy to build a robot.

<img src="https://github.com/sastejugaad/FREEBOT/blob/main/Circuit_diagram_v1.png" width="50%" height="50%">

# Handtracker

1. Install python 3.9
2. Install opencv
3. Install mediapipe
4. Download Handtracker.py
5. Get the IP address of FREEBOT
6. Enter in Python program

Hand tracking only works for left-hand.

# Robot Control center
## Robot Control via Live Camera Feed

This Python script captures a live video feed from a camera (either a webcam or a network camera) and allows the user to control a robot using keyboard inputs. The script establishes a UDP connection to send control commands to the robot.

## Prerequisites

- Python installed on your system
- Required libraries installed (`cv2`, `keyboard`)

## Usage

1. Replace `url` with the URL of your camera stream if you're not using a webcam.
2. Adjust `udp_host` and `udp_port` to match the IP address and port of your robot.
3. Run the script.
4. Use the following keyboard keys to control the robot:
   - 'W': Move the robot forward.
   - 'S': Move the robot backward.
   - 'A': Turn the robot left.
   - 'D': Turn the robot right.
   - 'Q': Quit the program.

## How It Works

- The script opens a UDP socket to communicate with the robot.
- It captures frames from the camera and displays them.
- Keyboard inputs are used to control the robot's movement.
- Control commands are sent to the robot via UDP.


# Add ESP32 to Arduino IDE
https://www.youtube.com/watch?v=mBaS3YnqDaU&ab_channel=RuiSantos

# How to use L298N motor driver
https://www.youtube.com/watch?v=dyjo_ggEtVU&ab_channel=DroneBotWorkshop

# SOCIAL
https://www.youtube.com/channel/UCe5G9yS2XvetGfjfT-O89vw
