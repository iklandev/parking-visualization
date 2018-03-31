//barId- Id of the div where char bar will be rendered
//pieId- Id of the div where pie will be rendered
//legendId- Id of the div where legend will be rendered
//groupType: 1 - Day of week, 2 - Monthly
//fData - data that will be shown on bar and pie
function drawChartPie(barId, pieId, legendId, groupType, fData){
	//Empty the divs
	$(barId).empty();
	$(pieId).empty();
	$(legendId).empty();
	
	
	var barColor = 'steelblue';
	//@Ivan
	function segColor(c){ return {
		1 :"#e74c3c",
		2 :"#8e44ad",
		3 :"#3498db",
		4 :"#16a085",
		5 :"#f4d03f",
		6 :"#566573",
		7 :"#99a3a4",
		8 :"#daf7a6",
		9 :"#ff00ff",
		10:"#ff5700",
		11:"#00ffff",
		12:"#6d4c41"}[c]; }
	
	function mapDayLegend(c){
	
		/*if (groupType == 1){
			return {
				1 :"MON",
				2 :"TUE",
				3 :"WED",
				4 :"THU",
				5 :"FRI",
				6 :"SAT",
				7 :"SUN"}[c];}
		else {
			return {
				1 :"JAN",
				2 :"FEB",
				3 :"MAR",
				4 :"APR",
				5 :"MAY",
				6 :"JUN",
				7 :"JUL",
				8 :"AUG",
				9 :"SEP",
				10 :"OCT",
				11 :"NOV",
				12 :"DEC"}[c];}*/
		
		if (groupType == 1){
			return {
				1 :"ПОН",
				2 :"ВТО",
				3 :"СРЕ",
				4 :"ЧЕТ",
				5 :"ПЕТ",
				6 :"САБ",
				7 :"НЕД"}[c];}
		else {
			return {
				1 :"ЈАН",
				2 :"ФЕБ",
				3 :"МАР",
				4 :"АПР",
				5 :"МАЈ",
				6 :"ЈУН",
				7 :"ЈУЛ",
				8 :"АВГ",
				9 :"СЕП",
				10 :"ОКТ",
				11 :"НОВ",
				12 :"ДЕК"}[c];}
	}
	//function segColor(c){ return {low:"#807dba", mid:"#e08214",high:"#41ab5d"}[c]; }

	// compute total for each state.
	//@Ivan
	fData.forEach(function(d){d.total=d.AVERAGE;});

	// function to handle histogram.
	function histoGram(fD){
		var hG={},    hGDim = {t: 60, r: 0, b: 100, l: 0};
		hGDim.w = $(barId).width() - hGDim.l - hGDim.r, 
		hGDim.h = $(barId).height() - hGDim.t - hGDim.b;

		//create svg for histogram.
		var hGsvg = d3.select(barId).append("svg")
		//.attr("width", "100%")
		.attr("viewBox", "0 0 800 300").attr("preserveAspectRatio", "xMidYMid meet")
		//.attr("height", hGDim.h + hGDim.t + hGDim.b)
		.append("g")
		.attr("transform", "translate(" + hGDim.l + "," + hGDim.t + ")");

		// create function for x-axis mapping.
		var x = d3.scale.ordinal().rangeRoundBands([0, hGDim.w], 0.1)
		.domain(fD.map(function(d) { return d[0]; }));

		// Add x-axis to the histogram svg.
		hGsvg.append("g").attr("class", "x axis")
		.attr("transform", "translate(0," + hGDim.h + ")")
		.call(d3.svg.axis().scale(x).orient("bottom"))
		.selectAll("text")
		.attr("y", 0)
		.attr("x", 9)
		.attr("dy", ".35em")
		.attr("transform", "rotate(90)")
		.style("text-anchor", "start");

		// Create function for y-axis map.
		var y = d3.scale.linear().range([hGDim.h, 0])
		.domain([0, d3.max(fD, function(d) { return d[1]; })]);

		// Create bars for histogram to contain rectangles and freq labels.
		var bars = hGsvg.selectAll(".bar").data(fD).enter()
		.append("g").attr("class", "bar");

		//create the rectangles.
		bars.append("rect")
		.attr("x", function(d) { return x(d[0]); })
		.attr("y", function(d) { return y(d[1]); })
		.attr("width", x.rangeBand())
		.attr("height", function(d) { return hGDim.h - y(d[1]); })
		.attr('fill',barColor)
		.on("mouseover",mouseover)// mouseover is defined below.
		.on("mouseout",mouseout);// mouseout is defined below.

		//Create the frequency labels above the rectangles.
		bars.append("text").text(function(d){ return d3.format(",")(d[1])})
		.attr("x", function(d) { return x(d[0])+x.rangeBand()/2; })
		.attr("y", function(d) { return y(d[1])-5; })
		.attr("text-anchor", "middle");

		function mouseover(d){  // utility function to be called on mouseover.
			// filter for selected state.
			//@Ivan
			var st = fData.filter(function(s){ return s.ZONE.NAME == d[0];})[0],
			nD = d3.keys(st.DETAILS).map(function(s){ return {type:s, DETAILS:st.DETAILS[s]};});

			// call update functions of pie-chart and legend.    
			pC.update(nD);
			leg.update(nD);
		}

		function mouseout(d){    // utility function to be called on mouseout.
			// reset the pie-chart and legend.    
			pC.update(dF);
			leg.update(dF);
		}

		// create function to update the bars. This will be used by pie-chart.
		hG.update = function(nD, color){
			// update the domain of the y-axis map to reflect change in frequencies.
			y.domain([0, d3.max(nD, function(d) { return d[1]; })]);

			// Attach the new data to the bars.
			var bars = hGsvg.selectAll(".bar").data(nD);

			// transition the height and color of rectangles.
			bars.select("rect").transition().duration(500)
			.attr("y", function(d) {return y(d[1]); })
			.attr("height", function(d) { return hGDim.h - y(d[1]); })
			.attr("fill", color);

			// transition the frequency labels location and change value.
			bars.select("text").transition().duration(500)
			.text(function(d){ return d3.format(",")(d[1])})
			.attr("y", function(d) {return y(d[1])-5; });            
		}        
		return hG;
	}

	// function to handle pieChart.
	function pieChart(pD){
		var pC ={},    pieDim ={w:300, h: 300};
		pieDim.r = Math.min(pieDim.w, pieDim.h) / 2;

		// create svg for pie chart.
		var piesvg = d3.select(pieId).append("svg")
		//.attr("width", pieDim.w).attr("height", pieDim.h)
		.attr("viewBox", "5 8 290 290").attr("preserveAspectRatio", "xMidYMid meet")
		.append("g")
		.attr("transform", "translate("+pieDim.w/2+","+pieDim.h/2+")");

		// create function to draw the arcs of the pie slices.
		var arc = d3.svg.arc().outerRadius(pieDim.r - 10).innerRadius(0);

		// create a function to compute the pie slice angles.
		//@Ivan
		var pie = d3.layout.pie().sort(null).value(function(d) { return d.DETAILS; });

		// Draw the pie slices.
		piesvg.selectAll("path").data(pie(pD)).enter().append("path").attr("d", arc)
		.each(function(d) { this._current = d; })
		.style("fill", function(d) { return segColor(d.data.type); })
		.on("mouseover",mouseover).on("mouseout",mouseout);

		// create function to update pie-chart. This will be used by histogram.
		pC.update = function(nD){
			piesvg.selectAll("path").data(pie(nD)).transition().duration(500)
			.attrTween("d", arcTween);
		}        
		// Utility function to be called on mouseover a pie slice.
		function mouseover(d){
			// call the update function of histogram with new data.
			hG.update(fData.map(function(v){
				//@Ivan
				return [v.ZONE.NAME,v.DETAILS[d.data.type]];}),segColor(d.data.type));
		}
		//Utility function to be called on mouseout a pie slice.
		function mouseout(d){
			// call the update function of histogram with all data.
			hG.update(fData.map(function(v){
				//@Ivan
				return [v.ZONE.NAME,v.total];}), barColor);
		}
		// Animating the pie-slice requiring a custom function which specifies
		// how the intermediate paths should be drawn.
		function arcTween(a) {
			var i = d3.interpolate(this._current, a);
			this._current = i(0);
			return function(t) { return arc(i(t));    };
		}    
		return pC;
	}

	// function to handle legend.
	function legend(lD){
		var leg = {};

		//create svg for the legend table
		var tableSvg =  d3.select(legendId).append("svg")
		.attr("viewBox", "0 0 135 420").attr("preserveAspectRatio", "xMidYMid meet");
		
		// create table for legend.
		var legend = tableSvg.append("foreignObject").attr("width", "100%")
	    .attr("height", "100%").append("xhtml:table").attr('class','legend');

		// create one row per segment.
		var tr = legend.append("tbody").selectAll("tr").data(lD).enter().append("tr");

		// create the first column for each segment.
		tr.append("td").append("svg").attr("width", '16').attr("height", '16').append("rect")
		.attr("width", '16').attr("height", '16')
		.attr("fill",function(d){ return segColor(d.type); });

		// create the second column for each segment.
		tr.append("td").text(function(d){ return mapDayLegend(d.type); });

		// create the third column for each segment.
		tr.append("td").attr("class",'legendFreq')
		//@Ivan
		.text(function(d){ return d3.format(",")(d.DETAILS);});

		// Utility function to be used to update the legend.
		leg.update = function(nD){
			// update the data attached to the row elements.
			var l = legend.select("tbody").selectAll("tr").data(nD);

			// update the frequencies.
			//@Ivan
			l.select(".legendFreq").text(function(d){ return d3.format(",")(d.DETAILS);});

		}

		return leg;
	}


	if (groupType == 1){
		var dF = ['1', '2', '3', '4', '5', '6', '7'].map(function(d){ 
			return {type:d, DETAILS: (d3.mean(fData.map(function(t){ return t.DETAILS[d];}))).toFixed(2)}; 
		});
	} else {
		var dF = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'].map(function(d){ 
			return {type:d, DETAILS: (d3.mean(fData.map(function(t){ return t.DETAILS[d];}))).toFixed(2)}; 
		});
	}
	

	// calculate total frequency by state for all segment.
	//@Ivan
	var sF = fData.map(function(d){return [d.ZONE.NAME, d.total];});

	var hG = histoGram(sF), // create the histogram.
	pC = pieChart(dF), // create the pie-chart.
	leg= legend(dF);  // create the legend.
}