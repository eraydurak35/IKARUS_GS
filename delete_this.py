# Import the required module for text
# to speech conversion
# from gtts import gTTS
# import playsound

# # This module is imported so that we can
# # play the converted audio
# import os
#
# # The text that you want to convert to audio
# mytext = 'gnss fix established'
#
# # Language in which you want to convert
# language = 'en'
#
# # Passing the text and language to the engine,
# # here we have marked slow=False. Which tells
# # the module that the converted audio should
# # have a high speed
# myobj = gTTS(text=mytext, lang=language, slow=False)
#
#
# # Saving the converted audio in a mp3 file named
# # welcome
# myobj.save("voices\\gnss_fix_established.mp3")
#
# # Playing the converted file
# # os.system("welcome.mp3")
# playsound.playsound("voices\\gnss_fix_established.mp3")


# from PIL import Image
# import math
#
# # Orijinal ikonun yüklenmesi
# icon = Image.open('kaynak_foto.png')
#
# # Yeni görsellerin boyutları
# new_size = (1024, 1024)
#
# # Merkezi bulmak için
# center = tuple([x // 2 for x in new_size])
#
# # 18 adet döndürülmüş kopya oluşturmak için döngü
# for i in range(36):
#     # Döndürme açısı
#     angle = (i * 10)
#
#     # Döndürülmüş görseli oluşturma
#     rotated = icon.rotate(angle, expand=True)
#
#     # Yeni bir görsel oluşturma ve ortalamak için
#     result = Image.new('RGBA', new_size, (0, 0, 0, 0))
#     result.paste(rotated, (center[0] - rotated.width // 2, center[1] - rotated.height // 2), rotated)
#
#     # Sonucu kaydetme
#     result.save(f'drone_pos_icon_{360 - angle}_deg.png')


# import tkinter as tk
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#
#
# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title('Tkinter Matplotlib Demo')
#
#         # Verileri hazırla
#         data = {'Python': 11.27, 'C': 11.16, 'Java': 10.46, 'C++': 7.5, 'C#': 5.26}
#         languages = list(data.keys())
#         popularity = list(data.values())
#
#         # Figür oluştur
#         figure = Figure(figsize=(6, 4), dpi=100)
#
#         # FigürCanvasTkAgg nesnesi oluştur
#         figure_canvas = FigureCanvasTkAgg(figure, self)
#
#         # Araç çubuğunu oluştur
#         NavigationToolbar2Tk(figure_canvas, self)
#
#         # Eksenleri oluştur
#         axes = figure.add_subplot()
#
#         # Bar grafiğini çiz
#         axes.bar(languages, popularity)
#         axes.set_title('En Popüler 5 Programlama Dili')
#         axes.set_ylabel('Popülerlik')
#
#         # Tkinter widget'ına figürü yerleştir
#         figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#
#
# if __name__ == '__main__':
#     app = App()
#     app.mainloop()


# import matplotlib.pyplot as plt
# import numpy as np
# import time
#
# # Veri dizisi
# data = np.random.rand(10)
#
# # Interaktif modu etkinleştir
# plt.ion()
#
# # Pencere boyutunu ayarla
# fig, ax = plt.subplots(figsize=(12, 6))
# line, = ax.plot(data)
#
# # Güncelleme fonksiyonu
# def update(new_data):
#     # Yeni veri ekle
#     global data
#     data = np.append(data, new_data)
#
#     # x ekseni için yeni bir indeks ekle     39.110908915217294, 27.187779046586474
#     x = np.arange(len(data))
#
#     # Grafiği güncelle
#     line.set_xdata(x)
#     line.set_ydata(data)
#     ax.relim()  # Yeniden sınırları hesapla
#     ax.autoscale_view()  # Ölçeklendirmeyi otomatik ayarla
#     fig.canvas.draw()  # Canvas'ı yeniden çiz
#     fig.canvas.flush_events()  # Olayları işle
#
# # For döngüsü ve time.sleep ile döngüyü yavaşlatma
# for _ in range(1000):  # 100 kez döngü yap
#     new_data_point = np.random.rand()
#     update(new_data_point)
#     time.sleep(0.1)  # Her iterasyonda 1 saniye bekle
#
# # Interaktif modu kapat
# plt.ioff()
# plt.show()

