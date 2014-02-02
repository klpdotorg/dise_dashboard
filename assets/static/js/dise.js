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
        updateUrlParams: function(params) {
            var existingParams = $.getUrlVars();
            console.log(existingParams);
            var params = $.mergeObj(existingParams, params);
            var hash = decodeURIComponent($.param(params));
            window.location.hash = hash;
        },
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

            this.search = function(entity, session, params, success) {
                return this.call(entity + '.search', session, params, success);
            }

            this.info = function(entity, session, params, success) {
                return this.call(entity + '.getInfo', session, params, success);
            }

            return this;
        },
        mergeObj: function(obj1, obj2) {
            var obj = {};
            for (var attrname in obj1) {
                obj[attrname] = obj1[attrname];
            }
            for (var attrname in obj2) {
                obj[attrname] = obj2[attrname];
            }
            return obj;
        },
        getUrlVars: function() {
            var vars = [],
                hash;
            if(window.location.href.indexOf('#') > 0){
                var hashes = window.location.href.slice(window.location.href.indexOf('#') + 1).split('&');
                for (var i = 0; i < hashes.length; i++) {
                    hash = hashes[i].split('=');
                    // vars.push(hash[0]);
                    vars[hash[0]] = hash[1];
                }
            }
            return vars;
        },
        getUrlVar: function(name) {
            return $.getUrlVars()[name];
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
        var academic_year = $('input[name=academic_year]:checked').val() || '10-11';
        if (entity == 'School') {
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
            $('#'+this.divid).find('.total_boys').html(school.total_boys);
            $('#'+this.divid).find('.total_girls').html(school.total_girls);
            $('#'+this.divid).find('.total_student').html(school.total_boys+school.total_girls);

            $('#'+this.divid).find('.total_toilet').html(
                school.toilet_common + school.toilet_girls + school.toilet_boys
            );
            $('#'+this.divid).find('.total_toilet_girls').html(school.toilet_girls);
            $('#'+this.divid).find('.total_toilet_boys').html(school.toilet_boys);

            $('#'+this.divid).find('.total_classrooms').html(school.tot_clrooms);
            $('#'+this.divid).find('.ptr').html(
                (school.total_boys+school.total_girls)/(school.male_tch+school.female_tch)
            );
            $('#'+this.divid).find('.medium_of_instruction').html(school.medium_of_instruction_display);
            $('#'+this.divid).find('.sch_category').html(school.sch_category_display);
            $('#'+this.divid).find('.sch_management').html(school.sch_management_display);
            $('#'+this.divid).find('.electricity').html(school.electricity_display);
            $('#'+this.divid).find('.library').html(school.library_yn_display + ", " + school.books_in_library + " books.");
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

    function getPane(entity) {
        if (['School', 'school'].indexOf(entity) > -1) {
            return SchoolPane;
        } else if (['cluster', 'block', 'district', 'pincode', 'Cluster', 'Block', 'District', 'Pincode'].indexOf(entity) > -1) {
            return OtherPane;
        }
    }

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

    function loadEntityData(entity, params) {
        bbox = map.getBounds().toBBoxString();
        var extraParams = {};
        // Clear current layers.
        currentLayers.clearLayers();

        var academic_year = $('input[name=academic_year]:checked').val() || '10-11';
        extraParams['do'] = entity + '.search';
        extraParams['session'] = academic_year;

        if(typeof params !== 'undefined' && typeof params === 'object'){
            extraParams = $.mergeObj(extraParams, params);
        }

        extraParams['bbox'] = bbox;

        $.updateUrlParams(extraParams);
    }

    function mapInit () {
        // Load the district data and plot.
        loadEntityData('District');
    }

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
      }else{
        var bbox = map.getBounds().toBBoxString();
        $.updateUrlParams({bbox: bbox});
      }
    })

// When the map is panned, load the data in the new bounds.
    map.on('dragend', function(e) {
      if (!filtersEnabled) {
        currentLayers.eachLayer(function(layer) {
          updateData(layer);
        });
      }else{
        var bbox = map.getBounds().toBBoxString();
        $.updateUrlParams({bbox: bbox});
      }
    })

// Function to set the map view to the layer when a filter/search
// is triggered.
    function setLayerView (layer, zoom) {
        map.setView(layer.getLayers()[0].getLatLng(), zoom);
    }

    function handleHashChange(e) {
        if ($.getUrlVar('do') !== undefined) {
            // Invoke initial map layers.
            var params = $.getUrlVars();
            var method = params.do;
            if(method.split('.').length !== 2){
                alert('invalid do parameter');
            }else{
                delete params.do;
                var entity = method.split('.')[0];
                var entity_lower = entity.toLowerCase();
                var action = method.split('.')[1];
            }

            if (['School', 'Cluster', 'Block', 'District', 'Pincode'].indexOf(entity) == -1) {
                alert('Sorry, ' + entity + ' is an unknown entity.');
                return;
            }

            var session = params.academic_year || $('input[name=academic_year]:checked').val() || '10-11';
            delete params.academic_year;

            // Clear current layers.
            currentLayers.clearLayers();

            if ($.getUrlVar('bbox') !== undefined){
                var bbox = $.getUrlVar('bbox').split(',');
                map.fitBounds([
                    [bbox[1], bbox[0]],
                    [bbox[3], bbox[2]]
                ]);
            }

            if (action == 'getInfo'){
                // just needs to place the marker and fill Pane
                DISE.call(method, session, params, function(data) {
                    if (data.error !== undefined) {
                        alert(data.error);
                        return;
                    }

                    pane = getPane(entity);
                    pane.fill(data[entity_lower].properties);

                    if (data[entity_lower].geometry.coordinates.length == 2) {
                        newLayer = createLayer(data[entity_lower], customIcon(entity_lower));
                        setLayerView(newLayer, 15);
                        newLayer.addTo(currentLayers);
                    } else {
                        alert('Sorry, no location available for this.');
                    }
                });
            } else if (['search', 'getSchools', 'getClusters', 'getBlocks'].indexOf(action) > -1) {
                // show all the markers
                // if include_entity is set, fill the Pane
            }
        }
    }

    if ("onhashchange" in window){
        $(window).on('hashchange', handleHashChange);
    }

    if ($.getUrlVar('do') === undefined) {
        // Invoke initial map layers.
        console.log('initiating map');
        mapInit();
    } else {
        // Invoke search mechanism
        filtersEnabled = true;
        console.log('do ' + $.getUrlVar('do'));

        // query and show the results in hash
        handleHashChange();
    };

});
