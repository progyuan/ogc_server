var HeightmapAndQuantizedMeshTerrainProvider = function HeightmapAndQuantizedMeshTerrainProvider(options) {
            if (!Cesium.defined(options) || !Cesium.defined(options.url)) {
        throw new Cesium.DeveloperError('options.url is required.');
    }
    
    this._url = options.url;
    if (this._url.length === 0 || this._url[this._url.length - 1] !== '/') {
        this._url = this._url + '/';
    }
    this._proxy = options.proxy;

    this._terrain_type = Cesium.defaultValue( options.terrain_type, 'quantized_mesh');
    this._tilingScheme = new Cesium.GeographicTilingScheme({
        numberOfLevelZeroTilesX : 2,
        numberOfLevelZeroTilesY : 1
    });

    this._heightmapWidth = 65;
    this._levelZeroMaximumGeometricError = Cesium.TerrainProvider.getEstimatedLevelZeroGeometricErrorForAHeightmap(this._tilingScheme.ellipsoid, this._heightmapWidth, this._tilingScheme.getNumberOfXTilesAtLevel(0));

    this._heightmapStructure = undefined;
    this._hasWaterMask = false;

    this._errorEvent = new Cesium.Event();

    var credit = options.credit;
    if (typeof credit === 'string') {
        credit = new Cesium.Credit(credit);
    }
    this._credit = credit;

    this._ready = false;

    var metadataUrl = this._url + 'layer.json' + '?terrain_type=' + this._terrain_type;
    if (Cesium.defined(this._proxy)) {
        metadataUrl = this._proxy.getURL(metadataUrl);
    }

    var that = this;
    var metadataError;

    function metadataSuccess(data) {
        var message;

        if (!data.format) {
            message = 'The tile format is not specified in the layer.json file.';
            metadataError = Cesium.TileProviderError.handleError(metadataError, that, that._errorEvent, message, undefined, undefined, undefined, requestMetadata);
            return;
        }

        if (!data.tiles || data.tiles.length === 0) {
            message = 'The layer.json file does not specify any tile URL templates.';
            metadataError = Cesium.TileProviderError.handleError(metadataError, that, that._errorEvent, message, undefined, undefined, undefined, requestMetadata);
            return;
        }

        if (data.format === 'heightmap-1.0') {
            that._heightmapStructure = {
                    heightScale : 1.0 / 5.0,
                    heightOffset : -1000.0,
                    elementsPerHeight : 1,
                    stride : 1,
                    elementMultiplier : 256.0,
                    isBigEndian : false
                };
            that._hasWaterMask = true;
        } else if (data.format === 'quantized-mesh-1.0') {
            that._hasWaterMask = false;
        } else {
            message = 'The tile format "' + data.format + '" is invalid or not supported.';
            metadataError = Cesium.TileProviderError.handleError(metadataError, that, that._errorEvent, message, undefined, undefined, undefined, requestMetadata);
            return;
        }

        var baseUri = new Cesium.Uri(metadataUrl);

        that._tileUrlTemplates = data.tiles;
        for (var i = 0; i < that._tileUrlTemplates.length; ++i) {
            that._tileUrlTemplates[i] = new Cesium.Uri(that._tileUrlTemplates[i] + '&terrain_type=' + that._terrain_type ).resolve(baseUri).toString().replace('{version}', data.version);
        }

        that._availableTiles = data.available;

        if (!Cesium.defined(that._credit) && Cesium.defined(data.attribution) && data.attribution !== null) {
            that._credit = new Cesium.Credit(data.attribution);
        }

        that._ready = true;
    }

    function metadataFailure(data) {
        if (Cesium.defined(data) && data.statusCode === 404) {
            metadataSuccess({
                tilejson: '2.1.0',
                format : 'heightmap-1.0',
                version : '1.0.0',
                scheme : 'tms',
                tiles : [
                    '{z}/{x}/{y}.terrain?v={version}&terrain_type=' + that._terrain_type
                ]
            });
            return;
        }
        var message = 'An error occurred while accessing ' + metadataUrl + '.';
        metadataError = Cesium.TileProviderError.handleError(metadataError, that, that._errorEvent, message, undefined, undefined, undefined, requestMetadata);
    }

    function requestMetadata() {
        var metadata = Cesium.loadJson(metadataUrl);
        Cesium.when(metadata, metadataSuccess, metadataFailure);
    }

    requestMetadata();
};

