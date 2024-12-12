import cv2
import numpy as np
import time
import os
import track_hands as TH

# Brush and eraser settings
brush_thickness = 15
eraser_thickness = 100
image_canvas = np.zeros((720, 1280, 3), np.uint8)

# Variables for FPS calculation
currentT = 0
previousT = 0

# Loading header images
header_img = "Images"
header_img_list = os.listdir(header_img)
if len(header_img_list) < 5:
    raise ValueError("Not enough header images in the 'Images' folder. Ensure at least 5 images are present.")

overlay_image = [cv2.imread(f'{header_img}/{i}') for i in header_img_list]

# Setup webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height
cap.set(cv2.CAP_PROP_FPS, 60)

# Default settings
default_overlay = overlay_image[0]
draw_color = (255, 200, 100)
tool_name = "Brush"

# Initialize hand detector
detector = TH.handDetector(min_detection_confidence=0.85)

xp, yp = 0, 0  # Previous coordinates

# Function to add text with background
def add_text_with_bg(img, text, pos, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, text_color=(255, 255, 255), bg_color=(0, 0, 0)):
    text_size = cv2.getTextSize(text, font, font_scale, 2)[0]
    x, y = pos
    cv2.rectangle(img, (x, y - text_size[1] - 10), (x + text_size[0] + 10, y + 5), bg_color, -1)
    cv2.putText(img, text, (x + 5, y - 5), font, font_scale, text_color, 2)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Unable to read frame. Exiting...")
        break

    frame = cv2.flip(frame, 1)

    # Display header overlay
    overlay_region = frame[0:125, 0:1280]
    frame[0:125, 0:1280] = cv2.addWeighted(overlay_region, 0.5, default_overlay, 0.5, 0)

    # Detect hands
    frame = detector.findHands(frame, draw=True)
    landmark_list = detector.findPosition(frame, draw=False)

    if landmark_list:
        x1, y1 = landmark_list[8][1:]  # Index finger tip
        x2, y2 = landmark_list[12][1:]  # Middle finger tip

        my_fingers = detector.fingerStatus()

        if my_fingers[1] and my_fingers[2]:  # Selection mode
            xp, yp = 0, 0
            tool_name = "Selector"
            if y1 < 125:
                if 200 < x1 < 340:
                    default_overlay = overlay_image[0]
                    draw_color = (255, 0, 0)
                    tool_name = "Red Brush"
                elif 340 < x1 < 500:
                    default_overlay = overlay_image[1]
                    draw_color = (47, 225, 245)
                    tool_name = "Blue Brush"
                elif 500 < x1 < 640:
                    default_overlay = overlay_image[2]
                    draw_color = (197, 47, 245)
                    tool_name = "Purple Brush"
                elif 640 < x1 < 780:
                    default_overlay = overlay_image[3]
                    draw_color = (53, 245, 47)
                    tool_name = "Green Brush"
                elif 1100 < x1 < 1280:
                    default_overlay = overlay_image[4]
                    draw_color = (0, 0, 0)
                    tool_name = "Eraser"

            cv2.line(frame, (x1, y1), (x2, y2), draw_color, 3)
            add_text_with_bg(frame, f'Mode: {tool_name}', (900, 680), font_scale=1.5, bg_color=(0, 0, 255))

        elif my_fingers[1] and not my_fingers[2]:  # Drawing mode
            tool_name = "Eraser" if draw_color == (0, 0, 0) else "Brush"
            add_text_with_bg(frame, f'Mode: {tool_name}', (900, 680), font_scale=1.5, bg_color=(0, 255, 0))
            cv2.circle(frame, (x1, y1), 15, draw_color, -1)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # Eraser or brush
            thickness = eraser_thickness if draw_color == (0, 0, 0) else brush_thickness
            cv2.line(frame, (xp, yp), (x1, y1), draw_color, thickness)
            cv2.line(image_canvas, (xp, yp), (x1, y1), draw_color, thickness)

            xp, yp = x1, y1

    else:
        add_text_with_bg(frame, "No hands detected", (10, 50), bg_color=(0, 0, 255))

    # Combine the canvas with the live feed
    img_gray = cv2.cvtColor(image_canvas, cv2.COLOR_BGR2GRAY)
    _, imginv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    imginv = cv2.cvtColor(imginv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, imginv)
    frame = cv2.bitwise_or(frame, image_canvas)

    # Calculate and display FPS
    currentT = time.time()
    fps = 1 / (currentT - previousT)
    previousT = currentT
    add_text_with_bg(frame, f'FPS: {int(fps)}', (10, 670), bg_color=(50, 50, 50))

    # Display the result
    cv2.imshow('Virtual Air Paint', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
