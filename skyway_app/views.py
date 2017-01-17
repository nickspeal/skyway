from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import fly_drone


def index(request):
  context = {'time_estimate': '5', 'GOOGLE_API_KEY': 'ADD HERE'}
  return render(request, 'skyway_app/index.html', context)

def go(request):
  lat = request.GET.get('latitude', None)
  lng = request.GET.get('longitude', None)
  if not lat or not lng:
    print "ERROR: BAD URL PARAMETERS"
  # call the dronekit module we wrote before
  fly_drone.execute(lat, lng)
  resp = "Arrived and landed. <br> <a href=/rtl>Return Home</a>"
  return HttpResponse(resp)

def rtl(request):
  resp = "Drone is (not) coming home. ETA is 5 minutes. <br> <a href=/>Try Again</a>"
  return HttpResponse(resp)