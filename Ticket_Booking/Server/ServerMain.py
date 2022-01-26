import datetime
import json
import Platfomr_Resetter

import requests
from dateutil import parser
from flask import Flask
from flask_restful import Api, Resource
import qrcode
import os
import sched, time
from PIL import Image,ImageDraw,ImageFont

app = Flask(__name__)
api = Api(app)
Port = 13412
ROOT_DIR = os.getcwd()
# def schedule():
#     Platfomr_Resetter.reset()


class Timings(Resource):
    def get(self, passengers):
        print("Function Called")
        return {"data": self.get_timings(passengers)}

    def get_timings(self, passengers):
        Timings_file = open("Timings.json")
        data = json.load(Timings_file)
        Available_Timings = []
        counter = 0
        hour = datetime.datetime.now().time().hour
        minute = datetime.datetime.now().time().minute
        for keys in data:
            try:
                key_start_time = keys.split("-")[0]
                # print(key_start_time)
                hour_key =  parser.parse(key_start_time).hour
                minute_key =  parser.parse(key_start_time).minute
                # print(hour_key)
                # print(minute_key)
                if(hour_key>=hour  and minute_key>minute):
                    if (data[keys]["Occupancy"] + passengers <= 168):
                        data[keys]["Occupancy"]+=passengers
                        Available_Timings.append(keys)
                        counter =  counter +  1

                if(counter ==  5):
                    break
            except:
                print(keys)
        return Available_Timings

