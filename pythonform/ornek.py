import tkinter as tk
from tkinter import messagebox, Toplevel
import serial
import time
import json
import os
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from datetime import datetime

SERIAL_PORT = 'COM4'
BAUD_RATE = 9600
USER_DATA_FILE = 'user_data.json'

# Global değişkenler
bpm_values = []
countdown_time = 30  # 30 saniyelik geri sayım süresi

def read_bpm_from_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        time.sleep(2)

        temp_bpm_values = []
        start_time = time.time()

        while time.time() - start_time < 10:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if 'BPM:' in line:
                    parts = line.split()
                    try:
                        bpm_index = parts.index('BPM:') + 1
                        bpm = int(parts[bpm_index])
                        temp_bpm_values.append(bpm)
                    except (ValueError, IndexError):
                        pass
        
        ser.close()

        filtered_bpm_values = filter_bpm_values(temp_bpm_values)
        if filtered_bpm_values:
            correct_bpm = calculate_average_bpm(filtered_bpm_values)
            return correct_bpm
        else:
            return None
    except Exception as e:
        messagebox.showerror("Hata", f"Seri port hatası: {e}")
        return None

def filter_bpm_values(bpm_values):
    MIN_BPM = 60
    MAX_BPM = 100
    return [bpm for bpm in bpm_values if MIN_BPM <= bpm <= MAX_BPM]

def calculate_average_bpm(bpm_values):
    if bpm_values:
        return sum(bpm_values) / len(bpm_values)
    return None

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        if not os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'w') as f:
                json.dump({}, f)
        
        with open(USER_DATA_FILE, 'r') as f:
            users = json.load(f)
        
        if username in users and users[username]['password'] == password:
            messagebox.showinfo("Hoşgeldiniz", f"Hoşgeldiniz {username}!")
            show_welcome_screen(username)
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")
    else:
        messagebox.showwarning("Uyarı", "Kullanıcı adı veya şifre boş olamaz.")

def register_user():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        if not os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'w') as f:
                json.dump({}, f)
        
        with open(USER_DATA_FILE, 'r') as f:
            users = json.load(f)
        
        if username in users:
            messagebox.showwarning("Uyarı", "Kullanıcı zaten mevcut.")
        else:
            users[username] = {"password": password, "measurements": []}
            with open(USER_DATA_FILE, 'w') as f:
                json.dump(users, f)
            messagebox.showinfo("Başarılı", "Kullanıcı kaydedildi.")
            show_welcome_screen(username)
    else:
        messagebox.showwarning("Uyarı", "Kullanıcı adı veya şifre boş olamaz.")

def show_welcome_screen(username):
    login_frame.pack_forget()
    welcome_frame.pack()
    username_label.config(text=f"Hoşgeldiniz {username}!")
    measure_bpm_button.config(command=lambda: measure_bpm(username))

def measure_bpm(username):
    messagebox.showinfo("Bilgi", "Lütfen elinizi sensöre koyun ve süreyi izleyin...")
    countdown_label.config(text="30")
    countdown(30, username)

def countdown(time_left, username):
    if time_left > 0:
        countdown_label.config(text=f"Kalan Süre: {time_left} saniye")
        root.after(1000, countdown, time_left - 1, username)
    else:
        bpm = read_bpm_from_serial()
        if bpm is not None:
            result_label.config(text=f"Doğru nabız: {bpm} BPM")
            save_bpm(username, bpm)
            bpm_values.append(bpm)
            plot_bpm_data()
        else:
            result_label.config(text="Yeterli veri yok.")

def save_bpm(username, bpm):
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            users = json.load(f)
        
        if username in users:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            users[username]['measurements'].append({"bpm": bpm, "timestamp": now})
            with open(USER_DATA_FILE, 'w') as f:
                json.dump(users, f)

def show_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            users = json.load(f)
        
        username = username_entry.get()
        if username in users:
            user_data = users[username]['measurements']
            if user_data:
                new_window = Toplevel(root)
                new_window.title(f"{username} - Önceki Ölçümler")
                for idx, data in enumerate(user_data):
                    measurement_label = tk.Label(new_window, text=f"{idx + 1}. Ölçüm: {data['bpm']} BPM, Tarih: {data['timestamp']}")
                    measurement_label.pack()
                
                return_button = tk.Button(new_window, text="Nabız Ölçmeye Dön", command=new_window.destroy)
                return_button.pack()
            else:
                messagebox.showinfo("Bilgi", "Önceki ölçüm verisi yok.")
        else:
            messagebox.showwarning("Uyarı", "Kullanıcı bulunamadı.")
    else:
        messagebox.showwarning("Uyarı", "Kullanıcı verileri mevcut değil.")

def plot_bpm_data():
    plt.clf()  # Mevcut grafiği temizle
    plt.plot(bpm_values, marker='o')
    plt.title('Kalp Atış Verileri')
    plt.xlabel('Ölçüm Zamanı')
    plt.ylabel('BPM')
    plt.grid(True)

    canvas = tkagg.FigureCanvasTkAgg(plt.gcf(), master=welcome_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def exit_program():
    messagebox.showinfo("Çıkış", "Sağlıkla kalın!")
    root.destroy()

# GUI oluşturma
root = tk.Tk()
root.title("Nabız Ölçüm Programı")

login_frame = tk.Frame(root)
login_frame.pack()

username_label = tk.Label(login_frame, text="Kullanıcı Adı:")
username_label.pack()

username_entry = tk.Entry(login_frame)
username_entry.pack()

password_label = tk.Label(login_frame, text="Şifre:")
password_label.pack()

password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()

login_button = tk.Button(login_frame, text="Giriş Yap", command=login)
login_button.pack()

register_button = tk.Button(login_frame, text="Kayıt Ol", command=register_user)
register_button.pack()

welcome_frame = tk.Frame(root)

welcome_label = tk.Label(welcome_frame, text="Hoşgeldiniz!")
welcome_label.pack()

countdown_label = tk.Label(welcome_frame, text="")  # Geri sayım göstermek için etiket
countdown_label.pack()

measure_bpm_button = tk.Button(welcome_frame, text="Nabzı Ölç", command=lambda: measure_bpm(username_entry.get()))
measure_bpm_button.pack()

result_label = tk.Label(welcome_frame, text="")
result_label.pack()

show_user_data_button = tk.Button(welcome_frame, text="Kullanıcı Verilerini Göster", command=show_user_data)
show_user_data_button.pack()

exit_button = tk.Button(welcome_frame, text="Çıkış", command=exit_program)
exit_button.pack()

root.mainloop()
