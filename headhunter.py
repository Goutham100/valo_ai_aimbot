import threading
import serial
from ultralytics import YOLO
import cv2
import numpy as np
import mss
import win32gui
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import serial.tools.list_ports
import time
import pyautogui
import random
running_flag = threading.Event()
def get_active_window_title():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

def aimbot():
    global arduino
    try:
        # Initialize Serial Communication
        arduino = serial.Serial(port='COM6', baudrate=115200, timeout=1)
    except serial.SerialException:
        return

    model = YOLO("ValBest_small.engine")
    sct = mss.mss()
    monitor = sct.monitors[1]
    
    screen_width = monitor["width"]
    screen_height = monitor["height"]

    region_width = 320
    region_height = 320
    region = {
        "top": (screen_height - region_height) // 2,
        "left": (screen_width - region_width) // 2,
        "width": region_width,
        "height": region_height,
    }

    print(f"Capturing region: {region}")

    screen_mid_x = region["left"] + region_width / 2
    screen_mid_y = region["top"] + region_height / 2
    threshold = 5
    while running_flag.is_set():
        active_window = get_active_window_title()
        if "VALORANT" in active_window.upper():
            print(f"Active window: {active_window}")
            screenshot = np.array(sct.grab(region))
            frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            results = model.predict(frame, imgsz=672, conf=0.25, device=0)
            target_box = None
            min_distance = float('inf')

            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]

                    if class_name == "enemy_head":
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        bbox_center_x = (x1 + x2) / 2
                        bbox_center_y = (y1 + y2) / 2

                        screen_x = int(region["left"] + bbox_center_x)
                        screen_y = int(region["top"] + bbox_center_y)

                        dx = screen_x - screen_mid_x
                        dy = screen_y - screen_mid_y
                        distance = dx * dx + dy * dy

                        if distance < min_distance:
                            min_distance = distance
                            target_box = (screen_x, screen_y)

            if target_box:
                screen_x, screen_y = target_box
                relative_x = screen_x - screen_mid_x
                relative_y = screen_y - screen_mid_y

                sensitivity = 0.8
                relative_x *= sensitivity
                relative_y *= sensitivity

                print(f"Shooting at {relative_x},{relative_y}")
                try:
                    arduino.write(f"M:{int(relative_x)},{int(relative_y)}\n".encode())
                    if (
                            abs(screen_x - screen_mid_x) <= threshold
                            and abs(screen_y - screen_mid_y) <= threshold
                    ):
                        arduino.write("C\n".encode())



                        
                except Exception as e:
                    print(f"Serial write error: {e}")

        else:
            continue

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    arduino.close()
def stop_bot():
    if not running_flag.is_set():
        messagebox.showinfo("Info", "Bot is not running.")
        return

    print("Bot Paused...",flush=True)

    try:
        if arduino and arduino.is_open:
            arduino.close()
    except Exception as e:
        print(f"Error while closing Arduino: {e}")

    running_flag.clear()
    messagebox.showinfo("Stopped", "Bot has been stopped.")
def on_closing():
    print("Exiting...")
    running_flag.clear()
    try:
        if arduino is globals() and arduino and arduino.is_open:
            arduino.close()
            print("Arduino connection closed.")
    except Exception as e:
        print(f"Closing Bot")
    root.destroy()
def start_bot_threaded():
    if running_flag.is_set():
        messagebox.showinfo("Info", "Bot is already running.")
        return
    running_flag.set()
    threading.Thread(target=aimbot, daemon=True).start()

start_bot_threaded()


root = tk.Tk()
root.title("HeadHunter.exe")
root.geometry("400x250")
root.geometry("420x450")
root.configure(bg="#101820")
root.resizable(False, False)
root.iconbitmap("images/kayo.ico")


label_font = ("Consolas", 11, "bold")
dropdown_font = ("Consolas", 10)
button_font = ("Consolas", 11, "bold")

neon_green = "#39FF14"
neon_red = "#FF3131"
neon_blue = "#00FFFF"
frame_border = "#00ffcc"


frame = tk.Frame(root, bg=frame_border, bd=3)
frame.place(relx=0.5, rely=0.5, anchor="center", width=390, height=420)

inner = tk.Frame(frame, bg="#101820")
inner.pack(fill="both", expand=True, padx=5, pady=5)



valo_img = Image.open("images/valorant_logo.png")
valo_img = valo_img.resize((80, 80), Image.Resampling.LANCZOS)
valo_photo = ImageTk.PhotoImage(valo_img)

logo_label = tk.Label(inner, image=valo_photo, bg="#101820")
logo_label.image = valo_photo  # Keep a reference
logo_label.pack(pady=(10, 0))

tk.Label(inner, text="🖧 Select Port", bg="#101820", fg=neon_blue, font=label_font).pack(pady=(15, 5))

selected_port = tk.StringVar(value="Select Port")
ports = serial.tools.list_ports.comports()
if ports:
    selected_port.set(ports[0].device)  # Default to first available port
    port_dropdown = tk.OptionMenu(inner, selected_port, *[port.device for port in ports])
else:
    selected_port.set("No Ports Available")
    print("No serial ports found. Please connect your Arduino.")
    port_dropdown = tk.OptionMenu(inner, selected_port, "No Ports Available")
port_dropdown.config(bg="#1f1f2e", fg=neon_green, font=dropdown_font, width=25, highlightthickness=0, bd=0, activebackground="#2c2c3c")
port_dropdown["menu"].config(bg="#1f1f2e", fg=neon_green, font=dropdown_font)
port_dropdown.pack()


start_btn = tk.Button(inner, text="▶ START BOT", command=start_bot_threaded,
                      bg=neon_green, fg="black", font=button_font, height=2, width=25,
                      activebackground="#00cc77", bd=0)
start_btn.pack(pady=20)

stop_btn = tk.Button(inner, text="⏸ PAUSE BOT", command=stop_bot,
                     bg=neon_red, fg="white", font=button_font, height=2, width=25,
                     activebackground="#cc0000", bd=0)
stop_btn.pack()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()