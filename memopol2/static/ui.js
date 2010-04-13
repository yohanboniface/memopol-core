jQuery.noConflict();

function changeVisibility(groupMap)
{
    for (var propName in groupMap)
    {
        if (! groupMap[propName])
            jQuery("#"+propName).hide("fast");
    }
    for (var propName in groupMap)
    {
        if (groupMap[propName])
            jQuery("#"+propName).show("fast").focus();
    }
}


function onClickChangeVisibility(buttonId, groupMap)
{
    jQuery("#" + buttonId).click(function() {
        changeVisibility(groupMap);
    });
}

var msgTimer = null;

function msg(m, d)
{
    jQuery("#msg").html(m).show();

    clearTimeout(msgTimer);
    if (d > 0)
        setTimeout("rmsg()", d*1000);

}

function rmsg()
{
    clearTimeout(msgTimer);
    jQuery("#msg").hide();
}

function ajaxButtonStart(btn)
{
    btn.attr('disabled', 'disabled');
    var spinner = jQuery("<img class='spinner' src='/static/spinner.gif'/>");
    btn.after(spinner);
    btn.data("spinner", spinner);
}

function ajaxButtonStop(btn)
{
    btn.removeAttr('disabled');
    btn.data("spinner").remove();
}

function disable(expr)
{
    jQuery(expr).attr('disabled', 'disabled');
}

function enable(expr)
{
    jQuery(expr).removeAttr('disabled');
}