var requestHeaders = {
    Accept : 'application/octet-stream,*/*;q=0.01'
    //Accept : 'application/octet-stream'
};

function loadTile(url) {
    //console.log('loadTile=' + url);
    return Cesium.loadArrayBuffer(url, requestHeaders);
}

function createHeightmapTerrainData(provider, buffer, level, x, y, tmsY) {
    var heightBuffer = new Uint16Array(buffer, 0, provider._heightmapWidth * provider._heightmapWidth);
    return new Cesium.HeightmapTerrainData({
        buffer : heightBuffer,
        childTileMask : new Uint8Array(buffer, heightBuffer.byteLength, 1)[0],
        waterMask : new Uint8Array(buffer, heightBuffer.byteLength + 1, buffer.byteLength - heightBuffer.byteLength - 1),
        width : provider._heightmapWidth,
        height : provider._heightmapWidth,
        structure : provider._heightmapStructure
    });
}

function createQuantizedMeshTerrainData(provider, buffer, level, x, y, tmsY) {
    var pos = 0;
    var uint16Length = 2;
    var uint32Length = 4;
    var float32Length = 4;
    var float64Length = 8;
    var cartesian3Elements = 3;
    var boundingSphereElements = cartesian3Elements + 1;
    var cartesian3Length = float64Length * cartesian3Elements;
    var boundingSphereLength = float64Length * boundingSphereElements;
    var vertexElements = 6;
    var encodedVertexElements = 3;
    var encodedVertexLength = uint16Length * encodedVertexElements;
    var triangleElements = 3;
    var triangleLength = uint16Length * triangleElements;

    var view = new DataView(buffer);
    var center = new Cesium.Cartesian3(view.getFloat64(pos, true), view.getFloat64(pos + 8, true), view.getFloat64(pos + 16, true));
    pos += cartesian3Length;

    var minimumHeight = view.getFloat32(pos, true);
    pos += float32Length;
    var maximumHeight = view.getFloat32(pos, true);
    pos += float32Length;

    var boundingSphere = new Cesium.BoundingSphere(
            new Cesium.Cartesian3(view.getFloat64(pos, true), view.getFloat64(pos + 8, true), view.getFloat64(pos + 16, true)),
            view.getFloat64(pos + cartesian3Length, true));
    pos += boundingSphereLength;

    var horizonOcclusionPoint = new Cesium.Cartesian3(view.getFloat64(pos, true), view.getFloat64(pos + 8, true), view.getFloat64(pos + 16, true));
    pos += cartesian3Length;

    var vertexCount = view.getUint32(pos, true);
    pos += uint32Length;
    var encodedVertexBuffer = new Uint16Array(buffer, pos, vertexCount * 3);
    pos += vertexCount * encodedVertexLength;

    if (vertexCount > 64 * 1024) {
        // More than 64k vertices, so indices are 32-bit.  Not supported right now.
        throw new Cesium.RuntimeError('HeightmapAndQuantizedMeshTerrainProvider currently does not support tiles with more than 65536 vertices.');
    }

    // Decode the vertex buffer.
    var uBuffer = encodedVertexBuffer.subarray(0, vertexCount);
    var vBuffer = encodedVertexBuffer.subarray(vertexCount, 2 * vertexCount);
    var heightBuffer = encodedVertexBuffer.subarray(vertexCount * 2, 3 * vertexCount);

    var i;
    var u = 0;
    var v = 0;
    var height = 0;

    function zigZagDecode(value) {
        return (value >> 1) ^ (-(value & 1));
    }

    for (i = 0; i < vertexCount; ++i) {
        u += zigZagDecode(uBuffer[i]);
        v += zigZagDecode(vBuffer[i]);
        height += zigZagDecode(heightBuffer[i]);

        uBuffer[i] = u;
        vBuffer[i] = v;
        heightBuffer[i] = height;
    }

    var triangleCount = view.getUint32(pos, true);
    pos += uint32Length;
    var indices = new Uint16Array(buffer, pos, triangleCount * triangleElements);
    pos += triangleCount * triangleLength;

    // High water mark decoding based on decompressIndices_ in webgl-loader's loader.js.
    // https://code.google.com/p/webgl-loader/source/browse/trunk/samples/loader.js?r=99#55
    // Copyright 2012 Google Inc., Apache 2.0 license.
    var highest = 0;
    for (i = 0; i < indices.length; ++i) {
        var code = indices[i];
        indices[i] = highest - code;
        if (code === 0) {
            ++highest;
        }
    }

    var westVertexCount = view.getUint32(pos, true);
    pos += uint32Length;
    var westIndices = new Uint16Array(buffer, pos, westVertexCount);
    pos += westVertexCount * uint16Length;

    var southVertexCount = view.getUint32(pos, true);
    pos += uint32Length;
    var southIndices = new Uint16Array(buffer, pos, southVertexCount);
    pos += southVertexCount * uint16Length;

    var eastVertexCount = view.getUint32(pos, true);
    pos += uint32Length;
    var eastIndices = new Uint16Array(buffer, pos, eastVertexCount);
    pos += eastVertexCount * uint16Length;

    var northVertexCount = view.getUint32(pos, true);
    pos += uint32Length;
    var northIndices = new Uint16Array(buffer, pos, northVertexCount);
    pos += northVertexCount * uint16Length;

    var skirtHeight = provider.getLevelMaximumGeometricError(level) * 5.0;

    return new Cesium.QuantizedMeshTerrainData({
        center : center,
        minimumHeight : minimumHeight,
        maximumHeight : maximumHeight,
        boundingSphere : boundingSphere,
        horizonOcclusionPoint : horizonOcclusionPoint,
        quantizedVertices : encodedVertexBuffer,
        indices : indices,
        westIndices : westIndices,
        southIndices : southIndices,
        eastIndices : eastIndices,
        northIndices : northIndices,
        westSkirtHeight : skirtHeight,
        southSkirtHeight : skirtHeight,
        eastSkirtHeight : skirtHeight,
        northSkirtHeight : skirtHeight,
        childTileMask: getChildMaskForTile(provider, level, x, tmsY)
    });
}

