import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
from shapely.geometry import Point, Polygon
from pyproj import Proj, Transformer
import threading

noktalar = [(1.2, -25.0), (50.0, 25.0), (20.0, 50.0), (10.0, 45.0), (1.0, 35.0)]
# noktalar = []
# noktalar = [(0.0, 0.0), (25.0, 0.0), (25.0, 25.0), (0.0, 25.0)]
grid_boyutu = 0.00005  # Kullanıcı tarafından belirlenecek grid boyutu
aci = -0.0  # Döndürme açısı derece cinsinden
maksimum_izin_verilen_kenar_mesafesi = 1.0  # Kullanıcının belirleyeceği maksimum kenar mesafesi

done_event = threading.Event()

birlesik_liste_latlon = []
bas_ve_son_noktalar_latlon = []

# WGS84 (enlem/boylam) projeksiyon tanımı
wgs84 = Proj('epsg:4326')

# İzmir için UTM projeksiyon tanımı
utm_izmir = Proj('epsg:32637')  # İzmir'i kapsayan UTM bölgesi

# Transformer sınıfını kullanarak dönüşüm
transformer = Transformer.from_crs("epsg:4326", "epsg:32637", always_xy=True)


# Enlem ve boylamdan UTM'ye dönüşüm
def latlon_to_utm(lat, lon):
    x, y = transformer.transform(lon, lat)
    return x, y


# UTM'den enlem ve boylama dönüşüm
def utm_to_latlon(x, y):
    lon, lat = transformer.transform(x, y, direction='INVERSE')
    return lat, lon


def en_uzak_noktalari_bul(noktalar):
    max_mesafe = 0
    for i, nokta1 in enumerate(noktalar):
        for nokta2 in noktalar[i + 1:]:
            mesafe = np.linalg.norm(np.array(nokta1) - np.array(nokta2))
            if mesafe > max_mesafe:
                max_mesafe = mesafe
    return max_mesafe


def dondurme_matrisi_olustur(acı):
    radian = np.deg2rad(acı)
    return np.array([[np.cos(radian), -np.sin(radian)], [np.sin(radian), np.cos(radian)]])


def kenara_olan_mesafeyi_hesapla(nokta, cokgen):
    point = Point(nokta)
    return cokgen.boundary.distance(point)


def grid_noktalari_donustur_ve_kontrol_et(noktalar, grid_boyutu, acı, maksimum_izin_verilen_kenar_mesafesi):
    # Çokgeni oluştur
    cokgen = Polygon(noktalar)
    path_cokgen = mpath.Path(noktalar)

    # Gridin merkezini hesapla
    grid_merkezi = ((max(noktalar, key=lambda x: x[0])[0] + min(noktalar, key=lambda x: x[0])[0]) / 2,
                    (max(noktalar, key=lambda x: x[1])[1] + min(noktalar, key=lambda x: x[1])[1]) / 2)

    # Döndürülmüş grid noktalarını içeren listeyi oluştur
    icerideki_noktalar = []

    expand_amount = en_uzak_noktalari_bul(noktalar)

    # Çokgenin sınırlarını hesapla
    min_x = min(noktalar, key=lambda x: x[0])[0] - expand_amount
    max_x = max(noktalar, key=lambda x: x[0])[0] + expand_amount
    min_y = min(noktalar, key=lambda x: x[1])[1] - expand_amount
    max_y = max(noktalar, key=lambda x: x[1])[1] + expand_amount

    # Grid boyutuna göre tüm noktaları kontrol et
    x = min_x
    while x <= max_x:
        y = min_y
        while y <= max_y:
            # Noktayı grid merkezine göre döndür
            nokta = np.array([x, y]) - grid_merkezi
            dondurulmus_nokta = np.dot(dondurme_matrisi_olustur(acı), nokta) + grid_merkezi
            if path_cokgen.contains_point(dondurulmus_nokta):
                # Çokgenin kenarına olan mesafeyi hesapla
                mesafe = kenara_olan_mesafeyi_hesapla(dondurulmus_nokta, cokgen)
                if mesafe >= maksimum_izin_verilen_kenar_mesafesi:
                    icerideki_noktalar.append(dondurulmus_nokta)
            y += 0.2 #grid_boyutu # * y_corrention
        x += grid_boyutu# * x_correction

    return icerideki_noktalar


