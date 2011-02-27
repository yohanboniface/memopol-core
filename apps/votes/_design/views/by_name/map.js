function(doc) {
    emit(doc.wiki, {
        '_id': doc._id,
        'label': doc.label,
        'wiki': doc.wiki,
        'doc': doc
    });
}
