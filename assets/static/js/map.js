// Global variable for the map.
var map;
// Central location, Bangalore
var karnataka = L.latLng([15.040,76.223]);
var bangalore = L.latLng([12.979,77.590]);

// FIXME: Set Bounds for the map
var bounds;

// Layers for each entities.
var districtLayer, blockLayer, clusterLayer, schoolLayer;
// Structure to hold auto-assigned layer IDs
var layerIDs = {'district': '', 'block': '', 'cluster': '',
              'school': ''};
// Initialise the map object.
map = L.map('map-holder', {zoomControl: true, attributionControl: false}).setView(karnataka, 8);

// Tile URL, Key and attribution.
var mapQuestUrl = 'http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.jpg',
    mapQuestSubdomains = '1234',
    mapQuestAttribution = 'Imagery and map information provided by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.';

// Create the Tile layer and add it to the map.
var cloudmadeLayer = L.tileLayer(mapQuestUrl, {
    subdomains: mapQuestSubdomains
}).addTo(map);

// Custom attribution control.
var attributionControl = L.control.attribution({position: 'bottomright', prefix: mapQuestAttribution}).addTo(map);

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
