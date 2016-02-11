# Create your views here.
# from django.contrib.gis.maps import google

import StringIO
import xlsxwriter
from models import EarthQuake
from django.db.models import Q
from django.db import connection
from django.http import HttpResponse
from django.utils.translation import ugettext
from django.utils.datetime_safe import datetime
from django.shortcuts import render_to_response, render



def load_main_page(request):
    today = datetime.today().date()
    eq_pos = EarthQuake.objects.filter(Origin_Time__contains=today)
    if request.GET.get("eq"):
        eq = request.GET.get("eq")
        return show_eq_details(request, eq)
    # elif request.is_ajax():
    #     content = request.GET.get('content')
    #     if content == "map":
    #         return HttpResponse("<script>window.location.replace('http://127.0.0.1:8000/');</script>")
    #     elif content == "report":
    #         is_filter = False
    #         return state_report(request, is_filter)
    #     elif content == "statistic":
    #         pass
    return render_to_response('MainPage.html', {'content': "map", 'eq_pos': eq_pos})

# ########## HTML Report ###################
whatToShow=[]

def state_report(request, is_filter=True):
    report = EarthQuake.objects.filter(Origin_Time__contains=datetime.date(datetime.today()))
    if request.is_ajax():
        query = Q()
        if request.POST.get('state'):
            state = request.POST.get('state')
            query &= (Q(Region__icontains=state))
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
        global whatToShow
    whatToShow = report
    return render(request, 'Report.html', {'earthquakes': report.reverse(), 'content':"report"})

def show_eq_details(request, eq):
    eq_reference = EarthQuake.objects.filter(id=eq)[0]
    return render(request, 'EQdetails.html', {'eq': eq_reference})


# ############## Excel Report ##################

def write_to_excel(request):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("EarthQuake_report")
    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bg_color': '#002266',
        'color': 'white',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    title_text = "Earthquake report"
    worksheet_s.merge_range('B2:H2', title_text, title)
    # worksheet_s.write(4, 0, ugettext("from date"), header)
    worksheet_s.write(4, 0, ugettext("NO."), header)
    worksheet_s.write(4, 1, ugettext("Region"), header)
    worksheet_s.write(4, 2, ugettext("Origin time"), header)
    worksheet_s.write(4, 3, ugettext("Magnitude"), header)
    worksheet_s.write(4, 4, ugettext("Latitude"), header)
    worksheet_s.write(4, 5, ugettext("Longitude"), header)

# the rest of the headers from the HTML file
    # Here we will adding the code to add data



    # global whatToShow
    for idx, data in enumerate(whatToShow):
        row = 5 + idx
        worksheet_s.write(row, 0, idx)
        worksheet_s.write(row, 1, data.Region,)
        worksheet_s.write(row, 2, data.Origin_Time)
        worksheet_s.write(row, 3, data.Magnitude)
        worksheet_s.write(row, 4, data.Latitude)
        worksheet_s.write(row, 5, data.Longitude)


    # the rest of the data
    # xlsx_data contains the Excel file
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


def download_excel(request):
    """

    :rtype : response
    """
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
    xlsx_data = write_to_excel(request)
    response.write(xlsx_data)
    return response


# ########### Show fault  ##################

def show_faults(request):
    return render_to_response('Maps.html')


# ################ Show most accoured #####################

def prone_areas(self):
    cursor = connection.cursor()
    cursor.execute('select "Region",COUNT("Region") as RCOUNT from "EQ_Analyzer_earthquake" group by "Region" order by RCOUNT DESC ')
    area = {}
    counter = 0
    for record in cursor:
        counter += 1
        if counter < 6:
            print record[0].encode("utf-8")
            print record[1]
            area[record[0].encode("utf-8").replace("\xc2\xa0", "")] = record[1]
        else:
            break
    print(area)
    return render_to_response('MostOccourred.html', context={'area': area})

# ################## Statistic ####################


def statistic(request):
    if request.is_ajax():
        month = request.GET.get('month')
        m = request.GET.get('number')
        n = int(m)+1
        year = str(datetime.today().year)
        from_date = '2015' + '-' + m + '-'+'1'
        until_date = year + '-' + str(n) + '-'+'1'
        data= EarthQuake.objects.filter(Origin_Time__gte=from_date, Origin_Time__lt=until_date)
        return render_to_response("graph.html", context={'data': data, 'month':month})
    else:
        return render_to_response("statistic.html")


# ##############################################

def monthly_report(self):
    pass


def crawl_spider(command):
    pass






