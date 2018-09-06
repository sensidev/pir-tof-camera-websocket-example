# Concept

Detect Motion, Distance and stream live Raspberry Pi camera using websockets.

# Prerequisites

1. Raspberry Pi + Camera
2. PIR Motion Sensors
3. ToF (Time-of-Flight) VL53L0X Distance Sensors

# Demo

1. Start your Raspberry Pi and `ssh` into it
2. `mkdir sandbox`
3. `cd sandbox`
4. `git clone --recursive https://github.com/sensidev/pir-tof-camera-websoket-example.git`
5. `python3 -m venv virtualenv`
6. `source virtualenv/bin/activate`
7. `cd pir-tof-camera-websoket-example/`
8. `pip install -r requirements.txt`
9. `cd VL53L0X_rasp_python && make && cd ..`
10. `PYTHONPATH=. python server.py`

Assuming your Raspberry Pi is connected to the same router as your workstation, and both received an IP from the DHCP server, use Raspberry's IP in your browser like this: 
```
http://192.168.0.71:8082
```
Enjoy playing around with motion and distance sensors while the live camera is watching you :)  

![In action](https://raw.githubusercontent.com/sensidev/pir-tof-camera-websoket-example/master/assets/images/demo.png "In action")