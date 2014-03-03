//define([
        //'../Core/defaultValue',
        //'../Core/defined',
        //'../Core/jsonp',
        //'../Core/Cartesian2',
        //'../Core/Cartographic',
        //'../Core/DeveloperError',
        //'../Core/Event',
        //'../Core/loadXML',
        //'../Core/writeTextToCanvas',
        //'../Core/Extent',
        //'./DiscardMissingTileImagePolicy',
        //'./ImageryProvider',
        //'./TileProviderError',
        //'./WebMercatorTilingScheme',
        //'./Credit',
        //'../ThirdParty/when'
    //], function(
        //defaultValue,
        //defined,
        //jsonp,
        //Cartesian2,
        //Cartographic,
        //DeveloperError,
        //Event,
        //loadXML,
        //writeTextToCanvas,
        //Extent,
        //DiscardMissingTileImagePolicy,
        //ImageryProvider,
        //TileProviderError,
        //WebMercatorTilingScheme,
        //Credit,
        //when) {
    //"use strict";

/*
var WMTSImageryProvider = function WMTSImageryProvider(description) {
    description = Cesium.defaultValue(description, {});

    if (!Cesium.defined(description.url)) {
        throw new Cesium.DeveloperError('description.url is required.');
    }

    this._tilematrix = new Array();
    this._url = description.url;
    this._tileDiscardPolicy = description.tileDiscardPolicy;
    this._proxy = description.proxy;

    this.defaultGamma = 1.0;

    this._tilingScheme = new Cesium.WebMercatorTilingScheme({
        numberOfLevelZeroTilesX : 2,
        numberOfLevelZeroTilesY : 2
    });

    this._tileWidth = undefined;
    this._tileHeight = undefined;
    this._maximumLevel = undefined;
    this._imageUrlTemplate = undefined;
    this._imageUrlSubdomains = undefined;

    this._errorEvent = new Cesium.Event();

    this._ready = false;
    
    
    this._logo = Cesium.writeTextToCanvas("kamijawa@gmail.com", {
            font : '24px sans-serif'
        });
    this._credit = new Cesium.Credit('WMTS', this._logo, 'http://www.wmts.com');
    

    var that = this;
    var metadataError;
        
    Cesium.loadXML(this._url + '?SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetCapabilities').then(function(xml) {
       var format = xml.getElementsByTagName('Format')[0];
       that._format = format.textContent;
       var fmtstr =  format.textContent.substring(format.textContent.indexOf('/')+1);
       that._fileExtension = Cesium.defaultValue(description.fileExtension, fmtstr);
   
       var tw0 = parseFloat(xml.getElementsByTagName('TileWidth')[0].textContent);
       var th0 = parseFloat(xml.getElementsByTagName('TileHeight')[0].textContent);
   
       that._tileWidth = Cesium.defaultValue(description.tileWidth, tw0, 10);
       that._tileHeight = Cesium.defaultValue(description.tileHeight, th0, 10);
       var tilesets = xml.getElementsByTagName('TileMatrix');
       that._maximumLevel = Cesium.defaultValue(description.maximumLevel, tilesets.length, 10);
           
           
           
       if (!Cesium.defined(that._tileDiscardPolicy)) {
           that._tileDiscardPolicy = new Cesium.DiscardMissingTileImagePolicy({
               missingImageUrl : buildImageUrl(that, 0, 0, that._maximumLevel),
               pixelsToCheck : [new Cesium.Cartesian2(0, 0), new Cesium.Cartesian2(120, 140), new Cesium.Cartesian2(130, 160), new Cesium.Cartesian2(200, 50), new Cesium.Cartesian2(200, 200)],
               disableCheckIfAllPixelsAreTransparent : true
           });
       }
           
           
   
       var tmsl = xml.getElementsByTagName('TileMatrixSetLink')[0];
       for(var i in tmsl.childNodes)
       {
           if(tmsl.childNodes[i].tagName=='TileMatrixSet')
           {
               that._tilematrixset =  tmsl.childNodes[i].textContent;
           }
       }
   
       var foundtilematrixset = false;
       var content = xml.getElementsByTagName('Contents')[0];
       for(var i in content.childNodes)
       {
           if(content.childNodes[i].tagName=='TileMatrixSet')
           {
               var TileMatrixSet = content.childNodes[i];
               for(var j in TileMatrixSet.childNodes)
               {
                   var cn = TileMatrixSet.childNodes[j];
                   if (cn.tagName=='ows:Identifier')
                   {
                       if(cn.textContent==that._tilematrixset)
                       {
                           foundtilematrixset = true;
                       }
                   }
                   if(foundtilematrixset)
                   {
                       if (cn.tagName=='TileMatrix')
                       {
                           for(var k in cn.childNodes)
                           {
                               var tm = cn.childNodes[k];
                               if (tm.tagName=='ows:Identifier')
                               {
                                   that._tilematrix.push(tm.textContent);
                                   break;
                               }
                           }
                       }
                   }
               }
               break;
           }
       }
   
       var layer = xml.getElementsByTagName('Layer')[0];
       for(var i in layer.childNodes)
       {
           if(layer.childNodes[i].tagName=='ows:Identifier')
           {
               that._layer = layer.childNodes[i].textContent;
           }
           if(layer.childNodes[i].tagName=='Style')
           {
               for(var j in layer.childNodes[i].childNodes)
               {
                   if(layer.childNodes[i].childNodes[j].tagName=='ows:Identifier')
                   {
                       that._style = layer.childNodes[i].childNodes[j].textContent;
                       break;
                   }
               }
           }
       }
   
       that._extent = description.extent;
       if (typeof that._extent === 'undefined') {
           var LowerCornerStr = xml.getElementsByTagName('LowerCorner')[0];
           var sw_lgt_lat =  LowerCornerStr.textContent.split(' ');
           var sw_lgt = parseFloat(sw_lgt_lat[0]);
           var sw_lat = parseFloat(sw_lgt_lat[1]);
           var sw = Cesium.Cartographic.fromDegrees(sw_lat, sw_lgt);
       
           var UpperCornerStr = xml.getElementsByTagName('UpperCorner')[0];
           var ne_lgt_lat =  UpperCornerStr.textContent.split(' ');
           var ne_lgt = parseFloat(ne_lgt_lat[0]);
           var ne_lat = parseFloat(ne_lgt_lat[1]);
           var ne = Cesium.Cartographic.fromDegrees(ne_lat, ne_lgt);
       
           that._extent = new Cesium.Extent(sw.longitude, sw.latitude, ne.longitude, ne.latitude);
           that._extent = Cesium.Extent.MAX_VALUE.clone();
       } else {
           that._extent = that._extent.clone();
       }
   
       var tilingScheme = new Cesium.WebMercatorTilingScheme({
           numberOfLevelZeroTilesX:1,
           numberOfLevelZeroTilesY:1
       });
   
   
       if (that._extent.west < tilingScheme.getExtent().west) {
           that._extent.west = tilingScheme.getExtent().west;
       }
       if (that._extent.east > tilingScheme.getExtent().east) {
           that._extent.east = tilingScheme.getExtent().east;
       }
       if (that._extent.south < tilingScheme.getExtent().south) {
           that._extent.south = tilingScheme.getExtent().south;
       }
       if (that._extent.north > tilingScheme.getExtent().north) {
           that._extent.north = tilingScheme.getExtent().north;
       }
   
       that._tilingScheme = tilingScheme;
   
       if(typeof that._layer === 'undefined')
       {
           that._layer = Cesium.defaultValue(description.layer, null);
       }
       if(typeof that._tilematrixset === 'undefined')
       {
           that._tilematrixset = Cesium.defaultValue(description.tilematrixset, null);
       }
       if(typeof that._style === 'undefined')
       {
           that._style = Cesium.defaultValue(description.style, 'default');
       }
       if(typeof that._format === 'undefined')
       {
           that._format = Cesium.defaultValue(description.format, 'image/png');
       }
   
   

       that._ready = true;
   }, function(error) {
        that._fileExtension = Cesium.defaultValue(description.fileExtension, 'png');
        that._tileWidth = Cesium.defaultValue(description.tileWidth, 256);
        that._tileHeight = Cesium.defaultValue(description.tileHeight, 256);
        that._minimumLevel = Cesium.defaultValue(description.minimumLevel, 0);
        that._maximumLevel = Cesium.defaultValue(description.maximumLevel, 18);
        that._tilingScheme = Cesium.defaultValue(description.tilingScheme, new Cesium.WebMercatorTilingScheme());
        that._extent = Cesium.defaultValue(description.extent, that._tilingScheme.getExtent());
        that._ready = false;
        if(typeof that._layer === 'undefined')
        {
            that._layer = Cesium.defaultValue(description.layer, null);
        }
        if(typeof that._tilematrixset === 'undefined')
        {
            that._tilematrixset = Cesium.defaultValue(description.tilematrixset, null);
        }
        if(typeof that._style === 'undefined')
        {
            that._style = Cesium.defaultValue(description.style, 'default');
        }
        if(typeof that._format === 'undefined')
        {
            that._format = Cesium.defaultValue(description.format, 'image/png');
        }
    });

};
   

WMTSImageryProvider.prototype.getUrl = function() {
    return this._url;
};

WMTSImageryProvider.prototype.getProxy = function() {
    return this._proxy;
};

WMTSImageryProvider.prototype.getKey = function() {
    return this._key;
};

WMTSImageryProvider.prototype.getMapStyle = function() {
    return this._mapStyle;
};

WMTSImageryProvider.prototype.getTileWidth = function() {
    if (!this._ready) {
        throw new Cesium.DeveloperError('getTileWidth must not be called before the imagery provider is ready.');
    }
    return this._tileWidth;
};

WMTSImageryProvider.prototype.getTileHeight = function() {
    if (!this._ready) {
        throw new Cesium.DeveloperError('getTileHeight must not be called before the imagery provider is ready.');
    }
    return this._tileHeight;
};

WMTSImageryProvider.prototype.getMaximumLevel = function() {
    if (!this._ready) {
        throw new Cesium.DeveloperError('getMaximumLevel must not be called before the imagery provider is ready.');
    }
    return this._maximumLevel;
};

WMTSImageryProvider.prototype.getMinimumLevel = function() {
    if (!this._ready) {
        throw new Cesium.DeveloperError('getMinimumLevel must not be called before the imagery provider is ready.');
    }
    return 0;
};

WMTSImageryProvider.prototype.getTilingScheme = function() {
    if (!this._ready) {
        throw new Cesium.DeveloperError('getTilingScheme must not be called before the imagery provider is ready.');
    }
    return this._tilingScheme;
};

WMTSImageryProvider.prototype.getExtent = function() {
    if (!this._ready) {
        throw new Cesium.DeveloperError('getExtent must not be called before the imagery provider is ready.');
    }
    return this._tilingScheme.getExtent();
};

WMTSImageryProvider.prototype.getTileDiscardPolicy = function() {
    if (!this._ready) {
        throw new Cesium.DeveloperError('getTileDiscardPolicy must not be called before the imagery provider is ready.');
    }
    return this._tileDiscardPolicy;
};

WMTSImageryProvider.prototype.getErrorEvent = function() {
    return this._errorEvent;
};

WMTSImageryProvider.prototype.isReady = function() {
    return this._ready;
};

WMTSImageryProvider.prototype.requestImage = function(x, y, level) {
    if (!this._ready) {
        throw new Cesium.DeveloperError('requestImage must not be called before the imagery provider is ready.');
    }
    var url = buildImageUrl(this, x, y, level);
    console.log("url=" + url);
    return Cesium.ImageryProvider.loadImage(this, url);
};

WMTSImageryProvider.prototype.getCredit = function() {
    return this._credit;
};



function buildImageUrl(imageryProvider, x, y, level) {

    var TILEMATRIX = imageryProvider._tilematrix[level];
    if(typeof TILEMATRIX == 'undefined')
    {
        TILEMATRIX = imageryProvider._tilematrix[imageryProvider._tilematrix.length-1];
    }

    var url = imageryProvider._url ;
    url += '?SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile';
    url += '&LAYER=' + imageryProvider._layer;
    url += '&STYLE=' + imageryProvider._style;
    url += '&TILEMATRIXSET=' + imageryProvider._tilematrixset;
    url += '&TILEMATRIX=' + TILEMATRIX;
    url += '&TILEROW=' + y;
    url += '&TILECOL=' + x;
    url += '&FORMAT=' + encodeURIComponent(imageryProvider._format);

    var proxy = imageryProvider._proxy;
    if (typeof proxy !== 'undefined') {
        url = proxy.getURL(url);
    }
    return url;
}


*/

