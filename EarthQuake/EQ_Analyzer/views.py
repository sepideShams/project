# Create your views here.
# from django.contrib.gis.maps import google
from django.db.models import Q
from django.shortcuts import render_to_response, render
from django.utils.datetime_safe import datetime
from django.http import HttpResponse
from EQ_Analyzer.models import EarthQuake


def load_main_page(request):
    today = datetime.today().date()
    eq_pos = EarthQuake.objects.filter(Origin_Time__contains=today)
    if request.GET.get("eq"):
        eq = request.GET.get("eq")
        return show_eq_details(request, eq)
    elif request.is_ajax():
        content = request.GET.get('content')
        if content == "map":
            return HttpResponse("<script>window.location.replace('http://127.0.0.1:8000/');</script>")
        elif content == "report":
            is_filter = False
            return state_report(request, is_filter)
        elif content == "statistic":
            pass
    return render_to_response('MainPage.html', {'content': "map", 'eq_pos': eq_pos})


def state_report(request, is_filter=True):
    report = EarthQuake.objects.all()
    if request.is_ajax() and is_filter:
        query = Q()
        if request.POST.get('state'):
            state = request.POST.get('state')
            query &= (Q(Region__contains=state))
        if request.POST.get('magnitude'):
            magnitude = request.POST.get('magnitude')
            query &= (Q(Magnitude=magnitude))
        if request.POST.get('fdate'):
            from_date = request.POST.get('fdate')
            query &= (Q( Origin_Time__gte=from_date))
        if request.POST.get('tdate'):
            to_date = request.POST.get('tdate')
            query &= (Q(Origin_Time__lte=to_date))
        report = EarthQuake.objects.filter(query)
    return render(request, 'Report.html', {'earthquakes': report,'content':"report"})


def show_eq_details(request, eq):
    eq_reference = EarthQuake.objects.filter(id=eq)[0]
    return render(request, 'EQdetails.html', {'eq': eq_reference})


def monthly_report(self):
    pass


def crawl_spider(command):
    pass






