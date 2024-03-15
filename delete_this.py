import tkinter as tk
from tkinter import messagebox

def create_dialog():
    response = messagebox.askyesnocancel("Dialog", "Devam etmek istiyor musunuz?")
    if response == True:
        print("Evet seçildi.")
    elif response == False:
        print("Hayır seçildi.")
    else:
        print("Çıkış yapıldı.")

root = tk.Tk()
button = tk.Button(root, text="Dialog Pencereyi Aç", command=create_dialog)
button.pack()

root.mainloop()
