# Import the required module for text
# to speech conversion
from gtts import gTTS
import playsound

# This module is imported so that we can
# play the converted audio
# import os
#
# The text that you want to convert to audio
# mytext = 'hh'
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
# myobj.save("voices\\test.mp3")

# Playing the converted file
# os.system("welcome.mp3")
# playsound.playsound("voices\\test_telem_recovered_0.5saniye.mp3")


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


import matplotlib.pyplot as plt
import numpy as np
import time

# Veri dizisi
data = np.random.rand(10)

# Interaktif modu etkinleştir
plt.ion()

# Pencere boyutunu ayarla
fig, ax = plt.subplots(figsize=(12, 6))
line, = ax.plot(data)

# Güncelleme fonksiyonu
def update(new_data):
    # Yeni veri ekle
    global data
    data = np.append(data, new_data)

    # x ekseni için yeni bir indeks ekle
    x = np.arange(len(data))

    # Grafiği güncelle
    line.set_xdata(x)
    line.set_ydata(data)
    ax.relim()  # Yeniden sınırları hesapla
    ax.autoscale_view()  # Ölçeklendirmeyi otomatik ayarla
    fig.canvas.draw()  # Canvas'ı yeniden çiz
    fig.canvas.flush_events()  # Olayları işle

# For döngüsü ve time.sleep ile döngüyü yavaşlatma
for _ in range(1000):  # 100 kez döngü yap
    new_data_point = np.random.rand()
    update(new_data_point)
    time.sleep(0.1)  # Her iterasyonda 1 saniye bekle

# Interaktif modu kapat
plt.ioff()
plt.show()

