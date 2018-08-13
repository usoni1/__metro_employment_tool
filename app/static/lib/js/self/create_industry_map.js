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

    function nec() {
                var t7 = {
                  "2.B.5.d": 2.29,
                  "2.B.4.e": 2.87,
                  "2.B.2.i": 2.77,
                  "2.B.4.g": 2.26,
                  "2.B.5.c": 1.9,
                  "2.B.4.h": 2.13,
                  "2.B.3.b": 1.44,
                  "2.B.3.c": 1.75,
                  "2.B.3.a": 1.69,
                  "2.B.5.a": 2.96,
                  "2.B.3.g": 2.56,
                  "2.B.3.d": 1.23,
                  "2.B.3.e": 1.27,
                  "2.B.3.j": 1.88,
                  "2.B.3.k": 2.04,
                  "2.B.3.h": 2.47,
                  "2.B.3.l": 1.82,
                  "2.B.3.m": 2.29,
                  "2.B.5.b": 1.78,
                  "2.B.1.a": 2.84,
                  "2.B.1.b": 2.93,
                  "2.B.1.c": 2.4,
                  "2.B.1.d": 2.3,
                  "2.B.1.e": 2.36,
                  "2.B.1.f": 2.67,
                  "2.A.1.c": 2.75,
                  "2.A.1.b": 3.17,
                  "2.A.1.a": 2.97,
                  "2.A.1.f": 1.5,
                  "2.A.1.e": 2.18,
                  "2.A.1.d": 3.17,
                  "2.A.2.d": 3.07,
                  "2.A.2.a": 3.09,
                  "2.A.2.b": 2.65,
                  "2.A.2.c": 2.33
        };

        var skill_scales = [
             {
                  "skill" : "2.A.1.a",
                  "element_name" : "Reading Comprehension",
                  "scale_id" : "IM",
                  "min_intensity" : 3.0862809618513833,
                  "max_intensity" : 3.457424493859939
             },
             {
                  "skill" : "2.A.1.a",
                  "element_name" : "Reading Comprehension",
                  "scale_id" : "LV",
                  "min_intensity" : 3.0418823020337507,
                  "max_intensity" : 3.601091934948556
             },
             {
                  "skill" : "2.A.1.b",
                  "element_name" : "Active Listening",
                  "scale_id" : "IM",
                  "min_intensity" : 3.3666234786022775,
                  "max_intensity" : 3.666479435365289
             },
             {
                  "skill" : "2.A.1.b",
                  "element_name" : "Active Listening",
                  "scale_id" : "LV",
                  "min_intensity" : 3.0935885355319988,
                  "max_intensity" : 3.5271086647727263
             },
             {
                  "skill" : "2.A.1.c",
                  "element_name" : "Writing",
                  "scale_id" : "IM",
                  "min_intensity" : 2.771486168866389,
                  "max_intensity" : 3.138921340856289
             },
             {
                  "skill" : "2.A.1.c",
                  "element_name" : "Writing",
                  "scale_id" : "LV",
                  "min_intensity" : 2.708364344439637,
                  "max_intensity" : 3.2568934616661136
             },
             {
                  "skill" : "2.A.1.d",
                  "element_name" : "Speaking",
                  "scale_id" : "IM",
                  "min_intensity" : 3.3178720062819003,
                  "max_intensity" : 3.6083455866907546
             },
             {
                  "skill" : "2.A.1.d",
                  "element_name" : "Speaking",
                  "scale_id" : "LV",
                  "min_intensity" : 2.977860227718884,
                  "max_intensity" : 3.4491282611435534
             },
             {
                  "skill" : "2.A.1.e",
                  "element_name" : "Mathematics",
                  "scale_id" : "LV",
                  "min_intensity" : 1.9502278069065264,
                  "max_intensity" : 2.6090242283438427
             },
             {
                  "skill" : "2.A.1.e",
                  "element_name" : "Mathematics",
                  "scale_id" : "IM",
                  "min_intensity" : 2.300755740372446,
                  "max_intensity" : 2.6545204115499508
             },
             {
                  "skill" : "2.A.1.f",
                  "element_name" : "Science",
                  "scale_id" : "IM",
                  "min_intensity" : 1.3354765553171928,
                  "max_intensity" : 1.8181480252240299
             },
             {
                  "skill" : "2.A.1.f",
                  "element_name" : "Science",
                  "scale_id" : "LV",
                  "min_intensity" : 0.4484528716680407,
                  "max_intensity" : 1.2873050116163294
             },
             {
                  "skill" : "2.A.2.a",
                  "element_name" : "Critical Thinking",
                  "scale_id" : "IM",
                  "min_intensity" : 3.13605365642579,
                  "max_intensity" : 3.468589445735148
             },
             {
                  "skill" : "2.A.2.a",
                  "element_name" : "Critical Thinking",
                  "scale_id" : "LV",
                  "min_intensity" : 3.074608394634358,
                  "max_intensity" : 3.5560769996681056
             },
             {
                  "skill" : "2.A.2.b",
                  "element_name" : "Active Learning",
                  "scale_id" : "IM",
                  "min_intensity" : 2.6952610914801727,
                  "max_intensity" : 3.034653194975423
             },
             {
                  "skill" : "2.A.2.b",
                  "element_name" : "Active Learning",
                  "scale_id" : "LV",
                  "min_intensity" : 2.5869375736160194,
                  "max_intensity" : 3.1119946896780624
             },
             {
                  "skill" : "2.A.2.c",
                  "element_name" : "Learning Strategies",
                  "scale_id" : "IM",
                  "min_intensity" : 2.4618531605810756,
                  "max_intensity" : 2.7731977401129955
             },
             {
                  "skill" : "2.A.2.c",
                  "element_name" : "Learning Strategies",
                  "scale_id" : "LV",
                  "min_intensity" : 2.4141403001265593,
                  "max_intensity" : 2.87199344620426
             },
             {
                  "skill" : "2.A.2.d",
                  "element_name" : "Monitoring",
                  "scale_id" : "IM",
                  "min_intensity" : 3.125378774181884,
                  "max_intensity" : 3.2769567246004887
             },
             {
                  "skill" : "2.A.2.d",
                  "element_name" : "Monitoring",
                  "scale_id" : "LV",
                  "min_intensity" : 2.9620284135753754,
                  "max_intensity" : 3.322804513773648
             },
             {
                  "skill" : "2.B.1.a",
                  "element_name" : "Social Perceptiveness",
                  "scale_id" : "IM",
                  "min_intensity" : 3.0352787593246964,
                  "max_intensity" : 3.36138018018018
             },
             {
                  "skill" : "2.B.1.a",
                  "element_name" : "Social Perceptiveness",
                  "scale_id" : "LV",
                  "min_intensity" : 2.7292520612485274,
                  "max_intensity" : 3.1766394494342687
             },
             {
                  "skill" : "2.B.1.b",
                  "element_name" : "Coordination",
                  "scale_id" : "LV",
                  "min_intensity" : 2.922138910812944,
                  "max_intensity" : 3.186976435446399
             },
             {
                  "skill" : "2.B.1.b",
                  "element_name" : "Coordination",
                  "scale_id" : "IM",
                  "min_intensity" : 3.0709206910090314,
                  "max_intensity" : 3.244235062376887
             },
             {
                  "skill" : "2.B.1.c",
                  "element_name" : "Persuasion",
                  "scale_id" : "IM",
                  "min_intensity" : 2.5863427561837455,
                  "max_intensity" : 2.912405539772728
             },
             {
                  "skill" : "2.B.1.c",
                  "element_name" : "Persuasion",
                  "scale_id" : "LV",
                  "min_intensity" : 2.4504416961130744,
                  "max_intensity" : 2.9121988636363634
             },
             {
                  "skill" : "2.B.1.d",
                  "element_name" : "Negotiation",
                  "scale_id" : "LV",
                  "min_intensity" : 2.268138728323699,
                  "max_intensity" : 2.7027848011363624
             },
             {
                  "skill" : "2.B.1.d",
                  "element_name" : "Negotiation",
                  "scale_id" : "IM",
                  "min_intensity" : 2.4505054509415256,
                  "max_intensity" : 2.7683643465909107
             },
             {
                  "skill" : "2.B.1.e",
                  "element_name" : "Instructing",
                  "scale_id" : "IM",
                  "min_intensity" : 2.565514330585002,
                  "max_intensity" : 2.9272316384180797
             },
             {
                  "skill" : "2.B.1.e",
                  "element_name" : "Instructing",
                  "scale_id" : "LV",
                  "min_intensity" : 2.500788056779245,
                  "max_intensity" : 2.9398916103012205
             },
             {
                  "skill" : "2.B.1.f",
                  "element_name" : "Service Orientation",
                  "scale_id" : "IM",
                  "min_intensity" : 2.768213082259664,
                  "max_intensity" : 3.339499099099099
             },
             {
                  "skill" : "2.B.1.f",
                  "element_name" : "Service Orientation",
                  "scale_id" : "LV",
                  "min_intensity" : 2.5908394449950443,
                  "max_intensity" : 3.1587387387387382
             },
             {
                  "skill" : "2.B.2.i",
                  "element_name" : "Complex Problem Solving",
                  "scale_id" : "IM",
                  "min_intensity" : 2.7548930772018854,
                  "max_intensity" : 3.14554928642549
             },
             {
                  "skill" : "2.B.2.i",
                  "element_name" : "Complex Problem Solving",
                  "scale_id" : "LV",
                  "min_intensity" : 2.579839863713799,
                  "max_intensity" : 3.1491669432459326
             },
             {
                  "skill" : "2.B.3.a",
                  "element_name" : "Operations Analysis",
                  "scale_id" : "IM",
                  "min_intensity" : 1.566465136804942,
                  "max_intensity" : 2.1995784931961495
             },
             {
                  "skill" : "2.B.3.a",
                  "element_name" : "Operations Analysis",
                  "scale_id" : "LV",
                  "min_intensity" : 0.8789691085613418,
                  "max_intensity" : 1.968586126783937
             },
             {
                  "skill" : "2.B.3.b",
                  "element_name" : "Technology Design",
                  "scale_id" : "IM",
                  "min_intensity" : 1.389068666140489,
                  "max_intensity" : 1.7707002987056084
             },
             {
                  "skill" : "2.B.3.b",
                  "element_name" : "Technology Design",
                  "scale_id" : "LV",
                  "min_intensity" : 0.4977505919494871,
                  "max_intensity" : 1.126110189180219
             },
             {
                  "skill" : "2.B.3.c",
                  "element_name" : "Equipment Selection",
                  "scale_id" : "IM",
                  "min_intensity" : 1.3232210109018827,
                  "max_intensity" : 1.7285797632938824
             },
             {
                  "skill" : "2.B.3.c",
                  "element_name" : "Equipment Selection",
                  "scale_id" : "LV",
                  "min_intensity" : 0.4854011299435028,
                  "max_intensity" : 1.0716234786022771
             },
             {
                  "skill" : "2.B.3.d",
                  "element_name" : "Installation",
                  "scale_id" : "LV",
                  "min_intensity" : 0.09226331360946746,
                  "max_intensity" : 0.4802083680613436
             },
             {
                  "skill" : "2.B.3.d",
                  "element_name" : "Installation",
                  "scale_id" : "IM",
                  "min_intensity" : 1.0562426035502959,
                  "max_intensity" : 1.3070078346391067
             },
             {
                  "skill" : "2.B.3.e",
                  "element_name" : "Programming",
                  "scale_id" : "IM",
                  "min_intensity" : 1.2988817299205642,
                  "max_intensity" : 1.748702480208614
             },
             {
                  "skill" : "2.B.3.e",
                  "element_name" : "Programming",
                  "scale_id" : "LV",
                  "min_intensity" : 0.36521800529567516,
                  "max_intensity" : 1.0819886104517225
             },
             {
                  "skill" : "2.B.3.g",
                  "element_name" : "Operation Monitoring",
                  "scale_id" : "IM",
                  "min_intensity" : 2.1371345826235095,
                  "max_intensity" : 2.671505692972125
             },
             {
                  "skill" : "2.B.3.g",
                  "element_name" : "Operation Monitoring",
                  "scale_id" : "LV",
                  "min_intensity" : 1.7165689948892673,
                  "max_intensity" : 2.3860738123282292
             },
             {
                  "skill" : "2.B.3.h",
                  "element_name" : "Operation and Control",
                  "scale_id" : "IM",
                  "min_intensity" : 1.7708325074331022,
                  "max_intensity" : 2.404301138594425
             },
             {
                  "skill" : "2.B.3.h",
                  "element_name" : "Operation and Control",
                  "scale_id" : "LV",
                  "min_intensity" : 1.2408622398414273,
                  "max_intensity" : 2.0824558303886924
             },
             {
                  "skill" : "2.B.3.j",
                  "element_name" : "Equipment Maintenance",
                  "scale_id" : "IM",
                  "min_intensity" : 1.2557035647279549,
                  "max_intensity" : 1.852235963879073
             },
             {
                  "skill" : "2.B.3.j",
                  "element_name" : "Equipment Maintenance",
                  "scale_id" : "LV",
                  "min_intensity" : 0.40275171982489055,
                  "max_intensity" : 1.3000392618767174
             },
             {
                  "skill" : "2.B.3.k",
                  "element_name" : "Troubleshooting",
                  "scale_id" : "IM",
                  "min_intensity" : 1.6032457786116323,
                  "max_intensity" : 2.081075775422065
             },
             {
                  "skill" : "2.B.3.k",
                  "element_name" : "Troubleshooting",
                  "scale_id" : "LV",
                  "min_intensity" : 0.9197123202001253,
                  "max_intensity" : 1.6186866902237929
             },
             {
                  "skill" : "2.B.3.l",
                  "element_name" : "Repairing",
                  "scale_id" : "IM",
                  "min_intensity" : 1.227560975609756,
                  "max_intensity" : 1.7829681978798588
             },
             {
                  "skill" : "2.B.3.l",
                  "element_name" : "Repairing",
                  "scale_id" : "LV",
                  "min_intensity" : 0.34575984990619135,
                  "max_intensity" : 1.1893776992540244
             },
             {
                  "skill" : "2.B.3.m",
                  "element_name" : "Quality Control Analysis",
                  "scale_id" : "LV",
                  "min_intensity" : 1.5459931856899491,
                  "max_intensity" : 2.209778034015567
             },
             {
                  "skill" : "2.B.3.m",
                  "element_name" : "Quality Control Analysis",
                  "scale_id" : "IM",
                  "min_intensity" : 2.0131959114139693,
                  "max_intensity" : 2.472423191278494
             },
             {
                  "skill" : "2.B.4.e",
                  "element_name" : "Judgment and Decision Making",
                  "scale_id" : "IM",
                  "min_intensity" : 2.9364762249141214,
                  "max_intensity" : 3.2096017258546303
             },
             {
                  "skill" : "2.B.4.e",
                  "element_name" : "Judgment and Decision Making",
                  "scale_id" : "LV",
                  "min_intensity" : 2.668520121159671,
                  "max_intensity" : 3.1388018586126774
             },
             {
                  "skill" : "2.B.4.g",
                  "element_name" : "Systems Analysis",
                  "scale_id" : "LV",
                  "min_intensity" : 1.9773833049403755,
                  "max_intensity" : 2.670106206438765
             },
             {
                  "skill" : "2.B.4.g",
                  "element_name" : "Systems Analysis",
                  "scale_id" : "IM",
                  "min_intensity" : 2.240575707611982,
                  "max_intensity" : 2.720481247925655
             },
             {
                  "skill" : "2.B.4.h",
                  "element_name" : "Systems Evaluation",
                  "scale_id" : "IM",
                  "min_intensity" : 2.209649781113195,
                  "max_intensity" : 2.6706604712910726
             },
             {
                  "skill" : "2.B.4.h",
                  "element_name" : "Systems Evaluation",
                  "scale_id" : "LV",
                  "min_intensity" : 1.9775897879705762,
                  "max_intensity" : 2.687079322933953
             },
             {
                  "skill" : "2.B.5.a",
                  "element_name" : "Time Management",
                  "scale_id" : "IM",
                  "min_intensity" : 2.9654951830443155,
                  "max_intensity" : 3.148749639873236
             },
             {
                  "skill" : "2.B.5.a",
                  "element_name" : "Time Management",
                  "scale_id" : "LV",
                  "min_intensity" : 2.74302119460501,
                  "max_intensity" : 3.049920454545455
             },
             {
                  "skill" : "2.B.5.b",
                  "element_name" : "Management of Financial Resources",
                  "scale_id" : "IM",
                  "min_intensity" : 1.654150054367525,
                  "max_intensity" : 1.9171025555924324
             },
             {
                  "skill" : "2.B.5.b",
                  "element_name" : "Management of Financial Resources",
                  "scale_id" : "LV",
                  "min_intensity" : 0.9825127978817301,
                  "max_intensity" : 1.482960504480585
             },
             {
                  "skill" : "2.B.5.c",
                  "element_name" : "Management of Material Resources",
                  "scale_id" : "IM",
                  "min_intensity" : 1.7839035882566145,
                  "max_intensity" : 2.036080318619316
             },
             {
                  "skill" : "2.B.5.c",
                  "element_name" : "Management of Material Resources",
                  "scale_id" : "LV",
                  "min_intensity" : 1.1196230518303736,
                  "max_intensity" : 1.597537338201129
             },
             {
                  "skill" : "2.B.5.d",
                  "element_name" : "Management of Personnel Resources",
                  "scale_id" : "IM",
                  "min_intensity" : 2.437181918109371,
                  "max_intensity" : 2.6600838068181822
             },
             {
                  "skill" : "2.B.5.d",
                  "element_name" : "Management of Personnel Resources",
                  "scale_id" : "LV",
                  "min_intensity" : 2.2930324264907944,
                  "max_intensity" : 2.6402489213408558
             }
        ];


        skill_list_real = [];
        for (var key in t7)
        {
             for(var i = 0; i < skill_scales.length; i ++) {
                  if(key == skill_scales[i]["skill"])
                  {
                       skill_list_real.push(skill_scales[i]["element_name"]);
                       break;
                  }
             }
        }
    }

    function update(source) {
            // Compute the flattened node list. TODO use d3.layout.hierarchy
        nec();
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



          var skill_labels1 = svg.selectAll(".skill_labels")
                  .data(skill_list_real)
                  .enter().append("text")
                    .attr("class", "skill_labels")
                    .on("click", function(d, i) {
                        var x = i * rect_space + t9;
                        var y1 = 0;
                        var y2 = y1 + height;
                        d3.selectAll(".temp_line1").remove();
                        svg.append("line").attr("class","temp_line1").attr("x1",x).attr("y1",y1).attr("x2",x).attr("y2",y2).attr("stroke-width",2).attr("stroke", "black");
                        svg.append("line").attr("class","temp_line1").attr("x1",x+rect_width +3).attr("y1",y1).attr("x2",x+rect_width+3).attr("y2",y2).attr("stroke-width",2).attr("stroke", "black");

                    })
                    .text(function(d) { return d; })
                    .attr("x", function(d, i) { return i * rect_space; })
                    .attr("y", 0)
                    .style("text-anchor", "start")
                    .attr("transform", function(d, i) { return "translate("+t8+", 0) rotate(-90 " + (i * rect_space + 6).toString()  + " -4)"; });


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
