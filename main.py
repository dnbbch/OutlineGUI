import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw
import subprocess

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(400, 700)
        self.set_title("OutlineGUI")

        # Создаем основное окно и элементы интерфейса
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)
        main_box.set_margin_start(10)
        main_box.set_margin_end(10)
        self.set_child(main_box)

        # Кнопка для подключения VPN
        connect_button = Gtk.Button(label="Connect VPN")
        connect_button.connect("clicked", self.connect_vpn)
        main_box.append(connect_button)

        # Кнопка для отключения VPN
        disconnect_button = Gtk.Button(label="Disconnect VPN")
        disconnect_button.connect("clicked", self.disconnect_vpn)
        main_box.append(disconnect_button)

        # Статус подключения VPN
        self.status_label = Gtk.Label(label="Status: Checking...")
        main_box.append(self.status_label)

        # Проверка состояния VPN при запуске
        self.check_vpn_status()

    def connect_vpn(self, button):
        # Вызов команды для подключения VPN
        try:
            result = subprocess.run(['sudo', 'vpn', 'connect'], capture_output=True, text=True)
            if result.returncode == 0:
                self.status_label.set_text("Status: Connected")
            else:
                self.status_label.set_text(f"Error: {result.stderr}")
        except Exception as e:
            self.status_label.set_text(f"Exception: {str(e)}")

    def disconnect_vpn(self, button):
        # Вызов команды для отключения VPN
        try:
            result = subprocess.run(['sudo', 'vpn', 'disconnect'], capture_output=True, text=True)
            if result.returncode == 0: 
                self.status_label.set_text("Status: Disconnected")
            else:
                self.status_label.set_text(f"Error: {result.stderr}")
        except Exception as e:
            self.status_label.set_text(f"Exception: {str(e)}")

    def check_vpn_status(self):
        # Вызов команды для проверки состояния VPN
        try:
            result = subprocess.run(['sudo', 'vpn', 'status'], capture_output=True, text=True)
            if "Connected" in result.stdout:
                self.status_label.set_text("Status: Connected")
            else:
                self.status_label.set_text("Status: Disconnected")
        except Exception as e:
            self.status_label.set_text(f"Exception: {str(e)}")

class OutlineGUIApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.example.OutlineGUI")
    
    def do_activate(self):
        win = MainWindow(application=self)
        win.present()

def main():
    app = OutlineGUIApp()
    app.run(sys.argv)

if __name__ == "__main__":
    main()
