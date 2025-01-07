import datetime
def booking_time_discovery(trainer_schedule, bookings, cur_date, **kwargs):
    start_time = cur_date.replace(hour=8)
    end_time = cur_date.replace(hour=20)

    all_time_slots = []
    current_time = start_time
    while current_time + datetime.timedelta(minutes=30) <= end_time:
        all_time_slots.append(current_time)
        current_time += datetime.timedelta(minutes=30)

    available_slots = []
    for slot in all_time_slots:
        slot_end = slot + datetime.timedelta(minutes=30)
        is_available = True
        for booking in bookings:
            booking_start = booking[0]
            booking_end = booking[1]
            if (slot < booking_end) and (slot_end > booking_start):
                is_available = False
                break
        if is_available:
            available_slots.append(slot)

    return available_slots


