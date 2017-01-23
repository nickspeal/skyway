# Connects to the drone,
# takes off and flies to the specified location
# and then disarms and exits

import dronekit
import time
import math

lat1 = 0;
lng1 = 0;

def _connect_to_drone():
  print 'Connecting to vehicle.'
  vehicle = dronekit.connect('tcp:127.0.0.1:5760', wait_ready=True)
  return vehicle

def _start_motors(vehicle):
  print "Basic pre-arm checks"
  # Don't try to arm until autopilot is ready
  while not vehicle.is_armable:
      print " Waiting for vehicle to initialise..."
      time.sleep(1)

      
  print "Arming motors"
  # Copter should arm in GUIDED mode
  vehicle.mode = dronekit.VehicleMode("GUIDED")
  vehicle.armed = True    

  # Confirm vehicle armed before attempting to take off
  while not vehicle.armed:      
      print " Waiting for arming..."
      time.sleep(.1)
  return

def _takeoff(vehicle, altitude):
  print "Taking off!"
  vehicle.simple_takeoff(altitude) # Take off to target altitude

  # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
  #  after Vehicle.simple_takeoff will execute immediately).
  while True:
      print " Altitude: ", vehicle.location.global_relative_frame.alt 
      #Break and return from function just below target altitude.        
      if vehicle.location.global_relative_frame.alt>=altitude*0.95: 
          print "Reached target altitude"
          break
      else:
        time.sleep(1)
  return

def _flyToLocation(vehicle, destination, speed):
  arrivalTolerance = 0.8
  print "Flying to location at speed: ", speed
  vehicle.airspeed = speed
  vehicle.simple_goto(destination)

  # wait for travel
  distanceToDestination = _get_distance_metres(vehicle.location.global_relative_frame, destination)
  while distanceToDestination > arrivalTolerance:
    distanceToDestination = _get_distance_metres(vehicle.location.global_relative_frame, destination)  
    print "Distance: {}".format(distanceToDestination)
    lat1 = vehicle.location.global_frame.lat
    #lng1 = vehicle.location.global_frame.lng
    time.sleep(1)
  print "Arrived in 2D Space"
  return


def _land(vehicle):
  print("Setting LAND mode...")
  vehicle.mode = dronekit.VehicleMode("LAND")

  while vehicle.armed == True:
    print "Landing - Vehicle armed state: ", vehicle.armed
    time.sleep(1)

def _get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def execute(lat, lng):
  vehicle = _connect_to_drone()
  _start_motors(vehicle)
  _takeoff(vehicle, altitude=10)
  destination = dronekit.LocationGlobalRelative(float(lat), float(lng), 20)
  _flyToLocation(vehicle, destination=destination, speed=60)
  _land(vehicle)

def getlat():
  return lat1

def getlng():
  return lng1

if __name__ == "__main__":
  lat = 39.32876637044429
  lng = -120.18753290176392
  execute(lat, lng)