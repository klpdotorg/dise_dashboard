// Module to call DISE OLAP API
// ============================

// Initialize like this -

//     var DISE = $.DiseAPI({
//         'base_url': window.location.toString() + 'api/v1/olap/'
//     })

// Then make calls like -

//     DISE.call('Cluster.getSchools', '10-11', {
//         name: e.added.id,
//         format: 'geo'
//     }, function(data) {
//         plotOnMap(data.schools, 8);
//     });

;(function($){
    $.extend({
        DiseAPI: function(options) {
            this.defaultOptions = {};

            // Take config options. `base_url` is mandatory
            var settings = $.extend({}, this.defaultOptions, options);

            this.call = function(method, session, params, success) {
                // @param {String}   method      Method name in the form of Entity.function
                // @param {String}   session     Session in the form of YY-YY e.g. 10-11 for 2010-2011
                // @param {object}   params      Required GET parameters e.g. name, code
                // @param {function} success     What to do with the return data? same as `success` for jQuery.getJSON()
                var result;
                base_params = {
                    'method': method,
                    'session': session,
                }
                params = $.extend({}, base_params, params);

                $.getJSON(
                    settings.base_url,
                    params,
                    success
                )
                return result;
            }

            return this;
        }
    });
})(jQuery);

$(function(){

    UI.init(); // Initialize UI elements
    filtersEnabled = false;

    $("#filter-select").select2({
        dropdownCssClass: "bigdrop",
        allowClear: true,
        minimumInputLength: 3,
        ajax: {
            url: "/api/v1/olap/search/",
            quietMillis: 300,
            data: function (term, page) {
                var values = {};
                $.each($('form[name=basic_filters]').serializeArray(), function(i, field) {
                    values[field.name] = field.value;
                });
                return {
                    q: term, // search term
                    filters: values
                };
            },
            results: function (data, page) {
                return {results: data};
            }
        }
        // data:
        // [
        //     {
        //         text: "District",
        //         children: [
        //             {
        //                 id: "d1",
        //                 text: "Bellary"
        //             },
        //             {
        //                 id: "d2",
        //                 text: "Koppal"
        //             }
        //         ]
        //     },
        //     {
        //         text: "Taluk",
        //         children: [
        //             {
        //                 id: "t1",
        //                 text: "Hospet"
        //             }
        //         ]
        //     }
        // ]
    });

    function onEachFeature(feature, layer) {
        // does this feature have a property named popupContent?
        if (feature.properties && feature.properties.popupContent) {
            layer.bindPopup(feature.properties.popupContent);
        }
    }

    function createLayer(feature_or_features, icon) {
        // @param {String} feature_or_features  Either Feature or FeatureCollection
        // @param {String} zoom                 Zoom level of the map
        // console.log(feature_or_features);
        return L.geoJson(
            feature_or_features,
            {
                pointToLayer: function (feature, latlng) {
                    // window.map.setView(latlng, zoom);
                    if (icon != undefined) {
                        return L.marker(latlng, {icon: icon});
                    }
                    else {
                        return L.marker(latlng);
                    }
                },
                onEachFeature: onEachFeature
            }
        );
    }

    // Initialize the API wrapper
    var DISE = $.DiseAPI({
        'base_url': window.location.toString() + 'api/v1/olap/'
    })

    function loadEntityData (entity) {
      bbox = map.getBounds().toBBoxString();
      // Clear current layers.
      currentLayers.clearLayers();
      DISE.call(entity+'.search', '10-11', {
          bbox: bbox,
      }, function(data) {
          if (entity=='Block') {
            blockLayer = createLayer(data.blocks, blockIcon);
            layerIDs.block = blockLayer._leaflet_id;
            blockLayer.addTo(currentLayers);
          }
          else if (entity=='Cluster') {
            clusterLayer = createLayer(data.clusters, clusterIcon);
            layerIDs.cluster = clusterLayer._leaflet_id;
            clusterLayer.addTo(currentLayers);
          }
          else if (entity=='District') {
            districtLayer = createLayer(data.districts, districtIcon);
            layerIDs.district = districtLayer._leaflet_id;
            districtLayer.addTo(currentLayers);
          }
          else {
            schoolLayer = createLayer(data.schools, schoolIcon);
            schoolLayer._leaflet_id = layerIDs.school;
            schoolLayer.addTo(currentLayers);
          }

      });
    }

    function mapInit () {
        // Load the district data and plot.
        bbox = map.getBounds().toBBoxString();
        DISE.call('District.search', '10-11', {
            bbox: bbox,
        }, function(data) {
            districtLayer = createLayer(data.districts, districtIcon);
            layerIDs.district = districtLayer._leaflet_id;
            districtLayer.addTo(currentLayers);
        });
    }
    // Invoke initial map layers.
    mapInit();

    function updateLayers (zoom) {
        if (zoom <=8) {
          // Load districts.
          mapInit();
        }
        else if (zoom == 9) {
          // Load blocks.
          loadEntityData('Block');
        }
        else if (zoom > 9 && zoom < 12) {
          // Load clusters.
          loadEntityData('Cluster');
        }
        else {
          // Load schools.
          loadEntityData('School');
        }
    }


    function updateData (layer) {
      layerID = layer._leaflet_id;
      if (layerID == layerIDs.district) {
        loadEntityData('District');
      }
      else if (layerID == layerIDs.block) {
        loadEntityData('Block');
      }
      else if (layerID == layerIDs.cluster) {
        loadEntityData('Cluster');
      }
      else {
        loadEntityData('School');
      }
    }

// When the map is zoomed, load the necessary data
    map.on('zoomend', function(e) {
      // If filters are enabled then don't load the usual layers.
      if (!filtersEnabled) {
        updateLayers(map.getZoom());
      }
    })

// When the map is panned, load the data in the new bounds.
    map.on('dragend', function(e) {
      if (!filtersEnabled) {
        currentLayers.eachLayer(function(layer) {
          updateData(layer);
        });
      }
    })

    $("#filter-select").on("change", function(e) {
        // Clear the preloaded layers when the search has been used
        currentLayers.clearLayers();
        // Flip the filter switch to disable all usual map interactions.
        filtersEnabled = true;
        if (e.added.type == 'school') {
            if(e.added.feature !== null && e.added.feature !== "{}"){
                newLayer = createLayer(JSON.parse(e.added.feature), schoolIcon);
                newLayer.addTo(currentLayers);
            } else {
                alert("Sorry, this school doesn't have a location.");
            }
        } else if (e.added.type == 'cluster'){
            DISE.call('Cluster.getSchools', '10-11', {
                name: e.added.id,
                format: 'geo'
            }, function(data) {
                newLayer = createLayer(data.schools, schoolIcon);
                newLayer.addTo(currentLayers);
            });
        } else {
            // do nothing
        }
    });
});