/**
 * Requests the geometry for a given tile.  This function should not be called before
 * {@link HeightmapAndQuantizedMeshTerrainProvider#ready} returns true.  The result must include terrain data and
 * may optionally include a water mask and an indication of which child tiles are available.
 *
 * @memberof HeightmapAndQuantizedMeshTerrainProvider
 *
 * @param {Number} x The X coordinate of the tile for which to request geometry.
 * @param {Number} y The Y coordinate of the tile for which to request geometry.
 * @param {Number} level The level of the tile for which to request geometry.
 * @param {Boolean} [throttleRequests=true] True if the number of simultaneous requests should be limited,
 *                  or false if the request should be initiated regardless of the number of requests
 *                  already in progress.
 * @returns {Promise|TerrainData} A promise for the requested geometry.  If this method
 *          returns undefined instead of a promise, it is an indication that too many requests are already
 *          pending and the request will be retried later.
 *
 * @exception {Cesium.DeveloperError} This function must not be called before {@link HeightmapAndQuantizedMeshTerrainProvider#ready}
 *            returns true.
 */
HeightmapAndQuantizedMeshTerrainProvider.prototype.requestTileGeometry = function(x, y, level, throttleRequests) {
    if (!this._ready) {
        throw new Cesium.DeveloperError('requestTileGeometry must not be called before the terrain provider is ready.');
    }
    var urlTemplates = this._tileUrlTemplates;
    if (urlTemplates.length === 0) {
        return undefined;
    }

    var yTiles = this._tilingScheme.getNumberOfYTilesAtLevel(level);

    var tmsY = (yTiles - y - 1);

    // Use the first URL template.  In the future we should use them all.
    var url = urlTemplates[0].replace('{z}', level).replace('{x}', x).replace('{y}', tmsY);

    var proxy = this._proxy;
    if (Cesium.defined(proxy)) {
        url = proxy.getURL(url);
    }

    var promise;

    throttleRequests = Cesium.defaultValue(throttleRequests, true);
    
    if (throttleRequests) {
        promise = Cesium.throttleRequestByServer(url, loadTile);
        if (!Cesium.defined(promise)) {
            return undefined;
        }
    } else {
        promise = Cesium.loadArrayBuffer(url);
    }

    var that = this;
    return Cesium.when(promise, function(buffer) {
        if (Cesium.defined(that._heightmapStructure)) {
            return createHeightmapTerrainData(that, buffer, level, x, y, tmsY);
        } else {
            return createQuantizedMeshTerrainData(that, buffer, level, x, y, tmsY);
        }
    });
};

