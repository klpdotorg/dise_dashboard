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