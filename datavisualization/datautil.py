import pandas as pn
from django.conf import settings
from . import util
from datetime import datetime, timedelta
from pandas.core.frame import DataFrame
from dateutil.relativedelta import relativedelta
    
def data_summary():
    #Get all records
    result={};
    parkings =util.create_data_frame(settings.CSV_EVENTS_FLIE_PATH, ['ZONEID','STARTDATE','ENDDATE', 'PRICE', 'CLIENT']);

    #Calculate number of all events
    result['EVENTS'] = parkings.shape[0];   
    #Calculate total price for the events
    result['FEES'] = int(round(parkings['PRICE'].sum()));
    #Calculate the number of parking zones
    result['ZONES'] = parkings.ZONEID.nunique()
    #Calculate the number of clients
    result['CLIENTS'] = parkings.CLIENT.nunique()
    
    return result;

def fee_summary_by_zone():
    
    result=[];
    zones = util.get_zones();
    
    parkings = util.create_data_frame(settings.CSV_EVENTS_FLIE_PATH, ['ZONEID','PRICE']);
    parkings = parkings.groupby('ZONEID')['PRICE'].sum().sort_values(axis='index', ascending=False);
    
    for ind, val in parkings.iteritems():
        temp_rec = {};
        temp_rec['ZONE'] = util.zone_to_dict(zones[zones['ZONEID']==ind]);
        temp_rec['FEE'] = int(round(val));
        result.append(temp_rec);

    return result;

def no_events_summary_by_zone():
    
    result=[];
    zones = util.get_zones();
    
    parkings = util.create_data_frame(settings.CSV_EVENTS_FLIE_PATH, ['ZONEID']);
    parkings = parkings['ZONEID'].value_counts().sort_values(ascending=False);
    
    for ind, val in parkings.iteritems():
        temp_rec = {};
        temp_rec['ZONE'] = util.zone_to_dict(zones[zones['ZONEID']==ind]);
        temp_rec['NO_EVENTS'] = int(val);
        result.append(temp_rec);

    return result;

def no_events_summary_daily():
    
    parkings = util.create_data_frame(settings.CSV_EVENTS_FLIE_PATH, ['STARTDATE', 'ENDDATE']);

    multi_daily_events = parkings.loc[(parkings['STARTDATE'] != parkings['ENDDATE'])].copy();
    parkings.drop('ENDDATE', axis=1, inplace=True);
    multi_daily_events.loc[:,'DAYS_DIF'] = pn.to_datetime(multi_daily_events['ENDDATE'],  format="%d/%m/%Y") - pn.to_datetime(multi_daily_events['STARTDATE'],  format="%d/%m/%Y");
    
    dict_res = [];
    for row in multi_daily_events.itertuples():
        startDate = pn.to_datetime(row[1],  format="%d/%m/%Y");
        startDate = startDate + timedelta(days=1)
        for n in range(row[3].days):
            dict_res.append({'STARTDATE':datetime
                             .strftime(startDate + timedelta(days=n),"%d/%m/%Y")});
   
    parkings = pn.concat([parkings,DataFrame.from_dict(dict_res, orient='columns', dtype=None)]); 
     
    parkings = parkings.groupby(['STARTDATE']).size().reset_index();
    parkings.columns = ['DATE', 'VALUE'];
   
    result = {};
    result['DATA'] = parkings.to_dict(orient='records');
    result['MAX_VALUE'] = int (parkings['VALUE'].max());  
    min_max_date = get_min_max_date();
    result['MIN_YEAR'] = (pn.to_datetime(min_max_date['min'], format="%d/%m/%Y")).year;  
    result['MAX_YEAR'] = (pn.to_datetime(min_max_date['max'], format="%d/%m/%Y")).year; 
    
    return result;

def get_min_max_date():
    
    parkings = util.create_data_frame(settings.CSV_EVENTS_FLIE_PATH, ['STARTDATE']);
    
    parkings['STARTDATE'] = pn.to_datetime(parkings['STARTDATE'], format="%d/%m/%Y")
    max = parkings['STARTDATE'].max();
    min = parkings['STARTDATE'].min();
    
    return {'max':datetime.strftime(max, "%d/%m/%Y"), 'min':datetime.strftime(min, "%d/%m/%Y")}

