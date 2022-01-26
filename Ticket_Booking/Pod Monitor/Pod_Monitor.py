import sys
import time
import json
import datetime
import threading

import requests
from dateutil import parser
from flask import Flask
from flask_restful import Api, Resource

function_stated = False

layout = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
broken_pods = []
listen = [0, 0]
currently_broken = []
simulated_broken = []
to_reactivate = False
portal_status = {
    "Platform1": {"status": None, "Time_Left": None, "Time_Session": None},
    "Platform2": {"status": None, "Time_Left": None, "Time_Session": None},
    "Platform3": {"status": None, "Time_Left": None, "Time_Session": None},
    "Platform4": {"status": None, "Time_Left": None, "Time_Session": None},
    "Platform5": {"status": None, "Time_Left": None, "Time_Session": None},
    "Platform6": {"status": None, "Time_Left": None, "Time_Session": None},
    "Platform7": {},
    "Platform8": {"status": None, "Time_Left": None, "Time_Session": None},
    "Platform9": {"status": None, "Time_Left": None, "Time_Session": None},
    "Platform10": {"status": None, "Time_Left": None, "Time_Session": None},
    "Platform11": {"status": None, "Time_Left": None, "Time_Session": None},
    "Platform12": {"status": None, "Time_Left": None, "Time_Session": None},
    "Platform13": {"status": None, "Time_Left": None, "Time_Session": None},
}

assigned_pod = {}
cycle_completed = False
can_enter = True
Boarding_Time = datetime.timedelta(minutes=5, seconds=30)
Docking_Time = datetime.timedelta(seconds=20)
Exiting_Time = datetime.timedelta(seconds=10)
Incoming_time = datetime.timedelta(seconds=30)
process = {"Boarding": Boarding_Time, "Docking": Docking_Time, "Exiting": Exiting_Time, "Incoming": Incoming_time}


def status_manager(countdown_time, target, platform):
    global portal_status

    while True:
        with open(f"Status_Manager{platform}.txt","a+") as f:
            f.write(f"Countdown state -  {countdown_time} target -  {target} platform - {platform}\n")
        decrementor = datetime.timedelta(seconds=1)
        countdown_time = countdown_time - decrementor
        print(str(countdown_time))
        d = {"Time_Left": str(countdown_time), "Platform": platform}
        portal_status["Platform7"] = {target: d}
        with open(f"Status_Manager{platform}.txt","a+") as f:
            f.write(f"D : {d}... Portal_status : {portal_status}")
        if (countdown_time.seconds == 0):
            del portal_status["Platform7"][target]
            break
        time.sleep(1)


