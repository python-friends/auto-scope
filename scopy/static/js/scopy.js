function makeSlideMap() {


    // Get the original image for setting the
    // width and height for Raster Coordinates:

    var img = new Image();

    // Asynchronous loading of image, wait for it
    // to be loaded first, then use the dimensions
    // to generate the raster coordinate tiles:

    img.onload = function(){

        var minZoom = 1;
        var maxZoom = 4;

        // create the map
        var map = L.map('llmap');

        var dim = [img.height, img.width];

        // assign map and image dimensions
        var rc = new L.RasterCoords(map, dim);

        console.log(dim);

        // // set max zoom Level (might be `x` if gdal2tiles was called with `-z 0-x` option)
        // map.setMaxZoom(rc.zoomLevel());

        // all coordinates need to be unprojected using the `unproject` method
        // set the view in the lower right edge of the image
        map.setView(rc.unproject([dim[0]/2, dim[1]/2]), 3);

        // set markers on click events in the map
        map.on('click', function (event) {
          // any position in leaflet needs to be projected to obtain the image coordinates
          var coords = rc.project(event.latlng);
          var marker = L.marker(rc.unproject(coords))
            .addTo(map);

          marker.on('click', function(){
              marker.remove()
          })
          // marker.bindPopup('[' + Math.floor(coords.x) + ',' + Math.floor(coords.y) + ']')
          //   .openPopup()
        });

        // var bounds = new L.LatLngBounds(test1, test2);
        //
        // var southWest = new L.LatLng(-252, 4);
        // var northEast = new L.LatLng(-5, 254);

        var southWest = rc.unproject([dim[0], 0]);
        var northEast = rc.unproject([0, dim[1]]);

        var bounds = new L.LatLngBounds(southWest, northEast);

        // var bounds = L.latLngBounds(southWest, northEast);

        console.log(southWest, northEast, bounds);

        map.setMaxBounds(bounds);

        // the tile layer containing the image generated with `gdal2tiles --leaflet -p raster -w none <img> tiles`
        L.tileLayer('/static/js/tiles/{z}/{x}/{y}.png', {
            minZoom: minZoom,
            maxZoom: maxZoom,
            noWrap: true
        }).addTo(map);

    };

    // Pour in the image:
    img.src = '/static/js/Image_4923.jpg';


}

$(function() {
    makeSlideMap();
});
