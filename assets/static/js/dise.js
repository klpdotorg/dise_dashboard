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
        setUrlParams: function(params) {
            var hash = decodeURIComponent($.param(params));
            console.log(hash);
            window.location.hash = hash;
        },
        updateUrlParams: function(params) {
            var existingParams = $.getUrlParams();

            var params = $.mergeObj(existingParams, params);
            $.setUrlParams(params);
        },
        getUrlParams: function() {
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
        getUrlParam: function(name) {
            return $.getUrlParams()[name];
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
        }
    });
})(jQuery);

$(function(){

    UI.init(); // Initialize UI elements
    var filtersEnabled;
    var filter_prefix = 'f_';

    var School = function(feature) {
        if (feature === undefined) return this;
        var self = this;

        self.id = feature.id;
        self.geometry = feature.geometry;
        self.properties = feature.properties;

        self.properties.address = ko.computed(function() {
            return [
                self.properties.cluster_name, self.properties.block_name,
                self.properties.district, self.properties.pincode
            ].join(', ').toString().toProperCase();
        });

        self.properties.total_student = ko.computed(function() {
            return self.properties.total_boys + self.properties.total_girls;
        });

        self.properties.total_toilet = ko.computed(function() {
            return self.properties.toilet_common + self.properties.toilet_girls + self.properties.toilet_boys
        });

        self.properties.ptr = ko.computed(function() {
            return Math.round((self.properties.total_boys+self.properties.total_girls)/(self.properties.male_tch+self.properties.female_tch))
        });

        self.properties.ptr_color = ko.computed(function() {
            var color = self.properties.ptr() <= 30 ? 'circle_stat green' : 'circle_stat red';
            return color;
        });

        self.properties.library = ko.computed(function() {
            return self.properties.library_yn_display + ", " + self.properties.books_in_library + " books";
        })
    }

    var AggregatedEntity = function(feature) {
        if (feature === undefined) return;
        var self = this;

        self.id = feature.id;
        self.geometry = feature.geometry;
        self.properties = feature.properties;

        self.properties.name = ko.computed(function() {
            var entity_name = '';
            if(self.properties.entity_type == 'district') {
                entity_name = 'district';
            }else if (self.properties.entity_type == 'pincode'){
                entity_name = 'pincode'
            }else{
                entity_name = self.properties.entity_type + '_name';
            }
            return self.properties[entity_name] + ' <small>' + self.properties.entity_type + '</small>'
        });

        self.properties.sum_pvt_schools = ko.computed(function() {
            return (self.properties.sum_schools - self.properties.sum_govt_schools);
        });

        self.properties.medium_of_instructions_list = ko.computed(function() {
            var moes = [];
            for (var i = 0; i < self.properties.medium_of_instructions.length; i++) {
                moes.push(self.properties.medium_of_instructions[i].moe + "(" + self.properties.medium_of_instructions[i].sch_count + ")");
            };
            console.log(moes);
            return moes.join(', ');
        });

        self.properties.sum_usable_classrooms = ko.computed(function() {
            return self.properties.sum_classrooms_in_good_condition + self.properties.sum_classrooms_require_minor_repair;
        });

        self.properties.sum_students = ko.computed(function() {
            return self.properties.sum_boys + self.properties.sum_girls;
        });

        self.properties.sum_total_toilet = ko.computed(function() {
            return self.properties.sum_toilet_common + self.properties.sum_toilet_boys + self.properties.sum_toilet_girls;
        });

        self.properties.sum_teachers = ko.computed(function() {
            return self.properties.sum_male_tch + self.properties.sum_female_tch;
        });

        self.properties.ptr = ko.computed(function() {
            return Math.round(self.properties.sum_students() / self.properties.sum_teachers());
        });

    }

    function SearchView(results, entity_type) {
        var self = this;

        self.results = ko.observableArray(results);
        self.search_entity = ko.observable(entity_type);

        self.n_results = ko.observable(0);

        self.n_results_map = ko.computed(function() {
            var count = 0;
            for (var i = 0; i < self.results().length; i++) {
                if (self.results()[i].geometry.coordinates.length == 2){
                    count++;
                }
            };
            return count;
        }, this);

        self.show_search_count = ko.computed(function() {
            if (self.results().length > 0) {
                return true;
            }
            return false;
        }, this);

        self.showPopupResultList = ko.observable(false);
        self.showPopupSchool = ko.observable(false);
        self.showPopupAggrEntity = ko.observable(false);

        self.highlightedSchool = ko.observable();
        self.highlightedEntity = ko.observable();

        self.highlightEntity = function(feature) {
            console.log('should highlight entity on sidebar');

            if (feature.properties.entity_type == 'school') {
                console.log('showing school');
                self.highlightedSchool(new School(feature));

                self.showPopupResultList(false);
                self.showPopupAggrEntity(false);
                self.showPopupSchool(true);
            } else {
                console.log('showing other entity');
                self.highlightedEntity(new AggregatedEntity(feature));

                self.showPopupResultList(false);
                self.showPopupSchool(false);
                self.showPopupAggrEntity(true);
            }
        }

        self.backToResultList = function() {
            self.showPopupResultList(true);
            self.showPopupSchool(false);
            self.showPopupAggrEntity(false);
            clearCrumbs();
        }
    }

    var search_view = new SearchView([], '');
    ko.applyBindings(search_view);

    // Initialize the API wrapper
    var DISE = $.DiseAPI({
        'base_url': window.location.protocol + '//' + window.location.host + '/api/v1/olap/'
    });

    /**
     * takes an object of url params and removes filters
     */
    function clear_filters_from_urlvars(url_params) {
        for (var i = 0; i < url_params.length; i++) {
            if (url_params[i].startsWith(filter_prefix)) {
                delete url_params[i];
            }
        };
        return url_params;
    }

    /**
     * removes filters from url and resets it
     */
    function clear_filters() {
        var url_params = $.getUrlParams();
        url_params = clear_filters_from_urlvars(url_params);
        $.setUrlParams(url_params);
    }

    $('body').on('change', "input[name='academic_year']", function(e) {
        var academic_year = e.target.value;
        $.updateUrlParams({
            session: academic_year
        });
    });
    $('body').on('change', "input[name='area']", function(e) {
        var area = e.target.value;
        $.updateUrlParams({
            area: area
        });
    });
    $('body').on('change', "input[name='management']", function(e) {
        var management = e.target.value;
        $.updateUrlParams({
            management: management
        });
    });

    $('#share').popover({
        html: true,
        content: "<input type='text' class='form-control' style='width: 200px' id='input-share' value='Getting URL ..'/>"
    }).on('show.bs.popover', function(e) {
        $.getJSON('https://api-ssl.bitly.com/v3/shorten?login=bibhasatklp&apiKey=R_9e527fdbc5a74a308978b90139884efc&longurl=' + encodeURIComponent(window.location.toString()), function(data) {
            if(data.status_txt == 'OK') {
                $('#input-share').val(data.data.url).focus().select();
            }
        })
    }).on('hidden.bs.popover', function(e) {
        $('#input-share').val('Getting URL ..')
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
        mapInit();
    }).on("select2-selecting", function(e) {
        // Clear the preloaded layers when the search has been used
        currentLayers.clearLayers();
        // Flip the filter switch to disable all usual map interactions.
        window.filtersEnabled = true;
        var academic_year = $('input[name=academic_year]:checked').val() || '10-11';
        if (e.object.type == 'school') {
            if(e.object.feature !== null && e.object.feature !== "{}"){
                school = JSON.parse(e.object.feature);
                $.updateUrlParams({
                    'do': 'School.getInfo',
                    session: academic_year,
                    code: school.id
                });
            } else {
                alert("Sorry, this school doesn't have a location.");
            }
        } else if (['cluster', 'assembly', 'parliament'].indexOf(e.object.type) >= 0){
            $.updateUrlParams({
                'do': e.object.type.toProperCase() + '.getSchools',
                session: academic_year,
                name: e.object.id,
                include_entity: 'true',
                z: 12
            });
        } else if (e.object.type == 'block'){
            $.updateUrlParams({
                'do': 'Block.getClusters',
                session: academic_year,
                name: e.object.id,
                include_entity: 'true',
                z: 12
            });
        } else if (e.object.type == 'district'){
            $.updateUrlParams({
                'do': 'District.getBlocks',
                session: academic_year,
                name: e.object.id,
                include_entity: 'true',
                z: 10
            });
        } else if (e.object.type == 'pincode'){
            $.updateUrlParams({
                'do': 'Pincode.getSchools',
                session: academic_year,
                pincode: e.object.id,
                include_entity: 'true',
                z: 14
            });
        } else {
            // do nothing
        }
    });

    /**
     * This is the select2 handler for preset dropdown
     */
    $(".preset_selector").select2({
        placeholder: "Select a preset",
        allowClear: true
    }).on("select2-selecting", function(e) {
        console.log(e);
    });

    $("#presets .glyphicon-cog").click(function(){
        var preset = $("select.preset_selector").val();

        if (preset == ""){
            alert('Please select a preset first');
        } else {
            $("#preset-editor-" + preset).toggleClass("activate");
        }
    });

    /**
     * This is fired when the Search button is hit on preset editors.
     * @param  {obj} e    Event object
     * @return {void}
     */
    $('body').on('click', '.filter-apply', function(e) {
        var data_type = $(e.target).attr('data-type');
        var academic_year = $('input[name=academic_year]:checked').val() || '10-11';

        switch (data_type) {
            case 'facilities':
                var filters = UI.serializePreset()[data_type];
                console.log(filters);

                if (filters.length == 0) {
                    window.location = window.location.protocol + '//' + window.location.host;
                }

                $.setUrlParams({
                    do: 'School.search',
                    session: academic_year,
                    bbox: map.getBounds().toBBoxString(),
                    f: encodeURIComponent(JSON.stringify({
                        facilities: filters
                    })),
                    enbl: 'f'
                });

                break;
        }
    });

    /**
     * Clears the breadcrumb area
     */
    function clearCrumbs(){
        $('li.crumb').remove();
    }

    /**
     * Fills the breadcrumb with the parent entities
     * @param  {str} entity_type       school/cluster/block/district
     * @param  {obj} entity_properties property part of the geojson
     * @return {void}                   [description]
     */
    function fillCrumb(entity_type, entity_properties) {
        clearCrumbs();
        var academic_year = $('input[name=academic_year]:checked').val() || '10-11';

        if (['School', 'school'].indexOf(entity_type) > -1) {
            UI.renderCrumbs([
                [entity_properties.district, "#" + $.param({
                    'do': 'District.getBlocks',
                    session: academic_year,
                    name: entity_properties.district,
                    include_entity: true,
                    z: 10
                }), 'district'],
                [entity_properties.block_name, "#" + $.param({
                    'do': 'Block.getClusters',
                    session: academic_year,
                    name: entity_properties.block_name,
                    include_entity: true,
                    z: 12
                }), 'block'],
                [entity_properties.cluster_name, "#" + $.param({
                    'do': 'Cluster.getSchools',
                    session: academic_year,
                    name: entity_properties.cluster_name,
                    block: entity_properties.block_name,
                    include_entity: true,
                    z: 13
                }), 'cluster']
            ]);
        } else if (['cluster', 'Cluster'].indexOf(entity_type) > -1) {
            UI.renderCrumbs([
                [entity_properties.district, "#" + $.param({
                    'do': 'District.getBlocks',
                    session: academic_year,
                    name: entity_properties.district,
                    include_entity: true,
                    z: 10
                }), 'district'],
                [entity_properties.block_name, "#" + $.param({
                    'do': 'Block.getClusters',
                    session: academic_year,
                    name: entity_properties.block_name,
                    include_entity: true,
                    z: 12
                }), 'block']
            ]);
        } else if (['block', 'Block'].indexOf(entity_type) > -1) {
            UI.renderCrumbs([
                [entity_properties.district, "#" + $.param({
                    'do': 'District.getBlocks',
                    session: academic_year,
                    name: entity_properties.district,
                    include_entity: true,
                    z: 10
                }), 'district']
            ]);
        }
    }

    function fillPane(feature) {
        var academic_year = $('input[name=academic_year]:checked').val() || '10-11';

        if (feature.properties.entity_type == 'district') {
            // Call district.getInfo and populate popup.
            DISE.call('District.getInfo', academic_year, {
                'name': feature.properties.district
            }, function (data) {
                if(data.error !== undefined){
                    alert(data.error);
                }else{
                    search_view.highlightEntity(data.district);
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
                    search_view.highlightEntity(data.block);
                    fillCrumb('block', data.block.properties);
                }
            });
        }
        else if (feature.properties.entity_type == 'pincode') {
            // Call block.getInfo and populate popup.
            DISE.call('Pincode.getInfo', academic_year, {
                'pincode': feature.properties.pincode
            }, function (data) {
                if(data.error !== undefined){
                    alert(data.error);
                }else{
                    search_view.highlightEntity(data.pincode);
                    fillCrumb('pincode', data.pincode.properties);
                }
            });
        }
        else if (feature.properties.entity_type == 'assembly') {
            // Call assembly.getInfo and populate popup.
            DISE.call('Assembly.getInfo', academic_year, {
                'name': feature.properties.assembly_name
            }, function (data) {
                if(data.error !== undefined){
                    alert(data.error);
                }else{
                    search_view.highlightEntity(data.assembly);
                    fillCrumb('assembly', data.assembly.properties);
                }
            });
        }
        else if (feature.properties.entity_type == 'parliament') {
            // Call parliament.getInfo and populate popup.
            DISE.call('Parliament.getInfo', academic_year, {
                'name': feature.properties.parliament_name
            }, function (data) {
                if(data.error !== undefined){
                    alert(data.error);
                }else{
                    search_view.highlightEntity(data.parliament);
                    fillCrumb('parliament', data.parliament.properties);
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
                    search_view.highlightEntity(data.cluster);
                    fillCrumb('cluster', data.cluster.properties);
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
                    search_view.highlightEntity(data.school);
                    fillCrumb('school', data.school.properties);
                }
            });
        };
    }

    function onEachFeature(feature, layer) {
        // Bypass the usual click event and register based on
        // the entity.
        layer.on({
            click: function(e) {
                console.log(e);
                $('.marker-bounce').removeClass('marker-bounce');
                $(e.target._icon).addClass('marker-bounce');

                fillPane(feature);
            }
        });
    }

    function createLayer(feature_or_features, icon) {
        // @param {String} feature_or_features  Either Feature or FeatureCollection
        // @param {String} zoom                 Zoom level of the map
        console.log(feature_or_features);
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

    function is_filter_enabled(){
        if($.getUrlParam('enbl') !== undefined && $.getUrlParam('enbl').indexOf('f') >= 0) {
            return true;
        } else if (window.filtersEnabled !== undefined) {
            return window.filtersEnabled;
        } else {
            return false;
        }
    }

    function mapInit () {
        // Load the district data and plot.
        window.filtersEnabled = is_filter_enabled();
        console.log('filter enabled: ' + window.filtersEnabled);
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
        } else if (layerID == layerIDs.block) {
            loadEntityData('Block');
        } else if (layerID == layerIDs.cluster) {
            loadEntityData('Cluster');
        } else {
            loadEntityData('School');
        }
    }

    // When the map is zoomed, load the necessary data
    map.on('zoomend', function(e) {
      // If filters are enabled then don't load the usual layers.
        //var bbox = map.getBounds().toBBoxString();
        console.log('zoooomed');

        if (!window.filtersEnabled) {
            console.log('filters not enabled, updating map');
            updateLayers(map.getZoom());
        }
    })

    // When the map is panned, load the data in the new bounds.
    map.on('dragend', function(e) {
        console.log('dragged');

        if (!window.filtersEnabled) {
            var bbox = map.getBounds().toBBoxString();
            $.updateUrlParams({bbox: bbox});
        }
    })

    // Function to set the map view to the layer when a filter/search
    // is triggered.
    function setLayerView (layer, zoom) {
        map.setView(layer.getLayers()[0].getLatLng(), zoom);
    }

    /**
     * Pans the map to focus the feature collection
     * @param  {[type]} sanitized_featurecollection Sanitized as in no Feature w/o coords
     */
    function panToFeatureCollection(sanitized_featurecollection) {
        var latlngs = [];
        for (var i = 0; i < sanitized_featurecollection.features.length; i++) {
            latlngs.push(sanitized_featurecollection.features[i].geometry.coordinates)
        };
        map.fitBounds(L.GeoJSON.coordsToLatLngs(latlngs));
    }

    function handleHashChange(e) {
        if ($.getUrlParam('do') === undefined) {
            return;
        }

        $('#share').popover('hide')

        // Invoke initial map layers.
        var params = $.getUrlParams();
        console.log(params);

        var method = params.do;
        if(method.split('.').length !== 2){
            alert('invalid do parameter');
        }else{
            delete params.do;
            var entity = method.split('.')[0];
            var entity_lower = entity.toLowerCase();
            var action = method.split('.')[1];
        }

        if (['School', 'Cluster', 'Block', 'District', 'Pincode', 'Assembly', 'Parliament'].indexOf(entity) == -1) {
            alert('Sorry, ' + entity + ' is an unknown entity.');
            return;
        }

        var session = params.session || $('input[name=academic_year]:checked').val() || '10-11';
        delete params.session;
        $('input[name=academic_year]').each(function(i) {
            if ($(this).val() == session) {
                $(this).parent('label').siblings('label').removeClass('active');
                $(this).parent('label').addClass('active');
                $(this).prop('checked', true);
                $(this).attr('checked', 'checked');
            } else {
                $(this).prop('checked', false);
                $(this).removeAttr('checked');
            }
        });

        // Clear current layers.
        currentLayers.clearLayers();

        if (action == 'getInfo'){
            // just needs to place the marker and fill Pane
            window.filtersEnabled = true;
            DISE.call(method, session, params, function(data) {
                if (data.error !== undefined) {
                    alert(data.error);
                    return;
                }

                search_view.highlightEntity(data[entity_lower]);
                search_view.show_search_count(false);

                fillCrumb(entity_lower, data[entity_lower].properties);

                if (data[entity_lower].geometry.coordinates.length == 2) {
                    newLayer = createLayer(data[entity_lower], customIcon(entity_lower));
                    newLayer.addTo(currentLayers);

                    map.panTo(L.GeoJSON.coordsToLatLng(data[entity_lower].geometry.coordinates));
                } else {
                    alert('Sorry, no location available for this.');
                }
            });
        } else if (['getSchools', 'getClusters', 'getBlocks'].indexOf(action) > -1) {
            // show all the markers
            // if include_entity is set, fill the Pane
            window.filtersEnabled = true;
            DISE.call(method, session, params, function(data) {
                if (data.error !== undefined) {
                    alert(data.error);
                    return;
                }

                // Let's sanitize the geojson
                var sanitized_results = {
                    type: "FeatureCollection",
                    features: []
                }

                for (var i = 0; i < data.results.features.length; i++) {
                    if (data.results.features[i].geometry.coordinates.length == 2) {
                        sanitized_results.features.push(data.results.features[i]);
                    }
                };

                // getSchools -> School
                child_entity = action.substr(0, action.length-1).replace('get', '');
                icon = customIcon(child_entity.toLowerCase());

                newLayer = createLayer(sanitized_results, icon);
                newLayer.addTo(currentLayers);

                // updates the result pane
                search_view.results(data.results.features);
                search_view.n_results(data.total_count);
                search_view.search_entity(child_entity);
                search_view.showPopupResultList(true);

                if (params.include_entity !== undefined && params.include_entity == 'true' && data[entity_lower] !== undefined) {
                    console.log('showing entity');
                    search_view.showPopupResultList(false);

                    search_view.highlightEntity(data[entity_lower]);
                    fillCrumb(entity_lower, data[entity_lower].properties);

                    if (data[entity_lower].geometry.coordinates.length == 2) {
                        newLayer = createLayer(data[entity_lower], customIcon(entity_lower));
                        newLayer.addTo(currentLayers);

                        map.panTo(L.GeoJSON.coordsToLatLng(data[entity_lower].geometry.coordinates));
                    } else {
                        alert('Sorry, no location available for this.');
                    }
                } else {
                    panToFeatureCollection(sanitized_results);
                }
            });
        } else if (['search'].indexOf(action) > -1) {
            window.filtersEnabled = is_filter_enabled();

            DISE.call(method, session, params, function(data) {
                if (data.error !== undefined) {
                    alert(data.error);
                    return;
                }

                // Let's sanitize the geojson
                var sanitized_results = {
                    type: "FeatureCollection",
                    features: []
                }

                for (var i = 0; i < data.results.features.length; i++) {
                    if (data.results.features[i].geometry.coordinates.length == 2) {
                        sanitized_results.features.push(data.results.features[i]);
                    }
                };

                // Let's plot the valid geojson now
                icon = customIcon(entity_lower);
                newLayer = createLayer(sanitized_results, icon);
                newLayer.addTo(currentLayers);

                // updates the count pane
                search_view.results(data.results.features);
                search_view.n_results(data.total_count);
                search_view.search_entity(entity);
                search_view.showPopupResultList(true);

                if ($.getUrlParam('bbox') !== undefined){
                    var bbox = $.getUrlParam('bbox').split(',');
                    map.fitBounds([
                        [bbox[1], bbox[0]],
                        [bbox[3], bbox[2]]
                    ]);
                }
            });
        }

        if ($.getUrlParam('z') !== undefined){
            map.setZoom(parseInt($.getUrlParam('z')));
        }

    }

    if ("onhashchange" in window){
        $(window).on('hashchange', handleHashChange);
    }

    if ($.getUrlParam('do') === undefined) {
        // Invoke initial map layers.
        console.log('initiating map');
        mapInit();
    } else {
        // query and show the results in hash
        handleHashChange();
    };

});
