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
           weight : 5,
           color : '#666',
           dashArray : '',
           fillOpacity : 0.7
        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
    }

    function resetHighLight(e) {
        central_map_layer.resetStyle(e.target);
        $('#map_tooltip')
            .css('display', 'none');
    }

    function onEachFeature(feature, layer) {
        layer.on({
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
           weight : 5,
           color : '#666',
           dashArray : '',
           fillOpacity : 0.7
        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
    }

    function resetHighLight(e) {
        central_map_layer.resetStyle(e.target);
        $('#map_tooltip')
            .css('display', 'none');
    }

    function onEachFeature(feature, layer) {
        layer.on({
            click : create_scatter
        });
    }

    us_map_layer = L.geoJson(metro_data, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(mymap2);
}

function create_scatter() {
    $("#map1").css("height", "25vh");
    $("#map2").css("height", "25vh");
    mymap1.invalidateSize(true);
    mymap2.invalidateSize(true);
    $(".analysis_space").css("visibility", "visible");
    generate_scatter_plot1();
}