import cv2
import mediapipe as mp
import json

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Open video
cap = cv2.VideoCapture('jasminnetw.mp4')  # Use the path to your video

# Set desired resolution (width, height)
frame_width = 720  # Example width
frame_height = 480  # Example height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# Open file for writing JSON data
with open('hand_pose_data.json', 'w') as f:
    # Begin writing an empty list for the hand pose data
    json.dump([], f)

# Create a list for storing hand pose data in real-time
hand_pose_data = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            landmarks = []
            for landmark in hand_landmarks.landmark:
                landmarks.append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z
                })
            hand_pose_data.append(landmarks)

    # Optional: Draw landmarks on the video
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the frame (optional, for debugging)
    cv2.imshow('Hand Pose Estimation', frame)

    # Save the hand pose data to the JSON file after each frame (real-time)
    with open('hand_pose_data.json', 'r+') as f:
        # Read existing data
        existing_data = json.load(f)
        # Add new hand pose data
        existing_data.append(hand_pose_data)
        # Move file pointer to the start to overwrite with updated data
        f.seek(0)
        # Write updated data back to file
        json.dump(existing_data, f)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

