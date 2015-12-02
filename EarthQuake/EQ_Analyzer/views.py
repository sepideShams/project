# Create your views here.
# from django.contrib.gis.maps import google
from django.shortcuts import render_to_response
from Django_EQ.models import EarthQuake


def load_main_page(self):
    # map = google.GoogleMap
    return render_to_response('MainPage.html')

def state_report(request):
    state = request.get.Get['state'] or 'tehran'
    from_date = request.get.Get['fdate'] or None
    to_date = request.get.Get['tdate'] or None
    report = EarthQuake.objects.filter(Region=state,from_date__gt=from_date,to_date__lt=to_date)
    return render_to_response('StateReport.html',contex={'state': state, 'EQ':report})


def monthly_report(self):
    pass


def crawl_spider(command):
    pass






