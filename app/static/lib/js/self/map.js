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

        az_map_layer = L.geoJson(az_map).addTo(mymap1);
        us_map_layer = L.geoJson(metro_data).addTo(mymap2);

    }
);
