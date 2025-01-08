from datetime import timedelta

def booking_time_discovery(schedule_start, schedule_end, trainer_bookings, search_window):
    start_time = schedule_start
    end_time = schedule_end

    # Формуємо список всіх можливих часових слотів з кроком 15 хвилин
    all_time_slots = []
    current_time = start_time
    while current_time + timedelta(minutes=search_window) <= end_time:
        all_time_slots.append(current_time)
        current_time += timedelta(minutes=15)

    # Видаляємо заброньовані слоти та слоти, які менші за `search_window`
    available_slots = []
    for slot in all_time_slots:
        slot_end = slot + timedelta(minutes=search_window)
        is_available = True
        for booking in trainer_bookings:
            booking_start = booking[0]
            booking_end = booking[1]
            # Перевіряємо, чи слот не перекривається з існуючим бронюванням
            if (slot < booking_end) and (slot_end > booking_start):
                is_available = False
                break
        if is_available:
            available_slots.append(slot)

    return available_slots

