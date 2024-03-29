import os
import config

data_location=config.config["dataDirectory"]

if not os.path.exists(data_location):
    os.makedirs(data_location)

# Read array from file
def get(file):
    file=data_location+file
    ret = []
    try:
        if not os.path.exists(file) :
            t = open(file, "w")
            t.close()
            return []

        f = open(file, "r+")
        for line in f:
            ret.append(line[:-1])

        f.close()
        return ret

    except Exception as e:
        print(str(e))

# Add to array
def addTo(file, string):
    file="data/"+file
    f = open(file, "a+")
    f.write(str(string + "\n"))
    f.close()

# Remove from array
def removeFrom(file, string):
    file="data/"+file
    arr = []
    f = open(file, "r+")
    for line in f:
        arr.append(line[:-1])

    if string in arr:
        arr.remove(string)

    f.close()
    f = open(file, "w+")
    f.write("")
    f.close()

    f = open(file, "a+")
    arr = arr[-5:]
    for string in arr:
        f.write(string + "\n")
    f.close()
