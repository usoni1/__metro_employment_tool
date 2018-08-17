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

    }
);
