from django.conf.urls import url

from . import views
from . import rest

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^densitydays', views.densitydays, name='densitydays'),
    url(r'^getdensitydays/$', rest.getdensitydays, name='getdensitydays'),
    url(r'^pointmapdaysofweek', views.pointmapdaysofweek, name='pointmapdaysofweek'),
    url(r'^heatmapdaysofweek', views.heatmapdaysofweek, name='heatmapdaysofweek'),
    url(r'^getanimation/$', rest.getanimation, name='getanimation'),
    url(r'^pointmapdate', views.pointmapdate, name='pointmapdate'),
    url(r'^heatmapdate', views.heatmapdate, name='heatmapdate'),
    url(r'^getparkingsfordate/$', rest.getparkingsfordate, name='getparkingsfordate'),
    url(r'^reports', views.reports, name='reports'),
    url(r'^calendardetail', views.calendardetail, name='calendardetail'),   
    url(r'^calendar', views.calendar, name='calendar'),
    url(r'^getreport/$', rest.getreport, name='getreport'),
    url(r'^getfeesummarybyzone', rest.get_fee_summary_by_zone, name='getfeesummarybyzone'),
    url(r'^geteventssummarybyzone', rest.get_no_events_summary_by_zone, name='geteventssummarybyzone'),   
    url(r'^geteventssummarydaily', rest.get_no_events_summary_daily, name='geteventssummarydaily'),
    url(r'^getfeessummarydaily', rest.get_fees_summary_daily, name='getfeessummarydaily'),  
    url(r'^getparkingtrend', rest.get_parking_trend, name='getparkingtrend'),
    url(r'^geteventslastsevendays', rest.get_events_last_seven_days, name='geteventslastsevendays'),
    url(r'^getcalendardetail', rest.get_calendar_detail, name='getcalendardetail'),
    
]