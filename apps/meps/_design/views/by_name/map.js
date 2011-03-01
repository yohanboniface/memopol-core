function(doc) {
    if (doc && doc.active == "true") {
        emit(doc.infos.name.last, {
            'id': doc._id,
            'group': doc.infos.group.abbreviation,
            'first': doc.infos.name.first,
            'last': doc.infos.name.last,
            'email': doc.contact.email.text,
            'scores': doc.scores
        });
    }
}
