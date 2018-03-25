import os
import re
from django.conf import settings
import pandas as pn
from datetime import datetime
import collections



# Create your Utility Functions here.

'''
Return the file path for the CSV file
@name: string
     name of the CSV file 
'''
def get_CSV_file_path (name):
    module_dir = os.path.dirname(__file__);  # get current directory
    
    return os.path.join(module_dir, name);

'''
Create data frame for the CSV file
@name: string
     name of the CSV file 
@columns: array
     subset of the columns to be read from the CSV file
'''
def create_data_frame (name, columns):
    
    return pn.read_csv(get_CSV_file_path(name), sep=';', index_col=False, usecols=columns, warn_bad_lines=False );

'''
Create data frame for the zone CSV file
'''
def get_zones():
    return pn.read_csv(get_CSV_file_path(settings.CSV_ZONES_FLIE_PATH), sep=';', index_col=False);


'''
Create dictionary for parking zone
@zone: data frame
    zone that will be transformed to dictionary 
'''
def zone_to_dict (zone):
    
    dict={};
    dict['CITY'] = str(zone['CITY'].item());
    dict['NAME'] = str(zone['NAME'].item());
    dict['ZONENUMBER'] = int (zone['ZONENUMBER'].item());
    dict['ZONEID'] = long(zone['ZONEID'].item());
    dict['LONGNAME'] = str(zone['LONGNAME'].item()); 
    dict['LONGITUDE'] = zone['LONGITUDE'].item();
    dict['LATITUDE'] = zone['LATITUDE'].item();
    
    return dict;

def calculate_percentage_increase (new_number, old_number):
    
    if new_number == old_number:
        return 0;
    
    elif old_number == 0:
        return 'Infinity';
    
    return float("{0:.2f}".format((float(new_number) - float(old_number))/float(old_number)*100));

###########################################################
def init_dict_for_zones (zones):
    result = {};
    for row in zones.itertuples():
        result[str(row[1])] = "0";    
    return result;

def initDictForGroupByField (grouptype):
    
    result = {};
    counter = 0;
    if grouptype == 1:
        counter = 7;
    elif grouptype == 2:
        counter = 12;
    
    for i in range(1, counter+1):
        result[int(i)] = int(0);        
    return result;

def getDayName (daytype):
    
    name = str(daytype);
    if daytype == 1:
        name = "Monday";
    elif daytype == 2:
        name = "Tuesday";
    elif daytype == 3:
        name = "Wednesday"; 
    elif daytype == 4:
        name = "Thursday";
    elif daytype == 5:
        name = "Friday";
    elif daytype == 6:
        name = "Saturday";
    elif daytype == 7:
        name = "Sunday";  

    return name;

def getMonthName (monthtype):
    
    name = str(monthtype);
    if monthtype == 1:
        name = "January";
    elif monthtype == 2:
        name = "February";
    elif monthtype == 3:
        name = "March"; 
    elif monthtype == 4:
        name = "April";
    elif monthtype == 5:
        name = "May";
    elif monthtype == 6:
        name = "June";
    elif monthtype == 7:
        name = "July";
    elif monthtype == 8:
        name = "August";
    elif monthtype == 9:
        name = "September"; 
    elif monthtype == 10:
        name = "October";
    elif monthtype == 11:
        name = "November"; 
    elif monthtype == 12:
        name = "December";    

    return name;

def getGroupByField (grouptype):
    
    field = str(grouptype);
    if grouptype == 1:
        field = 'DAYTYPE'  
    elif grouptype == 2: 
        field = 'MONTH'
    
    return field;

def getFieldName (grouptype, type):
    if grouptype == 1:
        return getDayName(type);
    else:
        return getMonthName(type);

def calculatePercentage (part, total):
    
    percentage = format (100 * float(part)/float(total), '.2f') ;
    return percentage; 

def createReportDict (zone, rank, field_value, percentage_value):
    dict={};
    dict['ZONE'] =  zone_to_dict(zone);
    dict['RANK'] = rank;
    dict['VALUE'] = field_value;
    dict['PERCENTAGE'] = percentage_value;
    
    return dict;

def calculateRank (current_rank, current_record, current_rank_value, value):
    
    if value != None:
        if current_rank_value == value:
            return current_rank

    return current_record;


#Functions that working with parking data  

