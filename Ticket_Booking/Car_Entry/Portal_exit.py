import tkinter as tk
import os
import json

import requests


class Portal_exit:

    def __init__(self):
        self.cwd = os.getcwd()

    def gui(self):
        self.root = tk.Tk()
        root = self.root
        self.Veh_exit = tk.StringVar()
        root.geometry("510x400")
        root.title("Hyperloop Portal")
        root.config(bg="#ADD8E6")
        heading = tk.Label(root, text="PORTAL EXIT", font=('Helvetica', 25))
        heading.config(bg="#ADD8E6")
        heading.place(x=150, y=18)

        vehicle_no = tk.Label(root, text="Enter the vehicle number: ", font=('Helvetica', 12))
        vehicle_no.config(bg="#ADD8E6")
        vehicle_no.place(x=170, y=150)
        vehicle_exit = tk.Entry(root, textvariable=self.Veh_exit, width=30)
        vehicle_exit.place(x=170, y=190)

        Exit_btn = tk.Button(root, text="EXIT", width=7, command=lambda : self.entry_successful())
        Exit_btn.place(x=230, y=330)
        self.root.mainloop()

    def entry_successful(self):
        print("In here")
        vech_type = str(self.Veh_exit.get())
        requests.post(f"http://127.0.0.1:5000/CarExit/{vech_type}")


Portal_exit().gui()