Cesium.defineProperties(HeightmapAndQuantizedMeshTerrainProvider.prototype, {
    /**
     * Gets an event that is raised when the terrain provider encounters an asynchronous error.  By subscribing
     * to the event, you will be notified of the error and can potentially recover from it.  Event listeners
     * are passed an instance of {@link Cesium.TileProviderError}.
     * @memberof HeightmapAndQuantizedMeshTerrainProvider.prototype
     * @type {Event}
     */
    errorEvent : {
        get : function() {
            return this._errorEvent;
        }
    },

    /**
     * Gets the credit to display when this terrain provider is active.  Typically this is used to credit
     * the source of the terrain.  This function should not be called before {@link HeightmapAndQuantizedMeshTerrainProvider#ready} returns true.
     * @memberof HeightmapAndQuantizedMeshTerrainProvider.prototype
     * @type {Credit}
     */
    credit : {
        get : function() {
            if (!this._ready) {
                throw new Cesium.DeveloperError('credit must not be called before the terrain provider is ready.');
            }
            
            return this._credit;
        }
    },

    /**
     * Gets the tiling scheme used by this provider.  This function should
     * not be called before {@link HeightmapAndQuantizedMeshTerrainProvider#ready} returns true.
     * @memberof HeightmapAndQuantizedMeshTerrainProvider.prototype
     * @type {GeographicTilingScheme}
     */
    tilingScheme : {
        get : function() {
            if (!this._ready) {
                throw new Cesium.DeveloperError('tilingScheme must not be called before the terrain provider is ready.');
            }
            
            return this._tilingScheme;
        }
    },

    /**
     * Gets a value indicating whether or not the provider is ready for use.
     * @memberof HeightmapAndQuantizedMeshTerrainProvider.prototype
     * @type {Boolean}
     */
    ready : {
        get : function() {
            return this._ready;
        }
    }
});

/**
 * Gets the maximum geometric error allowed in a tile at a given level.
 *
 * @memberof HeightmapAndQuantizedMeshTerrainProvider
 *
 * @param {Number} level The tile level for which to get the maximum geometric error.
 * @returns {Number} The maximum geometric error.
 */
HeightmapAndQuantizedMeshTerrainProvider.prototype.getLevelMaximumGeometricError = function(level) {
    return this._levelZeroMaximumGeometricError / (1 << level);
};

/**
 * Gets a value indicating whether or not the provider includes a water mask.  The water mask
 * indicates which areas of the globe are water rather than land, so they can be rendered
 * as a reflective surface with animated waves.
 *
 * @memberof HeightmapAndQuantizedMeshTerrainProvider
 *
 * @returns {Boolean} True if the provider has a water mask; otherwise, false.
 *
 * @exception {Cesium.DeveloperError} This function must not be called before {@link HeightmapAndQuantizedMeshTerrainProvider#ready}
 *            returns true.
 */
HeightmapAndQuantizedMeshTerrainProvider.prototype.hasWaterMask = function() {
    if (!this._ready) {
        throw new Cesium.DeveloperError('hasWaterMask must not be called before the terrain provider is ready.');
    }
    
    return this._hasWaterMask;
};

function getChildMaskForTile(terrainProvider, level, x, y) {
    var available = terrainProvider._availableTiles;
    if (!available || available.length === 0) {
        return 15;
    }

    var childLevel = level + 1;
    if (childLevel >= available.length) {
        return 0;
    }

    var levelAvailable = available[childLevel];

    var mask = 0;

    mask |= isTileInRange(levelAvailable, 2 * x, 2 * y) ? 1 : 0;
    mask |= isTileInRange(levelAvailable, 2 * x + 1, 2 * y) ? 2 : 0;
    mask |= isTileInRange(levelAvailable, 2 * x, 2 * y + 1) ? 4 : 0;
    mask |= isTileInRange(levelAvailable, 2 * x + 1, 2 * y + 1) ? 8 : 0;

    return mask;
}

function isTileInRange(levelAvailable, x, y) {
    for (var i = 0, len = levelAvailable.length; i < len; ++i) {
        var range = levelAvailable[i];
        if (x >= range.startX && x <= range.endX && y >= range.startY && y <= range.endY) {
            return true;
        }
    }

    return false;
}

