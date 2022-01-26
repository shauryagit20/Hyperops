import tkinter as tk
import os
import requests
import json

class Portal_entry:

    def __init__(self):
        self.cwd = os.getcwd()


    def gui(self):
        self.root = tk.Tk()
        root = self.root
        self.Choose_portal = tk.IntVar()
        self.Veh_entry = tk.StringVar()
        root.geometry("510x400")
        root.title("Hyperloop Portal")
        root.config(bg="#ADD8E6")
        heading = tk.Label(root, text="PORTAL ENTRY", font=('Helvetica', 25))
        heading.config(bg="#ADD8E6")
        heading.place(x=130, y=18)

        Select = tk.Label(root, text="Choose a Car or a Cab", font=('Helvetica', 12))
        Select.place(x=170, y=120)
        Select.config(bg="#ADD8E6")

        Car = tk.Radiobutton(root, text="Car", variable=self.Choose_portal, value=1)
        Car.config(bg="#ADD8E6")
        Car.place(x=190, y=150)

        Cab = tk.Radiobutton(root, text="Cab", variable=self.Choose_portal, value=2)
        Cab.config(bg="#ADD8E6")
        Cab.place(x=260, y=150)

        vehicle_no = tk.Label(root, text="Enter the vehicle number: ", font=('Helvetica', 12))
        vehicle_no.config(bg="#ADD8E6")
        vehicle_no.place(x=170, y = 220)
        vehicle_entry = tk.Entry(root, textvariable=self.Veh_entry, width=30)
        vehicle_entry.place(x=150, y=250)

        Entry_btn = tk.Button(root, text= "ENTRY", width = 7, command=lambda: self.entry_successful())
        Entry_btn.place(x=230, y= 330)
        self.root.mainloop()

    def entry_successful(self):
        print("In here")
        vech_type =  self.Choose_portal.get()
        if(vech_type ==  1):
            vech_type =  "Car"
        else:
            vech_type = "Cab"
        print(vech_type)
        requests.post(f"http://127.0.0.1:5000/CarEntry/{vech_type}/{str(self.Veh_entry.get())}")


Portal_entry().gui()