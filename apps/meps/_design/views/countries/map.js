function(doc) { 
    emit(doc.infos.constituency.country.name, { 
        name: doc.infos.constituency.country.name,
        code: doc.infos.constituency.country.code,
        count: 1
    }); 
}
