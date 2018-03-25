//calendarId- Id of the div where calendar will be rendered
//fData - data that will be shown on calendar with constrains
function drawDayHourCalendar(calendarId, fData){
	
	//Empty the divs
	$(calendarId).empty();
	
	var days = fData.DAYS;
	var data = fData.DATA;
	var daysLabel = fData.DAYS_LABEL != null ? fData.DAYS_LABEL : fData.DAYS; 
	
	data.forEach(function(d) {
		d.day = d.DAY;
		d.hour = d.HOUR;
		d.value = d.EVENTS;
	});
	
	var margin = { top: 20, right: 0, bottom: 40, left: 75 },
	width =  $(calendarId).width() - margin.left - margin.right,
	height =  $(calendarId).height() - margin.top - margin.bottom,
	gridSize = Math.floor(width / 24),
	legendElementWidth = gridSize*2,
	buckets = 9,
	colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"], // alternatively colorbrewer.YlGnBu[9]
	times = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
	         "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"];
	

	var svg = d3.select(calendarId).append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
	.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var dayLabels = svg.selectAll(".dayLabel")
	.data(daysLabel)
	.enter().append("text")
	.text(function (d) { return d; })
	.attr("x", 0)
	.attr("y", function (d, i) { return i * gridSize; })
	.style("text-anchor", "end")
	.attr("transform", "translate(-6," + gridSize / 1.5 + ")")
	.attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

	var timeLabels = svg.selectAll(".timeLabel")
	.data(times)
	.enter().append("text")
	.text(function(d) { return d; })
	.attr("x", function(d, i) { return i * gridSize; })
	.attr("y", 0)
	.style("text-anchor", "middle")
	.attr("transform", "translate(" + gridSize / 2 + ", -6)")
	.attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

	var colorScale = d3.scale.quantile()
	.domain([0, d3.max(data, function (d) { return d.value; })]).range(colors);

	var cards = svg.selectAll(".hour")
	.data(data, function(d) {return d.day+':'+d.hour;});

	

	cards.enter().append("rect")
	.attr("x", function(d) { return (d.hour) * gridSize; })
	.attr("y", function(d) { return (days.indexOf(d.day)) * gridSize; })
	.attr("rx", 4)
	.attr("ry", 4)
	.attr("class", "hour bordered")
	.attr("width", gridSize)
	.attr("height", gridSize)
	.style("fill", colors[0]);
	
	cards.append("title");

	cards.transition().duration(1000)
	.style("fill", function(d) { return colorScale(d.value); });
	
	cards.select("title").text(function(d) { return d.value; });

	cards.exit().remove();

	var legend = svg.selectAll(".legend")
	.data([0].concat(colorScale.quantiles()), function(d) { return d; });

	legend.enter().append("g")
	.attr("class", "legend");

	legend.append("rect")
	.attr("x", function(d, i) { return legendElementWidth * i; })
	.attr("y", height)
	.attr("width", legendElementWidth)
	.attr("height", gridSize / 2)
	.style("fill", function(d, i) { return colors[i]; });

	legend.append("text")
	.attr("class", "mono")
	.text(function(d) { return "≥ " + Math.round(d); })
	.attr("x", function(d, i) { return legendElementWidth * i; })
	.attr("y", height + gridSize);

	legend.exit().remove();
  

}