def getParkingEventsDistribution ():
    
    zonesgeotags = get_zones();
    csvframe = pn.read_csv(get_CSV_file_path(settings.CSV_EVENTS_FLIE_PATH), sep=';', index_col=False, usecols=['ZONEID']);
    total = csvframe.shape[0];
    t = csvframe['ZONEID'].value_counts();
    t.sort_values(ascending=False);
    
    current_rank = 1;
    current_record = 1;
    lastvalue = None;
    result = [];
    for ind, val in t.iteritems():
        zone = zonesgeotags[zonesgeotags['ZONEID']==ind]
        value_percentage = calculatePercentage(val, total);
        current_rank = calculateRank(current_rank, current_record,  value_percentage, lastvalue);
        result.append(createReportDict(zone, current_rank, 0, float(value_percentage)))
        current_record = current_record+1;
        lastvalue = value_percentage;
    
    return result;

def getEarnedMoneyDistribution():
    
    zonesgeotags = get_zones();
    csvframe = pn.read_csv(get_CSV_file_path(settings.CSV_EVENTS_FLIE_PATH), sep=';', index_col=False, usecols=['ZONEID', 'PRICE']);
    
    total = csvframe['PRICE'].sum();
    t = csvframe.groupby('ZONEID')['PRICE'].sum().sort_values(axis='index', ascending=False);

    current_rank = 1;
    current_record = 1;
    lastvalue = None;
    result = [];
    for ind, val in t.iteritems():
        zone = zonesgeotags[zonesgeotags['ZONEID']==ind]
        value_percentage = calculatePercentage(val, total);
        current_rank = calculateRank(current_rank, current_record,  value_percentage, lastvalue);
        result.append(createReportDict(zone, current_rank, 0, float(value_percentage)))
        current_record = current_record+1;
        lastvalue = value_percentage;
    
    return result;

def getAverageDuration():
    
    zonesgeotags = get_zones();
    csvframe = pn.read_csv(get_CSV_file_path(settings.CSV_EVENTS_FLIE_PATH), sep=';', index_col=False, usecols=['ZONEID', 'DURATION'])
    
    t = csvframe.groupby('ZONEID')['DURATION'].mean().sort_values(axis='index', ascending=False);
    total = t.sum()
    
    current_rank = 1;
    current_record = 1;
    lastvalue = None;
    result = [];
    for ind, val in t.iteritems():
        zone = zonesgeotags[zonesgeotags['ZONEID']==ind]
        value_percentage = calculatePercentage( int(val), total);
        current_rank = calculateRank(current_rank, current_record,  int(val), lastvalue);
        result.append(createReportDict(zone,  current_rank, int(val), float(value_percentage)))
        current_record = current_record+1;
        lastvalue =  int(val);
    
    return result;

def getAverageCost():
    
    zonesgeotags = get_zones();
    csvframe = pn.read_csv(get_CSV_file_path(settings.CSV_EVENTS_FLIE_PATH), sep=';', index_col=False, usecols=['ZONEID', 'PRICE'])
    
    t = csvframe.groupby('ZONEID')['PRICE'].mean().sort_values(axis='index', ascending=False);
    total = t.sum()
    
    current_rank = 1;
    current_record = 1;
    lastvalue = None;
    result = [];
    for ind, val in t.iteritems():
        zone = zonesgeotags[zonesgeotags['ZONEID']==ind]
        value_percentage = calculatePercentage( int(val), total);
        current_rank = calculateRank(current_rank, current_record,  int(val), lastvalue);
        result.append(createReportDict(zone,  current_rank, int(val), float(value_percentage)))
        current_record = current_record+1;
        lastvalue =  int(val);
    
    return result;

#groupType: 1 - Day of week, 2 - Monthly
def getAverageDurationInDetail(groupType):

    zonesgeotags = get_zones();
    csvframe = pn.read_csv(get_CSV_file_path(settings.CSV_EVENTS_FLIE_PATH), sep=';', index_col=False, usecols=['ZONEID', getGroupByField(groupType), 'DURATION'])
    
    t = csvframe.groupby('ZONEID');
    
    result = [];
    for name, group in t:
        resultTemp={};
        resultTemp['ZONE'] = zone_to_dict(zonesgeotags[zonesgeotags['ZONEID']==name]);
        resultTemp['AVERAGE'] = int(group.mean()['DURATION']);
        tempGroup = group.groupby(getGroupByField(groupType))['DURATION'].mean();
        resT=initDictForGroupByField(groupType);
        for ind, val in tempGroup.iteritems():
            resT[int(ind)] = int(val);
        resultTemp['DETAILS'] = collections.OrderedDict(sorted(resT.items()));
        result.append(resultTemp);
        
    return result;






