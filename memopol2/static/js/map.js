$(document).ready(function() {
   var onCountryClick = function(target) {
      window.location='/europe/parliament/country/'+target.iso2+"/";
   };
   $(function() {
        window.map = $K.map('#map');
        map.loadMap('/static/eu.svg', function(map) {
            map
                .addLayer('eu', 'bgback')
                .addLayer('eu', 'bg')
                .addLayer('eu', 'bgstroke')
                .addLayer({'id': 'countries', 'className': 'context'})
                .addLayer('graticule')
                .addLayer({'id': 'eu',
                           'className': 'fg',
                           'tooltip': {
                              content: function(obj,foo) {
                                 return foo.data.name;
                              }
                           },
                           'key': "id"
                          });

            map.onLayerEvent('click', onCountryClick, 'fg')

            map.addFilter('oglow', 'glow', { size: 3, color: '#988', strength: 1, inner: false });
            map.getLayer('bgback').applyFilter('oglow');

            map.addFilter('myglow', 'glow', { size: 2, color: '#945C1B', inner: true });
            map.getLayer('bg').applyFilter('myglow');
        });
    });
});