#                                                                                  AUTO MISSION CODE START
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.path as mpath
# from shapely.geometry import Point, Polygon
#
#
# def en_uzak_noktalari_bul(noktalar):
#     max_mesafe = 0
#     for i, nokta1 in enumerate(noktalar):
#         for nokta2 in noktalar[i + 1:]:
#             mesafe = np.linalg.norm(np.array(nokta1) - np.array(nokta2))
#             if mesafe > max_mesafe:
#                 max_mesafe = mesafe
#     return max_mesafe
#
#
# def dondurme_matrisi_olustur(acı):
#     radian = np.deg2rad(acı)
#     return np.array([[np.cos(radian), -np.sin(radian)], [np.sin(radian), np.cos(radian)]])
#
#
# def kenara_olan_mesafeyi_hesapla(nokta, cokgen):
#     point = Point(nokta)
#     return cokgen.boundary.distance(point)
#
#
# def grid_noktalari_donustur_ve_kontrol_et(noktalar, grid_boyutu, acı, maksimum_izin_verilen_kenar_mesafesi):
#     # Çokgeni oluştur
#     cokgen = Polygon(noktalar)
#     path_cokgen = mpath.Path(noktalar)
#
#     # Gridin merkezini hesapla
#     grid_merkezi = ((max(noktalar, key=lambda x: x[0])[0] + min(noktalar, key=lambda x: x[0])[0]) / 2,
#                     (max(noktalar, key=lambda x: x[1])[1] + min(noktalar, key=lambda x: x[1])[1]) / 2)
#
#     # Döndürülmüş grid noktalarını içeren listeyi oluştur
#     icerideki_noktalar = []
#
#     expand_amount = en_uzak_noktalari_bul(noktalar)
#
#     # Çokgenin sınırlarını hesapla
#     min_x = min(noktalar, key=lambda x: x[0])[0] - expand_amount
#     max_x = max(noktalar, key=lambda x: x[0])[0] + expand_amount
#     min_y = min(noktalar, key=lambda x: x[1])[1] - expand_amount
#     max_y = max(noktalar, key=lambda x: x[1])[1] + expand_amount
#
#     # Grid boyutuna göre tüm noktaları kontrol et
#     x = min_x
#     while x <= max_x:
#         y = min_y
#         while y <= max_y:
#             # Noktayı grid merkezine göre döndür
#             nokta = np.array([x, y]) - grid_merkezi
#             dondurulmus_nokta = np.dot(dondurme_matrisi_olustur(acı), nokta) + grid_merkezi
#             if path_cokgen.contains_point(dondurulmus_nokta):
#                 # Çokgenin kenarına olan mesafeyi hesapla
#                 mesafe = kenara_olan_mesafeyi_hesapla(dondurulmus_nokta, cokgen)
#                 if mesafe >= maksimum_izin_verilen_kenar_mesafesi:
#                     icerideki_noktalar.append(dondurulmus_nokta)
#             y += grid_boyutu
#         x += grid_boyutu
#
#     return icerideki_noktalar
#
#
# # Örnek kullanım:
# noktalar = [(1.2, -25.0), (50.0, 25.0), (20.0, 50.0), (10.0, 45.0), (1.0, 35.0)]
# # noktalar = [(0.0, 0.0), (25.0, 0.0), (25.0, 25.0), (0.0, 25.0)]
# grid_boyutu = 1  # Kullanıcı tarafından belirlenecek grid boyutu
# aci = -0.0  # Döndürme açısı derece cinsinden
# maksimum_izin_verilen_kenar_mesafesi = 1.0  # Kullanıcının belirleyeceği maksimum kenar mesafesi
# ret = grid_noktalari_donustur_ve_kontrol_et(noktalar, grid_boyutu, aci, maksimum_izin_verilen_kenar_mesafesi)
#
# # Numpy array'leri tuple'a dönüştür
# nokta_ciktisi = [tuple(nokta) for nokta in ret]
#
#
# # print(nokta_ciktisi)
#
#
# def ard_ardaki_noktalar_arasi_mesafe(noktalar):
#     # Ardışık noktalar arasındaki mesafeleri hesapla
#     mesafeler = [np.linalg.norm(np.array(noktalar[i]) - np.array(noktalar[i + 1])) for i in range(len(noktalar) - 1)]
#     return mesafeler
#
#
# mesafe_listesi = ard_ardaki_noktalar_arasi_mesafe(nokta_ciktisi)
#
#
# # print(mesafe_listesi)
#
#
# def gruplandir(noktalar, mesafeler, max_mesafe=grid_boyutu + 0.1):
#     gruplar = []
#     mevcut_grup = [noktalar[0]]  # İlk noktayı ilk gruba ekle
#
#     # İlk noktadan başlayarak mesafeleri kontrol et
#     for i in range(1, len(noktalar)):
#         if mesafeler[i - 1] <= max_mesafe:
#             # Eğer mesafe max_mesafe'den küçük veya eşitse, noktayı mevcut gruba ekle
#             mevcut_grup.append(noktalar[i])
#         else:
#             # Eğer mesafe max_mesafe'den büyükse, mevcut grubu gruplar listesine ekle ve yeni grup oluştur
#             gruplar.append(mevcut_grup)
#             mevcut_grup = [noktalar[i]]
#
#     # Son grubu da gruplar listesine ekle
#     gruplar.append(mevcut_grup)
#     return gruplar
#
#
# # Örnek kullanım:
# gruplanmis_noktalar = gruplandir(nokta_ciktisi, mesafe_listesi)
# for grup in gruplanmis_noktalar:
#     pass
#     # print(grup)
#
#
# def gruplari_birlestir(gruplar, yonelim):
#     ana_liste = []
#     bas_ve_sonlar = []  # Her grubun ilk ve son noktalarını saklayacak liste
#
#     # Grupları sırayla ve bazılarını ters çevirerek ana listeye ekle
#     for i, grup in enumerate(gruplar):
#         if i % 2 == 0:
#
#             if yonelim == 0:
#
#                 # Çift indeksli gruplar (0, 2, 4, ...) olduğu gibi eklenecek
#                 ana_liste.extend(grup)
#                 # Grubun ilk ve son noktalarını bas_ve_sonlar listesine ekle
#                 if grup:  # Grup boş değilse
#                     bas_ve_sonlar.append(grup[0])
#                     bas_ve_sonlar.append(grup[-1])
#
#             else:
#                 # Tek indeksli gruplar (1, 3, 5, ...) ters çevrilerek eklenecek
#                 grup_ters = list(reversed(grup))
#                 ana_liste.extend(grup_ters)
#                 # Ters çevrilmiş grubun ilk ve son noktalarını bas_ve_sonlar listesine ekle
#                 if grup_ters:  # Grup boş değilse
#                     bas_ve_sonlar.append(grup_ters[0])
#                     bas_ve_sonlar.append(grup_ters[-1])
#         else:
#
#             if yonelim == 0:
#
#                 # Tek indeksli gruplar (1, 3, 5, ...) ters çevrilerek eklenecek
#                 grup_ters = list(reversed(grup))
#                 ana_liste.extend(grup_ters)
#                 # Ters çevrilmiş grubun ilk ve son noktalarını bas_ve_sonlar listesine ekle
#                 if grup_ters:  # Grup boş değilse
#                     bas_ve_sonlar.append(grup_ters[0])
#                     bas_ve_sonlar.append(grup_ters[-1])
#             else:
#
#                 # Çift indeksli gruplar (0, 2, 4, ...) olduğu gibi eklenecek
#                 ana_liste.extend(grup)
#                 # Grubun ilk ve son noktalarını bas_ve_sonlar listesine ekle
#                 if grup:  # Grup boş değilse
#                     bas_ve_sonlar.append(grup[0])
#                     bas_ve_sonlar.append(grup[-1])
#
#     return ana_liste, bas_ve_sonlar
#
#
# birlesik_liste, bas_ve_son_noktalar = gruplari_birlestir(gruplanmis_noktalar, 1)
# # print(birlesik_liste)
# print(bas_ve_son_noktalar)
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



