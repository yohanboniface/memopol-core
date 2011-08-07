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


// table
$("table.mep-list, table.mp-list").tablesorter({ headers: { 3: { sorter: false }, }  });
// FIXME dont know why but sorting dont work with mp-list..
//$('table.mep-list, table.mp-list').tableFilter();
$('table.mep-list').tableFilter();

// contact details
$('a.more-contact').click(function() {
    // dynamic contact detail
    $('div.body', $(this).parents('td')).load($(this).attr('href'));
    return false;
});

// the image #call-now click get his link from a.call-now from the contact details
$('a#call-now').attr('href', $('a.call-now').attr('href'));

// live search
var livesearch = $('#livesearch');
$.extend($, {
    livesearchtext: null,
    livesearch: function(q) {
        if ($.livesearchtext == q) {
            $.get(livesearch.attr('alt')+'?limit=10&q='+q, function(data) {
                if (/li/.exec(data)) {
                    livesearch.html(data);
                    livesearch.show();
                } else {
                    livesearch.hide();
                }
            });
        }
    }
});
$('input.search-text').focus(function() {
    var self = $(this);
    var pos = self.offset();
    livesearch.css('left', pos.left);
    livesearch.css('top', pos.top+10+self.height());
});
$('input.search-text').keyup(function() {
    var self = $(this);
    var q = self.val();
    if (q.length > 2) {
        q += '*';
    $.livesearchtext = q;
    setTimeout(function() {$.livesearch(q)}, 1000);
    }
});
$('body').click(function() {livesearch.hide()});

}(jQuery));
