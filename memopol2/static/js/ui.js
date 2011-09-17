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

$('#content h1:first').addClass('document-title');

// table
$("table.mep-list").tablesorter();
$("table.mp-list").tablesorter({ headers: { 2: { sorter: false }, }  });
$("table.mp-list, table.mep-list").tableFilter({
    filteredRows: function() {
        $("table.mp-list, table.mep-list").trigger('filteredRows');
    }
});


function FilterExtension(table) {
    this.table = table;
    var filtersBackup = this.filtersBackup = [];
    this.table.find('.filters .filter').each(function(index, filter) {
        filtersBackup[index] = $(filter).children().clone();
    });
    this.table.bind('filteredRows', $.proxy(this, 'refresh'));
    this.refresh(true);
}

FilterExtension.prototype.refresh = function(keepEmptyOptions) {
    this.table.find('.filters .filter').each($.proxy(function(index, filter) {
        var $filter = $(filter);

        // reset select from previous state
        var filterValue = $filter.val();
        $filter.empty().append(this.filtersBackup[index].clone()).val(filterValue);
        
        this.displayCounts($filter, this.countEntries($filter), keepEmptyOptions);
    }, this));
};

FilterExtension.prototype.isSelected = function(filter) {
    var filterValue = filter.val();
    return $.trim(filterValue) || filterValue != new picnet.ui.filter.TableFilterOptions().selectOptionLabel;
};

FilterExtension.prototype.countEntries = function(filter) {
    var counts = {};
    var index = filter.parent().prevAll().length;
    var cells = this.table.find('tbody tr[filtermatch!=false] td:nth-child(' + (index + 1) + ')');
    cells.each(function(index, cell) {
        var html = $(cell).html();
        counts[html] = (counts[html] || 0) + 1;
    });
    return this.stripKeys(counts);
};

FilterExtension.prototype.displayCounts = function(filter, counts, keepEmptyOptions) {
    filter.find('option[value]').each($.proxy(function(index, option) {
        $option = $(option);
        count = counts[$.trim($option.val())] || 0;
        
        $option.html($option.html() + ' (' + count + ')');
        if (!count && !this.isSelected(filter)){
            $option.remove();
        }
    }, this));
};

FilterExtension.prototype.stripKeys = function(counts) {
    var stripedCounts = {};
    for (html in counts) {
        stripedCounts[jQuery.trim(html.replace(/<\/?[^>]+>/gi, ''))] = counts[html];
    }
    return stripedCounts;
};

var filterExtension = new FilterExtension($("table.mep-list"));

$("table.mep-list tbody tr, table.mp-list tbody tr").hover(
    function() {$(this).addClass('odd');},
    function() {$(this).removeClass('odd');}
);

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
    livesearchindex: -1,
    livesearchitems: null,
    livesearch: function(self, q) {
        if ($.livesearchtext == q) {
            q = self.val();
            q = q.replace(/\s+$/, '');
            if (!/\*$/.exec(q)) { q += '*'; }
            if ($('#search').length) {
                // serialize form and extract only types from qs
                q += '&' + $('#search').serialize().replace(/q=[^&]+/, '').substring(1);
            }
            $.get(livesearch.attr('alt')+'?limit=10&q='+q, function(data) {
                if (/li/.exec(data)) {
                    livesearch.html(data);
                    $.livesearchindex = -1;
                    $.livesearchitems = $('li', livesearch);
                    $.livesearchitems.hover(function() {
                        $.livesearchitems.removeClass('odd');
                        $(this).addClass('odd');
                    }, function() {
                        $(this).removeClass('odd');
                    });
                    livesearch.show();
                } else {
                    livesearch.hide();
                }
            });
        }
    }
});
$('input.search-text, #search #id_q').focus(function() {
    var self = $(this);
    var pos = self.offset();
    livesearch.css('left', pos.left);
    livesearch.css('top', pos.top+10+self.height());
});
$('input.search-text, #search #id_q').keydown(function(e) {
    var self = $(this);
    var code = (e.keyCode ? e.keyCode : e.which);
    if (code == 13) {
        // enter
        if ($.livesearchindex >= 0) {
            window.location.href = $('a', $.livesearchitems[$.livesearchindex]).attr('href');
            return false;
        }
    } else if (code == 40) {
        // up
        $.livesearchindex++;
        if ($.livesearchindex >= $.livesearchitems.length) {
            $.livesearchindex--;
        }
        $.livesearchitems.removeClass('odd');
        $($.livesearchitems[$.livesearchindex]).addClass('odd');
        return false;
    } else if (code == 38) {
        // down
        $.livesearchindex--;
        $.livesearchitems.removeClass('odd');
        if ($.livesearchindex >= 0) {
            $($.livesearchitems[$.livesearchindex]).addClass('odd');
        } else {
            $.livesearchindex = -1;
        }
        return false;
    } else {
        var q = self.val();
        if (q.length >= 2) {
            $.livesearchtext = q;
            setTimeout(function() {$.livesearch(self, q)}, 1000);
        }
    }
});
$('body').click(function() {livesearch.hide()});

}(jQuery));
