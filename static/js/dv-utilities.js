function Day (minHour, maxHour) {
	
	this.minHour = minHour;
	this.maxHour = maxHour>23 ? 23 : maxHour;
	this.hour = minHour;
	this.minute = 0;
	this.isEndOfDay = false;
	
	this.IncrementMinute = function () {
    	if (this.minute == 59) {
    		//Check if the day finish
    		if (this.hour == this.maxHour) {
    			this.isEndOfDay = true;
    			return;
	        } else {
	        	this.hour++;
	        }
    		this.minute = 0;
    	} else {
    		this.minute++;
    	}
    }
	
	this.Reset = function () {
		this.hour = minHour;
		this.minute = 0;
		this.isEndOfDay = false;
	}
}

function ParkingEventsDay (dayType, minHour, maxHour, parkings) {
	
	this.dayType = dayType
	//this.dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
	this.dayNames = ["Понеделник", "Вторник", "Среда", "Четврток", "Петок", "Сабота", "Недела"];
	this.day = new Day (minHour, maxHour);
	
	this.parkingCounter = 0;
	this.parkings = parkings;
	this.hasParkings = true;
	
	this.GetDayInfo = function() {
		return ""+this.dayNames[this.dayType-1]+";	 "+this.day.hour+":"+
		(this.day.minute<=9 ? "0"+this.day.minute : this.day.minute);
    };
	
	this.GetCurrentParkings = function () {
		
		var currentParkings = [];
		while ( this.parkingCounter<this.parkings.length 
	    		&& parseInt(this.parkings[this.parkingCounter]['STARTTIME']) <= this.day.hour
	    		&& parseInt(this.parkings[this.parkingCounter]['STARTMINUTE']) <= this.day.minute) {
			
			currentParkings.push(this.parkings[this.parkingCounter]);
	        this.parkingCounter++;
	      }
		
		if (this.day.isEndOfDay){
        	this.hasParkings = false;
        	return currentParkings;
        } else {
        	this.IncrementDayMinute();
        }
		
		return currentParkings;
	}
	
	this.IncrementDayMinute = function () {
		this.day.IncrementMinute();
	}
	
	this.RemoveEvents = function (addedMarkers, hour, minute) {
		if (addedMarkers.length>0){
	  		  for(var i=0; i<addedMarkers.length; i++){
	  			  if (addedMarkers[i].endHour == hour
	  					  && addedMarkers[i].endMinute == minute){
	  			  	addedMarkers[i].setMap(null);
	  			  }
	  		  }
	  		  
	  		for(var i=0; i<addedMarkers.length; i++){
	  			  if (addedMarkers[i].getMap() == null){
	  				addedMarkers.splice(i, 1);
	  			  	i=i-1
	  			  }
	  		  }
	  	  }
		}
	
	this.RemoveHeatEvents = function (addedMarkers, hour, minute) {
		if (addedMarkers.length>0){
	  		  for(var i=0; i<addedMarkers.length; i++){
	  			if (addedMarkers.getAt(i).endHour == hour
	  					  && addedMarkers.getAt(i).endMinute == minute){
	  			  	addedMarkers.removeAt(i);
	  			  	i=i-1;
	  			  }
	  		  }
	  	  }
		}	
	
	this.Reset = function () {
		this.day.Reset();
		this.parkingCounter = 0;
		this.hasParkings = true;
	}
	
	this.ClearMap = function (addedMarkers) {
		//clear the map
    	if (addedMarkers.length>0){
    		for(var i=0; i<addedMarkers.length; i++){
    			addedMarkers[i].setMap(null);
    		}
    		addedMarkers = [];
    	}
	}
}

function clearMapOverlays (listOfOverlays) {
	
	if (listOfOverlays.length>0){
		for(var i=0; i<listOfOverlays.length; i++){
			listOfOverlays[i].setMap(null);
		}
		listOfOverlays = [];
	}
}

