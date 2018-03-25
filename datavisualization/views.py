from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.http import HttpResponse
import os
import re
from django.http import JsonResponse
from . import util
from . import datautil
from django.utils import translation



# Create your views here.

def home(request):
    dict_result = {'page_title' : _("Dashboard")};
    dict_summary = datautil.data_summary();
    dict_result['EVENTS'] = dict_summary['EVENTS'];
    dict_result['FEES'] = dict_summary['FEES'];
    dict_result['ZONES'] = dict_summary['ZONES'];
    dict_result['CLIENTS'] = dict_summary['CLIENTS'];
    
    return render (request,"dashboard.html", dict_result);

def calendardetail(request):  
    zones = util.get_zones();
    zones = zones.sort_values('NAME', ascending=True);
    zones_list=[];  
    for row in zones.itertuples():
        zones_list.append({'NAME':row[2], 'ID': row[1]});
    
    dict_result = {};
    dict_result['ZONES'] = zones_list;
    dict_result['page_title'] = _("Calendar Detail");
            
    return render (request, "calendardetail.html", dict_result);

def calendar(request):        
    return render (request, "calendar.html", {'page_title' : _("Calendar View")})

def densitydays(request):
    return render (request, "densitydays.html", {'page_title' : _("Parking density by day of the week")})

def pointmapdaysofweek(request):
    return render (request, "pointmapdaysofweek.html", {'page_title' : _("Animation")})

def heatmapdaysofweek(request):
    return render (request, "heatmapdaysofweek.html", {'page_title' : _("Heatmap")})

def pointmapdate(request):
    dict_result = datautil.get_min_max_date();
    dict_result['page_title'] = _("Animation");
    return render (request, "pointmapdate.html", dict_result)

def heatmapdate(request):
    dict_result = datautil.get_min_max_date();
    dict_result['page_title'] = _("Heatmap");
    return render (request, "heatmapdate.html", dict_result)

def reports(request):        
    return render (request, "reports.html", {'page_title' : _("Reports")})
