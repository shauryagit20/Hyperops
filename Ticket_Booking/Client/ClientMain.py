import time
import tkinter as tk
import threading
import tkinter.messagebox
import requests
from sys import exit


class Ticket_Booking_Screen():
    def __init__(self):
        self.root = tk.Tk()
        self.Number_of_Passengers = tk.IntVar()
        self.Number_of_Passengers.set(1)
        self.Prev_Number_of_passengers = 0
        self.Passenger_Names = []
        self.Name_Entry_Label_References = []
        self.y_initial = 170
        self.Phone_no =  tk.IntVar()
        self.Phone_no.set(12345567890)
        self.Selected_Passengers = []
        self.Selected_Time =  tk.StringVar()
        self.BASE =  "http://127.0.0.1:5000/ "

    def Book_Ticket(self):
        temp_list = []

        for Passengers in self.Passenger_Names:
            temp_list.append(Passengers.get())

        string_list_passengers = ",".join(temp_list)
        print(self.Selected_Time.get())
        request = requests.post(f"http://127.0.0.1:5000/BookTicket/{string_list_passengers}/{self.Selected_Time.get()}/{self.Phone_no.get()}")
        print(request.json())

    def UI(self):
        root = self.root
        root.geometry("1020x980")
        root.config(bg = "#87ceeb")

        Title = tk.Label(root, text="Ticket Booking", font=("Helvetica", 40), bg= "#87ceeb")
        Title.pack(pady=10)

        Number_of_passengers_label = tk.Label(root, text="Number of passengers", font=("Calibra", 14), bg = "#87ceeb")
        Number_of_passengers_label.place(x=30, y=120)

        Number_of_passengers_entry = tk.Entry(root, textvariable=self.Number_of_Passengers)
        Number_of_passengers_entry.place(x=270, y=120)

        labelCreatorThread =  threading.Thread(target=self.labelCreator)
        labelCreatorThread.start()

        Book_Button =  tk.Button(root,text="Book Ticket",font=("Helvetica",14,"bold"),command = lambda:self.Book_Ticket())
        Book_Button.place(x = 880 ,  y =  900)

        root.mainloop()


    def labelCreator(self):
        while True:
            try:
                if(self.Number_of_Passengers.get()<=8):
                    if(self.Prev_Number_of_passengers!=int(self.Number_of_Passengers.get())):
                        self.Prev_Number_of_passengers = self.Number_of_Passengers.get()
                        self.Passenger_Names = [tk.StringVar() for Passengers in range(self.Number_of_Passengers.get())]
                        for objects in self.Name_Entry_Label_References:
                            objects.destroy()

                        self.y_initial =  170
                        self.Name_Entry_Label_References = []
                        print("Calling Function")
                        Time_Periods =  requests.get("http://127.0.0.1:5000/"+"Timings/1").json()["data"]
                        print(Time_Periods)
                        for Passengers in range(self.Number_of_Passengers.get()):
                            root = self.root
                            Name_Label = tk.Label(root, text=f"Name of Passenger {Passengers+1}  ", font=("Calibra", 14), bg = "#87ceeb")
                            Name_Entry = tk.Entry(root, textvariable=self.Passenger_Names[Passengers])

                            Name_Label.place(x=30, y=self.y_initial)
                            Name_Entry.place(x=270, y=self.y_initial)

                            self.Name_Entry_Label_References.append(Name_Label)
                            self.Name_Entry_Label_References.append(Name_Entry)
                            self.y_initial += 50
                        time.sleep(0.01)
                        Phone_no_label = tk.Label(self.root, text="Phone Number", font=("Calibra", 14), bg="#87ceeb")
                        Phone_no_Entry = tk.Entry(self.root, textvariable=self.Phone_no)

                        Phone_no_label.place(x=30, y=self.y_initial)
                        Phone_no_Entry.place(x=270, y=self.y_initial)

                        Option_Menu_Label =  tk.Label(self.root,text="Time - " ,font=("Calibra", 14), bg="#87ceeb")
                        Option_Menu_Label.place(x =  30, y =  self.y_initial + 50)

                        Option_Menu  =  tk.OptionMenu(self.root,self.Selected_Time,*Time_Periods)
                        Option_Menu.place(x =  270, y =  self.y_initial + 50)

                        self.Name_Entry_Label_References.append(Phone_no_Entry)
                        self.Name_Entry_Label_References.append(Phone_no_label)

                        self.Name_Entry_Label_References.append(Option_Menu_Label)
                        self.Name_Entry_Label_References.append(Option_Menu)


                else:
                    tkinter.messagebox.showinfo("INFORMATION", "Hey there, \nAt max there can be 8 passengers. ")
                    self.Number_of_Passengers.set(1)
                    time.sleep(0.01)
            except:
                pass
            time.sleep(0.011)

Ticket_Booking_Screen().UI()
