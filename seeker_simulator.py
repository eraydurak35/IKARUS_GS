
import serial
import struct
import time
import pygame
import numpy as np
import sys
import math

plane_data_format = 'ffffff'
seeker_data_format = 'fffffff'

# Uçaktan gelen verilerin tutulduğu yapı
plane_data_dict = {
    "ned_x_position": 0.0,
    "ned_y_position": 0.0,
    "ned_z_position": 0.0,
    "pitch_degree": 0.0,
    "roll_degree": 0.0,
    "heading_degree": 0.0
}
# Bu kod tarafından oluşturulan verilerin tutulduğu yapı
seeker_data_dict = {
    "x": 0.0,
    "y": 0.0,
    "valid": 0.0,
    "size": 0.0,
    "target_ned_x": 0.0,
    "target_ned_y": 0.0,
    "target_ned_z": 0.0
}
# seeker veri boyutu 7 * float = 28 byte
seeker_data_size = 28
# uçak verisinin boyutu 6 * float = 24 byte
plane_data_size = 24

# paketin başına eklenen tanımlayıcılar
seeker_data_header = b'\x2a'
plane_data_header = b'\x20'

# hedefin oluşturulduğu yerel pozisyon (metre)
target_ned_x = 1000 # kuzey
target_ned_y = -1500 # doğu
target_ned_z = 100 # yükseklik

# hedefin ilerleyeceği hız (m/s)
target_speed_ned_x = -10
target_speed_ned_y = 0
target_speed_ned_z = 0

boot_try_count = 5

# Renk tanımları
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)


# COM portunu aç
ser = serial.Serial('COM10', 57600, timeout=1)

pygame.init()
# görüntü pixel çözünürlüğü
img_width = 1024
img_height = 1024
scale = 1  # Gerekirse görüntü boyutunu büyütmek için
window = pygame.display.set_mode((img_width * scale, img_height * scale))
pygame.display.set_caption("Kamera Görüntüsü")
clock = pygame.time.Clock()

# Hedefin bulunduğu pixel değerleri
u = 0
v = 0

fx = 100  # Odak uzaklığı x (FOW fonksiyonu bunu otomatik hesaplıyor)
fy = 100  # Odak uzaklığı y (FOW fonksiyonu bunu otomatik hesaplıyor)

cx = img_width // 2  # Görüntü merkezinin x koordinatı (piksel)
cy = img_height // 2  # Görüntü merkezinin y koordinatı (piksel)

data_valid_button_color = blue

# Butona tıklama durumu
data_valid_button_clicked = False
data_valid_data_valid_mause_pressed = False

relative_speed = 0
prev_distance = 0


def initialize_camera_parameters(img_w, fov_x):
    global fx, fy
    # Görüş açısını radyana çevir
    fov_x_rad = math.radians(fov_x)
    # Odak uzaklıklarını hesapla
    fx = img_w / (2 * math.tan(fov_x_rad / 2))
    fy = fx  # Kare piksel varsayımı (aspect ratio 1:1 ise)

    return fx, fy, cx, cy


# Fow değerine göre kamera odak uzaklıklarını hesapla
initialize_camera_parameters(img_width, 90)


def read_uart_port():
    # bir byte oku
    data_header = ser.read(1)

    # header bulundu mu kontrol et
    if data_header == plane_data_header:
        # bulunduysa paket boyutu kadar byte oku
        data_bytes = ser.read(plane_data_size)
        # tüm byte'ları float'a çevir
        plane_data = struct.unpack(plane_data_format, data_bytes)
        # elde edlen float değerleri uçak veri yapısı içine atıyoruz
        for index, key in enumerate(plane_data_dict.keys()):
            plane_data_dict[key] = plane_data[index]

        # 0 +- 180 aralığından 0 360 aralığına çevir
        if plane_data_dict["heading_degree"] < 0:
            plane_data_dict["heading_degree"] = plane_data_dict["heading_degree"] + 360

        # veri paketi başarıyla alındı
        return True
    else:
        # okunan byte data header değil
        # print("data header bilinmiyor")
        return False


def write_uart_port():
    global ser
    # verinin byte'larının bulunacağı bytes değişkeni oluştur
    packed_data = bytes()
    for keys in seeker_data_dict.keys():
        # struct pack ile tüm float veriyi byte'larına ayır
        packed_data = packed_data + struct.pack('f', seeker_data_dict[keys])
    # paketin başına header ekle (42)
    packed_data = struct.pack('B', 42) + packed_data
    # paketlenen veriyi gönder
    ser.write(packed_data)


