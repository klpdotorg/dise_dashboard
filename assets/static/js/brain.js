$(function(){
    $(".filter-icon").tooltip();
    $("table.filter-icon-set td").click(function(){
	    $(this).toggleClass("selected");
    });

    $("#presets li").click(function(){
	    $("#presets li").removeClass("active");
	    $(this).addClass("active");
    });

    $(".reset_preset").tooltip();

    $(".reset_preset").click(function(e){
        if(!confirm("Are you sure? This action cannot be undone!")) return false;
    });

    $("#presets li .glyphicon-cog").click(function(){
        $("#preset-editor").toggleClass("activate");
    });

    $(".action-row button, .action-row a").click(function(e){
        $("#preset-editor").toggleClass("activate");
    });

    $("#control_toggle").click(function(e){
        $("#controls").toggleClass("hidden_controls");
        $("#control_toggle_icon").toggleClass("flip");
        var t = $("#control_toggle").find("span.text");
        var t_html = (t.html() === "Hide") ? "Show" : "Hide";
        t.html(t_html);
    });


    renderCrumbs([
        ["Karnataka", "#"],
        ["Bangalore", "#"],
        ["HSR Layout", "#"]
    ])

    // Sliders
    $(".range-slider").slider({
        range: true,
        min: 0,
        max: 30,
        values: [10,20],
        slide: function(e, s){
            var high = $("#" + $(this).attr("data-high"));
            var low = $("#" + $(this).attr("data-low"));
            high.val(s.values[1]);
            low.val(s.values[0]);
        }
    });

    // Filter
    $("#super-search-container button").click(function(){
        $("#filter-editor").toggleClass("activate");
    });

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

    $("#filter-select").on("change", function(e) {
        console.log(e);
        if (e.added.type == 'school' && e.added.feature !== null && e.added.feature !== "{}") {
            // var marker = L.marker(e.added.centroid).addTo(window.map);
            // marker.bindPopup(e.added.text).openPopup();
            console.log(JSON.parse(e.added.feature));
            L.geoJson(
                JSON.parse(e.added.feature),
                {
                    pointToLayer: function (feature, latlng) {
                        window.map.setView(latlng, 12);
                        return L.marker(latlng);
                    },
                    onEachFeature: onEachFeature
                }
            ).addTo(window.map);
        } else if (e.added.type == 'cluster'){
        } else {
            alert("Sorry, this school doesn't have a location.");
        }
    });
});


function renderCrumbs(bs){
    var ol = $("ol.top-breadcrumbs");
    ol.html('<li><a class="navbar-brand" href="#">DISE</a></li>');

    for (var i in bs){
        var b = bs[i];
        var li = $("<li>");
        var a = $("<a>").attr("href", b[1]).html(b[0]);
        ol.append(li.append(a));
    }


    // Coloring and z-index
    var class_array = ["a", "b", "c", "d", "e"]
    ol.find("li").each(function(i, e){
        $(e).addClass(class_array[i]);
    });
}
