telemetry_data_dict = {
    "packet_delivery": 0.0,
    "battery_voltage": 0.0,
    "pitch": 0.0,
    "roll": 0.0,
    "heading": 0.0,
    "altitude": 0.0,
    "altitude_calibrated": 0.0,
    "tof_distance_1": 0.0,
    "tof_distance_2": 0.0,
    "velocity_x_ms": 0.0,
    "velocity_y_ms": 0.0,
    "velocity_z_ms": 0.0,
    "flow_x_velocity": 0.0,
    "flow_y_velocity": 0.0,
    "flow_quality": 0.0,
    "flight_mode": 0.0,
    "arm_status": 0.0,

    "target_pitch": 0.0,
    "target_roll": 0.0,

    "target_heading": 0.0,
    "target_pitch_dps": 0.0,
    "target_roll_dps": 0.0,

    "target_yaw_dps": 0.0,
    "target_altitude": 0.0,
    "target_velocity_x_ms": 0.0,
    "target_velocity_y_ms": 0.0,
    "target_velocity_z_ms": 0.0,

    "barometer_pressure": 0.0,
    "barometer_temperature": 0.0,
    "imu_temperature": 0.0,

    "gyro_x_dps": 0.0,
    "gyro_y_dps": 0.0,
    "gyro_z_dps": 0.0,

    "acc_x_ms2": 0.0,
    "acc_y_ms2": 0.0,
    "acc_z_ms2": 0.0,

    "mag_x_gauss": 0.0,
    "mag_y_gauss": 0.0,
    "mag_z_gauss": 0.0,

    "gps_fix": 0.0,
    "gps_satCount": 0.0,
    "gps_latitude": 0.0,
    "gps_longitude": 0.0,
    "gps_altitude_m": 0.0,
    "gps_northVel_ms": 0.0,
    "gps_eastVel_ms": 0.0,
    "gps_downVel_ms": 0.0,
    "gps_headingOfMotion": 0.0,
    "gps_hdop": 0.0,
    "gps_vdop": 0.0,
    "gps_latitude_origin": 0.0,
    "gps_longitude_origin": 0.0,
    "gps_altitude_origin": 0.0,
    "target_latitude": 0.0,
    "target_longitude": 0.0,
    "distance_m_2d": 0.0,
    "distance_m_3d": 0.0,
    "velocity_ms_2d": 0.0
}

telemetry_format_dict = {
    "packet_delivery": "B",

    "battery_voltage": "f",
    "pitch": "f",
    "roll": "f",
    "heading": "f",

    "altitude": "h",
    "altitude_calibrated": "h",
    "tof_distance_1": "h",
    "tof_distance_2": "h",
    "velocity_x_ms": "h",
    "velocity_y_ms": "h",
    "velocity_z_ms": "h",
    "flow_x_velocity": "h",
    "flow_y_velocity": "h",

    "flow_quality": "B",
    "flight_mode": "B",
    "arm_status": "B",

    "target_pitch": "f",
    "target_roll": "f",
    "target_heading": "f",
    "target_pitch_dps": "f",
    "target_roll_dps": "f",
    "target_yaw_dps": "f",
    "target_altitude": "f",
    "target_velocity_x_ms": "f",
    "target_velocity_y_ms": "f",
    "target_velocity_z_ms": "f",

    "barometer_pressure": "h",
    "barometer_temperature": "H",
    "imu_temperature": "H",
    "gyro_x_dps": "h",
    "gyro_y_dps": "h",
    "gyro_z_dps": "h",
    "acc_x_ms2": "h",
    "acc_y_ms2": "h",
    "acc_z_ms2": "h",
    "mag_x_gauss": "h",
    "mag_y_gauss": "h",
    "mag_z_gauss": "h",

    "gps_fix": "B",
    "gps_satCount": "B",

    "gps_latitude": "i",
    "gps_longitude": "i",
    "gps_altitude_m": "i",
    "gps_northVel_ms": "i",
    "gps_eastVel_ms": "i",
    "gps_downVel_ms": "i",
    "gps_headingOfMotion": "i",

    "gps_hdop": "H",
    "gps_vdop": "H",

    "gps_latitude_origin": "i",
    "gps_longitude_origin": "i",
    "gps_altitude_origin": "i",
    "target_latitude": "i",
    "target_longitude": "i",
    "distance_m_2d": "f",
    "distance_m_3d": "f",
    "velocity_ms_2d": "f"
}

