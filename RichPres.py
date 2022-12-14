from pypresence import Presence
import time
import platform
import psutil
import GPUtil

def NvidaGpu():
    GPUs = GPUtil.getGPUs()
    if (len(GPUs) > 0):
        return True
    else:
        return False

client_id = "1050923361527664751"

winsystem = str(platform.system())
winversion = str(platform.release())

winVersion = winsystem + " " + winversion

startTime = int(time.time())

cpuType = platform.uname().machine

ramSize = (psutil.virtual_memory().total) / (1000000000);

Nvida = NvidaGpu()
gpuLoad = ""

RPC = Presence(client_id=client_id)
RPC.connect()


RPC.update(start=int(time.time()),state="On Desktop",details=winVersion)

while True:
    
    cpu = str(psutil.cpu_percent())
    ram = str(psutil.virtual_memory().percent)

    if(Nvida == True):
        GPUs = GPUtil.getGPUs()
        load = GPUs[0].load
        GPUname = GPUs[0].name
        gpuLoad = str("GPU (" + GPUname +") "+ str(load) + "%")

    print(cpu)
    RPC.update(state=("CPU (" + str(cpuType) + ") " + cpu + "% | RAM (" + str(round(ramSize)) + "GB) " + ram + "% | " + gpuLoad),start=int(startTime),details=winVersion)
    time.sleep(10)