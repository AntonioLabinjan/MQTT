#! best for now
import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import threading
import json
import random
import time
from datetime import datetime


BROKER = "localhost"
PORT = 1883


class DeviceWindow:

    def __init__(self, device_id):

        self.id = device_id

        self.root = tk.Toplevel()
        self.root.title(f"Device {device_id}")
        self.root.geometry("350x500")

        self.client = mqtt.Client(
            client_id=f"device_{device_id}"
        )

        self.client.on_message = self.on_message

        self.subscriptions = {}

        self.build_ui()

        self.client.connect(
            BROKER,
            PORT
        )

        self.client.loop_start()

        self.publish_status(
            "online"
        )


    def build_ui(self):

        ttk.Label(
            self.root,
            text=f"DEVICE {self.id}",
            font=("Arial", 18)
        ).pack(
            pady=10
        )


        sub_frame = ttk.LabelFrame(
            self.root,
            text="Subscribe to devices"
        )

        sub_frame.pack(
            fill="x",
            padx=10
        )


        for i in range(1,6):

            if i == self.id:
                continue


            var = tk.BooleanVar()

            self.subscriptions[i] = var


            ttk.Checkbutton(
                sub_frame,
                text=f"Device {i}",
                variable=var
            ).pack(
                anchor="w"
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
            text="Send event",
            command=self.send_event
        ).pack(
            pady=5
        )


        ttk.Button(
            self.root,
            text="Start auto mode",
            command=self.start_auto
        ).pack(
            pady=5
        )


        self.log = tk.Text(
            self.root,
            height=15
        )

        self.log.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


    def topic(self):

        return f"devices/{self.id}/events"


    def apply_subscriptions(self):

        for device, enabled in self.subscriptions.items():

            topic = f"devices/{device}/events"

            if enabled.get():

                self.client.subscribe(
                    topic
                )

                self.write(
                    f"Subscribed -> {topic}"
                )

            else:

                self.client.unsubscribe(
                    topic
                )


    def send_event(self):

        payload = {

            "sender":
                self.id,

            "event":
                random.choice(
                    [
                        "temperature",
                        "motion",
                        "face_detected",
                        "heartbeat"
                    ]
                ),

            "value":
                random.randint(
                    0,
                    100
                ),

            "time":
                datetime.now().strftime(
                    "%H:%M:%S"
                )
        }


        self.client.publish(
            self.topic(),
            json.dumps(payload)
        )


        self.write(
            f"Sent:\n{payload}"
        )


    def start_auto(self):

        threading.Thread(
            target=self.auto_loop,
            daemon=True
        ).start()


    def auto_loop(self):

        while True:

            self.send_event()

            time.sleep(
                random.randint(
                    2,
                    5
                )
            )


    def publish_status(self,status):

        payload = {

            "device":
                self.id,

            "status":
                status
        }


        self.client.publish(
            "devices/status",
            json.dumps(payload)
        )


    def on_message(
        self,
        client,
        userdata,
        msg
    ):

        self.write(
            f"""
Received:
{msg.topic}

{msg.payload.decode()}

----------------
"""
        )


    def write(self,text):

        self.log.insert(
            tk.END,
            text+"\n\n"
        )

        self.log.see(
            tk.END
        )



class App:


    def __init__(self):

        self.root = tk.Tk()

        self.root.withdraw()


        self.devices = []


        for i in range(1,6):

            device = DeviceWindow(
                i
            )

            self.devices.append(
                device
            )


        self.root.mainloop()



if __name__ == "__main__":

    App()
