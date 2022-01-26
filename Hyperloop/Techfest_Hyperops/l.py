import os
sum = 0
for files in os.listdir():
    try:
        if(files.split(".")[-1] == "py"):
            with open(files,"r+") as f:
                lines = f.readlines()
                sum =  sum+len(lines)
    except:
        continue

print(sum)
