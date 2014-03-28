var g_host = "http://localhost:88/";
var g_selected_obj_id;
var g_selected_obj_pos;
var g_view_extent;
var g_czml_towers = {};
var g_geojson_towers = {"type": "FeatureCollection","features": []};
var g_gltf_models = {};
$(function() {

	var providerViewModels = [];
	providerViewModels.push(new Cesium.ImageryProviderViewModel({
				name : 'WMTS',
				iconUrl : 'img/wmts.png',
				tooltip : 'WMTS',
				creationFunction : function() {
					return new WMTSImageryProvider({
						url :  g_host + 'wmts',
					});
				}
			}));
	providerViewModels.push(new Cesium.ImageryProviderViewModel({
				name : 'YNCFT',
				iconUrl : 'img/wmts.png',
				tooltip : 'YNCFT',
				creationFunction : function() {
					return new ArcgisTileImageryProvider({
						url : g_host + 'arcgistile',
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
	
	
	//if(true) return;
	
	
	
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
	//LoadTowerModel(viewer, ellipsoid, line_id);
	viewer.extend(Cesium.viewerDynamicObjectMixin);
	
	viewer.homeButton.viewModel.command.beforeExecute.addEventListener(function(commandInfo){
		//FlyToExtent(viewer.scene, 102.9554, 24.8844, 102.9842, 24.9037);
		//viewer.trackedObject = null;
		if(viewer.selectedObject)
		{
			g_selected_obj_id = viewer.selectedObject.id;
			g_selected_obj_pos = viewer.selectedObject.position._value;
		}
		commandInfo.cancel = false;
		viewer.selectedObject = undefined;
	});
	
	viewer.homeButton.viewModel.command.afterExecute.addEventListener(function(commandInfo){
		FlyToExtent(scene, g_view_extent['west'], g_view_extent['south'], g_view_extent['east'], g_view_extent['north']);
		//commandInfo.cancel = false;
	});
	
	
	var handler = new Cesium.ScreenSpaceEventHandler(scene.canvas);
	handler.setInputAction(
		function (movement) {
		
			if(viewer.selectedObject)
			{
				g_selected_obj_id = viewer.selectedObject.id;
				g_selected_obj_pos = ellipsoid.cartesianToCartographic(viewer.selectedObject.position._value);
				console.log(g_selected_obj_id);
				//console.log(g_selected_obj_pos);
				LoadTowerModelByTowerId(viewer, g_selected_obj_id);
			}
			else
			{
				g_selected_obj_id = null;
				g_selected_obj_pos = null;
			}
		}, Cesium.ScreenSpaceEventType.LEFT_CLICK//LEFT_DOUBLE_CLICK,LEFT_CLICK
	);
	handler.setInputAction(
		function (movement) {
			if(g_selected_obj_id)
			{
				LookAtTarget(scene, g_selected_obj_id);
			}
		}, Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK//LEFT_DOUBLE_CLICK,LEFT_CLICK
	);
	
});




function LoadTowerByLineId(viewer, ellipsoid, line_id)
{
	var geo_cond = {'db':'kmgd', 'collection':'towers', 'properties.line_id':line_id};
	var czml_cond = {'db':'kmgd', 'collection':'towers','use_czml':true, 'properties.line_id':line_id};
	var ext_cond = {'db':'kmgd', 'collection':'towers','get_extext':true, 'properties.line_id':line_id};
	MongoFind( geo_cond, 
		function(data){
			for(var i in data)
			{
				g_geojson_towers["features"].push(data[i]);
			}
	});
	MongoFind( czml_cond, 
		function(data){
			g_czml_towers[line_id] = data;
			viewer.dataSources.removeAll();
			//var geojson = {};
			//geojson['type'] =  'FeatureCollection';
			//geojson['features'] =  data;
			//var dataSource = new Cesium.GeoJsonDataSource();
			//var defaultPoint = dataSource.defaulPoint;
			//dataSource.load(geojson);
			var dataSource = new Cesium.CzmlDataSource();
			dataSource.load(data);
			viewer.dataSources.add(dataSource);
	});
	MongoFind( ext_cond, 
		function(data){
			g_view_extent = data;
			FlyToExtent(viewer.scene, g_view_extent['west'], g_view_extent['south'], g_view_extent['east'], g_view_extent['north']);
			console.log('view extent = ' + g_view_extent);
	});
}

function LookAtTarget(scene, id)
{
	//scene.camera.controller.lookAt(scene.camera.position, target, scene.camera.up);
	var ellipsoid = scene.primitives.centralBody.ellipsoid;
	
	for(var i in g_geojson_towers['features'])
	{
		var tower = g_geojson_towers['features'][i];
		//console.log(tower);
		if(tower['properties']['id'] == id)
		{
			var x = tower['geometry']['coordinates'][0];
			var y = tower['geometry']['coordinates'][1];
			var z = tower['properties']['geo_z'];
			//var west = Cesium.Math.toRadians(x - dx);
			//var south = Cesium.Math.toRadians(y - dy);
			//var east = Cesium.Math.toRadians(x + dx);
			//var north = Cesium.Math.toRadians(y + dy);
			FlyToPoint(scene, x, y, z, 1.05, 4000);
			//var extent = new Cesium.Extent(west, south, east, north);
			//scene.camera.controller.viewExtent(extent, ellipsoid);
			//FlyToExtent(scene, west, south, east, north);
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

	


