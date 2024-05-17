import copy
import json
import data_struct as ds
import serial_backend

def save_mission(path, angle, spacing, padding, reverse, invert):

    waypoints_json_data = {
        'waypoints': ds.waypoint_coordinates,
        'field_points': ds.field_coordinates,
        'altitudes': ds.waypoint_only_altitudes,
        'end_of_mission_behavior_code': serial_backend.end_of_wp_mission_behaviour_code,
        'auto_mission_angle': angle,
        'auto_mission_spacing': spacing,
        'auto_mission_padding': padding,
        'auto_mission_reverse': reverse,
        'auto_mission_invert': invert,
    }

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(waypoints_json_data, f, ensure_ascii=False, indent=4)


def load_mission(path):

    with open(path, 'r', encoding='utf-8') as f:
        waypoints_json_data = json.load(f)

    print(waypoints_json_data["waypoints"])

    waypoints_json_data["waypoints"] = [tuple(point) for point in waypoints_json_data["waypoints"]]
    waypoints_json_data["field_points"] = [tuple(point) for point in waypoints_json_data["field_points"]]

    print(waypoints_json_data["waypoints"])

    return waypoints_json_data