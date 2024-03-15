from data_struct import *
import tkinter
from tkinter import messagebox, END
import serial_backend
import customtkinter as ctk


def show_config_window():
    def request_config():
        serial_backend.request_config_data = True
        serial_backend.send_config_data = False
        serial_backend.send_gamepad_data = False
        config_window.destroy()

    def get_entries():

        response = messagebox.askyesnocancel("Send New Config", "Are you sure?")

        is_error_found = False

        if response:

            # PID FRAME
            if pitch_p_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["pitch_p"] = float(pitch_p_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    pitch_p_gain_label.configure(text=pitch_p_gain_entry.get())
                    pitch_p_gain_entry.delete(0, END)

            if pitch_i_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["pitch_i"] = float(pitch_i_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    pitch_i_gain_label.configure(text=pitch_i_gain_entry.get())
                    pitch_i_gain_entry.delete(0, END)

            if pitch_d_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["pitch_d"] = float(pitch_d_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    pitch_d_gain_label.configure(text=pitch_d_gain_entry.get())
                    pitch_d_gain_entry.delete(0, END)

            if roll_p_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["roll_p"] = float(roll_p_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    roll_p_gain_label.configure(text=roll_p_gain_entry.get())
                    roll_p_gain_entry.delete(0, END)

            if roll_i_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["roll_i"] = float(roll_i_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    roll_i_gain_label.configure(text=roll_i_gain_entry.get())
                    roll_i_gain_entry.delete(0, END)

            if roll_d_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["roll_d"] = float(roll_d_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    roll_d_gain_label.configure(text=roll_d_gain_entry.get())
                    roll_d_gain_entry.delete(0, END)

            if yaw_p_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["yaw_p"] = float(yaw_p_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    yaw_p_gain_label.configure(text=yaw_p_gain_entry.get())
                    yaw_p_gain_entry.delete(0, END)

            if yaw_i_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["yaw_i"] = float(yaw_i_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    yaw_i_gain_label.configure(text=yaw_i_gain_entry.get())
                    yaw_i_gain_entry.delete(0, END)

            if pos_p_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["position_p"] = float(pos_p_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    pos_p_gain_label.configure(text=pos_p_gain_entry.get())
                    pos_p_gain_entry.delete(0, END)

            if pos_i_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["position_i"] = float(pos_i_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    pos_i_gain_label.configure(text=pos_i_gain_entry.get())
                    pos_i_gain_entry.delete(0, END)

            if ff_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["ff_gain"] = float(ff_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    ff_gain_label.configure(text=ff_gain_entry.get())
                    ff_gain_entry.delete(0, END)

            if alt_p_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["altitude_p"] = float(alt_p_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    alt_p_gain_label.configure(text=alt_p_gain_entry.get())
                    alt_p_gain_entry.delete(0, END)

            if alt_i_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["altitude_i"] = float(alt_i_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    alt_i_gain_label.configure(text=alt_i_gain_entry.get())
                    alt_i_gain_entry.delete(0, END)

            if alt_d_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["altitude_d"] = float(alt_d_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    alt_d_gain_label.configure(text=alt_d_gain_entry.get())
                    alt_d_gain_entry.delete(0, END)

            # FRAME 3
            if max_pitch_angle_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["max_pitch_angle"] = float(max_pitch_angle_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    max_pitch_angle_label.configure(text=max_pitch_angle_entry.get())
                    max_pitch_angle_entry.delete(0, END)

            if max_roll_angle_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["max_roll_angle"] = float(max_roll_angle_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    max_roll_angle_label.configure(text=max_roll_angle_entry.get())
                    max_roll_angle_entry.delete(0, END)

            if max_pitch_rate_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["max_pitch_rate"] = float(max_pitch_rate_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    max_pitch_rate_label.configure(text=max_pitch_rate_entry.get())
                    max_pitch_rate_entry.delete(0, END)

            if max_roll_rate_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["max_roll_rate"] = float(max_roll_rate_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    max_roll_rate_label.configure(text=max_roll_rate_entry.get())
                    max_roll_rate_entry.delete(0, END)

            if max_yaw_rate_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["max_yaw_rate"] = float(max_yaw_rate_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    max_yaw_rate_label.configure(text=max_yaw_rate_entry.get())
                    max_yaw_rate_entry.delete(0, END)

            if max_vert_vel_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["max_vertical_velocity"] = float(max_vert_vel_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    max_vert_vel_label.configure(text=max_vert_vel_entry.get())
                    max_vert_vel_entry.delete(0, END)

            if max_horiz_vel_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["max_horizontal_velocity"] = float(max_horiz_vel_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    max_horiz_vel_label.configure(text=max_horiz_vel_entry.get())
                    max_horiz_vel_entry.delete(0, END)

            if pitch_rate_scale_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["pitch_rate_scale"] = float(pitch_rate_scale_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    pitch_rate_scale_label.configure(text=pitch_rate_scale_entry.get())
                    pitch_rate_scale_entry.delete(0, END)

            if roll_rate_scale_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["roll_rate_scale"] = float(roll_rate_scale_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    roll_rate_scale_label.configure(text=roll_rate_scale_entry.get())
                    roll_rate_scale_entry.delete(0, END)

            if yaw_rate_scale_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["yaw_rate_scale"] = float(yaw_rate_scale_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    yaw_rate_scale_label.configure(text=yaw_rate_scale_entry.get())
                    yaw_rate_scale_entry.delete(0, END)

            if takeoff_altitude_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["takeoff_altitude"] = float(takeoff_altitude_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    takeoff_altitude_label.configure(text=takeoff_altitude_entry.get())
                    takeoff_altitude_entry.delete(0, END)

            if v_drop_compensation_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["v_drop_compensation_gain"] = float(v_drop_compensation_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    v_drop_compensation_gain_label.configure(text=v_drop_compensation_gain_entry.get())
                    v_drop_compensation_gain_entry.delete(0, END)

            if mag_declination_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["mag_declination_deg"] = float(mag_declination_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    mag_declination_label.configure(text=mag_declination_entry.get())
                    mag_declination_entry.delete(0, END)

            if v_sens_coeff_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["v_sens_gain"] = float(v_sens_coeff_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    v_sens_coeff_label.configure(text=v_sens_coeff_entry.get())
                    v_sens_coeff_entry.delete(0, END)

            if hover_thr_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["hover_throttle"] = float(hover_thr_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    hover_thr_label.configure(text=hover_thr_entry.get())
                    hover_thr_entry.delete(0, END)

            if notch_1_freq_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["notch_1_freq"] = float(notch_1_freq_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    notch_1_freq_label.configure(text=notch_1_freq_entry.get())
                    notch_1_freq_entry.delete(0, END)

            if notch_1_width_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["notch_1_bandwidth"] = float(notch_1_width_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    notch_1_width_label.configure(text=notch_1_width_entry.get())
                    notch_1_width_entry.delete(0, END)

            if ahrs_filter_beta_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["ahrs_filter_beta"] = float(ahrs_filter_beta_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    ahrs_filter_beta_label.configure(text=ahrs_filter_beta_entry.get())
                    ahrs_filter_beta_entry.delete(0, END)

            if ahrs_filter_zeta_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["ahrs_filter_zeta"] = float(ahrs_filter_zeta_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    ahrs_filter_zeta_label.configure(text=ahrs_filter_zeta_entry.get())
                    ahrs_filter_zeta_entry.delete(0, END)

            if altitude_filter_beta_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["alt_filter_beta"] = float(altitude_filter_beta_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    altitude_filter_beta_label.configure(text=altitude_filter_beta_entry.get())
                    altitude_filter_beta_entry.delete(0, END)

            if velz_filter_beta_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["velz_filter_beta"] = float(velz_filter_beta_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    velz_filter_beta_label.configure(text=velz_filter_beta_entry.get())
                    velz_filter_beta_entry.delete(0, END)

            if velz_filter_zeta_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["velz_filter_zeta"] = float(velz_filter_zeta_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    velz_filter_zeta_label.configure(text=velz_filter_zeta_entry.get())
                    velz_filter_zeta_entry.delete(0, END)

            if velxy_filter_beta_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["velxy_filter_beta"] = float(velxy_filter_beta_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    velxy_filter_beta_label.configure(text=velxy_filter_beta_entry.get())
                    velxy_filter_beta_entry.delete(0, END)

            if alt_to_vel_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["alt_to_vel_gain"] = float(alt_to_vel_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    alt_to_vel_gain_label.configure(text=alt_to_vel_gain_entry.get())
                    alt_to_vel_gain_entry.delete(0, END)

            if wp_threshold_cm_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["wp_threshold_cm"] = float(wp_threshold_cm_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    wp_threshold_cm_label.configure(text=wp_threshold_cm_entry.get())
                    wp_threshold_cm_entry.delete(0, END)

            if wp_heading_correct_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["wp_heading_correct_gain"] = float(wp_heading_correct_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    wp_heading_correct_gain_label.configure(text=wp_heading_correct_gain_entry.get())
                    wp_heading_correct_gain_entry.delete(0, END)

            if wp_dist_to_vel_gain_entry.get() != "" and not is_error_found:
                try:
                    config_data_dict["wp_dist_to_vel_gain"] = float(wp_dist_to_vel_gain_entry.get())
                except ValueError:
                    messagebox.showinfo("ValueError", "Entry is not a number!!")
                    is_error_found = True
                else:
                    wp_dist_to_vel_gain_label.configure(text=wp_dist_to_vel_gain_entry.get())
                    wp_dist_to_vel_gain_entry.delete(0, END)

            if not is_error_found:
                serial_backend.send_config_data = True
                serial_backend.send_gamepad_data = False

    # //////////////////////////////////////////////////////////////////////////////////////////
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    config_window = ctk.CTkToplevel()
    # config_window.iconbitmap("UAV_Project_LOGO_icon.ico")
    config_window.geometry("1220x800")
    config_window.title("Drone Configuration")
    config_window.grab_set()
    config_window.resizable(False, False)

    # MAIN FRAME
    main_frame = ctk.CTkFrame(master=config_window, width=1200, height=780, corner_radius=10)
    main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    write_config_button = ctk.CTkButton(master=main_frame, width=100, height=40, corner_radius=10, text="Write Config",
                                        font=("Arial", 18, "bold"), command=get_entries)
    write_config_button.place(relx=0.815, rely=0.96, anchor=tkinter.CENTER)

    read_config_button = ctk.CTkButton(master=main_frame, width=100, height=40, corner_radius=10, text="Read Config",
                                       font=("Arial", 18, "bold"), command=request_config)
    read_config_button.place(relx=0.935, rely=0.96, anchor=tkinter.CENTER)

    #  GENERAL SETTINGS FRAME
    frame1 = ctk.CTkFrame(master=main_frame, width=280, height=760, corner_radius=10)
    frame1.place(relx=0.125, rely=0.5, anchor=tkinter.CENTER)

    # GENERAL SETTINGS
    general_settings_label = ctk.CTkLabel(master=frame1, width=200, height=35, corner_radius=10,
                                          text="General Settings", font=("Arial", 22, "bold"))
    general_settings_label.place(relx=0.5, rely=0.03, anchor=tkinter.CENTER)

    max_pitch_angle_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                         placeholder_text="Max Pitch Angle")
    max_pitch_angle_entry.place(relx=0.74, rely=0.09, anchor=tkinter.CENTER)
    max_pitch_angle_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                         text=f"{config_data_dict['max_pitch_angle']:.2f}",
                                         font=("Arial", 18, "bold"))
    max_pitch_angle_label.place(relx=0.26, rely=0.09, anchor=tkinter.CENTER)

    max_roll_angle_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                        placeholder_text="Max Roll Angle")
    max_roll_angle_entry.place(relx=0.74, rely=0.15, anchor=tkinter.CENTER)
    max_roll_angle_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                        text=f"{config_data_dict['max_roll_angle']:.2f}",
                                        font=("Arial", 18, "bold"))
    max_roll_angle_label.place(relx=0.26, rely=0.15, anchor=tkinter.CENTER)

    max_pitch_rate_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                        placeholder_text="Max Pitch Rate")
    max_pitch_rate_entry.place(relx=0.74, rely=0.21, anchor=tkinter.CENTER)
    max_pitch_rate_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                        text=f"{config_data_dict['max_pitch_rate']:.2f}",
                                        font=("Arial", 18, "bold"))
    max_pitch_rate_label.place(relx=0.26, rely=0.21, anchor=tkinter.CENTER)

    max_roll_rate_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                       placeholder_text="Max Roll Rate")
    max_roll_rate_entry.place(relx=0.74, rely=0.27, anchor=tkinter.CENTER)
    max_roll_rate_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                       text=f"{config_data_dict['max_roll_rate']:.2f}",
                                       font=("Arial", 18, "bold"))
    max_roll_rate_label.place(relx=0.26, rely=0.27, anchor=tkinter.CENTER)

    max_yaw_rate_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                      placeholder_text="Max Yaw Rate")
    max_yaw_rate_entry.place(relx=0.74, rely=0.33, anchor=tkinter.CENTER)
    max_yaw_rate_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                      text=f"{config_data_dict['max_yaw_rate']:.2f}",
                                      font=("Arial", 18, "bold"))
    max_yaw_rate_label.place(relx=0.26, rely=0.33, anchor=tkinter.CENTER)

    max_vert_vel_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                      placeholder_text="Max Vert Vel")
    max_vert_vel_entry.place(relx=0.74, rely=0.39, anchor=tkinter.CENTER)
    max_vert_vel_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                      text=f"{config_data_dict['max_vertical_velocity']:.2f}",
                                      font=("Arial", 18, "bold"))
    max_vert_vel_label.place(relx=0.26, rely=0.39, anchor=tkinter.CENTER)

    max_horiz_vel_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                       placeholder_text="Max Horiz Vel")
    max_horiz_vel_entry.place(relx=0.74, rely=0.45, anchor=tkinter.CENTER)
    max_horiz_vel_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                       text=f"{config_data_dict['max_horizontal_velocity']:.2f}",
                                       font=("Arial", 18, "bold"))
    max_horiz_vel_label.place(relx=0.26, rely=0.45, anchor=tkinter.CENTER)

    pitch_rate_scale_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                          placeholder_text="Pitch Rate Scale")
    pitch_rate_scale_entry.place(relx=0.74, rely=0.51, anchor=tkinter.CENTER)
    pitch_rate_scale_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                          text=f"{config_data_dict['pitch_rate_scale']:.2f}",
                                          font=("Arial", 18, "bold"))
    pitch_rate_scale_label.place(relx=0.26, rely=0.51, anchor=tkinter.CENTER)

    roll_rate_scale_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                         placeholder_text="Roll Rate Scale")
    roll_rate_scale_entry.place(relx=0.74, rely=0.57, anchor=tkinter.CENTER)
    roll_rate_scale_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                         text=f"{config_data_dict['roll_rate_scale']:.2f}",
                                         font=("Arial", 18, "bold"))
    roll_rate_scale_label.place(relx=0.26, rely=0.57, anchor=tkinter.CENTER)

    yaw_rate_scale_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                        placeholder_text="Yaw Rate Scale")
    yaw_rate_scale_entry.place(relx=0.74, rely=0.63, anchor=tkinter.CENTER)
    yaw_rate_scale_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                        text=f"{config_data_dict['yaw_rate_scale']:.2f}",
                                        font=("Arial", 18, "bold"))
    yaw_rate_scale_label.place(relx=0.26, rely=0.63, anchor=tkinter.CENTER)

    takeoff_altitude_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                          placeholder_text="TakeOff Altitude")
    takeoff_altitude_entry.place(relx=0.74, rely=0.69, anchor=tkinter.CENTER)
    takeoff_altitude_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                          text=f"{config_data_dict['takeoff_altitude']:.2f}",
                                          font=("Arial", 18, "bold"))
    takeoff_altitude_label.place(relx=0.26, rely=0.69, anchor=tkinter.CENTER)

    v_sens_coeff_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                      placeholder_text="V Sens Gain")
    v_sens_coeff_entry.place(relx=0.74, rely=0.75, anchor=tkinter.CENTER)
    v_sens_coeff_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                      text=f"{config_data_dict['v_sens_gain']:.2f}",
                                      font=("Arial", 18, "bold"))
    v_sens_coeff_label.place(relx=0.26, rely=0.75, anchor=tkinter.CENTER)

    mag_declination_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                         placeholder_text="Mag Declination")
    mag_declination_entry.place(relx=0.74, rely=0.81, anchor=tkinter.CENTER)
    mag_declination_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                         text=f"{config_data_dict['mag_declination_deg']:.2f}",
                                         font=("Arial", 18, "bold"))
    mag_declination_label.place(relx=0.26, rely=0.81, anchor=tkinter.CENTER)

    v_drop_compensation_gain_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                                  placeholder_text="Batt Comp Gain")
    v_drop_compensation_gain_entry.place(relx=0.74, rely=0.87, anchor=tkinter.CENTER)
    v_drop_compensation_gain_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                                  text=f"{config_data_dict['v_drop_compensation_gain']:.2f}",
                                                  font=("Arial", 18, "bold"))
    v_drop_compensation_gain_label.place(relx=0.26, rely=0.87, anchor=tkinter.CENTER)

    hover_thr_entry = ctk.CTkEntry(master=frame1, width=120, height=35, corner_radius=10,
                                   placeholder_text="Hover Throttle")
    hover_thr_entry.place(relx=0.74, rely=0.93, anchor=tkinter.CENTER)
    hover_thr_label = ctk.CTkLabel(master=frame1, width=120, height=35, corner_radius=10,
                                   text=f"{config_data_dict['hover_throttle']:.2f}",
                                   font=("Arial", 18, "bold"))
    hover_thr_label.place(relx=0.26, rely=0.93, anchor=tkinter.CENTER)

    # PID FRAME
    frame3 = ctk.CTkFrame(master=main_frame, width=280, height=760, corner_radius=10)
    frame3.place(relx=0.375, rely=0.5, anchor=tkinter.CENTER)

    pid_parameters_label = ctk.CTkLabel(master=frame3, width=200, height=35, corner_radius=10,
                                        text="PID Parameters", font=("Arial", 22, "bold"))
    pid_parameters_label.place(relx=0.5, rely=0.03, anchor=tkinter.CENTER)

    pitch_p_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10,
                                      placeholder_text="Pitch P")
    pitch_p_gain_entry.place(relx=0.74, rely=0.09, anchor=tkinter.CENTER)
    pitch_p_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                      text=f"{config_data_dict['pitch_p']:.2f}",
                                      font=("Arial", 18, "bold"))
    pitch_p_gain_label.place(relx=0.26, rely=0.09, anchor=tkinter.CENTER)

    pitch_i_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10,
                                      placeholder_text="Pitch I")
    pitch_i_gain_entry.place(relx=0.74, rely=0.15, anchor=tkinter.CENTER)
    pitch_i_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                      text=f"{config_data_dict['pitch_i']:.2f}",
                                      font=("Arial", 18, "bold"))
    pitch_i_gain_label.place(relx=0.26, rely=0.15, anchor=tkinter.CENTER)

    pitch_d_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10,
                                      placeholder_text="Pitch D")
    pitch_d_gain_entry.place(relx=0.74, rely=0.21, anchor=tkinter.CENTER)
    pitch_d_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                      text=f"{config_data_dict['pitch_d']:.2f}",
                                      font=("Arial", 18, "bold"))
    pitch_d_gain_label.place(relx=0.26, rely=0.21, anchor=tkinter.CENTER)

    roll_p_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10,
                                     placeholder_text="Roll P")
    roll_p_gain_entry.place(relx=0.74, rely=0.29, anchor=tkinter.CENTER)
    roll_p_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                     text=f"{config_data_dict['roll_p']:.2f}",
                                     font=("Arial", 18, "bold"))
    roll_p_gain_label.place(relx=0.26, rely=0.29, anchor=tkinter.CENTER)

    roll_i_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10,
                                     placeholder_text="Roll I")
    roll_i_gain_entry.place(relx=0.74, rely=0.35, anchor=tkinter.CENTER)
    roll_i_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                     text=f"{config_data_dict['roll_i']:.2f}",
                                     font=("Arial", 18, "bold"))
    roll_i_gain_label.place(relx=0.26, rely=0.35, anchor=tkinter.CENTER)

    roll_d_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10,
                                     placeholder_text="Roll D")
    roll_d_gain_entry.place(relx=0.74, rely=0.41, anchor=tkinter.CENTER)
    roll_d_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                     text=f"{config_data_dict['roll_d']:.2f}",
                                     font=("Arial", 18, "bold"))
    roll_d_gain_label.place(relx=0.26, rely=0.41, anchor=tkinter.CENTER)

    yaw_p_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10, placeholder_text="Yaw P")
    yaw_p_gain_entry.place(relx=0.74, rely=0.49, anchor=tkinter.CENTER)
    yaw_p_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                    text=f"{config_data_dict['yaw_p']:.2f}",
                                    font=("Arial", 18, "bold"))
    yaw_p_gain_label.place(relx=0.26, rely=0.49, anchor=tkinter.CENTER)

    yaw_i_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10, placeholder_text="Yaw I")
    yaw_i_gain_entry.place(relx=0.74, rely=0.55, anchor=tkinter.CENTER)
    yaw_i_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                    text=f"{config_data_dict['yaw_i']:.2f}",
                                    font=("Arial", 18, "bold"))
    yaw_i_gain_label.place(relx=0.26, rely=0.55, anchor=tkinter.CENTER)

    ff_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10, placeholder_text="FF G")
    ff_gain_entry.place(relx=0.74, rely=0.62, anchor=tkinter.CENTER)
    ff_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                 text=f"{config_data_dict['ff_gain']:.2f}",
                                 font=("Arial", 18, "bold"))
    ff_gain_label.place(relx=0.26, rely=0.62, anchor=tkinter.CENTER)

    pos_p_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10, placeholder_text="Pos P")
    pos_p_gain_entry.place(relx=0.74, rely=0.69, anchor=tkinter.CENTER)
    pos_p_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                    text=f"{config_data_dict['position_p']:.2f}",
                                    font=("Arial", 18, "bold"))
    pos_p_gain_label.place(relx=0.26, rely=0.69, anchor=tkinter.CENTER)

    pos_i_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10, placeholder_text="Pos I")
    pos_i_gain_entry.place(relx=0.74, rely=0.75, anchor=tkinter.CENTER)
    pos_i_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                    text=f"{config_data_dict['position_i']:.2f}",
                                    font=("Arial", 18, "bold"))
    pos_i_gain_label.place(relx=0.26, rely=0.75, anchor=tkinter.CENTER)

    alt_p_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10, placeholder_text="Alt P")
    alt_p_gain_entry.place(relx=0.74, rely=0.83, anchor=tkinter.CENTER)
    alt_p_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                    text=f"{config_data_dict['altitude_p']:.2f}",
                                    font=("Arial", 18, "bold"))
    alt_p_gain_label.place(relx=0.26, rely=0.83, anchor=tkinter.CENTER)

    alt_i_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10, placeholder_text="Alt I")
    alt_i_gain_entry.place(relx=0.74, rely=0.89, anchor=tkinter.CENTER)
    alt_i_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                    text=f"{config_data_dict['altitude_i']:.2f}",
                                    font=("Arial", 18, "bold"))
    alt_i_gain_label.place(relx=0.26, rely=0.89, anchor=tkinter.CENTER)

    alt_d_gain_entry = ctk.CTkEntry(master=frame3, width=120, height=35, corner_radius=10, placeholder_text="Alt D")
    alt_d_gain_entry.place(relx=0.74, rely=0.95, anchor=tkinter.CENTER)
    alt_d_gain_label = ctk.CTkLabel(master=frame3, width=120, height=35, corner_radius=10,
                                    text=f"{config_data_dict['altitude_d']:.2f}",
                                    font=("Arial", 18, "bold"))
    alt_d_gain_label.place(relx=0.26, rely=0.95, anchor=tkinter.CENTER)

    # KALMAN FRAME
    frame2 = ctk.CTkFrame(master=main_frame, width=280, height=760, corner_radius=10)
    frame2.place(relx=0.625, rely=0.5, anchor=tkinter.CENTER)

    # TITLE KALMAN
    other_parameters_label = ctk.CTkLabel(master=frame2, width=200, height=35, corner_radius=10,
                                          text="Other Parameters", font=("Arial", 22, "bold"))
    other_parameters_label.place(relx=0.5, rely=0.03, anchor=tkinter.CENTER)

    ahrs_filter_beta_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                          placeholder_text="AHRS Beta")
    ahrs_filter_beta_entry.place(relx=0.74, rely=0.09, anchor=tkinter.CENTER)
    ahrs_filter_beta_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                          text=f"{config_data_dict['ahrs_filter_beta']:.3f}",
                                          font=("Arial", 18, "bold"))
    ahrs_filter_beta_label.place(relx=0.26, rely=0.09, anchor=tkinter.CENTER)

    ahrs_filter_zeta_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                          placeholder_text="AHRS Zeta")
    ahrs_filter_zeta_entry.place(relx=0.74, rely=0.15, anchor=tkinter.CENTER)
    ahrs_filter_zeta_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                          text=f"{config_data_dict['ahrs_filter_zeta']:.3f}",
                                          font=("Arial", 18, "bold"))
    ahrs_filter_zeta_label.place(relx=0.26, rely=0.15, anchor=tkinter.CENTER)

    altitude_filter_beta_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                              placeholder_text="Alt Beta")
    altitude_filter_beta_entry.place(relx=0.74, rely=0.21, anchor=tkinter.CENTER)
    altitude_filter_beta_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                              text=f"{config_data_dict['alt_filter_beta']:.3f}",
                                              font=("Arial", 18, "bold"))
    altitude_filter_beta_label.place(relx=0.26, rely=0.21, anchor=tkinter.CENTER)

    velz_filter_beta_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                          placeholder_text="VelZ Beta")
    velz_filter_beta_entry.place(relx=0.74, rely=0.28, anchor=tkinter.CENTER)
    velz_filter_beta_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                          text=f"{config_data_dict['velz_filter_beta']:.3f}",
                                          font=("Arial", 18, "bold"))
    velz_filter_beta_label.place(relx=0.26, rely=0.28, anchor=tkinter.CENTER)

    velz_filter_zeta_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                          placeholder_text="VelZ Zeta")
    velz_filter_zeta_entry.place(relx=0.74, rely=0.34, anchor=tkinter.CENTER)
    velz_filter_zeta_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                          text=f"{config_data_dict['velz_filter_zeta']:.3f}",
                                          font=("Arial", 18, "bold"))
    velz_filter_zeta_label.place(relx=0.26, rely=0.34, anchor=tkinter.CENTER)

    velxy_filter_beta_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                           placeholder_text="VelXY Beta")
    velxy_filter_beta_entry.place(relx=0.74, rely=0.40, anchor=tkinter.CENTER)
    velxy_filter_beta_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                           text=f"{config_data_dict['velxy_filter_beta']:.3f}",
                                           font=("Arial", 18, "bold"))
    velxy_filter_beta_label.place(relx=0.26, rely=0.40, anchor=tkinter.CENTER)

    alt_to_vel_gain_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                         placeholder_text="Alt Vel Gain")
    alt_to_vel_gain_entry.place(relx=0.74, rely=0.47, anchor=tkinter.CENTER)
    alt_to_vel_gain_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                         text=f"{config_data_dict['alt_to_vel_gain']:.2f}",
                                         font=("Arial", 18, "bold"))
    alt_to_vel_gain_label.place(relx=0.26, rely=0.47, anchor=tkinter.CENTER)

    wp_threshold_cm_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                         placeholder_text="WP Threshold")
    wp_threshold_cm_entry.place(relx=0.74, rely=0.53, anchor=tkinter.CENTER)
    wp_threshold_cm_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                         text=f"{config_data_dict['wp_threshold_cm']:.0f}",
                                         font=("Arial", 18, "bold"))
    wp_threshold_cm_label.place(relx=0.26, rely=0.53, anchor=tkinter.CENTER)

    wp_heading_correct_gain_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                                 placeholder_text="WP head Corr Gain")
    wp_heading_correct_gain_entry.place(relx=0.74, rely=0.59, anchor=tkinter.CENTER)
    wp_heading_correct_gain_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                                 text=f"{config_data_dict['wp_heading_correct_gain']:.4f}",
                                                 font=("Arial", 18, "bold"))
    wp_heading_correct_gain_label.place(relx=0.26, rely=0.59, anchor=tkinter.CENTER)

    wp_dist_to_vel_gain_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                             placeholder_text="WP Dist Vel Gain")
    wp_dist_to_vel_gain_entry.place(relx=0.74, rely=0.65, anchor=tkinter.CENTER)
    wp_dist_to_vel_gain_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                             text=f"{config_data_dict['wp_dist_to_vel_gain']:.1f}",
                                             font=("Arial", 18, "bold"))
    wp_dist_to_vel_gain_label.place(relx=0.26, rely=0.65, anchor=tkinter.CENTER)

    q_pos_process_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                       placeholder_text="Q Position")
    q_pos_process_entry.place(relx=0.74, rely=0.72, anchor=tkinter.CENTER)

    q_pos_process_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                       text=f"-",
                                       font=("Arial", 18, "bold"))
    q_pos_process_label.place(relx=0.26, rely=0.72, anchor=tkinter.CENTER)

    r_pos_gnss_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                    placeholder_text="R Pos GNSS")
    r_pos_gnss_entry.place(relx=0.74, rely=0.78, anchor=tkinter.CENTER)

    r_pos_gnss_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                    text=f"-",
                                    font=("Arial", 18, "bold"))
    r_pos_gnss_label.place(relx=0.26, rely=0.78, anchor=tkinter.CENTER)

    r_horiz_vel_gnss_entry = ctk.CTkEntry(master=frame2, width=120, height=35, corner_radius=10,
                                          placeholder_text="R Horiz Vel GNSS")
    r_horiz_vel_gnss_entry.place(relx=0.74, rely=0.84, anchor=tkinter.CENTER)

    r_horiz_vel_gnss_label = ctk.CTkLabel(master=frame2, width=120, height=35, corner_radius=10,
                                          text=f"-",
                                          font=("Arial", 18, "bold"))
    r_horiz_vel_gnss_label.place(relx=0.26, rely=0.84, anchor=tkinter.CENTER)

    # FRAME 4
    frame4 = ctk.CTkFrame(master=main_frame, width=280, height=700, corner_radius=10)
    frame4.place(relx=0.875, rely=0.463, anchor=tkinter.CENTER)

    # FILTERS TITLE
    filter_settings_label = ctk.CTkLabel(master=frame4, width=200, height=35, corner_radius=10,
                                         text="Filter Settings", font=("Arial", 22, "bold"))
    filter_settings_label.place(relx=0.5, rely=0.03, anchor=tkinter.CENTER)

    # GYRO FILTER TITLE
    notch_1_filter_lable = ctk.CTkLabel(master=frame4, width=200, height=35, corner_radius=10,
                                        text="Notch Filter", font=("Arial", 16, "bold"))
    notch_1_filter_lable.place(relx=0.5, rely=0.09, anchor=tkinter.CENTER)

    notch_1_freq_entry = ctk.CTkEntry(master=frame4, width=120, height=35, corner_radius=10,
                                      placeholder_text="Notch 1 Freq")
    notch_1_freq_entry.place(relx=0.74, rely=0.15, anchor=tkinter.CENTER)
    notch_1_freq_label = ctk.CTkLabel(master=frame4, width=120, height=35, corner_radius=10,
                                      text=f"{config_data_dict['notch_1_freq']:.2f}",
                                      font=("Arial", 18, "bold"))
    notch_1_freq_label.place(relx=0.26, rely=0.15, anchor=tkinter.CENTER)

    notch_1_width_entry = ctk.CTkEntry(master=frame4, width=120, height=35, corner_radius=10,
                                       placeholder_text="Notch 1 Width")
    notch_1_width_entry.place(relx=0.74, rely=0.21, anchor=tkinter.CENTER)
    notch_1_width_label = ctk.CTkLabel(master=frame4, width=120, height=35, corner_radius=10,
                                       text=f"{config_data_dict['notch_1_bandwidth']:.2f}",
                                       font=("Arial", 18, "bold"))
    notch_1_width_label.place(relx=0.26, rely=0.21, anchor=tkinter.CENTER)

    # D TERM FILTER TITLE
    d_term_notch_filter_label = ctk.CTkLabel(master=frame4, width=200, height=35, corner_radius=10,
                                             text="D Term Notch", font=("Arial", 16, "bold"))
    d_term_notch_filter_label.place(relx=0.5, rely=0.27, anchor=tkinter.CENTER)

    d_term_notch_freq_entry = ctk.CTkEntry(master=frame4, width=120, height=35, corner_radius=10,
                                           placeholder_text="Center Freq")
    d_term_notch_freq_entry.place(relx=0.74, rely=0.33, anchor=tkinter.CENTER)
    d_term_notch_freq_label = ctk.CTkLabel(master=frame4, width=120, height=35, corner_radius=10,
                                           text=f"",
                                           font=("Arial", 18, "bold"))
    d_term_notch_freq_label.place(relx=0.24, rely=0.33, anchor=tkinter.CENTER)

    d_term_notch_width_entry = ctk.CTkEntry(master=frame4, width=120, height=35, corner_radius=10,
                                            placeholder_text="Notch Width")
    d_term_notch_width_entry.place(relx=0.74, rely=0.39, anchor=tkinter.CENTER)

    d_term_notch_width_label = ctk.CTkLabel(master=frame4, width=120, height=35, corner_radius=10,
                                            text=f"",
                                            font=("Arial", 18, "bold"))
    d_term_notch_width_label.place(relx=0.24, rely=0.39, anchor=tkinter.CENTER)
