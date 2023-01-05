#--import--
from pypresence import Presence
import time
import platform
import psutil
import GPUtil
import sys
import threading
import keyboard
import os


#--functions--
options = [["CPU Type", 1], ["CPU Usage", 0], ["Total Memory", 1], ["Memory Usage", 1], ["GPU Name", 1], ["GPU Usage", 1]]
selection = 2
def displayMenu():
    clear()
    global selection
    print("Enable * or Disable O | press esc when done")
    j = 0
    for i in options:
        print(">" if selection == j else " ","O     " if i[1] == 0 else "*     ",i[0])
        j += 1

def menuUp():
    global selection
    print("\n")
    selection -= 1
    if selection < 0:

        selection = 0
    displayMenu()

def menuDown():
    global selection
    global options
    print("\n")
    selection += 1
    displayMenu()

def menuSelect():
    global selection
    global options
    print(options[selection][1])
    if (options[selection][1] == 0):
        options[selection][1] = 1
    else:
        options[selection][1] = 0
    displayMenu()

def clear():
    try:
        os.system('cls')
    except:
        os.system('clear')

def clearHotkeys():
    keyboard.unregister_hotkey('enter')
    keyboard.unregister_hotkey('esc')
    keyboard.unregister_hotkey('w')
    keyboard.unregister_hotkey('s')

def setHotkeys():
    keyboard.add_hotkey('w', menuUp)
    keyboard.add_hotkey('s', menuDown)
    keyboard.add_hotkey('enter', menuSelect)
    keyboard.add_hotkey('esc', clearHotkeys)


def NvidiaGpu():
    GPUs = GPUtil.getGPUs()
    if (len(GPUs) > 0):
        return True
    else:
        return False

def getCpuUsage():
    return str(psutil.cpu_percent())

def getMemoryUsage():
    return str(psutil.virtual_memory().percent)

def getGpuUsage():
    try:
        GPUs = GPUtil.getGPUs()
        return str((GPUs[0].load)*(100))
    except:
        return ""

def updatePres(RPC,cpuType,ramSize,startTime,winVersion,updateTime):
    while True:
        # check for Nvidia card and usage
        gpuLoad = str("GPU ("  +") "+ str(getGpuUsage()) + "% |")
        # update rich pres
        RPC.update(state=("| CPU (" + str(cpuType) + ") " + getCpuUsage() + "% | RAM (" + str(round(ramSize)) + "GB) " + getMemoryUsage() + "% | " + gpuLoad),start=int(startTime),details=winVersion)
        time.sleep(updateTime)


#--delcaire--
client_id = "1050923361527664751"

#get systems os and major release ex: Windows 10
winsystem = str(platform.system())
winversion = str(platform.release())

winVersion = winsystem + " " + winversion

startTime = int(time.time())

cpuType = platform.uname().machine

ramSize = (psutil.virtual_memory().total) / (1000000000)

Nvidia = NvidiaGpu()
gpuLoad = ""

updateTime = 10



#--setup--
try:
    RPC = Presence(client_id=client_id)
    RPC.connect()
    RPC.update(start=int(time.time()),state="On Desktop",details=winVersion)
except:
    print("Could not connect please check that discord is open")
    sys.exit()

setHotkeys()
displayMenu()
keyboard.wait('esc',clearHotkeys)

print(" ")
time.sleep(1)
clear()





update = threading.Thread(target=updatePres, args=(RPC,cpuType,ramSize,startTime,winVersion,updateTime), daemon=True)
update.start()
print("connected")
print("Updating every " + str(updateTime) + " seconds")
print("CTRL-C to exit")


#--loop--
while True:
    i = input()
    if i == "e":
        break
     
