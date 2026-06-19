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


class VirtualDevice:

    def __init__(self, device_id, message_queue):

        self.id = device_id
        self.queue = message_queue

        self.client = mqtt.Client(
            client_id=f"device_{device_id}"
        )

        self.client.on_message = self.on_message

        self.running = False

        self.client.connect(
            BROKER,
            PORT
        )

        self.client.loop_start()


    def topic(self):

        return f"devices/{self.id}/events"


    def subscribe(self, device_id):

        self.client.subscribe(
            f"devices/{device_id}/events"
        )


        self.queue.put(
            f"Device {self.id} subscribed to Device {device_id}\n"
        )


    def unsubscribe(self, device_id):

        self.client.unsubscribe(
            f"devices/{device_id}/events"
        )


    def publish(self):

        payload = {
            "sender": self.id,
            "event": random.choice(
                [
                    "temperature",
                    "motion",
                    "face_detected",
                    "heartbeat"
                ]
            ),
            "value": random.randint(
                0,
                100
            ),
            "timestamp": datetime.now().strftime(
                "%H:%M:%S"
            )
        }


        self.client.publish(
            self.topic(),
            json.dumps(payload)
        )


    def start(self):

        if self.running:
            return

        self.running = True

        threading.Thread(
            target=self.loop,
            daemon=True
        ).start()


    def loop(self):

        while self.running:

            self.publish()

            time.sleep(
                random.uniform(
                    1,
                    3
                )
            )


    def on_message(
        self,
        client,
        userdata,
        msg
    ):

        self.queue.put(
            f"""
Device {self.id} received:

FROM:
{msg.topic}

MESSAGE:
{msg.payload.decode()}

------------------
"""
        )



class MQTTNetworkSimulator:


    def __init__(self, root):

        self.root = root

        self.root.title(
            "MQTT Network Simulator"
        )

        self.root.geometry(
            "900x700"
        )


        self.queue = Queue()

        self.devices = {}

        self.current_device = tk.IntVar(
            value=1
        )

        self.build_ui()


        for i in range(1,6):

            self.devices[i] = VirtualDevice(
                i,
                self.queue
            )


        self.root.after(
            100,
            self.process_messages
        )


    def build_ui(self):

        device_frame = ttk.LabelFrame(
            self.root,
            text="Active Device"
        )

        device_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )


        for i in range(1,6):

            ttk.Radiobutton(
                device_frame,
                text=f"Device {i}",
                variable=self.current_device,
                value=i
            ).pack(
                side="left",
                padx=10
            )


        subscribe_frame = ttk.LabelFrame(
            self.root,
            text="Subscriptions"
        )

        subscribe_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )


        self.subscriptions = {}


        for i in range(1,6):

            var = tk.BooleanVar()

            self.subscriptions[i] = var

            ttk.Checkbutton(
                subscribe_frame,
                text=f"Listen Device {i}",
                variable=var
            ).pack(
                side="left"
            )


        ttk.Button(
            self.root,
            text="Apply subscriptions",
            command=self.apply_subscriptions
        ).pack(
            pady=5
        )


        ttk.Button(
            self.root,
            text="Start all devices",
            command=self.start_devices
        ).pack(
            pady=5
        )


        log_frame = ttk.LabelFrame(
            self.root,
            text="Network Traffic"
        )

        log_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )


        self.log = tk.Text(
            log_frame
        )

        self.log.pack(
            fill="both",
            expand=True
        )


    def apply_subscriptions(self):

        device_id = self.current_device.get()

        device = self.devices[device_id]


        for target, enabled in self.subscriptions.items():

            if target == device_id:
                continue


            if enabled.get():

                device.subscribe(
                    target
                )


        self.queue.put(
            f"Device {device_id} subscriptions updated\n"
        )


    def start_devices(self):

        for device in self.devices.values():

            device.start()


        self.queue.put(
            "All devices started\n"
        )


    def process_messages(self):

        while not self.queue.empty():

            msg = self.queue.get()

            self.log.insert(
                tk.END,
                msg
            )

            self.log.see(
                tk.END
            )


        self.root.after(
            100,
            self.process_messages
        )



if __name__ == "__main__":

    root = tk.Tk()

    app = MQTTNetworkSimulator(
        root
    )

    root.mainloop()
