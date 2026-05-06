import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import time
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# ---------------- CHROME SETUP (FIXED) ----------------
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("user-data-dir=whatsapp_session")

driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com")

contacts = []
running = False

# ---------------- LOAD CONTACTS ----------------
def load_contacts():
    global contacts

    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if not file_path:
        return

    try:
        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            contacts = [row['number'] for row in reader]

        status_label.config(text=f"{len(contacts)} contacts loaded")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- SEND MESSAGE ----------------
def send_message(number, message, count, delay):

    try:
        driver.get(f"https://web.whatsapp.com/send?phone={number}")
        time.sleep(10)

        box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")

        for i in range(count):
            box.send_keys(f"{message} ({i+1})")
            box.send_keys(Keys.ENTER)
            time.sleep(delay)

    except Exception as e:
        print("Error:", e)

# ---------------- SEND ALL CONTACTS ----------------
def send_all():
    global running

    if not contacts:
        messagebox.showerror("Error", "Load contacts first!")
        return

    message = message_entry.get()
    count = int(count_entry.get())
    delay = float(delay_entry.get())

    running = True

    for number in contacts:
        if not running:
            break

        status_label.config(text=f"Sending to {number}")
        send_message(number, message, count, delay)

    status_label.config(text="Done!")

# ---------------- THREAD ----------------
def start():
    threading.Thread(target=send_all).start()

def stop():
    global running
    running = False
    status_label.config(text="Stopped")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Pro WhatsApp GUI (Stable Version)")
root.geometry("450x350")

tk.Button(root, text="Load Contacts (CSV)", command=load_contacts).pack(pady=5)

tk.Label(root, text="Message").pack()
message_entry = tk.Entry(root, width=40)
message_entry.pack()

tk.Label(root, text="Repeat Count").pack()
count_entry = tk.Entry(root)
count_entry.insert(0, "2")
count_entry.pack()

tk.Label(root, text="Delay (seconds)").pack()
delay_entry = tk.Entry(root)
delay_entry.insert(0, "2")
delay_entry.pack()

tk.Button(root, text="START", command=start).pack(pady=10)
tk.Button(root, text="STOP", command=stop).pack()

status_label = tk.Label(root, text="Status: Idle")
status_label.pack(pady=10)

root.mainloop()