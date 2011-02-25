function(keys, values, rereduce) {
    if (rereduce) {
        return sum(values);
    } else {
        var total = 0;
        for (index in values) {
            total += values[index].count;
        }
        return total;
    }
}
