$(document).ready(function() {

    var projection = d3.geo.mercator();
    var path = d3.geo.path().projection(projection);

    var translate = projection.translate();
    translate[0] = 190;
    translate[1] = 735;

    projection.translate(translate);
    projection.scale(410);

    var svg = d3.select("#map")
    .append("svg");

    var countries = svg.append("g")
    .attr("id", "countries");

    d3.json("/static/js/europe.json", function (json) {
    countries.selectAll("path")
        .data(json.features)
        .enter().append("path")
        .attr('class', function (d) { return isEU(d) ? 'eu': 'not_eu';})
        .attr("d", path)
        .on('click', click)
        .append("svg:title")
        .text(function(d) { return d.properties.NAME; });
    });

    var isEU = function (d) {
        var not_EU = [
            'NOR', 'ISL', 'CHE', 'HRV', 'BIH', 'MNE', 'ALB',
            'MKD', 'SRB', 'BLR', 'UKR', 'MDA'
        ];
        return not_EU.indexOf(d.properties.ISO3) === -1;
    };

    var click =  function (d) {
        if (!isEU(d)) { return false; }
        window.location = '/search/?q=country%3A'+ d.properties.ISO2 +' is_active%3A1';
    };

});
