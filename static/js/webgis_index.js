var g_host = "http://localhost:88/";
var g_selected_obj_id;
var g_selected_obj_pos;
var g_view_extent;
var g_czml_towers = {};
var g_geojson_towers = {"type": "FeatureCollection","features": []};
var g_gltf_models = {};
$(function() {

	var providerViewModels = [];
	//providerViewModels.push(new Cesium.ImageryProviderViewModel({
				//name : 'OSM卫星图',
				//iconUrl : 'img/wmts-sat.png',
				//tooltip : 'OSM卫星图',
				//creationFunction : function() {
					//return new Cesium.OpenStreetMapImageryProvider({
						////url :  g_host + 'wmts',
					//});
				//}
			//}));
	providerViewModels.push(new Cesium.ImageryProviderViewModel({
				name : '地图',
				iconUrl : 'img/wmts-map.png',
				tooltip : '地图',
				creationFunction : function() {
					return new WMTSImageryProvider({
						url :  g_host + 'wmts',
						imageType:'google_map',
					});
				}
			}));
	providerViewModels.push(new Cesium.ImageryProviderViewModel({
				name : '卫星图',
				iconUrl : 'img/wmts-sat.png',
				tooltip : '卫星图',
				creationFunction : function() {
					return new WMTSImageryProvider({
						url :  g_host + 'wmts',
						imageType:'google_sat',
					});
				}
			}));
	//providerViewModels.push(new Cesium.ImageryProviderViewModel({
				//name : 'YNCFT',
				//iconUrl : 'img/wmts.png',
				//tooltip : 'YNCFT',
				//creationFunction : function() {
					//return new ArcgisTileImageryProvider({
						//url : g_host + 'arcgistile',
					//});
				//}
			//}));
	//providerViewModels.push(new Cesium.ImageryProviderViewModel({
		//name : 'Bing Maps Aerial',
		//iconUrl : 'img/bingAerial.png',
		//tooltip : 'Bing Maps aerial imagery \nhttp://www.bing.com/maps',
		//creationFunction : function() {
			//return new Cesium.BingMapsImageryProvider({
				//url : 'http://dev.virtualearth.net',
				//mapStyle : Cesium.BingMapsStyle.AERIAL
				////proxy : proxyIfNeeded
			//});
		//}
	//}));
	
	//providerViewModels.push(new Cesium.ImageryProviderViewModel({
		//name : 'Bing Maps Aerial with Labels',
		//iconUrl : 'img/bingAerialLabels.png',
		//tooltip : 'Bing Maps aerial imagery with label overlays \nhttp://www.bing.com/maps',
		//creationFunction : function() {
			//return new Cesium.BingMapsImageryProvider({
				//url : 'http://dev.virtualearth.net',
				//mapStyle : Cesium.BingMapsStyle.AERIAL_WITH_LABELS
				////proxy : proxyIfNeeded
			//});
		//}
	//}));
	
	var viewer = new Cesium.Viewer('cesiumContainer',{
		baseLayerPicker:true,
		imageryProviderViewModels:providerViewModels,
		terrainProvider:new Cesium.CesiumTerrainProvider({
			url: g_host + "terrain"
		})
	});
	
	var scene = viewer.scene;
	var ellipsoid = scene.primitives.centralBody.ellipsoid;
	
	//var west = Cesium.Math.toRadians(102.70);
	//var south = Cesium.Math.toRadians(25.04);
	//var east = Cesium.Math.toRadians(103.720);
	//var north = Cesium.Math.toRadians(25.06);

	//var extent = new Cesium.Extent(west, south, east, north);
	//scene.camera.controller.viewExtent(extent, ellipsoid);
	
	
	if(true) return;
	
	
	
	//var handler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
	//handler.setInputAction(
		//function (movement) {
			//var pick = scene.pick(movement.endPosition);
			//if (Cesium.defined(pick) && Cesium.defined(pick.node) && Cesium.defined(pick.mesh)) {
				//console.log('node: ' + pick.node.name + '. mesh: ' + pick.mesh.name);
			//}
		//},
		//Cesium.ScreenSpaceEventType.MOUSE_MOVE
	//);
	var line_id = 'AF77864E-B8D5-479F-896B-C5F5DFE3450F';
	LoadTowerByLineId(viewer, ellipsoid, line_id);
	//viewer.extend(Cesium.viewerDynamicObjectMixin);
	TowerInfoMixin(viewer);
	
	
	
	//viewer.homeButton.viewModel.command.beforeExecute.addEventListener(function(commandInfo){
		//if(viewer.selectedObject)
		//{
			//g_selected_obj_id = viewer.selectedObject.id;
			//g_selected_obj_pos = viewer.selectedObject.position._value;
		//}
		//commandInfo.cancel = false;
		//viewer.selectedObject = undefined;
	//});
	
	//viewer.homeButton.viewModel.command.afterExecute.addEventListener(function(commandInfo){
		//FlyToExtent(scene, g_view_extent['west'], g_view_extent['south'], g_view_extent['east'], g_view_extent['north']);
		////commandInfo.cancel = false;
	//});
	
	
	//var handler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
	//handler.setInputAction(
		//function (movement) {
		
			//if(viewer.selectedObject)
			//{
				//g_selected_obj_id = viewer.selectedObject.id;
				//g_selected_obj_pos = ellipsoid.cartesianToCartographic(viewer.selectedObject.position._value);
				//console.log(g_selected_obj_id);
				////console.log(g_selected_obj_pos);
				//LoadTowerModelByTowerId(viewer, g_selected_obj_id);
			//}
			//else
			//{
				//g_selected_obj_id = null;
				//g_selected_obj_pos = null;
			//}
		//}, Cesium.ScreenSpaceEventType.LEFT_CLICK//LEFT_DOUBLE_CLICK,LEFT_CLICK
	//);
	//handler.setInputAction(
		//function (movement) {
			//if(g_selected_obj_id)
			//{
				//LookAtTarget(scene, g_selected_obj_id);
			//}
		//}, Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK//LEFT_DOUBLE_CLICK,LEFT_CLICK
	//);
	
});


