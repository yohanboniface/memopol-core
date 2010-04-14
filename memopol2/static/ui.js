jQuery.noConflict();


// shortcuts
// -----------------------

function disable(expr)
{
    jQuery(expr).attr('disabled', 'disabled');
}

function enable(expr)
{
    jQuery(expr).removeAttr('disabled');
}

// visibility helpers
// -------------------------------------------


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

// status messages
// --------------------------------

var msgTimer = null;




function msg(m, d, color)
{
    if (! color)
        color = "#FFFECA";
    if (! d)
        d = 3;

    jQuery("#msg").css("background-color", color).html(m).show();

    clearTimeout(msgTimer);
    msgTimer = setTimeout("rmsg()", d*1000);
}

function rmsg()
{
    if (msgTimer)
        clearTimeout(msgTimer);
    else
        alert("no timer");

    jQuery("#msg").hide();
}

// Spinner for ajax calls
// --------------------------------------

function startSpinner(btn)
{
    btn.attr('disabled', 'disabled');
    var spinner = jQuery("<img class='spinner' src='/static/spinner.gif'/>");
    btn.after(spinner);
    btn.data("spinner", spinner);
}

function stopSpinner(btn)
{
    btn.removeAttr('disabled');
    btn.data("spinner").remove();
}

