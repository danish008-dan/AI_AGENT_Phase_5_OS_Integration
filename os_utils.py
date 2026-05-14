# os_layer/os_utils.py

import subprocess
import webbrowser
import os
import psutil
from datetime import datetime
import pyautogui


# -----------------------------
# OPEN APPLICATION
# -----------------------------
def open_application(app_name):

    if "chrome" in app_name:
        subprocess.Popen("start chrome", shell=True)
        return "Opening Chrome"

    if "notepad" in app_name:
        subprocess.Popen("notepad", shell=True)
        return "Opening Notepad"

    if "calculator" in app_name:
        subprocess.Popen("calc", shell=True)
        return "Opening Calculator"

    return None


# -----------------------------
# OPEN WEBSITE
# -----------------------------
def open_website(url):

    if not url.startswith("http"):
        url = "https://" + url

    webbrowser.open(url)

    return f"Opening {url}"


# -----------------------------
# SYSTEM STATUS
# -----------------------------
def system_status():

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    return f"CPU usage {cpu} percent and RAM usage {ram} percent"


# -----------------------------
# SYSTEM TIME
# -----------------------------
def get_time():

    return datetime.now().strftime("%H:%M")


# -----------------------------
# VOLUME CONTROL
# -----------------------------
def volume_up():
    pyautogui.press("volumeup", presses=5)
    return "Volume increased"


def volume_down():
    pyautogui.press("volumedown", presses=5)
    return "Volume decreased"