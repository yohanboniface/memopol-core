jQuery.noConflict();
(function($) {

    var update_query = function()
    {
        var args = [];
        $("div.filter").each(function()
            {
                var key = $(this).find(".key").attr("id");
                var value = $(this).find(".value").val();
                if (key && value)
                {
                    args.push(key + "=" + encodeURIComponent(value));
                }
            });

        var url = "/europe/parliament/generic/";
        if (args.length != 0)
        {
            url += "?" + args.join("&");
        }
        $("span#show_query").html(url);
        $("#query").html("Loading...");
        $.get(url, function(data){
            $("#query").html(data);
        });
    };

    var update_filters_list = function() {

        $("select#filter_choice").find("option").each(function() {
            console.debug("label#" + $(this).attr("id"));
            console.debug($("label#" + $(this).attr("id")));
            if ($("label#" + $(this).attr("id")).length) {
                $(this).removeClass("visible");
                $(this).addClass("not_visible")
            } else {
                $(this).removeClass("not_visible");
                $(this).addClass("visible");
            }
        });

        if ($("option.visible").length) {
            $("select#filter_choice").val($("option.visible").first().attr("id"));
        } else {
            $("div#adders").hide()
        }
    };

    $("button#apply_filter").click(function(event) {
        update_query();
    });

    var button_remove = function(event) {
        console.debug("remove !");
        $(this).parent().remove();
        $("div#adders").show();
        update_filters_list();
    }

    $("button.remove").click(button_remove);

    $("button#add").click(function(event) {
        //var a = $("select#filter_choice").val();
        //$("div#filter_list").append('<div class="filter"><label class="key" id="' + $("select#filter_choice").val() + '">' + $("select#filter_choice").val() + '</label> <input class="value" value=""> <button class="remove">Remove</button> </div>');

        $.get("/europe/parliament/filter/" + $("select#filter_choice").val() + "/", function(data){
            var new_filter = document.createElement("div");
            new_filter.classList.add("filter");

            var new_label = document.createElement("label");
            new_label.classList.add("key");
            new_label.id = $("select#filter_choice").val();
            new_label.textContent = $("select#filter_choice").val();
            if (data.length) {
                var select = document.createElement("select");
                select.classList.add("value");
                var data = eval('(' + data + ')');
                for (d in data) {
                    var new_option = document.createElement("option");
                    new_option.value = data[d][0];
                    new_option.text = data[d][1];
                    select.appendChild(new_option)
                }
            } else {
                var select = document.createElement("input");
                select.classList.add("value");
            }
            var button = document.createElement("button");
            button.classList.add("value");
            button.textContent = "Remove";
            button.onclick = button_remove;

            new_filter.appendChild(new_label);
            new_filter.appendChild(select);
            new_filter.appendChild(button);

            $("div#filter_list").append(new_filter);

            update_filters_list();
        });
    })

    var remove = function(foo) {
        $(this).parent().remove();
    }

    update_filters_list();
    update_query();

}(jQuery));
