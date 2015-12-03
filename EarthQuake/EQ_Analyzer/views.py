# Create your views here.
# from django.contrib.gis.maps import google
from django.shortcuts import render_to_response, render
from EQ_Analyzer.models import EarthQuake


def load_main_page(request):
    return render_to_response('MainPage.html')


def state_report(request):
    if request.method =='POST':
        state = request.get.Get['state'] or 'tehran'
        from_date = request.get.Get['fdate'] or None
        to_date = request.get.Get['tdate'] or None
        report = EarthQuake.objects.filter(Region__contains=state,Origin_Time__gte=from_date,Origin_Time__lte=to_date)
    else:
        report = EarthQuake.objects.all()
    return render(request, 'Report.html', {'earthquakes': report})


def monthly_report(self):
    pass


def crawl_spider(command):
    pass