var WMTSImageryProvider = function WMTSImageryProvider(description) {
    var trailingSlashRegex = /\/$/;
    var defaultCredit = new Cesium.Credit('WMTS');
    description = Cesium.defaultValue(description, {});

    var url = Cesium.defaultValue(description.url, 'http://localhost:88/wmts');
    if (!trailingSlashRegex.test(url)) {
        //url = url + '/';
    }

    this._url = url;
    this._fileExtension = Cesium.defaultValue(description.fileExtension, 'png');
    this._proxy = description.proxy;
    this._tileDiscardPolicy = description.tileDiscardPolicy;

    
    this._tilingScheme = new Cesium.WebMercatorTilingScheme({
        numberOfLevelZeroTilesX : 2,
        numberOfLevelZeroTilesY : 2
    });

    this._tileWidth = 256;
    this._tileHeight = 256;

    this._minimumLevel = Cesium.defaultValue(description.minimumLevel, 0);
    this._maximumLevel = Cesium.defaultValue(description.maximumLevel, 18);

    this._extent = Cesium.defaultValue(description.extent, this._tilingScheme.extent);

    // Check the number of tiles at the minimum level.  If it's more than four,
    // throw an exception, because starting at the higher minimum
    // level will cause too many tiles to be downloaded and rendered.
    var swTile = this._tilingScheme.positionToTileXY(this._extent.getSouthwest(), this._minimumLevel);
    var neTile = this._tilingScheme.positionToTileXY(this._extent.getNortheast(), this._minimumLevel);
    var tileCount = (Math.abs(neTile.x - swTile.x) + 1) * (Math.abs(neTile.y - swTile.y) + 1);
    if (tileCount > 4) {
        throw new Cesium.DeveloperError('The imagery provider\'s extent and minimumLevel indicate that there are ' + tileCount + ' tiles at the minimum level. Imagery providers with more than four tiles at the minimum level are not supported.');
    }

    this._errorEvent = new Cesium.Event();

    this._ready = true;

    var credit = Cesium.defaultValue(description.credit, defaultCredit);
    if (typeof credit === 'string') {
        credit = new Cesium.Credit(credit);
    }
    this._credit = credit;
};

function buildImageUrl(imageryProvider, x, y, level) {
    //var url = imageryProvider._url + level + '/' + x + '/' + y + '.' + imageryProvider._fileExtension;
    var url = imageryProvider._url ;
    url += '?SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile';
    url += '&LAYER=' + '';
    url += '&STYLE=' + '';
    url += '&TILEMATRIXSET=' + 'sat_tiles';
    url += '&TILEMATRIX=' + level;
    url += '&TILEROW=' + y;
    url += '&TILECOL=' + x;
    url += '&FORMAT=' + imageryProvider._fileExtension;
    console.log("url=" + url);
    var proxy = imageryProvider._proxy;
    if (Cesium.defined(proxy)) {
        url = proxy.getURL(url);
    }
    return url;
}

Cesium.defineProperties(WMTSImageryProvider.prototype, {
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

WMTSImageryProvider.prototype.getTileCredits = function(x, y, level) {
    return undefined;
};

WMTSImageryProvider.prototype.requestImage = function(x, y, level) {
    if (!this._ready) {
        throw new Cesium.DeveloperError('requestImage must not be called before the imagery provider is ready.');
    }

    var url = buildImageUrl(this, x, y, level);
    return Cesium.ImageryProvider.loadImage(this, url);
};

