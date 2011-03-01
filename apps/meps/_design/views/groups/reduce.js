function(keys, values, rereduce) {
    var total = 0;
    for (index in values) {
        total += values[index].count;
    }
    return {name: values[0].name, count: total, code: values[0].code};
}
