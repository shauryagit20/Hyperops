import threading
import tkinter as tk
import tkinter.font as font
import sys
import time
import socket
import tkinter.font as font
from tkinter import Text, ttk
import tkinter.messagebox
import requests
PORT =  11234
HEADER_PORTAL_PASSENGERS = 30
Socket =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Socket.connect(("192.168.1.31",1981))
BASE_URL= "http://127.0.0.1:5657"

class UI:

    def __init__(self) -> None: #Constructor
        self.window_width = 1700
        self.window_height = 900
        self.selected_box = []
        self.wordFont = None
        self.Number_Of_Passengers = 0
        self.podCheckboxes = {}
        self.Platform_Number_Passenger_Number_hash ={}
        self.Time_Label = {}
        self.Status_Label = {}
        self.Empty_Spaces = 100
        self.mainCheckbox = None
        self.passenger_label = {}
        self.Platform_Count_Label = {}
        self.platformCheckboxes = [None, None, None, None, None, None, None, None, None, None, None, None, None]


        self.Taxi_Count_Value = 100
        self.Passenger_Portal_thread =  threading.Thread(target=self.Update_Passenger_Count)
        self.Button_Dict = {}

    def main(self): #Main method
        self.visuals()

    def visuals(self): #Visuals of the operator system
        root = tk.Tk()
        root.configure(bg='black')
        root.title('Hyperloop : Mumbai')
        root.geometry(f'{self.window_width}x{self.window_height}')
        root.resizable(False, False)
        # root.iconbitmap('./Images/hyper1.ico')

        self.wordFont = font.Font(family = 'Arial', size =10)

        broadcast_button = tk.Button(root, text = "BROADCAST", bg="red", fg="white", height = 2, width = 20, font = self.wordFont, command = lambda : self.broadcast())
        broadcast_button.place(x=1510,y=750)
        self.passenger_count_label =  tk.Label(root,text=f"Total number of passengers in the portal -  {self.Number_Of_Passengers}",fg="white",bg = "black",font=("Arial",15))
        self.passenger_count_label.place(x = 500,y =  845)
        Taxi_Count_Label =  tk.Label(root,text = "Number of Taxis " ,  bg = "black",fg = "white",font= ("Arial",17))
        Taxi_Count_Label.place(x = 1505, y = 220 )
        self.Taxi_Count_Value_Label =  tk.Label(root,text=f"{self.Taxi_Count_Value}",bg = "black",fg = "white",font =  ("Arial",40))
        self.Taxi_Count_Value_Label.place(x = 1540,y = 260)
        Parking_Space_Label =  tk.Label(root,text="Occupied Parking spaces",bg = "black", fg = "white",font=("Arial",12))
        Parking_Space_Label.place(x = 1495,y=380 )
        self.Parking_Space_Count =  tk.Label(root,text = f"{self.Empty_Spaces}",bg = "black",fg = "white",font =  ("Arial",40))
        self.Parking_Space_Count.place(x  = 1540,y = 420)
        canvas = tk.Canvas(root)
        canvas.config(height=600, width=1066,bg="black",highlightthickness=0)
        canvas.place(x=60,y=55)
        self.rectangles(canvas)
        self.Passenger_Portal_thread.start()
        root.mainloop()

    def Update_Passenger_Count(self):
        while True:
            sendMessage =  "TotalPassengers".encode()
            Socket.send(sendMessage)
            msg =  Socket.recv(30).decode()
            while msg:
                msg =  msg.strip()
                self.Number_Of_Passengers = int(msg)
                self.passenger_count_label.config(text  = f"Total number of passengers in the portal -  {self.Number_Of_Passengers}")
                time.sleep(0.1)
                break

    def rectangles(self, canvas):
        for i in range(13):
            Platform_Label = tk.Label(canvas, text=f"{i+1}", fg="white", bg="black")
            Platform_Label.grid(row=1, column=i, pady=3, padx=6)
            Passenger_Number_Label = tk.Label(canvas,text = f"Passengers:28", fg="white", bg="black")
            Passenger_Number_Label.grid(row = 2, column=i, pady=3, padx=6)
            self.Platform_Count_Label[f"Platform{i+1}"] =  Passenger_Number_Label
            for j in range(2,8):
                bt = tk.Button(canvas,bg = "red", height=5, width=4)
                self.Button_Dict[f"{j-2}X{i}"] = bt
                bt.grid(row=j+1, column=i, pady=3, padx=6)
            status_label = tk.Label(canvas, text="INCOMING", fg="white", bg="black")
            status_label.grid(row = j+10, column=i,pady=3, padx=6)
            time_label =  tk.Label(canvas,text="1:00",fg =  "white",bg = "black")
            self.Time_Label[f"Platform{i+1}"] =  time_label
            self.Status_Label[f"Platform{i+1}"] =  status_label
            time_label.grid(row=j+11,column =i,pady =3,padx = 6)

        pod_manager_thread = threading.Thread(target =  self.pod_manager)
        pod_manager_thread.start()
        status_manager_thread = threading.Thread(target =  self.status_time_manager)
        status_manager_thread.start()
        Platform7_manager_thread = threading.Thread(target=self.platform_7_manager)
        Platform7_manager_thread.start()
        t3 = threading.Thread(target=self.Vechicle_Manager)
        t3.start()
        t4 = threading.Thread(target=self.platform_1_passenger_count)
        t4.start()

    def pod_manager(self):
        while True:
            layout =  requests.get(f"{BASE_URL}/HStatus").json()["Data"]
            print(layout)
            for i in range(len(layout)):
                for j in range(len(layout[i])):
                    if(layout[i][j] == 1):
                        self.Button_Dict[f"{i}X{j}"].config(bg = "#399f14")
                    elif(layout[i][j] ==  0):
                        self.Button_Dict[f"{i}X{j}"].config(bg="#ef9b04")
                    else:
                        self.Button_Dict[f"{i}X{j}"].config(bg = "red")
            time.sleep(1)


    def status_time_manager(self):
        while True:
            status =  requests.get(f"{BASE_URL}/PStatus").json()["Data"]
            for keys in status:
                if(keys!="Platform7"):
                    self.Time_Label[keys].config(text = str(status[keys]["Time_Left"]))
                    if(status[keys]["status"] ==  "Boarding"):
                        self.Status_Label[keys].config(text = "BOARDING",  fg =  "yellow")
                    elif(status[keys]["status"] ==  "Docking"):
                        self.Status_Label[keys].config(text = "DOCKING", fg = "#FFA500")
                    elif(status[keys]["status"] == "Exiting"):
                        self.Status_Label[keys].config(text="EXITING", fg="red")
                    elif(status[keys]["status"] == "Incoming"):
                        self.Status_Label[keys].config(text = "INCOMING",fg = "green")
            time.sleep(1)

    def Vechicle_Manager(self):
        while True:
            vehicle_data = requests.get("http://127.0.0.1:5000/GetVech/Temp").json()
            print(vehicle_data)
            No_of_Cars = vehicle_data["Car"]
            No_of_Cabs = vehicle_data["Cab"]
            self.Parking_Space_Count.config(text=str(No_of_Cars))
            self.Taxi_Count_Value_Label.config(text =  str(No_of_Cabs))
            time.sleep(1)


    def broadcast(self):
        bc = tk.Tk()
        self.Selected_Time = tk.StringVar(bc)
        self.Selected_Time.set("Please select the time...")
        bc.title('Broadcast : Mumbai')
        bc.config(bg = "black")
        bc.resizable(False,False)
        bc.geometry(f'{self.window_width}x{self.window_height}')
        canvas = tk.Canvas(bc)
        canvas.config(height=600, width=1066, bg="black", highlightthickness=0)
        canvas.place(x=100, y=65)
        button_send_broadcast =  tk.Button(bc, text = "Send Broadcast",command=lambda:self.send_broadcast(), bg =  "green",width=16, height=2,borderwidth=0)
        button_send_broadcast.place(x=620, y=800)
        select_all = tk.Button(bc, text = "Select All",command=lambda:self.select_all(),bg =  "yellow",width=10, height=2,borderwidth=0)
        select_all.place(x=450, y=800)
        Label_Message =  tk.Label(bc,text = "Enter your message",fg = "white",bg = "black")
        Label_Message.place(x= 1200,y = 60)
        self.text_box = tk.Text(bc,height =  40, width =  80,bg = "#ADD8E6")
        self.text_box.place(x = 1200,y = 100)
        l =  requests.get("http://127.0.0.1:5000/"+"Timings/0").json()["data"]
        Option_Menu_Time_Selection = tk.OptionMenu(bc,self.Selected_Time,*l)
        Option_Menu_Time_Selection.place(x =  1400, y = 60)
        self.rectangles_2(canvas)
        bc.mainloop()

    def select_all(self):
        for i in range(13):
            for j in range(2, 8):
                if (f"{i}X{j - 2}" not in self.selected_box):
                    self.podCheckboxes[f"{i + 1}X{j - 2}"].config(bg="red")
                    self.selected_box.append(f"{i}X{j - 2}")
                    print(self.selected_box)

    def rectangles_2(self, canvas):
        print("In here")
        for i in range(13):
            for j in range(2, 8):
                Platform_Label = tk.Label(canvas, text=f"{i + 1}", fg="white", bg="black")
                Platform_Label.grid(row=1, column=i, pady=3, padx=6)
                bt = tk.Button(canvas, bg="green", height=5, width=4,command = lambda row = i, col =  j: self.select_button(row,col))
                self.podCheckboxes[f"{i+1}X{j-2}"] =  bt
                bt.grid(row=j + 1, column=i, pady=5, padx=12)

    def select_button(self,i,j):
        print(f"The value of i is {i}")
        print(f"The value of j is {j}")
        if(f"{i}X{j-2}" not in self.selected_box ):
            self.podCheckboxes[f"{i+1}X{j-2}"].config(bg = "red")
            self.selected_box.append(f"{i}X{j-2}")
            print(self.selected_box)
        elif(f"{i}X{j-2}" in self.selected_box):
            self.podCheckboxes[f"{i + 1}X{j - 2}"].config(bg="green")
            self.selected_box.remove(f"{i}X{j - 2}")
            print(self.selected_box)

    def send_broadcast(self):
        print(f"Sending Broadcast")
        BASE_URL_2 = "http://127.0.0.1:5550"
        s = ",".join(self.selected_box)
        inp = self.text_box.get(1.0, "end-1c")
        print(inp)
        if(self.Selected_Time.get() ==  "Please select the time..."):
            tkinter.messagebox.showerror(title="Date Selection Error",message =  "Please select the time")
        try:
            out =  requests.post(f"{BASE_URL_2}/BroadCast/{s}/{self.Selected_Time.get()}/{inp}")
            print(out)
        except:
            print("Error")

    def platform_7_manager(self):
        while True:
            status =  requests.get(f"{BASE_URL}/PStatus").json()["Data"]

            platform_7_status = status["Platform7"]
            print(platform_7_status)

            for keys in platform_7_status:
                print(keys)
                d = platform_7_status[keys]
                print(d)
                print(type(d))
                Platform_number = d["Platform"]
                print(f"Platform: {Platform_number}")
                Time =  platform_7_status[keys]["Time_Left"]
                self.Button_Dict[keys].config(text = f"{Platform_number}\n{Time}",justify = tk.LEFT)
            time.sleep(1)

    def platform_1_passenger_count(self):
        while True:
            p1 =  self.Platform_Count_Label["Platform1"]
            try:
                Noo = requests.get("http://127.0.0.1:5000/GetPassengers/1").json()["Passengers"]
            except:
                Noo = 100
            p1.config(text = f"Passengers:{Noo}")
            time.sleep(1)


#
# while True:
#     layout =  requests.get(f"{BASE_URL}/").json()
#     print(layout)
#     break

obj = UI()
obj.main()
