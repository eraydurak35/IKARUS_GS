import time
import customtkinter as ctk
from customtkinter import filedialog
import tkinter
import numpy as np
from PIL import Image, ImageTk
from data_struct import *
import serial_backend
import tkintermapview
import os
import pandas as pd
from datetime import datetime
import math
from config_ui import show_config_window
import mag_calibration
from tkinter import messagebox
import voice_notify
import motor_test_ui
import acc_calibration
import auto_mission_creator as amc
import save_load_mission as slm


class MainWindow:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.prev_flight_mode = 0
        self.prev_arm_status = 0
        self.prev_origin_latitude = 0
        self.prev_origin_longitude = 0
        self.prev_target_latitude = 0
        self.prev_target_longitude = 0
        self.prev_latitude = 0
        self.prev_longitude = 0
        self.bb_auto_record = True
        self.root = ctk.CTk()
        self.root.geometry("1920x1080")
        self.root.title("IKARUS Ground Station")
        self.root.attributes('-fullscreen', True)
        self.isAppAlive = True
        self.isBlackBoxRecording = False
        self.point_mode = "WP Mode"
        self.auto_mission_padding = 0
        self.auto_mission_angle = 0
        self.auto_mission_spacing = 1
        self.auto_mission_invert = 0
        self.auto_mission_reverse = 0
        self.is_auto_mission_create_requested = 0
        self.font = ("Ezarion", 16, "bold")
        self.font2 = ("Ezarion", 18, "bold")
        self.font3 = ("Ezarion", 12, "bold")

        self.close_img = ctk.CTkImage(Image.open("images/Close.png"), size=(30, 30))
        self.config_img = ctk.CTkImage(Image.open("images/settings_1.png"), size=(40, 40))
        self.alt_hold_active_img = ctk.CTkImage(Image.open("images/AltHold_active.png"), size=(40, 40))
        self.alt_hold_passive_img = ctk.CTkImage(Image.open("images/AltHold_passive.png"), size=(40, 40))
        self.pos_hold_active_img = ctk.CTkImage(Image.open("images/PositionHold_active.png"), size=(40, 40))
        self.pos_hold_passive_img = ctk.CTkImage(Image.open("images/PositionHold_passive.png"), size=(40, 40))
        self.blackbox_active_img = ctk.CTkImage(Image.open("images/blackbox_active.png"), size=(40, 40))
        self.blackbox_passive_img = ctk.CTkImage(Image.open("images/blackbox_passive.png"), size=(40, 40))
        self.center_drone_img = ctk.CTkImage(Image.open("images/focus_white.png"), size=(24, 24))
        self.center_map_img = ctk.CTkImage(Image.open("images/center_map_white.png"), size=(24, 24))
        self.waypoint_active_img = ctk.CTkImage(Image.open("images/waypoint_active.png"), size=(40, 40))
        self.waypoint_passive_img = ctk.CTkImage(Image.open("images/waypoint_passive.png"), size=(40, 40))
        self.request_wp_img = ctk.CTkImage(Image.open("images/recycling-point_white.png"), size=(24, 24))
        self.delete_trail_img = ctk.CTkImage(Image.open("images/delete_trail.png"), size=(24, 24))

        # Resimlerin saklanacağı liste
        self.cog_direction_images_degree_list = []
        self.drone_images_degree_list = []
        self.target_direction_images_degree_list = []

        # 0'dan 350'ye kadar 10'ar artışla döngü oluştur
        for deg in range(0, 360, 10):
            # Resmi aç, boyutlandır ve ImageTk.PhotoImage ile yükle
            img1 = ImageTk.PhotoImage(Image.open(f"images/cog_directions/cog_direction_{deg}_deg.png").resize((300, 300)))
            img2 = ImageTk.PhotoImage(Image.open(f"images/drone_pos/drone_pos_icon_{deg}_deg.png").resize((80, 80)))
            img3 = ImageTk.PhotoImage(Image.open(f"images/target_direction/target_direction_{deg}_deg.png").resize((300, 300)))

            # Resmi listeye ekle
            self.cog_direction_images_degree_list.append(img1)
            self.drone_images_degree_list.append(img2)
            self.target_direction_images_degree_list.append(img3)

        self.location_img = ImageTk.PhotoImage(Image.open("images/location_icon.png").resize((25, 25)))
        self.drone_origin_img = ImageTk.PhotoImage(Image.open("images/home_location.png").resize((25, 25)))
        self.target_location_img = ImageTk.PhotoImage(Image.open("images/target_pointer.png").resize((35, 40)))
        self.dist_empty_img = ImageTk.PhotoImage(Image.open("images/empty.png").resize((45, 45)))
        self.polygon_edge_img = ImageTk.PhotoImage(Image.open("images/polygon_edge_marker.png").resize((15, 15)))

        # MAP FRAME
        self.map_frame = ctk.CTkFrame(master=self.root, width=1600, height=830,
                                      corner_radius=10)
        self.map_frame.place(relx=0.422, rely=0.488, anchor=tkinter.CENTER)

        script_directory = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(script_directory, "offline_map_tiles.db")

        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, width=1600, height=830, corner_radius=10,
                                                        use_database_only=False, database_path=database_path)

        self.map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.map_widget.set_position(39.110946, 27.187785)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        self.map_widget.add_right_click_menu_command(label="Add Point", command=self.add_waypoint_event, pass_coords=True)
        self.map_widget.add_right_click_menu_command(label="", command=dummy_func, pass_coords=False)
        self.map_widget.add_right_click_menu_command(label="Add WP to Home", command=self.add_waypoint_to_home_event, pass_coords=False)
        self.map_widget.add_right_click_menu_command(label="", command=dummy_func, pass_coords=False)
        self.map_widget.add_right_click_menu_command(label="Delete Point", command=self.delete_waypoint_event, pass_coords=True)
        self.map_widget.add_right_click_menu_command(label="", command=dummy_func, pass_coords=False)
        self.map_widget.add_right_click_menu_command(label="Delete All Points", command=self.delete_all_points_event, pass_coords=False)
        self.map_widget.add_right_click_menu_command(label="", command=dummy_func, pass_coords=False)
        self.map_widget.add_right_click_menu_command(label="Send WP Mission", command=write_waypoints, pass_coords=False)

        self.waypoint_path = self.map_widget.set_path([(0, 0), (0, 0)], color="red", width=5)
        self.field_polygon_1 = self.map_widget.set_polygon([(0.0, 0.0)], fill_color=None,
                                                           # outline_color="red",
                                                           # border_width=12,
                                                           # command=self.field_clicked_event,
                                                           name="field_polygon_1")
        self.drone_path = self.map_widget.set_path([(0, 0), (0, 0)], color="lime green", width=5)

        self.drone_location_marker = self.map_widget.set_marker(0, 0, text="0.0m", text_color="gray1",
                                                                icon=self.drone_images_degree_list[0],
                                                                font=self.font3)

        self.cog_direction_marker = self.map_widget.set_marker(0, 0, icon=self.cog_direction_images_degree_list[0])
        self.target_direction_marker = self.map_widget.set_marker(0, 0, icon=self.target_direction_images_degree_list[1])

        self.drone_origin_marker = self.map_widget.set_marker(0, 0, text="", text_color="gray1",
                                                              icon=self.drone_origin_img, icon_anchor="s",
                                                              font=self.font3)

        self.target_location_marker = self.map_widget.set_marker(0, 0, text="", text_color="gray1",
                                                                 icon=self.target_location_img, icon_anchor="n",
                                                                 font=self.font3)

        self.map_request_wp_button = ctk.CTkButton(master=self.map_frame, width=24, height=24, corner_radius=0,
                                                   fg_color="#333333", text="", hover_color="#7f7f7f",
                                                   image=self.request_wp_img, command=read_waypoints)
        self.map_request_wp_button.place(relx=0.021, rely=0.14, anchor=tkinter.CENTER)

        self.center_drone_button = ctk.CTkButton(master=self.map_frame, width=24, height=24, corner_radius=0,
                                                 fg_color="#333333", text="", hover_color="#7f7f7f",
                                                 image=self.center_drone_img,
                                                 command=self.center_drone)
        self.center_drone_button.place(relx=0.021, rely=0.188, anchor=tkinter.CENTER)

        self.center_map_button = ctk.CTkButton(master=self.map_frame, width=20, height=20, corner_radius=0,
                                               fg_color="#333333", text="", hover_color="#7f7f7f",
                                               image=self.center_map_img,
                                               command=self.center_map_func)
        self.center_map_button.place(relx=0.021, rely=0.236, anchor=tkinter.CENTER)

        self.delete_trail_button = ctk.CTkButton(master=self.map_frame, width=20, height=20, corner_radius=0,
                                                 fg_color="#333333", text="", hover_color="#7f7f7f",
                                                 image=self.delete_trail_img,
                                                 command=self.delete_trail_func)
        self.delete_trail_button.place(relx=0.021, rely=0.284, anchor=tkinter.CENTER)

        self.close_button = ctk.CTkButton(master=self.root, width=30, height=30, corner_radius=0,
                                          fg_color="transparent", text="",
                                          image=self.close_img,
                                          command=self.close_application)
        self.close_button.place(relx=0.828, rely=0.03, anchor=tkinter.CENTER)

        #############################################

        self.wp_field_mode_tabview = ctk.CTkTabview(master=self.root, width=440, height=110, corner_radius=10, command=self.wp_field_mode_selection)
        self.wp_field_mode_tabview.place(relx=0.543, rely=0.045, anchor=tkinter.CENTER)

        self.wp_field_mode_tabview.add("WP Mode")  # add tab at the end
        self.wp_field_mode_tabview.add("Field Mode")  # add tab at the end
        self.wp_field_mode_tabview.set("WP Mode")  # set currently visible tab
        self.wp_field_mode_tabview.segmented_button.configure(font=("Ezarion", 13, "bold"))

        #                                               FIELD MODE ELEMENTS

        self.create_mission_for_field_invert_checkbox_variable = ctk.StringVar(value="off")
        self.create_mission_for_field_invert_checkbox = ctk.CTkCheckBox(master=self.wp_field_mode_tabview.tab("Field Mode"), checkbox_width=20, checkbox_height=20, corner_radius=5,
                                                                        text="Invert", font=("Arial", 11, "bold"), command=self.create_mission_for_field_invert_checkbox_event,
                                                                        onvalue="on", offvalue="off", variable=self.create_mission_for_field_invert_checkbox_variable)

        self.create_mission_for_field_invert_checkbox.place(relx=0.95, rely=0.74, anchor=tkinter.CENTER)

        self.create_mission_for_field_reverse_checkbox_variable = ctk.StringVar(value="off")
        self.create_mission_for_field_reverse_checkbox = ctk.CTkCheckBox(master=self.wp_field_mode_tabview.tab("Field Mode"), checkbox_width=20, checkbox_height=20,
                                                                         corner_radius=5,
                                                                         text="Reverse", font=("Ezarion", 11, "bold"), command=self.create_mission_for_field_reverse_checkbox_event,
                                                                         onvalue="on", offvalue="off", variable=self.create_mission_for_field_reverse_checkbox_variable)

        self.create_mission_for_field_reverse_checkbox.place(relx=0.95, rely=0.26, anchor=tkinter.CENTER)

        self.create_mission_for_field_button = ctk.CTkButton(master=self.wp_field_mode_tabview.tab("Field Mode"), width=30, height=25, corner_radius=10, text="Create",
                                                             command=self.create_mission_for_field_function, font=("Ezarion", 12, "bold"))
        self.create_mission_for_field_button.place(relx=0.72, rely=0.7, anchor=tkinter.CENTER)

        self.create_mission_for_field_angle_slider = ctk.CTkSlider(master=self.wp_field_mode_tabview.tab("Field Mode"),
                                                                   from_=-60, to=60,
                                                                   command=self.create_mission_for_field_angle_slider_event,
                                                                   width=140, height=15, number_of_steps=60)
        self.create_mission_for_field_angle_slider.place(relx=0.3, rely=0.2, anchor=tkinter.CENTER)

        self.create_mission_for_field_spacing_slider = ctk.CTkSlider(master=self.wp_field_mode_tabview.tab("Field Mode"),
                                                                     from_=1, to=10,
                                                                     command=self.create_mission_for_field_spacing_slider_event,
                                                                     width=140, height=15, number_of_steps=18)
        self.create_mission_for_field_spacing_slider.place(relx=0.3, rely=0.75, anchor=tkinter.CENTER)
        self.create_mission_for_field_spacing_slider.set(0)

        self.create_mission_for_field_padding_slider = ctk.CTkSlider(master=self.wp_field_mode_tabview.tab("Field Mode"),
                                                                     from_=0, to=10,
                                                                     command=self.create_mission_for_field_padding_slider_event,
                                                                     width=140, height=15, number_of_steps=20)
        self.create_mission_for_field_padding_slider.place(relx=0.64, rely=0.2, anchor=tkinter.CENTER)
        self.create_mission_for_field_padding_slider.set(0)

        self.create_mission_for_field_angle_label = ctk.CTkLabel(master=self.wp_field_mode_tabview.tab("Field Mode"),
                                                                 width=20, height=20, font=("Ezarion", 12, "bold"), text="Agl: 0")
        self.create_mission_for_field_angle_label.place(relx=0.06, rely=0.2, anchor=tkinter.CENTER)

        self.create_mission_for_field_spacing_label = ctk.CTkLabel(master=self.wp_field_mode_tabview.tab("Field Mode"),
                                                                   width=20, height=20, font=("Ezarion", 12, "bold"), text="Spc: 0.0")
        self.create_mission_for_field_spacing_label.place(relx=0.06, rely=0.75, anchor=tkinter.CENTER)

        self.create_mission_for_field_padding_label = ctk.CTkLabel(master=self.wp_field_mode_tabview.tab("Field Mode"),
                                                                   width=20, height=20, font=("Ezarion", 12, "bold"), text="Pad: 0.0")
        self.create_mission_for_field_padding_label.place(relx=0.56, rely=0.75, anchor=tkinter.CENTER)

        #                                               WP MODE ELEMENTS

        self.save_mission_button = ctk.CTkButton(master=self.wp_field_mode_tabview.tab("WP Mode"), width=35, height=18, corner_radius=10, text="Save",
                                                 command=self.save_mission_function, font=("Ezarion", 12, "bold"))
        self.save_mission_button.place(relx=0.1, rely=0.28, anchor=tkinter.CENTER)

        self.load_mission_button = ctk.CTkButton(master=self.wp_field_mode_tabview.tab("WP Mode"), width=35, height=18, corner_radius=10, text="Load",
                                                 command=self.load_mission_function, font=("Ezarion", 12, "bold"))
        self.load_mission_button.place(relx=0.1, rely=0.72, anchor=tkinter.CENTER)

        self.wp_altitude_input = ctk.CTkEntry(master=self.wp_field_mode_tabview.tab("WP Mode"), width=70, height=40, corner_radius=5,
                                              placeholder_text="WP Alt", font=("Ezarion", 13, "bold"))

        self.wp_altitude_input.place(relx=0.3, rely=0.5, anchor=tkinter.CENTER)

        self.wp_distance_label = ctk.CTkLabel(master=self.wp_field_mode_tabview.tab("WP Mode"), width=70, height=40, corner_radius=5,
                                              text="Distance:\n0.0m", font=("Ezarion", 13, "bold"), fg_color="#292929")

        self.wp_distance_label.place(relx=0.53, rely=0.5, anchor=tkinter.CENTER)

        self.rth_after_wp_checkbox_variable = ctk.StringVar(value="off")
        self.rth_after_wp_checkbox = ctk.CTkCheckBox(master=self.wp_field_mode_tabview.tab("WP Mode"), checkbox_width=20, checkbox_height=20, corner_radius=5,
                                                     text="RTH after Mission", font=("Ezarion", 11, "bold"), command=self.rth_after_wp_checkbox_event,
                                                     onvalue="on", offvalue="off", variable=self.rth_after_wp_checkbox_variable)

        self.rth_after_wp_checkbox.place(relx=0.82, rely=0.28, anchor=tkinter.CENTER)

        self.land_after_wp_checkbox_variable = ctk.StringVar(value="off")
        self.land_after_wp_checkbox = ctk.CTkCheckBox(master=self.wp_field_mode_tabview.tab("WP Mode"), checkbox_width=20, checkbox_height=20, corner_radius=5,
                                                      text="Lnd after Mission", font=("Ezarion", 11, "bold"), command=self.land_after_wp_checkbox_event,
                                                      onvalue="on", offvalue="off", variable=self.land_after_wp_checkbox_variable, state="disabled")

        self.land_after_wp_checkbox.place(relx=0.82, rely=0.72, anchor=tkinter.CENTER)

        #############################################

        self.voice_notification_checkbox = ctk.CTkCheckBox(master=self.root, width=20, height=20, corner_radius=5,
                                                           text="", command=voice_notification_enable_disable)

        self.voice_notification_checkbox.place(relx=0.828, rely=0.07, anchor=tkinter.CENTER)

        # UTILITY FRAME /*******************************************************************************/

        self.arm_utility_frame = ctk.CTkFrame(master=self.root, width=800, height=95,
                                              corner_radius=10)
        self.arm_utility_frame.place(relx=0.215, rely=0.053, anchor=tkinter.CENTER)

        self.config_button = ctk.CTkButton(master=self.arm_utility_frame, width=40, height=40, corner_radius=0,
                                           command=show_config_window, image=self.config_img, text="",
                                           fg_color="transparent", state="enabled")
        self.config_button.place(relx=0.05, rely=0.5, anchor=tkinter.CENTER)

        self.blackbox_button = ctk.CTkButton(master=self.arm_utility_frame, width=40, height=40, corner_radius=5,
                                             command=self.blackbox, text="", state="enabled", fg_color="transparent",
                                             image=self.blackbox_passive_img)

        self.blackbox_button.place(relx=0.12, rely=0.5, anchor=tkinter.CENTER)

        self.blackbox_auto_record_button = ctk.CTkButton(master=self.arm_utility_frame, width=10, height=40,
                                                         corner_radius=5,
                                                         command=self.auto_blackbox, text="", state="enabled",
                                                         fg_color="green")

        self.blackbox_auto_record_button.place(relx=0.16, rely=0.5, anchor=tkinter.CENTER)

        self.alt_hold_button = ctk.CTkButton(master=self.arm_utility_frame, width=40, height=40, corner_radius=5,
                                             text="", state="enabled", fg_color="transparent",
                                             image=self.alt_hold_passive_img)

        self.alt_hold_button.place(relx=0.23, rely=0.5, anchor=tkinter.CENTER)

        self.pos_hold_button = ctk.CTkButton(master=self.arm_utility_frame, width=40, height=40, corner_radius=5,
                                             text="", state="enabled", fg_color="transparent",
                                             image=self.pos_hold_passive_img)

        self.pos_hold_button.place(relx=0.32, rely=0.5, anchor=tkinter.CENTER)

        self.waypoint_button = ctk.CTkButton(master=self.arm_utility_frame, width=40, height=40, corner_radius=5,
                                             text="", state="enabled", fg_color="transparent",
                                             image=self.waypoint_passive_img)

        self.waypoint_button.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)

        self.save_button = ctk.CTkButton(master=self.arm_utility_frame, width=40, height=40, corner_radius=5,
                                         text_color="black", fg_color="#dcdde1", text="Save",
                                         command=save_on_click,
                                         font=("Ezarion", 14, "bold"))

        self.save_button.place(relx=0.49, rely=0.5, anchor=tkinter.CENTER)

        self.calibrate_mag_button = ctk.CTkButton(master=self.arm_utility_frame, width=110, height=40, corner_radius=5,
                                                  text_color="black", fg_color="#dcdde1", text="Start Mag Cal",
                                                  command=self.calibrate_mag_event, font=("Ezarion", 14, "bold"))

        self.calibrate_mag_button.place(relx=0.62, rely=0.5, anchor=tkinter.CENTER)

        self.calibrate_acc_button = ctk.CTkButton(master=self.arm_utility_frame, width=110, height=40, corner_radius=5,
                                                  text_color="black", fg_color="#dcdde1", text="Start Acc Cal",
                                                  command=self.calibrate_acc_event, font=("Ezarion", 14, "bold"))

        self.calibrate_acc_button.place(relx=0.78, rely=0.5, anchor=tkinter.CENTER)

        self.motor_test_button = ctk.CTkButton(master=self.arm_utility_frame, width=65, height=40, corner_radius=5,
                                               text_color="black", fg_color="#dcdde1", font=("Ezarion", 14, "bold"),
                                               text="Motor Test",
                                               command=motor_test_ui.show_motor_test_window)
        self.motor_test_button.place(relx=0.92, rely=0.5, anchor=tkinter.CENTER)

        # DATA FRAME  /*********************************************************************************/
        self.data_frame = ctk.CTkFrame(master=self.root, width=290, height=1060,
                                       corner_radius=20)
        self.data_frame.place(relx=0.92, rely=0.5, anchor=tkinter.CENTER)

        # DATA FRAME 1  ///////////////////////////////////////////////////////////////////////////////////
        self.imu_frame = ctk.CTkFrame(master=self.data_frame, width=270, height=180, corner_radius=10)
        self.imu_frame.place(relx=0.5, rely=0.095, anchor=tkinter.CENTER)

        self.gyroscope_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                            corner_radius=10, fg_color="gray35",
                                            text="Gyroscope (dps)",
                                            font=self.font)
        self.gyroscope_label.place(relx=0.5, rely=0.12, anchor=tkinter.CENTER)

        self.gyro_x_data_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                              corner_radius=10,
                                              text="X: 100.0",
                                              font=self.font)
        self.gyro_x_data_label.place(relx=0.2, rely=0.3, anchor=tkinter.CENTER)

        self.gyro_y_data_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                              corner_radius=10,
                                              text="Y: 100.0",
                                              font=self.font)
        self.gyro_y_data_label.place(relx=0.50, rely=0.3, anchor=tkinter.CENTER)

        self.gyro_z_data_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                              corner_radius=10,
                                              text="Z: 100.0",
                                              font=self.font)
        self.gyro_z_data_label.place(relx=0.8, rely=0.3, anchor=tkinter.CENTER)

        self.accelerometer_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                                corner_radius=10, fg_color="gray35",
                                                text="Accelerometer (m/s²)",
                                                font=self.font)
        self.accelerometer_label.place(relx=0.5, rely=0.52, anchor=tkinter.CENTER)

        self.accel_x_data_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="X: 100.0",
                                               font=self.font)
        self.accel_x_data_label.place(relx=0.2, rely=0.7, anchor=tkinter.CENTER)

        self.accel_y_data_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="Y: 100.0",
                                               font=self.font)
        self.accel_y_data_label.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.accel_z_data_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="Z: 100.0",
                                               font=self.font)
        self.accel_z_data_label.place(relx=0.8, rely=0.7, anchor=tkinter.CENTER)

        self.imu_core_temp_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="IMU core temp: 25.5 °C",
                                                font=self.font)
        self.imu_core_temp_label.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        # DATA FRAME 2  ////////////////////////////////////////////////////////////////////////////////////////
        self.magnetometer_frame = ctk.CTkFrame(master=self.data_frame, width=270, height=80, corner_radius=10)
        self.magnetometer_frame.place(relx=0.5, rely=0.23, anchor=tkinter.CENTER)

        self.magnetometer_label = ctk.CTkLabel(master=self.magnetometer_frame, width=100, height=25,
                                               corner_radius=10, fg_color="gray35",
                                               text="Magnetometer",
                                               font=self.font)
        self.magnetometer_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.mag_x_data_label = ctk.CTkLabel(master=self.magnetometer_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="X: 100.0",
                                             font=self.font)
        self.mag_x_data_label.place(relx=0.2, rely=0.70, anchor=tkinter.CENTER)

        self.mag_y_data_label = ctk.CTkLabel(master=self.magnetometer_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="Y: 100.0",
                                             font=self.font)
        self.mag_y_data_label.place(relx=0.5, rely=0.70, anchor=tkinter.CENTER)

        self.mag_z_data_label = ctk.CTkLabel(master=self.magnetometer_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="Z: 100.0",
                                             font=self.font)
        self.mag_z_data_label.place(relx=0.8, rely=0.70, anchor=tkinter.CENTER)

        # DATA FRAME 3  /////////////////////////////////////////////////////////////////////////////////////
        self.barometer_frame = ctk.CTkFrame(master=self.data_frame, width=270, height=130, corner_radius=10)
        self.barometer_frame.place(relx=0.5, rely=0.34, anchor=tkinter.CENTER)

        self.barometer_label = ctk.CTkLabel(master=self.barometer_frame, width=100, height=25,
                                            corner_radius=10, fg_color="gray35",
                                            text="Barometer",
                                            font=self.font)
        self.barometer_label.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.pressure_data_label = ctk.CTkLabel(master=self.barometer_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="Pressure:             1010.5 hPa",
                                                font=self.font)
        self.pressure_data_label.place(relx=0.5, rely=0.38, anchor=tkinter.CENTER)

        self.temp_data_label = ctk.CTkLabel(master=self.barometer_frame, width=100, height=25,
                                            corner_radius=10,
                                            text="Temperature:       25.5 °C",
                                            font=self.font)
        self.temp_data_label.place(relx=0.45, rely=0.61, anchor=tkinter.CENTER)

        self.altitude_data_label = ctk.CTkLabel(master=self.barometer_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="Altitude:                 1.5 m",
                                                font=self.font)
        self.altitude_data_label.place(relx=0.43, rely=0.84, anchor=tkinter.CENTER)

        # DATA FRAME 4 ////////////////////////////////////////////////////////////////////////////////////////
        self.tof_frame = ctk.CTkFrame(master=self.data_frame, width=270, height=80, corner_radius=10)
        self.tof_frame.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.tof_label = ctk.CTkLabel(master=self.tof_frame, width=100, height=25,
                                      corner_radius=10, fg_color="gray35",
                                      text="Range Finder (cm)",
                                      font=self.font)
        self.tof_label.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        self.tof_range_label = ctk.CTkLabel(master=self.tof_frame, width=100, height=25,
                                            corner_radius=10,
                                            text="Range: 120.0",
                                            font=self.font)
        self.tof_range_label.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        # DATA FRAME 5 ////////////////////////////////////////////////////////////////////////////////
        self.flow_frame = ctk.CTkFrame(master=self.data_frame, width=270, height=80, corner_radius=10)
        self.flow_frame.place(relx=0.5, rely=0.537, anchor=tkinter.CENTER)

        self.flow_label = ctk.CTkLabel(master=self.flow_frame, width=100, height=25,
                                       corner_radius=10, fg_color="gray35",
                                       text="Optical Flow (cm/s)",
                                       font=self.font)
        self.flow_label.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        self.flow_x_vel_data_label = ctk.CTkLabel(master=self.flow_frame, width=100, height=25,
                                                  corner_radius=10,
                                                  text="X: 0.00",
                                                  font=self.font)
        self.flow_x_vel_data_label.place(relx=0.2, rely=0.7, anchor=tkinter.CENTER)

        self.flow_y_vel_data_label = ctk.CTkLabel(master=self.flow_frame, width=100, height=25,
                                                  corner_radius=10,
                                                  text="Y: 0.00",
                                                  font=self.font)
        self.flow_y_vel_data_label.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.flow_quality_data_label = ctk.CTkLabel(master=self.flow_frame, width=100, height=25,
                                                    corner_radius=10,
                                                    text="Q: 100",
                                                    font=self.font)
        self.flow_quality_data_label.place(relx=0.8, rely=0.7, anchor=tkinter.CENTER)

        # DATA FRAME 5 - THROTTLE ////////////////////////////////////////////////////////////////////
        self.throttle_frame = ctk.CTkFrame(master=self.data_frame, width=270, height=50, corner_radius=10)
        self.throttle_frame.place(relx=0.5, rely=0.61, anchor=tkinter.CENTER)

        self.throttle_label = ctk.CTkLabel(master=self.throttle_frame, width=100, height=25,
                                           corner_radius=10,
                                           text="Throttle: 0",
                                           font=self.font)
        self.throttle_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # DATA FRAME 6 ////////////////////////////////////////////////////////////////////////////////
        self.gps_outer_frame = ctk.CTkFrame(master=self.data_frame, width=290, height=375, corner_radius=20,
                                            fg_color="#880808")
        self.gps_outer_frame.place(relx=0.5, rely=0.822, anchor=tkinter.CENTER)

        self.gps_frame = ctk.CTkFrame(master=self.gps_outer_frame, width=270, height=355, corner_radius=10)
        self.gps_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.gps_label = ctk.CTkLabel(master=self.gps_frame, width=80, height=25,
                                      corner_radius=10, fg_color="gray35",
                                      text="GNSS",
                                      font=self.font)
        self.gps_label.place(relx=0.5, rely=0.07, anchor=tkinter.CENTER)

        self.latitude_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="Latitude:     00.0000000",
                                                font=self.font)
        self.latitude_data_label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.longitude_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                 corner_radius=10,
                                                 text="Longitude:    00.0000000",
                                                 font=self.font)
        self.longitude_data_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.latitude_origin_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                       corner_radius=10,
                                                       text="H.Latitude:     00.0000000",
                                                       font=self.font)
        self.latitude_origin_data_label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.longitude_origin_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                        corner_radius=10,
                                                        text="H.Longitude:    00.0000000",
                                                        font=self.font)
        self.longitude_origin_data_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.north_vel_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                 corner_radius=10,
                                                 text="Vel N: 0",
                                                 font=self.font)
        self.north_vel_data_label.place(relx=0.18, rely=0.6, anchor=tkinter.CENTER)

        self.east_vel_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="E: 0",
                                                font=self.font)
        self.east_vel_data_label.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.down_vel_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="D: 0",
                                                font=self.font)
        self.down_vel_data_label.place(relx=0.82, rely=0.6, anchor=tkinter.CENTER)

        self.gps_alt_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="Altitude: 0",
                                               font=self.font)
        self.gps_alt_data_label.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

        self.head_motion_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                   corner_radius=10,
                                                   text="HoM: 0",
                                                   font=self.font)
        self.head_motion_data_label.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

        self.gps_fix_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="Fix: 0",
                                               font=self.font)
        self.gps_fix_data_label.place(relx=0.3, rely=0.8, anchor=tkinter.CENTER)

        self.gps_sat_count_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                     corner_radius=10,
                                                     text="Sats: 0",
                                                     font=self.font)
        self.gps_sat_count_data_label.place(relx=0.7, rely=0.8, anchor=tkinter.CENTER)

        self.hdop_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                            corner_radius=10,
                                            text="HDoP: 0",
                                            font=self.font)
        self.hdop_data_label.place(relx=0.3, rely=0.9, anchor=tkinter.CENTER)

        self.vdop_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                            corner_radius=10,
                                            text="VDoP: 0",
                                            font=self.font)
        self.vdop_data_label.place(relx=0.7, rely=0.9, anchor=tkinter.CENTER)

        # Bottom Frame  /******************************************************************************/
        self.bottom_frame = ctk.CTkFrame(master=self.root, width=1600, height=120,
                                         corner_radius=20)
        self.bottom_frame.place(relx=0.422, rely=0.935, anchor=tkinter.CENTER)

        # Utility Frame 1 //////////////////////////////////////////////////////////////////////////////
        self.utility_1_frame = ctk.CTkFrame(master=self.bottom_frame, width=180, height=100,
                                            corner_radius=10)
        self.utility_1_frame.place(relx=0.062, rely=0.5, anchor=tkinter.CENTER)

        self.battery_volt_label = ctk.CTkLabel(master=self.utility_1_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="Battery: 4.2V",
                                               font=self.font2)
        self.battery_volt_label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.rssi_label = ctk.CTkLabel(master=self.utility_1_frame, width=100, height=25,
                                       corner_radius=10,
                                       text="RSSI: -20 dBm",
                                       font=self.font2)
        self.rssi_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.packet_drop_ratio_label = ctk.CTkLabel(master=self.utility_1_frame, width=100, height=25,
                                                    corner_radius=10,
                                                    text="PDR: 0%",
                                                    font=self.font2)
        self.packet_drop_ratio_label.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        # Utility Frame 2 //////////////////////////////////////////////////////////////////////////////
        self.utility_2_frame = ctk.CTkFrame(master=self.bottom_frame, width=400, height=100,
                                            corner_radius=10)
        self.utility_2_frame.place(relx=0.25, rely=0.5, anchor=tkinter.CENTER)

        self.attitude_pitch_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                                 corner_radius=10,
                                                 text="Att  θ: 12.21",
                                                 font=self.font2)
        self.attitude_pitch_label.place(relx=0.2, rely=0.24, anchor=tkinter.CENTER)

        self.attitude_roll_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="φ: -12.61",
                                                font=self.font2)
        self.attitude_roll_label.place(relx=0.5, rely=0.24, anchor=tkinter.CENTER)

        self.attitude_heading_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                                   corner_radius=10,
                                                   text="ψ: 112.60",
                                                   font=self.font2)
        self.attitude_heading_label.place(relx=0.8, rely=0.24, anchor=tkinter.CENTER)

        self.target_attitude_pitch_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                                        corner_radius=10,
                                                        text="T.Att  θ: 12.21",
                                                        font=self.font2)
        self.target_attitude_pitch_label.place(relx=0.18, rely=0.55, anchor=tkinter.CENTER)

        self.target_attitude_roll_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                                       corner_radius=10,
                                                       text="φ: -12.61",
                                                       font=self.font2)
        self.target_attitude_roll_label.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        self.target_attitude_heading_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                                          corner_radius=10,
                                                          text="ψ: 112.60",
                                                          font=self.font2)
        self.target_attitude_heading_label.place(relx=0.8, rely=0.55, anchor=tkinter.CENTER)

        self.target_dps_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="t_dps   θ: 12.21 φ: -12.61 ψ: 112.60",
                                             font=("Arial", 12, "bold"))
        self.target_dps_label.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

        # Utility Frame 3 //////////////////////////////////////////////////////////////////////////////
        self.utility_3_frame = ctk.CTkFrame(master=self.bottom_frame, width=180, height=100,
                                            corner_radius=10)
        self.utility_3_frame.place(relx=0.438, rely=0.5, anchor=tkinter.CENTER)

        self.calibrated_altitude_label = ctk.CTkLabel(master=self.utility_3_frame, width=100, height=25,
                                                      corner_radius=10,
                                                      text="Alt: 10.85 m",
                                                      font=self.font2)
        self.calibrated_altitude_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.target_altitude_label = ctk.CTkLabel(master=self.utility_3_frame, width=100, height=25,
                                                  corner_radius=10,
                                                  text="T.Alt: 10.85 m",
                                                  font=self.font2)
        self.target_altitude_label.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        # Utility Frame 4 //////////////////////////////////////////////////////////////////////////////
        self.utility_4_frame = ctk.CTkFrame(master=self.bottom_frame, width=340, height=100,
                                            corner_radius=10)
        self.utility_4_frame.place(relx=0.607, rely=0.5, anchor=tkinter.CENTER)

        self.velocity_x_label = ctk.CTkLabel(master=self.utility_4_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="Vel X: 0.6",
                                             font=self.font2)
        self.velocity_x_label.place(relx=0.2, rely=0.3, anchor=tkinter.CENTER)

        self.velocity_y_label = ctk.CTkLabel(master=self.utility_4_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="Y: 0.2",
                                             font=self.font2)
        self.velocity_y_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.velocity_z_label = ctk.CTkLabel(master=self.utility_4_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="Z: 0.8",
                                             font=self.font2)
        self.velocity_z_label.place(relx=0.8, rely=0.3, anchor=tkinter.CENTER)

        self.target_velocity_x_label = ctk.CTkLabel(master=self.utility_4_frame, width=100, height=25,
                                                    corner_radius=10,
                                                    text="T.Vel X: 0.7",
                                                    font=self.font2)
        self.target_velocity_x_label.place(relx=0.18, rely=0.7, anchor=tkinter.CENTER)

        self.target_velocity_y_label = ctk.CTkLabel(master=self.utility_4_frame, width=100, height=25,
                                                    corner_radius=10,
                                                    text="Y: 0.1",
                                                    font=self.font2)
        self.target_velocity_y_label.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.target_velocity_z_label = ctk.CTkLabel(master=self.utility_4_frame, width=100, height=25,
                                                    corner_radius=10,
                                                    text="Z: -0.1",
                                                    font=self.font2)
        self.target_velocity_z_label.place(relx=0.8, rely=0.7, anchor=tkinter.CENTER)

        # Utility Frame 5 //////////////////////////////////////////////////////////////////////////////

        self.utility_5_frame = ctk.CTkFrame(master=self.bottom_frame, width=440, height=100,
                                            corner_radius=10)
        self.utility_5_frame.place(relx=0.857, rely=0.5, anchor=tkinter.CENTER)

        self.target_latitude_label = ctk.CTkLabel(master=self.utility_5_frame, width=100, height=25,
                                                  corner_radius=10,
                                                  text="T.Lat:  00.0000000",
                                                  font=self.font2)
        self.target_latitude_label.place(relx=0.25, rely=0.3, anchor=tkinter.CENTER)

        self.target_longitude_label = ctk.CTkLabel(master=self.utility_5_frame, width=100, height=25,
                                                   corner_radius=10,
                                                   text="T.Lon:  00.0000000",
                                                   font=self.font2)
        self.target_longitude_label.place(relx=0.75, rely=0.3, anchor=tkinter.CENTER)

        self.target_point_label = ctk.CTkLabel(master=self.utility_5_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="T.Point: N/A",
                                               font=self.font2)
        self.target_point_label.place(relx=0.2, rely=0.7, anchor=tkinter.CENTER)

        self.dist_to_target_2d_label = ctk.CTkLabel(master=self.utility_5_frame, width=100, height=25,
                                                    corner_radius=10,
                                                    text="Dist: 10.0",
                                                    font=self.font2)
        self.dist_to_target_2d_label.place(relx=0.55, rely=0.7, anchor=tkinter.CENTER)

        self.vel_2d_label = ctk.CTkLabel(master=self.utility_5_frame, width=100, height=25,
                                         corner_radius=10,
                                         text="Vel: 1.0",
                                         font=self.font2)
        self.vel_2d_label.place(relx=0.8, rely=0.7, anchor=tkinter.CENTER)

    def delete_trail_func(self):

        drone_path_coordinates.clear()
        self.drone_path.set_position_list([(0, 0), (0, 0)])

    def update_ui(self):
        self.root.mainloop()

    def update_telemetry_ui(self):

        # LOW BATTERY LOGIC
        if (((3.7 <= telemetry_data_dict["battery_voltage"] < 4.3)
             or (10.5 <= telemetry_data_dict["battery_voltage"] < 12.7))):
            if self.battery_volt_label.cget("fg_color") != "darkgreen":
                self.battery_volt_label.configure(fg_color="darkgreen")
        elif self.battery_volt_label.cget("fg_color") != "red4":
            self.battery_volt_label.configure(fg_color="red4")

        self.gyro_x_data_label.configure(text=f"X: {telemetry_data_dict['gyro_x_dps']:.1f}")
        self.gyro_y_data_label.configure(text=f"Y: {telemetry_data_dict['gyro_y_dps']:.1f}")
        self.gyro_z_data_label.configure(text=f"Z: {telemetry_data_dict['gyro_z_dps']:.1f}")

        self.accel_x_data_label.configure(text=f"X: {telemetry_data_dict['acc_x_ms2']:.1f}")
        self.accel_y_data_label.configure(text=f"Y: {telemetry_data_dict['acc_y_ms2']:.1f}")
        self.accel_z_data_label.configure(text=f"Z: {telemetry_data_dict['acc_z_ms2']:.1f}")

        self.mag_x_data_label.configure(text=f"X: {telemetry_data_dict['mag_x_gauss']:.0f}")
        self.mag_y_data_label.configure(text=f"Y: {telemetry_data_dict['mag_y_gauss']:.0f}")
        self.mag_z_data_label.configure(text=f"Z: {telemetry_data_dict['mag_z_gauss']:.0f}")

        self.imu_core_temp_label.configure(text=f"IMU Temp:    {telemetry_data_dict['imu_temperature']:.1f} °C")

        self.pressure_data_label.configure(
            text=f"Pressure:             {telemetry_data_dict['barometer_pressure']:.1f} hPa")
        self.temp_data_label.configure(text=f"Temperature:       {telemetry_data_dict['barometer_temperature']:.1f} °C")
        self.altitude_data_label.configure(text=f"Altitude:                 {telemetry_data_dict['altitude']:.1f} m")

        self.tof_range_label.configure(text=f"Range:      {telemetry_data_dict['tof_distance'] * 100.0:.1f}")
        self.throttle_label.configure(text=f"Throttle: {telemetry_data_dict['throttle']:.0f}")

        self.battery_volt_label.configure(text=f"Battery: {telemetry_data_dict['battery_voltage']:.1f} V")
        self.rssi_label.configure(text=f"RSSI: {telemetry_data_dict['RSSI']:.0f} dBm")
        self.packet_drop_ratio_label.configure(text=f"PDR: {telemetry_data_dict['packet_drop_ratio']:.0f} %")

        self.attitude_pitch_label.configure(text=f"Att θ: {telemetry_data_dict['pitch']:.1f}")
        self.attitude_roll_label.configure(text=f"φ: {telemetry_data_dict['roll']:.1f}")
        self.attitude_heading_label.configure(text=f"ψ: {telemetry_data_dict['heading']:.1f}")

        self.target_attitude_pitch_label.configure(text=f"T.Att θ: {telemetry_data_dict['target_pitch']:.1f}")
        self.target_attitude_roll_label.configure(text=f"φ: {telemetry_data_dict['target_roll']:.1f}")
        self.target_attitude_heading_label.configure(text=f"ψ: {telemetry_data_dict['target_heading']:.1f}")

        self.target_dps_label.configure(text=f"tdps   "
                                             f"θ: {telemetry_data_dict['target_pitch_dps']:.1f} "
                                             f"φ: {telemetry_data_dict['target_roll_dps']:.1f} "
                                             f"ψ: {telemetry_data_dict['target_yaw_dps']:.1f}")

        self.calibrated_altitude_label.configure(text=f"Alt: {telemetry_data_dict['altitude_calibrated']:.1f} m")
        self.target_altitude_label.configure(text=f"T.Alt: {telemetry_data_dict['target_altitude']:.1f} m")

        self.velocity_x_label.configure(text=f"Vel X: {telemetry_data_dict['velocity_x_ms']:.1f}")
        self.velocity_y_label.configure(text=f"Y: {telemetry_data_dict['velocity_y_ms']:.1f}")
        self.velocity_z_label.configure(text=f"Z: {telemetry_data_dict['velocity_z_ms']:.1f}")

        self.target_velocity_x_label.configure(text=f"T.Vel X: {telemetry_data_dict['target_velocity_x_ms']:.1f}")
        self.target_velocity_y_label.configure(text=f"Y: {telemetry_data_dict['target_velocity_y_ms']:.1f}")
        self.target_velocity_z_label.configure(text=f"Z: {telemetry_data_dict['target_velocity_z_ms']:.1f}")

        self.flow_x_vel_data_label.configure(text=f"X: {telemetry_data_dict['flow_x_velocity'] * 100.0:.1f}")
        self.flow_y_vel_data_label.configure(text=f"Y: {telemetry_data_dict['flow_y_velocity'] * 100.0:.1f}")
        self.flow_quality_data_label.configure(text=f"Q: {telemetry_data_dict['flow_quality']:.0f}%")

        self.drone_location_marker.set_text(f"{telemetry_data_dict['altitude_calibrated']:.1f}m")


        heading_rounded = int(round(telemetry_data_dict["heading"], -1) / 10.0)
        if heading_rounded == 36: heading_rounded = 0
        target_heading_rounded = int(round(telemetry_data_dict["target_heading"], -1) / 10.0)
        if target_heading_rounded == 36: target_heading_rounded = 0
        cog_rounded = int(round(telemetry_data_dict["gps_headingOfMotion"], -1) / 10.0)
        if cog_rounded == 36: cog_rounded = 0


        self.drone_location_marker.change_icon(self.drone_images_degree_list[heading_rounded])
        self.cog_direction_marker.change_icon(self.cog_direction_images_degree_list[cog_rounded])
        self.target_direction_marker.change_icon(self.target_direction_images_degree_list[target_heading_rounded])

        self.drone_location_marker.set_position(telemetry_data_dict["gps_latitude"], telemetry_data_dict["gps_longitude"])
        self.cog_direction_marker.set_position(telemetry_data_dict["gps_latitude"], telemetry_data_dict["gps_longitude"])
        self.target_direction_marker.set_position(telemetry_data_dict["gps_latitude"], telemetry_data_dict["gps_longitude"])

        self.latitude_data_label.configure(text=f"Latitude:            {telemetry_data_dict['gps_latitude']:.7f}")
        self.longitude_data_label.configure(text=f"Longitude:        {telemetry_data_dict['gps_longitude']:.7f}")
        self.latitude_origin_data_label.configure(
            text=f"H.Latitude:        {telemetry_data_dict['gps_latitude_origin']:.7f}")
        self.longitude_origin_data_label.configure(
            text=f"H.Longitude:     {telemetry_data_dict['gps_longitude_origin']:.7f}")
        self.north_vel_data_label.configure(text=f"V N: {telemetry_data_dict['gps_northVel_ms']:.1f}")
        self.east_vel_data_label.configure(text=f"E: {telemetry_data_dict['gps_eastVel_ms']:.1f}")
        self.down_vel_data_label.configure(text=f"D: {telemetry_data_dict['gps_downVel_ms']:.1f}")
        self.gps_alt_data_label.configure(text=f"Altitude: {telemetry_data_dict['gps_altitude_m']:.1f}")
        self.head_motion_data_label.configure(text=f"HoM: {telemetry_data_dict['gps_headingOfMotion']:.1f}")
        self.gps_fix_data_label.configure(text=f"Fix: {telemetry_data_dict['gps_fix']:.0f}")
        self.gps_sat_count_data_label.configure(text=f"Sats: {telemetry_data_dict['gps_satCount']:.0f}")
        self.hdop_data_label.configure(text=f"HDoP: {telemetry_data_dict['gps_hdop']:.1f}")
        self.vdop_data_label.configure(text=f"VDoP: {telemetry_data_dict['gps_vdop']:.1f}")
        self.target_latitude_label.configure(text=f"T.Lat: {telemetry_data_dict['target_latitude']:.7f}")
        self.target_longitude_label.configure(text=f"T.Lon: {telemetry_data_dict['target_longitude']:.7f}")
        self.dist_to_target_2d_label.configure(text=f"D2D: {telemetry_data_dict['distance_m_2d']:.2f}")
        self.vel_2d_label.configure(text=f"V2D: {telemetry_data_dict['velocity_ms_2d']:.2f}")

        if telemetry_data_dict["arm_status"] != self.prev_arm_status:

            if telemetry_data_dict["arm_status"] == 1:
                if not serial_backend.blackbox_state:
                    if self.bb_auto_record:
                        self.blackbox()
                self.arm_utility_frame.configure(fg_color="dim gray")

                self.calibrate_mag_button.configure(state="disabled")
                self.motor_test_button.configure(state="disable")
            else:
                if serial_backend.blackbox_state and self.bb_auto_record:
                    self.blackbox()
                self.arm_utility_frame.configure(fg_color="gray13")

                self.calibrate_mag_button.configure(state="enabled")
                self.motor_test_button.configure(state="enabled")
        self.prev_arm_status = telemetry_data_dict["arm_status"]

        if telemetry_data_dict["flight_mode"] != self.prev_flight_mode:
            if telemetry_data_dict["flight_mode"] == 0:
                self.alt_hold_button.configure(image=self.alt_hold_passive_img)
                self.pos_hold_button.configure(image=self.pos_hold_passive_img)
                self.waypoint_button.configure(image=self.waypoint_passive_img)
            elif telemetry_data_dict["flight_mode"] == 1:
                self.alt_hold_button.configure(image=self.alt_hold_active_img)
                self.pos_hold_button.configure(image=self.pos_hold_passive_img)
                self.waypoint_button.configure(image=self.waypoint_passive_img)
            elif telemetry_data_dict["flight_mode"] == 2:
                self.alt_hold_button.configure(image=self.alt_hold_passive_img)
                self.pos_hold_button.configure(image=self.pos_hold_active_img)
                self.waypoint_button.configure(image=self.waypoint_passive_img)
            elif telemetry_data_dict["flight_mode"] == 3:
                self.alt_hold_button.configure(image=self.alt_hold_active_img)
                self.pos_hold_button.configure(image=self.pos_hold_active_img)
                self.waypoint_button.configure(image=self.waypoint_passive_img)
            elif telemetry_data_dict["flight_mode"] == 4:
                self.alt_hold_button.configure(image=self.alt_hold_active_img)
                self.pos_hold_button.configure(image=self.pos_hold_active_img)
                self.waypoint_button.configure(image=self.waypoint_active_img)

        self.prev_flight_mode = telemetry_data_dict["flight_mode"]

        if (telemetry_data_dict["gps_latitude_origin"] != self.prev_origin_latitude) \
                or (telemetry_data_dict["gps_longitude_origin"] != self.prev_origin_longitude):
            self.drone_origin_marker.set_position(telemetry_data_dict["gps_latitude_origin"],
                                                  telemetry_data_dict["gps_longitude_origin"])

        self.prev_origin_latitude = telemetry_data_dict["gps_latitude_origin"]
        self.prev_origin_longitude = telemetry_data_dict["gps_longitude_origin"]

        if (telemetry_data_dict["target_latitude"] != self.prev_target_latitude or
                telemetry_data_dict["target_longitude"] != self.prev_target_longitude):

            self.target_location_marker.set_position(telemetry_data_dict["target_latitude"],
                                                     telemetry_data_dict["target_longitude"])

            idx, dist = find_nearest_coordinate((telemetry_data_dict["target_latitude"],
                                                 telemetry_data_dict["target_longitude"]), waypoint_coordinates)

            if idx is not None:

                if dist < 100.0:
                    self.target_point_label.configure(text=f"T.Point: -WP {idx + 1}-")
                elif get_distance_from_lat_lon(telemetry_data_dict["target_latitude"],
                                               telemetry_data_dict["target_longitude"],
                                               telemetry_data_dict["gps_latitude_origin"],
                                               telemetry_data_dict["gps_longitude_origin"]) < 100.0:
                    self.target_point_label.configure(text=f"T.Point: -Home-")
                else:
                    self.target_point_label.configure(text=f"T.Point: -Arbitrary-")

                self.prev_target_latitude = telemetry_data_dict["target_latitude"]
                self.prev_target_longitude = telemetry_data_dict["target_longitude"]

        if telemetry_data_dict["is_gnss_sanity_check_ok"] != 1:
            self.gps_outer_frame.configure(fg_color="#880808")  # RED
        else:
            self.gps_outer_frame.configure(fg_color="#008000")  # GREEN

        ####################################################################################

        if ((abs(telemetry_data_dict["gps_latitude"] - self.prev_latitude) > 0.00001
             or abs(telemetry_data_dict["gps_longitude"] - self.prev_longitude) > 0.00001)
                and (telemetry_data_dict["gps_latitude"] != 0
                     or telemetry_data_dict["gps_longitude"] != 0)):

            drone_path_coordinates.append((telemetry_data_dict["gps_latitude"],
                                           telemetry_data_dict["gps_longitude"]))

            if len(drone_path_coordinates) > 1:
                self.drone_path.set_position_list(drone_path_coordinates)

            self.prev_latitude = telemetry_data_dict["gps_latitude"]
            self.prev_longitude = telemetry_data_dict["gps_longitude"]

        if self.is_auto_mission_create_requested:
            if amc.is_auto_mission_planned():
                print("done.")
                self.is_auto_mission_create_requested = 0
                alt = 0
                if self.auto_mission_reverse == 1:
                    amc.bas_ve_son_noktalar_latlon.reverse()

                if self.wp_altitude_input.get() != "":
                    a = int(float(self.wp_altitude_input.get()) * 10)
                    if 0 <= alt <= 255:
                        alt = a
                for i in range(len(amc.bas_ve_son_noktalar_latlon)):

                    if i < waypoint_limit:
                        # waypoint_coordinates.append((all_points[i][0], all_points[i][1]))
                        waypoint_coordinates.append((amc.bas_ve_son_noktalar_latlon[i][0], amc.bas_ve_son_noktalar_latlon[i][1]))
                        waypoint_counter = waypoint_limit - 1
                        waypoint_only_altitudes.append(alt)

                self.redraw_waypoint_markers()

                total_dist = calculate_wp_distance()
                self.wp_distance_label.configure(text=f"Distance:\n{total_dist:.1f}m")
                self.redraw_wp_distance_markers()

            else:
                print("waiting...")

    def save_mission_function(self):

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Veri Dosyaları", "*.json")])

        if file_path != "":
            slm.save_mission(file_path, self.auto_mission_angle, self.auto_mission_spacing, self.auto_mission_padding, self.auto_mission_reverse, self.auto_mission_invert)
        else:
            print("File Save Canceled")

    def load_mission_function(self):
        global waypoint_coordinates
        global waypoint_only_altitudes
        global field_coordinates

        file_path = filedialog.askopenfilename(filetypes=[("Veri Dosyaları", "*.json")])

        if file_path != "":

            ret = slm.load_mission(file_path)

            waypoint_coordinates = ret["waypoints"]
            waypoint_only_altitudes = ret["altitudes"]
            serial_backend.end_of_wp_mission_behaviour_code = ret["end_of_mission_behavior_code"]
            self.auto_mission_invert = ret["auto_mission_invert"]
            self.auto_mission_reverse = ret["auto_mission_reverse"]
            self.auto_mission_angle = ret["auto_mission_angle"]
            self.auto_mission_spacing = ret["auto_mission_spacing"]
            self.auto_mission_padding = ret["auto_mission_padding"]

            if self.auto_mission_invert == 1:
                self.create_mission_for_field_invert_checkbox.select()
            else:
                self.create_mission_for_field_invert_checkbox.deselect()

            if self.auto_mission_reverse == 1:
                self.create_mission_for_field_reverse_checkbox.select()
            else:
                self.create_mission_for_field_reverse_checkbox.deselect()

            self.create_mission_for_field_spacing_slider.set(ret["auto_mission_spacing"])
            self.create_mission_for_field_spacing_label.configure(text=f"Spc: {ret['auto_mission_spacing']:.1f}")

            self.create_mission_for_field_padding_slider.set(ret["auto_mission_padding"])
            self.create_mission_for_field_padding_label.configure(text=f"Pad: {ret['auto_mission_padding']:.1f}")

            self.create_mission_for_field_angle_slider.set(ret["auto_mission_angle"])
            self.create_mission_for_field_angle_label.configure(text=f"Agl: {ret['auto_mission_angle']:.0f}")

            self.redraw_waypoint_markers()
            total_dist = calculate_wp_distance()
            self.wp_distance_label.configure(text=f"Distance:\n{total_dist:.1f}m")
            self.redraw_wp_distance_markers()

            for i in range(len(ret["field_points"])):

                if i == 0:
                    field_coordinates.append(ret["field_points"][i])
                    self.field_polygon_1 = self.map_widget.set_polygon(field_coordinates, name="field_polygon_1", fill_color=None)
                else:
                    self.field_polygon_1.add_position(ret["field_points"][i][0], ret["field_points"][i][1], index=i + 1)

            self.field_polygon_1.draw()
            self.redraw_field_markers()

        else:
            print("File Open Canceled")

    def add_waypoint_event(self, coords):
        global waypoint_counter, waypoint_altitude

        if self.point_mode == "WP Mode":

            if len(waypoint_coordinates) < waypoint_limit:

                if self.wp_altitude_input.get() != "":
                    alt = int(float(self.wp_altitude_input.get()) * 10)
                    if 0 <= alt <= 255:
                        waypoint_altitude = alt

                waypoint_coordinates.append((coords[0], coords[1]))
                # print("WP coord len: ", len(waypoint_coordinates))
                waypoint_only_altitudes.append(np.uint8(waypoint_altitude))
                waypoint_markers.append(self.map_widget.set_marker(coords[0], coords[1], icon=self.location_img, icon_anchor="s",
                                                                   text=f"{waypoint_counter + 1}|{waypoint_altitude / 10}",
                                                                   text_color="white", font=self.font3))
                waypoint_counter += 1
                if waypoint_counter > 1:
                    self.waypoint_path.set_position_list(waypoint_coordinates)
                total_dist = calculate_wp_distance()
                self.wp_distance_label.configure(text=f"Distance:\n{total_dist:.1f}m")
                self.redraw_wp_distance_markers()

            else:
                print("wp >= limit")

        elif self.point_mode == "Field Mode":

            field_markers.append(self.map_widget.set_marker(coords[0], coords[1], icon=self.polygon_edge_img))

            if len(field_coordinates) == 0:
                field_coordinates.append((coords[0], coords[1]))
                self.field_polygon_1 = self.map_widget.set_polygon(field_coordinates,
                                                                   # command=self.field_clicked_event,
                                                                   name="field_polygon_1", fill_color=None)

            else:
                self.field_polygon_1.add_position(coords[0], coords[1], index=len(field_coordinates))

            self.field_polygon_1.draw()

    def add_waypoint_to_home_event(self):
        global waypoint_counter, waypoint_altitude, telemetry_data_dict

        if (len(waypoint_coordinates) < waypoint_limit and telemetry_data_dict["gps_latitude_origin"] != 0 and
                telemetry_data_dict["gps_longitude_origin"] != 0):

            if self.wp_altitude_input.get() != "":
                alt = int(float(self.wp_altitude_input.get()) * 10)
                if 0 <= alt <= 255:
                    waypoint_altitude = alt

            waypoint_coordinates.append((telemetry_data_dict["gps_latitude_origin"], telemetry_data_dict["gps_longitude_origin"]))
            waypoint_only_altitudes.append(np.uint8(waypoint_altitude))
            waypoint_markers.append(self.map_widget.set_marker(telemetry_data_dict["gps_latitude_origin"],
                                                               telemetry_data_dict["gps_longitude_origin"], icon=self.location_img,
                                                               icon_anchor="s",
                                                               text=f"{waypoint_counter + 1}|{waypoint_altitude / 10}",
                                                               text_color="white", font=self.font3))
            waypoint_counter += 1
            if waypoint_counter > 1:
                self.waypoint_path.set_position_list(waypoint_coordinates)
            total_dist = calculate_wp_distance()
            self.wp_distance_label.configure(text=f"Distance:\n{total_dist:.1f}m")
            self.redraw_wp_distance_markers()
        else:
            print("WP home is zero or wp >= limit")

    def delete_all_points_event(self):

        if self.point_mode == "WP Mode":
            response = messagebox.askokcancel("WAYPOINTS", "Delete WAYPOINTS?")
            if response:
                self.clear_waypoints()

        elif self.point_mode == "Field Mode":
            response = messagebox.askokcancel("FIELD", "Delete FIELD POINTS?")
            if response:
                field_coordinates.clear()

                for item in field_markers:
                    item.delete()

                field_markers.clear()
                self.field_polygon_1.delete()

    def clear_waypoints(self):
        global waypoint_counter

        waypoint_coordinates.clear()
        waypoint_only_altitudes.clear()
        for item in waypoint_markers:
            item.delete()

        for item in wp_distance_markers:
            item.delete()

        waypoint_counter = 0
        self.waypoint_path.set_position_list([(0.0, 0.0), (0.0, 0.0)])
        total_dist = calculate_wp_distance()
        self.wp_distance_label.configure(text=f"Distance:\n{total_dist:.1f}m")
        self.redraw_wp_distance_markers()

    def delete_waypoint_event(self, coords):
        global waypoint_counter

        if self.point_mode == "WP Mode":

            if len(waypoint_coordinates) == 1:
                self.delete_all_points_event()
            else:
                index, distance = find_nearest_coordinate(coords, waypoint_coordinates)
                del waypoint_coordinates[index]
                del waypoint_only_altitudes[index]
                waypoint_markers[index].delete()
                del waypoint_markers[index]
                self.redraw_waypoint_markers()
            # total_dist = calculate_wp_distance()
            # self.wp_distance_label.configure(text=f"Distance:\n{total_dist:.1f}m")
            # self.redraw_wp_distance_markers()

        elif self.point_mode == "Field Mode":

            if len(field_coordinates) == 1:
                self.delete_all_points_event()
            else:
                index, distance = find_nearest_coordinate(coords, field_coordinates)
                self.field_polygon_1.remove_position(field_coordinates[index][0], field_coordinates[index][1])
                self.redraw_field_markers()
                self.field_polygon_1.draw()

    def redraw_field_markers(self):

        for index in field_markers:
            index.delete()
        field_markers.clear()

        for index, value in enumerate(field_coordinates):
            field_markers.append(self.map_widget.set_marker(value[0], value[1], icon=self.polygon_edge_img))

    def redraw_waypoint_markers(self):
        global waypoint_counter

        for index in waypoint_markers:
            index.delete()
        waypoint_markers.clear()
        for index, value in enumerate(waypoint_coordinates):
            waypoint_markers.append(self.map_widget.set_marker(value[0], value[1], icon=self.location_img, icon_anchor="s",
                                                               text=f"{index + 1}|{waypoint_only_altitudes[index] / 10}",
                                                               text_color="white",
                                                               font=self.font3))
            waypoint_counter = index + 1

        total_dist = calculate_wp_distance()
        self.wp_distance_label.configure(text=f"Distance:\n{total_dist:.1f}m")
        self.redraw_wp_distance_markers()

        if len(waypoint_coordinates) < 2:
            self.waypoint_path.set_position_list([(0.0, 0.0), (0.0, 0.0)])
        else:
            self.waypoint_path.set_position_list(waypoint_coordinates)

        if serial_backend.end_of_wp_mission_behaviour_code == 0:
            self.land_after_wp_checkbox.deselect()
            self.rth_after_wp_checkbox.deselect()
            self.land_after_wp_checkbox.configure(state="disabled")
        elif serial_backend.end_of_wp_mission_behaviour_code == 1:
            self.land_after_wp_checkbox.deselect()
            self.land_after_wp_checkbox.configure(state="normal")
            self.rth_after_wp_checkbox.select()
        elif serial_backend.end_of_wp_mission_behaviour_code == 2:
            self.land_after_wp_checkbox.select()
            self.land_after_wp_checkbox.configure(state="normal")
            self.rth_after_wp_checkbox.select()

    def redraw_wp_distance_markers(self):

        for item in wp_distance_markers:
            item.delete()

        wp_distance_markers.clear()

        if len(wp_distance_marker_coordinates) > 0:
            for index, item in enumerate(wp_distance_marker_coordinates):
                wp_distance_markers.append(self.map_widget.set_marker(item[0], item[1], icon=self.dist_empty_img, icon_anchor="n",
                                                                      text=f"{distance_between_wp_coordinates_list[index]:.1f}",
                                                                      text_color="white", font=("Ezarion", 11, "bold")))

    def create_mission_for_field_angle_slider_event(self, value):
        self.auto_mission_angle = self.create_mission_for_field_angle_slider.get()
        self.create_mission_for_field_angle_label.configure(text=f"Agl: {self.auto_mission_angle:.0f}")

    def create_mission_for_field_padding_slider_event(self, value):
        self.auto_mission_padding = self.create_mission_for_field_padding_slider.get()
        self.create_mission_for_field_padding_label.configure(text=f"Pad: {self.auto_mission_padding:.1f}")

    def create_mission_for_field_spacing_slider_event(self, value):
        self.auto_mission_spacing = self.create_mission_for_field_spacing_slider.get()
        self.create_mission_for_field_spacing_label.configure(text=f"Spc: {self.auto_mission_spacing:.1f}")

    def create_mission_for_field_invert_checkbox_event(self):
        value = self.create_mission_for_field_invert_checkbox_variable.get()
        if value == "off":
            self.auto_mission_invert = 0
        else:
            self.auto_mission_invert = 1

    def create_mission_for_field_reverse_checkbox_event(self):
        value = self.create_mission_for_field_reverse_checkbox_variable.get()
        if value == "off":
            self.auto_mission_reverse = 0
        else:
            self.auto_mission_reverse = 1

    def create_mission_for_field_function(self):
        global waypoint_counter

        if len(field_coordinates) > 2:

            self.clear_waypoints()
            amc.request_create_mission_from_point_list(field_coordinates, self.auto_mission_spacing, self.auto_mission_angle + 5, self.auto_mission_padding,
                                                       self.auto_mission_invert)
            self.is_auto_mission_create_requested = 1
            alt = 0
            # if no telemetry, feel free to block the main loop
            # if telemetry available than dont block, check if mission ready with ui update loop
            if telemetry_data_dict["packet_drop_ratio"] == 100:

                while self.is_auto_mission_create_requested == 1:

                    if amc.is_auto_mission_planned():

                        if self.auto_mission_reverse == 1:
                            amc.bas_ve_son_noktalar_latlon.reverse()

                        self.is_auto_mission_create_requested = 0

                        if self.wp_altitude_input.get() != "":
                            a = int(float(self.wp_altitude_input.get()) * 10)
                            if 0 <= alt <= 255:
                                alt = a

                        for i in range(len(amc.bas_ve_son_noktalar_latlon)):

                            if i < waypoint_limit:
                                # waypoint_coordinates.append((all_points[i][0], all_points[i][1]))
                                waypoint_coordinates.append((amc.bas_ve_son_noktalar_latlon[i][0], amc.bas_ve_son_noktalar_latlon[i][1]))
                                waypoint_counter = waypoint_limit - 1
                                waypoint_only_altitudes.append(alt)

                        self.redraw_waypoint_markers()
                        total_dist = calculate_wp_distance()
                        self.wp_distance_label.configure(text=f"Distance:\n{total_dist:.1f}m")
                        self.redraw_wp_distance_markers()

                    else:
                        time.sleep(0.5)

                print("all: ", amc.bas_ve_son_noktalar_latlon)
                print("field: ", field_coordinates)
        else:

            print("field needs to be more than 2 points")
            # print("all: ", all_points)
            # print("wp: ", wp)

    def rth_after_wp_checkbox_event(self):

        value = self.rth_after_wp_checkbox_variable.get()

        if value == "off":
            self.land_after_wp_checkbox.deselect()
            self.land_after_wp_checkbox.configure(state="disabled")
            serial_backend.end_of_wp_mission_behaviour_code = 0
        else:
            self.land_after_wp_checkbox.configure(state="normal")
            serial_backend.end_of_wp_mission_behaviour_code = 1

    def land_after_wp_checkbox_event(self):

        value = self.land_after_wp_checkbox_variable.get()

        if value == "off":
            serial_backend.end_of_wp_mission_behaviour_code = 1
        else:
            serial_backend.end_of_wp_mission_behaviour_code = 2

    def center_drone(self):
        # This has to be 2 times to work
        self.map_widget.set_zoom(int(self.map_widget.zoom))
        self.map_widget.set_position(float(telemetry_data_dict["gps_latitude"]),
                                     float(telemetry_data_dict["gps_longitude"]))
        self.map_widget.set_position(float(telemetry_data_dict["gps_latitude"]),
                                     float(telemetry_data_dict["gps_longitude"]))

    def center_map_func(self):
        # This has to be 2 times to work
        self.map_widget.set_zoom(int(self.map_widget.zoom))
        self.map_widget.set_position(39.110946, 27.187785)
        self.map_widget.set_position(39.110946, 27.187785)

    def auto_blackbox(self):
        if self.bb_auto_record:
            self.bb_auto_record = False
            self.blackbox_auto_record_button.configure(fg_color="gray20")
        else:
            self.bb_auto_record = True
            self.blackbox_auto_record_button.configure(fg_color="green")

    def blackbox(self):

        if serial_backend.blackbox_state:
            self.blackbox_button.configure(image=self.blackbox_passive_img)
            serial_backend.blackbox_state = False
        else:
            self.blackbox_button.configure(image=self.blackbox_active_img)
            time_now = datetime.now()
            serial_backend.blackbox_file_name = (str(time_now.year)
                                                 + "_" + str(time_now.month)
                                                 + "_" + str(time_now.day)
                                                 + "_" + str(time_now.hour)
                                                 + "_" + str(time_now.minute)
                                                 + "_" + str(time_now.second)
                                                 + ".csv")
            df = pd.DataFrame([telemetry_data_dict])
            df.to_csv("C:/Users/erayd/OneDrive/Masaüstü/Project STARLING/flight_logs/"
                      + serial_backend.blackbox_file_name, mode='a', index=False, header=True)
            serial_backend.blackbox_state = True

    def calibrate_mag_event(self):

        if mag_calibration.calibration_state == 0:
            response = messagebox.askokcancel("Start Mag Calibration", "Are you sure?")
            if response:
                serial_backend.mag_x_raw.clear()
                serial_backend.mag_y_raw.clear()
                serial_backend.mag_z_raw.clear()
                serial_backend.gather_mag_data_for_calibration = True
                self.calibrate_mag_button.configure(text="Stop Mag Cal")
                mag_calibration.calibration_state = 1

        elif mag_calibration.calibration_state == 1:
            serial_backend.gather_mag_data_for_calibration = False
            self.calibrate_mag_button.configure(text="Start Mag Cal")
            mag_calibration.calibration_state = 0
            if len(serial_backend.mag_x_raw) >= 250:
                mag_calibration.Magnetometer().run()
                show_mag_cal_data()
            else:
                messagebox.showinfo("Error!", "Not enough data points gathered to perform calibration!!")
                print("Not enough data points gathered to perform calibration!!")

    def calibrate_acc_event(self):

        if acc_calibration.state == 0:
            response = messagebox.askokcancel("Start Acc Calibration", "Are you sure?")

            if response:
                serial_backend.acc_calib_values.clear()
                serial_backend.acc_calib_values.append(
                    (telemetry_data_dict["acc_x_ms2"], telemetry_data_dict["acc_y_ms2"]))
                self.calibrate_acc_button.configure(text="Turn 180°")
                acc_calibration.state = 1

        elif acc_calibration.state == 1:
            serial_backend.acc_calib_values.append((telemetry_data_dict["acc_x_ms2"], telemetry_data_dict["acc_y_ms2"]))
            self.calibrate_acc_button.configure(text="Start Acc Cal")
            acc_calibration.state = 0
            serial_backend.acc_calib_result.clear()
            serial_backend.acc_calib_result.append(
                (serial_backend.acc_calib_values[0][0] + serial_backend.acc_calib_values[1][0]) / 2)
            serial_backend.acc_calib_result.append(
                (serial_backend.acc_calib_values[0][1] + serial_backend.acc_calib_values[1][1]) / 2)

            response = messagebox.askokcancel("Send Acc Calibration",
                                              f"X: {serial_backend.acc_calib_result[0]:.2f}   Y: {serial_backend.acc_calib_result[1]:.2f}")

            if response:
                serial_backend.send_gamepad_data = False
                serial_backend.send_acc_calib_data = True

    def wp_field_mode_selection(self):
        self.point_mode = self.wp_field_mode_tabview.get()

    def close_application(self):
        self.isAppAlive = False
        self.root.destroy()
        quit()


