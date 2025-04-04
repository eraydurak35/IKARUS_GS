import customtkinter as ctk
from data_struct import *
import data_struct

# Global değişkenler
mavlink_inspector_window = None
details_table_labels = {}  # {"HEARTBEAT": {"field1": label1, ...}, ...}
current_message_name = "HEARTBEAT"
current_message_label = None
details_frame = None
message_data = {
    "HEARTBEAT": mavlink_msg_heartbeat,
    "IMU": mavlink_msg_imu,
    "ATTITUDE": mavlink_msg_attitude,
    "TARGET_ATTITUDE": mavlink_msg_target_attitude,
    "GNSS": mavlink_msg_gnss,
    "BAROMETER": mavlink_msg_barometer,
    "TARGET_POS_VEL": mavlink_msg_target_pos_vel,
    "POS_VEL": mavlink_msg_pos_vel,
    "OPTICAL_FLOW": mavlink_msg_optical_flow,
    "RANGE_FINDER": mavlink_msg_range_finder,
    "CPU_USAGE": mavlink_msg_cpu_usage,
    "RC_CHANNELS": mavlink_msg_rc_channels
}


def clear_details_table():
    """Detay tablosunu tamamen temizler"""
    global details_table_labels
    if details_frame and details_frame.winfo_exists():
        for child in details_frame.winfo_children():
            child.destroy()
    details_table_labels = {}


def update_details_table_values(message_name: str):
    global message_freq
    """Mevcut tabloda sadece değerleri günceller"""
    if message_name not in details_table_labels:
        return

    msg_data = message_data.get(message_name, {})
    for field, value_label in details_table_labels[message_name].items():
        if field in msg_data:
            try:
                value_label.configure(text=str(msg_data[field]))
            except:
                pass

    message_freq = {
        "HEARTBEAT": data_struct.mavlink_msg_heartbeat_freq,
        "IMU": data_struct.mavlink_msg_imu_freq,
        "ATTITUDE": data_struct.mavlink_msg_attitude_freq,
        "TARGET_ATTITUDE": data_struct.mavlink_msg_target_attitude_freq,
        "GNSS": data_struct.mavlink_msg_gnss_freq,
        "BAROMETER": data_struct.mavlink_msg_barometer_freq,
        "TARGET_POS_VEL": data_struct.mavlink_msg_target_pos_vel_freq,
        "POS_VEL": data_struct.mavlink_msg_pos_vel_freq,
        "OPTICAL_FLOW": data_struct.mavlink_msg_optical_flow_freq,
        "RANGE_FINDER": data_struct.mavlink_msg_range_finder_freq,
        "CPU_USAGE": mavlink_msg_cpu_usage_freq,
        "RC_CHANNELS": mavlink_msg_rc_channels_freq
    }

    if current_message_label and current_message_label.winfo_exists():
        current_message_label.configure(text=f"{message_name} {message_freq[message_name]:.1f}Hz")



def create_details_table(message_name: str):
    """Yeni bir detay tablosu oluşturur"""
    global details_table_labels, current_message_name, message_freq

    # Önceki tabloyu temizle
    clear_details_table()

    # Yeni bir entry oluştur
    details_table_labels[message_name] = {}
    current_message_name = message_name

    # Mesaj verilerini al
    msg_data = message_data.get(message_name, {})

    if current_message_label and current_message_label.winfo_exists():
        current_message_label.configure(text=f"{message_name} {message_freq[message_name]:.1f}Hz")

    # Yeni tablo oluştur
    if details_frame and details_frame.winfo_exists():
        for i, (field, value) in enumerate(msg_data.items()):
            # Alan adı
            field_label = ctk.CTkLabel(
                details_frame,
                text=f"{field}:",
                anchor="w",
                width=200
            )
            field_label.grid(row=i, column=0, padx=5, pady=2, sticky="w")

            # Alan değeri
            value_label = ctk.CTkLabel(
                details_frame,
                text=str(value),
                anchor="w",
                width=200
            )
            value_label.grid(row=i, column=1, padx=5, pady=2, sticky="w")

            # Label'ı kaydet
            details_table_labels[message_name][field] = value_label


def show_message_details(message_name: str = None):
    """Akıllı mesaj detay gösterimi"""
    global current_message_name

    if not message_name:
        message_name = current_message_name

    # Pencere kontrolü
    if not mavlink_inspector_window or not mavlink_inspector_window.winfo_exists():
        return

    # Frame kontrolü
    if not details_frame or not details_frame.winfo_exists():
        return

    try:
        # Mesaj tipi değiştiyse tamamen yeniden oluştur
        if message_name != current_message_name or message_name not in details_table_labels:
            create_details_table(message_name)
        else:
            # Aynı mesaj tipi, sadece değerleri güncelle
            update_details_table_values(message_name)

    except Exception as e:
        print(f"Mesaj detay gösterim hatası: {e}")


def update_message_data(msg_type: str, new_data: dict):
    """Dışarıdan mesaj verilerini günceller"""
    global message_data

    if msg_type in message_data:
        message_data[msg_type].update(new_data)
        # Eğer güncellenen mesaj şu an gösteriliyorsa UI'ı güncelle
        if msg_type == current_message_name:
            show_message_details()


def show_mavlink_inspector_ui():
    """MAVLink Inspector UI'ını oluşturur"""
    global mavlink_inspector_window, current_message_label, details_frame

    # Pencere ayarları
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    mavlink_inspector_window = ctk.CTkToplevel()
    mavlink_inspector_window.title("MAVLink Inspector")
    mavlink_inspector_window.geometry("800x600")

    mavlink_inspector_window.grab_set()
    mavlink_inspector_window.resizable(False, False)

    # Ana frame
    main_frame = ctk.CTkFrame(master=mavlink_inspector_window, width=1200, height=780, corner_radius=10)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Sol panel (Mesaj listesi)
    left_panel = ctk.CTkFrame(main_frame, width=200)
    left_panel.pack(side="left", fill="y", padx=5, pady=5)

    # Sağ panel (Mesaj içeriği)
    right_panel = ctk.CTkFrame(main_frame)
    right_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    # Mesaj listesi
    message_listbox = ctk.CTkScrollableFrame(left_panel)
    message_listbox.pack(fill="both", expand=True)

    # Mesaj butonları oluştur
    for msg_name in message_data.keys():
        btn = ctk.CTkButton(
            message_listbox,
            text=msg_name,
            command=lambda name=msg_name: show_message_details(name)
        )
        btn.pack(fill="x", pady=2)

    # Detay görüntüleme alanı
    details_frame = ctk.CTkScrollableFrame(right_panel)
    details_frame.pack(fill="both", expand=True)

    # Başlık
    current_message_label = ctk.CTkLabel(
        right_panel,
        text="Mesaj Seçiniz",
        font=("Arial", 14, "bold")
    )
    current_message_label.pack(pady=5)

    # İlk mesajı göster
    show_message_details(current_message_name)
