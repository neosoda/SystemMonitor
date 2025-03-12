import sys
import psutil
import pyqtgraph as pg
import platform
import subprocess
import socket
import requests
from collections import deque
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import QTimer, Qt, QPoint, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QMouseEvent, QFont, QColor, QLinearGradient, QPainter, QBrush
import wmi  # Pour interagir avec WMI
import os

import os
import sys
import subprocess

def get_openhardwaremonitor_path():
    if getattr(sys, 'frozen', False):
        # Chemin absolu pour le test
        return r"A:\Python\OpenHardwareMonitor.exe"
    else:
        return os.path.join(os.path.dirname(__file__), 'OpenHardwareMonitor.exe')

OPENHARDWAREMONITOR_PATH = get_openhardwaremonitor_path()

def launch_openhardwaremonitor():
    try:
        print(f"Lancement de OpenHardwareMonitor depuis : {OPENHARDWAREMONITOR_PATH}")
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        process = subprocess.Popen([OPENHARDWAREMONITOR_PATH], startupinfo=startupinfo)
        print(f"OpenHardwareMonitor lancé avec PID : {process.pid}")
        return process
    except Exception as e:
        print(f"Erreur lors du lancement d'OpenHardwareMonitor: {e}")
        return None

# Appel de la fonction pour tester
launch_openhardwaremonitor()

def init_wmi():
    try:
        return wmi.WMI(namespace=r"root\OpenHardwareMonitor")
    except Exception as e:
        print(f"Erreur lors de l'initialisation de WMI: {e}")
        return None

def get_local_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except Exception as e:
        print(f"Erreur lors de la récupération de l'IP locale: {e}")
        return "N/A"

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        return response.text if response.status_code == 200 else "N/A"
    except Exception as e:
        print(f"Erreur lors de la récupération de l'IP publique: {e}")
        return "N/A"

class SystemData:
    def __init__(self):
        self.last_sent = psutil.net_io_counters().bytes_sent
        self.last_recv = psutil.net_io_counters().bytes_recv
        self.wmi_connection = init_wmi()

    def get_cpu_temperature(self):
        if platform.system() == "Windows" and self.wmi_connection:
            try:
                for sensor in self.wmi_connection.Sensor():
                    if sensor.SensorType == "Temperature" and ("CPU" in sensor.Name or "Core" in sensor.Name):
                        return round(sensor.Value, 1)
            except Exception as e:
                print(f"Erreur lors de l'accès au capteur de température: {e}")
        elif platform.system() == "Linux":
            try:
                temp = psutil.sensors_temperatures()
                if 'coretemp' in temp:
                    return round(temp['coretemp'][0].current, 1)
            except Exception as e:
                print(f"Erreur lors de l'accès au capteur de température Linux: {e}")
        return "N/A"

    def get_system_usage(self):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        cpu_temp = self.get_cpu_temperature()

        net_counters = psutil.net_io_counters()
        sent_speed = (net_counters.bytes_sent - self.last_sent) / 1024
        recv_speed = (net_counters.bytes_recv - self.last_recv) / 1024
        self.last_sent, self.last_recv = net_counters.bytes_sent, net_counters.bytes_recv

        return cpu_usage, ram_usage, disk_usage, cpu_temp, sent_speed, recv_speed

    def get_gpu_info(self):
        if platform.system() == "Windows" and self.wmi_connection:
            try:
                gpu_usage, gpu_temp = "N/A", "N/A"
                for sensor in self.wmi_connection.Sensor():
                    if sensor.SensorType == "Load" and "GPU" in sensor.Name:
                        gpu_usage = round(sensor.Value, 1)
                    elif sensor.SensorType == "Temperature" and "GPU" in sensor.Name:
                        gpu_temp = round(sensor.Value, 1)
                return gpu_usage, gpu_temp
            except Exception as e:
                print(f"Erreur lors de la récupération des informations GPU: {e}")
        return "N/A", "N/A"

