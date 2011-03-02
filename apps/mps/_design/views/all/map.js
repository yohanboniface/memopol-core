function(doc) {
    emit(doc.infos.name.last, {
        'id': doc._id,
        'extid': doc.extid,
        'last': doc.infos.name.last,
        'first': doc.infos.name.first,
        'group': doc.infos.group.abbreviation
    });
}