function CreateTowerCzmlFromGeojson(geojson)
{
	var ret = [];
	for(var i in geojson)
	{
		var tower = geojson[i];
		var cz = {}
		cz['id'] = tower['properties']['id'];
		cz['name'] = tower['properties']['tower_name'];
		cz['position'] = {};
		cz['position']['cartographicDegrees'] = [tower['geometry']['coordinates'][0], tower['geometry']['coordinates'][1], tower['properties']['geo_z']];
		cz['point'] = {};
		cz['point']['color'] = {'rgba':[255, 255, 0, 255]};
		cz['point']['outlineColor'] = {'rgba': [0, 0, 0, 255]};
		cz['point']['outlineWidth'] = 1;
		cz['point']['pixelSize'] = 10;
		cz['point']['show'] = {'boolean':true};
		cz['label'] = {};
		cz['label']['fillColor'] = {'rgba':[0, 255, 0, 255]};
		cz['label']['horizontalOrigin'] = 'LEFT';
		cz['label']['outlineColor'] = {'rgba':[0, 0, 0, 255]};
		cz['label']['pixelOffset'] = {'cartesian2':[10.0, 0.0]};
		cz['label']['scale'] = 0.5;
		cz['label']['show'] = {'boolean':true};
		cz['label']['style'] = 'FILL';
		cz['label']['text'] = tower['properties']['tower_name'];
		cz['label']['verticalOrigin'] = 'CENTER';
		cz['description'] = tower['properties']['tower_name'];
		ret.push(cz);
	}
	return ret;
}

