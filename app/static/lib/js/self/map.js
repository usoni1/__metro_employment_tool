$(document).ready(
    function () {
        console.log('server here!');

        mymap1 = L.map('map1')
            .setView([33.5, -111.98], 10);

        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            maxZoom: 18,
            id: 'mapbox.light',
            accessToken: 'pk.eyJ1IjoidXNvbmkxIiwiYSI6ImNqOGFvMmxiaTA1cnAyd255bDM5dnUybm8ifQ.dFxAGXFEJk6YMUoVrcPugQ'
        }).addTo(mymap1);

        mymap2 = L.map('map2')
            .setView([37.0902, -95.7129], 4);

        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            maxZoom: 18,
            id: 'mapbox.light',
            accessToken: 'pk.eyJ1IjoidXNvbmkxIiwiYSI6ImNqOGFvMmxiaTA1cnAyd255bDM5dnUybm8ifQ.dFxAGXFEJk6YMUoVrcPugQ'
        }).addTo(mymap2);

        $('#menu_tab a').click(function (e) {
          e.preventDefault();
          $(this).tab('show');
          mymap1.invalidateSize();
          mymap2.invalidateSize();
        });

        info = L.control();

        info.onAdd = function (map) {
            this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
            this.update();
            return this._div;
        };

        // method that we will use to update the control based on feature properties passed
        info.update = function (props) {
            this._div.innerHTML = '<h4>Display value</h4>' +  (props ?
                '<b>' + props.ZCTA_ID + '</b><br />' + props.display
                : 'Hover over a state');
        };


        info1 = L.control();

        info1.onAdd = function (map) {
            this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
            this.update();
            return this._div;
        };

        // method that we will use to update the control based on feature properties passed
        info1.update = function (props) {
            this._div.innerHTML = '<h4>US Population Density</h4>' +  (props ?
                '<b>' + props.GEOID + '</b><br />' + props.display
                : 'Hover over a state');
        };



        az_map_layer = L.geoJson(az_map).addTo(mymap1);
        us_map_layer = L.geoJson(metro_data).addTo(mymap2);

        info.addTo(mymap1);
        info1.addTo(mymap2);

        // lasso = L.lasso(mymap1);
        // lasso.enable();
        // mymap1.on('lasso.finished', (event) => {
        //     console.log(event.layers);
        // });

    }
);

function enable_lasso_select() {
    selectfeature1 = mymap1.selectAreaFeature.enable();
    selectfeature2 = mymap2.selectAreaFeature.enable();
}

function get_data() {
    var selected_features1 = selectfeature1.getFeaturesSelected( 'polygon' );
    var aggregation_type = $("input[name='aggregation_type']:checked").val();
    var skill_selected = $('#skill_list_loss option:selected').text().split(' : ')[0];
    var arr = [];
    var type = 0;
    if(selected_features1 != null) {
        selected_features1.forEach(function (f) {
            var prop = f.feature.properties;
            var zcta_id = prop.ZCTA_ID;
            arr.push(zcta_id);
            type = "ZCTA";
        });
    }

    var selected_features2 = selectfeature2.getFeaturesSelected( 'polygon' );
    if(selected_features2 != null) {
            selected_features2.forEach(function (f) {
            var prop = f.feature.properties;
            var geo_id = prop.GEOID;
            arr.push(geo_id);
            type = "MSA";
        });
    }

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200) {
            $("#here_data").html("Required info:" + this.responseText);
        }
    };
    xhr.open('GET', '/get_agg?type='+type+'&aggregation_type='+aggregation_type+'&skill_selected='+skill_selected+'&list='+arr);
    xhr.send();
}

function disable_lasso_select() {
    selectfeature1.removeLastArea();
    selectfeature2.removeLastArea();
}