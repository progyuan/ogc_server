var providerViewModels = [];
providerViewModels.push(new Cesium.ImageryProviderViewModel({
            name : 'WMTS',
            iconUrl : 'img/wmts.png',
            tooltip : 'WMTS',
            creationFunction : function() {
                return new WMTSImageryProvider({
                    url : 'http://localhost:88/wmts',
                });
            }
        }));
providerViewModels.push(new Cesium.ImageryProviderViewModel({
	name : 'Bing Maps Aerial',
	iconUrl : 'img/bingAerial.png',
	tooltip : 'Bing Maps aerial imagery \nhttp://www.bing.com/maps',
	creationFunction : function() {
		return new Cesium.BingMapsImageryProvider({
			url : 'http://dev.virtualearth.net',
			mapStyle : Cesium.BingMapsStyle.AERIAL
			//proxy : proxyIfNeeded
		});
	}
}));

providerViewModels.push(new Cesium.ImageryProviderViewModel({
	name : 'Bing Maps Aerial with Labels',
	iconUrl : 'img/bingAerialLabels.png',
	tooltip : 'Bing Maps aerial imagery with label overlays \nhttp://www.bing.com/maps',
	creationFunction : function() {
		return new Cesium.BingMapsImageryProvider({
			url : 'http://dev.virtualearth.net',
			mapStyle : Cesium.BingMapsStyle.AERIAL_WITH_LABELS
			//proxy : proxyIfNeeded
		});
	}
}));
		
var viewer = new Cesium.Viewer('cesiumContainer',{
	baseLayerPicker:true,
	imageryProviderViewModels:providerViewModels
});