def ard_ardaki_noktalar_arasi_mesafe(noktalar):
    # Ardışık noktalar arasındaki mesafeleri hesapla
    mesafeler = [np.linalg.norm(np.array(noktalar[i]) - np.array(noktalar[i + 1])) for i in range(len(noktalar) - 1)]
    # print("mesafeler: ", mesafeler)
    return mesafeler


# ret = grid_noktalari_donustur_ve_kontrol_et(noktalar, grid_boyutu, aci, maksimum_izin_verilen_kenar_mesafesi)
#
# # Numpy array'leri tuple'a dönüştür
# nokta_ciktisi = [tuple(nokta) for nokta in ret]
# mesafe_listesi = ard_ardaki_noktalar_arasi_mesafe(nokta_ciktisi)


def gruplandir(noktalar, mesafeler, max_mesafe):
    gruplar = []
    mevcut_grup = [noktalar[0]]  # İlk noktayı ilk gruba ekle

    # İlk noktadan başlayarak mesafeleri kontrol et
    for i in range(1, len(noktalar)):
        if mesafeler[i - 1] <= max_mesafe:
            # Eğer mesafe max_mesafe'den küçük veya eşitse, noktayı mevcut gruba ekle
            # print(f"mesafe <= max --> {mesafeler[i - 1]}   <=   {max_mesafe}")
            mevcut_grup.append(noktalar[i])
        else:
            # Eğer mesafe max_mesafe'den büyükse, mevcut grubu gruplar listesine ekle ve yeni grup oluştur
            # print(f"mesafe > max --> {mesafeler[i - 1]}   >   {max_mesafe}")
            gruplar.append(mevcut_grup)
            mevcut_grup = [noktalar[i]]

    # Son grubu da gruplar listesine ekle
    gruplar.append(mevcut_grup)
    return gruplar


# Örnek kullanım:
# gruplanmis_noktalar = gruplandir(nokta_ciktisi, mesafe_listesi)


def gruplari_birlestir(gruplar, is_inverted):
    ana_liste = []
    bas_ve_sonlar = []  # Her grubun ilk ve son noktalarını saklayacak liste

    # Grupları sırayla ve bazılarını ters çevirerek ana listeye ekle
    for i, grup in enumerate(gruplar):
        if i % 2 == 0:

            if is_inverted == 0:

                # Çift indeksli gruplar (0, 2, 4, ...) olduğu gibi eklenecek
                ana_liste.extend(grup)
                # Grubun ilk ve son noktalarını bas_ve_sonlar listesine ekle
                if grup:  # Grup boş değilse
                    bas_ve_sonlar.append(grup[0])
                    bas_ve_sonlar.append(grup[-1])

            else:
                # Tek indeksli gruplar (1, 3, 5, ...) ters çevrilerek eklenecek
                grup_ters = list(reversed(grup))
                ana_liste.extend(grup_ters)
                # Ters çevrilmiş grubun ilk ve son noktalarını bas_ve_sonlar listesine ekle
                if grup_ters:  # Grup boş değilse
                    bas_ve_sonlar.append(grup_ters[0])
                    bas_ve_sonlar.append(grup_ters[-1])
        else:

            if is_inverted == 0:

                # Tek indeksli gruplar (1, 3, 5, ...) ters çevrilerek eklenecek
                grup_ters = list(reversed(grup))
                ana_liste.extend(grup_ters)
                # Ters çevrilmiş grubun ilk ve son noktalarını bas_ve_sonlar listesine ekle
                if grup_ters:  # Grup boş değilse
                    bas_ve_sonlar.append(grup_ters[0])
                    bas_ve_sonlar.append(grup_ters[-1])
            else:

                # Çift indeksli gruplar (0, 2, 4, ...) olduğu gibi eklenecek
                ana_liste.extend(grup)
                # Grubun ilk ve son noktalarını bas_ve_sonlar listesine ekle
                if grup:  # Grup boş değilse
                    bas_ve_sonlar.append(grup[0])
                    bas_ve_sonlar.append(grup[-1])

    return ana_liste, bas_ve_sonlar


# birlesik_liste, bas_ve_son_noktalar = gruplari_birlestir(gruplanmis_noktalar, 1)
# # print(birlesik_liste)
# print(bas_ve_son_noktalar)



