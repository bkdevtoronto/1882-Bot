import os

# Read array from file
def get(file):
    ret = []
    try:
        f = open(file, "r")
        for line in f:
            ret.append(line[:-1])

        f.close()
        return ret

    except Exception as e:
        print(str(e))

# Add to array
def addTo(file, string):
    f = open(file, "a")
    f.write(str(string).encode('utf-8') + "\n")
    f.close()

# Remove from array
def removeFrom(file, string):
    arr = []
    f = open(file, "r")
    for line in f:
        arr.append(line[:-1])

    if string in arr:
        arr.remove(string)

    f.close()
    f = open(file, "w")
    f.write("")
    f.close()

    f = open(file, "a")
    arr = arr[-5:]
    for string in arr:
        f.write(string + "\n")
    f.close()
