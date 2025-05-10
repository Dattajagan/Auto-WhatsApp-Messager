import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import pywhatkit as kit
import pyautogui
from datetime import datetime, timedelta
import time

light_theme = {
    'bg': '#ffffff',       
    'fg': '#333333',
    'btn_bg': '#4CAF50',
    'btn_fg': '#ffffff',
    'entry_bg': '#ffffff',
    'entry_fg': '#000000'
}


dark_theme = {
    'bg': '#1e1e1e',
    'fg': '#ffffff',
    'btn_bg': '#007acc',
    'btn_fg': '#ffffff',
    'entry_bg': '#2d2d2d',
    'entry_fg': '#ffffff'
}

current_theme = light_theme

def apply_theme():
    root.configure(bg=current_theme['bg'])
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button, tk.Text, tk.Entry)):
            widget.configure(bg=current_theme.get('bg'), fg=current_theme.get('fg'))
            if isinstance(widget, tk.Button):
                widget.configure(bg=current_theme.get('btn_bg'), fg=current_theme.get('btn_fg'))
            elif isinstance(widget, (tk.Text, tk.Entry)):
                widget.configure(bg=current_theme.get('entry_bg'), fg=current_theme.get('entry_fg'))

def toggle_theme():
    global current_theme
    current_theme = dark_theme if current_theme == light_theme else light_theme
    apply_theme()

def send_instant():
    number = entry_number.get()
    message = entry_message.get("1.0", tk.END).strip()
    try:
        kit.sendwhatmsg_instantly(number, message, wait_time=20, tab_close=False)
        time.sleep(10)
        pyautogui.press('enter')
        messagebox.showinfo("Success", "Message sent instantly!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def send_scheduled():
    number = entry_number.get()
    message = entry_message.get("1.0", tk.END).strip()
    try:
        now = datetime.now() + timedelta(minutes=2)
        kit.sendwhatmsg(number, message, now.hour, now.minute)
        messagebox.showinfo("Success", "Message scheduled successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def send_bulk():
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    try:
        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                number = row['phone']
                message = row['message']
                now = datetime.now() + timedelta(minutes=2 + index * 1)
                kit.sendwhatmsg(number, message, now.hour, now.minute)
        messagebox.showinfo("Success", "Bulk messages scheduled!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def send_image():
    number = entry_number.get()
    message = entry_message.get("1.0", tk.END).strip()
    image_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if not image_path:
        return
    try:
        kit.sendwhats_image(number, image_path, '', tab_close=False, wait_time=15)
        time.sleep(12)
        pyautogui.click(500, 700)  # Adjust screen x, y according to your display
        time.sleep(1)
        pyautogui.write(message)
        pyautogui.press('enter')
        messagebox.showinfo("Success", "Image and message sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("WAutoMsg - WhatsApp Messenger 💬")
root.geometry("470x460")

tk.Label(root, text="📱 Phone Number (with +91):").pack(pady=5)
entry_number = tk.Entry(root, width=40)
entry_number.pack(pady=5)

tk.Label(root, text="💬 Message:").pack(pady=5)
entry_message = tk.Text(root, height=5, width=40)
entry_message.pack(pady=5)

tk.Button(root, text="Send Instantly", command=send_instant, width=25).pack(pady=5)
tk.Button(root, text="Send Scheduled (2 min later)", command=send_scheduled, width=25).pack(pady=5)
tk.Button(root, text="Send Bulk from CSV", command=send_bulk, width=25).pack(pady=5)
tk.Button(root, text="Send Image + Message", command=send_image, width=25).pack(pady=5)
tk.Button(root, text="🌙 Toggle Theme", command=toggle_theme, width=25).pack(pady=10)

apply_theme()
root.mainloop()
