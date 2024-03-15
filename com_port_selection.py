from tkinter import END
import customtkinter
import tkinter
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
selected_port = ""


def start():
    def refresh_com_ports_callback():
        global ports, selected_port
        selected_port = ""
        ok_button.configure(state="disabled")
        listbox.delete(0, END)
        ports = serial.tools.list_ports.comports()

        for item in ports:
            listbox.insert(ports.index(item), item.name)

    def ok_button_callback():
        root.quit()
        root.destroy()

    def listbox_select(event):
        global selected_port, ports
        if listbox.size() > 0:
            selected_port = ports[listbox.curselection()[0]].name
            ok_button.configure(state="normal")

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("350x350")
    root.title("STARLING Ground Station (COM Port Selection)")
    root.resizable(False, False)
    # root.iconbitmap("UAV_Project_LOGO_icon.ico")
    frame = customtkinter.CTkFrame(master=root, width=300, height=300, corner_radius=10)

    menu_title = customtkinter.CTkLabel(master=frame, text="Select COM Port", corner_radius=10, text_color="white",
                                        font=("arial", 20))

    refresh_button = customtkinter.CTkButton(master=frame, text="Refresh", command=refresh_com_ports_callback,
                                             border_width=0,
                                             corner_radius=8)

    ok_button = customtkinter.CTkButton(master=frame, text="Select", command=ok_button_callback, border_width=0,
                                        corner_radius=8, state="disabled")

    listbox = tkinter.Listbox(master=frame, width=45, height=5, font=("arial", 8, "bold"), bg="black", bd=5,
                              fg="white", selectmode="single", yscrollcommand="True")

    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    menu_title.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
    refresh_button.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
    listbox.place(relx=0.45, rely=0.55, anchor=tkinter.CENTER, x=15, y=15)
    ok_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
    listbox.bind("<<ListboxSelect>>", listbox_select)
    refresh_com_ports_callback()

    root.mainloop()