telemetry_scale_dict = {
    "packet_delivery": 1,

    "battery_voltage": 1,
    "pitch": 1,
    "roll": 1,
    "heading": 1,

    "altitude": 100.0,
    "altitude_calibrated": 100,
    "tof_distance_1": 1,
    "tof_distance_2": 1,
    "velocity_x_ms": 1000.0,
    "velocity_y_ms": 1000.0,
    "velocity_z_ms": 1000.0,
    "flow_x_velocity": 10.0,
    "flow_y_velocity": 10.0,

    "flow_quality": 1,
    "flight_mode": 1,
    "arm_status": 1,

    "target_pitch": 1,
    "target_roll": 1,
    "target_heading": 1,
    "target_pitch_dps": 1,
    "target_roll_dps": 1,
    "target_yaw_dps": 1,
    "target_altitude": 1,
    "target_velocity_x_ms": 1,
    "target_velocity_y_ms": 1,
    "target_velocity_z_ms": 1,

    "barometer_pressure": 10.0,
    "barometer_temperature": 100.0,
    "imu_temperature": 100.0,
    "gyro_x_dps": 100.0,
    "gyro_y_dps": 100.0,
    "gyro_z_dps": 100.0,
    "acc_x_ms2": 400.0,
    "acc_y_ms2": 400.0,
    "acc_z_ms2": 400.0,
    "mag_x_gauss": 1,
    "mag_y_gauss": 1,
    "mag_z_gauss": 1,

    "gps_fix": 1,
    "gps_satCount": 1,

    "gps_latitude": 10000000.0,
    "gps_longitude": 10000000.0,
    "gps_altitude_m": 1000.0,
    "gps_northVel_ms": 1000.0,
    "gps_eastVel_ms": 1000.0,
    "gps_downVel_ms": 1000.0,
    "gps_headingOfMotion": 100000.0,

    "gps_hdop": 100.0,
    "gps_vdop": 100.0,

    "gps_latitude_origin": 10000000.0,
    "gps_longitude_origin": 10000000.0,
    "gps_altitude_origin": 1000.0,
    "target_latitude": 10000000.0,
    "target_longitude": 10000000.0,
    "distance_m_2d": 1,
    "distance_m_3d": 1,
    "velocity_ms_2d": 1
}

config_data_dict = {
    "pitch_p": 0.0,
    "pitch_i": 0.0,
    "pitch_d": 0.0,

    "roll_p": 0.0,
    "roll_i": 0.0,
    "roll_d": 0.0,

    "yaw_p": 0.0,
    "yaw_i": 0.0,

    "ff_gain": 0.0,

    "position_p": 0.0,
    "position_i": 0.0,

    "altitude_p": 0.0,
    "altitude_i": 0.0,
    "altitude_d": 0.0,

    "max_pitch_angle": 0.0,
    "max_roll_angle": 0.0,
    "max_pitch_rate": 0.0,
    "max_roll_rate": 0.0,
    "max_yaw_rate": 0.0,

    "pitch_rate_scale": 0.0,
    "roll_rate_scale": 0.0,
    "yaw_rate_scale": 0.0,
    "max_vertical_velocity": 0.0,
    "max_horizontal_velocity": 0.0,

    "v_sens_gain": 0.0,
    "v_drop_compensation_gain": 0.0,
    "takeoff_altitude": 0.0,
    "hover_throttle": 0.0,

    "notch_1_freq": 0.0,
    "notch_1_bandwidth": 0.0,
    "notch_2_freq": 0.0,
    "notch_2_bandwidth": 0.0,
    "ahrs_filter_beta": 0.0,
    "ahrs_filter_zeta": 0.0,
    "alt_filter_beta": 0.0,
    "mag_declination_deg": 0.0,
    "velz_filter_beta": 0.0,
    "velz_filter_zeta": 0.0,
    "velxy_filter_beta": 0.0,

    "alt_to_vel_gain": 0.0,
    "wp_threshold_cm": 0.0,
    "wp_heading_correct_gain": 0.0,
    "wp_dist_to_vel_gain": 0.0
}

gamepad_data_dict = {
    "analog_LX": 0,
    "analog_LY": 0,
    "analog_RX": 0,
    "analog_RY": 0,
    "analog_LB": 0,
    "analog_RB": 0,
    "left_trigger": 0,
    "right_trigger": 0,
    "left_shoulder": 0,
    "right_shoulder": 0,
    "button_A": 0,
    "button_B": 0,
    "button_X": 0,
    "button_Y": 0
}

waypoint_coordinates = []
waypoint_only_latitudes = []
waypoint_only_longitudes = []
waypoint_only_altitudes = []
waypoint_markers = []
waypoint_counter = 0
waypoint_altitude = 0
motor_test_results = [0.0, 0.0, 0.0, 0.0]

drone_path_coordinates = []

