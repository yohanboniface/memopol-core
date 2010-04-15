function ajax_addPosition(mep_id, contents, cb)
{
    jQuery.getJSON("/mep/" +  mep_id  + "/addposition/", { mep_id: mep_id, text: contents }, function(json){
        cb(json);
    });
}

function ajax_getUnmoderatedPositions(last_id, cb)
{
    jQuery.getJSON("/moderation/get_unmoderated_positions", { last_id: last_id }, function(json) {
        cb(json);
    });
}

function ajax_moderatePosition(pos_id, decision, cb)
{
    jQuery.getJSON("/moderation/moderate_position", { pos_id: pos_id, decision: decision }, function(json) {
        cb(json);
    });
}
