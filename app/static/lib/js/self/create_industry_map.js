$(document).ready(
    function () {
        console.log("creating industry heirarchy visualization");
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState === 4 && this.status === 200) {
                    console.log("industry heirarchy data received");
                    received_data = JSON.parse(this.responseText)[0];
                    create_ind_hier(received_data);
                }
            };
            xhttp.open("GET", "/get_ind_heir_data");
            xhttp.send();
    }
);

function create_ind_hier(data) {
    var margin = {top: 180, right: 20, bottom: 30, left: 20},
    width = 1200 - margin.left - margin.right,
    barHeight = 15,
    barWidth = Math.floor(width / 35);

    var text_space = 150;
    var circle_rad = 6;
    var rect_width = 10;
    var rect_space = 15;

    var i = 0,
    duration = 500,
    root = data,
    source = data;

    var tree = d3.layout.tree()
    .nodeSize([0, 15]);

    var diagonal = d3.svg.line().interpolate('step-before')
        .x(function (d) { return d.x; })
        .y(function (d) { return d.y; });

    var svg = d3.select("#map3").append("svg")
        .attr("width", width + margin.left + margin.right)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    source.x0 = 0;
    source.y0 = 0;

    update(source);

    function update(source) {
            // Compute the flattened node list. TODO use d3.layout.hierarchy.
        nodes = tree.nodes(root);

          var scales = get_scales(nodes);

          var height = Math.max(500, nodes.length * barHeight + margin.top + margin.bottom);

          d3.select("#map3 svg").transition()
              .duration(duration)
              .attr("height", height);

          d3.select(self.frameElement).transition()
              .duration(duration)
              .style("height", height + "px");

          // Compute the "layout".
          nodes.forEach(function(n, i) {
            n.x = i * barHeight;
          });

          // Update the nodes…
          var node = svg.selectAll("g.node")
              .data(nodes, function(d) { return d.id || (d.id = ++i); });

          var nodeEnter = node.enter().append("g")
              .attr("class", "node")
              .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
              .style("opacity", 1e-6);

          // Enter any new nodes at the parent's previous position.
          nodeEnter.append("circle")
              .attr("r", circle_rad)
              .style("fill", color)
              .on("click", click);

          nodeEnter.append("text")
              .on("mouseover", function(d){
                  var x1 = d.y;
                  var x2 = width*3/4;
                  var y = d.x - circle_rad;
                  d3.selectAll(".temp_line2").remove();
                  svg.append("line").attr("class","temp_line2").attr("x1",x1).attr("y1",y).attr("x2",x2).attr("y2",y).attr("stroke-width",1).attr("stroke", "black");
                  svg.append("line").attr("class","temp_line2").attr("x1",x1).attr("y1",y + 2*circle_rad).attr("x2",x2).attr("y2",y + 2*circle_rad).attr("stroke-width",1).attr("stroke", "black");
              })
              .attr("dy", 2.5)
              .attr("dx", 7.5)
              .text(function(d) {
                t6 = (d.data[0].length > 26 ? 27 : d.data[0].length);
                return d.data[0].substr(0, t6) + (d.data[0].length > 28 ? "..." : "");
            })
              .append("title")
              .text(function(d){return d.data[0];});

          nodeEnter.each(function(d, i) {
            t2 = d.data[3];
            t1 = [];


            for (var key in t2) {
              if(t2.hasOwnProperty(key)) {
                t1.push([key, t2[key]]);
                //console.log(d[key]);
              }
            }

            t3 = d.depth;
            if(t3 == 1) {
              t4 = barHeight * 3;
            }
            else if(t3 == 2){
              t4 = barHeight*2;
            }
            else if(t3 == 3){
              t4 = barHeight;
            }
            else if(t3 == 4){
              t4 = 0;
            }
            else{
              t4 = 0;
              if(t3 !=0) {
                console.log(d);
                console.log("Depth Error");
              }
            }


            // d3.select(this)
            //   .append('g')
            //   .attr('class', 'skill_card')
            //   .attr('transform', 'translate('+ text_space +', -'+ circle_rad +')')
            //   .selectAll('rect')
            //   .data(t1)
            //   .enter()
            //   .append('rect')
            //   .attr('x', function(d, i) {return t4 + i*10;})
            //   .attr("width", rect_width)
            //   .attr("height", 2*circle_rad)
            //   .attr("rx", 2)
            //   .attr("ry", 2)
            //   .style("fill", function(d){ return colorScale1(d);});
            var t5;
            if(t3 == 2) {
              t5 = text_space + t4 - barHeight;
            }
            else if(t3 == 3) {
              t5 = text_space + t4;
            }
            else if(t3 == 4) {
              t5 = text_space + t4 + barHeight;
            }
            else{
              t5 = text_space;
            }




            d3.select(this)
              .append('g')
              .attr('class', 'skill_card')
              .attr('transform', 'translate('+ t5 +', -'+ circle_rad +')')
              .selectAll('rect')
              .data(t1)
              .enter()
              .append('rect')
              .attr('x', function(d, i) {return t4 + i*rect_space;})
              .attr("width", rect_width)
              .attr("height", 2*circle_rad)
              .attr("rx", 2)
              .attr("ry", 2)
              .style("fill", function(d){ return scales[d[0]].getColorInRange(d[1]);})
              .append("title")
              .text(function(d){return d[1]});

          d3.selectAll(".skill_card")
            .transition()
            .duration(duration)
            .attr('transform', 'translate('+ text_space +', -'+ circle_rad +')')

          });

          // nodeEnter.selectAll("g.node_rect").append("rect")
          //             .attr("x", function(d) { return  (d.skill_name - 1) * gridSize; })
          //             .attr("y", function(d) { return  (d.occupation_name - 1) * gridSize; })
          //             .attr("rx", 4)
          //             .attr("ry", 4)
          //             .attr("class", "skill_intensity")
          //             .attr("width", gridSize)
          //             .attr("height", gridSize)
          //             .style("fill", colors[0])
          //             .append("title");

          // Transition nodes to their new position.


          nodeEnter.transition()
              .duration(duration)
              .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })
              .style("opacity", 1);

          node.transition()
              .duration(duration)
              .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })
              .style("opacity", 1)
              .select("circle")
              .style("fill", color);

          // Transition exiting nodes to the parent's new position.
          node.exit().transition()
              .duration(duration)
              .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
              .style("opacity", 1e-6)
              .remove();

          // Update the links…
          var link = svg.selectAll("path.link")
              .data(tree.links(nodes), function(d) { return d.target.id; });

          // Enter any new links at the parent's previous position.
          link.enter().insert("path", "g")
              .attr("class", "link")
              .attr("d", function(d) {
                var o = {x: source.x0, y: source.y0};
                return diagonal([{y: d.source.x, x: d.source.y}, {y: d.source.x, x: d.source.y}]);
              })
            .transition()
              .duration(duration)
              .attr("d", function(d) {
                return diagonal(
                  [{
                          y: d.source.x,
                          x: d.source.y
                      }, {
                          y: d.target.x,
                          x: d.target.y
                  }]
                );

              });

          // Transition links to their new position.
          link.transition()
              .duration(duration)
              .attr("d", function(d) {
                return diagonal(
                  [{
                          y: d.source.x,
                          x: d.source.y
                      }, {
                          y: d.target.x,
                          x: d.target.y
                  }]
                );

              });

          // Transition exiting nodes to the parent's new position.
          link.exit().transition()
              .duration(duration)
              .attr("d", function(d) {
                return diagonal(
                  [{
                          y: d.source.x,
                          x: d.source.y
                      }, {
                          y: d.source.x,
                          x: d.source.y
                  }]
                );

              })
              .remove();

          // Stash the old positions for transition.
          nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
          });

          t8 = (text_space + t4 + barHeight -2);
          t9 = (text_space + 4*barHeight - 2);
          // var skill_labels1 = svg.selectAll(".skill_labels")
          //         .data(skill_list_real)
          //         .enter().append("text")
          //           .attr("class", "skill_labels")
          //           .on("click", function(d, i) {
          //               var x = i * rect_space + t9;
          //               var y1 = 0;
          //               var y2 = y1 + height;
          //               d3.selectAll(".temp_line1").remove();
          //               svg.append("line").attr("class","temp_line1").attr("x1",x).attr("y1",y1).attr("x2",x).attr("y2",y2).attr("stroke-width",2).attr("stroke", "black");
          //               svg.append("line").attr("class","temp_line1").attr("x1",x+rect_width +3).attr("y1",y1).attr("x2",x+rect_width+3).attr("y2",y2).attr("stroke-width",2).attr("stroke", "black");
          //
          //           })
          //           .text(function(d) { return d; })
          //           .attr("x", function(d, i) { return i * rect_space; })
          //           .attr("y", 0)
          //           .style("text-anchor", "start")
          //           .attr("transform", function(d, i) { return "translate("+t8+", 0) rotate(-90 " + (i * rect_space + 6).toString()  + " -4)"; });


    }

    function click(d) {
      if (d.children) {
        d._children = d.children;
        d.children = null;
      } else {
        d.children = d._children;
        d._children = null;
      }
      update(d);
    }

    function color(d) {
      // if(d._children.length == 0 ){
      //   return "#fd8d3c";
      // }
      //console.log(d.name + ":" +d._children.length)
      t1 = d._children ? d._children.length : 0;
      return d._children ? (t1 ? "#3182bd" : "#fd8d3c") : d.children ? "#c6dbef" : "#fd8d3c";
    }

    function get_scales(nodes) {
        //generates color scales for all the different skills
        skill_values_combined = {};
        nodes.forEach(function(node, idx) {
           skill_values = node["data"][3];
           for (var skill_info in skill_values) {
               if(idx === 0) {
                   continue
               }
               if(idx === 1) {
                   skill_values_combined[skill_info] = [skill_values[skill_info]];
               } else {
                   skill_values_combined[skill_info].push(skill_values[skill_info]);
               }
           }
        });
        skill_scales = {};
        for (var skill_code in skill_values_combined) {
            var brew = new classyBrew();
            brew.setSeries(skill_values_combined[skill_code]);
            brew.setNumClasses(5);
            brew.setColorCode("BuGn");
            brew.classify('jenks');
            skill_scales[skill_code] = brew;
            // console.log(brew.getBreaks());
        }
        return skill_scales;
    }

}

// Toggle children on click.
