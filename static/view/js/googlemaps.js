function initialize_map() {
    var mapOptions = {
        center: new google.maps.LatLng(56.8, 60.59),
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"),
        mapOptions);
}