class BookTicket(Resource):
    def post(self,list_of_passengers,ticket_booking_time,phone_no):
        list_of_passengers =  list(list_of_passengers.split(","))
        number_of_passengers =  len(list_of_passengers)
        data = json.load(open("Timings.json","r"))
        base =  data[ticket_booking_time]["Arrangement"]
        occupancy_pod_bay = {} #Dictionary for storing Platform number + Pod_bay and the number of seats leaft in key value pair
        occupancy_list = [] #List for storing the occupancy of the platforms
        
        for platforms in base:
            for pod_bays in base[platforms]:
                occupancy_pod_bay[str(platforms)+" " + str(pod_bays)] =  28 - base[platforms][pod_bays]
                occupancy_list.append(28 - base[platforms][pod_bays])

        occupancy_list.sort(reverse=True)
        data[ticket_booking_time]["Occupancy"]+=len(list_of_passengers)
        Seat_Arrangement = self.Seat_finder(occupancy_pod_bay,occupancy_list,list_of_passengers,data,ticket_booking_time)


        UID =  self.Save_Ticket_Data(Seat_Arrangement)
        self.Generate_Tickets(Seat_Arrangement,UID,ticket_booking_time,int(phone_no))
        request =  requests.post(f"http://127.0.0.1:5550/SendTicket/{int(UID)}/{int(phone_no)}")
        print(request)
        return Seat_Arrangement

    def Seat_finder(self,occupancy_pod_bay,occupancy_list,list_of_passengers,data,timing):
        List_of_platform_assigned = []
        list_of_left_passengers = list_of_passengers
        number_of_passengers_left =  len(list_of_left_passengers)
        Seat = {}
        while(number_of_passengers_left!=0):
            least_of_repeated_element =  None
            minimum_count =  len(List_of_platform_assigned)

            for ele in List_of_platform_assigned:
                r = List_of_platform_assigned.count(ele)
                if r< minimum_count:
                    minimum_count =  r
                    least_of_repeated_element =  ele

            if(least_of_repeated_element!=None):
                d_id = self.create_dictionary(occupancy_pod_bay,least_of_repeated_element)
            else:
                d_id =  occupancy_pod_bay

            for podbays in d_id:
                if(d_id[podbays]>=number_of_passengers_left):
                    for passengers in range(number_of_passengers_left):
                        Seat[list_of_left_passengers[passengers]] = podbays
                        List_of_platform_assigned.append(podbays)
                    list_of_left_passengers  = list_of_left_passengers[number_of_passengers_left::]
                    number_of_passengers_left =  len(list_of_left_passengers)
                    break
                else:
                    number_of_passengers_left = number_of_passengers_left - 1
        print(data)
        for ele in List_of_platform_assigned:
            data[timing]["Arrangement"][ele[:-1:].strip()][ele[-1]]+=1
        print(List_of_platform_assigned)
        with open('Timings.json', 'w') as f:
            json.dump(data, f)

        return Seat

    def create_dictionary(self,dictionary:dict,least_repeated_element):
        out_d = {}
        list_keys = list(dictionary.keys())
        upper_pointer =  list_keys.index(least_repeated_element)
        lower_pointer =  upper_pointer
        while(len(out_d)!=len(dictionary)):
            if(upper_pointer<11):
                upper_pointer =  upper_pointer+1
                out_d[list_keys[upper_pointer]] = dictionary[list_keys[upper_pointer]]
            if (lower_pointer > 0):
                lower_pointer = lower_pointer - 1
                out_d[list_keys[lower_pointer]] = dictionary[list_keys[lower_pointer]]
        return out_d

    def Save_Ticket_Data(self,Seat_Arrangement):
        Passengers_Ticket =  open("Ticket_Data.json","r")
        data = json.load(Passengers_Ticket)
        List_id = list(data.keys())
        UID = 0
        if(len(List_id) > 0  ):
            UID =  str(int(List_id[-1])+1)
        
        data[UID] =  Seat_Arrangement
        
        with open("Ticket_Data.json","w") as Passengers_Ticket:
            json.dump(data,Passengers_Ticket)
        
        print(f"The UID is {UID}")
        return UID

    def Generate_Tickets(self,Seat_Arrangement,UID,Selected_Time,Phone_No):
        self.root_Dir =  os.getcwd()
        UID =  str(UID)
        os.mkdir(UID)
        List_of_Passengers = list(Seat_Arrangement.keys())
        
        for Passengers in range(len(Seat_Arrangement)):
            im =  Image.open("Sample_Ticket.png")
            os.chdir(UID)
            Passenger_Name =  List_of_Passengers[Passengers]
            date  = datetime.date.today().strftime("%d/%m/%Y")
        
            QR_Code_Text = f"{UID} {List_of_Passengers[Passengers]} {Seat_Arrangement[List_of_Passengers[Passengers]]} {Selected_Time} {date}"
            Drawable_Image = ImageDraw.Draw(im)
        
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 50)
            Name_w , Name_h = font.getsize(Passenger_Name)
            Drawable_Image.text((int((1151-Name_w)//2)+240, 1459), Passenger_Name, font=font, fill="black")
            Platform_Number =  Seat_Arrangement[Passenger_Name][8:-1:].strip()
        
            Platform_w ,  Platform_h =  (font.getsize(Platform_Number))
            Drawable_Image.text((int((1151-Platform_w)//3)+190, 1579),Platform_Number,font = font, fill = "black")
            Podbay = Seat_Arrangement[Passenger_Name][-1].strip()
        
            Podbay_w, Podbay_h = (font.getsize(Platform_Number))
            Drawable_Image.text((int((1151 - Podbay_w) // 4) + 190, 1679), Podbay, font=font, fill="black")

            Time = f"{Selected_Time} {date}"
            Starting_Time = Selected_Time.split("-")[0]
            Starting_Time_Mins =  Starting_Time.split(":")[--1]
            Extra_Time =  int((int(Platform_Number)*30)//2)
            Starting_Time_Secs =  00

            Time = Time.strip()
            Time_w, Time_h = (font.getsize(Time))
            Drawable_Image.text((int((1151 - Time_w) // 4) + 300, 1782), Time, font=font, fill="black")

            UID_w, UID_h = (font.getsize(Time))
            Drawable_Image.text((int((1151 - UID_w) // 4) + 300, 1886), UID, font=font, fill="black")
            QR_Code = qrcode.make(QR_Code_Text)
            
            QR_Code.save(f"{List_of_Passengers[Passengers]}_QRCode.png")
            QR_code_Pil = Image.open(f"{List_of_Passengers[Passengers]}_QRCode.png")
            
            QR_code_Pil = QR_code_Pil.resize((945,945))
            QR_Code_w, QR_Code_h =  QR_code_Pil.size
            
            im.paste(QR_code_Pil,(((int(1511.8110236-QR_Code_w)//2)),((int(2267.7165354-QR_Code_h)//7))))
            im.save(f"{List_of_Passengers[Passengers]}_Ticket.png")

            os.remove(f"{Passenger_Name}_QRCode.png")
            os.chdir(self.root_Dir)
            with open("Ticket_Data_Assign.json","r") as f:
                d_t = json.load(f)
            Platform_Number_key = f"Platform{Platform_Number}"
            d_t[Selected_Time][Platform_Number_key][Podbay].append([Passenger_Name,Phone_No])
            with open("Ticket_Data_Assign.json","w") as f:
                json.dump(d_t,f)



class PassengerEntryPortal(Resource):
    def get(self,PassengerDetails):
        os.chdir(ROOT_DIR)
        print("INHERRRRRRRRRR")
        PassengerDetails_copy  = PassengerDetails
        PassengerDetails=  PassengerDetails.split("_")
        UID =  int(PassengerDetails[0])
        Name =  " ".join(PassengerDetails[1:PassengerDetails.index("Platform"):])
        Platform_No =  int(PassengerDetails[PassengerDetails.index("Platform")+1])
        Pod_Bay =   str(PassengerDetails[-3])
        Timings =  str(PassengerDetails[-2])
        Date =  str(PassengerDetails[-1])
        root_dir =  os.getcwd()
        status_in =  False
        if(f"{Name}{UID}{Platform_No}.txt" in os.listdir("PassengerInPortal")):
            status_in = True
        os.chdir(root_dir)
        if(str(UID) in os.listdir()):
            os.chdir(str(UID))
            tickets =  os.listdir()
            for ele in tickets:
                if(Name in ele and status_in==False):
                    os.chdir(root_dir)
                    with open("Portal_Details.json","r+") as f:
                        data =  json.load(f)
                    data["Total_Passengers"]+=1
                    print(data)
                    with open("Portal_Details.json","w+") as f:
                        json.dump(data,f)
                    os.chdir(root_dir)
                    os.chdir("PassengerInPortal")
                    os.mkdir(f"{Name}{UID}{Platform_No}.txt")
                    os.chdir(root_dir)
                    print(1)
                    return {"Type": "True","msg": "Welcome to Hyperloop Mumbai"}
                elif(status_in==True):
                    os.chdir(root_dir)
                    print(2)
                    return {"Type": "False1", "msg": "Nothing"}
                else:
                    print(3)
                    os.chdir(root_dir)
                    return {"Type":"False","msg":"Sorry I didn't find your ticket"}
        else:
            print(4)
            return {"Type":"False","msg":"Sorry I didn't find your ticket"}
        print(5)
        return {"Type":"False","msg":"Error"}

class PassengerEntryPlatform(Resource):
    def get(self,Ticket_Details,Platform_No):
        Ticket_Details = Ticket_Details.split("_")
        UID = Ticket_Details[0]
        Name =  " ".join(Ticket_Details[1:Ticket_Details.index("Platform"):])
        Platform_No_Ticket = int(Ticket_Details[-4])
        Pod_Bay = Ticket_Details[-3]
        Timings =  Ticket_Details[-2]
        Date = Ticket_Details[-1]
        print(Timings)

        if(Platform_No_Ticket !=  Platform_No):
            msg = f"Wrong Platform no, you have to go platform number {Platform_No_Ticket}"
            return {"Type":"False","msg":msg}

        with open("t.json", "r") as f:
            boarding_data = json.load(f)
        boarding_time = boarding_data["value"]

        with open("t.json", "r") as f:
            exit_data = json.load(f)
        exit_time = exit_data["value"]

        for index in range(len(boarding_time)):
            boarding_time[index] = boarding_time[index].split("-")[0]
            boarding_time[index] = parser.parse(boarding_time[index])

        for index in range(len(exit_time)):
            exit_time[index] = exit_time[index].split("-")[-1]
            exit_time[index] = parser.parse(exit_time[index])

        current_time = datetime.datetime.now().time()
        current_time = current_time.replace(microsecond=0)

        for object in range(len(boarding_time)):
            if (boarding_time[object].time() <= current_time):
                if (exit_time[object].time() >= current_time):
                    start_time = boarding_time[object].strftime("%H:%M:%S")
                    end_time = exit_time[object].strftime("%H:%M:%S")
        try:
            time = f"{start_time}-{end_time}"
        except:
            time = None

        if(time!=Timings):
            msg= f"Your Boarding has not started yet or it must have passed, the current time session is {time}"
            return {"Type":"False","msg":msg}

        else:
            with open("Portal_Details.json", "r+") as f:
                data = json.load(f)
            data[f"Platform{Platform_No}"] += 1
            with open("Portal_Details.json", "w+") as f:
                json.dump(data,f)
            msg = "Gates Opening"
            with open("In.json", "r+") as f:
                d =  json.load(f)
            return {"Type":"True","msg":msg}


class Car_Entry(Resource):
    def post(self,vech_type,car_no):
        print("Function Called")
        with open("Car_Spaces.json","r+") as f:
            d = json.load(f)
        if(vech_type ==  "Car"):
            d["Car"]+=1
        else:
            d["Cab"]+=1

        with open("Car_Spaces.json","w+") as f:
            json.dump(d,f)

        with open("vech_details.json","r+") as f:
            details =  json.load(f)
        details[car_no] =  vech_type
        with open("vech_details.json","w+") as f:
            json.dump(details,f)

class Car_Exit(Resource):
    def post(self,car_no):
        with open("vech_details.json","r+") as f:
            d1 = json.load(f)
        vech_type =  d1[car_no]

        with open("Car_Spaces.json","r+") as f:
            d = json.load(f)

        if(vech_type ==  "Car"):
            d["Car"]-=1
        else:
            d["cab"]-=1
        del d1[car_no]

        with open("vech_details.json","r+") as f:
            json.dump(d1,f)

        with open("Car_Spaces.json","w+") as f:
            json.dump(d,f)

class GetNoPassengers(Resource):
    def get(self,Platform_no):
        with open("Portal_Details.json","r+") as f:
            details = json.load(f)
        passengers = details[f"Platform{Platform_no}"]
        return {"Passengers":passengers}

class GetVech(Resource):
    def get(self,temp):
        print("In here")
        with open("Car_Spaces.json", "r+") as f:
            d = json.load(f)
        return d

api.add_resource(PassengerEntryPortal,"/PassengerEntryPortal/<string:PassengerDetails>")
api.add_resource(BookTicket,"/BookTicket/<string:list_of_passengers>/<string:ticket_booking_time>/<int:phone_no>")
api.add_resource(Timings, "/Timings/<int:passengers>")
api.add_resource(PassengerEntryPlatform,"/PassengerEntryPlatform/<string:Ticket_Details>/<int:Platform_No>")
api.add_resource(Car_Exit,"/CarExit/<string:car_no>")
api.add_resource(Car_Entry,"/CarEntry/<string:vech_type>/<string:car_no>")
api.add_resource(GetVech,"/GetVech/<string:temp>")
api.add_resource(GetNoPassengers,"/GetPassengers/<int:Platform_no>")

if __name__ == "__main__":
    app.run(debug=True)
