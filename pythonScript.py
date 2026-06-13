import cv2
import mediapipe as mp
import serial
import time

# ==========================
# ESP32
# ==========================
PORT = "COM5"

esp32 = serial.Serial(PORT, 115200)
time.sleep(2)

# ==========================
# MEDIAPIPE
# ==========================
mpHands = mp.solutions.hands

hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mpDraw = mp.solutions.drawing_utils

tipIds = [4, 8, 12, 16, 20]

# ==========================
# CAMERA
# ==========================
cap = cv2.VideoCapture(0)

glow_radius = 20
glow_dir = 1

pTime = 0

while True:

    success, img = cap.read()

    if not success:
        continue

    img = cv2.flip(img, 1)

    h, w, c = img.shape

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    fingers = [0, 0, 0, 0, 0]
    mode = "NO HAND"
    data = "00000"

    if results.multi_hand_landmarks:

        handType = results.multi_handedness[0].classification[0].label

        for handLms in results.multi_hand_landmarks:

            lmList = []

            xmin = w
            ymin = h
            xmax = 0
            ymax = 0

            for id, lm in enumerate(handLms.landmark):

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                lmList.append((cx, cy))

                xmin = min(xmin, cx)
                ymin = min(ymin, cy)

                xmax = max(xmax, cx)
                ymax = max(ymax, cy)

            # ==========================
            # BOUNDING BOX
            # ==========================

            cv2.rectangle(
                img,
                (xmin - 20, ymin - 20),
                (xmax + 20, ymax + 20),
                (0, 255, 255),
                2
            )

            # ==========================
            # THUMB
            # ==========================

            # THUMB DETECTION

            if handType == "Right":

                if lmList[4][0] < lmList[3][0]:
                    fingers[0] = 1

            else:

                if lmList[4][0] > lmList[3][0]:
                    fingers[0] = 1

            # ==========================
            # OTHER FINGERS
            # ==========================

            for i in range(1, 5):

                if lmList[tipIds[i]][1] < lmList[tipIds[i] - 2][1]:
                    fingers[i] = 1

            fingerCount = sum(fingers)

            data = ''.join(map(str, fingers))

            print("Hand:", handType)
            print("Fingers:", fingers)
            print("Sending:", data)

            # ==========================
            # SERIAL
            # ==========================

            if data == "111111":

                esp32.write(b"ANIMATION1\n")
                mode = "OPEN PALM"

            elif data == "000000":

                esp32.write(b"ANIMATION2\n")
                mode = "FIST"

            else:

                esp32.write((data + "\n").encode())
                mode = "LED CONTROL"

            # ==========================
            # LANDMARKS
            # ==========================

            mpDraw.draw_landmarks(
                img,
                handLms,
                mpHands.HAND_CONNECTIONS
            )

    # ==========================
    # GLOW EFFECT
    # ==========================

    glow_radius += glow_dir

    if glow_radius > 30:
        glow_dir = -1

    if glow_radius < 20:
        glow_dir = 1

    # ==========================
    # TEXT
    # ==========================

    cv2.putText(
        img,
        f"MODE: {mode}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.putText(
        img,
        f"FINGERS: {sum(fingers)}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        img,
        f"DATA: {data}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # ==========================
    # LED PANEL
    # ==========================

    cv2.rectangle(
        img,
        (10, 150),
        (300, 400),
        (40, 40, 40),
        -1
    )

    cv2.putText(
        img,
        "LED STATUS",
        (80, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    for i in range(5):

        x = 70
        y = 220 + (i * 35)

        if fingers[i]:

            cv2.circle(
                img,
                (x, y),
                glow_radius,
                (0, 80, 0),
                -1
            )

            cv2.circle(
                img,
                (x, y),
                15,
                (0, 255, 0),
                -1
            )

            status = "ON"
            color = (0, 255, 0)

        else:

            cv2.circle(
                img,
                (x, y),
                15,
                (60, 60, 60),
                -1
            )

            status = "OFF"
            color = (0, 0, 255)

        cv2.putText(
            img,
            f"LED{i+1}: {status}",
            (110, y + 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    # ==========================
    # FPS
    # ==========================

    cTime = time.time()

    fps = 1 / (cTime - pTime) if pTime else 0

    pTime = cTime

    cv2.putText(
        img,
        f"FPS: {int(fps)}",
        (w - 140, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.imshow("ESP32 Gesture LED Control", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
esp32.close()
cv2.destroyAllWindows()