function(doc) {
  var fn=doc.functions;
  for(var i=0; i < fn.length; i++) {
      emit([doc.infos.constituency.country.code, doc.infos.group.abbreviation, fn[i].abbreviation], doc);
  }
}
