#--import--
from pypresence import Presence
import time
import platform
import psutil
import GPUtil
import sys
import threading
import os
import tty
import termios






#--global vars--
options = [["CPU Type", 1], ["CPU Usage", 1], ["Total Memory", 1], ["Memory Usage", 1], ["GPU Name", 1], ["GPU Usage", 1]]
selection = 0
output = ""

startTime = int(time.time())

cpuType = platform.uname().machine

ramSize = (psutil.virtual_memory().total) // (1000000000)

updateTime = 10

gpu = 0 # 0 = none 1 = nvidia 2 = amd
try:
    from pyadl import *
    gpu = 2
except:
    print("none")

#--functions--
def checkAMDGPU():
    global gpu
    
    if (len(GPUtil.getGPUs()) > 0):
        gpu = 1
    elif (gpu == 2):
        print("AMD")
    else:
        gpu = 0

def menuLoop():
    orig_settings = termios.tcgetattr(sys.stdin)

    tty.setcbreak(sys.stdin)
    x = 0
    while x != chr(27): #esc breaks
        displayMenu()
        x=sys.stdin.read(1)[0]
        if(x == "w"):
            menuUp()
        elif ( x == "s"):
            menuDown()
        elif (x=="e"):
            menuSelect()

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings) 
    defaultMsg()


def displayMenu():
    clear()
    global selection
    print("--Enable * or Disable O | press esc when done --")
    print("--w selection up | s selection down | e select--")
    j = 0
    for i in options:
        print(">" if selection == j else " ","O     " if i[1] == 0 else "*     ",i[0])
        j += 1
    buildMessage()
    print(output)

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
    if (str(platform.system()) != "Linux"):
        os.system('cls')
    else:
        os.system('clear')



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



def getNVGpuUsage():
    try:
        GPUs = GPUtil.getGPUs()
        return str(round((GPUs[0].load)*(100),0))
    except:
        return ""

def getNVGpuName():
    try:
        GPUs = GPUtil.getGPUs()
        return str(GPUs[0].name)
    except:
        return ""

def getAMDGpuUsage():
    return str(ADLManager.getCurrentUsage())

def getAMDGpuName():
    return str(ADLManager.getDevices()[0])

def getGPUName():
    global gpu
    if gpu == 1:
        return getNVGpuName()
    elif gpu == 2:
        return getAMDGpuName()
    else:
        return "No GPU"

def getGPUUsage():
    global gpu
    if gpu == 1:
        return getNVGpuUsage()
    elif gpu == 2:
        return getAMDGpuUsage()
    else:
        return "No GPU"

def buildMessage():
    global options
    global output

    global ramSize
    
    output = ""

    if options[0][1] == 1 or options[1][1] == 1:
        output += "|CPU"
        if options[0][1] == 1:
            output += "(" + str(platform.uname().machine) + ")"
        if options[1][1] == 1:
            output += "(" + str(getCpuUsage()) + "%)"
        

    if options[2][1] == 1 or options[3][1] == 1:
        output += "|RAM"
        if options[2][1] == 1:
            output += "(" + str(ramSize) + "GB)"
        if options[3][1] == 1:
            output += "(" + str(getMemoryUsage()) + "%)"
        

    if options[4][1] == 1 or options[5][1] == 1:
        output += "|GPU"
        if options[4][1] == 1:
            output += "(" + str(getGPUName()) + ")"
        if options[5][1] == 1:
            output += "(" + str(getGPUUsage()) + "%)"
    output += "|"

def defaultMsg():
    global updateTime
    clear()
    print("connected")
    print("Updating every " + str(updateTime) + " seconds")
    print("press m to reopen settings | press x to exit")

def updatePres(RPC,winVersion,updateTime):
    global output
    while True:
        # update rich pres
        buildMessage()
        RPC.update(state=output,start=int(startTime),details=winVersion)
        time.sleep(updateTime)

#--vars--
client_id = "1050923361527664751"

#get systems os and major release ex: Windows 10
winsystem = str(platform.system())
winversion = str(platform.release())

winVersion = winsystem + " " + winversion

#--setup--
try:
    RPC = Presence(client_id=client_id)
    RPC.connect()
    RPC.update(start=int(time.time()),state="In Settings",details=winVersion)

    checkAMDGPU()

except:
    print("Could not connect please check that discord is open")
    sys.exit()
print(options)
menuLoop()


update = threading.Thread(target=updatePres, args=(RPC,winVersion,updateTime), daemon=True)
update.start()


#--loop--
stop = False
while True and stop != True:
    orig_settings = termios.tcgetattr(sys.stdin)

    tty.setcbreak(sys.stdin)
    x = 0
    x=sys.stdin.read(1)[0]
    if(x == "x"): 
        break
    elif ( x == "m"):
        menuLoop()

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings) 
     
