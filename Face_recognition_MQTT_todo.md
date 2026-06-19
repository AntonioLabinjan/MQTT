E sad već imamo dosta dobar "roadmap". Pošto već imaš **edge node + kameru + CLIP embeddinge + Qdrant**, ne krećemo od nule nego samo mijenjamo komunikacijsku arhitekturu i dodajemo skaliranje.

## Perceptryx MQTT/IoT arhitektura - TODO

### ✅ Postojeće

* [x] Edge node s kamerom
* [x] Lokalna detekcija lica
* [x] CLIP feature extraction na nodeu
* [x] Qdrant vektorska baza za identity search
* [x] Osnovna logika prepoznavanja

---

# 1. MQTT infrastruktura

* [ ] Dodati MQTT broker

  * Mosquitto za lokalni razvoj
  * kasnije cloud/embedded broker opcija

* [ ] Definirati topic strukturu

Primjer:

```
perceptryx/
    nodes/
        camera01/
            events
            status
            commands

        camera02/
            events
            status
            commands
```

---

# 2. Refaktor edge nodea

Trenutno:

```
Camera
 |
 HTTP
 |
Server
```

Novo:

```
Camera
 |
CLIP
 |
MQTT publish
```

TODO:

* [ ] Edge node postaje MQTT publisher
* [ ] Slati identity evente preko MQTT-a

Payload:

```json
{
  "node_id": "camera01",
  "event": "face_detected",
  "embedding": [],
  "timestamp": ""
}
```

* [ ] Dodati heartbeat

Primjer:

```json
{
 "node_id":"camera01",
 "status":"online",
 "fps":25
}
```

---

# 3. MQTT ingestion service

Novi servis između MQTT-a i AI obrade.

TODO:

* [ ] Napraviti MQTT consumer
* [ ] Subscribe na:

```
perceptryx/nodes/+/events
```

* [ ] Validirati poruke
* [ ] Proslijediti dalje

---

# 4. Redis queue layer

Dodati buffer između MQTT-a i recognitiona.

Flow:

```
MQTT
 |
Consumer
 |
Redis Queue
 |
Worker
```

TODO:

* [ ] Dodati Redis
* [ ] Event push u queue
* [ ] Recognition worker koji čita queue

Primjer:

```
face_event_queue

[
 event1,
 event2,
 event3
]
```

---

# 5. Recognition worker

Odvojiti AI obradu od komunikacije.

TODO:

* [ ] Worker uzima embedding iz Redisa
* [ ] Šalje embedding u Qdrant
* [ ] Dobiva najbliži identity match
* [ ] Donosi odluku

Flow:

```
Embedding
   |
   v
Qdrant search
   |
   v
Candidate
   |
   v
Threshold
   |
   v
Identity
```

---

# 6. Access control layer

Nakon identifikacije:

TODO:

* [ ] Permission management

Primjer:

```json
{
 "person":"Antonio",
 "zone":"lab",
 "allowed":true
}
```

* [ ] Access decision event

Topic:

```
perceptryx/access/result
```

---

# 7. Command channel prema nodeovima

Ne samo publish prema serveru.

Dodati:

```
perceptryx/nodes/camera01/commands
```

Primjeri:

```json
{
 "command":"restart"
}
```

ili:

```json
{
 "command":"change_threshold",
 "value":0.8
}
```

---

# 8. Device management

Da sustav zna koji nodeovi postoje.

TODO:

* [ ] Node registration

Pri paljenju:

```json
{
 "node_id":"camera01",
 "type":"camera",
 "version":"1.0"
}
```

* [ ] Online/offline tracking
* [ ] Last heartbeat timestamp

---

# 9. Dashboard

Za demonstraciju:

* [ ] Lista aktivnih nodeova
* [ ] Zadnje detekcije
* [ ] Identity events
* [ ] Access log
* [ ] System health

---

# 10. Kasnije IoT upgrade

Kad dođu ESP32 uređaji:

* [ ] ESP32 MQTT client
* [ ] Sensor events
* [ ] Door actuator
* [ ] Physical access control

---

Finalni cilj:

```
             Camera Node
                 |
              CLIP
                 |
              MQTT
                 |
          MQTT Broker
                 |
        Ingestion Service
                 |
              Redis
                 |
       Recognition Worker
                 |
              Qdrant
                 |
          Access Decision
                 |
              Device
```

Najveći milestoneovi bi po meni bili:

1. **Edge node → MQTT publish**
2. **MQTT consumer → Redis queue**
3. **Redis worker → Qdrant recognition**
4. **Više nodeova paralelno**

Nakon toga Perceptryx više nije samo demo prepoznavanja, nego stvarno distribuirani edge AI sustav. 😄
