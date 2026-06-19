import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import threading
import json
import random
import time
from datetime import datetime
from queue import Queue


BROKER = "localhost"
PORT = 1883


class MQTTToolbox:

    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Toolbox")
        self.root.geometry("900x650")

        self.client = mqtt.Client()
        self.connected = False
        self.queue = Queue()

        self.build_ui()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.root.after(100, self.process_messages)


    def build_ui(self):

        connection = ttk.LabelFrame(
            self.root,
            text="Broker"
        )
        connection.pack(fill="x", padx=10, pady=5)

        self.status = ttk.Label(
            connection,
            text="Disconnected"
        )
        self.status.pack(side="left", padx=10)

        ttk.Button(
            connection,
            text="Connect",
            command=self.connect
        ).pack(side="right", padx=10)


        publish = ttk.LabelFrame(
            self.root,
            text="Publish"
        )
        publish.pack(fill="x", padx=10, pady=5)

        self.pub_topic = ttk.Entry(publish)
        self.pub_topic.insert(0, "test/topic")
        self.pub_topic.pack(fill="x")

        self.pub_msg = tk.Text(
            publish,
            height=4
        )
        self.pub_msg.pack(fill="x")

        ttk.Button(
            publish,
            text="Publish",
            command=self.publish
        ).pack(pady=5)


        subscribe = ttk.LabelFrame(
            self.root,
            text="Subscribe"
        )
        subscribe.pack(fill="x", padx=10, pady=5)

        self.sub_topic = ttk.Entry(subscribe)
        self.sub_topic.insert(0, "#")
        self.sub_topic.pack(side="left", fill="x", expand=True)

        ttk.Button(
            subscribe,
            text="Subscribe",
            command=self.subscribe
        ).pack(side="right")


        simulator = ttk.LabelFrame(
            self.root,
            text="Simulators"
        )
        simulator.pack(fill="x", padx=10, pady=5)


        ttk.Button(
            simulator,
            text="Temperature Sensor",
            command=self.start_temperature
        ).pack(side="left", padx=5)


        ttk.Button(
            simulator,
            text="Camera Node",
            command=self.start_camera
        ).pack(side="left", padx=5)


        ttk.Button(
            simulator,
            text="Smart Lock",
            command=self.smart_lock
        ).pack(side="left", padx=5)


        messages = ttk.LabelFrame(
            self.root,
            text="Live Messages"
        )
        messages.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.output = tk.Text(
            messages,
            state="disabled"
        )

        self.output.pack(
            fill="both",
            expand=True
        )


    def connect(self):

        threading.Thread(
            target=self.connection_thread,
            daemon=True
        ).start()


    def connection_thread(self):

        self.client.connect(
            BROKER,
            PORT
        )

        self.client.loop_start()


    def on_connect(self, client, userdata, flags, rc):

        self.connected = True

        self.queue.put(
            "Connected to MQTT broker\n"
        )


    def publish(self):

        topic = self.pub_topic.get()
        msg = self.pub_msg.get(
            "1.0",
            tk.END
        )

        self.client.publish(
            topic,
            msg
        )


    def subscribe(self):

        topic = self.sub_topic.get()

        self.client.subscribe(
            topic
        )


        self.queue.put(
            f"Subscribed: {topic}\n"
        )


    def on_message(
        self,
        client,
        userdata,
        msg
    ):

        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )

        text = (
            f"[{timestamp}] "
            f"{msg.topic}\n"
            f"{msg.payload.decode()}\n\n"
        )

        self.queue.put(text)


    def process_messages(self):

        while not self.queue.empty():

            msg = self.queue.get()

            self.output.config(
                state="normal"
            )

            self.output.insert(
                tk.END,
                msg
            )

            self.output.config(
                state="disabled"
            )

            self.output.see(
                tk.END
            )

        self.root.after(
            100,
            self.process_messages
        )


    def start_temperature(self):

        threading.Thread(
            target=self.temperature_sensor,
            daemon=True
        ).start()


    def temperature_sensor(self):

        while True:

            payload = {
                "device":"temperature_sensor",
                "temperature":round(
                    random.uniform(20,30),
                    2
                ),
                "battery":random.randint(
                    50,
                    100
                )
            }

            self.client.publish(
                "iot/sensors/temp",
                json.dumps(payload)
            )

            time.sleep(2)


    def start_camera(self):

        threading.Thread(
            target=self.camera_node,
            daemon=True
        ).start()


    def camera_node(self):

        while True:

            payload = {
                "device":"camera01",
                "event":"face_detected",
                "identity":random.choice(
                    [
                        "Antonio",
                        "Unknown",
                        "Guest"
                    ]
                ),
                "confidence":round(
                    random.uniform(
                        0.6,
                        0.99
                    ),
                    2
                )
            }


            self.client.publish(
                "camera/events",
                json.dumps(payload)
            )

            time.sleep(3)


    def smart_lock(self):

        payload = {
            "device":"door01",
            "action":"unlock",
            "user":"Antonio"
        }


        self.client.publish(
            "access/control",
            json.dumps(payload)
        )



if __name__ == "__main__":

    root = tk.Tk()

    app = MQTTToolbox(
        root
    )

    root.mainloop()
