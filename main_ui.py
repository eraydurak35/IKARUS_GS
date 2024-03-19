import customtkinter as ctk
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


class MainWindow:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.prev_flight_mode = 0
        self.prev_arm_status = 0
        self.prev_origin_latitude = 0
        self.prev_origin_longitude = 0
        self.bb_auto_record = True
        self.root = ctk.CTk()
        self.root.geometry("1920x1080")
        self.root.title("IKARUS Ground Station")
        self.root.attributes('-fullscreen', True)
        self.isAppAlive = True
        self.isBlackBoxRecording = False
        self.map_follow_drone = False

        self.close_img = ctk.CTkImage(Image.open("Close.png"), size=(30, 30))
        self.config_img = ctk.CTkImage(Image.open("settings_1.png"), size=(40, 40))
        self.alt_hold_active_img = ctk.CTkImage(Image.open("AltHold_active.png"), size=(40, 40))
        self.alt_hold_passive_img = ctk.CTkImage(Image.open("AltHold_passive.png"), size=(40, 40))
        self.pos_hold_active_img = ctk.CTkImage(Image.open("PositionHold_active.png"), size=(40, 40))
        self.pos_hold_passive_img = ctk.CTkImage(Image.open("PositionHold_passive.png"), size=(40, 40))
        self.blackbox_active_img = ctk.CTkImage(Image.open("blackbox_active.png"), size=(40, 40))
        self.blackbox_passive_img = ctk.CTkImage(Image.open("blackbox_passive.png"), size=(40, 40))
        self.center_map_img = ctk.CTkImage(Image.open("focus.png"), size=(20, 20))
        self.map_follow_drone_img = ctk.CTkImage(Image.open("follow_drone.png"), size=(20, 20))
        self.waypoint_active_img = ctk.CTkImage(Image.open("waypoint_active.png"), size=(40, 40))
        self.waypoint_passive_img = ctk.CTkImage(Image.open("waypoint_passive.png"), size=(40, 40))
        self.request_wp_img = ctk.CTkImage(Image.open("read_wp_icon_.png"), size=(20, 20))

        self.drone_0_deg_img = ImageTk.PhotoImage(Image.open("drone_icon_0_deg.png").resize((45, 45)))
        self.drone_45_deg_img = ImageTk.PhotoImage(Image.open("drone_icon_45_deg.png").resize((45, 45)))
        self.drone_90_deg_img = ImageTk.PhotoImage(Image.open("drone_icon_90_deg.png").resize((45, 45)))
        self.drone_135_deg_img = ImageTk.PhotoImage(Image.open("drone_icon_135_deg.png").resize((45, 45)))
        self.drone_180_deg_img = ImageTk.PhotoImage(Image.open("drone_icon_180_deg.png").resize((45, 45)))
        self.drone_225_deg_img = ImageTk.PhotoImage(Image.open("drone_icon_225_deg.png").resize((45, 45)))
        self.drone_270_deg_img = ImageTk.PhotoImage(Image.open("drone_icon_270_deg.png").resize((45, 45)))
        self.drone_315_deg_img = ImageTk.PhotoImage(Image.open("drone_icon_315_deg.png").resize((45, 45)))
        self.location_img = ImageTk.PhotoImage(Image.open("location_icon.png").resize((40, 40)))
        self.drone_origin_img = ImageTk.PhotoImage(Image.open("drone_origin.png").resize((45, 45)))
        self.target_location_img = ImageTk.PhotoImage(Image.open("target_location_icon.png").resize((35, 35)))

        # MAP FRAME
        self.map_frame = ctk.CTkFrame(master=self.root, width=1600, height=830,
                                      corner_radius=10)
        self.map_frame.place(relx=0.422, rely=0.488, anchor=tkinter.CENTER)

        script_directory = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(script_directory, "offline_map_tiles.db")

        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, width=1600, height=830, corner_radius=10,
                                                        use_database_only=True, database_path=database_path)

        self.map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.map_widget.set_position(39.110946, 27.187785)
        self.map_widget.set_zoom(17)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        self.map_widget.add_right_click_menu_command(label="Add WP",
                                                     command=self.add_waypoint_event,
                                                     pass_coords=True)

        self.map_widget.add_right_click_menu_command(label="",
                                                     command=dummy_func,
                                                     pass_coords=False)

        self.map_widget.add_right_click_menu_command(label="Add WP to Home",
                                                     command=self.add_waypoint_to_home_event,
                                                     pass_coords=False)

        self.map_widget.add_right_click_menu_command(label="",
                                                     command=dummy_func,
                                                     pass_coords=False)

        self.map_widget.add_right_click_menu_command(label="Redraw WP",
                                                     command=self.redraw_waypoint_markers,
                                                     pass_coords=False)

        self.map_widget.add_right_click_menu_command(label="",
                                                     command=dummy_func,
                                                     pass_coords=False)

        self.map_widget.add_right_click_menu_command(label="Delete WP",
                                                     command=self.delete_waypoint_event,
                                                     pass_coords=True)

        self.map_widget.add_right_click_menu_command(label="",
                                                     command=dummy_func,
                                                     pass_coords=False)

        self.map_widget.add_right_click_menu_command(label="Delete All WP's",
                                                     command=self.delete_all_waypoints_event,
                                                     pass_coords=False)

        self.map_widget.add_right_click_menu_command(label="",
                                                     command=dummy_func,
                                                     pass_coords=False)

        self.map_widget.add_right_click_menu_command(label="Send WP Mission",
                                                     command=write_waypoints,
                                                     pass_coords=False)

        self.waypoint_path = self.map_widget.set_path([(0, 0), (0, 0)])

        self.drone_location_marker = self.map_widget.set_marker(0, 0, text="0.0m", text_color="gray1",
                                                                icon=self.drone_0_deg_img,
                                                                font=("Arial", 20, "bold"))

        self.drone_origin_marker = self.map_widget.set_marker(0, 0, text="", text_color="gray1",
                                                              icon=self.drone_origin_img,
                                                              font=("Arial", 20, "bold"))
        self.target_location_marker = self.map_widget.set_marker(0, 0, text="", text_color="gray1",
                                                                 icon=self.target_location_img, icon_anchor="center",
                                                                 font=("Arial", 20, "bold"))

        self.center_map_button = ctk.CTkButton(master=self.map_frame, width=20, height=20, corner_radius=0,
                                               fg_color="white", text="",
                                               image=self.center_map_img,
                                               command=self.center_map)
        self.center_map_button.place(relx=0.98, rely=0.97, anchor=tkinter.CENTER)

        self.map_follow_drone_button = ctk.CTkButton(master=self.map_frame, width=20, height=20, corner_radius=0,
                                                     fg_color="white", text="",
                                                     image=self.map_follow_drone_img,
                                                     command=self.map_follow_drone_func)
        self.map_follow_drone_button.place(relx=0.96, rely=0.97, anchor=tkinter.CENTER)

        self.map_request_wp_button = ctk.CTkButton(master=self.map_frame, width=20, height=20, corner_radius=0,
                                                   fg_color="white", text="",
                                                   image=self.request_wp_img, command=read_waypoints)
        self.map_request_wp_button.place(relx=0.94, rely=0.97, anchor=tkinter.CENTER)

        self.close_button = ctk.CTkButton(master=self.root, width=30, height=30, corner_radius=0,
                                          fg_color="transparent", text="",
                                          image=self.close_img,
                                          command=self.close_application)
        self.close_button.place(relx=0.828, rely=0.03, anchor=tkinter.CENTER)

        # UTILITY FRAME /*******************************************************************************/
        self.arm_utility_frame = ctk.CTkFrame(master=self.root, width=600, height=95,
                                              corner_radius=10)
        self.arm_utility_frame.place(relx=0.162, rely=0.053, anchor=tkinter.CENTER)

        self.config_button = ctk.CTkButton(master=self.arm_utility_frame, width=40, height=40, corner_radius=0,
                                           command=show_config_window, image=self.config_img, text="",
                                           fg_color="transparent", state="enabled")
        self.config_button.place(relx=0.07, rely=0.5, anchor=tkinter.CENTER)

        self.blackbox_button = ctk.CTkButton(master=self.arm_utility_frame, width=40, height=40, corner_radius=5,
                                             command=self.blackbox, text="", state="enabled", fg_color="transparent",
                                             image=self.blackbox_passive_img)

        self.blackbox_button.place(relx=0.18, rely=0.5, anchor=tkinter.CENTER)

        self.blackbox_auto_record_button = ctk.CTkButton(master=self.arm_utility_frame, width=10, height=40,
                                                         corner_radius=5,
                                                         command=self.auto_blackbox, text="", state="enabled",
                                                         fg_color="green")

        self.blackbox_auto_record_button.place(relx=0.23, rely=0.5, anchor=tkinter.CENTER)

        self.alt_hold_button = ctk.CTkButton(master=self.arm_utility_frame, width=40, height=40, corner_radius=5,
                                             text="", state="enabled", fg_color="transparent",
                                             image=self.alt_hold_passive_img)

        self.alt_hold_button.place(relx=0.32, rely=0.5, anchor=tkinter.CENTER)

        self.pos_hold_button = ctk.CTkButton(master=self.arm_utility_frame, width=40, height=40, corner_radius=5,
                                             text="", state="enabled", fg_color="transparent",
                                             image=self.pos_hold_passive_img)

        self.pos_hold_button.place(relx=0.42, rely=0.5, anchor=tkinter.CENTER)

        self.waypoint_button = ctk.CTkButton(master=self.arm_utility_frame, width=40, height=40, corner_radius=5,
                                             text="", state="enabled", fg_color="transparent",
                                             image=self.waypoint_passive_img)

        self.waypoint_button.place(relx=0.52, rely=0.5, anchor=tkinter.CENTER)

        self.save_button = ctk.CTkButton(master=self.arm_utility_frame, width=45, height=40, corner_radius=5,
                                         text="Save", state="enabled", command=self.save_on_click, font=("Arial", 14, "bold"))

        self.save_button.place(relx=0.62, rely=0.5, anchor=tkinter.CENTER)

        self.calibrate_mag_button = ctk.CTkButton(master=self.arm_utility_frame, width=65, height=40, corner_radius=5,
                                                  text="Start Mag Cal", state="enabled",
                                                  command=self.calibrate_mag_event, font=("Arial", 14, "bold"))

        self.calibrate_mag_button.place(relx=0.76, rely=0.5, anchor=tkinter.CENTER)

        self.wp_altitude_input = ctk.CTkEntry(master=self.arm_utility_frame, width=60, height=40, corner_radius=5,
                                              placeholder_text="WP Alt")

        self.wp_altitude_input.place(relx=0.92, rely=0.5, anchor=tkinter.CENTER)

        # DATA FRAME  /*********************************************************************************/
        self.data_frame = ctk.CTkFrame(master=self.root, width=290, height=1060,
                                       corner_radius=10)
        self.data_frame.place(relx=0.93, rely=0.5, anchor=tkinter.CENTER)

        # DATA FRAME 1  ///////////////////////////////////////////////////////////////////////////////////
        self.imu_frame = ctk.CTkFrame(master=self.data_frame, width=270, height=180, corner_radius=10)
        self.imu_frame.place(relx=0.5, rely=0.095, anchor=tkinter.CENTER)

        self.gyroscope_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                            corner_radius=10, fg_color="gray35",
                                            text="Gyroscope (dps)",
                                            font=("Arial", 16, "bold"))
        self.gyroscope_label.place(relx=0.5, rely=0.12, anchor=tkinter.CENTER)

        self.gyro_x_data_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                              corner_radius=10,
                                              text="X: 100.0",
                                              font=("Arial", 16, "bold"))
        self.gyro_x_data_label.place(relx=0.2, rely=0.3, anchor=tkinter.CENTER)

        self.gyro_y_data_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                              corner_radius=10,
                                              text="Y: 100.0",
                                              font=("Arial", 16, "bold"))
        self.gyro_y_data_label.place(relx=0.50, rely=0.3, anchor=tkinter.CENTER)

        self.gyro_z_data_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                              corner_radius=10,
                                              text="Z: 100.0",
                                              font=("Arial", 16, "bold"))
        self.gyro_z_data_label.place(relx=0.8, rely=0.3, anchor=tkinter.CENTER)

        self.accelerometer_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                                corner_radius=10, fg_color="gray35",
                                                text="Accelerometer (m/s²)",
                                                font=("Arial", 16, "bold"))
        self.accelerometer_label.place(relx=0.5, rely=0.52, anchor=tkinter.CENTER)

        self.accel_x_data_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="X: 100.0",
                                               font=("Arial", 16, "bold"))
        self.accel_x_data_label.place(relx=0.2, rely=0.7, anchor=tkinter.CENTER)

        self.accel_y_data_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="Y: 100.0",
                                               font=("Arial", 16, "bold"))
        self.accel_y_data_label.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.accel_z_data_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="Z: 100.0",
                                               font=("Arial", 16, "bold"))
        self.accel_z_data_label.place(relx=0.8, rely=0.7, anchor=tkinter.CENTER)

        self.imu_core_temp_label = ctk.CTkLabel(master=self.imu_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="IMU core temp: 25.5 °C",
                                                font=("Arial", 16, "bold"))
        self.imu_core_temp_label.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        # DATA FRAME 2  ////////////////////////////////////////////////////////////////////////////////////////
        self.magnetometer_frame = ctk.CTkFrame(master=self.data_frame, width=270, height=80, corner_radius=10)
        self.magnetometer_frame.place(relx=0.5, rely=0.23, anchor=tkinter.CENTER)

        self.magnetometer_label = ctk.CTkLabel(master=self.magnetometer_frame, width=100, height=25,
                                               corner_radius=10, fg_color="gray35",
                                               text="Magnetometer",
                                               font=("Arial", 16, "bold"))
        self.magnetometer_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.mag_x_data_label = ctk.CTkLabel(master=self.magnetometer_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="X: 100.0",
                                             font=("Arial", 16, "bold"))
        self.mag_x_data_label.place(relx=0.2, rely=0.70, anchor=tkinter.CENTER)

        self.mag_y_data_label = ctk.CTkLabel(master=self.magnetometer_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="Y: 100.0",
                                             font=("Arial", 16, "bold"))
        self.mag_y_data_label.place(relx=0.5, rely=0.70, anchor=tkinter.CENTER)

        self.mag_z_data_label = ctk.CTkLabel(master=self.magnetometer_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="Z: 100.0",
                                             font=("Arial", 16, "bold"))
        self.mag_z_data_label.place(relx=0.8, rely=0.70, anchor=tkinter.CENTER)

        # DATA FRAME 3  /////////////////////////////////////////////////////////////////////////////////////
        self.barometer_frame = ctk.CTkFrame(master=self.data_frame, width=270, height=130, corner_radius=10)
        self.barometer_frame.place(relx=0.5, rely=0.34, anchor=tkinter.CENTER)

        self.barometer_label = ctk.CTkLabel(master=self.barometer_frame, width=100, height=25,
                                            corner_radius=10, fg_color="gray35",
                                            text="Barometer",
                                            font=("Arial", 16, "bold"))
        self.barometer_label.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.pressure_data_label = ctk.CTkLabel(master=self.barometer_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="Pressure:             1010.5 hPa",
                                                font=("Arial", 16, "bold"))
        self.pressure_data_label.place(relx=0.5, rely=0.38, anchor=tkinter.CENTER)

        self.temp_data_label = ctk.CTkLabel(master=self.barometer_frame, width=100, height=25,
                                            corner_radius=10,
                                            text="Temperature:       25.5 °C",
                                            font=("Arial", 16, "bold"))
        self.temp_data_label.place(relx=0.45, rely=0.61, anchor=tkinter.CENTER)

        self.altitude_data_label = ctk.CTkLabel(master=self.barometer_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="Altitude:                 1.5 m",
                                                font=("Arial", 16, "bold"))
        self.altitude_data_label.place(relx=0.43, rely=0.84, anchor=tkinter.CENTER)

        # DATA FRAME 4 ////////////////////////////////////////////////////////////////////////////////////////
        self.tof_frame = ctk.CTkFrame(master=self.data_frame, width=270, height=100, corner_radius=10)
        self.tof_frame.place(relx=0.5, rely=0.46, anchor=tkinter.CENTER)

        self.tof_label = ctk.CTkLabel(master=self.tof_frame, width=100, height=25,
                                      corner_radius=10, fg_color="gray35",
                                      text="Range Finder (cm)",
                                      font=("Arial", 16, "bold"))
        self.tof_label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.tof_1_data_label = ctk.CTkLabel(master=self.tof_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="Range 1: 120.0",
                                             font=("Arial", 16, "bold"))
        self.tof_1_data_label.place(relx=0.5, rely=0.52, anchor=tkinter.CENTER)

        self.tof_2_data_label = ctk.CTkLabel(master=self.tof_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="Range 2: 120.0",
                                             font=("Arial", 16, "bold"))
        self.tof_2_data_label.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        # DATA FRAME 5 ////////////////////////////////////////////////////////////////////////////////
        self.flow_frame = ctk.CTkFrame(master=self.data_frame, width=270, height=120, corner_radius=10)
        self.flow_frame.place(relx=0.5, rely=0.575, anchor=tkinter.CENTER)

        self.flow_label = ctk.CTkLabel(master=self.flow_frame, width=100, height=25,
                                       corner_radius=10, fg_color="gray35",
                                       text="Flow (cm/s)",
                                       font=("Arial", 16, "bold"))
        self.flow_label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.flow_x_vel_data_label = ctk.CTkLabel(master=self.flow_frame, width=100, height=25,
                                                  corner_radius=10,
                                                  text="X: 0.00",
                                                  font=("Arial", 16, "bold"))
        self.flow_x_vel_data_label.place(relx=0.3, rely=0.52, anchor=tkinter.CENTER)

        self.flow_y_vel_data_label = ctk.CTkLabel(master=self.flow_frame, width=100, height=25,
                                                  corner_radius=10,
                                                  text="Y: 0.00",
                                                  font=("Arial", 16, "bold"))
        self.flow_y_vel_data_label.place(relx=0.7, rely=0.52, anchor=tkinter.CENTER)

        self.flow_quality_data_label = ctk.CTkLabel(master=self.flow_frame, width=100, height=25,
                                                    corner_radius=10,
                                                    text="Quality: 100",
                                                    font=("Arial", 16, "bold"))
        self.flow_quality_data_label.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
        # DATA FRAME 6 ////////////////////////////////////////////////////////////////////////////////
        self.gps_frame = ctk.CTkFrame(master=self.data_frame, width=270, height=365, corner_radius=10)
        self.gps_frame.place(relx=0.5, rely=0.816, anchor=tkinter.CENTER)

        self.gps_label = ctk.CTkLabel(master=self.gps_frame, width=80, height=25,
                                      corner_radius=10, fg_color="gray35",
                                      text="GNSS",
                                      font=("Arial", 16, "bold"))
        self.gps_label.place(relx=0.5, rely=0.07, anchor=tkinter.CENTER)

        self.latitude_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="Latitude:     00.0000000",
                                                font=("Arial", 16, "bold"))
        self.latitude_data_label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        self.longitude_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                 corner_radius=10,
                                                 text="Longitude:    00.0000000",
                                                 font=("Arial", 16, "bold"))
        self.longitude_data_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.latitude_origin_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                       corner_radius=10,
                                                       text="H.Latitude:     00.0000000",
                                                       font=("Arial", 16, "bold"))
        self.latitude_origin_data_label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.longitude_origin_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                        corner_radius=10,
                                                        text="H.Longitude:    00.0000000",
                                                        font=("Arial", 16, "bold"))
        self.longitude_origin_data_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.north_vel_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                 corner_radius=10,
                                                 text="Vel N: 0",
                                                 font=("Arial", 16, "bold"))
        self.north_vel_data_label.place(relx=0.18, rely=0.6, anchor=tkinter.CENTER)

        self.east_vel_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="E: 0",
                                                font=("Arial", 16, "bold"))
        self.east_vel_data_label.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.down_vel_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="D: 0",
                                                font=("Arial", 16, "bold"))
        self.down_vel_data_label.place(relx=0.82, rely=0.6, anchor=tkinter.CENTER)

        self.gps_alt_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="Altitude: 0",
                                               font=("Arial", 16, "bold"))
        self.gps_alt_data_label.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

        self.head_motion_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                   corner_radius=10,
                                                   text="HoM: 0",
                                                   font=("Arial", 16, "bold"))
        self.head_motion_data_label.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

        self.gps_fix_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="Fix: 0",
                                               font=("Arial", 16, "bold"))
        self.gps_fix_data_label.place(relx=0.3, rely=0.8, anchor=tkinter.CENTER)

        self.gps_sat_count_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                                     corner_radius=10,
                                                     text="Sats: 0",
                                                     font=("Arial", 16, "bold"))
        self.gps_sat_count_data_label.place(relx=0.7, rely=0.8, anchor=tkinter.CENTER)

        self.hdop_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                            corner_radius=10,
                                            text="HDoP: 0",
                                            font=("Arial", 16, "bold"))
        self.hdop_data_label.place(relx=0.3, rely=0.9, anchor=tkinter.CENTER)

        self.vdop_data_label = ctk.CTkLabel(master=self.gps_frame, width=100, height=25,
                                            corner_radius=10,
                                            text="VDoP: 0",
                                            font=("Arial", 16, "bold"))
        self.vdop_data_label.place(relx=0.7, rely=0.9, anchor=tkinter.CENTER)

        # Bottom Frame  /******************************************************************************/
        self.bottom_frame = ctk.CTkFrame(master=self.root, width=1600, height=120,
                                         corner_radius=10)
        self.bottom_frame.place(relx=0.422, rely=0.935, anchor=tkinter.CENTER)

        # Utility Frame 1 //////////////////////////////////////////////////////////////////////////////
        self.utility_1_frame = ctk.CTkFrame(master=self.bottom_frame, width=180, height=100,
                                            corner_radius=10)
        self.utility_1_frame.place(relx=0.062, rely=0.5, anchor=tkinter.CENTER)

        self.battery_volt_label = ctk.CTkLabel(master=self.utility_1_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="Battery: 4.2V",
                                               font=("Arial", 18, "bold"))
        self.battery_volt_label.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        self.conn_quality_label = ctk.CTkLabel(master=self.utility_1_frame, width=100, height=25,
                                               corner_radius=10,
                                               text="Connection:\n100.0%",
                                               font=("Arial", 18, "bold"))
        self.conn_quality_label.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

        # Utility Frame 2 //////////////////////////////////////////////////////////////////////////////
        self.utility_2_frame = ctk.CTkFrame(master=self.bottom_frame, width=400, height=100,
                                            corner_radius=10)
        self.utility_2_frame.place(relx=0.25, rely=0.5, anchor=tkinter.CENTER)

        self.attitude_pitch_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                                 corner_radius=10,
                                                 text="Att  θ: 12.21",
                                                 font=("Arial", 18, "bold"))
        self.attitude_pitch_label.place(relx=0.2, rely=0.24, anchor=tkinter.CENTER)

        self.attitude_roll_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                                corner_radius=10,
                                                text="φ: -12.61",
                                                font=("Arial", 18, "bold"))
        self.attitude_roll_label.place(relx=0.5, rely=0.24, anchor=tkinter.CENTER)

        self.attitude_heading_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                                   corner_radius=10,
                                                   text="ψ: 112.60",
                                                   font=("Arial", 18, "bold"))
        self.attitude_heading_label.place(relx=0.8, rely=0.24, anchor=tkinter.CENTER)

        self.target_attitude_pitch_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                                        corner_radius=10,
                                                        text="T.Att  θ: 12.21",
                                                        font=("Arial", 18, "bold"))
        self.target_attitude_pitch_label.place(relx=0.18, rely=0.55, anchor=tkinter.CENTER)

        self.target_attitude_roll_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                                       corner_radius=10,
                                                       text="φ: -12.61",
                                                       font=("Arial", 18, "bold"))
        self.target_attitude_roll_label.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        self.target_attitude_heading_label = ctk.CTkLabel(master=self.utility_2_frame, width=100, height=25,
                                                          corner_radius=10,
                                                          text="ψ: 112.60",
                                                          font=("Arial", 18, "bold"))
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
                                                      font=("Arial", 18, "bold"))
        self.calibrated_altitude_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.target_altitude_label = ctk.CTkLabel(master=self.utility_3_frame, width=100, height=25,
                                                  corner_radius=10,
                                                  text="T.Alt: 10.85 m",
                                                  font=("Arial", 18, "bold"))
        self.target_altitude_label.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        # Utility Frame 4 //////////////////////////////////////////////////////////////////////////////
        self.utility_4_frame = ctk.CTkFrame(master=self.bottom_frame, width=340, height=100,
                                            corner_radius=10)
        self.utility_4_frame.place(relx=0.607, rely=0.5, anchor=tkinter.CENTER)

        self.velocity_x_label = ctk.CTkLabel(master=self.utility_4_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="Vel X: 0.6",
                                             font=("Arial", 18, "bold"))
        self.velocity_x_label.place(relx=0.2, rely=0.3, anchor=tkinter.CENTER)

        self.velocity_y_label = ctk.CTkLabel(master=self.utility_4_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="Y: 0.2",
                                             font=("Arial", 18, "bold"))
        self.velocity_y_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.velocity_z_label = ctk.CTkLabel(master=self.utility_4_frame, width=100, height=25,
                                             corner_radius=10,
                                             text="Z: 0.8",
                                             font=("Arial", 18, "bold"))
        self.velocity_z_label.place(relx=0.8, rely=0.3, anchor=tkinter.CENTER)

        self.target_velocity_x_label = ctk.CTkLabel(master=self.utility_4_frame, width=100, height=25,
                                                    corner_radius=10,
                                                    text="T.Vel X: 0.7",
                                                    font=("Arial", 18, "bold"))
        self.target_velocity_x_label.place(relx=0.18, rely=0.7, anchor=tkinter.CENTER)

        self.target_velocity_y_label = ctk.CTkLabel(master=self.utility_4_frame, width=100, height=25,
                                                    corner_radius=10,
                                                    text="Y: 0.1",
                                                    font=("Arial", 18, "bold"))
        self.target_velocity_y_label.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.target_velocity_z_label = ctk.CTkLabel(master=self.utility_4_frame, width=100, height=25,
                                                    corner_radius=10,
                                                    text="Z: -0.1",
                                                    font=("Arial", 18, "bold"))
        self.target_velocity_z_label.place(relx=0.8, rely=0.7, anchor=tkinter.CENTER)

        # Utility Frame 5 //////////////////////////////////////////////////////////////////////////////

        self.utility_5_frame = ctk.CTkFrame(master=self.bottom_frame, width=440, height=100,
                                            corner_radius=10)
        self.utility_5_frame.place(relx=0.857, rely=0.5, anchor=tkinter.CENTER)

        self.target_latitude_label = ctk.CTkLabel(master=self.utility_5_frame, width=100, height=25,
                                                  corner_radius=10,
                                                  text="T.Lat:  00.0000000",
                                                  font=("Arial", 18, "bold"))
        self.target_latitude_label.place(relx=0.25, rely=0.3, anchor=tkinter.CENTER)

        self.target_longitude_label = ctk.CTkLabel(master=self.utility_5_frame, width=100, height=25,
                                                   corner_radius=10,
                                                   text="T.Lon:  00.0000000",
                                                   font=("Arial", 18, "bold"))
        self.target_longitude_label.place(relx=0.75, rely=0.3, anchor=tkinter.CENTER)

        self.dist_to_target_2d_label = ctk.CTkLabel(master=self.utility_5_frame, width=100, height=25,
                                                    corner_radius=10,
                                                    text="D2D: 10.0",
                                                    font=("Arial", 18, "bold"))
        self.dist_to_target_2d_label.place(relx=0.2, rely=0.7, anchor=tkinter.CENTER)

        self.dist_to_target_3d_label = ctk.CTkLabel(master=self.utility_5_frame, width=100, height=25,
                                                    corner_radius=10,
                                                    text="D3D: 10.0",
                                                    font=("Arial", 18, "bold"))
        self.dist_to_target_3d_label.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.vel_2d_label = ctk.CTkLabel(master=self.utility_5_frame, width=100, height=25,
                                         corner_radius=10,
                                         text="V2D: 1.0",
                                         font=("Arial", 18, "bold"))
        self.vel_2d_label.place(relx=0.8, rely=0.7, anchor=tkinter.CENTER)

    def update_ui(self):
        self.root.mainloop()

    def update_telemetry_ui(self):

        if telemetry_data_dict["battery_voltage"] >= 3.7 and self.battery_volt_label.cget("fg_color") != "darkgreen":
            self.battery_volt_label.configure(fg_color="darkgreen")
        elif telemetry_data_dict["battery_voltage"] < 3.7 and self.battery_volt_label.cget("fg_color") != "red4":
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

        self.tof_1_data_label.configure(text=f"Range 1:      {telemetry_data_dict['tof_distance_1']:.1f}")
        self.tof_2_data_label.configure(text=f"Range 2:      {telemetry_data_dict['tof_distance_2']:.1f}")

        self.battery_volt_label.configure(text=f"Battery: {telemetry_data_dict['battery_voltage']:.1f} V")
        self.conn_quality_label.configure(text=f"Connection:\n{telemetry_data_dict['packet_delivery']}%")

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

        self.calibrated_altitude_label.configure(
            text=f"Alt: {telemetry_data_dict['altitude_calibrated']:.1f} m")
        self.target_altitude_label.configure(text=f"T.Alt: {telemetry_data_dict['target_altitude']:.1f} m")

        self.velocity_x_label.configure(text=f"Vel X: {telemetry_data_dict['velocity_x_ms']:.1f}")
        self.velocity_y_label.configure(text=f"Y: {telemetry_data_dict['velocity_y_ms']:.1f}")
        self.velocity_z_label.configure(text=f"Z: {telemetry_data_dict['velocity_z_ms']:.1f}")

        self.target_velocity_x_label.configure(text=f"T.Vel X: {telemetry_data_dict['target_velocity_x_ms']:.1f}")
        self.target_velocity_y_label.configure(text=f"Y: {telemetry_data_dict['target_velocity_y_ms']:.1f}")
        self.target_velocity_z_label.configure(text=f"Z: {telemetry_data_dict['target_velocity_z_ms']:.1f}")

        self.flow_x_vel_data_label.configure(text=f"X: {telemetry_data_dict['flow_x_velocity']:.1f}")
        self.flow_y_vel_data_label.configure(text=f"Y: {telemetry_data_dict['flow_y_velocity']:.1f}")
        self.flow_quality_data_label.configure(text=f"Quality: {telemetry_data_dict['flow_quality']:.0f}%")

        self.drone_location_marker.set_text(f"{telemetry_data_dict['altitude_calibrated']:.1f}m")

        if 22.5 <= telemetry_data_dict["heading"] < 67.5:
            self.drone_location_marker.change_icon(self.drone_45_deg_img)
        elif 67.5 <= telemetry_data_dict["heading"] < 112.5:
            self.drone_location_marker.change_icon(self.drone_90_deg_img)
        elif 112.5 <= telemetry_data_dict["heading"] < 157.5:
            self.drone_location_marker.change_icon(self.drone_135_deg_img)
        elif 157.5 <= telemetry_data_dict["heading"] < 202.5:
            self.drone_location_marker.change_icon(self.drone_180_deg_img)
        elif 202.5 <= telemetry_data_dict["heading"] < 247.5:
            self.drone_location_marker.change_icon(self.drone_225_deg_img)
        elif 247.5 <= telemetry_data_dict["heading"] < 292.5:
            self.drone_location_marker.change_icon(self.drone_270_deg_img)
        elif 292.5 <= telemetry_data_dict["heading"] < 337.5:
            self.drone_location_marker.change_icon(self.drone_315_deg_img)
        else:
            self.drone_location_marker.change_icon(self.drone_0_deg_img)

        self.drone_location_marker.set_position(telemetry_data_dict["gps_latitude"],
                                                telemetry_data_dict["gps_longitude"])
        if self.map_follow_drone:
            self.map_widget.set_position(telemetry_data_dict["gps_latitude"],
                                         telemetry_data_dict["gps_longitude"])

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
            else:
                if serial_backend.blackbox_state and self.bb_auto_record:
                    self.blackbox()
                self.arm_utility_frame.configure(fg_color="gray13")
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

        self.target_location_marker.set_position(telemetry_data_dict["target_latitude"],
                                                 telemetry_data_dict["target_longitude"])

    def add_waypoint_event(self, coords):
        global waypoint_counter, waypoint_altitude

        if len(waypoint_coordinates) < 25:

            if self.wp_altitude_input.get() != "":
                alt = int(float(self.wp_altitude_input.get()) * 10)
                if 0 <= alt <= 255:
                    waypoint_altitude = alt

            waypoint_coordinates.append((coords[0], coords[1]))
            waypoint_only_altitudes.append(np.uint8(waypoint_altitude))
            waypoint_markers.append(
                self.map_widget.set_marker(coords[0], coords[1], icon=self.location_img, icon_anchor="s",
                                           text=f"{waypoint_counter + 1}|{waypoint_altitude / 10}",
                                           text_color="white", font=("Arial", 25, "bold")))
            waypoint_counter += 1
            if waypoint_counter > 1:
                self.waypoint_path.set_position_list(waypoint_coordinates)
        else:
            print("wp >= 25")

    def add_waypoint_to_home_event(self):
        global waypoint_counter, waypoint_altitude, telemetry_data_dict

        if len(waypoint_coordinates) < 25 and telemetry_data_dict["gps_latitude_origin"] != 0 and telemetry_data_dict[
            "gps_longitude_origin"] != 0:

            if self.wp_altitude_input.get() != "":
                alt = int(float(self.wp_altitude_input.get()) * 10)
                if 0 <= alt <= 255:
                    waypoint_altitude = alt

            waypoint_coordinates.append(
                (telemetry_data_dict["gps_latitude_origin"], telemetry_data_dict["gps_longitude_origin"]))
            waypoint_only_altitudes.append(np.uint8(waypoint_altitude))
            waypoint_markers.append(
                self.map_widget.set_marker(telemetry_data_dict["gps_latitude_origin"],
                                           telemetry_data_dict["gps_longitude_origin"], icon=self.location_img,
                                           icon_anchor="s",
                                           text=f"{waypoint_counter + 1}|{waypoint_altitude / 10}",
                                           text_color="white", font=("Arial", 25, "bold")))
            waypoint_counter += 1
            if waypoint_counter > 1:
                self.waypoint_path.set_position_list(waypoint_coordinates)
        else:
            print("WP home is zero or wp >= 25")

    def delete_all_waypoints_event(self):
        global waypoint_counter
        waypoint_coordinates.clear()
        waypoint_only_altitudes.clear()
        for item in waypoint_markers:
            item.delete()
        waypoint_counter = 0
        self.waypoint_path.set_position_list([(0.0, 0.0), (0.0, 0.0)])

    def delete_waypoint_event(self, coords):
        global waypoint_counter
        if len(waypoint_coordinates) == 1:
            self.delete_all_waypoints_event()
        else:
            index = find_nearest_coordinate(coords)
            del waypoint_coordinates[index]
            del waypoint_only_altitudes[index]
            waypoint_markers[index].delete()
            del waypoint_markers[index]
            self.redraw_waypoint_markers()

    def redraw_waypoint_markers(self):
        global waypoint_counter
        for index in waypoint_markers:
            index.delete()
        waypoint_markers.clear()
        for index, value in enumerate(waypoint_coordinates):
            waypoint_markers.append(
                self.map_widget.set_marker(value[0], value[1], icon=self.location_img, icon_anchor="s",
                                           text=f"{index + 1}|{waypoint_only_altitudes[index] / 10}",
                                           text_color="white",
                                           font=("Arial", 25, "bold")))
            waypoint_counter = index + 1

        if len(waypoint_coordinates) < 2:
            self.waypoint_path.set_position_list([(0.0, 0.0), (0.0, 0.0)])
        else:
            self.waypoint_path.set_position_list(waypoint_coordinates)

    def center_map(self):
        # This has to be 2 times to work
        self.map_widget.set_position(39.110946, 27.187785)
        self.map_widget.set_zoom(17)
        self.map_widget.set_position(39.110946, 27.187785)
        self.map_widget.set_zoom(17)

    def map_follow_drone_func(self):
        if self.map_follow_drone:
            self.map_follow_drone = False
            self.center_map_button.configure(state="enabled")
            self.map_follow_drone_button.configure(fg_color="white")
        else:
            self.map_follow_drone = True
            self.map_follow_drone_button.configure(fg_color="green")
            self.center_map_button.configure(state="disabled")

    def save_on_click(self):
        df = pd.DataFrame([telemetry_data_dict])
        df.to_csv(
            "C:/Users/erayd/OneDrive/Masaüstü/SAVE_ON_CLICK_FILE.csv",
            mode='a', index=False, header=False)

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
            serial_backend.blackbox_file_name = str(time_now.day) + "_" + str(time_now.month) + "_" + str(
                time_now.hour) + "_" + str(
                time_now.minute) + "_" + str(time_now.second) + ".csv"
            df = pd.DataFrame([telemetry_data_dict])
            df.to_csv(
                "C:/Users/erayd/OneDrive/Masaüstü/Project STARLING/flight_logs/" + serial_backend.blackbox_file_name,
                mode='a', index=False, header=True)
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
            if len(serial_backend.mag_x_raw) >= 5:
                mag_calibration.Magnetometer().run()
                show_mag_cal_data()
            else:
                print("Not enough data points gathered to perform calibration!!")

    def close_application(self):
        self.isAppAlive = False
        self.root.destroy()
        quit()


def find_nearest_coordinate(target_coord):
    if not waypoint_coordinates:
        return None  # Koordinat listesi boşsa None döndür

    # Başlangıçta en küçük mesafeyi sonsuz olarak ayarlayın
    min_distance = float('inf')
    nearest_index = None

    # Koordinat listesinde dolaşın ve en yakın koordinatı bulun
    for i, coord in enumerate(waypoint_coordinates):
        x, y = coord
        target_x, target_y = target_coord

        # Euclidean mesafesini hesapla
        distance = math.sqrt((x - target_x) ** 2 + (y - target_y) ** 2)

        # Eğer şu ana kadar hesaplanan en küçük mesafeden daha küçükse güncelle
        if distance < min_distance:
            min_distance = distance
            nearest_index = i

    return nearest_index


def write_waypoints():
    serial_backend.send_gamepad_data = False
    serial_backend.send_waypoints_data = True


def read_waypoints():
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
    textbox.insert("1.0", f"Length: {len(serial_backend.mag_x_raw)} | Resolution: {mag_calibration.mean_resolution:.0f}\n\n"
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
