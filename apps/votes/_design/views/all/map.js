function(doc) { 
    emit(doc._id, {'label': doc.label, 'wiki': doc.wiki}); 
}