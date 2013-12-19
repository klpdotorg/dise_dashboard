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
        $("#control_toggle").toggleClass("flip");
        var t = $("#control_toggle").parent().find("span.text");
        var t_html = (t.html() === "Hide") ? "Show" : "Hide";
        t.html(t_html);
    });


    // Breadcrumbs coloring and z-index
    var class_array = ["a", "b", "c", "d", "e"]
    $("ol.top-breadcrumbs li").each(function(i, e){
        $(e).addClass(class_array[i]);
    });

    // Sliders
    $(".range-slider").slider({
        range: true,
        min: 0,
        max: 30,
        values: [10,20]
    });

    // Filter
    $("#super-search-container button").click(function(){
        $("#filter-editor").toggleClass("activate");
    });

    $("#filter-select").select2({
        dropdownCssClass: "bigdrop",
        data:
        [
            {
                text: "District",
                children: [
                    {
                        id: "d1",
                        text: "Bellary"
                    },
                    {
                        id: "d2",
                        text: "Koppal"
                    }
                ]
            },
            {
                text: "Taluk",
                children: [
                    {
                        id: "t1",
                        text: "Hospet"
                    }
                ]
            }
        ]
    });
});
