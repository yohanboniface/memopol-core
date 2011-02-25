function(doc) {
    emit(doc._id, {
        'id': doc._id,
        'group': doc.infos.group.abbreviation,
        'first': doc.infos.name.first,
        'last': doc.infos.name.last
    });
}