function LoadTowerByLineId(viewer, ellipsoid, line_id)
{
	var geo_cond = {'db':'kmgd', 'collection':'towers', 'properties.line_id':line_id};
	var czml_cond = {'db':'kmgd', 'collection':'towers','use_czml':true, 'properties.line_id':line_id};
	var ext_cond = {'db':'kmgd', 'collection':'towers','get_extext':true, 'properties.line_id':line_id};
	MongoFind( ext_cond, 
		function(data){
			g_view_extent = data;
			FlyToExtent(viewer.scene, g_view_extent['west'], g_view_extent['south'], g_view_extent['east'], g_view_extent['north']);
			console.log(g_view_extent);
	});
	MongoFind( geo_cond, 
		function(data){
			for(var i in data)
			{
				g_geojson_towers["features"].push(data[i]);
			}
			g_czml_towers[line_id] = CreateTowerCzmlFromGeojson(data);
			//console.log(g_czml_towers[line_id]);
			//viewer.dataSources.removeAll();
			var dataSource = new Cesium.CzmlDataSource();
			dataSource.load(g_czml_towers[line_id]);
			viewer.dataSources.add(dataSource);
	});
}


function LookAtTarget(scene, id)
{
	//scene.camera.controller.lookAt(scene.camera.position, target, scene.camera.up);
	var ellipsoid = scene.primitives.centralBody.ellipsoid;
	
	for(var i in g_geojson_towers['features'])
	{
		var tower = g_geojson_towers['features'][i];
		if(tower['properties']['id'] == id)
		{
			var x = tower['geometry']['coordinates'][0];
			var y = tower['geometry']['coordinates'][1];
			var z = tower['properties']['geo_z'];
			FlyToPoint(scene, x, y, z, 1.05, 4000);
			break;
		}
	}
}
function LookAtTargetExtent(scene, id, dx, dy)
{
	var ellipsoid = scene.primitives.centralBody.ellipsoid;
	for(var i in g_geojson_towers['features'])
	{
		var tower = g_geojson_towers['features'][i];
		if(tower['properties']['id'] == id)
		{
			var x = tower['geometry']['coordinates'][0];
			var y = tower['geometry']['coordinates'][1];
			var west = Cesium.Math.toRadians(x - dx);
			var south = Cesium.Math.toRadians(y - dy);
			var east = Cesium.Math.toRadians(x + dx);
			var north = Cesium.Math.toRadians(y + dy);
			var extent = new Cesium.Extent(west, south, east, north);
			//scene.camera.controller.viewExtent(extent, ellipsoid);
			FlyToExtent(scene, west, south, east, north);
			break;
		}
	}
}


function FlyToPoint(scene, x, y, z, factor, duration)
{
	var destination = Cesium.Cartographic.fromDegrees(x,  y,  z * factor);
	var flight = Cesium.CameraFlightPath.createAnimationCartographic(scene, {
		destination : destination,
		duration	:duration
	});
	scene.animations.add(flight);
}

function FlyToPointCart3(scene, pos, duration)
{
	//var destination = scene.primitives.centralBody.ellipsoid.cartesianToCartographic(cart3);
	var flight = Cesium.CameraFlightPath.createAnimationCartographic(scene, {
		destination	:	pos,
		duration	:	duration
		//up			:	scene.camera.up,
		//direction	:	scene.camera.direction
	});
	scene.animations.add(flight);
}

function FlyToExtent(scene, west, south, east, north)
{
	var west1 = Cesium.Math.toRadians(west);
	var south1 = Cesium.Math.toRadians(south);
	var east1 = Cesium.Math.toRadians(east);
	var north1 = Cesium.Math.toRadians(north);

	var extent = new Cesium.Extent(west1, south1, east1, north1);
	var flight = Cesium.CameraFlightPath.createAnimationExtent(scene, {
		destination : extent
	});
	scene.animations.add(flight);
}

