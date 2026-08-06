import customtkinter as ctk
import subprocess
import os
import sys
import ctypes
import time
import requests
import webbrowser
from tkinter import messagebox
from threading import Thread

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CURRENT_VERSION = "1.0.7"
GITHUB_REPO = "dimacmirnov41-netizen/hux-huxLauncher"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

class SplashScreen(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("")
        self.geometry("400x320")
        self.resizable(False, False)
        self.overrideredirect(True)
        self.configure(fg_color=("#0a0a1a", "#0d0d2b"))
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 200
        y = (self.winfo_screenheight() // 2) - 160
        self.geometry(f"+{x}+{y}")
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0] if getattr(sys, 'frozen', False) else __file__)), "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except:
            pass
        
        self.title_label = ctk.CTkLabel(self, text="ZAPRET LAUNCHER", font=ctk.CTkFont(size=36, weight="bold"), text_color="#00d4ff")
        self.title_label.pack(pady=(50, 5))
        
        self.version_label = ctk.CTkLabel(self, text=f"Версия {CURRENT_VERSION}", font=ctk.CTkFont(size=16), text_color="#718096")
        self.version_label.pack(pady=(0, 15))
        
        self.status_label = ctk.CTkLabel(self, text="Загрузка...", font=ctk.CTkFont(size=13), text_color="#a0aec0")
        self.status_label.pack(pady=(10, 5))
        
        self.progress = ctk.CTkProgressBar(self, width=300, height=8, corner_radius=4, fg_color="#2d3748", progress_color="#00d4ff")
        self.progress.pack(pady=(15, 0))
        self.progress.set(0)
        
        self.steps = [
            "Загрузка иконок...",
            "Проверка обновлений...",
            "Загрузка конфигурации...",
            "Подготовка интерфейса...",
            "Запуск..."
        ]
        self.current_step = 0
        self.start_time = time.time()
        self.animate_progress()
    
    def animate_progress(self):
        elapsed = time.time() - self.start_time
        total_time = 5.0
        progress = min(elapsed / total_time, 1.0)
        self.progress.set(progress)
        
        step_index = int(progress * len(self.steps))
        if step_index >= len(self.steps):
            step_index = len(self.steps) - 1
        if step_index != self.current_step:
            self.current_step = step_index
            self.status_label.configure(text=self.steps[step_index])
        
        if progress < 1.0:
            self.after(20, self.animate_progress)
        else:
            self.status_label.configure(text="Готово!")
            self.progress.set(1.0)
            self.after(300, self.destroy)

class HelpWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Документация")
        self.geometry("420x450")
        self.resizable(False, False)
        self.configure(fg_color=("#0a0a1a", "#0d0d2b"))
        self.attributes('-topmost', True)
        
        x = (self.winfo_screenwidth() // 2) - 210
        y = (self.winfo_screenheight() // 2) - 225
        self.geometry(f"+{x}+{y}")
        
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0] if getattr(sys, 'frozen', False) else __file__)), "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except:
            pass
        
        self.title_label = ctk.CTkLabel(self, text="КУДА ТЫКАТЬ", font=ctk.CTkFont(size=24, weight="bold"), text_color="#00d4ff")
        self.title_label.pack(pady=(15, 5))
        
        self.info_label = ctk.CTkLabel(self, text="В открывшейся консоли введите цифру и нажмите Enter:", font=ctk.CTkFont(size=14), text_color="#a0aec0")
        self.info_label.pack(pady=(0, 10))
        
        frame = ctk.CTkFrame(self, fg_color=("#1a1a2e", "#16213e"), corner_radius=10, border_width=1, border_color="#00d4ff")
        frame.pack(pady=5, padx=20, fill="x")
        
        items = [
            ("1", "Установить сервис"),
            ("2", "Удалить сервис"),
            ("3", "Проверить статус"),
            ("4", "Game Filter"),
            ("5", "IPSet Filter"),
            ("6", "Auto-Update"),
            ("7", "Обновить IPSet"),
            ("8", "Обновить Hosts"),
            ("9", "Проверить обновления"),
            ("10", "Диагностика"),
            ("11", "Тесты")
        ]
        
        for i, (num, desc) in enumerate(items):
            row = i // 2
            col = i % 2
            label = ctk.CTkLabel(frame, text=f"{num} -> {desc}", font=ctk.CTkFont(size=13), text_color="#a0aec0")
            label.grid(row=row, column=col, padx=10, pady=3, sticky="w")
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        
        self.close_btn = ctk.CTkButton(self, text="ПОНЯЛ, ЗАКРЫТЬ", command=self.destroy, font=ctk.CTkFont(size=14, weight="bold"), height=40, corner_radius=10, fg_color="#00b894", hover_color="#00a381")
        self.close_btn.pack(pady=(15, 15), padx=40, fill="x")

class ZapretLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title("hux-huxLauncher")
        self.geometry("550x800")
        self.resizable(False, False)
        self.configure(fg_color=("#0a0a1a", "#0d0d2b"))
        
        if getattr(sys, 'frozen', False):
            self.zapret_path = os.path.dirname(sys.executable)
        else:
            self.zapret_path = os.path.dirname(os.path.abspath(__file__))
        
        try:
            icon_path = os.path.join(self.zapret_path, "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except:
            pass
        
        self.strategies = []
        self.update_available = False
        self.latest_version = ""
        self.download_url = ""
        
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(20, 5), fill="x")
        self.title_label = ctk.CTkLabel(self.header_frame, text="HUX-HUX LAUNCHER", font=ctk.CTkFont(size=30, weight="bold"), text_color="#00d4ff")
        self.title_label.pack()
        self.version_label = ctk.CTkLabel(self.header_frame, text=f"Версия {CURRENT_VERSION} | Выберите стратегию", font=ctk.CTkFont(size=12), text_color="#718096")
        self.version_label.pack(pady=(0, 5))
        
        self.update_frame = ctk.CTkFrame(self, fg_color=("#1a1a2e", "#16213e"), corner_radius=10, border_width=1, border_color="#f39c12")
        self.update_frame.pack(pady=5, padx=25, fill="x")
        self.update_label = ctk.CTkLabel(self.update_frame, text="Проверка обновлений...", font=ctk.CTkFont(size=12), text_color="#a0aec0")
        self.update_label.pack(pady=5)
        self.update_btn = ctk.CTkButton(self.update_frame, text="ПРОВЕРИТЬ ОБНОВЛЕНИЯ", command=self.check_updates, font=ctk.CTkFont(size=12, weight="bold"), height=30, corner_radius=8, fg_color="#2d3748", hover_color="#4a5568")
        self.update_btn.pack(pady=(0, 5))
        
        self.status_frame = ctk.CTkFrame(self, fg_color=("#1a1a2e", "#16213e"), corner_radius=12, border_width=1, border_color="#00d4ff")
        self.status_frame.pack(pady=5, padx=25, fill="x")
        self.status_label = ctk.CTkLabel(self.status_frame, text="Статус: Не установлен", font=ctk.CTkFont(size=14, weight="bold"), text_color="#fc8181")
        self.status_label.pack(pady=8)
        
        self.list_frame = ctk.CTkFrame(self, fg_color=("#1a1a2e", "#16213e"), corner_radius=15, border_width=2, border_color="#00d4ff")
        self.list_frame.pack(pady=10, padx=25, fill="both", expand=True)
        self.list_label = ctk.CTkLabel(self.list_frame, text="СТРАТЕГИИ", font=ctk.CTkFont(size=14, weight="bold"), text_color="#00d4ff")
        self.list_label.pack(pady=(10, 5))
        self.scroll_frame = ctk.CTkScrollableFrame(self.list_frame, fg_color="transparent", height=280)
        self.scroll_frame.pack(pady=5, padx=10, fill="both", expand=True)
        self.load_strategies()
        
        self.settings_frame = ctk.CTkFrame(self, fg_color=("#1a1a2e", "#16213e"), corner_radius=15, border_width=2, border_color="#f39c12")
        self.settings_frame.pack(pady=10, padx=25, fill="x")
        self.settings_label = ctk.CTkLabel(self.settings_frame, text="НАСТРОЙКИ", font=ctk.CTkFont(size=14, weight="bold"), text_color="#f39c12")
        self.settings_label.pack(pady=(8, 5))
        
        self.settings_btn = ctk.CTkButton(self.settings_frame, text="ОТКРЫТЬ НАСТРОЙКИ", command=self.open_settings, font=ctk.CTkFont(size=15, weight="bold"), height=45, corner_radius=10, fg_color="#2d3748", hover_color="#4a5568", border_width=1, border_color="#f39c12")
        self.settings_btn.pack(pady=(5, 10), padx=15, fill="x")
        
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=5, padx=25, fill="x")
        self.refresh_btn = ctk.CTkButton(self.btn_frame, text="ОБНОВИТЬ СПИСОК", command=self.refresh_strategies, font=ctk.CTkFont(size=13, weight="bold"), height=35, corner_radius=10, fg_color="#4a5568", hover_color="#718096")
        self.refresh_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.remove_btn = ctk.CTkButton(self.btn_frame, text="УДАЛИТЬ СЕРВИС", command=self.remove_service, font=ctk.CTkFont(size=13, weight="bold"), height=35, corner_radius=10, fg_color="#e53e3e", hover_color="#c53030", state="disabled")
        self.remove_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)
        
        self.footer_label = ctk.CTkLabel(self, text=f"{self.zapret_path}", font=ctk.CTkFont(size=9), text_color="#4a5568")
        self.footer_label.pack(pady=(0, 10))
        
        self.after(1000, self.check_updates)
        self.after(500, self.check_status)
    
    def compare_versions(self, v1, v2):
        v1_parts = [int(x) for x in v1.split('.')]
        v2_parts = [int(x) for x in v2.split('.')]
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_val = v1_parts[i] if i < len(v1_parts) else 0
            v2_val = v2_parts[i] if i < len(v2_parts) else 0
            if v1_val < v2_val:
                return True
            elif v1_val > v2_val:
                return False
        return False
    
    def check_updates(self):
        def check():
            try:
                self.update_label.configure(text="Проверка обновлений...", text_color="#f39c12")
                response = requests.get(GITHUB_API_URL, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    latest = data.get("tag_name", "").replace("v", "")
                    
                    if latest and self.compare_versions(CURRENT_VERSION, latest):
                        self.update_available = True
                        self.latest_version = latest
                        self.download_url = data.get("html_url", "")
                        self.update_label.configure(text=f"Доступна версия: {latest}", text_color="#48bb78")
                        self.update_btn.configure(text="СКАЧАТЬ ОБНОВЛЕНИЕ", fg_color="#00b894", hover_color="#00a381", command=self.download_update)
                    else:
                        self.update_label.configure(text="У вас последняя версия", text_color="#48bb78")
                        self.update_btn.configure(text="ПРОВЕРИТЬ ОБНОВЛЕНИЯ", fg_color="#2d3748", hover_color="#4a5568", command=self.check_updates)
                else:
                    self.update_label.configure(text="Не удалось проверить обновления", text_color="#fc8181")
            except:
                self.update_label.configure(text="Ошибка проверки обновлений", text_color="#fc8181")
        
        Thread(target=check, daemon=True).start()
    
    def download_update(self):
        if self.download_url:
            if messagebox.askyesno("Обновление", f"Доступна новая версия {self.latest_version}\n\nОткрыть страницу загрузки?"):
                webbrowser.open(self.download_url)
    
    def get_all_bat_files(self):
        files = []
        try:
            for f in os.listdir(self.zapret_path):
                full_path = os.path.join(self.zapret_path, f)
                if os.path.isfile(full_path) and f.endswith('.bat') and f.lower() != 'service.bat':
                    files.append(f)
            files.sort(key=lambda x: (0 if x.lower() == 'general.bat' else 1, x.lower()))
        except Exception as e:
            print(f"Ошибка: {e}")
        return files
    
    def load_strategies(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.strategies = self.get_all_bat_files()
        if self.strategies:
            for name in self.strategies:
                display_name = name.replace('.bat', '')
                btn = ctk.CTkButton(self.scroll_frame, text=f"> {display_name}", command=lambda n=name: self.run_strategy(n), font=ctk.CTkFont(size=12), height=35, corner_radius=8, fg_color="#2d3748", hover_color="#00b894", anchor="w", border_width=1, border_color="#4a5568")
                btn.pack(pady=2, padx=5, fill="x")
            self.list_label.configure(text=f"СТРАТЕГИИ ({len(self.strategies)})")
        else:
            label = ctk.CTkLabel(self.scroll_frame, text="Нет стратегий!\n\nПоложи .bat файлы в папку:\n" + f"{self.zapret_path}\n\nи нажми 'Обновить список'", font=ctk.CTkFont(size=13), text_color="#fc8181", justify="center")
            label.pack(pady=30)
            self.list_label.configure(text="СТРАТЕГИИ НЕ НАЙДЕНЫ")
    
    def refresh_strategies(self):
        self.load_strategies()
        self.check_status()
    
    def run_strategy(self, name):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            if not messagebox.askyesno("Права администратора", "Для запуска стратегии нужны права администратора.\n\nРазрешить запуск от имени администратора?"):
                return
            script = os.path.abspath(sys.argv[0])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", script, "", None, 1)
            self.destroy()
            return
        self.status_label.configure(text=f"Запуск: {name}...", text_color="#f39c12")
        self.update()
        try:
            full_path = os.path.join(self.zapret_path, name)
            subprocess.Popen(f'start cmd /c "{full_path}"', cwd=self.zapret_path, shell=True)
            self.status_label.configure(text=f"Запущена: {name}", text_color="#48bb78")
            self.after(3000, self.check_status)
        except Exception as e:
            self.status_label.configure(text=f"Ошибка: {str(e)[:50]}", text_color="#fc8181")
    
    def open_settings(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            messagebox.showwarning("Внимание!", "Для настроек нужны права администратора!\nПерезапустите программу от имени администратора.")
            return
        
        try:
            service_path = os.path.join(self.zapret_path, "service.bat")
            if not os.path.exists(service_path):
                messagebox.showerror("Ошибка", f"Файл service.bat не найден!\n\nПуть: {self.zapret_path}")
                return
            
            subprocess.Popen(f'start cmd /c "{service_path}" admin', cwd=self.zapret_path, shell=True)
            
            help_window = HelpWindow()
            help_window.focus()
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def check_status(self):
        try:
            result = subprocess.run('sc query "zapret"', capture_output=True, text=True, shell=True, timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode == 0:
                self.remove_btn.configure(state="normal")
                if "RUNNING" in result.stdout:
                    self.status_label.configure(text="Статус: ВКЛЮЧЕН", text_color="#48bb78")
                else:
                    self.status_label.configure(text="Статус: ВЫКЛЮЧЕН", text_color="#f39c12")
            else:
                self.remove_btn.configure(state="disabled")
                self.status_label.configure(text="Статус: НЕ УСТАНОВЛЕН", text_color="#fc8181")
        except:
            pass
    
    def remove_service(self):
        if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить сервис Zapret?"):
            return
        if not ctypes.windll.shell32.IsUserAnAdmin():
            messagebox.showwarning("Внимание!", "Для удаления нужны права администратора!\nПерезапустите программу от имени администратора.")
            return
        try:
            subprocess.run('net stop zapret', capture_output=True, shell=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run('sc delete zapret', capture_output=True, shell=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
            self.status_label.configure(text="Сервис удалён", text_color="#fc8181")
            self.after(1000, self.check_status)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    app = ZapretLauncher()
    splash = SplashScreen()
    splash.update()
    def show_main():
        app.deiconify()
        app.attributes('-topmost', True)
        app.attributes('-topmost', False)
    def check_splash():
        try:
            if not splash.winfo_exists():
                show_main()
                return
            app.after(100, check_splash)
        except:
            show_main()
    app.after(100, check_splash)
    app.mainloop()