def fees_summary_daily():
    
    parkings = util.create_data_frame(settings.CSV_EVENTS_FLIE_PATH, ['STARTDATE', 'ENDDATE', 'PRICE']);

    multi_daily_events = parkings.loc[(parkings['STARTDATE'] != parkings['ENDDATE'])].copy();
    parkings = parkings.loc[(parkings['STARTDATE'] == parkings['ENDDATE'])];
    parkings.drop('ENDDATE', axis=1, inplace=True);
    
    multi_daily_events.loc[:,'DAYS_DIF'] = pn.to_datetime(multi_daily_events['ENDDATE'],  format="%d/%m/%Y") - pn.to_datetime(multi_daily_events['STARTDATE'],  format="%d/%m/%Y");
    
    dict_res = [];
    for row in multi_daily_events.itertuples():
        price = row[3]/(row[4].days+1);
        startDate = pn.to_datetime(row[1],  format="%d/%m/%Y");
        for n in range(row[4].days+1):
            dict_res.append({'STARTDATE':datetime
                             .strftime(startDate + timedelta(days=n),"%d/%m/%Y"),
                             'PRICE':price});
   
    parkings = pn.concat([parkings,DataFrame.from_dict(dict_res, orient='columns', dtype=None)]); 
     
    parkings = (parkings.groupby(['STARTDATE'])['PRICE'].sum()).reset_index();
    parkings.columns = ['DATE', 'VALUE'];
    parkings['VALUE'] = parkings['VALUE'].apply(lambda x: float("{0:.2f}".format(x)));
   
    result = {};
    result['DATA'] = parkings.to_dict(orient='records');
    result['MAX_VALUE'] = float("{0:.2f}".format(parkings['VALUE'].max()));  
    min_max_date = get_min_max_date();
    result['MIN_YEAR'] = (pn.to_datetime(min_max_date['min'], format="%d/%m/%Y")).year;  
    result['MAX_YEAR'] = (pn.to_datetime(min_max_date['max'], format="%d/%m/%Y")).year; 
    
    return result;

def parking_trend(date):
    
    date_from = date + relativedelta(months=-2);
    date_from = date_from.replace(day=1, hour=0, minute=0, second=0, microsecond=0);

    parkings = util.create_data_frame(settings.CSV_EVENTS_FLIE_PATH, ['STARTDATE', 'ENDDATE', 'PRICE']);
    parkings['STARTDATE'] = pn.to_datetime(parkings['STARTDATE'],  format="%d/%m/%Y");
    parkings['ENDDATE'] = pn.to_datetime(parkings['ENDDATE'],  format="%d/%m/%Y");
    parkings = parkings.loc[(parkings['ENDDATE'] >= date_from) & (parkings['ENDDATE'] <= date)];
    
    multi_daily_events = parkings.loc[(parkings['STARTDATE'] != parkings['ENDDATE'])].copy();
    parkings = parkings.loc[(parkings['STARTDATE'] == parkings['ENDDATE'])];
    parkings.drop('ENDDATE', axis=1, inplace=True);
    
    dict_res = [];
    for row in multi_daily_events.itertuples():
        price = float("{0:.2f}".format(row[3]/((row[2]-row[1]).days+1)));
        startDate = date_from;
        for n in range((row[2]-date_from).days+1):
            startDate_temp=startDate + relativedelta(days=+n)
            dict_res.append({'STARTDATE':startDate_temp, 'PRICE':price});
            
    parkings = pn.concat([parkings,DataFrame.from_dict(dict_res, orient='columns', dtype=None)]);
    
    result = {}
    #Get events for the months
    result['MONTH'] = calculate_compare_events(parkings, 
                        date_from, (date_from + relativedelta(months=+1))+relativedelta(days=-1), 
                        date_from + relativedelta(months=+1), (date_from + relativedelta(months=+2))+relativedelta(days=-1));
    
    #Get events for the last 7 days
    result['SEVEN_DAYS'] = calculate_compare_events(parkings, 
                        date + relativedelta(days=-14), date + relativedelta(days=-8),
                        date + relativedelta(days=-7), date + relativedelta(days=-1));
    
    #Get events for the last days
    result['DAY'] = calculate_compare_events(parkings, 
                        date + relativedelta(days=-2), date + relativedelta(days=-2),
                        date + relativedelta(days=-1), date + relativedelta(days=-1));
        
    return result;

def events_for_data_range (parkings, date_from, date_to):
    
    return parkings.loc[(parkings['STARTDATE'] >= date_from.replace(hour=0, minute=0, second=0, microsecond=0)) & (parkings['STARTDATE'] <= date_to.replace(hour=23, minute=59, second=59, microsecond=999999))].copy();