function showZones () {
	if (zones.length>0){
		for (i=0; i<zones.length; i++){
			var record = zones[i];
			var zone = record.ZONE;
			var zoneLat = zone['LATITUDE'] 
			var zoneLng = zone['LONGITUDE'] 
			if (zoneLat != null && zoneLat !=null){
				var myLatlng = new google.maps.LatLng(zoneLat, zoneLng);
			
				var cityCircle = new google.maps.Circle({
	            	strokeColor: '#FF0000',
	            	clickable:true,
	            	strokeOpacity: 0.8,
	            	strokeWeight: 2,
	            	fillColor: '#FF0000',
	            	fillOpacity: 0.35,
	            	map: map,
	            	center: myLatlng,
	            	radius:  300*(record['PERCENTAGE']/100),
	          	});
				
				addedCircles.push(cityCircle);
			
				var info = [];
				/*info.push({name:"City", value:zone['CITY']});
				info.push({name:"Zone name", value:zone['NAME']});
				info.push({name:"Zone number", value:zone['ZONENUMBER']});
				info.push({name:"Long name", value:zone['LONGNAME']});*/
				
				info.push({name:"Град", value:zone['CITY']});
				info.push({name:"Паркинг Зона", value:zone['NAME']});
				attachInfoWindow (cityCircle, myLatlng, 
						info, getReportTitleAndValue($("#reportType").val(), 
								record['VALUE'], record['RANK'], record['PERCENTAGE'],
								zones.length));
			}
		}
	} else {
		alert ("No Data")
	}
}

function attachInfoWindow (circle, center, arrayInfo, titleInfo) {
	
	//var infoString = "<b>"+titleInfo+"</b><hr /><b>Parking Zone Info</b><br /><br />"
	var infoString = "<b>"+titleInfo+"</b><hr /><b>Информации за паркинг зона</b><br /><br />"
	
	if (arrayInfo!=null && arrayInfo.length>0){
		for (j=0;j<arrayInfo.length;j++){
			infoString += "<b>"+arrayInfo[j]['name']+": "+arrayInfo[j]['value']+"</b><br />" 
		}
	}
	
	//create info window
	var infoWindow= new google.maps.InfoWindow({
	    content: infoString
	});
	
	google.maps.event.addListener(circle, 'click', function(ev){
	    infoWindow.setPosition(center);
	    infoWindow.open(map);
	});
} 

function getReportTitleAndValue (reportType, value, rank, percentage,totalRecords) {
	titleInfo = "";
	switch (reportType) {
	case "1":
		/*titleInfo = "Parking events distribution <br />";
		titleInfo+= "Percentage from all events in this zone: "+percentage+"% <br />"
		titleInfo+= "Rank: "+rank+"/"+totalRecords;*/
		titleInfo = "Распределба на паркинг настани <br />";
		titleInfo+= "Процент од сите паркинг настани: "+percentage+"% <br />"
		titleInfo+= "Ранк: "+rank+"/"+totalRecords;
		break;
		
	case "2":
		/*titleInfo = "Earned money distribution <br />";
		titleInfo+= "Percentage from all earned money in this zone: "+percentage+"% <br />"
		titleInfo+= "Rank: "+rank+"/"+totalRecords;*/
		titleInfo = "Распределба на заработувачка <br />";
		titleInfo+= "Процент од заработувачката: "+percentage+"% <br />"
		titleInfo+= "Ранк: "+rank+"/"+totalRecords;
		break;
	
	case "3":
		/*titleInfo = "Average duration <br />";
		titleInfo+= "Average duration for the event: "+value+" minutes <br />"
		titleInfo+= "Rank: "+rank+"/"+totalRecords;*/
		titleInfo = "Просечно времетраење <br />";
		titleInfo+= "Просечно времетраење на паркинг настан: "+value+" минути <br />"
		titleInfo+= "Ранк: "+rank+"/"+totalRecords;
		break;
	case "4":
		/*titleInfo = "Average cost <br />";
		titleInfo+= "Average cost for the event: $"+value+" <br />"
		titleInfo+= "Rank: "+rank+"/"+totalRecords;*/
		titleInfo = "Просечна цена <br />";
		titleInfo+= "Просечна цена на паркинг настан: $"+value+" <br />"
		titleInfo+= "Ранк: "+rank+"/"+totalRecords;
		break;

	default:
		break;
	}
	
	return titleInfo;
}