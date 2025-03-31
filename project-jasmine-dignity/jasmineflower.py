import cv2
import mediapipe as mp
import json

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Open video
cap = cv2.VideoCapture('your_video.mp4')  # Use the path to your video

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

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save the hand pose data to JSON
with open('hand_pose_data.json', 'w') as f:
    json.dump(hand_pose_data, f)

cap.release()
cv2.destroyAllWindows()

