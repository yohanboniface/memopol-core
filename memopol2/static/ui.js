jQuery.noConflict();

function changeVisibility(groupMap)
{
    for (var propName in groupMap)
    {
        if (groupMap[propName])
        {
            jQuery("#"+propName).show("fast").focus();
        }
        else
            jQuery("#"+propName).hide("fast");
    }
}


function onClickChangeVisibility(buttonId, groupMap)
{
    jQuery("#" + buttonId).click(function() {
        changeVisibility(groupMap);
    });
}

