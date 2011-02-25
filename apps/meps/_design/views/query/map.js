function(doc) {
  var fn=doc.functions;
  for(var i=0; i < fn.length; i++) {
      emit([doc.country.code, doc.group, fn[i].abbreviation], doc);
  }
}