def thread(_points, _grid_distance, _angle, _padding_distance, _is_inverted, done_event):
    global birlesik_liste_latlon, bas_ve_son_noktalar_latlon
    global grid_boyutu, aci, maksimum_izin_verilen_kenar_mesafesi

    noktalar = [latlon_to_utm(lat, lon) for lat, lon in _points]

    grid_boyutu = _grid_distance
    aci = -_angle
    maksimum_izin_verilen_kenar_mesafesi = _padding_distance

    ret = grid_noktalari_donustur_ve_kontrol_et(noktalar, grid_boyutu, aci, maksimum_izin_verilen_kenar_mesafesi)

    nokta_ciktisi = [tuple(nokta) for nokta in ret]
    mesafe_listesi = ard_ardaki_noktalar_arasi_mesafe(nokta_ciktisi)
    gruplanmis_noktalar = gruplandir(nokta_ciktisi, mesafe_listesi, grid_boyutu + 0.2)
    birlesik_liste, bas_ve_son_noktalar = gruplari_birlestir(gruplanmis_noktalar, _is_inverted)

    birlesik_liste_latlon = [utm_to_latlon(x, y) for x, y in birlesik_liste]
    bas_ve_son_noktalar_latlon = [utm_to_latlon(x, y) for x, y in bas_ve_son_noktalar]

    done_event.set()


def request_create_mission_from_point_list(points, grid_distance, angle, padding_distance, is_inverted):
    global birlesik_liste_latlon, bas_ve_son_noktalar_latlon, done_event

    done_event = threading.Event()

    t = threading.Thread(target=thread, args=(points, grid_distance, angle, padding_distance, is_inverted, done_event))
    t.start()
    # t.join()
    # global grid_boyutu, aci, maksimum_izin_verilen_kenar_mesafesi
    #
    # noktalar = [latlon_to_utm(lat, lon) for lat, lon in points]
    #
    # grid_boyutu = grid_distance
    # aci = -angle
    # maksimum_izin_verilen_kenar_mesafesi = padding_distance
    #
    # ret = grid_noktalari_donustur_ve_kontrol_et(noktalar, grid_boyutu, aci, maksimum_izin_verilen_kenar_mesafesi)
    #
    #
    # nokta_ciktisi = [tuple(nokta) for nokta in ret]
    # mesafe_listesi = ard_ardaki_noktalar_arasi_mesafe(nokta_ciktisi)
    # gruplanmis_noktalar = gruplandir(nokta_ciktisi, mesafe_listesi, grid_boyutu + 0.2)
    # birlesik_liste, bas_ve_son_noktalar = gruplari_birlestir(gruplanmis_noktalar, is_inverted)
    #
    #
    # birlesik_liste_latlon = [utm_to_latlon(x, y) for x, y in birlesik_liste]
    # bas_ve_son_noktalar_latlon = [utm_to_latlon(x, y) for x, y in bas_ve_son_noktalar]

    # return birlesik_liste_latlon, bas_ve_son_noktalar_latlon



def is_auto_mission_planned():

    return done_event.is_set()

# ret = grid_noktalari_donustur_ve_kontrol_et(noktalar, grid_boyutu, aci, maksimum_izin_verilen_kenar_mesafesi)
# nokta_ciktisi = [tuple(nokta) for nokta in ret]
# mesafe_listesi = ard_ardaki_noktalar_arasi_mesafe(nokta_ciktisi)
# gruplanmis_noktalar = gruplandir(nokta_ciktisi, mesafe_listesi)
# birlesik_liste, bas_ve_son_noktalar = gruplari_birlestir(gruplanmis_noktalar, 0)
#
#
# # Grafik çizimi
# plt.figure()
# noktalar.append(noktalar[0])
# x, y = zip(*noktalar)
# plt.plot(x, y, 'ro-')  # Çokgenin köşe noktaları
# # x, y = zip(*nokta_ciktisi)
# # plt.plot(x, y, 'bo-')  # İçerideki grid noktaları
# x, y = zip(*bas_ve_son_noktalar)
# plt.plot(x, y, 'bo-')  # İçerideki grid noktaları
# # x, y = zip(*birlesik_liste)
# # plt.plot(x, y, 'yo-')  # İçerideki grid noktaları
#
# plt.grid(True)
# plt.show()