function LoadTowerModelByTowerId(viewer, tower_id)
{
	var scene = viewer.scene;
	var ellipsoid = scene.primitives.centralBody.ellipsoid;
	
	for(var i in g_geojson_towers['features'])
	{
		var tower = g_geojson_towers['features'][i];
		//console.log(tower);
		if(tower['properties']['id'] == tower_id)
		{
			if(!g_gltf_models[tower_id])
			{
				var model = CreateTowerModel(
					scene, 
					ellipsoid, 
					GetModelUrl(tower['properties']['model_code_height']), 
					tower['geometry']['coordinates'][0],  
					tower['geometry']['coordinates'][1], 
					tower['properties']['geo_z'] ,  
					tower['properties']['rotate'],
					10
				);
				g_gltf_models[tower_id] = model;
				console.log("load model for [" + tower_id + "]");
			}
			break;
		}
	}
}

function LoadTowerModelByLineId(viewer, ellipsoid, line_id)
{
	var scene = viewer.scene;
	scene.primitives.removeAll(); // Remove previous model
	
	var idx = 0;
	var labels = new Cesium.LabelCollection();
	
	var cond = {'db':'kmgd', 'collection':'towers', 'properties.line_id':line_id};
	MongoFind( cond, 
		function(data){
			for(var i in data)
			{
				var t = data[i];
				var label = labels.add({
					position : ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(t['geometry']['coordinates'][0],  t['geometry']['coordinates'][1],  t['properties']['geo_z'])),
					text     : t['properties']['tower_name'],
					fillColor : { red : 0.0, blue : 1.0, green : 0.0, alpha : 1.0 }
				});
				
				var model = CreateTowerModel(scene, ellipsoid, GetModelUrl(t['properties']['model_code_height']), t['geometry']['coordinates'][0],  t['geometry']['coordinates'][1], t['properties']['geo_z'] ,  t['properties']['rotate'] );
				if(idx > 10)
				{
					FlyToPoint(scene, t['geometry']['coordinates'][0],  t['geometry']['coordinates'][1],  t['properties']['geo_z'] );
					var controller = scene.screenSpaceCameraController;
					//controller.ellipsoid = Cesium.Ellipsoid.UNIT_SPHERE;
					//controller.enableTilt = true;
					var r = t['properties']['geo_z'];
					//controller.minimumZoomDistance = r ;
					break;
				}
				idx++;
			}
			scene.primitives.add(labels);
	});
}

function MongoFind(data, success)
{
	//$.ajaxSetup( { "async": true, scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8" } );
	$.post(g_host + 'post', JSON.stringify(data), function( data1 ){
		ret = JSON.parse(decodeURIComponent(data1));
		if(ret.result)
		{
			console.log(ret.result);
			success([]);
		}
		else
		{
			success(ret);
		}
	}, 'text');
}


