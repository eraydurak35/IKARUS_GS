import serial
import struct
from data_struct import *
import pandas as pd
import numpy as np

serial_instance = serial
expected_telemetry_data_size = 0
expected_config_data_size = 0
gamepad_data_size = 0
send_gamepad_data = True
send_config_data = False
send_waypoints_data = False
request_config_data = False
request_wp_data = False
blackbox_state = False
blackbox_file_name = ""


def port_init(com_port):
    global serial_instance
    global expected_telemetry_data_size
    global expected_config_data_size
    global gamepad_data_size

    for key in telemetry_format_dict.keys():

        if telemetry_format_dict[key] == "f" or telemetry_format_dict[key] == "i" or telemetry_format_dict[key] == "I":
            expected_telemetry_data_size = expected_telemetry_data_size + 4
        elif telemetry_format_dict[key] == "b" or telemetry_format_dict[key] == "B":
            expected_telemetry_data_size = expected_telemetry_data_size + 1
        elif telemetry_format_dict[key] == "h" or telemetry_format_dict[key] == "H":
            expected_telemetry_data_size = expected_telemetry_data_size + 2

    expected_config_data_size = len(config_data_dict) * 4
    gamepad_data_size = len(gamepad_data_dict) * 4
    if com_port == "":
        quit()
    serial_instance = serial.Serial(com_port, 921600)


def read_serial():
    global serial_instance

    data_header = serial_instance.read(1)
    # if header is found
    if data_header == b'\xff':
        size = int.from_bytes(bytes=serial_instance.read(1), byteorder="big")
        if size - 3 != expected_telemetry_data_size:
            print(f"received telem data size: {size - 3} bytes, expected: {expected_telemetry_data_size} bytes")
            serial_instance.read(size)

        else:
            data_bytes = serial_instance.read(size)
            is_ok = checksum_validate(data_bytes)

            if is_ok == 1:

                parsed_data = []
                i = 0
                for key in telemetry_format_dict.keys():

                    if telemetry_format_dict[key] == "f":
                        four_bytes = bytearray(4)
                        four_bytes[0] = data_bytes[i]
                        four_bytes[1] = data_bytes[i + 1]
                        four_bytes[2] = data_bytes[i + 2]
                        four_bytes[3] = data_bytes[i + 3]
                        parsed_data.append(struct.unpack('f', four_bytes)[0])
                        i = i + 4

                    elif telemetry_format_dict[key] == "i":
                        four_bytes = bytearray(4)
                        four_bytes[0] = data_bytes[i]
                        four_bytes[1] = data_bytes[i + 1]
                        four_bytes[2] = data_bytes[i + 2]
                        four_bytes[3] = data_bytes[i + 3]
                        parsed_data.append(struct.unpack('i', four_bytes)[0])
                        i = i + 4

                    elif telemetry_format_dict[key] == "B":
                        one_byte = bytearray(1)
                        one_byte[0] = data_bytes[i]
                        parsed_data.append(struct.unpack('B', one_byte)[0])
                        i = i + 1

                    elif telemetry_format_dict[key] == "h":
                        two_bytes = bytearray(2)
                        two_bytes[0] = data_bytes[i]
                        two_bytes[1] = data_bytes[i + 1]
                        parsed_data.append(struct.unpack('h', two_bytes)[0])
                        i = i + 2

                    elif telemetry_format_dict[key] == "H":
                        two_bytes = bytearray(2)
                        two_bytes[0] = data_bytes[i]
                        two_bytes[1] = data_bytes[i + 1]
                        parsed_data.append(struct.unpack('H', two_bytes)[0])
                        i = i + 2

                for index, key in enumerate(telemetry_scale_dict.keys()):
                    # if key == "gps_satCount":
                    #     print(parsed_data[index])
                    parsed_data[index] = parsed_data[index] / telemetry_scale_dict[key]

                for index, key in enumerate(telemetry_data_dict.keys()):
                    telemetry_data_dict[key] = parsed_data[index]

                if blackbox_state:
                    df = pd.DataFrame([telemetry_data_dict])
                    df.to_csv("C:/Users/erayd/OneDrive/Masaüstü/Project STARLING/flight_logs/" + blackbox_file_name,
                              mode='a', index=False, header=False)
            else:
                print("checksum error telem!!")


    elif data_header == b'\xfe':

        size = int.from_bytes(bytes=serial_instance.read(1), byteorder="big")
        if size - 3 != expected_config_data_size:
            print(f"received config data size: {size - 3} bytes, expected: {expected_config_data_size} bytes")
            serial_instance.read(size)

        else:

            data_bytes = serial_instance.read(size)
            is_ok = checksum_validate(data_bytes)
            if is_ok:

                float_data = []
                four_bytes = bytearray(4)
                for i in range(0, expected_config_data_size, 4):
                    four_bytes[0] = data_bytes[i]
                    four_bytes[1] = data_bytes[i + 1]
                    four_bytes[2] = data_bytes[i + 2]
                    four_bytes[3] = data_bytes[i + 3]
                    float_data.append(struct.unpack('f', four_bytes)[0])

                for index, key in enumerate(config_data_dict.keys()):
                    config_data_dict[key] = float_data[index]
            else:
                print("checksum error config!!")

    elif data_header == b'\xfd':
        size = int.from_bytes(bytes=serial_instance.read(1), byteorder="big")

        if (size != 228):
            print("wp size is not 228")

        else:
            data_bytes = serial_instance.read(size)
            is_ok = checksum_validate(data_bytes)
            if is_ok == 1:
                parsed_data = []

                for i in range(0, 200, 4):

                    four_bytes = bytearray(4)
                    four_bytes[0] = data_bytes[i]
                    four_bytes[1] = data_bytes[i + 1]
                    four_bytes[2] = data_bytes[i + 2]
                    four_bytes[3] = data_bytes[i + 3]
                    parsed_data.append(struct.unpack('i', four_bytes)[0] / 10000000.0)

                for i in range(200, 225, 1):
                    one_byte = bytearray(1)
                    one_byte[0] = data_bytes[i]
                    parsed_data.append(struct.unpack('B', one_byte)[0])

                waypoint_coordinates.clear()
                waypoint_only_altitudes.clear()
                for i in range(0, 25, 1):

                    if parsed_data[i] != 0 or parsed_data[i + 25] != 0:
                        waypoint_coordinates.append((parsed_data[i], parsed_data[i + 25]))
                        waypoint_only_altitudes.append(np.uint8(parsed_data[i + 50]))

                return 1
            else:
                print("checksum error wp!!")

    return 0
