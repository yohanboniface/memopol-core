function(doc) {
    emit(doc._id, {
        'id': doc._id,
        'extid': doc.extid,
        'last': doc.infos.name.last,
        'first': doc.infos.name.first,
        'infos': doc.infos,
        'doc': doc
    });
}