def find_nearest_coordinate(target_coord, coord_list):
    if not coord_list:
        return None, None  # Koordinat listesi boşsa None döndür

    # Başlangıçta en küçük mesafeyi sonsuz olarak ayarlayın
    min_distance = float('inf')
    nearest_index = None

    # Koordinat listesinde dolaşın ve en yakın koordinatı bulun
    for i, coord in enumerate(coord_list):
        x, y = coord
        target_x, target_y = target_coord

        distance = get_distance_from_lat_lon(x, y, target_x, target_y)

        # Eğer şu ana kadar hesaplanan en küçük mesafeden daha küçükse güncelle
        if distance < min_distance:
            min_distance = distance
            nearest_index = i

    return nearest_index, min_distance


def write_waypoints():
    response = messagebox.askokcancel("Send WP mission?", "Are you sure?")
    if response:
        serial_backend.send_gamepad_data = False
        serial_backend.send_waypoints_data = True


def read_waypoints():
    response = messagebox.askokcancel("Read WP mission?", "Are you sure?")
    if response:
        serial_backend.send_gamepad_data = False
        serial_backend.request_wp_data = True


def dummy_func():
    pass


def show_mag_cal_data():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    config_window = ctk.CTkToplevel()
    # config_window.iconbitmap("UAV_Project_LOGO_icon.ico")
    config_window.geometry("320x320")
    config_window.title("Calibration Result")
    config_window.grab_set()
    config_window.resizable(False, False)

    # MAIN FRAME
    main_frame = ctk.CTkFrame(master=config_window, width=300, height=300, corner_radius=10)
    main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    textbox = ctk.CTkTextbox(master=main_frame, width=280, height=220, corner_radius=10, font=("Arial", 14, "bold"))
    textbox.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

    apply_mag_calib_button = ctk.CTkButton(master=main_frame, width=140, height=35, corner_radius=10,
                                           text="Send Calibration Values", font=("Arial", 14, "bold"),
                                           command=send_mag_calib_values)
    apply_mag_calib_button.place(relx=0.5, rely=0.88, anchor=tkinter.CENTER)

    textbox.tag_config("center", justify="center")
    textbox.insert("1.0",
                   f"Length: {len(serial_backend.mag_x_raw)} | Resolution: {mag_calibration.mean_resolution:.0f}\n\n"
                   f"Hard Iron Bias:\n\n"
                   f"X: {mag_calibration.mag_bias[0][0]:.2f}    "
                   f"Y: {mag_calibration.mag_bias[1][0]:.2f}    "
                   f"Z: {mag_calibration.mag_bias[2][0]:.2f}\n\n"
                   f"Soft Iron Matrix:\n\n"
                   f"{mag_calibration.mag_matrix[0][0]:.4f}    "
                   f"{mag_calibration.mag_matrix[0][1]:.4f}    "
                   f"{mag_calibration.mag_matrix[0][2]:.4f}\n"
                   f"{mag_calibration.mag_matrix[1][0]:.4f}    "
                   f"{mag_calibration.mag_matrix[1][1]:.4f}    "
                   f"{mag_calibration.mag_matrix[1][2]:.4f}\n"
                   f"{mag_calibration.mag_matrix[2][0]:.4f}    "
                   f"{mag_calibration.mag_matrix[2][1]:.4f}    "
                   f"{mag_calibration.mag_matrix[2][2]:.4f}", "center")
    textbox.configure(state="disabled")  # configure textbox to be read-only


