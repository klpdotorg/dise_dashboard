// Global variable for the map.
var map;
// Central location, Bangalore
var bangalore = L.latLng([12.9719,77.5937]);
// FIXME: Set Bounds for the map
var bounds;

// Initialise the map object.
map = L.map('map-holder', {zoomControl: true, attributionControl: false}).setView(bangalore, 9);

// Tile URL, Key and attribution.
var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/{key}/997/256/{z}/{x}/{y}.png',
cloudmadeKey = '3c4ab920016a46d8ba10c88227539774',
cloudmadeAttribution = '<a href="http://osm.org">OpenStreetMap</a>, <a href="http://cloudmade.com">CloudMade</a>';

// Create the Tile layer and add it to the map.
var cloudmadeLayer = L.tileLayer(cloudmadeUrl, {key: cloudmadeKey}).addTo(map);

// Custom attribution control.
var attributionControl = L.control.attribution({position: 'bottomright', prefix: cloudmadeAttribution}).addTo(map);

// Custom school icon.
var schoolIcon = L.icon({
  iconUrl: 'https://f.cloud.github.com/assets/9491/1809460/c7971e88-6de8-11e3-9d4e-077d00736010.png',
  iconSize: [35, 40],
  iconAnchor: [10, 40],
  popupAnchor: [8, -35]
});