# Pitch, Roll, Yaw açılarından dönüşüm matrisi oluşturan fonksiyon
def create_rotation_matrix(pitch, roll, yaw):

    pitch_rad = math.radians(pitch)
    roll_rad = math.radians(roll)
    yaw_rad = math.radians(yaw)

    # # Roll (z ekseni etrafında)
    Rz = np.array([
        [np.cos(yaw_rad), -np.sin(yaw_rad), 0],
        [np.sin(yaw_rad), np.cos(yaw_rad), 0],
        [0, 0, 1]
    ])

    # Pitch (y ekseni etrafında)
    Ry = np.array([
        [np.cos(pitch_rad), 0, np.sin(pitch_rad)],
        [0, 1, 0],
        [-np.sin(pitch_rad), 0, np.cos(pitch_rad)]
    ])

    # Yaw (x ekseni etrafında)
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(roll_rad), -np.sin(roll_rad)],
        [0, np.sin(roll_rad), np.cos(roll_rad)]
    ])

    return Rz @ Ry @ Rx


def calculate_seeker_data():
    global u, v, img_width, img_height, cx, cy, fx, fy
    global target_ned_x, target_ned_y, target_ned_z

    pitch = plane_data_dict["pitch_degree"]  # Derece cinsinden
    roll = plane_data_dict["roll_degree"]    # Derece cinsinden
    yaw = plane_data_dict["heading_degree"]    # Derece cinsinden


    # Cismin dünya koordinatlarındaki pozisyonu (X, Y, Z)
    # X pozitifse uçak soldadır
    # Y pozitifse uçak yukarıdadır
    # Z pozitifse uçak geridedir
    world_coord = np.array([plane_data_dict["ned_z_position"] - target_ned_z, target_ned_y - plane_data_dict["ned_y_position"],
                             target_ned_x - plane_data_dict["ned_x_position"]])  # X, Y, Z değerleri metre cinsinden

    R = create_rotation_matrix(pitch, yaw, roll)
    # Cisim koordinatlarını kameranın koordinat sistemine dönüştür
    camera_coord = R @ world_coord
    # Z ekseni kameranın derinlik ekseni olduğu için negatifse görünmez demektir
    if camera_coord[2] <= 0:
        return

    # hedefin kameraya olan izdüşümünü hesapla
    v = fx * (camera_coord[0] / camera_coord[2]) + cx
    u = fy * (camera_coord[1] / camera_coord[2]) + cy


def calculate_distance_to_target():
    global target_ned_x, target_ned_y, target_ned_z
    return math.sqrt((target_ned_x - plane_data_dict["ned_x_position"]) ** 2 + (target_ned_y - plane_data_dict["ned_y_position"]) ** 2
                     + (target_ned_z - plane_data_dict["ned_z_position"]) ** 2)

# Ekrana artı işareti çizdir
def draw_grid():
    global img_height, img_width, scale
    pygame.draw.line(window, (200, 200, 200), ((img_width * scale / 2), 0), ((img_width * scale / 2), img_width * scale,))
    pygame.draw.line(window, (200, 200, 200), (0, (img_width * scale / 2)), (img_width * scale, (img_width * scale / 2)))


def draw_text(text, size, x, y, color):
    global img_height, img_width, scale
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)


def draw_button(text, x, y, width, height, color):
    font = pygame.font.Font(None, 22)
    pygame.draw.rect(window, color, (x, y, width, height))
    text_surface = font.render(text, True, white)
    window.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))


