import time

# Runtime state
traffic_start_time = None

def check_traffic_jam(cars_in_zone, max_car_number, traffic_time_limit):
    global traffic_start_time

    current_time = time.time()

    if cars_in_zone > max_car_number:
        if traffic_start_time is None:
            traffic_start_time = current_time
        final_time = current_time - traffic_start_time

        if final_time >= traffic_time_limit:
            return True, int(final_time)
        else:
            return False, int(final_time)
    else:
        traffic_start_time = None  # Reset if count drops
        return False, 0