def write_serial():
    global send_config_data
    global send_gamepad_data
    global send_waypoints_data
    global gamepad_data_size
    global request_config_data
    global request_wp_data

    if send_gamepad_data:

        packed_data = bytes()
        for keys in gamepad_data_dict.keys():
            packed_data = packed_data + struct.pack('i', gamepad_data_dict[keys])

        cs1, cs2 = checksum_generate(packed_data, len(gamepad_data_dict) * 4)
        packed_data = struct.pack('B', 255) + struct.pack('B',
                                                          (len(gamepad_data_dict) * 4) + 3) + packed_data + struct.pack(
            'B', cs1) + struct.pack('B', cs2) + struct.pack('B', 0x69)
        serial_instance.write(packed_data)

    elif send_config_data:
        send_config_data = False
        send_gamepad_data = True
        packed_data = bytes()
        for keys in config_data_dict.keys():
            packed_data = packed_data + struct.pack('f', config_data_dict[keys])

        cs1, cs2 = checksum_generate(packed_data, len(config_data_dict) * 4)
        packed_data = struct.pack('B', 254) + struct.pack('B',
                                                          (len(config_data_dict) * 4) + 3) + packed_data + struct.pack(
            'B', cs1) + struct.pack('B', cs2) + struct.pack('B', 0x69)
        serial_instance.write(packed_data)

    elif send_waypoints_data:
        send_waypoints_data = False
        send_gamepad_data = True

        waypoint_only_latitudes.clear()
        waypoint_only_longitudes.clear()

        for lat, lon in waypoint_coordinates:
            waypoint_only_latitudes.append(np.int32(lat * 10000000))
            waypoint_only_longitudes.append(np.int32(lon * 10000000))

        wp_altitudes = waypoint_only_altitudes.copy()

        if len(waypoint_coordinates) < 25:
            waypoint_only_latitudes.extend([np.int32(0)] * (25 - len(waypoint_coordinates)))
            waypoint_only_longitudes.extend([np.int32(0)] * (25 - len(waypoint_coordinates)))
            wp_altitudes.extend([np.uint8(0)] * (25 - len(waypoint_coordinates)))

        packed_data = bytes()
        for values in waypoint_only_latitudes:
            packed_data = packed_data + struct.pack('i', values)
        for values in waypoint_only_longitudes:
            packed_data = packed_data + struct.pack('i', values)
        for values in wp_altitudes:
            packed_data = packed_data + struct.pack('B', values)

        total_len = len(waypoint_only_latitudes) * 4 + len(waypoint_only_longitudes) * 4 + len(wp_altitudes)
        cs1, cs2 = checksum_generate(packed_data, total_len)
        packed_data = (struct.pack('B', 253) + struct.pack('B', total_len + 3) + packed_data
                       + struct.pack('B', cs1) + struct.pack('B', cs2) + struct.pack('B', 0x69))
        serial_instance.write(packed_data)

    elif request_config_data:

        request_config_data = False
        send_gamepad_data = True
        packed_data = bytes()
        packed_data = packed_data + struct.pack('B', 10)
        cs1, cs2 = checksum_generate(packed_data, 1)
        packed_data = struct.pack('B', 252) + struct.pack('B',
                                                          1 + 3) + packed_data + struct.pack(
            'B', cs1) + struct.pack('B', cs2) + struct.pack('B', 0x69)
        serial_instance.write(packed_data)

    elif request_wp_data:

        request_wp_data = False
        send_gamepad_data = True
        print("wp requested!!")
        packed_data = bytes()
        packed_data = packed_data + struct.pack('B', 20)
        cs1, cs2 = checksum_generate(packed_data, 1)
        packed_data = struct.pack('B', 252) + struct.pack('B',
                                                          1 + 3) + packed_data + struct.pack(
            'B', cs1) + struct.pack('B', cs2) + struct.pack('B', 0x69)
        serial_instance.write(packed_data)


def checksum_generate(data_byte, size):
    data = bytearray(data_byte)
    checksum1 = 0
    checksum2 = 0
    for i in range(size):
        checksum1 = (checksum1 + data[i]) % 256
        checksum2 = (checksum2 + checksum1) % 256

    return checksum1, checksum2


def checksum_validate(data):
    size = len(data)
    cs1, cs2 = checksum_generate(data, size - 3)
    if data[size - 3] == cs1 and data[size - 2] == cs2:
        return 1
    else:
        return 0
