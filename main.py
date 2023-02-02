import sys
import time
import pystray
import threading
import screeninfo
import subprocess
import tkinter as tk
from PIL import Image

icon_file = 'icon.png'

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