class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.themes = self.load_themes()
        self.current_theme = "Azure"
        self.system_data = SystemData()
        self.data_x = list(range(60))  # Ajoutez cette ligne pour définir data_x
        self.init_ui()
        self.init_graphs()
        self.init_timer()
        self._drag_active = False

    def load_themes(self):
        return {
            "Azure": {
                "background": "#F0F0F0",
                "text": "#0078D7",
                "button": "#0078D7",
                "button_hover": "#005A9E",
                "border": "#C0C0C0",
                "graph_background": "#FFFFFF",
                "graph_text": "#0078D7",
            },
        }

    def init_ui(self):
        self.setWindowTitle("Tableau de bord PC - Surveillance")
        self.setGeometry(100, 100, 400, 200)
        self.apply_theme()
        self.setup_layout()

    def setup_layout(self):
        self.main_layout = QVBoxLayout()
        self.add_info_sections()
        self.add_toggle_graph_button()
        self.setLayout(self.main_layout)

    def add_info_sections(self):
        self.local_ip_label = QLabel(f"IP Locale : {get_local_ip()}")
        self.public_ip_label = QLabel(f"IP Publique : {get_public_ip()}")
        self.cpu_usage_label = QLabel("Utilisation CPU : 0%")
        self.cpu_temp_label = QLabel("Température CPU : N/A")
        self.ram_label = QLabel("Utilisation RAM : 0%")
        self.disk_label = QLabel("Utilisation Disque : 0%")
        self.net_label = QLabel("Réseau : 0 Ko/s")
        self.gpu_usage_label = QLabel("Utilisation GPU : N/A")
        self.gpu_temp_label = QLabel("Température GPU : N/A")

        ip_layout = QHBoxLayout()
        ip_layout.addWidget(self.local_ip_label)
        ip_layout.addWidget(self.public_ip_label)
        self.main_layout.addLayout(ip_layout)

        cpu_layout = QHBoxLayout()
        cpu_layout.addWidget(self.cpu_usage_label)
        cpu_layout.addWidget(self.cpu_temp_label)
        self.main_layout.addLayout(cpu_layout)

        self.main_layout.addWidget(self.ram_label)
        self.main_layout.addWidget(self.disk_label)
        self.main_layout.addWidget(self.net_label)

        gpu_layout = QHBoxLayout()
        gpu_layout.addWidget(self.gpu_usage_label)
        gpu_layout.addWidget(self.gpu_temp_label)
        self.main_layout.addLayout(gpu_layout)

    def add_toggle_graph_button(self):
        self.toggle_graph_button = QPushButton("Afficher/Masquer les graphiques")
        self.toggle_graph_button.clicked.connect(self.toggle_graph)
        self.toggle_graph_button.setStyleSheet(self.get_button_style())
        self.main_layout.addWidget(self.toggle_graph_button)

    def get_button_style(self):
        theme = self.themes[self.current_theme]
        return f"""
            QPushButton {{
                background-color: {theme['button']};
                color: white;
                border: 2px solid {theme['border']};
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {theme['button_hover']};
                color: {theme['background']};
            }}
        """

    def init_graphs(self):
        self.graph = self.create_graph("Utilisation CPU (%)", "#0078D7")
        self.ram_graph = self.create_graph("Utilisation RAM (%)", "#0078D7")
        self.disk_graph = self.create_graph("Utilisation Disque (%)", "#0078D7")
        self.net_graph = self.create_graph("Utilisation Réseau (Ko/s)", "#0078D7")
        self.gpu_graph = self.create_graph("Utilisation GPU (%)", "#0078D7")

        self.main_layout.addWidget(self.graph)
        self.main_layout.addWidget(self.ram_graph)
        self.main_layout.addWidget(self.disk_graph)
        self.main_layout.addWidget(self.net_graph)
        self.main_layout.addWidget(self.gpu_graph)

        self.hide_graphs()

    def create_graph(self, title, color):
        graph = pg.PlotWidget()
        graph.setTitle(title, color=color, size="12pt")
        graph.setBackground(self.themes[self.current_theme]["graph_background"])
        graph.showGrid(x=True, y=True, alpha=0.5)
        graph.setYRange(0, 100)
        data_y = deque([0] * 60, maxlen=60)
        curve = graph.plot(self.data_x, data_y, pen=pg.mkPen(color=color, width=2))
        graph.curve = curve
        graph.data_y = data_y
        return graph

    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def update_data(self):
        cpu_usage, ram_usage, disk_usage, cpu_temp, sent_speed, recv_speed = self.system_data.get_system_usage()
        gpu_usage, gpu_temp = self.system_data.get_gpu_info()

        self.cpu_usage_label.setText(f"Utilisation CPU : {cpu_usage}%")
        self.ram_label.setText(f"Utilisation RAM : {ram_usage}%")
        self.disk_label.setText(f"Utilisation Disque : {disk_usage}%")
        self.cpu_temp_label.setText(f"Température CPU : {cpu_temp}°C")
        self.net_label.setText(f"Réseau : {recv_speed:.2f} Ko/s ↓ | {sent_speed:.2f} Ko/s ↑")
        self.gpu_usage_label.setText(f"Utilisation GPU : {gpu_usage}%")
        self.gpu_temp_label.setText(f"Température GPU : {gpu_temp}°C")

        self.update_label_colors(cpu_usage, ram_usage, disk_usage, gpu_usage)
        self.update_graphs(cpu_usage, ram_usage, disk_usage, recv_speed, gpu_usage)

    def update_label_colors(self, cpu_usage, ram_usage, disk_usage, gpu_usage):
        self.cpu_usage_label.setStyleSheet(f"color: red;" if cpu_usage > 80 else f"color: {self.themes[self.current_theme]['text']};")
        self.ram_label.setStyleSheet(f"color: red;" if ram_usage > 80 else f"color: {self.themes[self.current_theme]['text']};")
        self.disk_label.setStyleSheet(f"color: red;" if disk_usage > 90 else f"color: {self.themes[self.current_theme]['text']};")
        self.gpu_usage_label.setStyleSheet(f"color: red;" if gpu_usage != "N/A" and gpu_usage > 80 else f"color: {self.themes[self.current_theme]['text']};")

    def update_graphs(self, cpu_usage, ram_usage, disk_usage, recv_speed, gpu_usage):
        self.graph.data_y.append(cpu_usage)
        self.ram_graph.data_y.append(ram_usage)
        self.disk_graph.data_y.append(disk_usage)
        self.net_graph.data_y.append(recv_speed)
        self.gpu_graph.data_y.append(gpu_usage if gpu_usage != "N/A" else 0)

        self.graph.curve.setData(self.data_x, self.graph.data_y)
        self.ram_graph.curve.setData(self.data_x, self.ram_graph.data_y)
        self.disk_graph.curve.setData(self.data_x, self.disk_graph.data_y)
        self.net_graph.curve.setData(self.data_x, self.net_graph.data_y)
        self.gpu_graph.curve.setData(self.data_x, self.gpu_graph.data_y)

    def toggle_graph(self):
        if self.graph.isVisible():
            self.hide_graphs()
        else:
            self.show_graphs()

    def show_graphs(self):
        self.graph.setVisible(True)
        self.ram_graph.setVisible(True)
        self.disk_graph.setVisible(True)
        self.net_graph.setVisible(True)
        self.gpu_graph.setVisible(True)
        self.animate_resize(QRect(self.x(), self.y(), 600, 700))

    def hide_graphs(self):
        self.graph.setVisible(False)
        self.ram_graph.setVisible(False)
        self.disk_graph.setVisible(False)
        self.net_graph.setVisible(False)
        self.gpu_graph.setVisible(False)
        self.animate_resize(QRect(self.x(), self.y(), 400, 200))

    def animate_resize(self, target_rect):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(target_rect)
        self.animation.start()

    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['background']};
                color: {theme['text']};
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 14px;
                border-radius: 8px;
                border: 1px solid {theme['border']};
            }}
            QLabel {{
                color: {theme['text']};
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton {{
                background-color: {theme['button']};
                color: white;
                border: 2px solid {theme['border']};
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {theme['button_hover']};
                color: {theme['background']};
            }}
        """)

    def closeEvent(self, event):
        if openhardwaremonitor_process:
            openhardwaremonitor_process.terminate()
        event.accept()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_start_pos = event.pos()
            self._window_start_pos = self.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_active:
            self.move(self._window_start_pos + event.pos() - self._drag_start_pos)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_active = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    openhardwaremonitor_process = launch_openhardwaremonitor()
    monitor = SystemMonitor()
    monitor.show()
    sys.exit(app.exec_())
