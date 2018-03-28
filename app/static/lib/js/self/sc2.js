var curr_quadrant = -1;
var new_quadrant;
var generated = false;
var suit_length = 100;
function generate_scatter_plot1(selected_zcta)
{
	// var selected_zcta = $("#scatter_plot1_select_zcta :selected").text();
	// var selected_occ = $("#scatter_plot1_select_occ :selected").text();

	//scatter_plot1_data[0] -> suitability, scatter_plot1_data[1] ->  location quotient
	suit_length = runif(50, 200);
	var scatter_plot1_data = [];
	for (var i = 0; i < suit_length; i++) {
		scatter_plot1_data.push([runif(-1, 1)]);
	}

	for (var i = 0; i < suit_length; i++) {
		scatter_plot1_data[i].push(Math.abs(rnorm(0, 1)));
	}

	for (var i = 0; i < scatter_plot1_data.length; i++) {
		scatter_plot1_data[i].key = i+1;
		scatter_plot1_data[i].name = "TEMP";
		scatter_plot1_data[i].type = "industry";
	}


	generate_scatter_plot(scatter_plot1_data);

	
}



function generate_scatter_plot(scatter_plot1_data) 
{
	

	var margin = {top: 20, right: 20, bottom: 130, left: 60},
      width = 560 - margin.left - margin.right,
      height = 600 - margin.top - margin.bottom,
      duration = 1000, svg, focus_duration = 400;

    var margin_slider_automation = {top: height + 40, left: 20, right: 20};

    x = d3.scale.linear()
      .range([0, width]);

    y = d3.scale.linear()
      .range([height, 0]);

    var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

    var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left");


    x.domain(d3.extent(scatter_plot1_data, function(d) { return d3.max([0, d[1]]); })).nice();
	y.domain(d3.extent(scatter_plot1_data, function(d) { return d[0]; })).nice();

    var quad_x_bounds = []; //x2,y2 
    var quad_x_x2 = x.ticks()[x.ticks().length - 1];
    var quad_x_y2 = (y.ticks()[y.ticks().length - 1] + y.ticks()[0]) / 2;
    quad_x_bounds.push([quad_x_x2, quad_x_y2]);

    var quad_y_bounds = [];
    // x2 = (x.ticks()[x.ticks().length - 1] + x.ticks()[0]) / 2;
    var quad_y_x2 = 1; //for location quotient 1
    var quad_y_y2 = y.ticks()[y.ticks().length - 1];
    var quad_y_y1 = y.ticks()[0];
    quad_y_bounds.push([quad_y_x2, quad_y_y2, quad_y_y1]); //x2, y2, y1(not necessarilily 0)

    quad_x_bounds[0].axis = "X";
	quad_y_bounds[0].axis = "Y";

	var rect_x1, rect_x2, rect_width, rect_height;



    var drag_scatter = d3.behavior.drag()
    			.origin(function(d) {
    				var t1 = {};
    				// console.log(d);
    				if(d.axis == "X") {
    					t1.x = x(quad_y_bounds[0]); //as data bound has no X information
    					t1.y = y(d[1]);
    					return  t1;
    				} else {
    					t1.x = x(d[0]);
    					t1.y = y(quad_x_bounds[1]); //as data bound has no Y information
    					return t1;
    				}
    			})
    			.on("dragstart", dragstarted_scatter)
    			.on("drag", dragged_scatter)
    			.on("dragend", dragend_scatter);




    if(generated == false)
    {
    	svg = d3.select("#scatter_plot1").append("svg")
				      .attr("width", width + margin.left + margin.right)
				      .attr("height", height + margin.top + margin.bottom)
				      .append("g")
				      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
				      .attr("id", "scatter_plot1_group");
		
		svg.append("g")
	        .attr("class", "x axis")
	        .attr("transform", "translate(0," + height + ")")
	        .call(xAxis)
	        .append("text")
	        .attr("class", "label")
	        .attr("x", width)
	        .attr("y", -6)
	        .style("text-anchor", "end")
	        .text("Location Quotient");

	    svg.append("g")
	        .attr("class", "y axis")
	        .call(yAxis)
	        .append("text")
	        .attr("class", "label")
	        .attr("transform", "rotate(-90)")
	        .attr("y", -50)
	        .attr("dy", ".71em")
	        .style("text-anchor", "end")
	        .text("Suitability");

	    svg.selectAll(".quad_lines.quad_x")
			.data(quad_x_bounds)
			.enter()
			.append("line")
			.attr("class", "quad_lines quad_x")
			.attr("x1", x(0))
			.attr("y1", function(d) {return y(d[1]); })
			.attr("x2", function(d) {return x(d[0]); })
			.attr("y2", function(d) {return y(d[1]); })
			.call(drag_scatter);

		svg.append("text")
			.attr("class", "quad_x_text")
			.attr("x", x(quad_x_bounds[0][0]))
			.attr("y", y(quad_x_bounds[0][1]))
			.attr("stroke", "none")
			.attr("fill", "red")
			.text("5.5")
			.attr("dx", -9)
			.attr("dy", -4)
			.style("opacity", 0);

		svg.selectAll(".quad_lines.quad_y")
			.data(quad_y_bounds)
			.enter()
			.append("line")
			.attr("class", "quad_lines quad_y")
			.attr("x1", function(d) {return x(d[0]); })
			.attr("y1", function(d) {return y(d[2]); })
			.attr("x2", function(d) {return x(d[0]); })
			.attr("y2", function(d) {return y(d[1]); })
			.call(drag_scatter);

		svg.append("text")
			.attr("class", "quad_y_text")
			.attr("x", x(quad_y_bounds[0][0]))
			.attr("y", y(quad_y_bounds[0][1]))
			.attr("stroke", "none")
			.attr("fill", "red")
			.text("12")
			.attr("dx", 3)
			.attr("dy", 7)
			.style("opacity", 0);

	    svg.selectAll(".dot")
	        .data(scatter_plot1_data, function(d) {return d.key;})
	        .enter()
	        .append("circle")
	        .attr("class", "dot")
	        .attr("r", 2)
	        .attr("cx", function(d) { return 0; })
	        .attr("cy", function(d) { return 0; })
	        .style("fill", function(d) { return "rgb(31, 119, 180)"; })
	        .attr("opacity", function(d) {if(d[1] == -1) {return 0} else{return 1}})
	        .on("click", function(d, ind_index) { generate_scatter_plot_report(zcta_index, ind_index);} );

	    svg.selectAll(".dot")
	    	.transition()
	    	.duration(duration)
	    	.attr("cx", function(d) { return x(d[1]); })
	        .attr("cy", function(d) { return y(d[0]); })
	        .attr("opacity", function(d) {
	        	if(d[1] == -1) 
	        	{
	        		return 0;
	        	} else
	        	{
	        		return 1;
	        	}
	        });

	    // console.log(quad_x_bounds);
	    // console.log(quad_y_bounds);  

	    svg.insert("rect", ".quad_lines.quad_x")
	    	.attr("width", width)
	    	.attr("height", height)
	    	.attr("x", 0)
	    	.attr("y", 0)
	    	.attr("class", "scatter_plot1_background")
	    	.on("mouseover", mouseover)
	    	.on("mousemove", mousemove)
	    	.on("mouseout", mouseout)
	    	.on("click", mouseclick_focus);

		generated = true;
    } else {

    	var svg = d3.select("#scatter_plot1_group");
		
	    svg.select(".x.axis")
	    	.transition()
	    	.duration(duration)
	        .call(xAxis);
	        
	    svg.select(".y.axis")
	    	.transition()
	    	.duration(duration)
	        .call(yAxis);
	        

	    svg.selectAll(".dot")
	        .data(scatter_plot1_data, function(d) {return d.key;})
	        .enter()
	        .append("circle")
	        .attr("class", "dot")
	        .attr("r", 2)
	        .attr("cx", function(d) { return 0; })
	        .attr("cy", function(d) { return 0; })
	        .attr("fill", "rgb(31, 119, 180)")
	        .attr("opacity", function(d) {if(d[1] == -1) {return 0} else{return 1}})
	        .on("click", function(d, ind_index) { generate_scatter_plot_report(zcta_index, ind_index);} );	  


	    svg.selectAll(".dot")
	    	.transition()
	    	.duration(duration)
	    	.attr("cx", function(d) { return x(d[1]); })
	        .attr("cy", function(d) { return y(d[0]); })
	        .attr("opacity", function(d) {
	        	if(d[1] == -1) 
	        	{
	        		return 0;
	        	} else
	        	{
	        		return 1
	        	}
	        });

	    svg.selectAll(".dot")
			.data(scatter_plot1_data, function(d) {return d.key;})
			.exit()
			.remove();

		// console.log(quad_x_bounds);
	    // console.log(quad_y_bounds);

		svg.selectAll(".quad_lines.quad_x")
			.data(quad_x_bounds)
			.transition()
			.duration(duration)
			.attr("x1", x(0))
			.attr("y1", function(d) {return y(d[1]); })
			.attr("x2", function(d) {return x(d[0]); })
			.attr("y2", function(d) {return y(d[1]); });
			

		svg.selectAll(".quad_lines.quad_y")
			.data(quad_y_bounds)
			.transition()
			.duration(duration)
			.attr("x1", function(d) {return x(d[0]); })
			.attr("y1", function(d) {return y(d[2]); })
			.attr("x2", function(d) {return x(d[0]); })
			.attr("y2", function(d) {return y(d[1]); });

		
		//taking care of the quad focus rectangle
    	if(new_quadrant == 1) {
			rect_x1 = quad_y_bounds[0][0];
			rect_y1 = quad_y_bounds[0][1];
			rect_x2 = quad_x_bounds[0][0];
			rect_y2 = quad_x_bounds[0][1];
		} else if(new_quadrant == 2) {
			rect_x1 = 0;
			rect_y1 = quad_y_bounds[0][1];
			rect_x2 = quad_y_bounds[0][0];
			rect_y2 = quad_x_bounds[0][1];
		} else if (new_quadrant == 3) {
			rect_x1 = 0;
			rect_y1 = quad_x_bounds[0][1];
			rect_x2 = quad_y_bounds[0][0];
			rect_y2 = quad_y_bounds[0][2];
		} else {
			rect_x1 = quad_y_bounds[0][0];
			rect_y1 = quad_x_bounds[0][1];
			rect_x2 = quad_x_bounds[0][0];
			rect_y2 = quad_y_bounds[0][2];
		}

		rect_width = Math.abs(x(rect_x2) - x(rect_x1));
		rect_height = Math.abs(y(rect_y2) - y(rect_y1));

		svg.select(".scatter_plot1_focus")
			.transition()
			.duration(duration)
			.attr("x", x(rect_x1))
			.attr("y", y(rect_y1))
			.attr("width", rect_width)
			.attr("height", rect_height)
			.attr("fill", "#ffff99")
			.attr("cursor", "pointer")
			.attr("class", "scatter_plot1_focus")
			.attr("opacity", 0.6);

		d3.select(".handle_automation")
			.transition()
			.duration(duration)
			.attr("cx", x_slider.range()[0]);
	}

	function mouseover() {
    	var curr_x = x.invert(d3.mouse(this)[0]);
    	var curr_y = y.invert(d3.mouse(this)[1]);
    	if(curr_x  > quad_y_bounds[0][0]) {
    		if(curr_y > quad_x_bounds[0][1]) {
    			new_quadrant = 1;
    		} else {
    			new_quadrant = 4;
    		}
    	} else {
    		if(curr_y > quad_x_bounds[0][1]) {
    			new_quadrant = 2;
    		} else {
    			new_quadrant = 3;
    		}
		}

		// console.log(curr_x + " , " + curr_y);
		// console.log(quad_x_bounds);
		// console.log(quad_y_bounds);
    	// console.log(curr_quadrant);
    }

    function mousemove() {
    	var curr_x = x.invert(d3.mouse(this)[0]);
    	var curr_y = y.invert(d3.mouse(this)[1]);
    	
    	if(curr_x  > quad_y_bounds[0][0]) {
    		if(curr_y > quad_x_bounds[0][1]) {
    			new_quadrant = 1;
    		} else {
    			new_quadrant = 4;
    		}
    	} else {
    		if(curr_y > quad_x_bounds[0][1]) {
    			new_quadrant = 2;
    		} else {
    			new_quadrant = 3;
    		}
		}
		if (new_quadrant != curr_quadrant) {

			svg.select(".scatter_plot1_focus")
				.attr("opacity", 0)
				.remove();

			t1 = generate_focus_coord();
			rect_x1 = t1[0];
			rect_y1 = t1[1];
			rect_width = t1[2];
			rect_height = t1[3]; 

			// console.log("Rectangle data: (X,Y) (" + rect_x1 + ", " + rect_y1 + ") width and height: (" + x.invert(rect_width)+ ", " + y.invert(rect_height)+ ")" );

			svg.insert("rect", ".scatter_plot1_background")
				.attr("x", x(rect_x1))
				.attr("y", y(rect_y1))
				.attr("width", rect_width)
				.attr("height", rect_height)
				.attr("fill", "#ffff99")
				.attr("cursor", "pointer")
				.attr("class", "scatter_plot1_focus")
				.attr("opacity", 0)
				.transition()
				.duration(focus_duration)
				.attr("opacity", 0.6);

			curr_quadrant = new_quadrant;
		}

		// console.log(curr_quadrant);
    	// console.log(x.invert(d3.mouse(this)[0]) + ", " + y.invert(d3.mouse(this)[1]));
    }

    function generate_focus_coord() {
    	var rect_x1, rect_x2, rect_width, rect_height, rect_y1, rect_y2;

    	quad_x_bounds = []; //x2,y2 
	    var quad_x_x2 = x.ticks()[x.ticks().length - 1];
	    var quad_x_y2 = y.invert(d3.select(".quad_x").attr("y1")); //getting new Y coordinate of the X-axis line
	    quad_x_bounds.push([quad_x_x2, quad_x_y2]);

	    quad_y_bounds = [];
	    var quad_y_x2 = x.invert(d3.select(".quad_y").attr("x1")); //getting new X coordinate of the Y-axis line
	    var quad_y_y2 = y.ticks()[y.ticks().length - 1];
	    var quad_y_y1 = y.ticks()[0];
	    quad_y_bounds.push([quad_y_x2, quad_y_y2, quad_y_y1]); //x2, y2, y1(not necessarilily 0)

	    quad_x_bounds[0].axis = "X";
		quad_y_bounds[0].axis = "Y";

		if(new_quadrant == 1) {
			rect_x1 = quad_y_bounds[0][0];
			rect_y1 = quad_y_bounds[0][1];
			rect_x2 = quad_x_bounds[0][0];
			rect_y2 = quad_x_bounds[0][1];
		} else if(new_quadrant == 2) {
			rect_x1 = 0;
			rect_y1 = quad_y_bounds[0][1];
			rect_x2 = quad_y_bounds[0][0];
			rect_y2 = quad_x_bounds[0][1];
		} else if (new_quadrant == 3) {
			rect_x1 = 0;
			rect_y1 = quad_x_bounds[0][1];
			rect_x2 = quad_y_bounds[0][0];
			rect_y2 = quad_y_bounds[0][2];
		} else {
			rect_x1 = quad_y_bounds[0][0];
			rect_y1 = quad_x_bounds[0][1];
			rect_x2 = quad_x_bounds[0][0];
			rect_y2 = quad_y_bounds[0][2];
		}

		rect_width = Math.abs(x(rect_x2) - x(rect_x1));
		rect_height = Math.abs(y(rect_y2) - y(rect_y1));
		// console.log( rect_x1 + ", " + rect_y1 );
		// console.log( rect_x2 + ", " + rect_y2 );
		// console.log( new_quadrant + ": " + rect_x1 + ", " + rect_y1 + " ||| "+ rect_x2 + ", " + rect_y2);

		return [rect_x1, rect_y1, rect_width, rect_height];
    }

    //Do not remove, it messes up somehow
    function mouseout() { //TODO implement removing focus when out of the SVG
    // 	console.log();
    // 	svg.select(".scatter_plot1_focus")
				// .attr("opacity", 0)
				// .remove();
    	// console.log(x.invert(d3.mouse(this)[0]) + ", " + y.invert(d3.mouse(this)[1]));
    }
    
    function mouseclick_focus() {
    	reference_origin = [ quad_y_bounds[0][0], quad_x_bounds[0][1] ]
		str1 = "";
		d3.selectAll(".dot")
			.attr("r", 2)
			.style("stroke", "#000")
			.style("stroke-width", null)
			.filter(function(d) {
    			var dot_x = d[1];
    			var dot_y = d[0];
    			var point_quadrant;
    			if(dot_x > reference_origin[0]) {
    				if(dot_y > reference_origin[1]) {
    					point_quadrant = 1;
    				} else {
    					point_quadrant = 4;
    				}
    			} else {
					if(dot_y > reference_origin[1]) {
					    point_quadrant = 2;
					} else {
					    point_quadrant = 3;				
					}
    			}

    			if(point_quadrant == new_quadrant) {
    				return true;
    			}
    		})
    		.attr("r", 3)
    		.style("stroke", "red")
    		.style("stroke-width", "1")
    		.each(function(d) {
    			// console.log(d.name);
    			str1 = str1 + '<tr><td>' + d.name + "</td></tr>";
    		});

    	$("#map_settings_scatter_ind_list_table").html(str1);
    }

    function dragstarted_scatter(d) {
    	
    	if(d.axis == "X") {
			d3.select(this)
    			.attr("id", "dragging_scatter_x");
    	} else {
    		d3.select(this)
    			.attr("id", "dragging_scatter_y");
    	}
	}

    function dragged_scatter(d) {

    	if(d.axis == "X") {
    		d3.select(this).attr("y1", d3.mouse(this)[1]).attr("y2", d3.mouse(this)[1]);
    		d3.select(".quad_x_text").style("opacity", 1);
    		d3.select(".quad_x_text").attr("y", d3.mouse(this)[1]);
    		d3.select(".quad_x_text").text((y.invert(d3.mouse(this)[1])).toFixed(2));
    		quad_x_bounds[0][1] = y.invert(d3.mouse(this)[1]);
    		if(new_quadrant == 1 || new_quadrant == 2) {
    			d3.select(".scatter_plot1_focus").attr("height", Math.abs(y(quad_y_bounds[0][1]) - y(quad_x_bounds[0][1])));
    		} else {
    			d3.select(".scatter_plot1_focus").attr("y", y(quad_x_bounds[0][1])).attr("height", Math.abs(y(quad_x_bounds[0][1]) - y(quad_y_bounds[0][2])));
    		}
    		
    	} else {
			d3.select(this).attr("x1", d3.mouse(this)[0]).attr("x2", d3.mouse(this)[0]);
			d3.select(".quad_y_text").style("opacity", 1);
			d3.select(".quad_y_text").attr("x", d3.mouse(this)[0]);
			d3.select(".quad_y_text").text((x.invert(d3.mouse(this)[0])).toFixed(2));
			quad_y_bounds[0][0] = x.invert(d3.mouse(this)[0]);
			if(new_quadrant == 2 || new_quadrant == 3) {
    			d3.select(".scatter_plot1_focus").attr("width", Math.abs(x(quad_y_bounds[0][0]) - x(0)));
    		} else {
    			d3.select(".scatter_plot1_focus").attr("x", x(quad_y_bounds[0][0])).attr("width", Math.abs(x(quad_x_bounds[0][0]) - x(quad_y_bounds[0][0])));
    		}
    	}

	}

    function dragend_scatter(d) {
    	d3.select(this)
    		.attr("id", null);
    	d3.select(".quad_x_text").style("opacity", 0);
		d3.select(".quad_y_text").style("opacity", 0);

    }

}


