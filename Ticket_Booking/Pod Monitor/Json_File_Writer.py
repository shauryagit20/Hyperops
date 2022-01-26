import json
import os
root = os.getcwd()
os.chdir("/media/intact/DATA/Techfest_Hyperops/Ticket_Booking/Server")
with open("Timings.json","r+") as f:
    data =  json.load(f)

d = {"value":[]}

for keys in data:
    d["value"].append(keys)
print(d)
os.chdir(root)
with open("Timings.json","w") as f:
    json.dump(d,f)
