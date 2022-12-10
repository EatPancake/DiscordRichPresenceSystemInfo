from pypresence import Presence
import time
import platform
import psutil

client_id = "1050923361527664751"

winsystem = str(platform.system())
winversion = str(platform.release())

winVersion = winsystem + " " + winversion

startTime = int(time.time())

RPC = Presence(client_id=client_id)
RPC.connect()


RPC.update(start=int(time.time()),state="On Desktop",details=winVersion)

while True:
    
    cpu = str(psutil.cpu_percent())
    ram = str(psutil.virtual_memory().percent)

    print(cpu)
    RPC.update(state=("CPU " + cpu + "% RAM " + ram + "%"),start=int(startTime),details=winVersion)
    time.sleep(10)

i = input("no");