generated_report = false;
//  zcta_lq_arr;
//  ind_lq_arr;
function generate_scatter_plot_report(zcta_index, ind_index) 
{ 
	var ind_lq_arr = ind_lq[ind_index].slice();
	var  zcta_lq_arr = zcta_lq[zcta_index].slice();
	for ( i = 0; i < ind_lq_arr.length; i++) {
		ind_lq_arr[i] = [ind_lq_arr[i], i];
	}

	ind_lq_arr.sort(function(a, b) {
		return b[0] - a[0];
	});

	var sorted_occ_indices = [];
	for ( i = 0; i < ind_lq_arr.length; i++) {
		sorted_occ_indices.push(ind_lq_arr[i][1])
		ind_lq_arr[i] = ind_lq_arr[i][0];
	}

	var corresponding_zcta_occ_values = [];
	for ( i = 0; i < zcta_lq_arr.length; i++) {
		corresponding_zcta_occ_values.push(zcta_lq_arr[sorted_occ_indices[i]]);  
	}

	// console.log("Industry: " + ind_index + "top 5 LQs indices");
	// console.log(sorted_occ_indices.slice(0, 5));
	// console.log("Values:");
	// console.log(ind_lq_arr.slice(0, 5));

	// console.log("Corresponding lq for zcta: " + zcta_index + " :")
	// console.log(corresponding_zcta_occ_values.slice(0,5));

	var compare_no = 5;
	var final_ind_lq = ind_lq_arr.slice(0, 5);
	var final_zcta_lq = corresponding_zcta_occ_values.slice(0, 5);

	var dataset = [];
	var j = 0;
	for ( i = 0; i < 5; i++) {
		dataset.push({key: ++j, value: final_ind_lq[i]});
		dataset.push({key: ++j, value: final_zcta_lq[i]});
	}


	var margin = {top: 20, right: 20, bottom: 30, left: 60},
      width = 560 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom,
      duration = 1000;

    var yScale = d3.scale.ordinal()
    		.domain(d3.range(dataset.length))
      		.rangeRoundBands([0, height], 0.05);

    var xScale = d3.scale.linear()
    				.domain([0, d3.max(dataset, function(d){ return d.value;})])
      				.range([0, width]);

    var key = function(d) {
    	return d.key;
    }

    var xAxis = d3.svg.axis()
      .scale(xScale)
      .orient("bottom");

    var yAxis = d3.svg.axis()
      .scale(yScale)
      .orient("left");

    //  zoom = d3.behavior.zoom().scaleExtent([1, 10])

    if(generated_report == false)
    {
    	var svg = d3.select("#scatter_report1").append("svg")
				      .attr("width", width + margin.left + margin.right)
				      .attr("height", height + margin.top + margin.bottom)
				      .append("g")
				      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
				      .attr("id", "scatter_report1_group");
				      // .call(zoom);

	    // x.domain(d3.extent(scatter_plot1_data, function(d) { return d3.max([0, d[1]]); })).nice();
	    // y.domain(d3.extent(scatter_plot1_data, function(d) { return d[0]; })).nice();

	    svg.append("g")
	        .attr("class", "x axis")
	        .attr("transform", "translate(0," + height + ")")
	        .call(xAxis)
	        .append("text")
	        .attr("class", "label")
	        .attr("x", width)
	        .attr("y", -6)
	        .style("text-anchor", "end")
	        .text("Location Quotient");

	    svg.append("g")
	        .attr("class", "y axis")
	        .call(yAxis);
	        // .append("text")
	        // .attr("class", "label")
	        // .attr("transform", "rotate(-90)")
	        // .attr("y", -50)
	        // .attr("dy", ".71em")
	        // .style("text-anchor", "end")
	        // .text("Labor Market Suitability");

	    svg.selectAll("rect")
			   .data(dataset, key)
			   .enter()
			   .append("rect")
			   .attr("x", function(d) {
			   		return 0;
			   })
			   .attr("y", function(d, i) {
			   		return yScale(i);
			   })
			   .attr("height", yScale.rangeBand())
			   .attr("width", function(d) {
			   		return xScale(d.value);
			   })
			   .attr("fill", function(d, i) {
			   		if(i%2 == 0) {
			   			return "rgb(0, 0, " + 245 + ")";
			   		} else {
			   			return "rgb(0, 0, " + 100 + ")";
			   		}
					
			   });

	    // svg.selectAll(".dot")
	    // 	.transition()
	    // 	.duration(duration)
	    // 	.attr("cx", function(d) { return x(d[1]); })
	    //     .attr("cy", function(d) { return y(d[0]); })
	    //     .attr("opacity", function(d) {
	    //     	if(d[1] == -1) 
	    //     	{
	    //     		return 0;
	    //     	} else
	    //     	{
	    //     		return 1;
	    //     	}
	    //     });
	        
	    generated_report = true;
    } else {
    	var svg = d3.select("#scatter_report1_group");
				      

	    var yScale = d3.scale.ordinal()
    		.domain(d3.range(dataset.length))
      		.rangeRoundBands([0, height], 0.05);

	    var xScale = d3.scale.linear()
	    				.domain([0, d3.max(dataset, function(d){ return d.value;})])
	      				.range([0, width]);

	    var key = function(d) {
	    	return d.key;
	    }

	    var xAxis = d3.svg.axis()
	      .scale(xScale)
	      .orient("bottom");

	    var yAxis = d3.svg.axis()
	      .scale(yScale)
	      .orient("left");

	    //Select…
		var bars = svg.selectAll("rect")
					.data(dataset, key);
	        

	    //Enter…
		bars.enter()
			   .append("rect")
			   .attr("x", function(d) {
			   		return 0;
			   })
			   .attr("y", function(d, i) {
			   		return yScale(i);
			   })
			   .attr("height", yScale.rangeBand())
			   .attr("width", function(d) {
			   		return xScale(d.value);
			   })
			   .attr("fill", function(d, i) {
			   		if(i%2 == 0) {
			   			return "rgb(0, 0, " + 245 + ")";
			   		} else {
			   			return "rgb(0, 0, " + 100 + ")";
			   		}
					
			   });	        

	    //Update…
		bars.transition()
			.duration(500)
			.attr("x", function(d) {
				return 0;
			})
			.attr("y", function(d, i) {
				return yScale(i);
			})
			.attr("height", yScale.rangeBand())
			.attr("width", function(d) {
				return xScale(d.value);
			});

	    bars.exit()
			.transition()
			.duration(500)
			.attr("x", -yScale.rangeBand())
			.remove();
    }
}

function close_analysis_space() 
{
	$("#map1").css("height", "98vh");
    $("#map2").css("height", "98vh");
    mymap1.invalidateSize(true);
    mymap2.invalidateSize(true);
	$("#analysis_space").css("visibility", "hidden");
    d3.select("#scatter_plot1 > svg").remove();
    generated = false;
    generated_report = false;
}