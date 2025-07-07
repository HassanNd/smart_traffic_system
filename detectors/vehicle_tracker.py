from deep_sort_realtime.deepsort_tracker import DeepSort

tracker=DeepSort(
    max_age=30 ,
    n_init=3,
    max_cosine_distance=0.4 , 
    nn_budget=None ,
    override_track_class=None
)

def track_vehicles(car_boxes , frame):
    detections = []

    # getting the position of the cars after getting the car position from YOLO in the main
    for (x1, y1, x2, y2 ,class_name) in car_boxes:
        #making the position as the format of deepsort input
        w= x2 - x1
        h=y2-y1
        # Deep SORT expects detections as ([x, y, w, h], confidence, class_name)
        detection = ([x1, y1, w, h], 0.9, class_name)  
        detections.append(detection)

    # Update tracker with current detections and frame
    tracks = tracker.update_tracks(detections, frame=frame)

    tracked_vehicles = []
    for track in tracks:
        if not track.is_confirmed():
            continue  # Skip if the tracker is not yet stable

        # Unique ID for the tracked object
        track_id = track.track_id

        # Bounding box in left, top, right, bottom format
        x1, y1, x2, y2 = map(int, track.to_ltrb()) 

        tracked_vehicles.append((track_id, x1, y1, x2, y2))

    return tracked_vehicles