#                                                                                  AUTO MISSION CODE END






#
# from pyproj import Proj, Transformer
# import numpy as np
# # WGS84 (enlem/boylam) projeksiyon tanımı
# wgs84 = Proj('epsg:4326')
#
# # İzmir için UTM projeksiyon tanımı
# utm_izmir = Proj('epsg:32637') # İzmir'i kapsayan UTM bölgesi
#
# # Transformer sınıfını kullanarak dönüşüm
# transformer = Transformer.from_crs("epsg:4326", "epsg:32637", always_xy=True)
#
# # Enlem ve boylamdan UTM'ye dönüşüm
# def latlon_to_utm(lat, lon):
#     x, y = transformer.transform(lon, lat)
#     return x, y
#
# # UTM'den enlem ve boylama dönüşüm
# def utm_to_latlon(x, y):
#     lon, lat = transformer.transform(x, y, direction='INVERSE')
#     return lat, lon
#
# # Örnek enlem ve boylam listesi
# coordinates = [(39.11090067918387, 27.187865238566637), (39.110465503745225, 27.187941199640594)] # İzmir koordinatları
#
# # Kartezyen koordinatlara dönüştürme
# utm_coordinates = [latlon_to_utm(lat, lon) for lat, lon in coordinates]
# print("utm??: ", utm_coordinates)
# # İşlemlerden sonra...
# # ... işlemlerinizi burada yapın ...
#
# dist = np.linalg.norm(np.array(utm_coordinates[0]) - np.array(utm_coordinates[1]))
# print("dist: ", dist)
# # Sonra tekrar enlem ve boylama dönüştürme
# latlon_coordinates = [utm_to_latlon(x, y) for x, y in utm_coordinates]
# print("latlon??: ", latlon_coordinates)
















