function ReadTable(url, success, failed)
{
	$.ajaxSetup( { "async": true, scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8" } );
	$.getJSON( url)
	.done(function( data ){
		success(data);
	})
	.fail(function( jqxhr ){
		failed();
	});	
}


function GetModelUrl(model_code_height)
{
	return g_host + "gltf/" + model_code_height + ".json" ;
	//return "http://localhost:88/gltf/test.json";//?random=" + $.uuid();
}

function CreateTowerModel(scene, ellipsoid, modelurl,  lng,  lat,  height, rotate, scale) 
{

	height = Cesium.defaultValue(height, 0.0);
	var cart3 = ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(lng, lat, height));
	var modelMatrix = Cesium.Transforms.eastNorthUpToFixedFrame(cart3);
	var quat = Cesium.Quaternion.fromAxisAngle(Cesium.Cartesian3.UNIT_Z, Cesium.Math.toRadians(rotate - 90));
	var mat3 = Cesium.Matrix3.fromQuaternion(quat);
	var mat4 = Cesium.Matrix4.fromRotationTranslation(mat3, Cesium.Cartesian3.ZERO);
	var m = Cesium.Matrix4.multiplyTransformation(modelMatrix, mat4);
	var model = scene.primitives.add(Cesium.Model.fromGltf({
		url : modelurl,
		modelMatrix : m,
		scale:scale
	}));
	
	model.readyToRender.addEventListener(function(model) {
		// Play and loop all animations at half-spead
		model.activeAnimations.addAll({
			speedup : 0.5,
			loop : Cesium.ModelAnimationLoop.REPEAT
		});

		//// Zoom to model
		//var worldBoundingSphere = model.computeWorldBoundingSphere();
		//var center = worldBoundingSphere.center;
		//var transform = Cesium.Transforms.eastNorthUpToFixedFrame(center);
		//var camera = scene.camera;
		//camera.transform = transform;
		//camera.controller.constrainedAxis = Cesium.Cartesian3.UNIT_Z;
		//var controller = scene.screenSpaceCameraController;
		//controller.ellipsoid = Cesium.Ellipsoid.UNIT_SPHERE;
		//controller.enableTilt = true;
		//var r = 1.25 * Math.max(worldBoundingSphere.radius, camera.frustum.near);
		//controller.minimumZoomDistance = r * 0.25;
		//camera.controller.lookAt(new Cesium.Cartesian3(r, r, r), Cesium.Cartesian3.ZERO, Cesium.Cartesian3.UNIT_Z);
	});
	return model;
}


function TowerInfoMixin(viewer) 
{
	if (!Cesium.defined(viewer)) {
		throw new Cesium.DeveloperError('viewer is required.');
	}
	if (viewer.hasOwnProperty('trackedObject')) {
		throw new Cesium.DeveloperError('trackedObject is already defined by another mixin.');
	}
	if (viewer.hasOwnProperty('selectedObject')) {
		throw new Cesium.DeveloperError('selectedObject is already defined by another mixin.');
	}

	var infoBox = viewer.infoBox;
	var infoBoxViewModel = Cesium.defined(infoBox) ? infoBox.viewModel : undefined;

	var selectionIndicator = viewer.selectionIndicator;
	var selectionIndicatorViewModel = Cesium.defined(selectionIndicator) ? selectionIndicator.viewModel : undefined;

	var enableInfoOrSelection = Cesium.defined(infoBox) || Cesium.defined(selectionIndicator);

	var eventHelper = new Cesium.EventHelper();
	var dynamicObjectView;

	function trackSelectedObject() {
		viewer.trackedObject = viewer.selectedObject;
	}

	function clearTrackedObject() {
		viewer.trackedObject = undefined;
	}

	function clearSelectedObject() {
		viewer.selectedObject = undefined;
	}

	function clearObjects() {
		viewer.trackedObject = undefined;
		viewer.selectedObject = undefined;
	}

	if (Cesium.defined(infoBoxViewModel)) {
		eventHelper.add(infoBoxViewModel.cameraClicked, trackSelectedObject);
		eventHelper.add(infoBoxViewModel.closeClicked, clearSelectedObject);
	}

	var scratchVertexPositions;
	var scratchBoundingSphere;

	function onTick(clock) {
		var time = clock.currentTime;
		if (Cesium.defined(dynamicObjectView)) {
			dynamicObjectView.update(time);
		}

		var selectedObject = viewer.selectedObject;
		var showSelection = Cesium.defined(selectedObject) && enableInfoOrSelection;
		if (showSelection) {
			var oldPosition = Cesium.defined(selectionIndicatorViewModel) ? selectionIndicatorViewModel.position : undefined;
			var position;
			var enableCamera = false;

			if (selectedObject.isAvailable(time)) {
				if (Cesium.defined(selectedObject.position)) {
					position = selectedObject.position.getValue(time, oldPosition);
					enableCamera = Cesium.defined(position) && (viewer.trackedObject !== viewer.selectedObject);
				} else if (Cesium.defined(selectedObject.vertexPositions)) {
					scratchVertexPositions = selectedObject.vertexPositions.getValue(time, scratchVertexPositions);
					scratchBoundingSphere = Cesium.BoundingSphere.fromPoints(scratchVertexPositions, scratchBoundingSphere);
					position = scratchBoundingSphere.center;
					// Can't track scratch positions: "enableCamera" is false.
				}
				// else "position" is undefined and "enableCamera" is false.
			}
			// else "position" is undefined and "enableCamera" is false.

			if (Cesium.defined(selectionIndicatorViewModel)) {
				selectionIndicatorViewModel.position = position;
			}

			if (Cesium.defined(infoBoxViewModel)) {
				infoBoxViewModel.enableCamera = enableCamera;
				infoBoxViewModel.isCameraTracking = (viewer.trackedObject === viewer.selectedObject);

				if (Cesium.defined(selectedObject.description)) {
					infoBoxViewModel.descriptionRawHtml = Cesium.defaultValue(selectedObject.description.getValue(time), '');
				} else {
					infoBoxViewModel.descriptionRawHtml = '';
				}
			}
		}

		if (Cesium.defined(selectionIndicatorViewModel)) {
			selectionIndicatorViewModel.showSelection = showSelection;
			selectionIndicatorViewModel.update();
		}

		if (Cesium.defined(infoBoxViewModel)) {
			infoBoxViewModel.showInfo = showSelection;
		}
	}
	eventHelper.add(viewer.clock.onTick, onTick);

	function pickDynamicObject(e) {
		var picked = viewer.scene.pick(e.position);
		if (Cesium.defined(picked)) {
			var id = Cesium.defaultValue(picked.id, picked.primitive.id);
			if (id instanceof Cesium.DynamicObject) {
				return id;
			}
		}
	}

	function trackObject(dynamicObject) {
		if (Cesium.defined(dynamicObject) && Cesium.defined(dynamicObject.position)) {
			viewer.trackedObject = dynamicObject;
		}
	}

	function pickAndTrackObject(e) {
		var dynamicObject = pickDynamicObject(e);
		if (Cesium.defined(dynamicObject)) {
			trackObject(dynamicObject);
			var id = dynamicObject.id;
			console.log('track id=' + id);
			LookAtTarget(viewer.scene, id);
			
		}
	}

	function pickAndSelectObject(e) {
		viewer.selectedObject = pickDynamicObject(e);
		
		if (Cesium.defined(viewer.selectedObject)) 
		{
			var id = viewer.selectedObject.id;
			g_selected_obj_id = id;
			console.log('selected id=' + id);
			LoadTowerModelByTowerId(viewer, id);
		}
	}

	if (Cesium.defined(viewer.homeButton)) {
		eventHelper.add(viewer.homeButton.viewModel.command.beforeExecute, clearTrackedObject);
		eventHelper.add(viewer.homeButton.viewModel.command.afterExecute, function(commandInfo){
			if (Cesium.defined(g_view_extent))
			{
				FlyToExtent(viewer.scene, g_view_extent['west'], g_view_extent['south'], g_view_extent['east'], g_view_extent['north']);
				if (Cesium.defined(g_selected_obj_id))
				{
					//LookAtTargetExtent(viewer.scene, g_selected_obj_id, 0.001, 0.001);
					g_selected_obj_id = undefined;
				}
			}
		});
	}

	if (Cesium.defined(viewer.geocoder)) {
		eventHelper.add(viewer.geocoder.viewModel.search.beforeExecute, clearObjects);
	}

	function onDynamicCollectionChanged(collection, added, removed) {
		var length = removed.length;
		for (var i = 0; i < length; i++) {
			var removedObject = removed[i];
			if (viewer.trackedObject === removedObject) {
				viewer.homeButton.viewModel.command();
			}
			if (viewer.selectedObject === removedObject) {
				viewer.selectedObject = undefined;
			}
		}
	}

	function dataSourceAdded(dataSourceCollection, dataSource) {
		var dynamicObjectCollection = dataSource.getDynamicObjectCollection();
		dynamicObjectCollection.collectionChanged.addEventListener(onDynamicCollectionChanged);
	}

	function dataSourceRemoved(dataSourceCollection, dataSource) {
		var dynamicObjectCollection = dataSource.getDynamicObjectCollection();
		dynamicObjectCollection.collectionChanged.removeEventListener(onDynamicCollectionChanged);

		if (Cesium.defined(viewer.trackedObject)) {
			if (dynamicObjectCollection.getById(viewer.trackedObject.id) === viewer.trackedObject) {
				viewer.homeButton.viewModel.command();
			}
		}

		if (Cesium.defined(viewer.selectedObject)) {
			if (dynamicObjectCollection.getById(viewer.selectedObject.id) === viewer.selectedObject) {
				viewer.selectedObject = undefined;
			}
		}
	}

	var dataSources = viewer.dataSources;
	var dataSourceLength = dataSources.length;
	for (var i = 0; i < dataSourceLength; i++) {
		dataSourceAdded(dataSources, dataSources.get(i));
	}

	eventHelper.add(viewer.dataSources.dataSourceAdded, dataSourceAdded);
	eventHelper.add(viewer.dataSources.dataSourceRemoved, dataSourceRemoved);

	viewer.screenSpaceEventHandler.setInputAction(pickAndSelectObject, Cesium.ScreenSpaceEventType.LEFT_CLICK);
	viewer.screenSpaceEventHandler.setInputAction(pickAndTrackObject, Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK);

	viewer.trackedObject = undefined;

	viewer.selectedObject = undefined;

	Cesium.knockout.track(viewer, ['trackedObject', 'selectedObject']);

	var knockoutSubscriptions = [];

	knockoutSubscriptions.push(Cesium.subscribeAndEvaluate(viewer, 'trackedObject', function(value) {
		var scene = viewer.scene;
		var sceneMode = scene.frameState.mode;
		var isTracking = Cesium.defined(value);

		if (sceneMode === Cesium.SceneMode.COLUMBUS_VIEW || sceneMode === Cesium.SceneMode.SCENE2D) {
			scene.screenSpaceCameraController.enableTranslate = !isTracking;
		}

		if (sceneMode === Cesium.SceneMode.COLUMBUS_VIEW || sceneMode === Cesium.SceneMode.SCENE3D) {
			scene.screenSpaceCameraController.enableTilt = !isTracking;
		}

		if (isTracking && Cesium.defined(value.position)) {
			dynamicObjectView = new Cesium.DynamicObjectView(value, scene, viewer.centralBody.ellipsoid);
		} else {
			dynamicObjectView = undefined;
		}
	}));

	knockoutSubscriptions.push(Cesium.subscribeAndEvaluate(viewer, 'selectedObject', function(value) {
		if (Cesium.defined(value)) {
			if (Cesium.defined(infoBoxViewModel)) {
				infoBoxViewModel.titleText = Cesium.defined(value.name) ? value.name : value.id;
			}

			if (Cesium.defined(selectionIndicatorViewModel)) {
				selectionIndicatorViewModel.animateAppear();
			}
		} else {
			if (Cesium.defined(selectionIndicatorViewModel)) {
				selectionIndicatorViewModel.animateDepart();
			}
		}
	}));

	viewer.destroy = Cesium.wrapFunction(viewer, viewer.destroy, function() {
		eventHelper.removeAll();

		var i;
		for (i = 0; i < knockoutSubscriptions.length; i++) {
			knockoutSubscriptions[i].dispose();
		}

		viewer.screenSpaceEventHandler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_CLICK);
		viewer.screenSpaceEventHandler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK);

		var dataSources = viewer.dataSources;
		var dataSourceLength = dataSources.length;
		for (i = 0; i < dataSourceLength; i++) {
			dataSourceRemoved(dataSources, dataSources.get(i));
		}
	});
}

	


