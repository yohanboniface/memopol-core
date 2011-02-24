function(doc) { 
    emit(doc._id, {
        'id': doc._id, 
        'extid': doc.extid,
        'name': doc.infos.name.first+' '+doc.infos.name.last
    }); 
}