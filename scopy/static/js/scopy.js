function makeSlideMap() {


    // Get the original image for setting the
    // width and height for Raster Coordinates:
    var img = new Image();

    // This will hold the marker data
    // on click and remove, for saving to DB:
    var markerData = {};

    // Asynchronous loading of image, wait for it
    // to be loaded first, then use the dimensions
    // to generate the raster coordinate tiles:
    img.onload = function(){

        var minZoom = 1;
        var maxZoom = 4;

        // create the map
        var map = L.map('llmap', {
            minZoom: minZoom,
            maxZoom: maxZoom
        });

        var dim = [img.height, img.width];

        // assign map and image dimensions
        var rc = new L.RasterCoords(map, dim);

        console.log(dim);

        // All coordinates need to be un-projected using the `unproject` method:
        map.setView(rc.unproject([dim[0]/2, dim[1]/2]), 3);

        // Set markers on click events in the map:
        map.on('click', function (event) {
            // Any position in leaflet needs to be projected
            // to obtain the image coordinates:
            var coords = rc.project(event.latlng);
            var markerID = uuid();
            var marker = L.marker(rc.unproject(coords), {'markerID': markerID}).addTo(map);

            markerData[markerID] = marker;

            console.log("Pushed to", markerData);
            // Remove markers:
            marker.on('click', function(){
                delete markerData[markerID];
                marker.remove();
                console.log("Popped", markerData);
          })
        });

        // Maximum bounds for slide tiles:
        var bottomLeft = rc.unproject([dim[0], 0]);
        var topRight = rc.unproject([0, dim[1]]);
        var bounds = new L.LatLngBounds(bottomLeft, topRight);

        // Tile layer containing the image generated with
        // `gdal2tiles --leaflet -p raster -w none <img> tiles`
        L.tileLayer('/static/assets/tiles/{z}/{x}/{y}.png', {
            noWrap: true,
            bounds: bounds
        }).addTo(map);

    };

    // Pour in the image:
    img.src = '/static/assets/Image_4923.jpg';

}

$(function() {
    makeSlideMap();
});
