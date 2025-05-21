import cv2
import mediapipe as mp
import serial
import time

# === SERIAL SETUP ===
arduino = serial.Serial('COM3', 9600)  # Change to your Arduino port if needed
time.sleep(2)

# === HAND TRACKING SETUP ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# === CAMERA SETUP ===
cap = cv2.VideoCapture(0)

# Label fingertips for visual debugging
label_map = {
    4: "Thumb",
    8: "Index",
    12: "Middle",
    16: "Ring",
    20: "Pinky"
}

last_sent = ""

def count_fingers(hand_landmarks):
    fingers = []
    tip_ids = [4, 8, 12, 16, 20]

    # Thumb (check horizontal movement)
    fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x else 0)

    # Index to Pinky (check vertical)
    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y - 0.02:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def is_only_middle_raised(fingers, landmarks):
    if fingers == [0, 0, 1, 0, 0]:
        return True

    mid_tip = landmarks[12].y
    mid_joint = landmarks[10].y
    index_tip = landmarks[8].y
    ring_tip = landmarks[16].y
    pinky_tip = landmarks[20].y
    thumb_tip = landmarks[4].x
    thumb_joint = landmarks[3].x

    is_middle_raised = mid_tip < mid_joint
    is_others_down = (
        index_tip > landmarks[6].y and
        ring_tip > landmarks[14].y and
        pinky_tip > landmarks[18].y and
        abs(thumb_tip - thumb_joint) < 0.03
    )

    return is_middle_raised and is_others_down

while True:
    success, img = cap.read()
    if not success:
        continue

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    h, w, _ = img.shape

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # Draw finger labels
            for id in label_map:
                cx = int(handLms.landmark[id].x * w)
                cy = int(handLms.landmark[id].y * h)
                cv2.putText(img, label_map[id], (cx - 20, cy - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            fingers = count_fingers(handLms)
            total = sum(fingers)

            if is_only_middle_raised(fingers, handLms.landmark):
                if last_sent != "MIDDLE":
                    arduino.write("MIDDLE\n".encode())
                    last_sent = "MIDDLE"
                    print("🖕 Middle finger detected – Sending: MIDDLE")
            else:
                if last_sent != str(total):
                    arduino.write(f"{total}\n".encode())
                    last_sent = str(total)
                    print(f"✋ {total} finger(s) up – Sending: {total}")
    else:
        # No hand detected → show "0"
        if last_sent != "0":
            arduino.write("0\n".encode())
            last_sent = "0"
            print("🙈 No hand detected – Sending: 0")

    cv2.imshow("Hand Tracker", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
