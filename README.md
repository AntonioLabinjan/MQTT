# MQTT Toolbox 🛠️

A small interactive MQTT playground for learning and experimenting with the MQTT protocol.

This project provides a simple GUI environment where you can connect to an MQTT broker, publish messages, subscribe to topics, and simulate IoT devices without needing any physical hardware.

The goal is not to be a production MQTT client, but rather a visual sandbox for understanding how MQTT-based systems work.

---

## What is MQTT?

MQTT (Message Queuing Telemetry Transport) is a lightweight publish/subscribe messaging protocol commonly used in:

- IoT devices
- embedded systems
- smart homes
- industrial automation
- edge computing
- sensor networks

Instead of devices communicating directly with each other, MQTT uses a broker that routes messages between publishers and subscribers.

Architecture:

```
Publisher
    |
    |  publish(topic, message)
    |
    v
 MQTT Broker
    |
    |  subscribe(topic)
    |
    v
Subscriber
```

Example:

A temperature sensor publishes:

```
iot/sensors/temp

{
    "temperature": 24.5
}
```

Any client subscribed to:

```
iot/sensors/temp
```

will receive the message.

---

# Features

## MQTT Connection

Connect to any MQTT broker:

- local Mosquitto broker
- Raspberry Pi broker
- cloud MQTT services

Default:

```
localhost:1883
```

---

## Publish Messages

Send custom MQTT messages through the GUI.

Example:

Topic:

```
home/livingroom/light
```

Payload:

```json
{
    "state": "ON"
}
```

---

## Subscribe to Topics

Listen to MQTT topics and inspect incoming messages in real time.

Supports MQTT wildcards:

```
#
```

Subscribe to everything.

Example:

```
iot/#
```

Subscribe to all IoT-related events.

---

# Built-in Device Simulators

The toolbox contains simple IoT device simulators.

## Temperature Sensor

Generates fake sensor data:

Topic:

```
iot/sensors/temp
```

Example message:

```json
{
    "device": "temperature_sensor",
    "temperature": 24.7,
    "battery": 85
}
```

---

## Camera Node Simulator

Simulates a computer vision edge device.

Topic:

```
camera/events
```

Example:

```json
{
    "device": "camera01",
    "event": "face_detected",
    "identity": "Unknown",
    "confidence": 0.83
}
```

---

## Smart Lock Simulator

Simulates an access control device.

Topic:

```
access/control
```

Example:

```json
{
    "device": "door01",
    "action": "unlock",
    "user": "Antonio"
}
```

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd mqtt-toolbox
```

Create virtual environment:

```bash
python3 -m venv venv
```

Activate:

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install paho-mqtt
```

---

# Running

Start an MQTT broker.

Example using Mosquitto:

Ubuntu:

```bash
sudo apt install mosquitto
sudo systemctl start mosquitto
```

Run the toolbox:

```bash
python mqtt_toolbox.py
```

---

# Example Workflow

1. Start MQTT broker

2. Open MQTT Toolbox

3. Connect to broker

4. Subscribe to:

```
#
```

5. Start the Temperature Sensor simulator

6. Observe MQTT messages flowing through the system

---

# Project Structure

Currently intentionally simple:

```
mqtt-toolbox/
│
├── mqtt_toolbox.py
└── README.md
```

The entire application is contained in a single Python file to make experimentation easier.

---

# Why this exists?

MQTT is one of the core technologies behind modern IoT and distributed edge systems.

This project was created as a small learning environment to understand:

- publish/subscribe architecture
- MQTT topics
- message routing
- device communication
- event-driven systems

---

# Possible Future Improvements

- [ ] MQTT authentication support
- [ ] TLS encrypted connections
- [ ] QoS selector (0/1/2)
- [ ] Retained messages
- [ ] Last Will Testament support
- [ ] Topic tree visualization
- [ ] Message history database
- [ ] Real-time message graphs
- [ ] Multiple simulated devices

---

## License

MIT License
