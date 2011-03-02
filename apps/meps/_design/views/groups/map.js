function(doc) { 
   if(doc.active) {
    emit(doc.infos.group.abbreviation, { 
        code: doc.infos.group.abbreviation,
        name: doc.infos.group.name,
        count: 1
    }); 
   }
}
