from playsound import playsound
from data_struct import telemetry_data_dict

prev_packet_delivery = telemetry_data_dict['packet_delivery']
is_gps_reliable = False
is_battery_low = False
is_takeoff = False
is_landing = False
voice_queue = []
is_enabled = 0


def check_for_voice_notify():
    global prev_packet_delivery, voice_queue, is_enabled, is_gps_reliable, is_battery_low, is_takeoff, is_landing

    if is_enabled:
        # TELEMETRY SIGNAL NOTIFICATION
        if prev_packet_delivery == 0 and telemetry_data_dict["packet_delivery"] > 0:
            voice_queue.append("voices\\telemetry_recovered.mp3")
            is_battery_low = False

        elif telemetry_data_dict["packet_delivery"] == 0 and prev_packet_delivery > 0:
            voice_queue.append("voices\\telemetry_lost.mp3")

        # GNSS SIGNAL NOTIFICATION
        if is_gps_reliable and (telemetry_data_dict["gps_fix"] < 3 or telemetry_data_dict["gps_satCount"] < 6 or
                                telemetry_data_dict["gps_hdop"] > 2.0):
            is_gps_reliable = False
            voice_queue.append("voices\\gnss_unreliable.mp3")

        elif not is_gps_reliable and (telemetry_data_dict["gps_fix"] >= 3 and telemetry_data_dict["gps_satCount"] >= 6
                                      and telemetry_data_dict["gps_hdop"] <= 2.0):
            voice_queue.append("voices\\gnss_fix_established.mp3")
            is_gps_reliable = True

        # BATTERY VOLTAGE NOTIFICATION
        if not ((3.7 <= telemetry_data_dict["battery_voltage"] < 4.3) or (
                10.5 <= telemetry_data_dict["battery_voltage"] < 12.7)) and not is_battery_low:
            voice_queue.append("voices\\low_battery_voltage.mp3")
            is_battery_low = True

        # TAKEOFF NOTIFICATION
        if (telemetry_data_dict["flight_mode"] == 1 or telemetry_data_dict["flight_mode"] == 3) and not is_takeoff and \
                telemetry_data_dict["arm_status"] == 1:
            voice_queue.append("voices\\takeoff.mp3")
            is_takeoff = True
        elif telemetry_data_dict["arm_status"] == 1:
            is_takeoff = True
        elif telemetry_data_dict["arm_status"] == 0 and is_takeoff:
            is_takeoff = False

        # LANDING NOTIFICATION
        if telemetry_data_dict["target_altitude"] < 0 and not is_landing and telemetry_data_dict["arm_status"] == 1:
            voice_queue.append("voices\\landing.mp3")
            is_landing = True
        elif (telemetry_data_dict["arm_status"] == 0 and is_landing) or (telemetry_data_dict["arm_status"] == 1
                                                                         and telemetry_data_dict[
                                                                             "target_altitude"] >= 0):
            is_landing = False

        process_voice_notify_queue()

    prev_packet_delivery = telemetry_data_dict["packet_delivery"]


def process_voice_notify_queue():
    global voice_queue

    if len(voice_queue) > 0:
        playsound(voice_queue.pop(0))
