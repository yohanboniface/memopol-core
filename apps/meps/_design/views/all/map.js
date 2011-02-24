function(doc) { 
    emit(doc._id, {
        'id': doc._id, 
        'doc': doc
    }); 
}