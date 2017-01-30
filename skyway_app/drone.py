# Connects to the drone,
# takes off and flies to the specified location
# and then disarms and exits

import dronekit
import time
import math

# DRONE_ADDRESS = 'tcp:127.0.0.1:5760'
DRONE_ADDRESS = '0.0.0.0:14550'

class drone(object):

  def __init__(self):
    self.distanceToDestination = None
    self.cruise_altitude = None
    self.cruise_speed = None

  def connectToDrone(self):
    print 'Connecting to vehicle.'
    self.solo = dronekit.connect(DRONE_ADDRESS, wait_ready=True)
    self.solo.commands.download()
    #self.solo = dronekit.connect('0.0.0.0:14550', wait_ready=True)    

    #while self.homeLat == 0:
    #  self.homeLat = self.solo.location.global_frame.lat
    #  self.homeLon = self.solo.location.global_frame.lon
    #  time.sleep(1)
    print 'Made it past.'

  def takeoff(self, altitude=20):
    self.cruise_altitude = altitude
    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not self.solo.is_armable:
      print " Waiting for vehicle to initialise..."
      time.sleep(1)
    #print "Arming motors"
    # Copter should arm in GUIDED mode
    self.solo.mode = dronekit.VehicleMode("GUIDED")
    self.solo.armed = True    

    # Confirm vehicle armed before attempting to take off
    while not self.solo.armed:      
        #print " Waiting for arming..."
        time.sleep(.1)

    #print "Taking off!"
    #print "Altitude: ", altitude
    self.solo.simple_takeoff(altitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        #print " Altitude: ", self.solo.location.global_relative_frame.alt 
        #Break and return from function just below target altitude.        
        if self.solo.location.global_relative_frame.alt>=altitude*0.95: 
            #print "Reached target altitude"
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

  # Fly to a point `alt` above the home location
  # and then fly to the destination location
  # and then land
  def flyTo(self, lat, lon, alt, cruise_speed):
    
    wp1 = dronekit.LocationGlobalRelative(self.solo.home_location.lat, self.solo.home_location.lon, alt)
    wp2 = dronekit.LocationGlobalRelative(float(lat), float(lon), alt)

    print "Going to wp1"
    self._flyTo(wp1, cruise_speed)
    print "going to wp2"
    self._flyTo(wp2, cruise_speed)
    print "Arrived in 2d space. landing"
    self._land()

  def _flyTo(self, waypoint, cruise_speed):
    self.cruise_speed = cruise_speed
    self.solo.simple_goto(waypoint, cruise_speed)

    # wait for travel
    ARRIVAL_TOLERANCE = 0.8 # m ?
    while self.get_distance_metres(self.solo.location.global_relative_frame, waypoint) > ARRIVAL_TOLERANCE:
      time.sleep(0.2)

  def _land(self):
    self.solo.mode = dronekit.VehicleMode("LAND")
    while self.solo.armed == True:
      time.sleep(0.2)

  def getHomeLat(self):
    #print "Trying to get home location: ", self.solo.home_location
    
    if self.solo.home_location:
      return self.solo.home_location.lat
    else:
      print "no solo.home_location yet"
      return 0
    
  def getHomeLng(self):
    if self.solo.home_location:
      return self.solo.home_location.lon
    else:
      return 0

  def getLat(self):
    return self.solo.location.global_relative_frame.lat

  def getLng(self):
    return self.solo.location.global_frame.lon

  def getSpeed(self):
    return self.solo.airspeed

  def getElevation(self):
    return self.solo.location.global_relative_frame.alt

  def getETA(self):
    
    # TODO UPDATE THE DISTNACE HERE
    # self.get_distance_metres(self.solo.location.global_relative_frame, destination)

    CLIMB_SPEED = 3.0

    # Climb / descent time
    if self.cruise_altitude:
      alt = self.cruise_altitude
    else:
      alt = 20.0 # If not set yet, make a guess for a rough estimate
    
    climb_time = alt/CLIMB_SPEED

    # Cruise Time
    if self.cruise_speed:
      speed = self.cruise_speed
    else:
      speed = 15.0 # If not set yet, make a guess for a rough estimate

    if not self.distanceToDestination:
      return None
    else:
      cruise_time = self.distanceToDestination / speed

    acceleration_time = (1 - self.solo.airspeed/speed)*5

    total_time = 2*climb_time + cruise_time + acceleration_time # climb and descent

    return total_time

  def getMode(self):
    return self.solo.mode.name

  def isArmable(self):
    return self.solo.is_armable

  def getArmed(self):
    return self.solo.armed