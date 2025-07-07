# ==== main.py ====
import cv2
from ultralytics import YOLO
import time
from detectors.car_detectors import detect_cars  
from notifications.email_sender import send_traffic_alert_email

# === Configuration ===
cap = cv2.VideoCapture("images_videos/Cars in Highway Traffic (FREE STOCK VIDEO).mp4")

# Zone boundaries (horizontal lines)
y_line_1 = 790
y_line_2 = 350

# Traffic jam detection parameters
traffic_time_limit = 15  # seconds
max_car_number = 7  #cars
traffic_start_time = None
jam_detected = False
alert_sent=False

# === Main Loop ===
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for speed
    resized_frame = cv2.resize(frame, (1300, 800))

    # === Step 1: Detect Cars ===
    car_information = detect_cars(resized_frame)

    cars_in_zone = 0  # Reset per frame

    for x1, y1, x2, y2, class_name in car_information:
        car_center_y = (y1 + y2) // 2

        # Draw bounding box and label
        cv2.rectangle(resized_frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
        cv2.putText(resized_frame, class_name, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Count cars within the zone
        if y_line_2 < car_center_y < y_line_1:
            cars_in_zone += 1

    # === Step 2: Traffic Jam Detection ===
    current_time = time.time()
    if cars_in_zone > max_car_number:
        if traffic_start_time is None:
            traffic_start_time = current_time
            alert_sent=False

        final_time = current_time - traffic_start_time
        if final_time >= traffic_time_limit:
            jam_detected = True
            if not alert_sent:
                send_traffic_alert_email()
                alert_sent=True
        else:
            jam_detected = False
    else:
        traffic_start_time = None
        jam_detected = False
        alert_sent=False

    # === Step 3: Draw Info ===
    cv2.putText(resized_frame, f"Cars in Zone: {cars_in_zone}", (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 1)

    if jam_detected:
        cv2.putText(resized_frame, "TRAFFIC JAM DETECTED!!", (350, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        
    #time counter
    elif traffic_start_time:
        final_time = int(current_time - traffic_start_time)
        cv2.putText(resized_frame, f"Jam Timer: {final_time}s", (30, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Draw zone lines
    cv2.line(resized_frame, (0, y_line_1), (1450, y_line_1), (115, 147, 179), 1)
    cv2.line(resized_frame, (0, y_line_2), (1450, y_line_2), (115, 147, 179), 1)

    # Show result
    cv2.imshow("YOLOv8 - Zone Detection", resized_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Cleanup ===
cap.release()
cv2.destroyAllWindows()
