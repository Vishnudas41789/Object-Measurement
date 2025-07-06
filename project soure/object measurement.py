import cv2
import numpy as np

KNOWN_WIDTH_CM = 5.0  # Width of reference object (e.g. card)
pixels_per_cm = None

def is_rectangle(approx):
    return len(approx) == 4 and cv2.isContourConvex(approx)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))  # standard size
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(blurred, 30, 100)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 1000 or area > 100000:
            continue

        # Get rotated rectangle
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = box.astype(int)

        # Check if it's a clean rectangle
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

        if not is_rectangle(approx):
            continue

        # Draw box
        cv2.drawContours(frame, [box], 0, (255, 0, 0), 2)

        # Measure size
        (tl, tr, br, bl) = box
        width_px = np.linalg.norm(tr - tl)
        height_px = np.linalg.norm(tr - br)

        # Calibrate once
        if pixels_per_cm is None:
            pixels_per_cm = width_px / KNOWN_WIDTH_CM
            print(f"Calibrated: {pixels_per_cm:.2f} px/cm")

        width_cm = width_px / pixels_per_cm
        height_cm = height_px / pixels_per_cm

        # Label measurements
        cv2.putText(frame, f"{width_cm:.1f}cm x {height_cm:.1f}cm",
                    (int(tl[0]), int(tl[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Box Measurement", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
