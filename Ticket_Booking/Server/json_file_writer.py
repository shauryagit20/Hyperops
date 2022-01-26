import json
with open("Daily_Schedule.json","r") as  f:
    d =  json.load(f)
l =  d.keys()
print(l)
empty_d ={}
for i in l:
    d2 = {}
    for counter in range(1,14):
        p = f"Platform{counter}"
        l2 = []
        for letters in range(65,71):
            l2.append(chr(letters))
        d3 = {}
        for char in l2:
            d3[char] = []
        d2[p] =  d3
    empty_d[i] =  d2
print(empty_d)
with open("Ticket_Data_Assign.json","w") as f:
    json.dump(empty_d,f)
