# Connects to the drone,
# takes off and flies to the specified location
# and then disarms and exits

import dronekit
import time
import math

class drone(object):

  def __init__(self):
    x = 0;

  def connectToDrone(self):
    print 'Connecting to vehicle.'
    self.solo = dronekit.connect('tcp:127.0.0.1:5760', wait_ready=True)
    self.homeLat = self.solo.location.global_frame.lat
    self.homeLon = self.solo.location.global_frame.lon

    while self.homeLat == 0:
      self.homeLat = self.solo.location.global_frame.lat
      self.homeLon = self.solo.location.global_frame.lon
      time.sleep(1)
    
    self.lat = self.homeLat
    self.lon = self.homeLon
    print "home location in drone.py, lat: ", self.homeLat, ". lon: ", self.homeLon
    print 'Made it past.'

  def takeoff(self, altitude=20):
    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not self.solo.is_armable:
      print " Waiting for vehicle to initialise..."
      time.sleep(1)
    print "Arming motors"
    # Copter should arm in GUIDED mode
    self.solo.mode = dronekit.VehicleMode("GUIDED")
    self.solo.armed = True    

    # Confirm vehicle armed before attempting to take off
    while not self.solo.armed:      
        print " Waiting for arming..."
        time.sleep(.1)

    print "Taking off!"
    print "Altitude: ", altitude
    self.solo.simple_takeoff(altitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", self.solo.location.global_relative_frame.alt 
        #Break and return from function just below target altitude.        
        if self.solo.location.global_relative_frame.alt>=altitude*0.95: 
            print "Reached target altitude"
            break
        else:
          time.sleep(1)

    return

  def get_distance_metres(self, aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    #print "aLocation2.lat: ,", aLocation2.lat, ". aLocation1.lat: ,", aLocation1.lat
    #print "aLocation2.lon: ,", aLocation2.lon, ". aLocation1.lon: ,", aLocation1.lon
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

  def flyTo(self, lat, lon, speed):
    destination = dronekit.LocationGlobalRelative(float(lat), float(lon), 20)

    print "Flying to location at speed: ", speed
    self.solo.airspeed = speed
    self.solo.simple_goto(destination)

    # wait for travel
    distanceToDestination = self.get_distance_metres(self.solo.location.global_relative_frame, destination)
    arrivalTolerance = 0.8

    while distanceToDestination > arrivalTolerance:
      #print "solo location: ", self.solo.location.global_relative_frame
      #print "destination: ", destination
      distanceToDestination = self.get_distance_metres(self.solo.location.global_relative_frame, destination)  
      print "Distance: {}".format(distanceToDestination)
      #print "self.solo.location.global_frame.lat: ", self.solo.location.global_frame.lat
      #print "self.solo.location.global_frame.lon: ", self.solo.location.global_frame.lon
      self.lat = self.solo.location.global_frame.lat
      self.lon = self.solo.location.global_frame.lon
      #self.lon = self.solo.location.global_frame.lon      
      time.sleep(1)
    print "Arrived in 2D Space"
    self.land()

  def land(self):
    print("Setting LAND mode...")
    self.solo.mode = dronekit.VehicleMode("LAND")

    while self.solo.armed == True:
      print "Landing - Vehicle armed state: ", self.solo.armed
      time.sleep(1)

  def gethomeLat(self):
    return self.homeLat

  def gethomeLon(self):
    return self.homeLon

  def getlat(self):
    return self.lat

  def getlon(self):
    return self.lon