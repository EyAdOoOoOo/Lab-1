import tkinter as tk
from tkinter import messagebox
import random
import time
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class IoTDeviceSimulator:
    def __init__(self, root):
        # Device parameters
        self.mode = "Manual"
        self.sensor_value = 100  # Initial moisture value (0-100%)
        self.actuator_state = "OFF"
        self.critical_threshold = 30  # Moisture threshold for automatic mode
        self.is_running = True
        self.update_period = 10  # Time interval for sensor updates (seconds)
        
        # GUI setup
        self.root = root
        self.root.title("IoT Device Simulator")
        
        # Mode selection
        tk.Label(root, text="Mode:").grid(row=0, column=0)
        self.mode_var = tk.StringVar(value="Manual")
        self.manual_button = tk.Radiobutton(root, text="Manual", variable=self.mode_var, value="Manual", command=self.set_mode)
        self.auto_button = tk.Radiobutton(root, text="Automatic", variable=self.mode_var, value="Automatic", command=self.set_mode)
        self.manual_button.grid(row=0, column=1)
        self.auto_button.grid(row=0, column=2)
        
        # Sensor display
        tk.Label(root, text="Soil Moisture:").grid(row=1, column=0)
        self.sensor_label = tk.Label(root, text=f"{self.sensor_value}%")
        self.sensor_label.grid(row=1, column=1)
        
        # Actuator controls
        tk.Label(root, text="Pump State:").grid(row=2, column=0)
        self.actuator_label = tk.Label(root, text=self.actuator_state)
        self.actuator_label.grid(row=2, column=1)
        self.start_button = tk.Button(root, text="Start Pump", command=self.start_pump)
        self.start_button.grid(row=3, column=0)
        self.stop_button = tk.Button(root, text="Stop Pump", command=self.stop_pump)
        self.stop_button.grid(row=3, column=1)
        
        # Plot setup
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Soil Moisture Levels")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Moisture (%)")
        self.times = [0]
        self.moisture_values = [self.sensor_value]
        self.canvas = FigureCanvasTkAgg(self.fig, root)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=3)
        
        # Background thread for sensor updates
        self.update_thread = Thread(target=self.update_sensor_values)
        self.update_thread.daemon = True
        self.update_thread.start()
        
    def set_mode(self):
        self.mode = self.mode_var.get()
        messagebox.showinfo("Mode Changed", f"Device is now in {self.mode} mode.")
    
    def start_pump(self):
        self.actuator_state = "ON"
        self.update_actuator_label()
    
    def stop_pump(self):
        self.actuator_state = "OFF"
        self.update_actuator_label()
    
    def update_actuator_label(self):
        self.actuator_label.config(text=self.actuator_state)
    
    def update_sensor_values(self):
        while self.is_running:
            time.sleep(self.update_period)
            
            # Decrease moisture naturally over time
            if self.actuator_state == "OFF":
                self.sensor_value -= random.randint(5, 10)
            elif self.actuator_state == "ON":
                self.sensor_value += random.randint(10, 15)
            
            # Clamp sensor value between 0 and 100
            self.sensor_value = max(0, min(100, self.sensor_value))
            self.sensor_label.config(text=f"{self.sensor_value}%")
            
            # Automatic mode logic
            if self.mode == "Automatic" and self.sensor_value <= self.critical_threshold:
                self.actuator_state = "ON"
                self.update_actuator_label()
            elif self.mode == "Automatic" and self.sensor_value > self.critical_threshold + 10:
                self.actuator_state = "OFF"
                self.update_actuator_label()
            
            # Update plot
            self.times.append(self.times[-1] + self.update_period)
            self.moisture_values.append(self.sensor_value)
            self.ax.clear()
            self.ax.plot(self.times, self.moisture_values, label="Soil Moisture")
            self.ax.set_title("Soil Moisture Levels")
            self.ax.set_xlabel("Time (s)")
            self.ax.set_ylabel("Moisture (%)")
            self.canvas.draw()

def main():
    root = tk.Tk()
    app = IoTDeviceSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
