// Module to call DISE OLAP API
// ============================

// Initialize like this -

//     var DISE = $.DiseAPI({
//         'base_url': window.location.toString() + 'api/v1/olap/'
//     })

// Then make calls like -

//     DISE.call('Cluster.getSchools', '10-11', {
//         name: e.object.id,
//         format: 'geo'
//     }, function(data) {
//         plotOnMap(data.schools, 8);
//     });

;(function($){
    String.prototype.toProperCase = function () {
        return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    };

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
    // Initialize the API wrapper
    var DISE = $.DiseAPI({
        'base_url': window.location.protocol + '//' + window.location.host + '/api/v1/olap/'
    });

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
    }).on('select2-clearing', function(e) {
        // When you clear select2 with close button
        filtersEnabled = false;
        currentLayers.clearLayers();
        map.setZoom(8);
    }).on("select2-selecting", function(e) {
        // Clear the preloaded layers when the search has been used
        currentLayers.clearLayers();
        // Flip the filter switch to disable all usual map interactions.
        filtersEnabled = true;
        var academic_year = $('input[name=academic_year]:checked').val();
        if (e.object.type == 'school') {
            if(e.object.feature !== null && e.object.feature !== "{}"){
                school = JSON.parse(e.object.feature);
                SchoolPane.fill(school.properties);
                newLayer = createLayer(school, schoolIcon);
                setLayerView(newLayer, 15);
                newLayer.addTo(currentLayers);
            } else {
                alert("Sorry, this school doesn't have a location.");
            }
        } else if (e.object.type == 'cluster'){
            DISE.call('Cluster.getSchools', academic_year, {
                name: e.object.id,
                include_entity: 'True'
            }, function(data) {
                OtherPane.fill(data.cluster.properties);
                newLayer = createLayer(data.schools, schoolIcon);
                setLayerView(newLayer, 12);
                newLayer.addTo(currentLayers);
            });
        } else if (e.object.type == 'block'){
            DISE.call('Block.getSchools', academic_year, {
                name: e.object.id,
                include_entity: 'True'
            }, function(data) {
                OtherPane.fill(data.block.properties);
                newLayer = createLayer(data.schools, schoolIcon);
                setLayerView(newLayer, 12);
                newLayer.addTo(currentLayers);
            });
        } else if (e.object.type == 'district'){
            DISE.call('District.getSchools', academic_year, {
                name: e.object.id,
                include_entity: 'True'
            }, function(data) {
                OtherPane.fill(data.district.properties);
                newLayer = createLayer(data.schools, schoolIcon);
                setLayerView(newLayer, 12);
                newLayer.addTo(currentLayers);
            });
        } else if (e.object.type == 'pincode'){
            DISE.call('Pincode.getSchools', academic_year, {
                pincode: e.object.id,
                include_entity: 'True'
            }, function(data) {
                OtherPane.fill(data.pincode.properties);
                newLayer = createLayer(data.schools, schoolIcon);
                setLayerView(newLayer, 12);
                newLayer.addTo(currentLayers);
            });
        } else {
            // do nothing
        }
    });

    var SchoolPane = {
        divid: 'popup-school',
        show: function() {
            // shows the school pane
            $('#'+this.divid).show();
        },
        hide: function() {
            // hides the school pane
            $('#'+this.divid).hide();
        },
        fill: function(school) {
            // fills the pane for Schools
            OtherPane.hide();
            this.hide();

            $('#'+this.divid).find('.name').html(school.school_name + ' <small> Estd. ' + school.yeur_estd + '</small>');
            $('#'+this.divid).find('.total_student').html(school.total_boys+school.total_girls);
            $('#'+this.divid).find('.total_tch').html(school.male_tch+school.female_tch);
            $('#'+this.divid).find('.medium_of_instruction').html(school.medium_of_instruction_display);
            $('#'+this.divid).find('.sch_category').html(school.sch_category_display);
            $('#'+this.divid).find('.sch_management').html(school.sch_management_display);
            $('#'+this.divid).find('.electricity').html(school.electricity_display);
            $('#'+this.divid).find('.library_yn').html(school.library_yn_display);
            $('#'+this.divid).find('.books_in_library').html(school.books_in_library);
            $('#'+this.divid).find('.address').html([
                    school.cluster_name, school.block_name,
                    school.district, school.pincode
                ].join(', ').toString().toProperCase());

            this.show();
        }
    }

    var OtherPane = {
        divid: 'popup-cluster',
        show: function() {
            // shows the other entity pane
            $('#'+this.divid).show();
        },
        hide: function() {
            // hides the other entity pane
            $('#'+this.divid).hide();
        },
        fill: function(entity) {
            // fills the pane for other entities
            SchoolPane.hide();
            this.hide();

            console.log('OtherPane.fill called');
            console.log(entity);

            var entity_name = '';
            if(entity.entity_type == 'district') {
                entity_name = 'district';
            }else if (entity.entity_type == 'pincode'){
                entity_name = 'pincode'
            }else{
                entity_name = entity.entity_type + '_name';
            }

            $('#'+this.divid).find('.entity_name').html(entity[entity_name] + ' <small>' + entity.entity_type + '</small>');
            $('#'+this.divid).find('.entity_school').html(entity.sum_schools);
            $('#'+this.divid).find('.entity_student').html(entity.sum_boys+entity.sum_girls);
            $('#'+this.divid).find('.entity_teacher').html(entity.sum_male_tch+entity.sum_female_tch);
            $('#'+this.divid).find('.entity_library').html(entity.sum_has_library);
            $('#'+this.divid).find('.entity_electricity').html(entity.sum_has_electricity);
            $('#'+this.divid).find('.entity_toilet').html(entity.sum_toilet_common+entity.sum_toilet_boys+entity.sum_toilet_girls);

            this.show();
        }
    }

    SchoolPane.hide();
    OtherPane.hide();

    function onEachFeature(feature, layer) {
        // Bypass the usual click event and register based on
        // the entity.
        layer.on({
            click: function(e) {
                console.log(e);
                $('.marker-bounce').removeClass('marker-bounce');
                $(e.target._icon).addClass('marker-bounce');
                var academic_year = $('input[name=academic_year]:checked').val() || '10-11';
                if (feature.properties.entity_type == 'district') {
                    // Call district.getInfo and populate popup.
                    DISE.call('District.getInfo', academic_year, {
                        'name': feature.properties.district
                    }, function (data) {
                        if(data.error !== undefined){
                            alert(data.error);
                        }else{
                            OtherPane.fill(data.district.properties);
                        }
                    });
                }
                else if (feature.properties.entity_type == 'block') {
                    // Call block.getInfo and populate popup.
                    DISE.call('Block.getInfo', academic_year, {
                        'name': feature.properties.block_name
                    }, function (data) {
                        if(data.error !== undefined){
                            alert(data.error);
                        }else{
                            OtherPane.fill(data.block.properties);
                        }
                    });
                }
                else if (feature.properties.entity_type == 'cluster') {
                  // Call cluster.getInfo and populate popup.
                    DISE.call('Cluster.getInfo', academic_year, {
                        'name': feature.properties.cluster_name,
                        'block': feature.properties.block_name
                    }, function (data) {
                        if(data.error !== undefined){
                            alert(data.error);
                        }else{
                            OtherPane.fill(data.cluster.properties);
                        }
                    });
                }
                else if (feature.properties.entity_type == 'school') {
                  // Call school.getInfo and populate popup.
                    DISE.call('School.getInfo', academic_year, {
                        'code': feature.id
                    }, function (data) {
                        if(data.error !== undefined){
                            alert(data.error);
                        }else{
                            SchoolPane.fill(data.school.properties);
                        }
                    });
                };
            }
        });
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

    function loadEntityData(entity) {
        bbox = map.getBounds().toBBoxString();
        // Clear current layers.
        currentLayers.clearLayers();
        DISE.call(entity + '.search', '10-11', {
            bbox: bbox,
        }, function(data) {
            if (entity == 'Block') {
                blockLayer = createLayer(data.blocks, blockIcon);
                layerIDs.block = blockLayer._leaflet_id;
                blockLayer.addTo(currentLayers);
            } else if (entity == 'Cluster') {
                clusterLayer = createLayer(data.clusters, clusterIcon);
                layerIDs.cluster = clusterLayer._leaflet_id;
                clusterLayer.addTo(currentLayers);
            } else if (entity == 'District') {
                districtLayer = createLayer(data.districts, districtIcon);
                layerIDs.district = districtLayer._leaflet_id;
                districtLayer.addTo(currentLayers);
            } else {
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

// Function to set the map view to the layer when a filter/search
// is triggered.
    function setLayerView (layer, zoom) {
        map.setView(layer.getLayers()[0].getLatLng(), zoom);
    }

});