def listen_status(key, value, is_greater, Greater_Platform):
    global can_enter
    global portal_status
    global layout

    while True:
        key_split = key.split("X")
        Platform = int(key_split[0]) + 1
        i = int(value.split("X")[0])
        with open(f"{Platform}.txt","a+") as f:
            f.write(f"The value of i is {i}. The value of can_enter is {can_enter}\n")

        if (portal_status[f"Platform{Platform+1}"]["status"] == "Incoming"):
            layout[i][6] = 0
            # layout[int(key_split[0])][Platform-1] =  -1
            time.sleep(30)
            with open("Reactivate.json", "r") as f:
                reactivate_data = json.load(f)

            if (reactivate_data["reactivate"] != "True"):
                with open(f"{Platform}.txt", "a+") as f:
                    f.write(f"The value of key is {key}. The value of can_enter is {can_enter}\n")

                if (is_greater == True):
                    can_enter = False
                    layout[i][6] = 1
                    countdown_time = datetime.timedelta(minutes=6, seconds=00)
                    countdown_time_manager = threading.Thread(target=status_manager,
                                                              args=(countdown_time, f"{i}X6", Platform))
                    countdown_time_manager.start()

                else:
                    print("Lower")
                    with open("Logger.txt", "a+") as f:
                        f.write(f"In lower \n The value of can_enter is {can_enter}\n")
                    if (can_enter == False):
                        layout[2][6] = 1
                        current_status = portal_status[f"Platform{Greater_Platform+1}"]["status"]
                        time_passed_current_status = portal_status[f"Platform{Greater_Platform}"]["Time_Left"]
                        time_passed_datetime_format = datetime.datetime.strptime(time_passed_current_status, '%H-%M-%S')
                        time_passed_delta_time = datetime.timedelta(minutes=time_passed_datetime_format.minute,
                                                                    seconds=time_passed_datetime_format.second)
                        Status_key = list(process.keys())
                        index_start = Status_key.index(current_status)
                        sum_time = datetime.timedelta(seconds=0)
                        for indexes in range(index_start, len(Status_key) - 1):
                            if (Status_key[indexes] == current_status):
                                sum_time = sum_time + (process[current_status] - time_passed_delta_time)
                            else:
                                sum_time = sum_time + process[Status_key[indexes]]
                        Thread_status_manager = threading.Thread(target=status_manager,
                                                                 args=(sum_time, "2X6", Platform))
                        Thread_status_manager.start()
                        time.sleep(sum_time)
                        layout[i][6] = 1
                        countdown_time = datetime.timedelta(minutes=6, seconds=00)
                        countdown_time_manager = threading.Thread(target=status_manager,
                                                                  args=(countdown_time, f"{i}X6", Platform))
                        countdown_time_manager.start()

                    else:
                        layout[0][6] = 1
                        countdown_time = datetime.timedelta(minutes=6, seconds=00)
                        countdown_time_manager = threading.Thread(target=status_manager,
                                                                  args=(countdown_time, f"{i}X6", Platform))
                        countdown_time_manager.start()

            else:
                print(f"The value of can enter is {can_enter} ")
                print("Exiting...")
                sys.exit()
        time.sleep(1)


def find_greater(podbays):
    l = []
    for pods in podbays:
        pods_list = pods.split("X")
        l.append(list(pods_list))
    if (len(l) == 1):
        return None
    else:
        if (l[0][1] > l[1][1]):
            return 0
        elif (l[0][1] < l[1][1]):
            return 1
        elif (l[0][0] > l[1][0]):
            return 0
        else:
            return 1


def call_me():
    global can_enter
    with open("TEXTTT.txt", "a+") as f:
        f.write("RAN Call me\n")

    with open("Assigned_Pod.json", "r") as f:
        data = json.load(f)

    listen = [0, 0]
    keys_list = list(data.keys())
    greater_pod_bay = keys_list[find_greater(keys_list)]
    with open("Log.txt","a+") as f:
        f.write(f"The value of greater pod bay is {greater_pod_bay}\n")
        f.write(f"The value of keys _list is {keys_list}\n")

    Platform_No_Greater_pod_bay = int(greater_pod_bay.split("X")[1])
    Ran_json =  {f"Platform{keys_list[0]}":False,f"Platform{keys_list[1]}":False}
    with open("Ran.json","w+") as f:
        json.dump(Ran_json,f)
    for ele in range(len(keys_list)):
        with open("ele.txt","a+") as f:
            f.write(f"{keys_list[ele]}...  Greater : {greater_pod_bay} \n")
        if (keys_list[ele] == greater_pod_bay):
            with open("ele2.txt", "a+") as f:
                f.write(f"{keys_list[ele]}...  Greater : {greater_pod_bay} \n")
            is_greater = True
            t = threading.Thread(target=listen_status,
                                 args=(keys_list[ele], data[keys_list[ele]], is_greater, Platform_No_Greater_pod_bay))
            t.start()
        else:
            is_greater =  False
            print("In here......")
            with open("Log3.txt","a+") as f:
                f.write(f"The value of is greater is {is_greater}, the greater pod bay is {greater_pod_bay}, and the current pod bay is {keys_list[ele]}\n")
            t2 = threading.Thread(target=listen_status, args=(
                keys_list[ele], data[keys_list[ele]], is_greater, Platform_No_Greater_pod_bay))
            t2.start()



