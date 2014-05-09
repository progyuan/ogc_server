
var g_selected_obj_id;
var g_prev_selected_id;
var g_prev_selected_pos;
var g_view_extent;
var g_czmls = {};
//var g_geojson_towers = {"type": "FeatureCollection","features": []};
var g_geojsons = {};
var g_lines = [];
var g_segments = [];
var g_gltf_models = {};
var g_dlg_tower_info;
var g_contextmenu_metal;
var g_selected_metal_item;
var g_polylines_segments = [];
var g_use_catenary = true;
var g_validates = {};





$(function() {
	ShowProgressBar(true, 670, 200, '载入中', '正在载入，请稍候...');
	//if(true) return;
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
	providerViewModels.push(new Cesium.ImageryProviderViewModel({
				name : '地图',
				iconUrl : 'img/wmts-map.png',
				tooltip : '地图',
				creationFunction : function() {
					return new WMTSImageryProvider({
						//url :  g_host + 'wmts',
						url :  "http://cf-storage:88/" + 'wmts',
						imageType:'google_map',
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
		animation:false,
		baseLayerPicker:true,
		geocoder:false,
		timeline:false,
		imageryProviderViewModels:providerViewModels,
		terrainProvider:new Cesium.CesiumTerrainProvider({
			//url: g_host + "terrain"
			url: "http://cf-storage:88/" + "terrain"
		})
	});
	
	var scene = viewer.scene;
	var ellipsoid = scene.primitives.centralBody.ellipsoid;
	
	
	
	
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
	var line_name = '七罗I回';
	LoadTowerByLineName(viewer, ellipsoid, line_name);
	//viewer.extend(Cesium.viewerDynamicObjectMixin);
	TowerInfoMixin(viewer);

	var iframe = $('#tower_info_model').find('iframe');
	iframe.load(function(){
		var iframeDoc = iframe.contents().get(0);
		$(iframeDoc).off();
		$(iframeDoc).on('mousedown', function(e){
			for (var i = 1; i < 99; i++)
			{
				iframe[0].contentWindow.clearInterval(i);
			}
		});
	});
	//$(window).on('message',function(e) {
		////console.log('recv:' + text);
		//var text = e.originalEvent.data;
		//console.log('recv:' + text);
		//var obj = JSON.parse(text);
		//console.log(obj);
		
	//});
	
	g_validates['form_tower_info_base'] = $('#form_tower_info_base' ).validate({
		debug:true,
		errorElement:'div'
	});
	g_validates['form_tower_info_metal'] = $('#form_tower_info_metal' ).validate({
		debug:true,
		errorElement:'div'
	});
	
	$('#button_search_clear').on( 'click', function(){
		$('#input_search').val('');
	});
	$( "#input_search" ).autocomplete({
		minLength:2,
		delay: 500,
		_resizeMenu: function() {
			this.menu.element.outerHeight( 500 );
		},		
		source:function(request,  response)
		{
			var py_cond = {'db':'kmgd', 'collection':'*', 'action':'pinyinsearch', 'data':{'py':request.term}};
			$('#text_search_waiting').css('display','block');
			MongoFind( py_cond, 
				function(data){
					$('#text_search_waiting').css('display','none');
					response($.map( data, function( item, idx ) {
						var name = '';
						var pos;
						if(item.properties && item.properties.line_name) name = item.properties.line_name;
						if(item.properties && item.properties.tower_name) name = item.properties.tower_name;
						if(item.properties && item.properties.NAME) name = item.properties.NAME;
						if(item.geometry)
						{
							if(item.geometry.type == 'Point')
							{
								pos = item.geometry.coordinates;
							}
							if(item.geometry.type == 'LineString')
							{
								var idx = item.geometry.coordinates.length/2;
								pos = item.geometry.coordinates[idx];
							}
						}
						return {
						  label: name,
						  value: name,
						  pos:pos,
						  geojson:item
						};
					}));
					
			});
		},
		select: function( event, ui ) {
			//console.log(ui.item.pos);
			FlyToPoint(scene, ui.item.pos[0], ui.item.pos[1], 2000, 1.05, 4000);
			ShowSearchResult(viewer, ui.item.geojson);
		}
	});
	$('#button_search').on( 'click', function(){
			if($('#input_search').css('display') == 'none')
			{
				$('#input_search').show('slide',{}, 500, function(){
					$('#button_search_clear').css('display','block');
				});
				$('#button_search').css('background-color', '#00FF00');
				
			}else
			{
				$('#input_search').hide('slide',{}, 500, function(){
					$('#button_search_clear').css('display','none');
				});
				$('#button_search').css('background-color', '#FFFFFF');
			}
	});
	$('#button_search').on( 'mouseenter', function(){
		$('#button_search').css('background-color', '#00FFFF');
	});
	$('#button_search').on( 'mouseleave', function(){
		$('#button_search').css('background-color', '#FFFFFF');
		if($('#input_search').css('display') !== 'none')
		{
			$('#button_search').css('background-color', '#00FF00');
		}
	});
	
});

function ShowSearchResult(viewer, geojson)
{
	if(geojson['_id'])
	{
		if(geojson['properties'] && geojson['properties']['tower_name'])
		{
			if(!g_geojsons[geojson['_id']])
			{
				g_geojsons[geojson['_id']] = geojson;
			}
			if(!g_czmls[geojson['_id']])
			{
				g_czmls[geojson['_id']] = CreateTowerCzmlFromGeojson(geojson);
				var dataSource = new Cesium.CzmlDataSource();
				var arr = [g_czmls[geojson['_id']]];
				dataSource.load(arr);
				viewer.dataSources.add(dataSource);
			}
		}
	}
}
function CreateTowerCzmlFromGeojson(tower)
{
	//var ret = [];
	//for(var i in geojsonarray)
	//{
	//var tower = geojson[i];
	var cz = {}
	//cz['id'] = tower['properties']['id'];
	cz['id'] = tower['_id'];
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
	cz['description'] = '<!--HTML-->\r\n<p>' + tower['properties']['tower_name'] + '</p>';
		//ret.push(cz);
	//}
	//return ret;
	return cz;
}

function GetLineIdFromLineName(line_name)
{
	var ret = null;
	for(var i in g_lines)
	{
		if(g_lines[i]['properties']['line_name'] == line_name)
		{
			ret = g_lines[i]['_id'];
			break;
		}
	}
	return ret;
}

function LoadTowerByLineName(viewer, ellipsoid, line_name)
{
	var geo_cond = {'db':'kmgd', 'collection':'mongo_get_towers_by_line_name', 'properties.line_name':line_name};
	var line_cond = {'db':'kmgd', 'collection':'lines', 'properties.line_name':line_name};
	var ext_cond = {'db':'kmgd', 'collection':'mongo_get_towers_by_line_name','get_extext':true, 'properties.line_name':line_name};
	var segs_cond = {'db':'kmgd', 'collection':'segments'};
	
	MongoFind( segs_cond, 
		function(data){
			g_segments = data;
			//console.log(g_segments);
	});
	MongoFind( line_cond, 
		function(linedata){
			g_lines = linedata;
			var line_id = GetLineIdFromLineName(line_name);
			if(line_id)
			{
				MongoFind( ext_cond, 
					function(data){
						g_view_extent = data;
						FlyToExtent(viewer.scene, g_view_extent['west'], g_view_extent['south'], g_view_extent['east'], g_view_extent['north']);
						console.log(g_view_extent);
				});
				MongoFind( geo_cond, 
					function(data){
						var arr = [];
						for(var i in data)
						{
							if(!g_geojsons[data[i]['_id']])
							{
								g_geojsons[data[i]['_id']] = data[i];
							}
							var cz = CreateTowerCzmlFromGeojson(data[i]);
							if(!g_czmls[data[i]['_id']])
							{
								g_czmls[data[i]['_id']] = cz;
								arr.push(cz);
							}
						}
						//viewer.dataSources.removeAll();
						var dataSource = new Cesium.CzmlDataSource();
						dataSource.load(arr);
						viewer.dataSources.add(dataSource);
						ShowProgressBar(false);
				});
			}
	});
}


function LookAtTarget(scene, id)
{
	//scene.camera.controller.lookAt(scene.camera.position, target, scene.camera.up);
	var ellipsoid = scene.primitives.centralBody.ellipsoid;
	
	if(g_geojsons[id])
	{
		var tower = g_geojsons[id];
		var x = tower['geometry']['coordinates'][0];
		var y = tower['geometry']['coordinates'][1];
		var z = tower['properties']['geo_z'];
		FlyToPoint(scene, x, y, z, 1.05, 4000);
	}
}
function LookAtTargetExtent(scene, id, dx, dy)
{
	var ellipsoid = scene.primitives.centralBody.ellipsoid;
	if(g_geojsons[id])
	{
		var tower = g_geojsons[id];
		var x = tower['geometry']['coordinates'][0];
		var y = tower['geometry']['coordinates'][1];
		var west = Cesium.Math.toRadians(x - dx);
		var south = Cesium.Math.toRadians(y - dy);
		var east = Cesium.Math.toRadians(x + dx);
		var north = Cesium.Math.toRadians(y + dy);
		var extent = new Cesium.Extent(west, south, east, north);
		//scene.camera.controller.viewExtent(extent, ellipsoid);
		FlyToExtent(scene, west, south, east, north);
	}
}
function ViewExtentByPos(scene, lng, lat,  dx, dy)
{
	var ellipsoid = scene.primitives.centralBody.ellipsoid;
	var west = Cesium.Math.toRadians(lng - dx);
	var south = Cesium.Math.toRadians(lat - dy);
	var east = Cesium.Math.toRadians(lng + dx);
	var north = Cesium.Math.toRadians(lat + dy);
	var extent = new Cesium.Extent(west, south, east, north);
	//scene.camera.controller.viewExtent(extent, ellipsoid);
	scene.camera.controller.viewExtent(extent, ellipsoid);

			
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

function GetTowerInfoByTowerId(id)
{
	var ret = null;
	if(g_geojsons[id])
	{
		ret = g_geojsons[id];
	}
	return ret;
}

function LoadTowerModelByTower(viewer, tower)
{
	var scene = viewer.scene;
	var ellipsoid = scene.primitives.centralBody.ellipsoid;
	
	if(tower)
	{
		var id = tower['_id'];
		if(!g_gltf_models[id])
		{
			if(tower['properties']['model']['model_code_height'])
			{
				var lng = parseFloat($('input[id="tower_baseinfo_lng"]').val()),
					lat = parseFloat($('input[id="tower_baseinfo_lat"]').val()),
					height = parseFloat($('input[id="tower_baseinfo_alt"]').val()),
					rotate = parseFloat($('input[id="tower_baseinfo_rotate"]').val());
				if($.isNumeric(lng) && $.isNumeric(lat) && $.isNumeric(height) && $.isNumeric(rotate))
				{
					var model = CreateTowerModel(
						scene, 
						ellipsoid, 
						GetModelUrl(tower['properties']['model']['model_code_height']), 
						//tower['geometry']['coordinates'][0],  
						//tower['geometry']['coordinates'][1], 
						//tower['properties']['geo_z'] ,  
						//tower['properties']['rotate'],
						lng,  
						lat, 
						height ,  
						rotate,
						10
					);
					if(model)
					{
						g_gltf_models[id] = model;
						console.log("load model for [" + id + "]");
					}
				}
			}
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




function GetNextTowerModelData(ids)
{
	var ret = [];
	for(var i in ids)
	{
		var id = ids[i];
		if(g_geojsons[id])
		{
			var tower = g_geojsons[id];
			ret.push(tower['properties']['model']);
		}
	}
	return ret;
}
function GetNextModelUrl(ids)
{
	var ret = [];
	for(var i in ids)
	{
		var id = ids[i];
		if(g_geojsons[id])
		{
			var tower = g_geojsons[id];
			var url = GetModelUrl(tower['properties']['model']['model_code_height']);
			if(url.length>0)
			{
				ret.push(url);
			}
		}
		
	}
	return ret;
}

function GetModelUrl(model_code_height)
{
	if(!model_code_height)
	{
		return '';
	}
	return g_host + "gltf/" + model_code_height + ".json" ;
	//return "http://localhost:88/gltf/test.json";//?random=" + $.uuid();
}

function CreateTowerModel(scene, ellipsoid, modelurl,  lng,  lat,  height, rotate, scale) 
{
	if(modelurl.length==0)
	{
		return null;
	}
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
	//console.log(infoBox);
	var infoBoxViewModel = Cesium.defined(infoBox) ? infoBox.viewModel : undefined;

	var selectionIndicator = viewer.selectionIndicator;
	var selectionIndicatorViewModel = Cesium.defined(selectionIndicator) ? selectionIndicator.viewModel : undefined;

	var enableInfoOrSelection = Cesium.defined(infoBox) || Cesium.defined(selectionIndicator);

	var eventHelper = new Cesium.EventHelper();
	var dynamicObjectView;

	function trackSelectedObject() {
		viewer.trackedObject = viewer.selectedObject;
		var id = viewer.trackedObject.id;
		//console.log('track id=' + id);
		LookAtTarget(viewer.scene, id);
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

				//if (Cesium.defined(selectedObject.description)) {
					//infoBoxViewModel.descriptionRawHtml = Cesium.defaultValue(selectedObject.description.getValue(time), '');
				//} else {
					//infoBoxViewModel.descriptionRawHtml = '';
				//}
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
			//console.log('track id=' + id);
			LookAtTarget(viewer.scene, id);
			
		}
	}

	function pickAndSelectObject(e) {
		viewer.selectedObject = pickDynamicObject(e);
		
		if (Cesium.defined(viewer.selectedObject)) 
		{
			var id = viewer.selectedObject.id;
			g_prev_selected_pos = viewer.selectedObject.position;
			g_prev_selected_id = g_selected_obj_id;
			g_selected_obj_id = id;
			console.log('selected id=' + id);
			console.log('prev selected id=' + g_prev_selected_id);
			if(g_prev_selected_id != g_selected_obj_id)
			{
				if(g_prev_selected_id)
				{
					if(CheckTowerInfoModified())
					{
						
						ShowConfirm(500, 200,
							'保存确认',
							'检测到数据被修改，确认保存吗? 确认的话数据将会提交到服务器上，以便所有人都能看到修改的结果。',
							function(){
								SaveTower();
								ShowTowerInfo(viewer, g_selected_obj_id);
							},
							function(){
								ShowTowerInfo(viewer, g_selected_obj_id);
							}
						);
						
					}else{
						ShowTowerInfo(viewer, g_selected_obj_id);
					}
				}
				else{
					ShowTowerInfo(viewer, g_selected_obj_id);
				}
			}
			
		}
		else{
			g_prev_selected_id = g_selected_obj_id;
			g_selected_obj_id = undefined;
			if(g_prev_selected_pos)
			{
				var vm = viewer.homeButton.viewModel;
				//vm.flightDuration = 1;
				vm.command();
				var pos = viewer.scene.primitives.centralBody.ellipsoid.cartesianToCartographic(g_prev_selected_pos._value);
				
				FlyToPoint(viewer.scene, Cesium.Math.toDegrees(pos.longitude) , Cesium.Math.toDegrees(pos.latitude), pos.height, 1.6, 1);
				//ViewExtentByPos(viewer.scene, Cesium.Math.toDegrees(pos.longitude) , Cesium.Math.toDegrees(pos.latitude), 0.00001, 0.00001);
				g_prev_selected_pos = null;
			}
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

	function ClearTrackedObj(viewer)
	{
		var vm = viewer.homeButton.viewModel;
		var transitioner = vm._transitioner;
		//var ellipsoid = viewer.scene.primitives.centralBody.ellipsoid;
		var ellipsoid = vm._ellipsoid;
		var scene = viewer.scene;
        var mode = scene.mode;
        var controller = scene.screenSpaceCameraController;
		var flightDuration = 1;

        controller.ellipsoid = ellipsoid;
        controller.columbusViewMode = Cesium.CameraColumbusViewMode.FREE;

        var context = scene.context;
        if (Cesium.defined(transitioner) && mode === Cesium.SceneMode.MORPHING) {
            transitioner.completeMorph();
        }
        var flight;
        var description;

        if (mode === Cesium.SceneMode.SCENE2D) {
            description = {
                destination : Cesium.Extent.MAX_VALUE,
                duration : flightDuration,
                endReferenceFrame : new Cesium.Matrix4(0, 0, 1, 0,
                                                1, 0, 0, 0,
                                                0, 1, 0, 0,
                                                0, 0, 0, 1)
            };
            flight = Cesium.CameraFlightPath.createAnimationExtent(scene, description);
            scene.animations.add(flight);
        } else if (mode === Cesium.SceneMode.SCENE3D) {
            var defaultCamera = new Cesium.Camera(context);
            description = {
                destination : defaultCamera.position,
                duration : flightDuration,
                up : defaultCamera.up,
                direction : defaultCamera.direction,
                endReferenceFrame : Cesium.Matrix4.IDENTITY
            };
            flight = Cesium.CameraFlightPath.createAnimation(scene, description);
            scene.animations.add(flight);
        } else if (mode === Cesium.SceneMode.COLUMBUS_VIEW) {
            var maxRadii = ellipsoid.maximumRadius;
            var position = Cesium.Cartesian3.multiplyByScalar(Cesium.Cartesian3.normalize(new Cesium.Cartesian3(0.0, -1.0, 1.0)), 5.0 * maxRadii);
            var direction = Cesium.Cartesian3.normalize(Cesium.Cartesian3.subtract(Cesium.Cartesian3.ZERO, position));
            var right = Cesium.Cartesian3.cross(direction, Cesium.Cartesian3.UNIT_Z);
            var up = Cesium.Cartesian3.cross(right, direction);

            description = {
                destination : position,
                duration : flightDuration,
                up : up,
                direction : direction,
                endReferenceFrame : new Cesium.Matrix4(0, 0, 1, 0,
                                                1, 0, 0, 0,
                                                0, 1, 0, 0,
                                                0, 0, 0, 1)
            };

            flight = Cesium.CameraFlightPath.createAnimation(scene, description);
            scene.animations.add(flight);
        }
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

		if (isTracking &&  Cesium.defined(value.position)) {
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

function GetNeighborTowers(ids)
{
	var ret = [];
	for(var j in ids)
	{
		var id = ids[j];
		if(g_geojsons[id])
		{
			var tower = g_geojsons[id];
			ret.push(tower);
		}
	}
	return ret;
}

function GetSegmentPairsByTowTowerId(id0, id1)
{
	var ret = [];
	for(var i in g_segments)
	{
		var seg = g_segments[i];
		if(seg['start_tower'] == id0 && seg['end_tower'] == id1)
		{
			ret = seg['contact_points'];
			break;
		}
	}
	return ret;
}

function GetPhaseColor(phase)
{
	var ret = '#000000';
	if(g_phase_color_mapping[phase])
	{
		ret = g_phase_color_mapping[phase];
	}
	return ret;
}

function GetContactPointByIndex(tower, side, index)
{
	var ret = null;
	for(var i in tower['properties']['model']['contact_points'])
	{
		var cp = tower['properties']['model']['contact_points'][i];
		if(cp['side'] == side && cp['contact_index'] == index)
		{
			ret = cp;
			break;
		}
	}
	return ret;
}

function GetSegmentsModel(tower0, tower1)
{
	var ret = null;
	for(var i in g_polylines_segments)
	{
		var seg = g_polylines_segments[i];
		if(
			(seg['start'] == tower0['_id'] && seg['end'] == tower1['_id'])
		|| 	(seg['end'] == tower0['_id'] && seg['start'] == tower1['_id'])
		){
			ret = seg['model'];
			break;
		}
	}
	return ret;
}
function RemoveSegmentsFromArray(tower0, tower1)
{
	var ret = null;
	for(var i in g_polylines_segments)
	{
		var seg = g_polylines_segments[i];
		if(
			(seg['start'] == tower0['_id'] && seg['end'] == tower1['_id'])
		|| 	(seg['end'] == tower0['_id'] && seg['start'] == tower1['_id'])
		){
			ret = seg;
			g_polylines_segments.splice(i,1);
			break;
		}
	}
	return ret;
}

function CheckSegmentsExist(tower0, tower1)
{
	var ret = false;
	for(var i in g_polylines_segments)
	{
		var seg = g_polylines_segments[i];
		if(
			(seg['start'] == tower0['_id'] && seg['end'] == tower1['_id'])
		|| 	(seg['end'] == tower0['_id'] && seg['start'] == tower1['_id'])
		){
			ret = true;
			break;
		}
	}
	return ret;
}

function RemoveSegmentsBetweenTow(scene, tower0, tower1)
{
	if(CheckSegmentsExist(tower0, tower1))
	{
		var seg = RemoveSegmentsFromArray(tower0, tower1);
		if(seg)
		{
			while(!seg['model'].isDestroyed())
			{
				//seg['model'].destroy();
				var ret = scene.primitives.remove(seg['model']);
				//console.log(ret);
			}
		}
	}
}

function DrawSegmentsBetweenTowTower(scene, tower0, tower1)
{
	if(tower0 && tower1 && !CheckSegmentsExist(tower0, tower1))
	{
		var ellipsoid = scene.primitives.centralBody.ellipsoid;
		var lng0 = tower0['geometry']['coordinates'][0],
			lat0 = tower0['geometry']['coordinates'][1],
			height0 = tower0['properties']['geo_z'],
			rotate0 = Cesium.Math.toRadians(tower0['properties']['rotate'] - 90),
			lng1 = tower1['geometry']['coordinates'][0],
			lat1 = tower1['geometry']['coordinates'][1],
			height1 = tower1['properties']['geo_z'],
			rotate1 = Cesium.Math.toRadians(tower1['properties']['rotate'] - 90);
			
		var cart3_0 = ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(lng0, lat0, height0));
		var	modelMatrix_0 = Cesium.Transforms.eastNorthUpToFixedFrame(cart3_0);
		var	quat_0 = Cesium.Quaternion.fromAxisAngle(Cesium.Cartesian3.UNIT_Z, rotate0);
		var	rot_mat3_0 = Cesium.Matrix3.fromQuaternion(quat_0);
		
		var cart3_1 = ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(lng1, lat1, height1));
		var	modelMatrix_1 = Cesium.Transforms.eastNorthUpToFixedFrame(cart3_1);
		var	quat_1 = Cesium.Quaternion.fromAxisAngle(Cesium.Cartesian3.UNIT_Z, rotate1);
		var	rot_mat3_1 = Cesium.Matrix3.fromQuaternion(quat_1);
		
		var segpairs = GetSegmentPairsByTowTowerId(tower0['_id'], tower1['_id']);
		
		//var mat4 = Cesium.Matrix4.fromRotationTranslation(rot_mat3_0, Cesium.Cartesian3.ZERO);
		//mat4 = Cesium.Matrix4.multiplyByTranslation(mat4, cart3_0);
		//var m = Cesium.Matrix4.multiplyTransformation(modelMatrix_0, mat4);
		
		
		var polylines = new Cesium.PolylineCollection({'modelMatrix':Cesium.Matrix4.IDENTITY});
		for(var i in segpairs)
		{
			var pair = segpairs[i];
			var cp0 = GetContactPointByIndex(tower0, 0, pair['start']);
			var	cp1 = GetContactPointByIndex(tower1, 1, pair['end']);
			var color = Cesium.Color.fromCssColorString(GetPhaseColor(pair['phase']));
			if(cp0 && cp1)
			{
				var tran_vec3_0 = new Cesium.Cartesian3(cp0['x'], cp0['z'], cp0['y']);
				var mat4_0 = Cesium.Matrix4.fromRotationTranslation(rot_mat3_0, Cesium.Cartesian3.ZERO);
				mat4_0 = Cesium.Matrix4.multiplyByTranslation(mat4_0, tran_vec3_0);
				var m_0 = Cesium.Matrix4.multiplyTransformation(modelMatrix_0, mat4_0);
				
				
				var tran_vec3_1 = new Cesium.Cartesian3(cp1['x'], cp1['z'], cp1['y']);
				var mat4_1 = Cesium.Matrix4.fromRotationTranslation(rot_mat3_1, Cesium.Cartesian3.ZERO);
				mat4_1 = Cesium.Matrix4.multiplyByTranslation(mat4_1, tran_vec3_1);
				var m_1 = Cesium.Matrix4.multiplyTransformation(modelMatrix_1, mat4_1);

				var p0 = Cesium.Matrix4.getTranslation(m_0),
					p1 = Cesium.Matrix4.getTranslation(m_1);
				//var p0 = tran_vec3_0,
					//p1 = tran_vec3_1;
				
				var positions = CalcCatenary(ellipsoid, p0, p1, 15);
				var polyline = polylines.add({
					positions : positions,
					material : Cesium.Material.fromType('Color', {
						color : color
					}),
					width : 1.0
				});
			}
		}
		scene.primitives.add(polylines);
		g_polylines_segments.push({'start':tower0['_id'], 'end':tower1['_id'], 'model':polylines});
	}
	
}

function CalcCatenary(ellipsoid, p0, p1, segnum)
{
	var ret = [];
	if(g_use_catenary)
	{
		//var l = MathLib.sqrt((p0.x-p1.x)*(p0.x-p1.x) + (p0.y-p1.y)*(p0.y-p1.y));
		//var h = p1.z - p0.z;
		//var step = l/segnum;
		//var dx = (p1.x-p0.x)/segnum,
			//dy = (p1.y-p0.y)/segnum;
		
		//for(var i=0; i<=segnum; i++)
		//{
			//var z = get_z(l, h, p0.z, i*step, 0.7, 0.001);
			//var p = new Cesium.Cartesian3(p0.x + i * dx,  p0.y + i * dy,  z);
			//ret.push(p);
		//}
		var carto0 = ellipsoid.cartesianToCartographic(p0);
		var carto1 = ellipsoid.cartesianToCartographic(p1);
		//var l = MathLib.sqrt((carto0.longitude-carto1.longitude)*(carto0.longitude-carto1.longitude) + (carto0.latitude-carto1.latitude)*(carto0.latitude-carto1.latitude));
		var l = MathLib.sqrt((p0.x-p1.x)*(p0.x-p1.x) + (p0.y-p1.y)*(p0.y-p1.y));
		var h = carto1.height - carto0.height;
		var step = l/segnum;
		var dx = (carto1.longitude-carto0.longitude)/segnum,
			dy = (carto1.latitude-carto0.latitude)/segnum;
		
		for(var i=0; i<=segnum; i++)
		{
			var z = get_z(l, h, carto0.height, i*step, 0.9, 0.001);
			var carto = new Cesium.Cartographic(carto0.longitude + i * dx,  carto0.latitude + i * dy,  z);
			var p = ellipsoid.cartographicToCartesian(carto);
			ret.push(p);
		}
	}else
	{
		ret = [	p0,
				p1
			];
	}
	return ret;
}


function RemoveSegmentsTower(scene, tower)
{
	var prev_towers = GetNeighborTowers(tower['properties']['prev_ids']);
	var next_towers = GetNeighborTowers(tower['properties']['next_ids']);
	for(var i in prev_towers)
	{
		var t = prev_towers[i];
		RemoveSegmentsBetweenTow(scene, t, tower);
	}
	for(var i in next_towers)
	{
		var t = next_towers[i];
		RemoveSegmentsBetweenTow(scene, tower, t);
	}
}
function DrawSegmentsByTower(scene, tower)
{
	var prev_towers = GetNeighborTowers(tower['properties']['prev_ids']);
	var next_towers = GetNeighborTowers(tower['properties']['next_ids']);
	
	var lng = parseFloat($('input[id="tower_baseinfo_lng"]').val()),
		lat = parseFloat($('input[id="tower_baseinfo_lat"]').val()),
		height = parseFloat($('input[id="tower_baseinfo_alt"]').val()),
		rotate = parseFloat($('input[id="tower_baseinfo_rotate"]').val());
	if($.isNumeric(lng) && $.isNumeric(lat) && $.isNumeric(height) && $.isNumeric(rotate))
	{
		var tt = {};
		tt['_id'] = tower['_id'];
		tt['geometry'] = {};
		tt['geometry']['coordinates'] = [lng, lat];
		tt['properties'] = {};
		tt['properties']['geo_z'] = height;
		tt['properties']['rotate'] = rotate;
		tt['properties']['model'] = tower['properties']['model'];
		for(var i in prev_towers)
		{
			var t = prev_towers[i];
			DrawSegmentsBetweenTowTower(scene, t, tt);
		}
		for(var i in next_towers)
		{
			var t = next_towers[i];
			DrawSegmentsBetweenTowTower(scene, tt, t);
		}
	}
}


function CheckTowerInfoModified()
{
	var id = $('input[id="tower_baseinfo_id"]').val();
	//console.log('tower_id=' + id);
	var tower = GetTowerInfoByTowerId(id);
	if(tower)
	{
		var lng = $('input[id="tower_baseinfo_lng"]').val(),
			lat = $('input[id="tower_baseinfo_lat"]').val(),
			height = $('input[id="tower_baseinfo_alt"]').val(),
			rotate = $('input[id="tower_baseinfo_rotate"]').val();
		var mc = $('input[id="tower_baseinfo_model_code"]').val();
		if(lng != tower['geometry']['coordinates'][0] 
		|| lat != tower['geometry']['coordinates'][1]
		|| height != tower['properties']['geo_z']
		|| rotate != tower['properties']['rotate']
		|| mc != tower['properties']['model']['model_code']
		)
		{
			return true;
		}
		for(var k in tower['properties'])
		{
			var kk = 'tower_baseinfo_' + k;
			if($('input[id="' + kk + '"]').length)
			{
				var v = $('input[id="' + kk + '"]').val();
				if(v.length>0 && v != tower['properties'][k] )
				{
					return true;
				}
			}
		}
	}
	return false;
}

function SaveTower(id)
{
	if(id)
	{
		console.log('save tower ' + id);
	}else
	{
		var id = $('input[id="tower_baseinfo_id"]').val();
		console.log('save form tower ' + id);
	}
}
function ShowTowerInfo(viewer, id)
{
	var tower = GetTowerInfoByTowerId(id);
	if(tower)
	{
		ShowTowerInfoDialog(viewer, tower);
		LoadTowerModelByTower(viewer, tower);
		DrawSegmentsByTower(viewer.scene, tower);
	}

}
function ShowTowerInfoDialog(viewer, tower)
{
	var infoBox = viewer.infoBox;
	var title = '';
	if(tower)
	{
		title = tower['properties']['tower_name'];
	}
	$('#dlg_tower_info').dialog({
		width: 640,
		height: 730,
		minWidth:200,
		minHeight: 200,
		draggable: true,
		resizable: true, 
		modal: false,
		position:{at: "right center"},
		title:title,
		buttons:[
			{ 	text: "保存", 
				click: function(){ 
					if($('#form_tower_info_base').valid())
					{
						if(CheckTowerInfoModified())
						{
							ShowConfirm(500, 200,
								'保存确认',
								'检测到数据被修改，确认保存吗? 确认的话数据将会提交到服务器上，以便所有人都能看到修改的结果。',
								function(){
									SaveTower();
								},
								function(){
								
								}
							);
						}
						else{
							//$( this ).dialog( "close" );
						}
					}
				}
			},
			{ 	text: "关闭", 
				click: function(){ 
					$( this ).dialog( "close" );
				}
			}
		
		]
	});
	$('#tabs_tower_info').tabs({ 
		collapsible: false,
		active: 0,
		beforeActivate: function( event, ui ) {
			var title = ui.newTab.context.innerText;
			if(title == '杆塔模型')
			{
				var iframe = $(ui.newPanel.context).find('#tower_info_model').find('iframe');
				var url = GetModelUrl(tower['properties']['model']['model_code_height']);
				if(url.length>0)
				{
					var obj = {};
					obj['url'] = '/' + url;
					obj['data'] = tower['properties']['model'];
					obj['tower_id'] = tower['_id'];
					obj['denomi_height'] = tower['properties']['denomi_height'];
					$('#title_model_code').html('杆塔型号：' + tower['properties']['model']['model_code'] + ' 呼称高：' + tower['properties']['denomi_height']);
					var json = encodeURIComponent(JSON.stringify(obj));
					iframe.attr('src', g_host + 'threejs/editor/index.html?' + json);
				}
			}
			if(title == '架空线段')
			{
				var iframe = $(ui.newPanel.context).find('#tower_info_segment').find('iframe');
				var url = GetModelUrl(tower['properties']['model']['model_code_height']);
				var url_next = GetNextModelUrl(tower['properties']['next_ids']);
				if(url.length>0 && url_next.length>0)
				{
					var obj = {};
					obj['url'] = '/' + url;
					for(var i in url_next)
					{
						url_next[i] = '/' + url_next[i];
					}
					obj['url_next'] = url_next;
					obj['data'] = tower['properties']['model'];
					obj['tower_id'] = tower['_id'];
					obj['next_ids'] = tower['properties']['next_ids'];
					obj['data_next'] = GetNextTowerModelData(tower['properties']['next_ids']);
					obj['segments'] = GetSegmentsByTowerStartEnd(tower['_id'], tower['properties']['next_ids']);
					//obj['denomi_height'] = tower['properties']['denomi_height'];
					//$('#title_model_code').html('杆塔型号：' + tower['properties']['model']['model_code'] + ' 呼称高：' + tower['properties']['denomi_height']);
					var json = encodeURIComponent(JSON.stringify(obj));
					iframe.attr('src', g_host + 'threejs/editor/index.html?' + json);
				}
			}
		}
		//threejs/editor/index.html
	});
		
	BuildForm(viewer.scene, 'form_tower_info_base', g_tower_baseinfo_fields);
	if(tower)
	{
		var data = {
			'tower_baseinfo_id':tower['_id'], 
			'tower_baseinfo_lng':tower['geometry']['coordinates'][0],
			'tower_baseinfo_lat':tower['geometry']['coordinates'][1],
			'tower_baseinfo_alt':tower['properties']['geo_z'],
			'tower_baseinfo_rotate':tower['properties']['rotate'],
			'tower_baseinfo_tower_name':tower['properties']['tower_name'],
			'tower_baseinfo_tower_code':tower['properties']['tower_code'],
			'tower_baseinfo_model_code':tower['properties']['model']['model_code'],
			'tower_baseinfo_denomi_height':tower['properties']['denomi_height'],
			'tower_baseinfo_grnd_resistance':tower['properties']['grnd_resistance'],
			'tower_baseinfo_horizontal_span':tower['properties']['horizontal_span'],
			'tower_baseinfo_vertical_span':tower['properties']['vertical_span'],
			'tower_baseinfo_project':GetProjectNameByTowerId(tower['_id'])
		};	
		SetFormData('form_tower_info_base', data);
	}
	if(tower)
	{
		var data = [];
		var idx = 1;
		for(var i in tower['properties']['metals'])
		{
			data.push({
				'idx':idx, 
				'type':tower['properties']['metals'][i]['type'],
				'model':tower['properties']['metals'][i]['model']
				});
			idx += 1;
		}
	}
	
	
	//var form_tower_info_metal = $("#form_tower_info_metal").ligerForm({
		//inputWidth: 120, labelWidth: 120, space: 10,
		//validate : true,
		//fields: []
	//});
	
	if(!g_contextmenu_metal)
	{
		g_contextmenu_metal = $.ligerMenu({ top: 100, left: 100, width: 120, items:
			[
			{ text: '增加金具', icon:'add',
				children:[
					{ text:'绝缘子串',click: AddMetal},
					{ text:'防振锤',click: AddMetal},
					{ text:'接地装置',click: AddMetal},
					{ text:'基础',click: AddMetal},
					{ text:'拉线',click: AddMetal},
					{ text:'防鸟刺',click: AddMetal},
					{ text:'在线监测装置',click: AddMetal},
					{ text:'雷电计数器',click: AddMetal}
				]
			},
			{ text: '删除金具', click: DeleteMetal,icon:'delete' }
			//{ line: true },
			//{ text: '查看', click: onclick11 },
			//{ text: '关闭', click: onclick112 }
			]
		});
	}
	
	$("#listbox_tower_info_metal").bind("contextmenu", function (e)
	{
		g_contextmenu_metal.show({ top: e.pageY, left: e.pageX });
		return false;
	});

	var listbox_tower_info_metal = $("#listbox_tower_info_metal").ligerListBox({
		data: data,
		valueField:'idx',
		textField: 'type',
		//readonly:true,
		columns: [
			{ header: 'ID', name: 'idx', width: 20 },
			{ header: '金具类型', name: 'type' },
			{ header: '金具型号', name: 'model' }
		],
		isMultiSelect: false,
		isShowCheckBox: false,
		width: 500,
		height:150,
		onSelected:function(idx, name, obj){
			if(obj)
			{
				g_selected_metal_item = obj;
				var o = obj;
				var flds = [];
				var formdata = {};
				if(o['type'] == '绝缘子串')
				{
					//var insulator_type_list = [
						//{'value':'导线绝缘子','text':'导线绝缘子'},
						//{'value':'跳线绝缘子','text':'跳线绝缘子'},
						//{'value':'地线绝缘子','text':'地线绝缘子'},
						//{'value':'OPGW绝缘子串','text':'OPGW绝缘子串'}
					//];
					//var mat_type_list = [
						//{'value':'未知','text':'陶瓷'},
						//{'value':'玻璃','text':'玻璃'},
						//{'value':'合成','text':'合成'},
						//{'value':'未知','text':'未知'}
					//];
					//var insulator_flds = [
						//{display: "类型", name: "type", newline: true,  type: "text", editor:{readonly:true}, width:275, validate:{required:true}},
						//{display: "绝缘子类型", name: "insulator_type", newline: true,  type: "select", editor: {data:insulator_type_list},  width:275},
						//{display: "绝缘子材料", name: "material", newline: true,  type: "select", editor: {data:mat_type_list},  width:275},
						//{display: "绝缘子型号", name: "model", newline: true,  type: "text", width:275},
						//{display: "串数", name: "strand", newline: true,  type: "digits", width:70},
						//{display: "片数", name: "slice", newline: false,  type: "digits", width:70},
						//{display: "生产厂家", name: "manufacturer", newline: true,  type: "text", width:275},
						//{display: "组装图号", name: "assembly_graph", newline: true,  type: "text", width:275}
					//];
					
					
					flds = g_insulator_flds;
					var metal = tower['properties']['metals'][o['idx']-1];
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
				}
				if(o['type'] == '防振锤')
				{
					//var damper_list = [
						//{'value':'导线大号侧','text':'导线大号侧'},
						//{'value':'导线小号侧','text':'导线小号侧'},
						//{'value':'地线大号侧','text':'地线大号侧'},
						//{'value':'地线小号侧','text':'地线小号侧'}
					//];
					//var damper_flds = [
						//{display: "类型", name: "type", newline: true,  type: "text", editor:{readonly:true},  width:275, validate:{required:true}},
						//{display: "安装部位", name: "side", newline: true,  type: "select", editor: {data:damper_list},  width:275},
						//{display: "防振锤型号", name: "model", newline: true,  type: "text", width:275},
						//{display: "防振锤数量", name: "count", newline: true,  type: "digits", width:70},
						//{display: "安装距离", name: "distance", newline: false,  type: "number", width:80},
						//{display: "生产厂家", name: "manufacturer", newline: true,  type: "text", width:275},
						//{display: "组装图号", name: "assembly_graph", newline: true,  type: "text", width:275}
					//];
					flds = g_damper_flds;
					var metal = tower['properties']['metals'][o['idx']-1];
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
				}
				if(o['type'] == '接地装置')
				{
					//var grd_flds = [
						//{display: "类型", name: "type", newline: true,  type: "text", editor:{readonly:true},  width:275, validate:{required:true}},
						//{display: "型号", name: "model", newline: true,  type: "text", width:275},
						//{display: "数量", name: "count", newline: true,  type: "digits", width:70},
						//{display: "埋深", name: "depth", newline: false,  type: "number", width:80},
						//{display: "生产厂家", name: "manufacturer", newline: true,  type: "text", width:275},
						//{display: "组装图号", name: "assembly_graph", newline: true,  type: "text", width:275}
					//];
					flds = g_grd_flds;
					var metal = tower['properties']['metals'][o['idx']-1];
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
				}
				if(o['type'] == '基础')
				{
					//var platform_model_list = [
						//{'value':'铁塔','text':'铁塔'},
						//{'value':'水泥塔','text':'水泥塔'}
					//];
					//var base_flds = [
						//{display: "类型", name: "type", newline: true,  type: "text", editor:{readonly:true},  width:275, validate:{required:true}},
						//{display: "平台类型", name: "platform_model", newline: true,  type: "select", editor: {data:platform_model_list}, width:275},
						//{display: "数量", name: "count", newline: true,  type: "digits", width:70},
						//{display: "埋深", name: "depth", newline: false,  type: "number", width:80},
						//{display: "生产厂家", name: "manufacturer", newline: true,  type: "text", width:275},
						//{display: "组装图号", name: "assembly_graph", newline: true,  type: "text", width:275}
					//];
					//flds = grd_flds;
					flds = g_base_flds_1;
					var metal = tower['properties']['metals'][o['idx']-1];
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
				}
				if(o['type'] == '拉线' || o['type'] == '防鸟刺' || o['type'] == '在线监测装置')
				{
					//var base_flds = [
						//{display: "类型", name: "type", newline: true,  type: "text", editor:{readonly:true},  width:275, validate:{required:true}},
						//{display: "型号", name: "model", newline: true,  type: "text", width:275},
						//{display: "数量", name: "count", newline: true,  type: "digits", width:70},
						//{display: "生产厂家", name: "manufacturer", newline: true,  type: "text", width:275},
						//{display: "组装图号", name: "assembly_graph", newline: true,  type: "text", width:275}
					//];
					flds = g_base_flds_2_3_4;
					var metal = tower['properties']['metals'][o['idx']-1];
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
				}
				if(o['type'] == '雷电计数器')
				{
					//var base_flds = [
						//{display: "类型", name: "type", newline: true,  type: "text", editor:{readonly:true},  width:275, validate:{required:true}},
						//{display: "型号", name: "model", newline: true,  type: "text", width:275},
						//{display: "读数", name: "counter", newline: true,  type: "digits", width:70},
						//{display: "生产厂家", name: "manufacturer", newline: true,  type: "text", width:275},
						//{display: "组装图号", name: "assembly_graph", newline: true,  type: "text", width:275}
					//];
					flds = g_base_flds_5;
					var metal = tower['properties']['metals'][o['idx']-1];
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
				}
				
				//$("#form_tower_info_metal").empty();
				//var form_tower_info_metal = $("#form_tower_info_metal").ligerForm({
					//inputWidth: 120, labelWidth: 120, space: 10,
					//validate : true,
					//fields: flds
				//});
				//form_tower_info_metal.setData(formdata);
				
				BuildForm(viewer.scene, 'form_tower_info_metal', flds);
				//console.log(formdata);
				SetFormData('form_tower_info_metal', formdata, 'tower_metal_');
			}
		}
	});
}

function GetSegmentsByTowerStartEnd(start_id, end_ids)
{
	var ret = [];
	for(var i in end_ids)
	{
		var end_id = end_ids[i];
		for(var j in g_segments)
		{
			var seg = g_segments[j];
			if(seg['start_tower'] == start_id && seg['end_tower'] == end_id)
			{
				ret.push(seg);
				break;
			}
		}
	}
	return ret;
}



function PositionModel(ellipsoid, model, lng, lat, height, rotate)
{
	if($.isNumeric(lng) && $.isNumeric(lat) && $.isNumeric(height) && $.isNumeric(rotate))
	{
		var cart3 = ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(parseFloat(lng), parseFloat(lat), parseFloat(height)));
		var modelMatrix = Cesium.Transforms.eastNorthUpToFixedFrame(cart3);
		var quat = Cesium.Quaternion.fromAxisAngle(Cesium.Cartesian3.UNIT_Z, Cesium.Math.toRadians(rotate - 90));
		var mat3 = Cesium.Matrix3.fromQuaternion(quat);
		var mat4 = Cesium.Matrix4.fromRotationTranslation(mat3, Cesium.Cartesian3.ZERO);
		var m = Cesium.Matrix4.multiplyTransformation(modelMatrix, mat4);
		model.modelMatrix = m;
	}

}


function GetProjectNameByTowerId(id)
{
	var ret = '';
	var l = [];
	for(var i in g_lines)
	{
		for(var j in g_lines[i]['properties']['towers'])
		{
			if(g_lines[i]['properties']['towers'][j] == id)
			{
				l.push(g_lines[i]['properties']['line_name']);
			}
		}
	}
	for(var i in l)
	{
		ret += l[i] + ',';
	}
	return ret;
}

function AddMetal(e)
{
	if(g_selected_obj_id && g_geojsons[g_selected_obj_id])
	{
		var tower = g_geojsons[g_selected_obj_id];
		var o = {};
		o['type'] = e.text;
		o['assembly_graph'] = '';
		o['manufacturer'] = '';
		o['model'] = '';
		if(e.text == '绝缘子串')
		{
			o['insulator_type'] = '';
			o['material'] = '';
			o['strand'] = 0;
			o['slice'] = 0;
		}
		if(e.text == '防振锤')
		{
			o['side'] = '';
			o['count'] = 0;
			o['distance'] = 0;
		}
		if(e.text == '接地装置')
		{
			o['count'] = 0;
			o['depth'] = 0;
		}
		if(e.text == '雷电计数器')
		{
			o['counter'] = 0;
		}
		if(e.text == '防鸟刺' || e.text == '在线监测装置' || e.text == '拉线')
		{
			o['count'] = 0;
		}
		if(e.text == '基础')
		{
			o['count'] = 0;
			o['platform_model'] = '';
			o['anchor_model'] = '';
			o['depth'] = 0;
		}
		tower['properties']['metals'].push(o);
		var data = [];
		var idx = 1;
		for(var i in tower['properties']['metals'])
		{
			data.push({
				'idx':idx, 
				'type':tower['properties']['metals'][i]['type'],
				'model':tower['properties']['metals'][i]['model']
				});
			idx += 1;
		}
		g_selected_metal_item = undefined;
		$("#listbox_tower_info_metal").ligerListBox().setData(data);
		
	}
}

function DeleteMetal()
{
	if(g_selected_obj_id && g_geojsons[g_selected_obj_id])
	{
		var tower = g_geojsons[g_selected_obj_id];
		if(g_selected_metal_item)
		{
			var o = g_selected_metal_item;
			tower['properties']['metals'].splice(o['idx']-1, 1);
		}
		var data = [];
		var idx = 1;
		for(var i in tower['properties']['metals'])
		{
			data.push({
				'idx':idx, 
				'type':tower['properties']['metals'][i]['type'],
				'model':tower['properties']['metals'][i]['model']
				});
			idx += 1;
		}
		g_selected_metal_item = undefined;
		$("#listbox_tower_info_metal").ligerListBox().setData(data);
	}
}



