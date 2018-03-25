//barChartId - Id of the div where bar char will be rendered
//fData - data that will be shown on bar chart
function drawHorizontalbarChart(barChartId, fData){
	
	fData.forEach(function(d) {
		if (d.ZONE!=null){
			d.label = d.ZONE.NAME;
		}
		if (d.NO_EVENTS!=null){
			d.value = d.NO_EVENTS; 
		} else if (d.FEE!=null){
			d.value = d.FEE
		}
	});

	//Empty the div
	$(barChartId).empty();
	
    var div = d3.select(barChartId).append("div").attr("class", "toolTip");

    var axisMargin = 20,
            margin = 40,
            valueMargin = 4,
            width = parseInt(d3.select(barChartId).style('width'), 10),
            height = parseInt(d3.select(barChartId).style('height'), 10),
            barHeight = (height-axisMargin-margin*2)* 0.85/fData.length,
            barPadding = 5,
            fData, bar, svg, scale, xAxis, labelWidth = 0;

    max = d3.max(fData, function(d) { return d.value; });

    svg = d3.select(barChartId)
            .append("svg")
            .attr("width", width)
            .attr("height", height);


    bar = svg.selectAll("g")
            .data(fData)
            .enter()
            .append("g");

    bar.attr("class", "bar")
            .attr("cx",0)
            .attr("transform", function(d, i) {
                return "translate(" + margin + "," + (i * (barHeight + barPadding) + barPadding) + ")";
            });

    bar.append("text")
            .attr("class", "label")
            .attr("y", barHeight / 2)
            .attr("dy", ".35em") //vertical align middle
            .text(function(d){
                return d.label;
            }).each(function() {
        labelWidth = Math.ceil(Math.max(labelWidth, this.getBBox().width));
    });

    scale = d3.scale.linear()
            .domain([0, max])
            .range([0, width - margin*2 - labelWidth]);

    xAxis = d3.svg.axis()
            .scale(scale)
            .tickSize(-height + 2*margin + axisMargin)
            .orient("bottom");

    bar.append("rect")
            .attr("transform", "translate("+labelWidth+", 0)")
            .attr("height", barHeight)
            .attr("width", function(d){
                return scale(d.value);
            });

    bar.append("text")
            .attr("class", "value")
            .attr("y", barHeight / 2)
            .attr("dx", -valueMargin + labelWidth) //margin right
            .attr("dy", ".35em") //vertical align middle
            .attr("text-anchor", "end")
            .text(function(d){
                return (d.value);
            })
            .attr("x", function(d){
                var width = this.getBBox().width;
                return Math.max(width + valueMargin, scale(d.value));
            });

    svg.insert("g",":first-child")
            .attr("class", "axisHorizontal")
            .attr("transform", "translate(" + (margin + labelWidth) + ","+ (height - axisMargin - margin)+")")
            .call(xAxis);
}