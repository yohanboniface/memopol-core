jQuery.noConflict();
(function($) {

    var update_query = function()
    {
        var args = [];
        $("div.filter").each(function()
            {
                args.push($(this).find(".key").val() + "=" + $(this).find(".value").val());
            });

        var url = "/europe/parliament/generic/";
        if (args.length != 0)
        {
            url += "?" + args.join("&");
        }
        $("#query").html("Loading...");
        $.get(url, function(data){
            $("#query").html(data);
        });
    };

    $("button#apply_filter").click(function(event) {
        update_query();
    });

    $("button.remove").click(function(event) {
        $(this).parent().remove();
    });

    $("button#add").click(function(event) {
        $("div#filter_list").append('<div class="filter"><input class="key" value=""> <input class="value" value=""> <button class="remove">Remove</button> </div>');
    })

    var remove = function(foo) {
        $(this).parent().remove();
    }

    update_query();

}(jQuery));
