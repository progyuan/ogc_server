var g_drawhelper_mode;
var g_rulerButton;

var DrawHelper2D = (function() {


    // constructor
    function _(leafletMap, toolbar_id) {
        this._viewer = leafletMap;
        this._scene = leafletMap;
		this._tooltip = createTooltip(leafletMap.getContainer());
		this._tooltip.setVisible(false);
        this._surfaces = [];
		this._primitives = [];
        this.initialiseHandlers();
		this.toolbar_container_id = toolbar_id;
		//this.save_callback = save_callback;
        this.enhancePrimitives();

    }

    _.prototype.initialiseHandlers = function() {
        var _self = this;
        
		
        //var handler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
        //function callPrimitiveCallback(name, position) {
            //if(_self._handlersMuted == true) return;
            //var pickedObject = scene.pick(position);
            //if(pickedObject && pickedObject.primitive && pickedObject.primitive[name]) {
                //pickedObject.primitive[name](position);
            //}
        //}
        //handler.setInputAction(
            //function (movement) {
                //callPrimitiveCallback('leftClick', movement.position);
        //}, Cesium.ScreenSpaceEventType.LEFT_CLICK);
        //handler.setInputAction(
            //function (movement) {
                //callPrimitiveCallback('leftDoubleClick', movement.position);
            //}, Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK);
        //var mouseOutObject;
        //handler.setInputAction(
            //function (movement) {
                //if(_self._handlersMuted == true) return;
                //var pickedObject = scene.pick(movement.endPosition);
                //if(mouseOutObject && (!pickedObject || mouseOutObject != pickedObject.primitive)) {
                    //!(mouseOutObject.isDestroyed && mouseOutObject.isDestroyed()) && mouseOutObject.mouseOut(movement.endPosition);
                    //mouseOutObject = null;
                //}
                //if(pickedObject && pickedObject.primitive) {
                    //pickedObject = pickedObject.primitive;
                    //if(pickedObject.mouseOut) {
                        //mouseOutObject = pickedObject;
                    //}
                    //if(pickedObject.mouseMove) {
                        //pickedObject.mouseMove(movement.endPosition);
                    //}
                //}
            //}, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
        //handler.setInputAction(
            //function (movement) {
                //callPrimitiveCallback('leftUp', movement.position);
            //}, Cesium.ScreenSpaceEventType.LEFT_UP);
        //handler.setInputAction(
            //function (movement) {
                //callPrimitiveCallback('leftDown', movement.position);
            //}, Cesium.ScreenSpaceEventType.LEFT_DOWN);
    }

    _.prototype.setListener = function(primitive, type, callback) {
        primitive[type] = callback;
    }

    _.prototype.muteHandlers = function(muted) {
        this._handlersMuted = muted;
    }
    _.prototype.addPrimitive = function(primitive) {
        this._primitives.push(primitive);
    }
    _.prototype.clearPrimitive = function() {
		var map = this._scene;
		map.eachLayer(function (layer) {
			//console.log(layer);
			if(layer.name && layer.name.indexOf('tmp_')>-1)
			{
				map.removeLayer(layer);
			}
		});
		if(this._layerPaint) {
			this._layerPaint.clearLayers();
		}

    }
    _.prototype.close = function() {
		this.stopDrawing();
		this.disableAllEditMode();
		this.disableAllHighlights();
		this.clearPrimitive();
		//console.log('close');
		this._tooltip.destroy();
		$('#' + this.toolbar_container_id).css('display','none');
    }
    _.prototype.show = function(isshow) {
		$('#' + this.toolbar_container_id).css('display',isshow?'block':'none');
    }
    _.prototype.isVisible = function() {
		if($('#' + this.toolbar_container_id).css('display') == 'block') 
			return true;
		return false;
    }


    _.prototype.startDrawing = function(cleanUp) {
        this.disableAllEditMode();
        if(this.editCleanUp) {
            this.editCleanUp();
        }
        this.editCleanUp = cleanUp;
        this.muteHandlers(true);
    }

    _.prototype.stopDrawing = function() {
        if(this.editCleanUp) {
            this.editCleanUp();
            this.editCleanUp = null;
        }
        this.muteHandlers(false);
    }

    _.prototype.disableAllHighlights = function() {
        this.setHighlighted(undefined);
    }

    _.prototype.setHighlighted = function(surface) {
        if(this._highlightedSurface && !this._highlightedSurface.isDestroyed() && this._highlightedSurface != surface) {
            this._highlightedSurface.setHighlighted(false);
        }
        this._highlightedSurface = surface;
    }

    _.prototype.disableAllEditMode = function() {
        this.setEdited(undefined);
    }

    _.prototype.setEdited = function(surface) {
        if(this._editedSurface && !this._editedSurface.isDestroyed()) {
            this._editedSurface.setEditMode(false);
        }
        this._editedSurface = surface;
    }

    var material = Cesium.Material.fromType(Cesium.Material.ColorType);
    material.uniforms.color = new Cesium.Color(1.0, 1.0, 0.0, 0.5);

    var defaultShapeOptions = {
        ellipsoid: Cesium.Ellipsoid.WGS84,
        textureRotationAngle: 0.0,
        height: 0.0,
        asynchronous: true,
        show: true,
        debugShowBoundingVolume: false
    }

    var defaultSurfaceOptions = copyOptions(defaultShapeOptions, {
        appearance: new Cesium.EllipsoidSurfaceAppearance({
            aboveGround : false
        }),
    	material : material,
        granularity: Math.PI / 180.0
    });

    var defaultPolygonOptions = copyOptions(defaultShapeOptions, {});
    var defaultExtentOptions = copyOptions(defaultShapeOptions, {});
    var defaultCircleOptions = copyOptions(defaultShapeOptions, {});
    var defaultEllipseOptions = copyOptions(defaultSurfaceOptions, {rotation: 0});

    var defaultPolylineOptions = copyOptions(defaultShapeOptions, {
        width: 5,
        geodesic: true,
        granularity: 10000,
        appearance: new Cesium.PolylineMaterialAppearance({
            aboveGround : false
        }),
    	material : material
    });

    
    var ChangeablePrimitive = (function() {
        function _() {
        }

        _.prototype.initialiseOptions = function(options) {

            fillOptions(this, options);

            this._ellipsoid = undefined;
            this._granularity = undefined;
            this._height = undefined;
            this._textureRotationAngle = undefined;
            this._id = undefined;

            // set the flags to initiate a first drawing
            this._createPrimitive = true;
            this._primitive = undefined;
            this._outlinePolygon = undefined;

        }

        _.prototype.setAttribute = function(name, value) {
            this[name] = value;
            this._createPrimitive = true;
        };

        _.prototype.getAttribute = function(name) {
            return this[name];
        };

        _.prototype.update = function(context, frameState, commandList) {

            if (!Cesium.defined(this.ellipsoid)) {
                throw new Cesium.DeveloperError('this.ellipsoid must be defined.');
            }

            if (!Cesium.defined(this.appearance)) {
                throw new Cesium.DeveloperError('this.material must be defined.');
            }

            if (this.granularity < 0.0) {
                throw new Cesium.DeveloperError('this.granularity and scene2D/scene3D overrides must be greater than zero.');
            }

            if (!this.show) {
                return;
            }

            if (!this._createPrimitive && (!Cesium.defined(this._primitive))) {
                // No positions/hierarchy to draw
                return;
            }

            if (this._createPrimitive ||
                (this._ellipsoid !== this.ellipsoid) ||
                (this._granularity !== this.granularity) ||
                (this._height !== this.height) ||
                (this._textureRotationAngle !== this.textureRotationAngle) ||
                (this._id !== this.id)) {

                var geometry = this.getGeometry();
                if(!geometry) {
                    return;
                }

                this._createPrimitive = false;
                this._ellipsoid = this.ellipsoid;
                this._granularity = this.granularity;
                this._height = this.height;
                this._textureRotationAngle = this.textureRotationAngle;
                this._id = this.id;

                this._primitive = this._primitive && this._primitive.destroy();

                this._primitive = new Cesium.Primitive({
                    geometryInstances : new Cesium.GeometryInstance({
                        geometry : geometry,
                        id : this.id,
                        pickPrimitive : this
                    }),
                    appearance : this.appearance,
                    asynchronous : this.asynchronous
                });

                this._outlinePolygon = this._outlinePolygon && this._outlinePolygon.destroy();
                if(this.strokeColor && this.getOutlineGeometry) {
                    // create the highlighting frame
                    this._outlinePolygon = new Cesium.Primitive({
                        geometryInstances : new Cesium.GeometryInstance({
                            geometry : this.getOutlineGeometry(),
                            attributes : {
                                color : Cesium.ColorGeometryInstanceAttribute.fromColor(this.strokeColor)
                            }
                        }),
                        appearance : new Cesium.PerInstanceColorAppearance({
                            flat : true,
                            renderState : {
                                depthTest : {
                                    enabled : true
                                },
                                //lineWidth : Math.min(this.strokeWidth || 4.0, context.getMaximumAliasedLineWidth())
                                lineWidth : Math.min(this.strokeWidth || 4.0, context.maximumAliasedLineWidth)
                            }
                        })
                    });
                }
            }

            var primitive = this._primitive;
            primitive.appearance.material = this.material;
            primitive.debugShowBoundingVolume = this.debugShowBoundingVolume;
            primitive.update(context, frameState, commandList);
            this._outlinePolygon && this._outlinePolygon.update(context, frameState, commandList);

        };

        _.prototype.isDestroyed = function() {
            return false;
        };

        _.prototype.destroy = function() {
            this._primitive = this._primitive && this._primitive.destroy();
            return Cesium.destroyObject(this);
        };

        _.prototype.setStrokeStyle = function(strokeColor, strokeWidth) {
            if(!this.strokeColor || !this.strokeColor.equals(strokeColor) || this.strokeWidth != strokeWidth) {
                this._createPrimitive = true;
                this.strokeColor = strokeColor;
                this.strokeWidth = strokeWidth;
            }
        }

        return _;
    })();

    _.ExtentPrimitive = (function() {
        function _(options) {

            if(!Cesium.defined(options.extent)) {
                throw new Cesium.DeveloperError('Extent is required');
            }

            options = copyOptions(options, defaultSurfaceOptions);

            this.initialiseOptions(options);

            this.setExtent(options.extent);

        }

        _.prototype = new ChangeablePrimitive();

        _.prototype.setExtent = function(extent) {
            this.setAttribute('extent', extent);
        };

        _.prototype.getExtent = function() {
            return this.getAttribute('extent');
        };

        _.prototype.getGeometry = function() {

            if (!Cesium.defined(this.extent)) {
                return;
            }

            return new Cesium.RectangleGeometry({
                rectangle : this.extent,
                height : this.height,
                vertexFormat : Cesium.EllipsoidSurfaceAppearance.VERTEX_FORMAT,
                stRotation : this.textureRotationAngle,
                ellipsoid : this.ellipsoid,
                granularity : this.granularity
            });
        };

        _.prototype.getOutlineGeometry = function() {
            return new Cesium.RectangleOutlineGeometry({
                rectangle: this.extent
            });
        }

        return _;
    })();

    _.PolygonPrimitive = (function() {
    	
        function _(options) {

            options = copyOptions(options, defaultSurfaceOptions);

            this.initialiseOptions(options);

        }

        _.prototype = new ChangeablePrimitive();

        _.prototype.setPositions = function(positions) {
            this.setAttribute('positions', positions);
        };

        _.prototype.getPositions = function() {
            return this.getAttribute('positions');
        };

        _.prototype.getGeometry = function() {

            if (!Cesium.defined(this.positions) || this.positions.length < 3) {
                return;
            }

            return Cesium.PolygonGeometry.fromPositions({
                positions : this.positions,
                height : this.height,
                vertexFormat : Cesium.EllipsoidSurfaceAppearance.VERTEX_FORMAT,
                stRotation : this.textureRotationAngle,
                ellipsoid : this.ellipsoid,
                granularity : this.granularity
            });
        };

        _.prototype.getOutlineGeometry = function() {
            return Cesium.PolygonOutlineGeometry.fromPositions({
                positions : this.getPositions()
            });
        }

        return _;
    })();

    _.CirclePrimitive = (function() {
    	
        function _(options) {

            if(!(Cesium.defined(options.center) && Cesium.defined(options.radius))) {
                throw new Cesium.DeveloperError('Center and radius are required');
            }

            options = copyOptions(options, defaultSurfaceOptions);

            this.initialiseOptions(options);

            this.setRadius(options.radius);

        }

        _.prototype = new ChangeablePrimitive();

        _.prototype.setCenter = function(center) {
            this.setAttribute('center', center);
        };

        _.prototype.setRadius = function(radius) {
            this.setAttribute('radius', Math.max(0.1, radius));
        };

        _.prototype.getCenter = function() {
            return this.getAttribute('center');
        };

        _.prototype.getRadius = function() {
            return this.getAttribute('radius');
        };

        _.prototype.getGeometry = function() {

            if (!(Cesium.defined(this.center) && Cesium.defined(this.radius))) {
                return;
            }

            return new Cesium.CircleGeometry({
                center : this.center,
                radius : this.radius,
                height : this.height,
                vertexFormat : Cesium.EllipsoidSurfaceAppearance.VERTEX_FORMAT,
                stRotation : this.textureRotationAngle,
                ellipsoid : this.ellipsoid,
                granularity : this.granularity
            });
        };

        _.prototype.getOutlineGeometry = function() {
            return new Cesium.CircleOutlineGeometry({
                center: this.getCenter(),
                radius: this.getRadius()
            });
        }

        return _;
    })();

    _.EllipsePrimitive = (function() {
        function _(options) {

            if(!(Cesium.defined(options.center) && Cesium.defined(options.semiMajorAxis) && Cesium.defined(options.semiMinorAxis))) {
                throw new Cesium.DeveloperError('Center and semi major and semi minor axis are required');
            }

            options = copyOptions(options, defaultEllipseOptions);

            this.initialiseOptions(options);

        }

        _.prototype = new ChangeablePrimitive();

        _.prototype.setCenter = function(center) {
            this.setAttribute('center', center);
        };

        _.prototype.setSemiMajorAxis = function(semiMajorAxis) {
            if(semiMajorAxis < this.getSemiMinorAxis()) return;
            this.setAttribute('semiMajorAxis', semiMajorAxis);
        };

        _.prototype.setSemiMinorAxis = function(semiMinorAxis) {
            if(semiMinorAxis > this.getSemiMajorAxis()) return;
            this.setAttribute('semiMinorAxis', semiMinorAxis);
        };

        _.prototype.setRotation = function(rotation) {
            return this.setAttribute('rotation', rotation);
        };

        _.prototype.getCenter = function() {
            return this.getAttribute('center');
        };

        _.prototype.getSemiMajorAxis = function() {
            return this.getAttribute('semiMajorAxis');
        };

        _.prototype.getSemiMinorAxis = function() {
            return this.getAttribute('semiMinorAxis');
        };

        _.prototype.getRotation = function() {
            return this.getAttribute('rotation');
        };

        _.prototype.getGeometry = function() {

            if(!(Cesium.defined(this.center) && Cesium.defined(this.semiMajorAxis) && Cesium.defined(this.semiMinorAxis))) {
                return;
            }

            return new Cesium.EllipseGeometry({
                        ellipsoid : this.ellipsoid,
                        center : this.center,
                        semiMajorAxis : this.semiMajorAxis,
                        semiMinorAxis : this.semiMinorAxis,
                        rotation : this.rotation,
                        height : this.height,
                        vertexFormat : Cesium.EllipsoidSurfaceAppearance.VERTEX_FORMAT,
                        stRotation : this.textureRotationAngle,
                        ellipsoid : this.ellipsoid,
                        granularity : this.granularity
                    });
        };

        _.prototype.getOutlineGeometry = function() {
            return new Cesium.EllipseOutlineGeometry({
                center: this.getCenter(),
                semiMajorAxis: this.getSemiMajorAxis(),
                semiMinorAxis: this.getSemiMinorAxis(),
                rotation: this.getRotation()
            });
        }

        return _;
    })();

    function getGeodesicPath(cartesians, granularity) {
        var index, cartographicPath = ellipsoid.cartesianArrayToCartographicArray(cartesians), geodesic, increment, ellipsoidCartographicPath = [];
        for(index = 0; index < cartographicPath.length - 1; index++) {
            geodesic = new Cesium.EllipsoidGeodesic(cartographicPath[index], cartographicPath[index + 1]);
            // add a point every granularity
            //var totalDistance = geodesic.getSurfaceDistance(),
            var totalDistance = geodesic.surfaceDistance,
                distance = 0;
            for(; distance < totalDistance; distance += granularity) {
                ellipsoidCartographicPath.push(geodesic.interpolateUsingSurfaceDistance(distance));
            }
        }
        ellipsoidCartographicPath.push(cartographicPath[cartographicPath.length - 1]);
        return ellipsoid.cartographicArrayToCartesianArray(ellipsoidCartographicPath);
    }

    _.PolylinePrimitive = (function() {
    	
        function _(options) {

            options = copyOptions(options, defaultPolylineOptions);

            this.initialiseOptions(options);

        }

        _.prototype = new ChangeablePrimitive();

        _.prototype.setPositions = function(positions) {
            this.setAttribute('positions', positions);
        };

        _.prototype.setWidth = function(width) {
            this.setAttribute('width', width);
        };

        _.prototype.setGeodesic = function(geodesic) {
            this.setAttribute('geodesic', geodesic);
        };

        _.prototype.getPositions = function() {
            return this.getAttribute('positions');
        };

        _.prototype.getWidth = function() {
            return this.getAttribute('width');
        };

        _.prototype.getGeodesic = function(geodesic) {
            return this.getAttribute('geodesic');
        };

        _.prototype.getGeometry = function() {
        	
            if (!Cesium.defined(this.positions) || this.positions.length < 2) {
                return;
            }

            return new Cesium.PolylineGeometry({
                    positions: this.geodesic ? getGeodesicPath(this.positions, Math.max(this.granularity, 50000)) : this.positions,
                    height : this.height,
                    width: this.width < 1 ? 1 : this.width,
                    vertexFormat : Cesium.EllipsoidSurfaceAppearance.VERTEX_FORMAT,
                    ellipsoid : this.ellipsoid
                });
        }
        
        return _;
    })();

    var defaultBillboard = {
        iconUrl: "img/dragIcon.png",
        shiftX: 0,
        shiftY: 0
    }

    var dragBillboard = {
        iconUrl: "img/dragIcon.png",
        shiftX: 0,
        shiftY: 0
    }

    var dragHalfBillboard = {
        iconUrl: "img/dragIconLight.png",
        shiftX: 0,
        shiftY: 0
    }

    _.prototype.createBillboardGroup = function(points, options, callbacks) {
        var markers = new _.BillboardGroup(this, options);
        markers.addBillboards(points, callbacks);
        return markers;
    }

    _.BillboardGroup = function(drawHelper, options) {

        this._drawHelper = drawHelper;
        this._scene = drawHelper._scene;

        this._options = copyOptions(options, defaultBillboard);

        
        var b = new Cesium.BillboardCollection();
        
        this._scene.primitives.add(b);
		this._drawHelper.addPrimitive(b);
        this._billboards = b;
        
        this._orderedBillboards = [];

        var image = new Image();
        var _self = this;
        image.src = options.iconUrl;
    }

    _.BillboardGroup.prototype.createBillboard = function(position, callbacks) {
		if(this._billboards.isDestroyed())
		{
			var b = new Cesium.BillboardCollection();
			//b.textureAtlas = this._textureAtlas;
			this._scene.primitives.add(b);
			this._drawHelper.addPrimitive(b);
			this._billboards = b;
		}
        var billboard = this._billboards.add({
            show : true,
            position : position,
            pixelOffset : new Cesium.Cartesian2(this._options.shiftX, this._options.shiftY),
            eyeOffset : new Cesium.Cartesian3(0.0, 0.0, 0.0),
            horizontalOrigin : Cesium.HorizontalOrigin.CENTER,
            verticalOrigin : Cesium.VerticalOrigin.CENTER,
            scale : 1.0,
            imageIndex : 0,
            color : new Cesium.Color(1.0, 1.0, 1.0, 1.0)
        });

        // if editable
        if(callbacks) {
            var _self = this;
            var screenSpaceCameraController = this._scene.screenSpaceCameraController;
            function enableRotation(enable) {
                screenSpaceCameraController.enableRotate = enable;
            }
            function getIndex() {
                // find index
                for (var i = 0, I = _self._orderedBillboards.length; i < I && _self._orderedBillboards[i] != billboard; ++i);
                return i;
            }
            if(callbacks.dragHandlers) {
                var _self = this;
                setListener(billboard, 'leftDown', function(position) {
                    // TODO - start the drag handlers here
                    // create handlers for mouseOut and leftUp for the billboard and a mouseMove
                    function onDrag(position) {
                        //billboard.setPosition(position);
                        billboard.position = position;
                        // find index
                        for (var i = 0, I = _self._orderedBillboards.length; i < I && _self._orderedBillboards[i] != billboard; ++i);
                        callbacks.dragHandlers.onDrag && callbacks.dragHandlers.onDrag(getIndex(), position);
                    }
                    function onDragEnd(position) {
                        handler.destroy();
                        enableRotation(true);
                        callbacks.dragHandlers.onDragEnd && callbacks.dragHandlers.onDragEnd(getIndex(), position);
                    }

                    var handler = new Cesium.ScreenSpaceEventHandler(_self._scene.canvas);

                    handler.setInputAction(function(movement) {
                        //var cartesian = _self._scene.camera.pickEllipsoid(movement.endPosition, ellipsoid);
						var ray = _self._scene.camera.getPickRay(movement.endPosition);
						var cartesian = _self._scene.globe.pick(ray, _self._scene);					
                        
                        if (cartesian) {
                            onDrag(cartesian);
                        } else {
                            onDragEnd(cartesian);
                        }
                    }, Cesium.ScreenSpaceEventType.MOUSE_MOVE);

                    handler.setInputAction(function(movement) {
                        //onDragEnd(_self._scene.camera.pickEllipsoid(movement.position, ellipsoid));
						var ray = _self._scene.camera.getPickRay(movement.position);
						var cartesian = _self._scene.globe.pick(ray, _self._scene);					
                        onDragEnd(cartesian);
                    }, Cesium.ScreenSpaceEventType.LEFT_UP);

                    enableRotation(false);

                    //callbacks.dragHandlers.onDragStart && callbacks.dragHandlers.onDragStart(getIndex(), _self._scene.camera.pickEllipsoid(position, ellipsoid));
                    //var cartesian = _self._scene.camera.pickEllipsoid(position, ellipsoid);
					var ray = _self._scene.camera.getPickRay(position);
					var cartesian = _self._scene.globe.pick(ray, _self._scene);					
                    callbacks.dragHandlers.onDragStart && callbacks.dragHandlers.onDragStart(getIndex(), cartesian);
                });
            }
            if(callbacks.onDoubleClick) {
                setListener(billboard, 'leftDoubleClick', function(position) {
                    callbacks.onDoubleClick(getIndex());
                });
            }
            if(callbacks.onClick) {
                setListener(billboard, 'leftClick', function(position) {
                    callbacks.onClick(getIndex());
                });
            }
            if(callbacks.tooltip) {
                setListener(billboard, 'mouseMove', function(position) {
                    _self._drawHelper._tooltip.showAt(position, callbacks.tooltip());
                });
                setListener(billboard, 'mouseOut', function(position) {
                    _self._drawHelper._tooltip.setVisible(false);
                });
            }
        }

        return billboard;
    }

    _.BillboardGroup.prototype.insertBillboard = function(index, position, callbacks) {
        this._orderedBillboards.splice(index, 0, this.createBillboard(position, callbacks));
    }

    _.BillboardGroup.prototype.addBillboard = function(position, callbacks) {
        this._orderedBillboards.push(this.createBillboard(position, callbacks));
    }

    _.BillboardGroup.prototype.addBillboards = function(positions, callbacks) {
        var index =  0;
        for(; index < positions.length; index++) {
            this.addBillboard(positions[index], callbacks);
        }
    }

    _.BillboardGroup.prototype.updateBillboardsPositions = function(positions) {
        var index =  0;
        for(; index < positions.length; index++) {
            //this.getBillboard(index).setPosition(positions[index]);
            this.getBillboard(index).position = positions[index];
        }
    }

    _.BillboardGroup.prototype.countBillboards = function() {
        return this._orderedBillboards.length;
    }

    _.BillboardGroup.prototype.getBillboard = function(index) {
        return this._orderedBillboards[index];
    }

    _.BillboardGroup.prototype.removeBillboard = function(index) {
        this._billboards.remove(this.getBillboard(index));
        this._orderedBillboards.splice(index, 1);
    }

    _.BillboardGroup.prototype.remove = function() {
		try
		{
			this._billboards = this._billboards && this._billboards.removeAll() && this._billboards.destroy();
		}catch(e){}
    }

    _.BillboardGroup.prototype.setOnTop = function() {
        this._scene.primitives.raiseToTop(this._billboards);
    }

    _.prototype.startDrawingMarker = function(options) {
        var _self = this;
        var map = this._scene;

        var options = copyOptions(options, defaultBillboard);

        this.startDrawing(
            function() {
                //map.removeLayer(markers);
				map.off('click', null);
				map.off('mousemove', null);
                tooltip.setVisible(false);
            }
        );

        //var primitives = scene.primitives;
        var tooltip = this._tooltip;
		
		map.on('click', function(e){
			_self.stopDrawing();
			options.callback(e.latlng);
		});
		map.on('mousemove', function(e){
			tooltip.showAt(e.containerPoint, "<p>当前坐标: </p>" + GetDisplayLatLngString2D(e.latlng, 7));
		});
    }

    _.prototype.startDrawingPolygon = function(options) {
        var options = copyOptions(options, defaultSurfaceOptions);
        this.startDrawingPolyshape(true, options);
    }

    _.prototype.startDrawingPolyline = function(options) {
        var options = copyOptions(options, defaultPolylineOptions);
        this.startDrawingPolyshape(false, options);
    }

    _.prototype.startDrawingPolyshape = function(isPolygon, options) {
		this.startDrawing(
			function() {
				map.off('click', null);
				map.off('dblclick', null);
				map.off('mousemove', null);
				tooltip.setVisible(false);
			}
		);

        var _self = this;
        var map = this._scene;
        var tooltip = this._tooltip;
        var minPoints = isPolygon ? 3 : 2;
		
		var positions = [];
		if(!this._layerPaint) {
			this._layerPaint = L.layerGroup().addTo(map);
			//this._layerPaint.name = 'tmp_polyline';
		}

		if(!this._points) {
			this._points = [];
		}
		
		if(!this._finishPath)
		{
			this._finishPath = function() {
				
				if(_self._lastCircle) {
					_self._layerPaint.removeLayer(_self._lastCircle);
				}
				tooltip.setVisible(false);
				if(_self._layerPaint && _self._layerPaintPathTemp) {
					_self._layerPaint.removeLayer(_self._layerPaintPathTemp);
				}
				_self._restartPath();
				
			};
		}
		if(!this._restartPath)
		{
			this._restartPath = function() {
				_self._distance = 0;
				_self._lastCircle = undefined;
				_self._lastPoint = undefined;
				_self._layerPaintPath = undefined;
				_self._layerPaintPathTemp = undefined;
				_self._points = [];
			};
		}
		map.on('click', function(e){
			if(!e.latlng)
			{
				return;
			}
			if(_self._lastPoint) {
				if(!_self._distance) {
					_self._distance = 0;
				}
				var distance = e.latlng.distanceTo(_self._lastPoint);
				_self._distance += distance;
			}
			
			if(_self._lastPoint && !_self._layerPaintPath) 
			{
				if(isPolygon)
				{
					_self._layerPaintPath = L.polygon([_self._lastPoint], { 
						color: 'yellow',
						weight: 5,
						clickable: false
					}).addTo(_self._layerPaint);
				}else
				{
					_self._layerPaintPath = L.polyline([_self._lastPoint], { 
						color: 'yellow',
						weight: 5,
						clickable: false
					}).addTo(_self._layerPaint);
				}
			}
	
			if(_self._layerPaintPath) {
				_self._layerPaintPath.addLatLng(e.latlng);
			}
	
			if(_self._lastCircle) {
				_self._layerPaint.removeLayer(_self._lastCircle);
			}
	
			_self._lastCircle = new L.CircleMarker(e.latlng, { 
				color: 'yellow', 
				opacity: 1, 
				weight: 1, 
				fill: true, 
				fillOpacity: 1,
				radius:5,
				//clickable: _self._lastCircle ? true : false
				clickable: false
			}).addTo(_self._layerPaint);
			
			//_self._lastCircle.on('click', function() { 
				//_self._finishPath();
			//}, _self);
			_self._lastPoint = e.latlng;
			_self._points.push(e.latlng);
		});
		map.on('mousemove', function(e){
			//if(!e.latlng || !this._lastPoint) {
				//return;
			//}
			
			if(_self._points.length == 0) 
			{
				tooltip.showAt(e.containerPoint, "<p>单击添加点</p>");
				return;
			}
			if(!_self._layerPaintPathTemp) 
			{
				if(isPolygon)
				{
					_self._layerPaintPathTemp = L.polygon([_self._lastPoint, e.latlng], { 
						color: 'yellow',
						weight: 5,
						clickable: false,
						dashArray: '6,12'
					}).addTo(_self._layerPaint);
				}else
				{
					_self._layerPaintPathTemp = L.polyline([_self._lastPoint, e.latlng], { 
						color: 'yellow',
						weight: 5,
						clickable: false,
						dashArray: '6,12'
					}).addTo(_self._layerPaint);
				}
			} else {
				if(isPolygon)
				{
					_self._layerPaintPathTemp.spliceLatLngs(1, 2, _self._lastPoint, e.latlng);
				}else
				{
					_self._layerPaintPathTemp.spliceLatLngs(0, 2, _self._lastPoint, e.latlng);
				}
			}
			
			
			if(!_self._distance) {
				_self._distance = 0;
			}

			var distance = e.latlng.distanceTo(_self._lastPoint);
			
			var tip = "";
			if(g_drawhelper_mode === 'ruler')
			{
				if(!isPolygon)
				{
					tip = "<p>当前位置" + GetDisplayLatLngString2D(e.latlng, 6) + "</p>" 
					+ (distance > 0 ? "<p>距离上一点长度:" + distance.toFixed(0) + "米</p>" : "")
					+ (_self._distance > 0 ? "<p>总长度:" + (_self._distance + distance).toFixed(0) + "米</p>" : "");
				}
				else
				{
					tip = "<p>当前位置" + GetDisplayLatLngString2D(e.latlng, 6) + "</p>";
					if(_self._points.length >= minPoints - 1)
					{
						var polypos = [];
						for(var i in _self._points)
						{
							var latlng = _self._points[i];
							var carto = Cesium.Cartographic.fromDegrees(latlng.lng, latlng.lat, 0);
							var merc = ToWebMercator(carto);
							polypos.push(merc[0]);
							polypos.push(merc[1]);
						}
						var carto = Cesium.Cartographic.fromDegrees(e.latlng.lng, e.latlng.lat, 0);
						var merc = ToWebMercator(carto);
						polypos.push(merc[0]);
						polypos.push(merc[1]);
						
						var area = PolyK.GetArea(polypos);
						area = Math.abs(area);
						if(area > 1000000)
						{
							tip += "<p>面积:" + (area/1000000).toFixed(3) + "平方千米</p>";
						}
						else
						{
							tip += "<p>面积:" + area.toFixed(0) + "平方米</p>";
						}
					}
				}
			}
			else 
			{
				tip = "<p>单击添加第" + _self._points.length + "点" + GetDisplayLatLngString2D(e.latlng, 6) + "</p>" + (_self._points.length > minPoints ? "<p>双击结束添加</p>" : "");
			}
			tooltip.showAt(e.containerPoint, tip);
		});
		map.on('dblclick', function(e){
			if(_self._lastPoint)
			{
				_self.stopDrawing();
				options.callback(_self._points);
				_self._finishPath();
			}
		});
    }

    _.prototype.startDrawingExtent = function(options) {
        var options = copyOptions(options, defaultSurfaceOptions);
        this.startDrawing(
            function() {
				map.off('click', null);
				map.off('dblclick', null);
				map.off('mousemove', null);
				tooltip.setVisible(false);
            }
        );
		
        var _self = this;
        var map = this._scene;
        var tooltip = this._tooltip;
		
		var positions = [];
		if(!this._layerPaint) {
			this._layerPaint = L.layerGroup().addTo(map);
		}

		if(!this._points) {
			this._points = [];
		}
		
		if(!this._finishPath)
		{
			this._finishPath = function() {
				
				if(_self._lastCircle) {
					_self._layerPaint.removeLayer(_self._lastCircle);
				}
				tooltip.setVisible(false);
				if(_self._layerPaint && _self._layerPaintPathTemp) {
					_self._layerPaint.removeLayer(_self._layerPaintPathTemp);
				}
				_self._restartPath();
				
			};
		}
		if(!this._restartPath)
		{
			this._restartPath = function() {
				_self._distance = 0;
				_self._lastCircle = undefined;
				_self._lastPoint = undefined;
				_self._layerPaintPath = undefined;
				_self._layerPaintPathTemp = undefined;
				_self._points = [];
			};
		}
		map.on('click', function(e){
			if(!e.latlng)
			{
				return;
			}
			if(_self._lastPoint === undefined)
			{
				_self._lastPoint = e.latlng;
			}
			
		});
		map.on('mousemove', function(e){
			//if(!e.latlng || !this._lastPoint) {
				//return;
			//}
			var bounds;
			if(_self._lastPoint === undefined) 
			{
				tooltip.showAt(e.containerPoint, "<p>点击鼠标设定矩形范围顶点</p>");
				return;
			}else
			{
				bounds = L.latLngBounds(_self._lastPoint, e.latlng);
				if(!_self._layerPaintPathTemp)
				{
					_self._layerPaintPathTemp = L.rectangle(bounds, { 
						color: 'yellow',
						weight: 5,
						clickable: false,
						dashArray: '6,12'
					}).addTo(_self._layerPaint);
				}
				_self._layerPaintPathTemp.setBounds(bounds);
			}
			
			var pts = [];
			pts.push(bounds.getNorthWest());
			pts.push(bounds.getSouthWest());
			pts.push(bounds.getSouthEast());
			pts.push(bounds.getNorthEast());
			_self._points = pts;
			var tip = '<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;北' + bounds.getNorth().toFixed(5) + '°</p>';
			tip += '<p>西' + bounds.getWest().toFixed(5) + '°&nbsp;&nbsp;东' + bounds.getEast().toFixed(5) + '°</p>';
			tip += '<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;南' + bounds.getSouth().toFixed(5) + '°</p>';
			if(g_drawhelper_mode === 'ruler')
			{
				
				var polypos = [];
				for(var i in pts)
				{
					var latlng = pts[i];
					var carto = Cesium.Cartographic.fromDegrees(latlng.lng, latlng.lat, 0);
					var merc = ToWebMercator(carto);
					polypos.push(merc[0]);
					polypos.push(merc[1]);
				}
				
				var area = PolyK.GetArea(polypos);
				area = Math.abs(area);
				if(area > 1000000)
				{
					tip += "<p>面积:" + (area/1000000).toFixed(3) + "平方千米</p>";
				}
				else
				{
					tip += "<p>面积:" + area.toFixed(0) + "平方米</p>";
				}
			}
			tooltip.showAt(e.containerPoint, tip);
		});
		map.on('dblclick', function(e){
			if(_self._lastPoint)
			{
				var bounds = L.latLngBounds(_self._lastPoint, e.latlng);
				if(!_self._layerPaintPath)
				{
					_self._layerPaintPath = L.rectangle(bounds, { 
						color: 'yellow',
						weight: 5,
						clickable: false,
					}).addTo(_self._layerPaint);
				}
				_self.stopDrawing();
				options.callback(_self._points);
				_self._finishPath();
			}
		});
    }

    _.prototype.startDrawingCircle = function(options) {

        var options = copyOptions(options, defaultSurfaceOptions);

        this.startDrawing(
            function() {
				map.off('click', null);
				map.off('dblclick', null);
				map.off('mousemove', null);
				tooltip.setVisible(false);
            }
        );
		
        var _self = this;
        var map = this._scene;
        var tooltip = this._tooltip;
		
		var positions = [];
		if(!this._layerPaint) {
			this._layerPaint = L.layerGroup().addTo(map);
		}

		if(!this._points) {
			this._points = [];
		}
		
		if(!this._finishPath)
		{
			this._finishPath = function() {
				
				if(_self._lastCircle) {
					_self._layerPaint.removeLayer(_self._lastCircle);
				}
				tooltip.setVisible(false);
				if(_self._layerPaint && _self._layerPaintPathTemp) {
					_self._layerPaint.removeLayer(_self._layerPaintPathTemp);
				}
				_self._restartPath();
				
			};
		}
		if(!this._restartPath)
		{
			this._restartPath = function() {
				_self._distance = 0;
				_self._lastCircle = undefined;
				_self._lastPoint = undefined;
				_self._layerPaintPath = undefined;
				_self._layerPaintPathTemp = undefined;
				_self._points = [];
			};
		}
		map.on('click', function(e){
			if(!e.latlng)
			{
				return;
			}
			if(_self._lastPoint === undefined)
			{
				_self._lastPoint = e.latlng;
			}
			
		});
		map.on('mousemove', function(e){
			//if(!e.latlng || !this._lastPoint) {
				//return;
			//}
			if(!_self._distance)
			{
				_self._distance = 0;
			}
			if(_self._lastPoint === undefined) 
			{
				tooltip.showAt(e.containerPoint, "<p>点击鼠标设定圆心</p>");
				return;
			}else
			{
				_self._distance = e.latlng.distanceTo(_self._lastPoint);
				if(!_self._layerPaintPathTemp)
				{
					_self._layerPaintPathTemp = L.circle(_self._lastPoint, _self._distance, { 
						color: 'yellow',
						weight: 5,
						clickable: false,
						dashArray: '6,12'
					}).addTo(_self._layerPaint);
				}
				_self._layerPaintPathTemp.setRadius(_self._distance);
			}
			
			var tip = '<p>圆心:' + GetDisplayLatLngString2D(_self._lastPoint, 7) + '</p>';
			tip += '<p>半径:' + _self._distance.toFixed(0) + '米</p>';
			if(g_drawhelper_mode === 'ruler')
			{
				var area = Math.PI * _self._distance * _self._distance;
				if(area < 1000000)
				{
					tip += '<p>面积:' + area.toFixed(0) + '平方米</p>';
				}else
				{
					tip += '<p>面积:' + (area/1000000).toFixed(3) + '平方千米</p>';
				}
			}
			tooltip.showAt(e.containerPoint, tip);
		});
		map.on('dblclick', function(e){
			if(_self._lastPoint)
			{
				if(!_self._layerPaintPath)
				{
					_self._layerPaintPath = L.circle(_self._lastPoint, _self._distance, { 
						color: 'yellow',
						weight: 5,
						clickable: false,
					}).addTo(_self._layerPaint);
				}
				_self.stopDrawing();
				options.callback(_self._lastPoint, _self._distance);
				_self._finishPath();
			}
		});
    }

    _.prototype.enhancePrimitives = function() {

        var drawHelper = this;

        Cesium.Billboard.prototype.setEditable = function() {

            if(this._editable) {
                return;
            }

            this._editable = true;

            var billboard = this;

            var _self = this;

            function enableRotation(enable) {
                drawHelper._scene.screenSpaceCameraController.enableRotate = enable;
            }

            setListener(billboard, 'leftDown', function(position) {
                // TODO - start the drag handlers here
                // create handlers for mouseOut and leftUp for the billboard and a mouseMove
                function onDrag(position) {
                    //billboard.setPosition(position);
                    billboard.position = position;
                    _self.executeListeners({name: 'drag', positions: position});
                }
                function onDragEnd(position) {
                    handler.destroy();
                    enableRotation(true);
                    _self.executeListeners({name: 'dragEnd', positions: position});
                }

                var handler = new Cesium.ScreenSpaceEventHandler(drawHelper._scene.canvas);

                handler.setInputAction(function(movement) {
                    //var cartesian = drawHelper._scene.camera.pickEllipsoid(movement.endPosition, ellipsoid);
					var ray = drawHelper._scene.camera.getPickRay(movement.endPosition);
					var cartesian = drawHelper._scene.globe.pick(ray, drawHelper._scene);					
                    if (cartesian) {
                        onDrag(cartesian);
                    } else {
                        onDragEnd(cartesian);
                    }
                }, Cesium.ScreenSpaceEventType.MOUSE_MOVE);

                handler.setInputAction(function(movement) {
                    //onDragEnd(drawHelper._scene.camera.pickEllipsoid(movement.position, ellipsoid));
					var ray = drawHelper._scene.camera.getPickRay(movement.position);
					var cartesian = drawHelper._scene.globe.pick(ray, drawHelper._scene);					
					onDragEnd(cartesian);
                }, Cesium.ScreenSpaceEventType.LEFT_UP);

                enableRotation(false);

            });

            enhanceWithListeners(billboard);

        }
        
        function setHighlighted(highlighted) {

            var scene = drawHelper._scene;

            // if no change
            // if already highlighted, the outline polygon will be available
            if(this._highlighted && this._highlighted == highlighted) {
                return;
            }
            // disable if already in edit mode
            if(this._editMode === true) {
                return;
            }
        	this._highlighted = highlighted;
            // highlight by creating an outline polygon matching the polygon points
            if(highlighted) {
                // make sure all other shapes are not highlighted
                drawHelper.setHighlighted(this);
                this._strokeColor = this.strokeColor;
                this.setStrokeStyle(Cesium.Color.fromCssColorString('white'), this.strokeWidth);
            } else {
                if(this._strokeColor) {
                    this.setStrokeStyle(this._strokeColor, this.strokeWidth);
                } else {
                    this.setStrokeStyle(undefined, undefined);
                }
            }
        }

        function setEditMode(editMode) {
                // if no change
                if(this._editMode == editMode) {
                    return;
                }
                // make sure all other shapes are not in edit mode before starting the editing of this shape
                drawHelper.disableAllHighlights();
                // display markers
                if(editMode) {
                    drawHelper.setEdited(this);
                    var scene = drawHelper._scene;
                    var _self = this;
                    // create the markers and handlers for the editing
                    if(this._markers == null) {
                        var markers = new _.BillboardGroup(drawHelper, dragBillboard);
                        var editMarkers = new _.BillboardGroup(drawHelper, dragHalfBillboard);
                        var positions = this.getPositions();
                        // function for updating the edit markers around a certain point
                        function updateHalfMarkers(index, positions) {
                            // update the half markers before and after the index
                            var editIndex = index - 1 < 0 ? positions.length - 1 : index - 1;
                            if(editIndex < editMarkers.countBillboards()) {
                                //editMarkers.getBillboard(editIndex).setPosition(calculateHalfMarkerPosition(editIndex));
                                editMarkers.getBillboard(editIndex).position = calculateHalfMarkerPosition(editIndex);
                            }
                            editIndex = index;
                            if(editIndex < editMarkers.countBillboards()) {
                                //editMarkers.getBillboard(editIndex).setPosition(calculateHalfMarkerPosition(editIndex));
                                editMarkers.getBillboard(editIndex).position = calculateHalfMarkerPosition(editIndex);
                            }
                        }
                        function onEdited() {
                            _self.executeListeners({name: 'onEdited', positions: _self.getPositions()});
                        }
                        var handleMarkerChanges = {
                            dragHandlers: {
                                onDrag: function(index, position) {
                                    positions = _self.getPositions();
                                    positions[index] = position;
                                    _self.setPositions(positions);
                                    updateHalfMarkers(index, positions);
                                },
                                onDragEnd: function(index, position) {
                                    onEdited();
                                }
                            },
                            onDoubleClick: function(index) {
                                if(_self.getPositions().length < 4) {
                                    return;
                                }
                                // remove the point and the corresponding markers
                                positions = _self.getPositions();
                                positions.splice(index, 1);
                                markers.removeBillboard(index);
                                editMarkers.removeBillboard(index);
                                _self.setPositions(positions);
                                updateHalfMarkers(index, positions);
                                onEdited();
                            },
                            tooltip: function() {
                                if(_self.getPositions().length > 3) {
                                    return "Double click to remove this point";
                                }
                            }
                        };
                        // add billboards and keep an ordered list of them for the polygon edges
                        markers.addBillboards(positions, handleMarkerChanges);
                        this._markers = markers;
                        function calculateHalfMarkerPosition(index) {
                            positions = _self.getPositions();
                            return ellipsoid.scaleToGeodeticSurface(Cesium.Cartesian3.lerp(positions[index], positions[index < positions.length - 1 ? index + 1 : 0], 0.5));
                        }
                        var halfPositions = [];
                        var index = 0;
                        var length = positions.length + (this.isPolygon ? 0 : -1);
                        for(; index < length; index++) {
                            halfPositions.push(calculateHalfMarkerPosition(index));
                        }
                        var handleEditMarkerChanges = {
                            dragHandlers: {
                                onDragStart: function(index, position) {
                                    // add a new position to the polygon but not a new marker yet
                                    positions = _self.getPositions();
                                    this.index = index + 1;
                                    positions.splice(this.index, 0, position);
                                    _self.setPositions(positions);
                                },
                                onDrag: function(index, position) {
                                    positions = _self.getPositions();
                                    positions[this.index] = position;
                                    _self.setPositions(positions);
                                },
                                onDragEnd: function(index, position) {
                                    // create new sets of makers for editing
                                    markers.insertBillboard(this.index, position, handleMarkerChanges);
                                    //editMarkers.getBillboard(this.index - 1).setPosition(calculateHalfMarkerPosition(this.index - 1));
                                    editMarkers.getBillboard(this.index - 1).position = calculateHalfMarkerPosition(this.index - 1);
                                    editMarkers.insertBillboard(this.index, calculateHalfMarkerPosition(this.index), handleEditMarkerChanges);
                                    onEdited();
                                }
                            },
                            tooltip: function() {
                                return "Drag to create a new point";
                            }
                        };
                        editMarkers.addBillboards(halfPositions, handleEditMarkerChanges);
                        this._editMarkers = editMarkers;
                        // add a handler for clicking in the globe
                        this._globeClickhandler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
                        this._globeClickhandler.setInputAction(
                            function (movement) {
                                var pickedObject = scene.pick(movement.position);
                                if(!(pickedObject && pickedObject.primitive)) {
                                    try{
										_self.setEditMode(false);
									}catch(e)
									{
									}
                                }
                            }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

                        // set on top of the polygon
                        markers.setOnTop();
                        editMarkers.setOnTop();
                    }
                    this._editMode = true;
                } else {
                    if(this._markers != null) {
                        this._markers.remove();
                        this._editMarkers.remove();
                        this._markers = null;
                        this._editMarkers = null;
                        this._globeClickhandler.destroy();
                    }
                    this._editMode = false;
                }
        }

        DrawHelper.PolylinePrimitive.prototype.setEditable = function() {

            if(this.setEditMode) {
                return;
            }

             var polyline = this;
            polyline.isPolygon = false;
            polyline.asynchronous = false;

            drawHelper.registerEditableShape(polyline);

            polyline.setEditMode = setEditMode;

            var originalWidth = this.getWidth();

            polyline.setHighlighted = function(highlighted) {
                // disable if already in edit mode
                if(this._editMode === true) {
                    return;
                }
                if(highlighted) {
                    drawHelper.setHighlighted(this);
                    this.setWidth(originalWidth * 2);
                } else {
                    this.setWidth(originalWidth);
                }
            }

            polyline.getExtent = function() {
                return Cesium.Rectangle.fromCartographicArray(ellipsoid.cartesianArrayToCartographicArray(this.getPositions()));
            }

            enhanceWithListeners(polyline);

            polyline.setEditMode(false);

        }

        DrawHelper.PolygonPrimitive.prototype.setEditable = function() {

            var polygon = this;
            polygon.asynchronous = false;

            drawHelper.registerEditableShape(polygon);

            polygon.setEditMode = setEditMode;

            polygon.setHighlighted = setHighlighted;

            enhanceWithListeners(polygon);

            polygon.setEditMode(false);

        }

        DrawHelper.ExtentPrimitive.prototype.setEditable = function() {

            if(this.setEditMode) {
                return;
            }

            var extent = this;
            var scene = drawHelper._scene;

            drawHelper.registerEditableShape(extent);
            extent.asynchronous = false;

            extent.setEditMode = function(editMode) {
                // if no change
                if(this._editMode == editMode) {
                    return;
                }
                drawHelper.disableAllHighlights();
                // display markers
                if(editMode) {
                    // make sure all other shapes are not in edit mode before starting the editing of this shape
                    drawHelper.setEdited(this);
                    // create the markers and handlers for the editing
                    if(this._markers == null) {
                        function getCorners(extent) {
                            return ellipsoid.cartographicArrayToCartesianArray([Cesium.Rectangle.getNortheast(extent), Cesium.Rectangle.getNorthwest(extent), Cesium.Rectangle.getSouthwest(extent), Cesium.Rectangle.getSoutheast(extent)]);
                        }
                        var markers = new _.BillboardGroup(drawHelper, dragBillboard);
                        function onEdited() {
                            extent.executeListeners({name: 'onEdited', extent: extent.extent});
                        }
                        var handleMarkerChanges = {
                            dragHandlers: {
                                onDrag: function(index, position) {
                                    var corner = markers.getBillboard((index + 2) % 4).position;
                                    extent.setExtent(getExtent(ellipsoid.cartesianToCartographic(corner), ellipsoid.cartesianToCartographic(position)));
                                    markers.updateBillboardsPositions(getCorners(extent.extent));
                                },
                                onDragEnd: function(index, position) {
                                    onEdited();
                                }
                            },
                            tooltip: function() {
                                return "Drag to change the corners of this extent";
                            }
                        };
                        markers.addBillboards(getCorners(extent.extent), handleMarkerChanges);
                        this._markers = markers;
                        // add a handler for clicking in the globe
                        this._globeClickhandler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
                        this._globeClickhandler.setInputAction(
                            function (movement) {
                                var pickedObject = scene.pick(movement.position);
                                if(!(pickedObject && pickedObject.primitive)) {
                                    try{
										extent.setEditMode(false);
									}catch(e){
									}
                                }
                            }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

                        // set on top of the polygon
                        markers.setOnTop();
                    }
                    this._editMode = true;
                } else {
                    if(this._markers != null) {
                        this._markers.remove();
                        this._markers = null;
                        this._globeClickhandler.destroy();
                    }
                    this._editMode = false;
                }
            }

            extent.setHighlighted = setHighlighted;

            enhanceWithListeners(extent);

            extent.setEditMode(false);

        }

        _.EllipsePrimitive.prototype.setEditable = function() {

            if(this.setEditMode) {
                return;
            }

            var ellipse = this;
            var scene = drawHelper._scene;

            ellipse.asynchronous = false;

            drawHelper.registerEditableShape(ellipse);

            ellipse.setEditMode = function(editMode) {
                // if no change
                if(this._editMode == editMode) {
                    return;
                }
                drawHelper.disableAllHighlights();
                // display markers
                if(editMode) {
                    // make sure all other shapes are not in edit mode before starting the editing of this shape
                    drawHelper.setEdited(this);
                    var _self = this;
                    // create the markers and handlers for the editing
                    if(this._markers == null) {
                        var markers = new _.BillboardGroup(drawHelper, dragBillboard);
                        function getMarkerPositions() {
                            return Cesium.Shapes.computeEllipseBoundary(ellipsoid, ellipse.getCenter(), ellipse.getSemiMajorAxis(), ellipse.getSemiMinorAxis(), ellipse.getRotation() + Math.PI / 2, Math.PI / 2.0).splice(0, 4);
                        }
                        function onEdited() {
                            ellipse.executeListeners({name: 'onEdited', center: ellipse.getCenter(), semiMajorAxis: ellipse.getSemiMajorAxis(), semiMinorAxis: ellipse.getSemiMinorAxis(), rotation: 0});
                        }
                        var handleMarkerChanges = {
                            dragHandlers: {
                                onDrag: function(index, position) {
                                    var distance = Cesium.Cartesian3.distance(ellipse.getCenter(), position);
                                    if(index%2 == 0) {
                                        ellipse.setSemiMajorAxis(distance);
                                    } else {
                                        ellipse.setSemiMinorAxis(distance);
                                    }
                                    markers.updateBillboardsPositions(getMarkerPositions());
                                },
                                onDragEnd: function(index, position) {
                                    onEdited();
                                }
                            },
                            tooltip: function() {
                                return "Drag to change the excentricity and radius";
                            }
                        };
                        markers.addBillboards(getMarkerPositions(), handleMarkerChanges);
                        this._markers = markers;
                        // add a handler for clicking in the globe
                        this._globeClickhandler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
                        this._globeClickhandler.setInputAction(
                            function (movement) {
                                var pickedObject = scene.pick(movement.position);
                                if(!(pickedObject && pickedObject.primitive)) {
                                    try{
										_self.setEditMode(false);
									}catch(e){
									}
                                }
                            }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

                        // set on top of the polygon
                        markers.setOnTop();
                    }
                    this._editMode = true;
                } else {
                    if(this._markers != null) {
                        this._markers.remove();
                        this._markers = null;
                        this._globeClickhandler.destroy();
                    }
                    this._editMode = false;
                }
            }

            ellipse.setHighlighted = setHighlighted;

            enhanceWithListeners(ellipse);

            ellipse.setEditMode(false);
        }

        _.CirclePrimitive.prototype.setEditable = function() {

            if(this.setEditMode) {
                return;
            }

            var circle = this;
            var scene = drawHelper._scene;

            circle.asynchronous = false;

            drawHelper.registerEditableShape(circle);

            circle.setEditMode = function(editMode) {
                // if no change
                if(this._editMode == editMode) {
                    return;
                }
                drawHelper.disableAllHighlights();
                // display markers
                if(editMode) {
                    // make sure all other shapes are not in edit mode before starting the editing of this shape
                    drawHelper.setEdited(this);
                    var _self = this;
                    // create the markers and handlers for the editing
                    if(this._markers == null) {
                        var markers = new _.BillboardGroup(drawHelper, dragBillboard);
                        function getMarkerPositions() {
                            //return Cesium.Shapes.computeCircleBoundary(ellipsoid, circle.getCenter(), circle.getRadius(), Math.PI / 2.0).splice(0, 4);
							var cg = new Cesium.CircleOutlineGeometry({
							   center : circle.getCenter(),
							   radius : circle.getRadius(),
							   granularity : Math.PI / 4
							});
							var geometry = Cesium.CircleOutlineGeometry.createGeometry(cg);
							var float64ArrayPositions = geometry.attributes.position.values;
							var positions = [].slice.call(float64ArrayPositions);                            
                            return positions;
                        }
                        function onEdited() {
                            circle.executeListeners({name: 'onEdited', center: circle.getCenter(), radius: circle.getRadius()});
                        }
                        var handleMarkerChanges = {
                            dragHandlers: {
                                onDrag: function(index, position) {
                                    circle.setRadius(Cesium.Cartesian3.distance(circle.getCenter(), position));
                                    markers.updateBillboardsPositions(getMarkerPositions());
                                },
                                onDragEnd: function(index, position) {
                                    onEdited();
                                }
                            },
                            tooltip: function() {
                                return "Drag to change the radius";
                            }
                        };
                        markers.addBillboards(getMarkerPositions(), handleMarkerChanges);
                        this._markers = markers;
                        // add a handler for clicking in the globe
                        this._globeClickhandler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
                        this._globeClickhandler.setInputAction(
                            function (movement) {
                                var pickedObject = scene.pick(movement.position);
                                if(!(pickedObject && pickedObject.primitive)) 
								{
                                    try{
										_self.setEditMode(false);
									}catch(e)
									{
										//console.log(e);
									}
                                }
                            }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

                        // set on top of the polygon
                        markers.setOnTop();
                    }
                    this._editMode = true;
                } else {
                    if(this._markers != null) {
                        this._markers.remove();
                        this._markers = null;
                        this._globeClickhandler.destroy();
                    }
                    this._editMode = false;
                }
            }

            circle.setHighlighted = setHighlighted;

            enhanceWithListeners(circle);

            circle.setEditMode(false);
        }

    }

    _.DrawHelperWidget = (function() {

        // constructor
        function _(drawHelper, options) {

            // container must be specified
            if(!(Cesium.defined(options.container))) {
                throw new Cesium.DeveloperError('Container is required');
            }

            var drawOptions = {
                buttons: [],
                markerIcon: "./img/glyphicons_242_google_maps.png",
                polylineIcon: "./img/glyphicons_097_vector_path_line.png",
                polygonIcon: "./img/glyphicons_096_vector_path_polygon.png",
                circleIcon: "./img/glyphicons_095_vector_path_circle.png",
                extentIcon: "./img/glyphicons_094_vector_path_square.png",
                saveIcon: "./img/glyphicons_save.png",
                clearIcon: "./img/glyphicons_067_cleaning.png",
                closeIcon: "./img/glyphicons_close.png",
                polylineDrawingOptions: defaultPolylineOptions,
                polygonDrawingOptions: defaultPolygonOptions,
                extentDrawingOptions: defaultExtentOptions,
                circleDrawingOptions: defaultCircleOptions
            };

            fillOptions(options, drawOptions);

            var _self = this;

            var toolbar = document.createElement('DIV');
            toolbar.className = "toolbar";
            options.container.appendChild(toolbar);

            function addIcon(id, url, title, callback) {
                var div = document.createElement('DIV');
                div.className = 'button';
                div.title = title;
                toolbar.appendChild(div);
                div.onclick = callback;
                var span = document.createElement('SPAN');
                div.appendChild(span);
                var image = document.createElement('IMG');
                image.src = url;
                span.appendChild(image);
                return div;
            }

            var scene = drawHelper._scene;

            var index;
            for(index = 0; index < options.buttons.length; index++) {
                addButton(options.buttons[index]);
            }
            // add a clear button at the end
            // add a divider first
            var div = document.createElement('DIV');
            div.className = 'divider';
            toolbar.appendChild(div);
            //addIcon('save', options.saveIcon, '保存', function() {
            //});
            addIcon('clear', options.clearIcon, '清除', function() {
                
                //scene.primitives.removeAll();
				drawHelper.clearPrimitive();
            });
            addIcon('close', options.closeIcon, '关闭', function() {
                //scene.primitives.removeAll();
				drawHelper.clearPrimitive();
				drawHelper.show(false);
				if(g_rulerButton)
				{
					$(g_rulerButton.viewModel.button).css('background-color', 'rgba(38, 38, 38, 0.75)');
					g_drawhelper_mode = undefined;
				}
            });

            function addButton(button) {

                if(button == 'marker') {
                    addIcon('marker', options.markerIcon, '地标', function() {
                        
                        drawHelper.startDrawingMarker({
                            callback: function(position) {
								
                                _self.executeListeners({name: 'markerCreated', position: position});
                            }
                        });
                    });
                } else if(button == 'polyline') {
                    addIcon('polyline', options.polylineIcon, '折线', function() {
                        drawHelper.startDrawingPolyline({
                            callback: function(positions) {
                                _self.executeListeners({name: 'polylineCreated', positions: positions});
                            }
                        });
                    });
                } else if(button == 'polygon') {
                    addIcon('polygon', options.polygonIcon, '多边形', function() {
                        drawHelper.startDrawingPolygon({
                            callback: function(positions) {
                                _self.executeListeners({name: 'polygonCreated', positions: positions});
                            }
                        });
                    });
                } else if(button == 'extent') {
                    addIcon('extent', options.extentIcon, '矩形范围', function() {
                        drawHelper.startDrawingExtent({
                            callback: function(positions) {
                                _self.executeListeners({name: 'extentCreated', positions: positions});
                            }
                        });
                    });
                } else if(button == 'circle') {
                    addIcon('circle', options.circleIcon, '圆', function() {
                        drawHelper.startDrawingCircle({
                            callback: function(center, radius) {
                                _self.executeListeners({name: 'circleCreated', center: center, radius: radius});
                            }
                        });
                    });
                }

            }

            enhanceWithListeners(this);

        }

        return _;

    })();

    _.prototype.addToolbar = function(container, options) {
        options = copyOptions(options, {container: container});
        return new _.DrawHelperWidget(this, options);
    }

    function getExtent(mn, mx) {
        var e = new Cesium.Rectangle();
		
        // Re-order so west < east and south < north
        e.west = Math.min(mn.longitude, mx.longitude);
        e.east = Math.max(mn.longitude, mx.longitude);
        e.south = Math.min(mn.latitude, mx.latitude);
        e.north = Math.max(mn.latitude, mx.latitude);

        // Check for approx equal (shouldn't require abs due to re-order)
        var epsilon = Cesium.Math.EPSILON7;

        if ((e.east - e.west) < epsilon) {
            e.east += epsilon * 2.0;
        }

        if ((e.north - e.south) < epsilon) {
            e.north += epsilon * 2.0;
        }

        return e;
    };

    function createTooltip(frameDiv) {

        var tooltip = function(frameDiv) {

            var div = document.createElement('DIV');
            div.className = "twipsy right";

            var arrow = document.createElement('DIV');
            arrow.className = "twipsy-arrow";
            div.appendChild(arrow);

            var title = document.createElement('DIV');
            title.className = "twipsy-inner";
            div.appendChild(title);

            this._div = div;
            this._title = title;
			
            // add to frame div and display coordinates
            frameDiv.appendChild(div);
			//$(div).attr('id', 'drawhelp2d_tooltip');
        }

        tooltip.prototype.setVisible = function(visible) {
            this._div.style.display = visible ? 'block' : 'none';
        }
        tooltip.prototype.destroy = function(visible) {
            $(this._div).remove();
        }

        tooltip.prototype.showAt = function(position, message) {
            if(position && message) {
                this.setVisible(true);
                this._title.innerHTML = message;
                this._div.style.left = position.x + 10 + "px";
                this._div.style.top = (position.y - this._div.clientHeight / 2) + "px";
            }
        }

        return new tooltip(frameDiv);
    }


    function clone(from, to) {
        if (from == null || typeof from != "object") return from;
        if (from.constructor != Object && from.constructor != Array) return from;
        if (from.constructor == Date || from.constructor == RegExp || from.constructor == Function ||
            from.constructor == String || from.constructor == Number || from.constructor == Boolean)
            return new from.constructor(from);

        to = to || new from.constructor();

        for (var name in from) {
            to[name] = typeof to[name] == "undefined" ? clone(from[name], null) : to[name];
        }

        return to;
    }
    
    function fillOptions(options, defaultOptions) {
        options = options || {};
        var option;
        for(option in defaultOptions) {
            if(options[option] === undefined) {
                options[option] = clone(defaultOptions[option]);
            }
        }
    }

    // shallow copy
    function copyOptions(options, defaultOptions) {
        var newOptions = clone(options), option;
        for(option in defaultOptions) {
            if(newOptions[option] === undefined) {
                newOptions[option] = clone(defaultOptions[option]);
            }
        }
        return newOptions;
    }

    function setListener(primitive, type, callback) {
        primitive[type] = callback;
    }

    function enhanceWithListeners(element) {

        element._listeners = {};

        element.addListener = function(name, callback) {
            this._listeners[name] = (this._listeners[name] || []);
            this._listeners[name].push(callback);
            return this._listeners[name].length;
        }

        element.executeListeners = function(event, defaultCallback) {
            if(this._listeners[event.name] && this._listeners[event.name].length > 0) {
                var index = 0;
                for(;index < this._listeners[event.name].length; index++) {
                    this._listeners[event.name][index](event);
                }
            } else {
                if(defaultCallback) {
                    defaultCallback(event);
                }
            }
        }

    }

    return _;
})();

