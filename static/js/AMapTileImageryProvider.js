
var AMapTileImageryProvider = function AMapTileImageryProvider(description) {
    var trailingSlashRegex = /\/$/;
    var defaultCredit = new Cesium.Credit('AMap');
    description = Cesium.defaultValue(description, {});

    var url = Cesium.defaultValue(description.url, 'http://webrd03.is.autonavi.com/appmaptile');

    this._url = url;
    this._imageType = Cesium.defaultValue(description.imageType, 'amap_map');
    this._fileExtension = Cesium.defaultValue(description.fileExtension, 'png');
    this._proxy = description.proxy;
    this._tileDiscardPolicy = description.tileDiscardPolicy;
    this._queryType = Cesium.defaultValue(description.queryType, 'client');
    this._imageType = Cesium.defaultValue(description.imageType, 'amap_map');

    
    this._tilingScheme = new Cesium.WebMercatorTilingScheme({
        numberOfLevelZeroTilesX : 1,
        numberOfLevelZeroTilesY : 1
    });

    this._tileWidth = 256;
    this._tileHeight = 256;

    this._minimumLevel = Cesium.defaultValue(description.minimumLevel, 0);
    this._maximumLevel = Cesium.defaultValue(description.maximumLevel, 17);
    this._extent = Cesium.defaultValue(description.extent, this._tilingScheme.extent);
    this._rectangle = Cesium.defaultValue(description.rectangle, this._tilingScheme.rectangle);


    this._errorEvent = new Cesium.Event();

    this._ready = true;

    var credit = Cesium.defaultValue(description.credit, defaultCredit);
    if (typeof credit === 'string') {
        credit = new Cesium.Credit(credit);
    }
    this._credit = credit;
};




AMapTileImageryProvider.prototype.buildImageUrl = function(imageryProvider, imageType, x, y, level) {
    var url = imageryProvider._url ;
    //url += '?image_type=' + imageType + '&x=' + x + '&y=' + y + '&level=' + level;
    if(imageryProvider._queryType === 'server')
    {
        url += '?image_type=' + imageryProvider._imageType + '&x=' + x + '&y=' + y + '&level=' + level;
    }else
    {
        url += '?lang=zh_cn&size=1&scale=1&style=7' + '&x=' + x + '&y=' + y + '&z=' + level;
    }
    //console.log("url=" + url);
    var proxy = imageryProvider._proxy;
    if (Cesium.defined(proxy)) {
        url = proxy.getURL(url);
    }
    return url;
}

Cesium.defineProperties(AMapTileImageryProvider.prototype, {
    url : {
        get : function() {
            return this._url;
        }
    },

    proxy : {
        get : function() {
            return this._proxy;
        }
    },

    tileWidth : {
        get : function() {
            if (!this._ready) {
                throw new Cesium.DeveloperError('tileWidth must not be called before the imagery provider is ready.');
            }

            return this._tileWidth;
        }
    },

    tileHeight: {
        get : function() {
            if (!this._ready) {
                throw new Cesium.DeveloperError('tileHeight must not be called before the imagery provider is ready.');
            }

            return this._tileHeight;
        }
    },

    maximumLevel : {
        get : function() {
            if (!this._ready) {
                throw new Cesium.DeveloperError('maximumLevel must not be called before the imagery provider is ready.');
            }
            return this._maximumLevel;
        }
    },

    minimumLevel : {
        get : function() {
            if (!this._ready) {
                throw new Cesium.DeveloperError('minimumLevel must not be called before the imagery provider is ready.');
            }

            return this._minimumLevel;
        }
    },

    tilingScheme : {
        get : function() {
            if (!this._ready) {
                throw new DeveloperError('tilingScheme must not be called before the imagery provider is ready.');
            }
            return this._tilingScheme;
        }
    },

    extent : {
        get : function() {
            if (!this._ready) {
                throw new Cesium.DeveloperError('extent must not be called before the imagery provider is ready.');
            }
            return this._extent;
        }
    },
    rectangle : {
        get : function() {
            if (!this._ready) {
                throw new DeveloperError('rectangle must not be called before the imagery provider is ready.');
            }
            return this._rectangle;
        }
    },

    tileDiscardPolicy : {
        get : function() {
            if (!this._ready) {
                throw new Cesium.DeveloperError('tileDiscardPolicy must not be called before the imagery provider is ready.');
            }
            return this._tileDiscardPolicy;
        }
    },

    errorEvent : {
        get : function() {
            return this._errorEvent;
        }
    },

    ready : {
        get : function() {
            return this._ready;
        }
    },

    credit : {
        get : function() {
            return this._credit;
        }
    }
});

AMapTileImageryProvider.prototype.getTileCredits = function(x, y, level) {
    return undefined;
};

AMapTileImageryProvider.prototype.requestImage = function(x, y, level) {
    if (!this._ready) {
        throw new Cesium.DeveloperError('requestImage must not be called before the imagery provider is ready.');
    }

    var url = AMapTileImageryProvider.prototype.buildImageUrl(this, this._imageType, x, y, level);
    return Cesium.ImageryProvider.loadImage(this, url);
};

