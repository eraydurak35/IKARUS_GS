from playsound import playsound
from data_struct import telemetry_data_dict

prev_packet_delivery = telemetry_data_dict['packet_delivery']
voice_queue = []
is_enabled = 0


def check_for_voice_notify():
    global prev_packet_delivery, voice_queue, is_enabled

    if is_enabled:
        if prev_packet_delivery == 0 and telemetry_data_dict["packet_delivery"] > 0:
            voice_queue.append("voices\\telemetry_recovered.mp3")

        elif telemetry_data_dict["packet_delivery"] == 0 and prev_packet_delivery > 0:
            voice_queue.append("voices\\telemetry_lost.mp3")

        process_voice_notify_queue()

    prev_packet_delivery = telemetry_data_dict["packet_delivery"]


def process_voice_notify_queue():
    global voice_queue

    if len(voice_queue) > 0:
        playsound(voice_queue.pop(0))
