from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import pandas as pn
import os
import re
from django.http import JsonResponse
from __builtin__ import str
from . import util
from . import datautil
from django.conf import settings


# Create your REST Web Services here.

def get_fee_summary_by_zone (request):
    
    return JsonResponse(datautil.fee_summary_by_zone(), safe=False);

def get_no_events_summary_by_zone (request):
    
    return JsonResponse(datautil.no_events_summary_by_zone(), safe=False);

def get_no_events_summary_daily (request):
    
    return JsonResponse(datautil.no_events_summary_daily(), safe=False);

def get_fees_summary_daily (request):
    
    return JsonResponse(datautil.fees_summary_daily(), safe=False);

def get_parking_trend(request):
    
    return JsonResponse(datautil.parking_trend(datetime(2016, 4, 4, 18, 00)), safe=False);

def get_events_last_seven_days(request):
    
    return JsonResponse(datautil.parking_events_last_seven_days(datetime(2016, 4, 4, 18, 00)), safe=False);

def get_calendar_detail(request):
    zone = int(request.GET.get('zone', 0));
    return  JsonResponse(datautil.no_events_day_of_week_by_zone_and_hour(zone), safe=False);

def getdensitydays (request):
   
    daytype = int(request.GET.get('daytype', 0));
    result=[];
    if daytype>0 and daytype<=7:
        csvframe = pn.read_csv(util.get_CSV_file_path(settings.CSV_EVENTS_FLIE_PATH), sep=';', index_col=False, usecols=['DAYTYPE','LONGITUDE','LATITUDE'], warn_bad_lines=False );
        latLng = csvframe.loc[(csvframe['DAYTYPE'] == daytype) & (csvframe['LONGITUDE'].notnull()) & (csvframe['LATITUDE'].notnull())];
        csvframe = [];
        
        latLng.drop('DAYTYPE', axis=1, inplace=True);
        result=latLng.to_dict(orient='records');
    
 
    return JsonResponse(result, safe=False)

def getanimation(request):
    
    daytype = int(request.GET.get('daytype', 0));
    resultDict={};
    if daytype>0 and daytype<=7:
        csvframe = pn.read_csv(util.get_CSV_file_path(settings.CSV_EVENTS_FLIE_PATH), sep=';', index_col=False, usecols=['DAYTYPE', 'STARTTIME','LONGITUDE','LATITUDE','ENDTIME', 'STARTDATE', 'ENDDATE']);
        latLng = csvframe.loc[(csvframe['DAYTYPE'] == daytype) & (csvframe['LONGITUDE'].notnull()) & (csvframe['LATITUDE'].notnull())];

        if latLng.empty:
            return JsonResponse(resultDict, safe=False)
            
        result = latLng.sort_values('STARTTIME', ascending=True);
    
        result.loc[:,'STARTMINUTE'] = result.apply(lambda row: row['STARTTIME'].split(":")[1], axis=1);
        result['STARTTIME'] = result.apply(lambda row: row['STARTTIME'].split(":")[0], axis=1);
    
        result.loc[:,'ENDMINUTE'] = result.apply(lambda row: row['ENDTIME'].split(":")[1], axis=1);
        result['ENDTIME'] = result.apply(lambda row: row['ENDTIME'].split(":")[0] if row['ENDDATE'] == row['STARTDATE'] else str(25), axis=1);
        
        result.drop('DAYTYPE', axis=1, inplace=True);
        result.drop('STARTDATE', axis=1, inplace=True);
        result.drop('ENDDATE', axis=1, inplace=True);
        
        minMaxHour={};
        minMaxHour['MINHOUR'] = int (result['STARTTIME'].min());
        minMaxHour['MAXHOUR'] = int (result['ENDTIME'].max());
        
        resultDict['PARKINGDATA'] = result.to_dict(orient='records'); 
        resultDict['CONSTRAINTS'] = minMaxHour;
        
    return JsonResponse(resultDict, safe=False)

def getparkingsfordate (request):
    
    resultDict={};
    date = str(request.GET.get('date', ''));
    
    csvframe = pn.read_csv(util.get_CSV_file_path(settings.CSV_EVENTS_FLIE_PATH), sep=';', index_col=False, usecols=['DAYTYPE', 'STARTDATE', 'STARTTIME', 'LONGITUDE', 'LATITUDE', 'ENDTIME', 'ENDDATE']);
    latLng = csvframe.loc[(csvframe['STARTDATE'] == date) & (csvframe['LONGITUDE'].notnull()) & (csvframe['LATITUDE'].notnull())];
    
    if latLng.empty:
         return JsonResponse({}, safe=False);
    
    result = latLng.sort_values('STARTTIME', ascending=True);
    result.loc[:,'STARTMINUTE'] = result.apply(lambda row: row['STARTTIME'].split(":")[1], axis=1);
    result['STARTTIME'] = result.apply(lambda row: row['STARTTIME'].split(":")[0], axis=1);
    
    result.loc[:,'ENDMINUTE'] = result.apply(lambda row: row['ENDTIME'].split(":")[1], axis=1);
    result['ENDTIME'] = result.apply(lambda row: row['ENDTIME'].split(":")[0] if row['ENDDATE'] == row['STARTDATE'] else str(25), axis=1);
    
    minMaxHour={};
    minMaxHour['MINHOUR'] = int (result['STARTTIME'].min());
    minMaxHour['MAXHOUR'] = int (result['ENDTIME'].max());
    minMaxHour['DAYTYPE'] = int (result['DAYTYPE'].max());
    
    result.drop('DAYTYPE', axis=1, inplace=True);
    result.drop('STARTDATE', axis=1, inplace=True);
    result.drop('ENDDATE', axis=1, inplace=True);
    
    resultDict['PARKINGDATA'] = result.to_dict(orient='records'); 
    resultDict['CONSTRAINTS'] = minMaxHour;
    
    return JsonResponse(resultDict, safe=False)

def getreport (request):
    
    report = []
    reportType = int(request.GET.get('type', 0));
    if reportType == 1: 
        report = util.getParkingEventsDistribution();
    if reportType == 2: 
        report = util.getEarnedMoneyDistribution();
    if reportType == 3: 
        report = util.getAverageDuration();
    if reportType == 4: 
        report = util.getAverageCost();
    if reportType == 5:
        report = util.getAverageDurationInDetail(1);
    if reportType == 6:
        report = util.getAverageDurationInDetail(2);
    if reportType == 7:
        report = util.getSumOfParkingEventsByDay();
    
    return JsonResponse(report, safe=False)
