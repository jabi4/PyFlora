import tkinter as tk
import paho.mqtt.client as mqtt

class SensorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Sensor App")

        # Inicijalizacija MQTT klijenta
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("mqtt.server.com", 1883, 60)
        self.mqtt_client.subscribe("sensor/data")

        # Stvaranje oznaka za prikaz podataka senzora
        self.moisture_label = tk.Label(root, text="Vlažnost zemlje: N/A")
        self.moisture_label.pack()
        self.ph_label = tk.Label(root, text="PH vrijednost zemlje: N/A")
        self.ph_label.pack()
        self.salinity_label = tk.Label(root, text="Salinitet zemlje: N/A")
        self.salinity_label.pack()
        self.light_level_label = tk.Label(root, text="Razina svjetla: N/A")
        self.light_level_label.pack()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()
        data_dict = json.loads(data)
        self.moisture_label.config(text="Vlažnost zemlje: " + str(data_dict['moisture']))
        self.ph_label.config(text="PH vrijednost zemlje: " + str(data_dict['ph']))
        self.salinity_label.config(text="Salinitet zemlje: " + str(data_dict['salinity']))
        self.light_level_label.config(text="Razina svjetla: " + str(data_dict['light_level']))

if __name__ == "__main__":
    root = tk.Tk()
    app = SensorApp(root)
    root.mainloop()
