#--import--
from pypresence import Presence
import time
import platform
import psutil
import GPUtil

#--functions--
def NvidiaGpu():
    GPUs = GPUtil.getGPUs()
    if (len(GPUs) > 0):
        return True
    else:
        return False
#--delcaire--
client_id = "1050923361527664751"

#get systems os and major release ex: Windows 10
winsystem = str(platform.system())
winversion = str(platform.release())

winVersion = winsystem + " " + winversion

startTime = int(time.time())

cpuType = platform.uname().machine

ramSize = (psutil.virtual_memory().total) / (1000000000);

Nvidia = NvidiaGpu()
gpuLoad = ""

updateTime = 10

RPC = Presence(client_id=client_id)

#--setup--
RPC.connect()
print("connected I hope")


RPC.update(start=int(time.time()),state="On Desktop",details=winVersion)
print("ok actually connected")

print("Updating every " + str(updateTime) + " seconds")
print("CTRL-D to exit")
#--loop--
while True:
    # get system usage
    cpu = str(psutil.cpu_percent())
    ram = str(psutil.virtual_memory().percent)

    # check for Nvidia card and usage
    if(Nvidia == True):
        GPUs = GPUtil.getGPUs()
        load = GPUs[0].load
        GPUname = GPUs[0].name
        gpuLoad = str("GPU (" + GPUname +") "+ str(load) + "% |")
    # update rich pres
    RPC.update(state=("| CPU (" + str(cpuType) + ") " + cpu + "% | RAM (" + str(round(ramSize)) + "GB) " + ram + "% | " + gpuLoad),start=int(startTime),details=winVersion)
    time.sleep(updateTime)
