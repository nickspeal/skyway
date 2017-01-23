from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.templatetags.static import static
import drone
import json

solo = drone.drone()
soloconnected = False

def index(request):
  global soloconnected
  if soloconnected == False:
    solo.connectToDrone()
    soloconnected = True
  
  print "here 1"
  context = {'time_estimate': '5', 'GOOGLE_API_KEY': 'AIzaSyBN-Q9c7O40j-z3TRcc3KFHRRcpP290s-8'}     
  print "here 2"
  return render(request, 'skyway_app/index.html', context)

def go(request):
  print "go executing"
  lat = request.GET.get('latitude', None)
  lon = request.GET.get('longitude', None)
  if not lat or not lon:
    print "ERROR: BAD URL PARAMETERS"
  # call the dronekit module we wrote before
  request.session['testing2']= "testing2"
  solo.takeoff()
  resp = "Arrived and landed."
  solo.flyTo(lat,lon, 500)
  resp = "Arrived and landed. <br> <a href=/rtl>Return Home</a>"
  return HttpResponse(resp)

def rtl(request):
  resp = "Drone is (not) coming home. ETA is 5 minutes. <br> <a href=/>Try Again</a>"
  return HttpResponse(resp)

def coordinates(request):
  #print solo
  lat = solo.getlat()
  lon = solo.getlon()
  #print "lat: ", lat, ". lon: ", lon
  data = {'lat':lat,'lon':lon}
  #print "data: ", data
  #print "data.lat: ", data['lat'], "data.lon: ", data['lon']
  return HttpResponse(json.dumps(data))

def homecoordinates(request):
  #print solo
  lat = solo.gethomeLat()
  lon = solo.gethomeLon()
  print "home location, lat: ", lat, ". lon: ", lon
  data = {'lat':lat,'lon':lon}
  #print "data: ", data
  #print "data.lat: ", data['lat'], "data.lon: ", data['lon']
  return HttpResponse(json.dumps(data))