// Global variable for the map.
var map;
// Central location, Bangalore
var karnataka = L.latLng([15.040,76.223]);
var bangalore = L.latLng([12.979,77.590]);
// FIXME: Set Bounds for the map
var bounds;

// Initialise the map object.
map = L.map('map-holder', {zoomControl: true, attributionControl: false}).setView(karnataka, 8);

// Tile URL, Key and attribution.
var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/{key}/997/256/{z}/{x}/{y}.png',
cloudmadeKey = '3c4ab920016a46d8ba10c88227539774',
cloudmadeAttribution = '<a href="http://osm.org">OpenStreetMap</a>, <a href="http://cloudmade.com">CloudMade</a>';

// Create the Tile layer and add it to the map.
var cloudmadeLayer = L.tileLayer(cloudmadeUrl, {key: cloudmadeKey}).addTo(map);

// Custom attribution control.
var attributionControl = L.control.attribution({position: 'bottomright', prefix: cloudmadeAttribution}).addTo(map);

// Group of layers that are on the map at any given
// time.
var currentLayers = L.layerGroup().addTo(map);

// Custom icons.
function customIcon (entity) {
  return L.icon({
  iconUrl: 'static/img/'+entity+'.png',
  iconSize: [25, 30],
  iconAnchor: [10, 40],
  popupAnchor: [4, -35]
 });
}

districtIcon = customIcon('district');
blockIcon = customIcon('block');
clusterIcon = customIcon('cluster');
schoolIcon = customIcon('school');



