/*global define*/
//define('Scene/HeatMapImageryProvider',[
        //'../Core/defaultValue',
        //'../Core/writeTextToCanvas',
        //'../Core/DeveloperError',
        //'../Core/Extent',
        //'../Core/Math',
        //'./ImageryProvider',
        //'./WebMercatorTilingScheme',
        //'./GeographicTilingScheme',
        //'../ThirdParty/when'
    //], function(
        //defaultValue,
        //writeTextToCanvas,
        //DeveloperError,
        //Extent,
        //CesiumMath,
        //ImageryProvider,
        //WebMercatorTilingScheme,
        //GeographicTilingScheme,
        //when) {
    


var HeatMapPoint = function(option) {
        //var rad = src.radius || this.defaultRadius;
        //var intensity = src.intensity || this.defaultIntensity;
        //var center = src.center;
    if(!option.radius) 
        throw new Cesium.DeveloperError('radius must be specified.');
    if(!option.intensity) 
        throw new Cesium.DeveloperError('intensity must be specified.');
    if(!option.center) 
        throw new Cesium.DeveloperError('center must be specified.');
    this._center = option.center;
    this._intensity = option.intensity;
    this._radius = option.radius;

};

Cesium.defineProperties(HeatMapPoint.prototype, {
    radius : {
        get : function() {
            return this._radius;
        }
    },
    intensity : {
        get : function() {
            return this._intensity;
        }
    },
    center : {
        get : function() {
            return this._center;
        }
    }
});


var HeatMapImageryProvider = function(description) {
    description = Cesium.defaultValue(description, {});

    this._tileWidth = 2048;
    this._tileHeight = 1024;
    this._maximumLevel = 0;
    this._rectangle = Cesium.Rectangle.MAX_VALUE;
                                 
    this._tilingScheme = new Cesium.GeographicTilingScheme({
        numberOfLevelZeroTilesX : 1,
        numberOfLevelZeroTilesY : 1
    });
    //this._logo = undefined;
    this._ready = true;
    this.canvas = document.createElement("canvas");
    this.canvas.width = this._tileWidth;
    this.canvas.height = this._tileHeight;
    this.points = [];
    this.cache = {};
    this.defaultRadius = 20;
    this.defaultIntensity = 0.2;
    this.gradientStops = {
      '0.00': 0xffffff00,
      '0.33': 0x00ff00ff, //green
      '0.66': 0xffff00ff, //yellow
      '1.00': 0xff0000ff  //red
    };
    var gradients = description.gradientStops || this.gradientStops;
    this.setGradientStops(gradients);
};


//HeatMapImageryProvider.prototype.getUrl = function() {
    //return this._url;
//};

///**
 //* Gets the width of each tile, in pixels.
 //*
 //* @returns {Number} The width.
 //*/
//HeatMapImageryProvider.prototype.getTileWidth = function() {
    //return this._tileWidth;
//};

///**
 //* Gets the height of each tile, in pixels.
 //*
 //* @returns {Number} The height.
 //*/
//HeatMapImageryProvider.prototype.getTileHeight = function() {
    //return this._tileHeight;
//};

///**
 //* Gets the maximum level-of-detail that can be requested.
 //*
 //* @returns {Number} The maximum level.
 //*/
//HeatMapImageryProvider.prototype.getMaximumLevel = function() {
    //return this._maximumLevel;
//};

///**
 //* Gets the tiling scheme used by this provider.
 //*
 //* @returns {TilingScheme} The tiling scheme.
 //* @see WebMercatorTilingScheme
 //* @see GeographicTilingScheme
 //*/
//HeatMapImageryProvider.prototype.getTilingScheme = function() {
    //return this._tilingScheme;
//};

///**
 //* Gets the extent, in radians, of the imagery provided by this instance.
 //*
 //* @returns {Extent} The extent.
 //*/
//HeatMapImageryProvider.prototype.getRectangle = function() {
    //return this._tilingScheme.rectangle;
//};

///**
 //* Gets the tile discard pHeatMapicy.  If not undefined, the discard pHeatMapicy is responsible
 //* for filtering out "missing" tiles via its shouldDiscardImage function.
 //* By default, no tiles will be filtered.
 //*
 //* @returns {TileDiscardPHeatMapicy} The discard pHeatMapicy.
 //*/
//HeatMapImageryProvider.prototype.getTileDiscardPHeatMapicy = function() {
    //return this._tileDiscardPHeatMapicy;
//};

///**
 //* Gets a value indicating whether or not the provider is ready for use.
 //*
 //* @returns {BoHeatMapean} True if the provider is ready to use; otherwise, false.
 //*/
//HeatMapImageryProvider.prototype.isReady = function() {
    //return this._ready;
//};

/**
 * Requests the image for a given tile.
 *
 * @param {Number} x The tile X coordinate.
 * @param {Number} y The tile Y coordinate.
 * @param {Number} level The tile level.
 *
 * @return {Promise} A promise for the image that will resHeatMapve when the image is available, or
 *         undefined if there are too many active requests to the server, and the request
 *         should be retried later.  If the resulting image is not suitable for display,
 *         the promise can resHeatMapve to undefined.  The resHeatMapved image may be either an
 *         Image or a Canvas DOM object.
 */
HeatMapImageryProvider.prototype.requestImage = function(x, y, level) {
    var that = this;
    return Cesium.when(true, function() {
        return that.canvas;
    });
};

