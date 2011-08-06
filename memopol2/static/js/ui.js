jQuery.noConflict();

// replace mugshot by placeholder on errors
// --------------------------------------

function onMugshotError(source) {
    source.src = "/static/img/default-mugshot.png";
    source.className = "defaultMugshot";
    source.onerror = "";
    return true;
}

(function($) {

// collapsible elements
$(".collapsed~.body").hide();
$(".collapsible").click(function(){
    if ($(this).hasClass("collapsed"))
    {
        $(this).removeClass("collapsed").addClass("expanded");
        $(this).next(".body").show("fast");
    }
    else
    {
        $(this).removeClass("expanded").addClass("collapsed");
        $(this).next(".body").hide("fast");
    }
});

// contact details
$('span.collapsible-contact').click(function() {
    // dynamic contact detail
    $('div.body', $(this).parents('td')).load($(this).attr('alt'));
});


// table
$("table.mep-list, table.mp-list").tablesorter({ headers: { 3: { sorter: false }, }  });
// FIXME dont know why but sorting dont work with mp-list..
//$('table.mep-list, table.mp-list').tableFilter();
$('table.mep-list').tableFilter();

}(jQuery));
