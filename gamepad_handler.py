import inputs
from inputs import get_gamepad
from data_struct import *
import time


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def handle_gamepad():

    if inputs.devices.gamepads:
        # gamepad_ = inputs.devices.gamepads[0]
        # gamepad_.set_vibration(0.2, 0.2, 5000)
        events = get_gamepad()

        for event in events:
            if event.code == "ABS_RY":
                gamepad_data_dict["analog_RY"] = int(map_value(event.state, -32768, 32767, 1000, -1000))

            if event.code == "ABS_RX":
                gamepad_data_dict["analog_RX"] = int(map_value(event.state, -32768, 32767, -1000, 1000))

            if event.code == "ABS_Y":
                gamepad_data_dict["analog_LY"] = int(map_value(event.state, -32768, 32767, -1000, 1000))

            if event.code == "ABS_X":
                gamepad_data_dict["analog_LX"] = int(map_value(event.state, -32768, 32767, -1000, 1000))

            if event.code == "ABS_RZ":
                gamepad_data_dict["right_trigger"] = int(round(map_value(event.state, 0, 255, 0, 1000)))

            if event.code == "ABS_Z":
                gamepad_data_dict["left_trigger"] = int(round(map_value(event.state, 0, 255, 0, 1000)))

            if event.code == "BTN_TL":
                gamepad_data_dict["left_shoulder"] = int(event.state)

            if event.code == "BTN_TR":
                gamepad_data_dict["right_shoulder"] = int(event.state)

            if event.code == "BTN_SOUTH":
                gamepad_data_dict["button_A"] = int(event.state)

            if event.code == "BTN_NORTH":
                gamepad_data_dict["button_Y"] = int(event.state)

            if event.code == "BTN_EAST":
                gamepad_data_dict["button_B"] = int(event.state)

            if event.code == "BTN_WEST":
                gamepad_data_dict["button_X"] = int(event.state)

            if event.code == "BTN_THUMBL":
                gamepad_data_dict["analog_LB"] = int(event.state)

            if event.code == "BTN_THUMBR":
                gamepad_data_dict["analog_RB"] = int(event.state)

    else:
        print("No gamepad found...")
        time.sleep(20)
