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
    $("#filter-select").select2({
        dropdownCssClass: "bigdrop",
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

    function plotOnMap(feature_or_features, zoom, icon) {
        // @param {String} feature_or_features  Either Feature or FeatureCollection
        // @param {String} zoom                 Zoom level of the map
        // console.log(feature_or_features);
        L.geoJson(
            feature_or_features,
            {
                pointToLayer: function (feature, latlng) {
                    window.map.setView(latlng, zoom);
                    if (icon != undefined) {
                        return L.marker(latlng, {icon: icon});
                    }
                    else {
                        return L.marker(latlng);
                    }
                },
                onEachFeature: onEachFeature
            }
        ).addTo(window.map);
    }

    // Initialize the API wrapper
    var DISE = $.DiseAPI({
        'base_url': window.location.toString() + 'api/v1/olap/'
    })

    $("#filter-select").on("change", function(e) {
        // console.log(e);
        if (e.added.type == 'school') {
            if(e.added.feature !== null && e.added.feature !== "{}"){
                plotOnMap(JSON.parse(e.added.feature), 15, schoolIcon);
            } else {
                alert("Sorry, this school doesn't have a location.");
            }
        } else if (e.added.type == 'cluster'){
            DISE.call('Cluster.getSchools', '10-11', {
                name: e.added.id,
                format: 'geo'
            }, function(data) {
                console.log(data);
                plotOnMap(data.schools, 10, schoolIcon);
            });
        } else {
            // do nothing
        }
    });
});