class Monitor:
    def __init__(self):
        self.Running_boarding_monitor = []

    def Main(self):
        while True:
            self.func()
            time.sleep(1)

    def remove_convoy(self):
        global layout
        global function_stated
        global cycle_completed
        c = 0
        to_break = False
        # print("Removing Convoy....")
        # print(f"The value of convoy is {c}")
        while to_break == False:
            if (c == 1):
                with open("Text.txt", "w+") as f:
                    f.write("True")
                cycle_completed = True
            if (c != 6):
                time.sleep(30)
                self.Running_boarding_monitor.remove(f"Platform{c + 1}")
                # print("In here")
                for i in range(len(layout)):
                    layout[i][c] = 0

            if (c == 12):
                to_break = True
                cycle_completed = True
                break
            c = c + 1

        function_stated = False

        sys.exit()

    def update_status(self, platform_number, status):
        global portal_status
        Platform_Name = f"Platform{platform_number}"
        portal_status[Platform_Name]["status"] = "Boarding"

    def boarding_monitor(self, platform_number, ending_time):
        global portal_status
        difference = 10000
        delta_time = datetime.timedelta(minutes=5, seconds=30)
        start_time = portal_status[f"Platform{platform_number + 1}"]["Time_Session"]
        target_time = delta_time + start_time
        time_remaining = target_time - datetime.datetime.now()

        while time_remaining.seconds != 0:
            portal_status[f"Platform{platform_number + 1}"]["Time_Left"] = str(time_remaining).split(".")[0]
            current_time = datetime.datetime.now()
            time_remaining = target_time - current_time
            time.sleep(1)
        portal_status[f"Platform{platform_number + 1}"]["status"] = "Docking"
        Docking_Thread = threading.Thread(target=self.docking_out, args=(platform_number, "Temp"))
        Docking_Thread.start()
        sys.exit()

    def docking_out(self, Platform_no, temp):
        current_time = datetime.datetime.now()
        delta_time = datetime.timedelta(seconds=20)
        target_time = current_time + delta_time
        time_left = target_time - current_time

        while (time_left.seconds != 0):
            portal_status[f"Platform{Platform_no + 1}"]["Time_Left"] = str(time_left).split(".")[0]
            current_time = datetime.datetime.now()
            time_left = target_time - current_time
            time.sleep(1)

        portal_status[f"Platform{Platform_no + 1}"]["status"] = "Exiting"
        Exit_Thread = threading.Thread(target=self.exit_monitor, args=(Platform_no, "Temp"))
        Exit_Thread.start()
        sys.exit()

    def exit_monitor(self, platform_number, Temp):
        global portal_status
        current_time = datetime.datetime.now()
        delta_time = datetime.timedelta(seconds=10)
        target_time = current_time + delta_time
        time_left = target_time - current_time
        while (time_left.seconds != 0):
            portal_status[f"Platform{platform_number + 1}"]["Time_Left"] = str(str(time_left).split(".")[0])
            current_time = datetime.datetime.now()
            time_left = target_time - current_time
            time.sleep(1)

        portal_status[f"Platform{platform_number + 1}"]["status"] = "Incoming"
        Incoming_Thread = threading.Thread(target=self.incoming_monitor, args=(platform_number, "Temp"))
        Incoming_Thread.start()
        sys.exit()

    def incoming_monitor(self, platform_number, Temp):
        global portal_status
        current_time = datetime.datetime.now()
        delta_time = datetime.timedelta(seconds=30)
        target_time = current_time + delta_time
        time_left = target_time - current_time
        while (time_left.seconds != 0):
            portal_status[f"Platform{platform_number + 1}"]["Time_Left"] = str(str(time_left).split(".")[0])
            current_time = datetime.datetime.now()
            time_left = target_time - current_time
            time.sleep(1)

        portal_status[f"Platform{platform_number + 1}"]["status"] = "Boarding"
        sys.exit()

    def func(self):
        global portal_status
        global layout
        global to_reactivate
        global function_stated
        global broken_pods
        global currently_broken
        global simulated_broken
        with open("Timings.json", "r") as f:
            boarding_data = json.load(f)
        boarding_time = boarding_data["value"]

        with open("Timings.json", "r") as f:
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
            duration_passed = datetime.datetime.combine(datetime.date.today(),
                                                        current_time) - datetime.datetime.combine(datetime.date.today(),
                                                                                                  parser.parse(
                                                                                                      start_time).time())
            # Issue can be with the start time
            seconds_passed = int(duration_passed.total_seconds())
            # print(f"The number of seconds passed is {seconds_passed} ")
            # print(broken_pods)
            if (seconds_passed < 180):
                Convoys_present = int((seconds_passed + 30) // 30)
                counter = 0
                # print(f"The number of convoys present: {Convoys_present}")
                try:
                    with open("Assigned_Pod.json", "r") as f:
                        ap = json.load(f)
                        # print(f"The ap is {ap}")
                except Exception as e:
                    # print(f"The {e}")
                    ap = {}
                while counter < Convoys_present:
                    if (counter != 6):
                        # print("In here")
                        # print(portal_status)
                        if (f"Platform{counter + 1}" not in self.Running_boarding_monitor):
                            # print(portal_status)
                            try:
                                with open("Assigned_Pod.json", "r") as f:
                                    ap = json.load(f)
                                    # print(f"The ap is {ap}")
                            except Exception as e:
                                # print(f"The error is  {e}")
                                ap = {}

                            for pod_bay_number in range(6):
                                # print("X"*1000)
                                # print(f"{pod_bay_number}X{counter}")
                                # print("X"*1000)
                                # print(f"The ap is {ap}")
                                # print(portal_status)
                                if (f"{pod_bay_number}X{counter}" in ap and portal_status[f"Platform{counter + 1}"][
                                    "status"] == "Incoming"):
                                    try:
                                        with open(f"Reactivate.json", "r") as f:
                                            data = json.load(f)
                                            if (data["Reactivate"] == "True"):
                                                to_reactivate = True
                                    except:
                                        to_reactivate = False

                                    # print(f"The value of reactivate is {to_reactivate}")
                                    if (to_reactivate == True):
                                        # print(portal_status)
                                        layout[pod_bay_number][counter] = 1
                                        del ap[f"{pod_bay_number}X{counter}"]
                                        with open("Assigned_Pod.json", "w") as f:
                                            # print(f"The new assigned pod is {ap}")
                                            json.dump(ap, f)

                                        with open("Assigned_Pod.json", "w") as f:
                                            # print(f"The new assigned pod is {ap}")
                                            ap = json.load(f)
                                        with open("log.txt", "a+") as f:
                                            f.write(f"The new ap is {ap}")

                                        simulated_broken.remove(f"{pod_bay_number}X{counter}")
                                        currently_broken.remove((pod_bay_number, counter))

                                    else:
                                        # print(f"The portal status is {portal_status}")
                                        # print("Deactivated...")
                                        layout[pod_bay_number][counter] = -1
                                        simulated_broken.append(f"{pod_bay_number}X{counter}")

                            try:
                                with open("Assigned_Pod.json", "r") as f:
                                    ap = json.load(f)
                            except:
                                ap = {}

                            if (len(ap) == 0):
                                data = {"reactivate": False}
                                to_reactivate = False
                                with open("Reactivate.json", "w+") as f:
                                    json.dump(data, f)

                            current_time_docking = datetime.datetime.now()
                            portal_status[f"Platform{counter + 1}"]["Time_Session"] = current_time_docking
                            self.Running_boarding_monitor.append(f"Platform{counter + 1}")
                            portal_status[f"Platform{counter + 1}"]["status"] = "Boarding"
                            # print(f"The current portal status is {portal_status}")
                            t = threading.Thread(target=self.boarding_monitor, args=(counter, "Temp"))
                            t.start()

                        # print(f"Outside Incoming_Monitor The ap is {ap} ")
                        for i in range(len(layout)):
                            if (f"{i}X{counter}" not in ap):
                                layout[i][counter] = 1

                        if (len(ap) == 0):
                            data = {"reactivate": False}
                            to_reactivate = False
                            with open("Reactivate.json", "w+") as f:
                                json.dump(data, f)

                    counter = counter + 1
            else:
                Convoys_present = int((seconds_passed + 30) // 30) + 1
                counter = 0
                # print(f"The number of convoys present is {Convoys_present}")
                # print(f"The value of counter is {counter}")
                # print(f"The current portal status is {portal_status}")
                try:
                    with open("Assigned_Pod.json", "r") as f:
                        ap = json.load(f)
                        # print(f"The ap is {ap}")
                except Exception as e:
                    # print(f"The {e}")
                    ap = {}
                while counter < Convoys_present:
                    if (counter != 6):
                        # print(f"The value of counter is {counter + 1}")
                        # print(f"The value of List is {self.Running_boarding_monitor}")
                        # print(f"The current portal status is {portal_status}")
                        if (f"Platform{counter + 1}" not in self.Running_boarding_monitor):
                            # print("X"*100)

                            try:
                                with open("Assigned_Pod.json", "r") as f:
                                    ap = json.load(f)
                            except Exception as e:
                                # print(f"The reason why the file is not opening is {e}")
                                ap = {}

                            for pod_bay_number in range(6):
                                # print(f"Pod bay number : {pod_bay_number}X{counter}")
                                if (f"{pod_bay_number}X{counter}" in ap and portal_status[f"Platform{counter + 1}"][
                                    "status"] == "Incoming"):
                                    try:
                                        with open(f"Reactivate.json", "r") as f:
                                            data = json.load(f)
                                            if (data["Reactivate"] == "True"):
                                                to_reactivate = True
                                    except:
                                        data = {}
                                        to_reactivate = False

                                    # print(f"The value of reactivate is {to_reactivate}")
                                    if (to_reactivate == True):
                                        # print(portal_status)
                                        layout[pod_bay_number][counter] = 1
                                        del ap[f"{pod_bay_number}X{counter}"]
                                        with open("Assigned_Pod.json", "w") as f:
                                            # print(f"The new assigned pod is {ap}")
                                            json.dump(ap, f)

                                        with open("Assigned_Pod.json", "w") as f:
                                            # print(f"The new assigned pod is {ap}")
                                            ap = json.load(f)

                                        with open("log.txt", "a+") as f:
                                            f.write(f"The new ap is {ap}")

                                        simulated_broken.remove(f"{pod_bay_number}X{counter}")
                                        currently_broken.remove((pod_bay_number, counter))
                                    else:
                                        layout[pod_bay_number][counter] = -1
                                        simulated_broken.append(f"{pod_bay_number}X{counter}")

                            with open("Assigned_Pod.json", "w") as f:
                                json.dump(ap, f)

                            if (len(ap) == 0):
                                data = {"reactivate": False}
                                to_reactivate = False
                                with open("Reactivate.json", "w+") as f:
                                    json.dump(data, f)

                            current_time_docking = datetime.datetime.now()
                            # print(f"The current docking time is {current_time_docking}")
                            portal_status[f"Platform{counter + 1}"]["Time_Session"] = current_time_docking
                            portal_status[f"Platform{counter + 1}"]["status"] = "Boarding"
                            self.Running_boarding_monitor.append(f"Platform{counter + 1}")
                            t = threading.Thread(target=self.boarding_monitor, args=(counter, "Temp"))
                            t.start()

                        for i in range(len(layout)):
                            if (f"{i}X{counter}" not in ap):
                                layout[i][counter] = 1

                        if (len(ap) == 0):
                            data = {"reactivate": False}
                            to_reactivate = False
                            with open("Reactivate.json", "w") as f:
                                json.dump(data, f)
                    counter = counter + 1

                count_12 = False
                for indexes in range(6):
                    if (layout[indexes].count(1) == 12):
                        count_12 = True
                        break
                if (count_12 == True and function_stated == False):
                    # print(f)
                    function_stated = True
                    exit_thread = threading.Thread(target=self.remove_convoy)
                    exit_thread.start()

        except Exception as error:
            print(error)

        print(layout)


def func_stater():
    with open("Timings.json", "r") as f:
        boarding_data = json.load(f)
    boarding_time = boarding_data["value"]

    with open("Timings.json", "r") as f:
        exit_data = json.load(f)
    exit_time = exit_data["value"]
    function_toStart = False

    for index in range(len(boarding_time)):
        boarding_time[index] = boarding_time[index].split("-")[0]
        boarding_time[index] = parser.parse(boarding_time[index])

    for index in range(len(exit_time)):
        exit_time[index] = exit_time[index].split("-")[-1]
        exit_time[index] = parser.parse(exit_time[index])

    while function_toStart == False:
        current_time = datetime.datetime.now().time()
        start_time = None
        current_time = current_time.replace(microsecond=0)
        # print(f"Time left to start  : {current_time}")
        for object in range(len(boarding_time)):
            if (boarding_time[object].time() <= current_time):
                if (exit_time[object].time() >= current_time):
                    start_time = boarding_time[object].strftime("%H:%M:%S")
                    end_time = exit_time[object].strftime("%H:%M:%S")
                    break
        if (start_time == None):
            break

        time.sleep(1)
    Monitor().Main()


app = Flask(__name__)
api = Api(app)


class Platform_Status(Resource):
    def get(self):
        global portal_status
        for keys in portal_status:
            for o in portal_status[keys]:
                portal_status[keys][o] = str(portal_status[keys][o])
        return {"Data": portal_status}


def Assign_Pod(currently_broken):
    podbays = []
    final_data = {}
    for pods in currently_broken:
        value = f"{pods[0]}X{pods[1]}"
        podbays.append(value)

    if (len(podbays) > 1):
        greater = find_greater(podbays)

        if (greater == 1):
            final_data[podbays[1]] = f"1X6"
            final_data[podbays[0]] = f"0X6"
        else:
            final_data[podbays[0]] = f"1X6"
            final_data[podbays[1]] = f"0X6"

        with open(f"Assigned_Pod.json", "w") as f:
            json.dump(final_data, f)
    else:
        final_data[podbays[0]] = f"0X6"
        with open(f"Assigned_Pod.json", "w") as f:
            json.dump(final_data, f)
    out_thread = threading.Thread(target=call_me)
    out_thread.start()

    return final_data


def Simulate_Breaking():
    global layout
    global broken_pods
    global currently_broken
    while True:
        if (len(currently_broken) <= 2):
            for pods in broken_pods:
                if (pods not in currently_broken):
                    row, col = map(int, pods.split("X"))
                    currently_broken.append((col, row))
            Assign_Pod(currently_broken)
        time.sleep(1)


class Hyperloop_Status(Resource):
    def get(self):
        global layout
        return {"Data": layout}


class Pod_Breaking(Resource):

    def post(self, Pod_Bays):
        global broken_pods
        if (to_reactivate == True):
            return {"DATA": "Please wait while the pods are being reactivated"}
        try:
            with open("Assigned_Pod.json", "r") as f:
                d = json.load(f)
        except:
            d = {}
        if (len(d) > 0):
            return {"DATA": "ERROR, REACTIVATE THE PREVIOUS ONE BEFORE TRYING TO DEACTIVATE OTHERS"}
        broken_pod = Pod_Bays.split(",")
        broken_pods = broken_pod
        # print(broken_pods)
        for pods in broken_pods:
            if (pods not in d):
                row, col = map(int, pods.split("X"))
                currently_broken.append((col, row))
        p = Assign_Pod(currently_broken)
        requests.get(f"http://127.0.0.1:5550/BroadcastError")
        return {"DATA": p}


class Start(Resource):
    def get(self):
        global cycle_completed
        if (cycle_completed == True):
            return {"Data": True}
        else:
            return {"Data": False}


class Reactivate(Resource):
    global to_reactivate
    def post(self, Pod_Bays):
        data = {"Reactivate": "True"}
        with open("Reactivate.json", "w") as f:
            json.dump(data, f)
        #
        return {"Data": "Reactivating"}


api.add_resource(Start, "/Start")
api.add_resource(Hyperloop_Status, "/HStatus")
api.add_resource(Platform_Status, "/PStatus")
api.add_resource(Pod_Breaking, "/PodBroken/<string:Pod_Bays>")
api.add_resource(Reactivate, "/Repair/<string:Pod_Bays>")
Main_Thread = threading.Thread(target=func_stater)
# Breaking_Thread =  threading.Thread(target = Simulate_Breaking)

if __name__ == "__main__":
    Main_Thread.start()
    # Breaking_Thread.start()
    app.run(debug=True, port=5657)
