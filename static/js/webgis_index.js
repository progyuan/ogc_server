var g_host = "http://localhost:88/";

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
	LoadTower(viewer, ellipsoid, line_id);
	LoadTowerModel(viewer, ellipsoid, line_id);
	viewer.extend(Cesium.viewerDynamicObjectMixin);
});

function LoadTower(viewer, ellipsoid, line_id)
{
	var cond = {'db':'kmgd', 'collection':'towers','use_czml':true, 'properties.line_id':line_id};
	MongoFind( cond, 
		function(data){
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
			viewer.homeButton.viewModel.command();
			
	});
	
}

function LoadTowerModel(viewer, ellipsoid, line_id)
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
				//console.log(t);
				var label = labels.add({
					position : ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(t['geometry']['coordinates'][0],  t['geometry']['coordinates'][1],  t['properties']['geo_z'])),
					text     : t['properties']['tower_name'],
					fillColor : { red : 0.0, blue : 1.0, green : 0.0, alpha : 1.0 }
				});
				
				//label.setScale(3.0);
				//console.log(t['tower_name'] + "=" + t['rotate']);
				
				var model = CreateTowerModel(scene, ellipsoid, GetModelUrl(t['properties']['model_code_height']), t['geometry']['coordinates'][0],  t['geometry']['coordinates'][1], t['properties']['geo_z'] ,  t['properties']['rotate'] );
				if(idx > 10)
				{
					var destination = Cesium.Cartographic.fromDegrees(t['geometry']['coordinates'][0],  t['geometry']['coordinates'][1],  t['properties']['geo_z'] * 1.5);
					var flight = Cesium.CameraFlightPath.createAnimationCartographic(scene, {
						destination : destination
					});
					scene.animations.add(flight);
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

	
	//var url = g_host + "get?table=TABLE_TOWER&line_id=" + line_id + "&area=" + area;
	//ReadTable(url, function(data){
		//var idx = 0;
        //var labels = new Cesium.LabelCollection();
		//for(var i in data)
		//{
			//var t = data[i];
			//var label = labels.add({
				//position : ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(t['geo_x'],  t['geo_y'], t['geo_z'])),
				//text     : t['tower_name'],
				//fillColor : { red : 0.0, blue : 1.0, green : 0.0, alpha : 1.0 }
			//});
			
			////label.setScale(3.0);
			//console.log(t['tower_name'] + "=" + t['rotate']);
			
			//var model = CreateTowerModel(scene, ellipsoid, GetModelUrl(t['model_code_height']), t['geo_x'],  t['geo_y'], t['geo_z'],  t['rotate'] );
			//if(idx > 10)
			//{
				//var destination = Cesium.Cartographic.fromDegrees(t['geo_x'],  t['geo_y'],  t['geo_z']*1.5);
				//var flight = Cesium.CameraFlightPath.createAnimationCartographic(scene, {
					//destination : destination
				//});
				//scene.animations.add(flight);
				//var controller = scene.screenSpaceCameraController;
				////controller.ellipsoid = Cesium.Ellipsoid.UNIT_SPHERE;
				////controller.enableTilt = true;
				//var r = t['geo_z'];
				//controller.minimumZoomDistance = r ;
				//break;
			//}
			//idx++;
		//}
		//scene.primitives.add(labels);

	//},
	//function(){
	
	//});

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

function CreateTowerModel(scene, ellipsoid, modelurl,  lng,  lat,  height, rotate) 
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
		scale:10
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

	