///**
 //* DOC_TBA
 //* @memberof HeatMapImageryProvider
 //*/
//HeatMapImageryProvider.prototype.getLogo = function() {
    //return this._logo;
//};

HeatMapImageryProvider.prototype.setGradientStops = function(stops) {

    // There is no need to perform the linear interpolation manually,
    // it is sufficient to let the canvas implementation do that.

    var ctx = document.createElement('canvas').getContext('2d');
    var grd = ctx.createLinearGradient(0, 0, 256, 0);

    for (var i in stops) {
      grd.addColorStop(i, 'rgba(' +
        ((stops[i] >> 24) & 0xFF) + ',' +
        ((stops[i] >> 16) & 0xFF) + ',' +
        ((stops[i] >>  8) & 0xFF) + ',' +
        ((stops[i] >>  0) & 0xFF) + ')');
    }

    ctx.fillStyle = grd;
    ctx.fillRect(0, 0, 256, 1);
    this.gradient = ctx.getImageData(0, 0, 256, 1).data;
  };

HeatMapImageryProvider.prototype.drawHeatMap = function(ellipsoid, points) {
    var ctx = this.canvas.getContext('2d');
    ctx.clearRect (0, 0, this.canvas.width, this.canvas.height);

    if(points === undefined) return;
    this.points = points;
    for (var i = 0; i < this.points.length; i++) 
    {
        var src = this.points[i];
        //if (!src.geometry)
        //{
            //continue;
        //}
        var rad = src.radius || this.defaultRadius;
        var intensity = src.intensity || this.defaultIntensity;
        var carto = src.center;
        //var carto = ellipsoid.cartesianToCartographic(src.center);
        //var pos = this.getPxFromLonLat(new OpenLayers.LonLat(center.x,center.y));
        var pos = this.getPxFromLonLat(ellipsoid, carto);
        //console.log(pos);
        if(!pos) continue;
        var x = pos.x - rad;
        var y = pos.y - rad;
    
        if (!this.cache[intensity]) 
        {
            this.cache[intensity] = {};
        }
    
        if (!this.cache[intensity][rad]) 
        {
            var grd = ctx.createRadialGradient(rad, rad, 0, rad, rad, rad);
            grd.addColorStop(0.0, 'rgba(0, 0, 0, ' + intensity + ')');
            grd.addColorStop(1.0, 'transparent');
            this.cache[intensity][rad] = grd;
        }
    
        ctx.fillStyle = this.cache[intensity][rad];
        ctx.translate(x, y);
        ctx.fillRect(0, 0, 2 * rad, 2 * rad);
        ctx.translate(-x, -y);
    }
    
    var dat = ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
    var dim = this.canvas.width * this.canvas.height * 4;
    var pix = dat.data;
    
    for (var p = 0; p < dim; /* */) 
    {
        var a = pix[ p + 3 ] * 4;
        pix[ p++ ] = this.gradient[ a++ ];
        pix[ p++ ] = this.gradient[ a++ ];
        pix[ p++ ] = this.gradient[ a++ ];
        pix[ p++ ] = this.gradient[ a++ ];
    }
    ctx.putImageData(dat, 0, 0);
};
HeatMapImageryProvider.prototype.getPxFromLonLat = function(ellipsoid, carto){
    var px;
    var halfw = this.canvas.width/2;
    var halfh = this.canvas.height/2;
    var sLat = Cesium.Math.toDegrees(this.rectangle.south);
    var eLon = Cesium.Math.toDegrees(this.rectangle.east);
    var nLat = Cesium.Math.toDegrees(this.rectangle.north);
    var wLon = Cesium.Math.toDegrees(this.rectangle.west);
    if (carto) 
    {
        //Handle points displayed when camera is over IDL.
        //This code gives correct pixel values but points still are sometimes not visible on globe.
        //Probably an issue with Globe.js when setting a _tilingScheme._extent that spans the IDL.
        if(wLon < -180 && Cesium.Math.toDegrees(carto.longitude) > 0){ //handle points west of dateline
           wLon+=360;
           eLon+=360;
        }else if(wLon > 0 && Cesium.Math.toDegrees(carto.longitude) < 0 ){ //handle points east of dateline
           carto.longitude += Cesium.Math.toRadians(360);
        }
        //px = new OpenLayers.Pixel(
        px = {
            x:(halfw * (Cesium.Math.toDegrees(carto.longitude)-wLon)) / ((eLon-wLon)/2),
            y:(halfh * (Cesium.Math.toDegrees(carto.latitude)-nLat)) / (-((nLat-sLat)/2))
        };
    }
    return px;
};

    //return HeatMapImageryProvider;
//});


Cesium.defineProperties(HeatMapImageryProvider.prototype, {
    url : {
        get : function() {
            return this._url;
        }
    },

    /**
     * Gets the proxy used by this provider.
     * @memberof BingImageryFromServerProvider.prototype
     * @type {Proxy}
     */
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
            return 0;
        }
    },

    tilingScheme : {
        get : function() {
            if (!this._ready) {
                throw new Cesium.DeveloperError('tilingScheme must not be called before the imagery provider is ready.');
            }
            return this._tilingScheme;
        }
    },

    rectangle : {
        get : function() {
            if (!this._ready) {
                throw new Cesium.DeveloperError('rectangle must not be called before the imagery provider is ready.');
            }
            return this._tilingScheme.rectangle;
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
    },

    hasAlphaChannel : {
        get : function() {
            return false;
        }
    }
});