def calculate_number_of_events (parkings):
    
    return parkings.shape[0];

def calculate_fee (parkings):
    
    return float("{0:.2f}".format(parkings['PRICE'].sum()));

def calculate_compare_events (parkings, previous_date_from, previous_date_to, current_date_from, current_date_to):
    
    result = {};
    previous_parkings = events_for_data_range(parkings, previous_date_from, previous_date_to);
    result['PREVIOUS_EVENTS'] = calculate_number_of_events(previous_parkings);
    result['PREVIOUS_FEE'] = calculate_fee(previous_parkings);
    current_parkings = events_for_data_range(parkings, current_date_from, current_date_to);
    result['EVENTS'] = calculate_number_of_events(current_parkings);
    result['FEE'] = calculate_fee(current_parkings);
    result['INCREASE_FEE'] = util.calculate_percentage_increase(result['FEE'], result['PREVIOUS_FEE']);
    result['INCREASE_EVENTS'] = util.calculate_percentage_increase(result['EVENTS'], result['PREVIOUS_EVENTS']);
    
    return result;
    
def parking_events_last_seven_days(date):
    
    date_from = date + relativedelta(days=-7);
    date_from = date_from.replace(hour=0, minute=0, second=0, microsecond=0);
    date_to = date_from + relativedelta(days=6);
    date_to = date_to.replace(hour=23, minute=59, second=59, microsecond=999999);
      
    parkings = util.create_data_frame(settings.CSV_EVENTS_FLIE_PATH, ['STARTDATE', 'ENDDATE', 'STARTTIME', 'ENDTIME']);
    parkings['STARTDATE'] = pn.to_datetime(parkings['STARTDATE']+' '
                                           +parkings['STARTTIME'],
                                            format="%d/%m/%Y %H:%M");
                                            
    parkings['ENDDATE'] = pn.to_datetime(parkings['ENDDATE'] +' '
                                         +parkings['ENDTIME'],
                                            format="%d/%m/%Y %H:%M");

    parkings = parkings.loc[(parkings['ENDDATE'] >= date_from) 
                            & (parkings['STARTDATE'] <= date_to)];

    
    parkings['STARTDATE'] = parkings.apply(lambda row: row['STARTDATE'].replace(minute=0, second=0, microsecond=0), axis=1);
    parkings['ENDDATE'] = parkings.apply(lambda row: row['ENDDATE'].replace(minute=0, second=0, microsecond=0), axis=1);
    
    parkings.drop('STARTTIME', axis=1, inplace=True);
    parkings.drop('ENDTIME', axis=1, inplace=True);

    loop_date = date_from;
    result = [];
    dayTemp=None;
    days=[];
    while loop_date < date_to:
        temp = {};
        day = datetime.strftime(loop_date.date(), "%d/%m/%Y");
        temp ['DAY'] = day;
        if dayTemp!=day:
            dayTemp = day;
            days.append(dayTemp);
            
        temp ['HOUR'] = loop_date.hour;
        events = parkings.loc[(parkings['ENDDATE'] >= loop_date) 
                            & (parkings['STARTDATE'] <= loop_date)];
        temp ['EVENTS'] = events.shape[0];
        result.append(temp);
        loop_date = loop_date + relativedelta(hours=1);
        
        
        
    return {'DATA':result, 'DAYS':days};

def no_events_day_of_week_by_zone_and_hour(zone_id):
    
    parkings = util.create_data_frame(settings.CSV_EVENTS_FLIE_PATH, ['STARTTIME', 'ZONEID', 'DAYTYPE']);
    parkings = parkings.loc[parkings['ZONEID'] == zone_id];
    parkings.drop('ZONEID', axis=1, inplace=True);
    
    parkings['STARTTIME'] = parkings.apply(lambda row: int (row['STARTTIME'].split(":")[0]), axis=1);
    
    parkings = parkings.groupby('DAYTYPE');
    
    result = [];
    for name, group in parkings:
        for hour in range(24):
            events = group.loc[group['STARTTIME']==hour];
            result.append({'DAY':str(name), 'HOUR':int(hour), 'EVENTS':int(events.shape[0])});  
                            
    return {'DATA':result, 'DAYS':["1", "2", "3", "4", "5", "6", "7"], 'DAYS_LABEL':["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]};