def update():
    global u, v, scale, target_ned_x, target_ned_y, target_ned_z, is_target_spawned, boot_try_count
    global oto_data_valid, prev_distance, relative_speed
    # Okunan ilk 5 değeri görmezden gel
    while boot_try_count > 0:
        ret = read_uart_port()
        time.sleep(0.03)
        if ret:
            boot_try_count = boot_try_count - 1

    ret = read_uart_port()
    # UART'tan yeni veri paketi geldiyse
    if ret:

        # Hedefi hareket ettir 0.03 delta time
        target_ned_x += target_speed_ned_x * 0.03
        target_ned_y += target_speed_ned_y * 0.03
        target_ned_z += target_speed_ned_z * 0.03

        window.fill((0, 0, 0))  # Arka planı siyah yap

        # seeker pixel koordinatlarını hesapla
        calculate_seeker_data()

        distance = 0
        # hedef kamera çözünürlüğü içindeyse
        if (0 < u < (img_width - 1)) and (0 < u < (img_height - 1)):
            distance = calculate_distance_to_target()
            print(f"{distance:.1f}")
            relative_speed = (distance - prev_distance) / 0.03
            prev_distance = distance
            radius = max(1, int(1000.0 / distance))
            u_int = int(u)
            v_int = int(v)
            # belirlenen pixel koordinatlarına bir daire çiz. Boyutu mesafe ile ters orantılı olarak artacak
            pygame.draw.circle(window, (255, 255, 255), (u_int * scale, v_int * scale), radius)

            # pixel değerlerini +- 1.0 aralığına sınırla
            seeker_data_dict["y"] = (((v / img_height) * -2.0) + 1.0)
            if seeker_data_dict["y"] > 1.0:
                seeker_data_dict["y"] = 1.0
            elif seeker_data_dict["y"] < -1.0:
                seeker_data_dict["y"] = -1.0

            # pixel değerlerini +- 1.0 aralığına sınırla
            seeker_data_dict["x"] = ((u / img_width) * 2.0) - 1.0
            if seeker_data_dict["x"] > 1.0:
                seeker_data_dict["x"] = 1.0
            elif seeker_data_dict["x"] < -1.0:
                seeker_data_dict["x"] = -1.0

            seeker_data_dict["size"] = radius
        else:
            # değilse ekranın ortasına uyarı yaz
            draw_text("Hedef Tespit Edilmedi", 50, cx * scale, cy * scale, white)


        # Fare pozisyonu ve tıklamayı kontrol et
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        # Buton konumu ve boyutları
        data_valid_button_x, data_valid_button_y = 50, 10
        data_valid_button_width, data_valid_button_height = 100, 25
        draw_button("Switch Dv", data_valid_button_x, data_valid_button_y, data_valid_button_width, data_valid_button_height, data_valid_button_color)

        # Fare tıklamasını kontrol et
        global data_valid_button_clicked, data_valid_mause_pressed
        if (data_valid_button_x <= mouse_pos[0] <= data_valid_button_x + data_valid_button_width and data_valid_button_y <= mouse_pos[1] <= data_valid_button_y
                + data_valid_button_height):
            if mouse_click[0]:  # Sol fare tuşuna basılıysa
                if not data_valid_mause_pressed:  # Daha önce basılı değilse
                    data_valid_mause_pressed = True  # Fare tıklaması başladı
                    data_valid_button_clicked = True  # Buton tıklandı

                    # tıklandığında data_valid değişkeninin durumunu değiştir
                    if seeker_data_dict["valid"] > 0.0:
                        seeker_data_dict["valid"] = 0.0
                    elif seeker_data_dict["valid"] < 1.0:
                        seeker_data_dict["valid"] = 1.0
            else:
                data_valid_mause_pressed = False

        # Buton tıklanınca rengi değiştir
        if data_valid_button_clicked:
            draw_button("Switch Dv", data_valid_button_x, data_valid_button_y, data_valid_button_width, data_valid_button_height, green)
            data_valid_button_clicked = False

        # ekranın köşesine gerekli bilgileri yazdır
        draw_grid()
        draw_text(f"valid = {seeker_data_dict['valid']:.0f}", 25, 100, 50, white)
        draw_text(f"X: {seeker_data_dict['x']:.2f} Y: {seeker_data_dict['y']:.2f}", 25, 100, 80, white)
        draw_text(f"Size: {seeker_data_dict['size']:.0f}", 25, 100, 110, white)
        draw_text(f"Distance: {distance:.0f}m", 25, 100, 140, white)
        # draw_text(f"Rel Spd: {relative_speed:.1f}m/s", 25, cx - 10, cy + 5, white)

        # hedefin konumunu kaydet
        seeker_data_dict["target_ned_x"] = target_ned_x
        seeker_data_dict["target_ned_y"] = target_ned_y
        seeker_data_dict["target_ned_z"] = target_ned_z

        # tüm veriyi uçağa gönder
        write_uart_port()
        pygame.display.update()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    update()
    clock.tick(30)  # Her saniyede bir kare
pygame.quit()
sys.exit()

