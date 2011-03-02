function(doc) {
    emit(doc.infos.name.last, {
        'id': doc._id,
        'extid': doc.extid,
        'name': doc.infos.name.first+' '+doc.infos.name.last
    });
}
