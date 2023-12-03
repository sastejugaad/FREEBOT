import cv2
import mediapipe as mp
import math
import socket

robotAddressPort   = ("192.168.137.230", 12345)
# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize VideoCapture
cap = cv2.VideoCapture(0)  # Change the parameter if you have multiple cameras
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set height

# Set the desired window size
cv2.namedWindow('Hand Tracking', cv2.WINDOW_NORMAL)  # Create a resizable window
cv2.resizeWindow('Hand Tracking', 1280, 720)  # Set the window size to 1280x720

# Get the height and width of the frame
#height, width, _ = frame.shape

height = 720
width = 1280
    
# Calculate the coordinates of the center of the screen
center_x = width // 2
center_y = height // 2
    
# Calculate the coordinates of the top left and bottom right corners of the top box
top_box_top_left = (center_x - 100, 0)
top_box_bottom_right = (center_x + 100, 200)
    
# Calculate the coordinates of the top left and bottom right corners of the bottom box
bottom_box_top_left = (center_x - 100, height - 200)
bottom_box_bottom_right = (center_x + 100, height)

while cap.isOpened():
    global turn
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally (mirror image)
    frame = cv2.flip(frame, 1)
    
    # Convert the image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the image with MediaPipe Hands
    results = hands.process(image)
    
    # If hands are detected, annotate the image and label them
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get the hand landmarks
            landmarks = []
            for landmark in hand_landmarks.landmark:
                x, y, _ = image.shape
                landmarks.append((int(landmark.x * y), int(landmark.y * x)))
            
            # Calculate the distances between fingers
            thumb_tip = landmarks[4]  # Thumb tip landmark
            index_tip = landmarks[8]  # Index finger tip landmark
            middle_tip = landmarks[12]  # Middle finger tip landmark
            pinky_tip = landmarks[20]  # Pinky finger tip landmark
            
            # Calculate the distances between fingers
            dist_thumb_index = thumb_tip[0] - index_tip[0]
            dist_index_middle = index_tip[0] - middle_tip[0]
            dist_middle_pinky = middle_tip[0] - pinky_tip[0]
            
            # Determine left or right hand based on finger distances
            if dist_thumb_index < 0 and dist_index_middle < 0 and dist_middle_pinky < 0:
                hand_label = "Right Hand"
            else:
                # Draw a green line from wrist to middle finger MCP
                wrist = landmarks[0]  # Wrist landmark
                middle_mcp = landmarks[9]  # Middle finger MCP landmark
                cv2.line(frame, wrist, middle_mcp, (0, 255, 0), 2)  # Green line
                
                # Calculate angle of rotation
                angle = math.atan2(wrist[1] - middle_mcp[1], wrist[0] - middle_mcp[0])
                angle = math.degrees(angle)
                angle -= 90  # Adjust for top of the screen as zero degrees
                if angle <= -180:
                    angle += 360
                elif angle > 180:
                    angle -= 360
                
                # Display rotation angle on the left side of the screen
                cv2.putText(frame, f"Rotation Angle: {angle:.2f}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
                
                # Check and print on screen based on angle condition
                if angle > 20:
                    hand_label = "Right"
                    turn=True
                    sendTorobot("r")
                elif angle < -20:
                    hand_label = "Left"
                    turn = True
                    sendTorobot("l")
                else:
                    turn = False
                    hand_label = ""


                # Add the logic to check if landmarks 9 and 13 are inside the boxes
                if (top_box_top_left[0] < landmarks[9][0] < top_box_bottom_right[0] and
                    top_box_top_left[1] < landmarks[9][1] < top_box_bottom_right[1]) and \
                    (top_box_top_left[0] < landmarks[13][0] < top_box_bottom_right[0] and
                    top_box_top_left[1] < landmarks[13][1] < top_box_bottom_right[1]):
                    # Display rotation angle on the left side of the screen
                    cv2.putText(frame, f"Forward", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
                    sendTorobot("f")
                    print("Forward")
                elif (bottom_box_top_left[0] < landmarks[9][0] < bottom_box_bottom_right[0] and
                    bottom_box_top_left[1] < landmarks[9][1] < bottom_box_bottom_right[1]) and \
                    (bottom_box_top_left[0] < landmarks[13][0] < bottom_box_bottom_right[0] and
                    bottom_box_top_left[1] < landmarks[13][1] < bottom_box_bottom_right[1]):
                    cv2.putText(frame, f"Back", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
                    sendTorobot("b")
                    print("Back")
                elif turn != True:
                    cv2.putText(frame, f"Stop", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
                    sendTorobot("s")
                    print("Stop")
            
            # Display the label on the frame after flipping
            cv2.putText(frame, hand_label, (landmarks[0][0], landmarks[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    


    # Draw the boxes on the frame with red color and 2 pixels thickness
    cv2.rectangle(frame, top_box_top_left, top_box_bottom_right, (0, 0, 255), 2)
    cv2.rectangle(frame, bottom_box_top_left, bottom_box_bottom_right, (0, 0, 255), 2)
    

    def sendTorobot(move):
        msg4robot = ','.join([move,'100,0,0,0'])
        print(msg4robot)
        bytesToSend         = str.encode(msg4robot)
        bufferSize          = 1024
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPClientSocket.sendto(bytesToSend, robotAddressPort)

    # Display the output
    cv2.imshow('Hand Tracking', frame)
    
    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release resources
cap.release()
cv2.destroyAllWindows()
