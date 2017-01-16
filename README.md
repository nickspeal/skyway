# About

Skyway is a drone delivery application. The user selects a destination on a map using a web interface and the drone automatically takes off, flies to the location, and lands.

# Dependencies

Django (1.10.5)
dronekit (2.9.0)
dronekit-sitl (3.2.0)
dronekit-solo (1.3.0)
MAVProxy (1.5.7)

# Setup

* Start the simulator: `dronekit-sitl solo-2.0.20`
* Use MAVProxy to split the TCP stream into 2 UDP streams such that multiple GCSes can connect to the drone: `mavproxy.py --master tcp:127.0.0.1:5760 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550 --out`127.0.0.1:14551
* Run the webserver: `python manage.py runserver`

# Status

Initial prototype has been started. It generally works in simulation.

# License

Written by Nick Speal and Bryan Altman at Truckee Labs. All rights reserved.

