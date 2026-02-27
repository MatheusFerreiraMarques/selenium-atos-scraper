import os 
from datetime import datetime

file = None

def setup_logs():
    global file
    logdir = f"./rpalog/{datetime.now()}.log"
    os.makedirs(os.path.dirname(logdir), exist_ok=True)
    file = open(logdir, "w")

def log(msg, type="info"):
    msgstr = f"[{type}][{datetime.now()}] {msg}"
    if file != None:
        file.write(msgstr + "\n")
    print(msgstr)

def close_file():
    if file:
        file.close()