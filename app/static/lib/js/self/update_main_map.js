function update_main_map() {
    update_main_map1();
    update_main_map2();
}

function update_main_map1(brew_map) {
    function style(feature) {

        if(feature.properties.display === -1) {
                return {
                    fillColor: '#ffffff',
                    weight: 2,
                    opacity: 0,
                    color: 'white',
                    fillOpacity: 0
                };
        }
        return {
            fillColor: brew_map.getColorInRange(feature.properties.display),
            weight: 2,
            opacity: 0.6,
            color: 'white',
            fillOpacity: 0.7
        };
    }

	function highlightFeature(e) {
		var layer = e.target;

		layer.setStyle({
			weight: 5,
			color: '#666',
			dashArray: '',
			fillOpacity: 0.7
		});

		if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
			layer.bringToFront();
		}
        info.update(layer.feature.properties);
	}

	function resetHighlight(e) {
		az_map_layer.resetStyle(e.target);
		info.update();
	}


    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
			mouseout: resetHighlight,
            click : create_scatter
        });
    }


    az_map_layer = L.geoJson(az_map, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(mymap1);
}

function update_main_map2(brew_map) {

    function style(feature) {
        if(feature.properties.display === -1) {
                return {
                    fillColor: '#ffffff',
                    weight: 2,
                    opacity: 0,
                    color: 'white',
                    fillOpacity: 0
                };
        }
        return {
            fillColor: brew_map.getColorInRange(feature.properties.display),
            weight: 2,
            opacity: 1,
            color: 'white',
            fillOpacity: 0.7
        };
    }

    function highlightFeature(e) {
		var layer = e.target;

		layer.setStyle({
			weight: 5,
			color: '#666',
			dashArray: '',
			fillOpacity: 0.7
		});

		if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
			layer.bringToFront();
		}
        info1.update(layer.feature.properties);
	}

	function resetHighlight(e) {
		us_map_layer.resetStyle(e.target);
		info1.update();
	}

    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
			mouseout: resetHighlight,
            click : create_scatter
        });
    }

    us_map_layer = L.geoJson(metro_data, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(mymap2);
}


function create_scatter(e) {
    // $("#map1").css("height", "25vh");
    // $("#map2").css("height", "25vh");
    // mymap1.invalidateSize(true);
    // mymap2.invalidateSize(true);
    // $(".analysis_space").css("visibility", "visible");
    var layer = e.target;
    var prop = layer.feature.properties;
    if ("ZCTA_ID" in prop){
        var zcta_id = prop.ZCTA_ID;
            populate_occ_rank_list(zcta_id);
            populate_ind_rank_list(zcta_id);
            populate_skill_rank_list(zcta_id);
    }
    if("GEOID" in prop) {
        var zcta_id = prop.GEOID;
        populate_occ_rank_list_m(zcta_id);
        populate_ind_rank_list_m(zcta_id);
        populate_skill_rank_list_m(zcta_id);
    }

    generate_scatter_plot1();
}

function generate_scatter_plot1() {
    console.log("Generating the scatter plot as per the unit selected");
}