# import tkinter as tk
# from tkinter import filedialog
#
# root = tk.Tk()
# root.withdraw()
#
# file_path = filedialog.asksaveasfilename(
#     defaultextension=".txt",
#     filetypes=[("Veri Dosyaları", "*.json"), ("Tüm Dosyalar", "*.*")]
# )
# print(f"Kaydedilecek dosya yolu: {file_path}")
#
#
#
#
# import json
#
# # Kaydedilecek veriler
# waypoints_json_data = {
#     'waypoints': [],
#     'field_points': [],
#     'altitudes': [],
#     'rth_after_mission': False,
#     'land_after_mission': False,
#     'auto_mission_angle': 0.0,
#     'auto_mission_spacing': 0.0,
#     'auto_mission_padding': 0.0,
#     'auto_mission_reverse': False,
#     'auto_mission_invert': False,
# }
#
#
#
# waypoints = [(39.1108671997783, 27.187541607977316), (39.11126892626414, 27.187518946555386), (39.112010731097094, 27.187545680917722), (39.110858877985166, 27.187610658091614), (39.11085055614758, 27.187679708199344), (39.112011297227475, 27.187614230826522), (39.11201186331666, 27.18768278074664), (39.110840456713724, 27.18774885856492), (39.11083213478692, 27.18781790865766), (39.112014206916655, 27.18775123040456), (39.11201477292378, 27.187819780349056), (39.110823812815674, 27.18788695874383), (39.11081549079997, 27.187956008823424), (39.11201533888972, 27.18788833030486), (39.112017682367416, 27.187956780003695), (39.11080716873983, 27.188025058896443), (39.11079884663525, 27.188094108962886), (39.11201824825128, 27.188025329983873), (39.11201881409395, 27.188093879975366), (39.11079052448621, 27.188163159022746), (39.11078220229272, 27.18823220907604), (39.11202115744936, 27.188162329715116), (39.11202172320996, 27.18823087973098), (39.110772102500356, 27.18830135937252), (39.11076378021766, 27.188370409410823), (39.112022288929374, 27.188299429758157), (39.112024632162516, 27.188367879538816), (39.1107554578905, 27.188439459442552), (39.110747135518906, 27.188508509467702), (39.11202519779986, 27.188436429590364), (39.11202576339602, 27.188504979653224), (39.11073881310286, 27.188577559486284), (39.11073049064238, 27.188646609498278), (39.11202810650686, 27.188573429474797), (39.11202867202095, 27.18864197956203), (39.11072216813745, 27.188715659503696), (39.11071206803134, 27.188784809739477), (39.112029237493836, 27.188710529660572), (39.112029802925534, 27.188779079770423), (39.110703745437185, 27.188853859729917), (39.110695422798585, 27.18892290971377), (39.112032145873215, 27.188847529645965), (39.11203271122285, 27.18891607978019), (39.11068710011554, 27.188991959691045), (39.11067877738805, 27.189061009661746), (39.11203327653128, 27.188984629925724), (39.11203561935669, 27.189053079842175), (39.11067045461611, 27.189130059625867), (39.11066213179972, 27.18919910958341), (39.11203618458306, 27.189121630012075), (39.11203674976824, 27.189190180193293), (39.11066091917489, 27.189267758637747), (39.11105254711263, 27.189314258142716), (39.11203909247136, 27.18925863015065), (39.11203965757446, 27.18932718035623), (39.111444175140676, 27.189360757632706), (39.11183580325907, 27.189407257107735), (39.11204022263638, 27.189395730573125)]
# field_points = [(39.11203653798363, 27.187484592590295), (39.11084610254707, 27.187484592590295), (39.11062133276029, 27.189297765884362), (39.11206983658785, 27.189469427261315)]
#
#
# waypoints_json_data["waypoints"] = waypoints
# waypoints_json_data["field_points"] = field_points
#
# # Verileri JSON dosyasına yazma
# with open(file_path, 'w', encoding='utf-8') as f:
#     json.dump(waypoints_json_data, f, ensure_ascii=False, indent=4)
#
#
#
#
# # import tkinter as tk
# # from tkinter import filedialog
#
# # root = tk.Tk()
# root.withdraw()
#
# file_path = filedialog.askopenfilename(
#     filetypes=[("Veri Dosyaları", "*.json")]
# )
# print(f"Seçilen dosya yolu: {file_path}")
#
#
#
# # import json
#
# # JSON dosyasını okuma
# with open(file_path, 'r', encoding='utf-8') as f:
#     okunan_veri = json.load(f)
#
# print(okunan_veri["waypoints"])
# print(okunan_veri["field_points"])


