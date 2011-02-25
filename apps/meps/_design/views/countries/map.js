function(doc) { 
    emit(doc.infos.constituency.country.code, { 
        code: doc.infos.constituency.country.code,
        name: doc.infos.constituency.country.name,
        count: 1
    }); 
}
