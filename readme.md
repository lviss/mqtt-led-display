# Setup

Set up scrollphathd library:

```
curl https://get.pimoroni.com/scrollphathd | bash
```

Install paho-mqtt library:

```
pip install paho-mqtt
```

# Run

```
./mqtt-led-display.py
```

# Run at boot

```
sudo cp mqtt-led-display.service /etc/systemd/system/
sudo systemctl enable mqtt-led-display.service
sudo systemctl start mqtt-led-display.service
```
