import sys
import com_port_selection
import serial_backend
import gamepad_handler
import main_ui
import threading
import time
import config_ui

counter = 0


def thread1():
    global counter
    while ui_main.isAppAlive:
        counter = counter + 1

        ret = serial_backend.read_serial()

        if ret == 1:
            ui_main.redraw_waypoint_markers()
        elif ret == 2:
            config_ui.show_config_window()


        if counter > 1:
            counter = 0
            ui_main.update_telemetry_ui()
    quit()


def thread2():
    while ui_main.isAppAlive:
        serial_backend.write_serial()
        time.sleep(0.025)
    quit()


# def thread3():
#     while ui_main.isAppAlive:
#         gamepad_handler.handle_gamepad()
#     quit()


com_port_selection.start()
serial_backend.port_init(com_port_selection.selected_port)
ui_main = main_ui.MainWindow()

t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)
# t3 = threading.Thread(target=thread3)
t1.start()
t2.start()
# t3.start()

while ui_main.isAppAlive:
    ui_main.update_ui()
quit()
