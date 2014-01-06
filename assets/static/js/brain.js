var UI = {

    init: function(){

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


        this.renderCrumbs([
            ["Karnataka", "#"],
            ["Bangalore", "#"],
            ["HSR Layout", "#"]
        ]);

        this.initICheck();
        this.initSliders();
    },


    initICheck: function(){
        $('.check-list').iCheck({
            checkboxClass: 'icheckbox_square-orange',
            radioClass: 'iradio_flat'
        });
    },

    initSliders: function(){
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
    },

    renderCrumbs: function(bs){
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
    },

    serializeCategory: function(){
        var data = {
            "academic_year": [],
            "area": [],
            "management": [],
        };

        $("input[name='academic_year']").each(function(){
            var $this = $(this);
            if ($this.prop("checked")) {
                data["academic_year"].push($this.val());
            }
        });

        $("input[name='area']").each(function(){
            var $this = $(this);
            if ($this.prop("checked")) {
                data["area"].push($this.val());
            }
        });

        $("input[name='management']").each(function(){
            var $this = $(this);
            if ($this.prop("checked")) {
                data["management"].push($this.val());
            }
        });

        return data;
    },

    serializePreset: function() {
        var data = {
            "facilities" : [],
            "rte": [],
            "teachers": [],
            "range": {
                "classrooms": [],
                "teachers": [],
                "girls_in_class": [],
                "boys_in_class": [],
            },
            "compound": {
                "girls_lesser_than_boys": false,
                "enrollment_from": [],
                "pupil_teacher_ratio": []
            }
        };


        $("input[name='facilities']").each(function(){
            var $this = $(this);
            if ($this.prop("checked")) {
                data["facilities"].push($this.val());
            }
        });

        $("input[name='rte']").each(function(){
            var $this = $(this);
            if ($this.prop("checked")) {
                data["rte"].push($this.val());
            }
        });

        $("input[name='teachers']").each(function(){
            var $this = $(this);
            if ($this.prop("checked")) {
                data["teachers"].push($this.val());
            }
        });


        data["compound"]["girls_lesser_than_boys"] = $("#wgltb").prop("checked");
        data["compound"]["enrollment_from"] = [$("#wef-low").val(), $("#wef-high").val()];
        data["compound"]["pupil_teacher_ratio"] = [$("#wptrf-low").val(), $("#wptrf-high").val()];

        data["range"]["classrooms"] = [$("#wncb-low").val(), $("#wncb-high").val()];
        data["range"]["teachers"] = [$("#wntb-low").val(), $("#wntb-high").val()];
        data["range"]["girls_in_class"] = [$("#wngic-low").val(), $("#wngic-high").val()];
        data["range"]["boys_in_class"] = [$("#wnbic-low").val(), $("#wnbic-high").val()];

        return data;
    }
}
