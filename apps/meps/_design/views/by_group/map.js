function(doc) {
    if (doc && doc.active == "true") {
        emit(doc.infos.group.abbreviation, {
            'id': doc._id,
            'group': doc.infos.group.abbreviation,
            'first': doc.infos.name.first,
            'last': doc.infos.name.last,
            'country_code': doc.infos.constituency.country.code
        });
    }
}
