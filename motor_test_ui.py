from data_struct import *
import tkinter
from tkinter import messagebox
import serial_backend
import customtkinter as ctk
from PIL import Image


def show_motor_test_window():
    def test_left_bottom_motor():

        response = messagebox.askokcancel("Test", "Test Left Bottom Motor?")

        if response:
            serial_backend.motor_test_number = 1
            serial_backend.send_gamepad_data = False
            serial_backend.request_motor_test_data = True
            motor_test_window.destroy()

    def test_left_top_motor():
        response = messagebox.askokcancel("Test", "Test Left Top Motor?")

        if response:
            serial_backend.motor_test_number = 2
            serial_backend.send_gamepad_data = False
            serial_backend.request_motor_test_data = True
            motor_test_window.destroy()

    def test_right_bottom_motor():
        response = messagebox.askokcancel("Test", "Test Right Bottom Motor?")

        if response:
            serial_backend.motor_test_number = 3
            serial_backend.send_gamepad_data = False
            serial_backend.request_motor_test_data = True
            motor_test_window.destroy()

    def test_right_top_motor():
        response = messagebox.askokcancel("Test", "Test Right Top Motor?")

        if response:
            serial_backend.motor_test_number = 4
            serial_backend.send_gamepad_data = False
            serial_backend.request_motor_test_data = True
            motor_test_window.destroy()

    if telemetry_data_dict["arm_status"] == 0:

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        motor_test_window = ctk.CTkToplevel()
        # config_window.iconbitmap("UAV_Project_LOGO_icon.ico")
        motor_test_window.geometry("500x500")
        motor_test_window.title("Motor Test")
        motor_test_window.grab_set()
        motor_test_window.resizable(False, False)

        drone_img = ctk.CTkImage(Image.open("images/motor_test_drone_image.png"), size=(280, 280))
        # MAIN FRAME
        main_frame = ctk.CTkFrame(master=motor_test_window, width=480, height=480, corner_radius=10)
        main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        #####################################################################################################################################
        drone_img_label = ctk.CTkLabel(master=motor_test_window, image=drone_img, text="", bg_color="#212121",
                                       fg_color="transparent")
        drone_img_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        #####################################################################################################################################
        forward_label = ctk.CTkLabel(master=motor_test_window, text="  Forward  ", fg_color="#474747",
                                     font=("Arial", 15, "bold"), corner_radius=6, width=40, height=30)
        forward_label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        #####################################################################################################################################
        left_top_motor_label = ctk.CTkLabel(master=motor_test_window, text=f"{motor_test_results[1]:.2f}", fg_color="#474747",
                                            font=("Arial", 15, "bold"), corner_radius=6, width=40, height=30)
        left_top_motor_label.place(relx=0.12, rely=0.27, anchor=tkinter.CENTER)

        #####################################################################################################################################
        left_top_motor_button = ctk.CTkButton(master=motor_test_window, text="Test", font=("Arial", 15, "bold"),
                                              corner_radius=6, width=40, height=30, command=test_left_top_motor)
        left_top_motor_button.place(relx=0.12, rely=0.35, anchor=tkinter.CENTER)

        #####################################################################################################################################
        left_bottom_motor_label = ctk.CTkLabel(master=motor_test_window, text=f"{motor_test_results[0]:.2f}", fg_color="#474747",
                                               font=("Arial", 15, "bold"), corner_radius=6, width=40, height=30)
        left_bottom_motor_label.place(relx=0.12, rely=0.73, anchor=tkinter.CENTER)

        #####################################################################################################################################
        left_bottom_motor_button = ctk.CTkButton(master=motor_test_window, text="Test", font=("Arial", 15, "bold"),
                                                 corner_radius=6, width=40, height=30, command=test_left_bottom_motor)
        left_bottom_motor_button.place(relx=0.12, rely=0.65, anchor=tkinter.CENTER)

        #####################################################################################################################################
        right_bottom_motor_label = ctk.CTkLabel(master=motor_test_window, text=f"{motor_test_results[2]:.2f}", fg_color="#474747",
                                                font=("Arial", 15, "bold"), corner_radius=6, width=40, height=30)
        right_bottom_motor_label.place(relx=0.88, rely=0.73, anchor=tkinter.CENTER)

        #####################################################################################################################################
        right_bottom_motor_button = ctk.CTkButton(master=motor_test_window, text="Test", font=("Arial", 15, "bold"),
                                                  corner_radius=6, width=40, height=30, command=test_right_bottom_motor)
        right_bottom_motor_button.place(relx=0.88, rely=0.65, anchor=tkinter.CENTER)

        #####################################################################################################################################
        right_top_motor_label = ctk.CTkLabel(master=motor_test_window, text=f"{motor_test_results[3]:.2f}", fg_color="#474747",
                                             font=("Arial", 15, "bold"), corner_radius=6, width=40, height=30)
        right_top_motor_label.place(relx=0.88, rely=0.27, anchor=tkinter.CENTER)

        #####################################################################################################################################
        right_top_motor_button = ctk.CTkButton(master=motor_test_window, text="Test", font=("Arial", 15, "bold"),
                                               corner_radius=6, width=40, height=30, command=test_right_top_motor)
        right_top_motor_button.place(relx=0.88, rely=0.35, anchor=tkinter.CENTER)

        #####################################################################################################################################
        # test_all_button = ctk.CTkButton(master=motor_test_window, text="Test All", font=("Arial", 15, "bold"),
        #                                 corner_radius=6, width=40, height=30, command=test_all_motors)
        # test_all_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)



# def test_all_motors():
#     response = messagebox.askokcancel("Test", "Test All Motors?")
#
#     if response:
#         serial_backend.motor_test_number = 5
#         serial_backend.send_gamepad_data = False
#         serial_backend.request_motor_test_data = True


