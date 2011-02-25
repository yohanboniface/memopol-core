function(doc) {
  var fn=doc.functions;
  for(var i=0; i < fn.length; i++) {
    if (fn[i].role=="Membre") {
      emit(fn[i].abbreviation, fn[i].label);
    }
  }
}
