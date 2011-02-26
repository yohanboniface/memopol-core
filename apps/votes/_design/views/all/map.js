function(doc) {
    var d = doc.vote[0].date;
    var datetime = new Date(d.year, d.month, d.day, d.hour, d.minute, d.second);
    var timestamp = datetime.getTime();

    emit(timestamp, {
        'id': doc._id,
        'label': doc.label,
        'wiki': doc.wiki
    });
}
