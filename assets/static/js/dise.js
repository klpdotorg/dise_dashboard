;(function($){
    $.extend({
        DiseAPI: function(options) {
            this.defaultOptions = {};

            var settings = $.extend({}, this.defaultOptions, options);

            this.call = function(method, session, params, success) {
                var result;
                base_params = {
                    'method': method,
                    'session': session,
                }
                console.log(base_params);
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