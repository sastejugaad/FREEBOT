# FREEBOT (Frugal Robot Engineered from Efficient and Budget Optimised Technology)
FREEBOT is an open-source robot that aims to make robotics easy and affordable. This project is great for beginners who want to learn robotics and IoT. We will also implement some basic computer vision concepts. 
Note:- Robot firmware is the same for all the computer version projects that I have shown. Only the python file running on the PC is different so you can refer to the Part-1 of the project to build the FREEBOT.
<img src="https://github.com/sastejugaad/FREEBOT/blob/main/Circuit_diagram_v1.png" width="50%" height="50%">

# Tutorial series
- Part-1 [https://www.youtube.com/watch?v=SvNt3h0w55A&ab_channel=SasteJugaad](https://youtu.be/ymNAXm_j8do?si=0M8imzcQLlhn9ULn)
- Part-2 https://youtu.be/j49aA8wwWxY?si=1lki8r9_ucNTEMC0
- Part-3 https://youtu.be/SvNt3h0w55A?si=uS_L-zJ2iLNq51DY

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

# Ball Chasing Robot

This project is a demonstration of a ball-chasing robot that uses computer vision to track and follow a green ball in its environment. The robot's movement is controlled based on the position of the detected ball relative to a central rectangle in the camera feed. Use `Ball_chasing_robot.py` for this project. In this script I have removed the keyboard control robot will only follow the ball. Adjust the speed and accuracy of ball detection using the sliders.

## Libraries to Install

Before running the program, make sure you have the following libraries installed:

- OpenCV (`opencv-python`)
- NumPy (`numpy`)
- Pillow (`PIL`)

You can install these libraries using pip:
 `pip install opencv-python numpy Pillow`


## How to Run the Program

1. Clone the repository or download the source code files.
2. Ensure you have a camera connected or provide the appropriate URL for accessing the video feed in the script (`url` variable).
3. Connect your robot to the network and note its IP address and the port it listens to.
4. Update the IP address and port in the script (`sock.sendto()` function call).
5. Run the script using Python:
`python ball_chasing_robot.py`


## Step-by-Step Explanation

1. **Initialization**: The script initializes a UDP socket to communicate with the robot and sets up parameters such as the green color range, speed, and buffer for tracking the ball's trail.

2. **Detecting Green Ball**: The `detect_green_ball` function takes a frame from the camera feed, converts it to the HSV color space, applies a color threshold to isolate green pixels, and finds contours representing the green ball.

3. **Live Camera Feed**: The `show_live_camera_feed` function continuously captures frames from the camera feed. It detects the green ball in each frame, draws a bounding box around it, calculates its diameter, and tracks its movement.

4. **Controlling the Robot**: Based on the position of the green ball relative to a central rectangle in the frame, the script determines the appropriate movement command for the robot. Commands include moving forward, backward, left, right, or stopping altogether.

5. **Sending Commands**: The script sends the calculated movement command to the robot over UDP.

6. **User Interaction**: The script provides a graphical interface with trackbars to adjust the robot's speed and the green color threshold for ball detection.

7. **Termination**: The program terminates when the 'q' key is pressed, releasing the camera and closing all OpenCV windows.

By following these steps, you can set up and run the ball-chasing robot project to demonstrate real-time computer vision-based control of a robot.

  
# Add ESP32 to Arduino IDE
https://www.youtube.com/watch?v=mBaS3YnqDaU&ab_channel=RuiSantos

# How to use L298N motor driver
https://www.youtube.com/watch?v=dyjo_ggEtVU&ab_channel=DroneBotWorkshop

# SOCIAL
https://www.youtube.com/channel/UCe5G9yS2XvetGfjfT-O89vw
