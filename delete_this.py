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


from PIL import Image
import math

# Orijinal ikonun yüklenmesi
icon = Image.open('kaynak_foto.png')

# Yeni görsellerin boyutları
new_size = (1024, 1024)

# Merkezi bulmak için
center = tuple([x // 2 for x in new_size])

# 18 adet döndürülmüş kopya oluşturmak için döngü
for i in range(36):
    # Döndürme açısı
    angle = (i * 10)

    # Döndürülmüş görseli oluşturma
    rotated = icon.rotate(angle, expand=True)

    # Yeni bir görsel oluşturma ve ortalamak için
    result = Image.new('RGBA', new_size, (0, 0, 0, 0))
    result.paste(rotated, (center[0] - rotated.width // 2, center[1] - rotated.height // 2), rotated)

    # Sonucu kaydetme
    result.save(f'drone_pos_icon_{360 - angle}_deg.png')
