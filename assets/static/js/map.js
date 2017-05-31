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
var klpMapUrl = 'https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWVnaGFrbHAiLCJhIjoiY2l2YzVsdmRlMDBhdjJ5bGJsejVkY3lweSJ9._HlzNg5ngnMg7psaRm8tTg',
	klpAttribution = '<a href="https://www.mapbox.com/about/maps/" target="_blank">© Mapbox</a> <a href="https://openstreetmap.org/about/" target="_blank">© OpenStreetMap</a> <a class="mapbox-improve-map" href="https://www.mapbox.com/map-feedback/#mapbox.streets/-74.500/40.000/9" target="_blank">Improve this map</a>';

// Create the Tile layer and add it to the map.
var klpLayer = L.tileLayer(klpMapUrl).addTo(map);

// Custom attribution control.
var attributionControl = L.control.attribution({position: 'bottomright', prefix: klpAttribution}).addTo(map);

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