def send_mag_calib_values():
    response = messagebox.askokcancel("Send Mag Calibration Values", "Are you sure?")
    if response:
        serial_backend.send_gamepad_data = False
        serial_backend.send_mag_calib_data = True


def voice_notification_enable_disable():
    if voice_notify.is_enabled:
        voice_notify.is_enabled = 0
    else:
        voice_notify.is_enabled = 1


def get_distance_from_lat_lon(lat1, lon1, lat2, lon2):
    # Dereceden radyana dönüşüm ((PI / 180) / 10000000)
    lat1_rad = lat1 * (math.pi / 180.0)
    lat2_rad = lat2 * (math.pi / 180.0)
    lon1_rad = lon1 * (math.pi / 180.0)
    lon2_rad = lon2 * (math.pi / 180.0)

    # Enlem ve boylam farklarının hesaplanması
    dLat = lat2_rad - lat1_rad
    dLon = lon2_rad - lon1_rad

    # Haversine mesafesinin hesaplanması
    sin_dlat = math.sin(dLat / 2.0)
    sin_dlon = math.sin(dLon / 2.0)
    cos_lat1 = math.cos(lat1_rad)

    a = sin_dlat * sin_dlat
    distance_north_cm = math.atan2(math.sqrt(a), math.sqrt(1.0 - a)) * 1274200000.0

    if dLat > 0:
        distance_north_cm = -distance_north_cm

    a = cos_lat1 * cos_lat1 * sin_dlon * sin_dlon
    distance_east_cm = math.atan2(math.sqrt(a), math.sqrt(1.0 - a)) * 1274200000.0

    if dLon > 0:
        distance_east_cm = -distance_east_cm

    distance_cm = math.sqrt(distance_north_cm * distance_north_cm + distance_east_cm * distance_east_cm)

    return distance_cm


def calculate_wp_distance():
    global total_wp_distance, distance_between_wp_coordinates_list, wp_distance_marker_coordinates
    total_wp_distance = 0
    distance_between_wp_coordinates_list.clear()
    wp_distance_marker_coordinates.clear()

    if len(waypoint_coordinates) > 1:

        for i in range(1, len(waypoint_coordinates)):
            lat1, lon1 = waypoint_coordinates[i - 1]
            lat2, lon2 = waypoint_coordinates[i]
            dist = get_distance_from_lat_lon(lat1, lon1, lat2, lon2) / 100.0  # cm to m
            distance_between_wp_coordinates_list.append(dist)
            total_wp_distance = total_wp_distance + dist
            wp_distance_marker_coordinates.append(((lat1 + lat2) / 2.0, (lon1 + lon2) / 2.0))
    return total_wp_distance


def save_on_click():
    df = pd.DataFrame([telemetry_data_dict])
    df.to_csv("C:/Users/erayd/OneDrive/Masaüstü/SAVE_ON_CLICK_FILE.csv",
              mode='a', index=False, header=False)
