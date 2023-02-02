import os
import sys
import time
import base64
import pystray
import threading
import screeninfo
import subprocess
import tkinter as tk
from PIL import Image

icon = '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S5r3iOiL/XUPlJSU4LqLMJzgi9z8xStyFp8esKlWSuweLJgFumjPNHXM+qbcYphrG9BN+qBnh4b9qkYDmZkb2mQimGnX8a/TuQuLi4sNuyONHdrwyyuyq7dGO28Wakure8/c/wQ6fEq6pbyyNjfW35tLHQLbReytt97qsrx08JZyR+oQbYkplFv3eC78nRW5/7N+/foMvW0VFRVJozLP/tx1R43Q8mbhjNM819Cp39GKJMNS22233dY47eqKidOHn5raKcnREq28mZmWVu96vR2UfeNqnXICfXu0AdXRCEMH3YvUqlWrMtae7vlKmS11CBH5d1B1T/MGFyL1Ramcx+10Y8deJ6pOjySirXrb7Nu5ZVdOafWBs02dBhut18Ov86zmfcN9U/y+63j266tXrx48depUm97+jB492kZEa7Zt2/bOqQph0NELSeOa7aw751zknETi3LU2TsSJc+JEsuwUZFmm2kZr3vm6Tjc02jtYSWf7hg9PNthXveW8N9l0HyVz/zxwuHEmEf09zI8eTMDdBy5Cq1evTi4+lTt/X0P3mUT+QUQVMPSm6VyYno6zl2dc+Kio/7nxhYWF9XrbnvPnLbO3nem/xEwwM71vit+18xddvv/WJx+6871InMelS5dmHC9LHvb5ifyXL9R1Hh7OCIVA57Xm3Ick2Wvd73tGYRAlWh0tv304v+uUKVMaI3FcgKroRWnHuYx79td3n2n21j1+1U8id1XK/7kAB6q731hWz6822vaIrJrijARbXTh5s3D6m316MnfeunXrItKxddasWbXPzinaUXT11yNv6LN/pum8mdGxk2I6ETkd9Yrnr3pGYYhkdyQllZY15kXvGxN/ENguMo/P3Vz0YXXfeWbzZrrBLMittD8+lztnw4YNut+N6dOnN13b/dTPw8mbhdPf7Gxtx35HLyTeEMlzOnv2bPsrz965/IZ+B+4JljcL2OVDG+DJNwJDUObbSKTT51uui8oXJk4hsF1Enpq36cbN5f3XtNnzNA36mx2oyhxT3yz3MdqPYVnVG9ItzfXRGqe553T3Z4uLi62RPr/D+9Qv/W6vb58kE0ErWCup01anc4NN36u0XEZgiyAEtovEnxYUD91U2mejXteFYMHMzDhNbavmwYr00Ub7Mn369NqRWaceM92BtZX9zY6WdR5ZWi1fHulzPGPGDD6sd+mS1MRm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'


icon_file = "icon.png"
if not os.path.exists(icon_file):
    icondata = base64.b64decode(icon)
    iconfile = open(icon_file,"wb")
    iconfile.write(icondata)
    iconfile.close()
    del icondata

class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
 
    def start(self):
        self.__run_backup = self.run
        self.run = self.__run         
        threading.Thread.start(self)
 
    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup
 
    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None
 
    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace
 
    def kill(self):
        self.killed = True

def restartTaskbarX():
    subprocess.Popen('\"C:\Program Files\TaskbarX\TaskbarX.exe\" -stop', shell=False)
    time.sleep(.1)
    subprocess.Popen('\"C:\Program Files\TaskbarX\TaskbarX.exe\" -tbs=1 -color=0;0;0;50 -tpop=100 -tsop=100 -as=cubiceaseinout -obas=cubiceaseinout -tbr=0 -asp=300 -ptbo=0 -stbo=0 -lr=400 -oblr=400 -sr=0 -sr2=0 -sr3=0 -ftotc=1 -rzbt=1', shell=False)
    time.sleep(.1)

def checkMonitor():
    prev = screeninfo.get_monitors()
    while True:
        time.sleep(1)
        current = screeninfo.get_monitors()
        if current != prev:
            time.sleep(5)
            prev = current
            restartTaskbarX()

def openTaskbarX():
    subprocess.Popen('\"C:\Program Files\TaskbarX\TaskbarX Configurator.exe\"', shell=False)

def minimizeTA():
    window.withdraw()
    traysystem = pystray.Icon("TaskbarX Tools", Image.open(icon_file), "TaskbarX Tools",
                    menu=pystray.Menu(
                        pystray.MenuItem("Open", tray_system_click),
                        pystray.MenuItem("Restart TaskbarX", tray_system_click),
                        pystray.MenuItem("Exit", tray_system_click)
                ))
    traysystem.run()

def exitTA():
    background_thread.kill()
    window.destroy()

def tray_system_click(traysystem, query):
    if str(query) == "Open":
        traysystem.stop()
        window.deiconify()
        window.attributes("-topmost", True)
    elif str(query) == "Restart TaskbarX":
        subprocess.Popen('\"C:\Program Files\TaskbarX\TaskbarX.exe\" -stop', shell=False)
        time.sleep(.1)
        subprocess.Popen('\"C:\Program Files\TaskbarX\TaskbarX.exe\" -tbs=1 -color=0;0;0;50 -tpop=100 -tsop=100 -as=cubiceaseinout -obas=cubiceaseinout -tbr=0 -asp=300 -ptbo=0 -stbo=0 -lr=400 -oblr=400 -sr=0 -sr2=0 -sr3=0 -ftotc=1 -rzbt=1', shell=False)
        time.sleep(.1)
    elif str(query) == "Exit":
        traysystem.stop()
        exitTA()



background_thread = thread_with_trace(target=checkMonitor)
background_thread.start()

window = tk.Tk()
window.title("TaskbarX Tools")
window.iconphoto(False, tk.PhotoImage(file = icon_file))
window.protocol("WM_DELETE_WINDOW", exitTA)

greeting = tk.Label(text="TaskbarX Tools").grid(column=1,row=1, sticky='nesw')
button1 = tk.Button(text="Open TaskbarX Configurator",
                    command = openTaskbarX
                    ).grid(column=1,row=2, sticky='nesw')
button2 = tk.Button(text="Restart TaskbarX",
                    command = restartTaskbarX
                    ).grid(column=1,row=3, sticky='nesw')
button3 = tk.Button(text="Minimize",
                    command = minimizeTA
                    ).grid(column=1,row=4, sticky='nesw')
button4 = tk.Button(text="Exit",
                    command = exitTA,
                    bg='#FF605C'
                    ).grid(column=1,row=5, sticky='nesw')
window.mainloop()