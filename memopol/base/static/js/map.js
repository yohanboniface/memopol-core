$(document).ready(function() {
   $(function() {
        window.map = $K.map('#map');
        map.loadMap('/static/eu.svg', function(map) {
            map
                .addLayer('eu', {"name": 'bgback'})
                .addLayer('eu', {"name": 'bg'})
                .addLayer('eu', {"name": 'bgstroke'})
                .addLayer('countries', {'name': 'context'})
                .addLayer('graticule')
                .addLayer('eu', {
                            title: function(data) {
                                 return data.name;
                            },
                            click: function (data, path, event) {
                              window.location='/europe/parliament/country/'+data.iso2+"/";
                            },
                           'key': "id",
                           "name": "fg"
                          });

            map.addFilter('oglow', 'glow', { size: 3, color: '#988', strength: 1, inner: false });
            map.getLayer('bgback').applyFilter('oglow');

            map.addFilter('myglow', 'glow', { size: 2, color: '#945C1B', inner: true });
            map.getLayer('bg').applyFilter('myglow');
        });
    });
});
