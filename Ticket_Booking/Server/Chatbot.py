import datetime
import json
import os
import File_Uploader
import flask
from flask_restful import Api, Resource
from twilio.rest import Client
from dateutil import parser
app = flask.Flask(__name__)
api =  Api(app)
ACCOUNT_SID =  "AC6575bf446b4121f2af51b6de40264585"
ACCOUNT_TOKEN = "a55f9f2e0b7e1dec442f85d4eace742d"
CURRENT_DIR = os.getcwd()
client = Client(ACCOUNT_SID,ACCOUNT_TOKEN)
BASE  = "https://res.cloudinary.com/dr0ppt3js/image/upload/v1639574328/"

class SendTicket(Resource):
    def post(self,UID: int,phone_no: int):
        os.chdir(CURRENT_DIR)
        os.chdir(str(UID))
        for files in os.listdir():
            File_Uploader.upload_files(files,UID)
            files_link = "_".join(files.split(" "))
            url = f"{BASE}{UID}_{files_link}.png"
            print(url)
            print(phone_no)
            message = client.messages.create(media_url=url,
                        from_='whatsapp:+14155238886',
                        to=f'whatsapp:+91{str(phone_no)}'
                    )
            print("Over here")
            print(message.sid)
        os.chdir(CURRENT_DIR)
        return "SENT"

class Broadcast(Resource):
    def post(self,List,selected_time,message):
        print("Called")
        broad_cast_list = List.split(",")
        match_dict = {1:"A",2:"B",3:"C",4:"D",5:"E",6:"F"}
        for pair in broad_cast_list:
            pair_list =  pair.split("X")
            n =  int(pair_list[0])+1
            platform_number = f"Platform{n}"
            pod_bay_number = match_dict[int(pair_list[1])+1]
            with open("Ticket_Data_Assign.json","r") as f:
                data_d =  json.load(f)
            print(data_d.keys())
            print(selected_time)
            print(platform_number)
            print(pod_bay_number)
            list_of_passengers = data_d[selected_time][platform_number][pod_bay_number]
            print(type(list_of_passengers))
            print(list_of_passengers)
            print(f"The message is {message}")
            m = message
            for tup in list_of_passengers:
                passenger_name = tup[0]
                print(passenger_name)
                phone_no = tup[1]
                print(phone_no)
                message = client.messages.create(body=m,
                                                 from_='whatsapp:+14155238886',
                                                 to=f'whatsapp:+91{str(phone_no)}'
                                                 )
                print(message.sid)
            return {"status":"message broadcasted"}


class Broadcast_Error(Resource):
    def get(self):
        print("Called")
        m =  "Your pod bay has stopped working please go to Platform Number 7, our team will present at Platform 7 will guide you.\n Sorry for the inconvenience"
        time =  None

        while time== None:
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
                print("Here")
            try:
                time = f"{start_time}-{end_time}"
            except:
                time = None
        to_break = True
        with open("t.json", "r") as f:
            data = json.load(f)
        data = data["value"]
        start_index =  data.index(time)
        for index in range(start_index,len(data)):
            with open("Ticket_Data_Assign.json","r") as f:
                data_d =  json.load(f)
            list_to_send = data_d[data[index]]["Platform1"]["A"]
            for tup in list_to_send:
                passenger_name = tup[0]
                print(passenger_name)
                phone_no = tup[1]
                print(phone_no)
                message = client.messages.create(body=m,
                                                 from_='whatsapp:+14155238886',
                                                 to=f'whatsapp:+91{str(phone_no)}'
                                                 )
                print(message.sid)
                to_break =  True
                break
            break
        return {"status":"message broadcasted"}





api.add_resource(SendTicket,"/SendTicket/<int:UID>/<int:phone_no>")
api.add_resource(Broadcast,"/BroadCast/<string:List>/<string:selected_time>/<string:message>")
api.add_resource(Broadcast_Error,"/BroadcastError")
if(__name__ == "__main__"):
    app.run(host='127.0.0.1', port=5550,debug=True)