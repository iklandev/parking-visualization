//calendarId- Id of the div where calendar will be rendered
//fData - data that will be shown on calendar with constrains
function drawCalendar(calendarId, fData){
	//Empty the divs
	$(calendarId).empty();
	
	var data = d3.nest()
	.key(function(d) { return d.DATE; })
	.rollup(function(d) { return d[0].VALUE; })
	.map(fData['DATA']);

	var width = $(calendarId).width(),
	height = 136,
	cellSize = 17; // cell size

	var format = d3.time.format("%d/%m/%Y");

	var color = d3.scale.quantize()
	.domain([0, fData['MAX_VALUE']])
	.range(d3.range(11).map(function(d) { return "q" + d + "-11"; }));

	var svg = d3.select(calendarId).selectAll("svg")
	.data(d3.range(fData['MIN_YEAR'], fData['MAX_YEAR']+1))
	.enter().append("svg")
	.attr("width", width)
	.attr("height", height)
	.attr("class", "RdYlGn")
	.append("g")
	.attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1) + ")");

	svg.append("text")
	.attr("transform", "translate(-6," + cellSize * 3.5 + ")rotate(-90)")
	.style("text-anchor", "middle")
	.text(function(d) { return d; });

	var rect = svg.selectAll(".day")
	.data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
	.enter().append("rect")
	.attr("class", "day")
	.attr("width", cellSize)
	.attr("height", cellSize)
	.attr("x", function(d) { return d3.time.weekOfYear(d) * cellSize; })
	.attr("y", function(d) { return d.getDay() * cellSize; })
	.datum(format);

	rect.append("title")
	.text(function(d) { return d; });

	svg.selectAll(".month")
	.data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
	.enter().append("path")
	.attr("class", "month")
	.attr("d", monthPath);


	rect.filter(function(d) { return d in data; })
	.attr("class", function(d) { return "day " + color(data[d]); })
	.select("title")
	.text(function(d) { return d + ": " + data[d]; });


	function monthPath(t0) {
		var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
		d0 = t0.getDay(), w0 = d3.time.weekOfYear(t0),
		d1 = t1.getDay(), w1 = d3.time.weekOfYear(t1);
		return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
		+ "H" + w0 * cellSize + "V" + 7 * cellSize
		+ "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
		+ "H" + (w1 + 1) * cellSize + "V" + 0
		+ "H" + (w0 + 1) * cellSize + "Z";
	}
}