
$.webgis.data.czmls = {};
$.webgis.data.geojsons = {};
$.webgis.data.lines = {};
$.webgis.data.codes = {};
$.webgis.data.segments = [];
$.webgis.data.gltf_models = {};
$.webgis.data.models_gltf_files = [];
$.webgis.mapping.models_mapping = {};
$.webgis.geometry.segments = [];
$.webgis.geometry.lines = {};

$.webgis.config.is_tower_focus = false;

$.webgis.data.buffers = {};
$.webgis.data.borders = {};

$.webgis.data.image_thumbnail_tower_info = [];
$.webgis.config.terrain_z_offset = -40;
$.webgis.config.node_connect_mode = false;

$.webgis.mapping.leaflet_old_style = {};

$.webgis.data.heatmap_layers = {};
$.webgis.current_userinfo = {};
$.webgis.data.sysrole = [];
$.webgis.config.map_backend = 'cesium';
$.webgis.config.use_catenary = true;



$.webgis.config.max_file_size = 5000000;


/*
	jquery全局初始化函数
*/
//window.addEventListener("message", receiveMessage, false);
//function receiveMessage(event)
//{
	//console.log(event.data);
//}




$(function() {

	$.webgis.current_userinfo = GetParamsFromUrl();

	$.jGrowl.defaults.closerTemplate = '<div class="bubblestylesuccess">关闭所有提示信息</div>';
	
	var viewer;

	var load_init_data = function()
	{
		ShowProgressBar(true, 670, 200, '载入中', '正在载入南网编码规范，请稍候...');
		LoadCodeData($.webgis.db.db_name, function(){
			ShowProgressBar(true, 670, 200, '载入中', '正在载入线路信息，请稍候...');
			LoadLineData($.webgis.db.db_name, function(){
				ShowProgressBar(true, 670, 200, '载入中', '正在载入架空线路信息，请稍候...');
				LoadSegments($.webgis.db.db_name, function(){
					ShowProgressBar(true, 670, 200, '载入中', '正在载入3D模型信息，请稍候...');
					LoadModelsList($.webgis.db.db_name, function(){
						ShowProgressBar(true, 670, 200, '载入中', '正在载入3D模型信息，请稍候...');
						LoadModelsMapping($.webgis.db.db_name, function(){
							if($.webgis.db.db_name === 'ztgd') name = '永发I回线';
							var extent = GetDefaultExtent($.webgis.db.db_name);
							FlyToExtent(viewer, extent['west'], extent['south'], extent['east'], extent['north']);
							LoadSysRole($.webgis.db.db_name, function(){
								$('#lnglat_indicator').html( '当前用户:' + $.webgis.current_userinfo['displayname'] );
							});
						});
						//$.webgis.config.zaware = true;
						//LoadAllDNNode(viewer, $.webgis.db.db_name, function(){
							//LoadAllDNEdge(viewer, $.webgis.db.db_name, function(){
								//var extent = GetExtentByCzml();
								//FlyToExtent(viewer, extent['west'], extent['south'], extent['east'], extent['north']);
								//ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
							//});
						//});
					
					});
				});
			});
		});
	};


	
	try{
		//throw "unsupport_cesium_exception";
		ShowProgressBar(true, 670, 200, '载入中', '正在载入，请稍候...');
		viewer = InitCesiumViewer();
		$.webgis.viewer = viewer;
		InitRuler(viewer);
		InitLogout(viewer);
		InitWebGISFormDefinition();
		InitDrawHelper(viewer);
		$.webgis.control.drawhelper.show(false);
		InitPoiInfoDialog();
		//InitTowerInfoDialog();
		InitSearchBox(viewer);
		InitToolPanel(viewer);
		InitModelList(viewer);
		InitKeyboardEvent(viewer);
		load_init_data();
		InitAntiBird(viewer);
		InitScreenSize();
	}catch(ex)
	{
		console.log(ex);
		$('#cesiumContainer').empty();
		$('#control_toolpanel_kmgd_left').css('display','none');
		ShowProgressBar(false);
		ShowMessage(null, 400, 300, '提示', '系统检测到该浏览器不支持最新HTML5标准WEBGL部分，因此将禁用3D视图。请使用Chrome浏览器或内置Chrome内核的浏览器以获得最佳浏览体验。', function(){
			$.webgis.config.map_backend = 'leaflet';
			viewer = InitLeafletViewer();
			$.webgis.viewer = viewer;
			
			InitHomeButton2D(viewer);
			InitLayerControl2D(viewer);
			InitRuler(viewer);
			InitNavigationHelp(viewer);
			InitLogout(viewer);
		
			InitWebGISFormDefinition();
			InitDrawHelper2D(viewer);
			$.webgis.control.drawhelper.show(false);
			
			InitPoiInfoDialog();
			//InitTowerInfoDialog();
			
			InitSearchBox(viewer);
			InitToolPanel(viewer);
			InitModelList(viewer);
			InitKeyboardEvent(viewer);
			load_init_data();
			InitAntiBird(viewer);
		});
	}
	
	
	
	
	//LoadBorder(viewer, $.webgis.db.db_name, {'properties.name':'云南省'});
	//LoadBorder(viewer, $.webgis.db.db_name, {'properties.type':'cityborder'});
	//LoadBorder(viewer, $.webgis.db.db_name, {'properties.type':'countyborder'});
	
	//$.webgis.data.heatmap_layers['testheatmap'] = {
		//layer: new HeatMapImageryProvider({
					//name:'testheatmap',
					//viewer:viewer,
					//points:testdata()
				//}),
		//type: 'heatmap'
	//};
	//$.webgis.data.heatmap_layers['yn_ice_100'] = {
		//layer: CreateTileHeatMap(viewer, {
					//url:'http://xiejun-desktop:6080/arcgis/rest/services/YN_HEATMAP/yn_ice_100/ImageServer',
					//maximumLevel: 11,
					//name:'yn_ice_100'
				//}),
		//type: 'tile'
	//};
});

function InitScreenSize()
{
	$('#cesiumContainer').css('height', $( window ).height() + 'px');
}
function CreateTileHeatMap(viewer, options)
{
	var aip = new ArcGisMapServerImageryProvider({
		url : options.url,
		maximumLevel: options.maximumLevel
	});
	var lyr = viewer.scene.imageryLayers.addImageryProvider(aip);
	lyr.alpha = 0.4;
	lyr.show = true;
	lyr.name = options.name;
	return lyr;
}

//function InitPostMessageListener()
//{
	//$(window).on("message", function(e) {
		//var data = e.originalEvent.data;
		//console.log(data);
	//});
//}

function IFrameUpdateTower(tower_id, data)
{
	for(var i in data)
	{
		var geojson = data[i];
		var id = geojson['_id'];
		if($.webgis.data.geojsons[id])
		{
			$.webgis.data.geojsons[id] = geojson; //AddTerrainZOffset(geojson);
			$.webgis.data.czmls[id] = CreateCzmlFromGeojson($.webgis.data.geojsons[id]);
		}
	}
	var selected_id = $.webgis.select.selected_geojson['_id'];
	if($.webgis.data.geojsons[selected_id])
	{
		$.webgis.select.selected_geojson['properties']['model'] = $.webgis.data.geojsons[selected_id]['properties']['model'];
	}
}
function IFrameUpdateModel(tower_id, data)
{
	for(var i in data)
	{
		var obj = data[i];
		var model_code_height = obj['model_code_height'];
		delete obj['_id'];
		$.webgis.mapping.models_mapping[model_code_height] = obj;
	}
}
function IFrameUpdateSegments(data)
{
	for(var i in data)
	{
		var obj = data[i];
		var id = obj['_id'];
		var find = false;
		for(var j in $.webgis.data.segments)
		{
			if($.webgis.data.segments[j]['_id'] === id)
			{
				$.webgis.data.segments[j] = obj;
				find = true;
				break;
			}
		}
		if(!find)
		{
			$.webgis.data.segments.push(obj);
		}
		if($.webgis.select.selected_obj && $.webgis.select.selected_obj.id)
		{
			RemoveSegmentsTower($.webgis.viewer, $.webgis.data.geojsons[$.webgis.select.selected_obj.id]);
			DrawSegmentsByTower($.webgis.viewer, $.webgis.data.geojsons[$.webgis.select.selected_obj.id]);
		}
	}
}



function LoadAllDNEdge(viewer, db_name, callback)
{
	var cond = {'db':db_name, 'collection':'edges', 'properties.webgis_type':'edge_dn'};
	MongoFind(cond, function(data){
		if(data.length>0)
		{
			for(var i in data)
			{
				var id = data[i]['_id'];
				if(!$.webgis.data.geojsons[id]) $.webgis.data.geojsons[id] = data[i];
				DrawEdgeBetweenTwoNode(viewer, 'edge_dn', $.webgis.data.geojsons[id]['properties']['start'],$.webgis.data.geojsons[id]['properties']['end'], false);
			}
		}
		if(callback) callback(data);
	});
}

function LoadEdgeByLineId(viewer, db_name, lineid, callback)
{
	console.log(lineid);
	var cond = {'db':db_name, 'collection':'-', action:'loadtoweredge', 'lineid':lineid};
	MongoFind(cond, function(data){
		if(data.length>0)
		{
			for(var i in data)
			{
				var id = data[i]['_id'];
				if(!$.webgis.data.geojsons[id]) 
				{
					//console.log(data[i]);
					$.webgis.data.geojsons[id] = data[i];
				}
			}
		}
		if(callback) callback(data);
	});
}




function LoadAllDNNode(viewer, db_name, callback)
{
	var cond = {'db':db_name, 'collection':'features', 'properties.webgis_type':'point_dn'};
	MongoFind(cond, function(data){
		//console.log(data);
		if(data.length>0)
		{
			for(var i in data)
			{
				var id = data[i]['_id'];
				if(!$.webgis.data.geojsons[id]) $.webgis.data.geojsons[id] = data[i]; //AddTerrainZOffset(data[i]);
				if(!$.webgis.data.czmls[id]) $.webgis.data.czmls[id] = CreateCzmlFromGeojson($.webgis.data.geojsons[id]);
				//$.webgis.data.czmls[id]['position']['cartographicDegrees'][2] = $.webgis.data.geojsons[id]['geometry']['coordinates'][2];
				//console.log($.webgis.data.czmls[id]['position']['cartographicDegrees'][2]);
			}
			if(callback) callback(data);
		}
	});
}


function InitLeafletViewer()
{
	$('#lnglat_indicator').css('width', '300px');
	$('#lnglat_indicator').css('text-align', 'right');
	$("#cesiumContainer").height($(window).height()).width($(window).width());
	$("#cesiumContainer").append('<div class="cesium-viewer-toolbar"></div>');
	$('.cesium-viewer-toolbar').css('z-index', '9');
	var center = GetDefaultCenter($.webgis.db.db_name);
	var c = L.latLng(center[1], center[0]);
	//console.log(c);
	var layers = [];
	var url_temlate, lyr;
	var baseMaps = {};
	
	url_temlate = 'http://' + $.webgis.remote.tiles_host + ':' + $.webgis.remote.tiles_port + '/tiles?image_type={image_type}&x={x}&y={y}&level={z}';
	
	
	lyr = L.tileLayer(url_temlate, {
		image_type:'arcgis_sat', 
		noWrap:true,
		tms:false,
		zoomOffset:0,
		zoomReverse:false,
		minZoom: 1,
		maxZoom: 18,
	});
	lyr.name = 'ESRI卫星图';
	lyr.iconUrl = Cesium.buildModuleUrl('/img/esri-sat.png');
	lyr.tooltip = 'ESRI卫星图';
	layers.push(lyr);
	baseMaps['ESRI卫星图'] = lyr;
	
	
	lyr = L.tileLayer(url_temlate, {
		image_type:'bing_sat', 
		noWrap:true,
		tms:false,
		zoomOffset:-1,
		minZoom: 1,
		maxZoom: 18,
	});
	
	lyr.name = 'Bing卫星图';
	lyr.iconUrl = Cesium.buildModuleUrl('/img/bingAerial.png');
	lyr.tooltip = 'Bing卫星图';
	layers.push(lyr);
	baseMaps['Bing卫星图'] = lyr;
	
	lyr = L.tileLayer(url_temlate, {
		image_type:'amap_map', 
		noWrap:true,
		tms:false,
		zoomOffset:0,
		minZoom: 1,
		maxZoom: 18,
	});
	lyr.name = '高德地图';
	lyr.iconUrl = Cesium.buildModuleUrl('/img/wmts-map.png');
	lyr.tooltip = '高德地图';
	layers.push(lyr);
	baseMaps['高德地图'] = lyr;
	
	
	//var prefix = '';
	//if($.webgis.remote.arcserver_host == '10.181.160.72')
	//{
		//prefix = 'ztgdgis/';
	//}
	//var url_arcgis = 'http://' + $.webgis.remote.arcserver_host + ':6080/arcgis/rest/services/' + prefix + 'YN_SAT/ImageServer';
	//lyr = L.esri.imageMapLayer(url_arcgis, {
		////image_type:'arcserver_imagery',
		////imagery_url:url_arcgis,
		////noWrap:true,
		////tms:false,
		////zoomOffset:1,
		////zoomReverse:false,
		//minZoom: 0,
		//maxZoom: 17,
	//});
	//layers.push(lyr);
	//baseMaps['YN_SAT'] = lyr;

	
	//if(CheckInternetConnection())
	//{
		//lyr = L.tileLayer.chinaProvider('GaoDe.Normal.Map');
	//}
	var map = L.map('cesiumContainer',{
		minZoom:1,
		maxZoom:18,
		zoomControl:false,
		//layers:layers,
		crs:L.CRS.EPSG900913
		//crs:L.CRS.EPSG4326
	}).setView(c, 6);
	map.layers = layers;
	
	//var markers = L.markerClusterGroup({
	//});
	$.webgis.control.leaflet_geojson_layer = L.geoJson({type: "FeatureCollection",features:[]}, {
		style: function (feature) {
			//if(feature.properties.webgis_type.indexOf('point_')>-1)
			//{
			var o = {};
			if(feature.geometry)
			{
				o.color = ColorArrayToHTMLColor($.webgis.mapping.style_mapping[feature.properties.webgis_type].color);
				var weight = 5;
				if($.webgis.mapping.style_mapping[feature.properties.webgis_type].pixelWidth)
				{
					o.weight = $.webgis.mapping.style_mapping[feature.properties.webgis_type].pixelWidth * 5;
				}
			}
			return o;
		},
		pointToLayer:function (feature, latlng) {
			var m = L.circleMarker(latlng, {
				radius: $.webgis.mapping.style_mapping[feature.properties.webgis_type].pixelSize,
				fillColor: ColorArrayToHTMLColor($.webgis.mapping.style_mapping[feature.properties.webgis_type].color),
				color: ColorArrayToHTMLColor($.webgis.mapping.style_mapping[feature.properties.webgis_type].outlineColor),
				weight: 1,
				opacity: 1,
				fillOpacity: 0.7
			});
			//if(feature.properties.name)
			//{
				//m.bindLabel(feature.properties.name);
			//}
			return m;
		},
		onEachFeature: function (feature, layer) {
			//markers.addLayer(layer);
			layer.on('mouseover', function (e) {
				if(e.target.feature.properties.name && $('#chb_show_label_' + e.target.feature.properties.webgis_type).is(':checked'))
				{
					$.webgis.control.drawhelper._tooltip.setVisible(true);
				}
			});
			layer.on('mousemove', function (e) {
				if(e.target.feature.properties.name && $('#chb_show_label_' + e.target.feature.properties.webgis_type).is(':checked'))
				{
					if($.webgis.control.drawhelper._tooltip.getVisible())
					{
						$.webgis.control.drawhelper._tooltip.showAt(e.containerPoint, e.target.feature.properties.name);
					}
				}
			});
			layer.on('mouseout', function (e) {
				$.webgis.control.drawhelper._tooltip.setVisible(false);
			});
			layer.on('click', function (e) {
				console.log(e.target.feature._id);
				ClearSelectColor2D(map);
				if($.webgis.select.selected_obj)
				{
					$.webgis.select.prev_selected_obj = $.webgis.select.selected_obj;
				}
				$.webgis.select.selected_obj = e.target.feature;
				$.webgis.select.selected_obj.id = e.target.feature._id;
				if(e.target.feature && e.target.feature.properties && e.target.feature.properties.webgis_type)
				{
					if(e.target.feature.properties.webgis_type.indexOf('point_'))
					{
						$.webgis.select.selected_obj.point = true;
					}
					else if(e.target.feature.properties.webgis_type.indexOf('polyline_'))
					{
						$.webgis.select.selected_obj.polyline = true;
					}
					else if(e.target.feature.properties.webgis_type.indexOf('polygon_'))
					{
						$.webgis.select.selected_obj.polygon = true;
					}
				}
				
				
				if(!$.webgis.mapping.leaflet_old_style[e.target.feature._id])
				{
					$.webgis.mapping.leaflet_old_style[e.target.feature._id] = {color:e.target.options.color, weight:e.target.options.weight};
				}
				e.target.setStyle({color:'green', weight: 10});
				OnSelect(map, null);
			});
			
		}
	});
	
	
	//markers.on('mouseover', function (e) {
		//if(e.layer.feature.properties.name && $('#chb_show_label_' + e.layer.feature.properties.webgis_type).is(':checked'))
		//{
			//$.webgis.control.drawhelper._tooltip.setVisible(true);
		//}
	//});
	//markers.on('mousemove', function (e) {
		//if(e.layer.feature.properties.name && $('#chb_show_label_' + e.layer.feature.properties.webgis_type).is(':checked'))
		//{
			//if($.webgis.control.drawhelper._tooltip.getVisible())
			//{
				//$.webgis.control.drawhelper._tooltip.showAt(e.containerPoint, e.layer.feature.properties.name);
			//}
		//}
	//});
	//markers.on('mouseout', function (e) {
		//$.webgis.control.drawhelper._tooltip.setVisible(false);
	//});
	//markers.on('click', function (e) {
		////console.log(e.layer.feature._id);
	//});
	//map.addLayer(markers, false);
	map.addLayer($.webgis.control.leaflet_geojson_layer);
	
	
	//L.control.layers(baseMaps, {}).addTo(map);
	L.control.mousePosition().addTo(map);
	
	map.invalidateSize();
	return map;
}


function InitCesiumViewer()
{
	var providerViewModels = [];
	var prefix = '';
	if($.webgis.remote.arcserver_host == '10.181.160.72')
	{
		prefix = 'ztgdgis/';
	}
	providerViewModels.push(new Cesium.ProviderViewModel({
		name : 'Esri卫星图',
		iconUrl : 'img/esri-sat.png',
		tooltip : 'Esri卫星图',
		creationFunction : function() {
			return new ESRIImageryFromServerProvider({
				//url : 'http://dev.virtualearth.net',
				//mapStyle : Cesium.BingMapsStyle.AERIAL
				////proxy : proxyIfNeeded
				url :  'http://' + $.webgis.remote.tiles_host + ':' + $.webgis.remote.tiles_port + '/tiles',
				imageType: 'arcgis_sat',
				queryType: 'server'
			});
		}
	}));
	providerViewModels.push(new Cesium.ProviderViewModel({
		name : 'YN_SAT',
		iconUrl : 'img/wmts-sat.png',
		tooltip : 'YN_SAT',
		creationFunction : function() {
			return new ArcGisMapServerImageryProvider({
				url : 'http://' + $.webgis.remote.arcserver_host + ':6080/arcgis/rest/services/' + prefix + 'YN_SAT/ImageServer',
				name: 'YN_SAT'
				//usePreCachedTilesIfAvailable:false
			});
		}
	}));
	providerViewModels.push(new Cesium.ProviderViewModel({
		name : 'Bing卫星图',
		iconUrl : 'img/bingAerial.png',
		tooltip : 'Bing卫星图',
		creationFunction : function() {
			return new BingImageryFromServerProvider({
				//url : 'http://dev.virtualearth.net',
				//mapStyle : Cesium.BingMapsStyle.AERIAL
				////proxy : proxyIfNeeded
				url :  'http://' + $.webgis.remote.tiles_host + ':' + $.webgis.remote.tiles_port + '/tiles',
				imageType: 'bing_sat',
				queryType: 'server'
			});
		}
	}));
	providerViewModels.push(new Cesium.ProviderViewModel({
		name : '高德地图',
		iconUrl : 'img/wmts-map.png',
		tooltip : '高德地图',
		creationFunction : function() {
			return new AMapTileImageryProvider({
				url :  'http://' + $.webgis.remote.tiles_host + ':' + $.webgis.remote.tiles_port + '/tiles',
				imageType: 'amap_map',
				queryType: 'server'
			});
		}
	}));
	
	//providerViewModels.push(new Cesium.ProviderViewModel({
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
	
	
	var terrainProviderViewModels = [];
	terrainProviderViewModels.push(new Cesium.ProviderViewModel({
		name : '无地形',
		iconUrl : Cesium.buildModuleUrl('Widgets/Images/TerrainProviders/Ellipsoid.png'),
		tooltip : 'no-terrain',
		creationFunction : function() {
			return new Cesium.EllipsoidTerrainProvider();
		}
	}));


	terrainProviderViewModels.push(new Cesium.ProviderViewModel({
		name : 'quantized-mesh中国云南',
		iconUrl : Cesium.buildModuleUrl('/img/aster-gdem.png'),
		tooltip : 'quantized-mesh中国云南',
		creationFunction : function() {
			return new HeightmapAndQuantizedMeshTerrainProvider({
				//url : "terrain",
				url :  'http://' + $.webgis.remote.tiles_host + ':' + $.webgis.remote.tiles_port + '/terrain',
				terrain_type : 'quantized_mesh',
				credit : ''
			});
		}
	}));
	//terrainProviderViewModels.push(new Cesium.ProviderViewModel({
		//name : 'Small Terrain heightmaps with water',
		//iconUrl : Cesium.buildModuleUrl('Widgets/Images/TerrainProviders/STK.png'),
		//tooltip : 'Medium-resolution, heightmap-based terrain for the entire globe. This tileset also includes a water mask. Free for use on the Internet.\nhttp://www.agi.com',
		//creationFunction : function() {
			//return new Cesium.CesiumTerrainProvider({
				//url : '//cesiumjs.org/smallterrain',
				//credit : 'Terrain data courtesy Analytical Graphics, Inc.'
			//});
		//}
	//}));
	var viewer;
	
	viewer = new Cesium.Viewer('cesiumContainer',{
		fullscreenButton:false,
		showRenderLoopErrors:false,
		scene3DOnly:true,
		animation:false,
		baseLayerPicker:true,
		geocoder:false,
		timeline:false,
		selectionIndicator:true,
		sceneModePicker:false,
		navigationInstructionsInitiallyVisible:false,
		infoBox:false,
		imageryProviderViewModels:providerViewModels,
		terrainProviderViewModels:terrainProviderViewModels
	});
	viewer.scene.camera.frustum.fov = Cesium.Math.PI_OVER_TWO;
	TranslateToCN();
	TowerInfoMixin(viewer);
	return viewer;
}



function ClearSelectColor2D(viewer)
{
	if($.webgis.control.leaflet_geojson_layer)
	{
		$.webgis.control.leaflet_geojson_layer.eachLayer(function(layer){
			if(layer.feature && layer.feature._id)
			{
				if($.webgis.mapping.leaflet_old_style[layer.feature._id])
				{
					var opt = $.webgis.mapping.leaflet_old_style[layer.feature._id];
					layer.setStyle({color:opt.color, weight:opt.weight});
					delete $.webgis.mapping.leaflet_old_style[layer.feature._id];
				}
			}
		});
	}
	viewer.eachLayer(function(layer){
		if(layer.eachLayer)
		{
			layer.eachLayer(function(lyr){
				if(lyr.geojson && lyr.geojson._id && $.webgis.mapping.leaflet_old_style[lyr.geojson._id])
				{
					var opt = $.webgis.mapping.leaflet_old_style[lyr.geojson._id];
					lyr.setStyle({color:opt.color, weight:opt.weight});
					delete $.webgis.mapping.leaflet_old_style[lyr.geojson._id];
				}
				
			});
		}
	});
	
}

function InitKeyboardEvent(viewer)
{
	var get_current_edge = function(id0, id1)
	{
		var ret;
		for(var i in $.webgis.geometry.segments)
		{
			var seg = $.webgis.geometry.segments[i];
			if(  (seg['webgis_type'] == 'edge_dn' || seg['webgis_type'] == 'edge_tower') && seg['start'] == id0 && seg['end'] == id1)
			{
				ret = seg['primitive'];
				break;
			}
		}
		return ret;
	};
	var change_color = function(webgis_type, id)
	{
		if($.webgis.config.map_backend === 'cesium')
		{
			var c = Cesium.Color.fromCssColorString("rgba(200,200,0,1)");
			var edge = get_current_edge($.webgis.select.prev_selected_obj.id, $.webgis.select.selected_obj.id);
			var m =	Cesium.Material.fromType('PolylineArrow', {
							color : c
					});
			for(var i=0; i<edge.length; i++)
			{
				var p = edge.get(i);
				p.material = m;
			}
		}
		if($.webgis.config.map_backend === 'leaflet' && webgis_type && id)
		{
			var color = ColorArrayToHTMLColor([200,200,0,1]);
			var lyr_polylinegroup;
			viewer.eachLayer(function (layer) {
				if(layer.name && layer.name === webgis_type)
				{
					lyr_polylinegroup = layer;
					return;
				}
			});
			if(lyr_polylinegroup)
			{
				lyr_polylinegroup.eachLayer(function(layer){
					if(layer.geojson && layer.geojson.properties && layer.geojson.properties.start === $.webgis.select.prev_selected_obj.id && layer.geojson.properties.end === $.webgis.select.selected_obj.id)
					{
						layer.geojson._id = id;
						layer.setStyle({color:color, weight:5});
						return;
					}
				});
			}
		}
	};
	
	if($.webgis.config.map_backend === 'leaflet')
	{
		viewer.on('click', function(e){
			//console.log('mapclick');
			if($.webgis.select.selected_obj)
			{
				//$.webgis.select.prev_selected_obj = $.extend(true, {}, $.webgis.select.selected_obj);
				delete $.webgis.select.selected_obj;
				$.webgis.select.selected_obj = undefined;
			}
			if($.webgis.select.prev_selected_obj)
			{
				delete $.webgis.select.prev_selected_obj;
				$.webgis.select.prev_selected_obj = undefined;
			}
			ClearSelectColor2D(viewer);
			
		});
	}
	$(document).on('click', function(e){
		if( e.target.id != 'anti_bird_msg_list_container' && e.target.id != 'button_anti_bird' && e.target.id != 'anti_bird_msg_list_filter') {
			$("#anti_bird_msg_list_container").hide('slide', {direction:'right'}, 500);
		}
	});
	
	$(document).on('keyup', function(e){
		if(e.keyCode == 76)//ctrl(17) L(76)
		{
			//if()
			//{
				//$.jGrowl("请先勾选“线路-->显示结点关系”",{
					//life: 2000,
					//position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
					//theme: 'bubblestylefail',
					//glue:'before'
				//});
				//return;
			//}
			$.webgis.config.node_connect_mode = !$.webgis.config.node_connect_mode;
			if($.webgis.config.node_connect_mode)
			{
				//$(".jGrowl-notification:last-child").remove();
				$.jGrowl('<div>连接模式开启(L键关闭)</div><span id="div_edge_instruction"></span><button  id="btn_edge_save">保存</button>', { 
					sticky:true,
					//life:3000,
					position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
					theme: 'bubblestylesuccess',
					glue:'before',
					afterOpen:function(){
						$('#btn_edge_save').off();
						$('#btn_edge_save').on('click', function(){
							SaveEdge(viewer, null, function(data){
								$('#btn_edge_save').attr('disabled','disabled');
								if(data.length>0)
								{
									if(data[0]['result'])
									{
										$.jGrowl(data[0]['result'], { 
											life: 2000,
											position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
											theme: 'bubblestylefail',
											glue:'before'
										});
									}
									else
									{
										var webgis_type;
										for(var i in data)
										{
											var g = data[i];
											webgis_type = g['properties']['webgis_type'];
											if(!$.webgis.data.geojsons[g['_id']]) 
											{
												$.webgis.data.geojsons[g['_id']] = g;
												if($.webgis.config.map_backend === 'leaflet')
												{
													change_color(webgis_type, g['_id']);
												}
											}
										}
										if($.webgis.config.map_backend === 'cesium')
										{
											change_color();
										}
										$.jGrowl("保存成功", { 
											life: 2000,
											position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
											theme: 'bubblestylesuccess',
											glue:'before'
										});
									}
								}
							});
						});
						$('#btn_edge_save').attr('disabled','disabled');
					}
				});
			}
			else
			{
				//$(".jGrowl-notification:last").trigger('jGrowl.close');
				$('.jGrowl-notification').trigger('jGrowl.close');
				$.jGrowl("连接模式关闭(L键开启)", { 
					life:3000,
					position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
					theme: 'bubblestylesuccess',
					glue:'before'
				});
			}
		}
		if(e.keyCode == 46)//delete
		{
			$('#control_toolpanel_kmgd_left').hide('slide',{}, 400, function(){
				$('#control_toolpanel_kmgd_handle').css('display','block');
			});
			try{
				$('#dlg_tower_info').dialog("close");
				$('#dlg_poi_info').dialog("close");
				
			}catch(e)
			{
				//console.log(e);
			}
			console.log($.webgis.select.selected_obj);
			if($.webgis.select.selected_obj && $.webgis.select.selected_obj.id && $.webgis.select.selected_obj.id.properties && $.webgis.select.selected_obj.id.properties.webgis_type.indexOf('edge_')>-1)
			{
				if(!CheckPermission('edge_delete'))
				{
					return;
				}
				var get_name = function()
				{
					var s0 = '', s1 = '';
					var id0 = $.webgis.select.selected_obj.id.properties.start;
					var id1 = $.webgis.select.selected_obj.id.properties.end;
					if($.webgis.data.geojsons[id0]) s0 = $.webgis.data.geojsons[id0].properties.name;
					if($.webgis.data.geojsons[id1]) s1 = $.webgis.data.geojsons[id1].properties.name;
					return s0 + '-' + s1;
				};
				var get_id = function()
				{
					var ret;
					for(var k in $.webgis.data.geojsons)
					{
						var g = $.webgis.data.geojsons[k];
						if(g.properties.start == $.webgis.select.selected_obj.id.properties.start && g.properties.end == $.webgis.select.selected_obj.id.properties.end)
						{
							ret = g['_id'];
							break;
						}
					}
					return ret;
				};
				var name = get_name();
				
				ShowConfirm(null, 400, 280, '删除确认', '你确认要删除[' + name + ']之间的联系吗?', function(){
					//console.log($.webgis.select.selected_obj.id);
					var id = get_id();
					//console.log(id);
					if(id)
					{
						var cond = {'db':$.webgis.db.db_name, 'collection':'edges', 'action':'remove', '_id':id};
						MongoFind( cond, 
							function(data){
								if(data.length>0)
								{
									if(data[0]['ok'] === 1)
									{
										$.jGrowl("删除成功", { 
											life:2000,
											position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
											theme: 'bubblestylesuccess',
											glue:'before'
										});
										if($.webgis.config.map_backend === 'leaflet')
										{
											viewer.eachLayer(function(layer){
												if(layer.eachLayer)
												{
													layer.eachLayer(function(lyr){
														if(lyr.geojson && lyr.geojson._id && lyr.geojson._id == id)
														{
															layer.removeLayer(lyr);
														}
													});
												}
											});
											
										}
									}else
									{
									}
								}
						});
					}
					RemoveSegmentsBetweenTwoNode(viewer, {id:$.webgis.select.selected_obj.id.properties.start},{id:$.webgis.select.selected_obj.id.properties.end});
					
				});
			}
			if($.webgis.select.selected_obj && $.webgis.select.selected_obj.id && ($.webgis.select.selected_obj.point || $.webgis.select.selected_obj.polyline || $.webgis.select.selected_obj.polygon) && $.webgis.data.geojsons[$.webgis.select.selected_obj.id]  && 
			(  $.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'] === 'point_marker'
			|| $.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'] === 'point_hazard'
			|| $.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'] === 'point_tower'
			|| $.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'] === 'point_dn'
			|| $.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'] === 'polyline_marker'
			|| $.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'] === 'polyline_hazard'
			|| $.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'] === 'polygon_marker'
			|| $.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'] === 'polygon_hazard'
			|| $.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'] === 'polygon_buffer'
			))
			{
				if($.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'] === 'point_tower')
				{
					if(!CheckPermission('tower_delete'))
					{
						return;
					}
				}
				if(!CheckPermission('feature_delete'))
				{
					return;
				}
				
				ShowConfirm(null, 400, 180, '删除确认', '你确认要删除对象[' + $.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['name'] + ']吗?', function(){
					//if($.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'] === 'point_tower')
					//{
						//return;
					//}
					var cond = {'db':$.webgis.db.db_name, 'collection':'features', 'action':'remove', '_id':$.webgis.select.selected_obj.id};
					MongoFind( cond, 
						function(data){
							if(data.length>0)
							{
								//console.log(data[0]);
								if(data[0]['ok'] === 1)
								{
									$.jGrowl("删除成功", { 
										life:2000,
										position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
										theme: 'bubblestylesuccess',
										glue:'before'
									});

									if($.webgis.data.geojsons[$.webgis.select.selected_obj.id])
									{
										delete $.webgis.data.geojsons[$.webgis.select.selected_obj.id];
										$.webgis.data.geojsons[$.webgis.select.selected_obj.id] = undefined;
										//console.log($.webgis.data.geojsons[$.webgis.select.selected_obj.id]);
									}
									if($.webgis.config.map_backend === 'cesium')
									{
										if($.webgis.data.czmls[$.webgis.select.selected_obj.id])
										{
											delete $.webgis.data.czmls[$.webgis.select.selected_obj.id];
											$.webgis.data.czmls[$.webgis.select.selected_obj.id] = undefined;
											//console.log($.webgis.data.czmls[$.webgis.select.selected_obj.id]);
										}
									}
									delete $.webgis.select.prev_selected_obj;
									$.webgis.select.prev_selected_obj = undefined;
									delete $.webgis.select.selected_obj;
									$.webgis.select.selected_obj = undefined;
									viewer.selectedEntity = undefined;
									viewer.trackedEntity = undefined;
									if($.webgis.config.map_backend === 'cesium')
									{
										ReloadCzmlDataSource(viewer, $.webgis.config.zaware, true);
									}
								}
								else
								{
									if(data[0]['err'] === 'edge_exist')
									{
										ShowMessage(null, 400, 300, '无法删除有关联的结点', '请先删除该结点与其他结点之间的所有关联。方法是：地图图层->线路->显示节点关系，勾选后用鼠标选择两个结点之间的关联线，点击DEL键删除。');
									}
								}
							}
					});
				});
			}
		}
	});
}





function Logout(callback)
{
	var cond = {'db':$.webgis.db.db_name, 'collection':'userinfo', 'url':'/logout'};
	MongoFind(cond, function(data){
		if(callback) callback(data);
	});

}

function InitLogout(viewer)
{
    var LogoutButtonViewModel = function() {
        var that = this;
        this._command = Cesium.createCommand(function() {
            //console.log('logout');
			ShowConfirm(null, 500, 200,
				'登出确认',
				'确认要登出吗?',
				function(){
					Logout(function(data){
						if(data.result)
						{
							window.location.href = '/webgis_login.html';
						}
					});
				},
				function(){
				}
			);
        });
        this.tooltip = '退出';
    };

    Cesium.defineProperties(LogoutButtonViewModel.prototype, {
        command : {
            get : function() {
                return this._command;
            }
        }
    });
	
    var LogoutButton = function(options) {
        if (!Cesium.defined(options) || !Cesium.defined(options.container)) {
            throw new Cesium.DeveloperError('options.container is required.');
        }
        var container = Cesium.getElement(options.container);

        var viewModel = new LogoutButtonViewModel();
        viewModel._svgPath = 'M0 765.76q0 83.936 59.292 143.472t143.228 59.536h72.224q33.184 0 56.852 -23.668t23.668 -56.852 -23.668 -56.852 -56.852 -23.668h-72.224q-17.08 0 -29.524 -12.2t-12.444 -29.768v-531.92q0 -17.08 12.444 -29.28t29.524 -12.2h72.224q33.184 0 56.852 -23.668t23.668 -56.852 -23.668 -56.608 -56.852 -23.424h-72.224q-83.936 0 -143.228 59.048t-59.292 142.984v531.92zm238.144 -251.808q0 -33.184 23.668 -56.608t56.852 -23.424h344.04l-109.8 -110.776q-23.912 -23.424 -23.912 -56.852t23.912 -56.852q23.424 -23.424 56.608 -23.424t56.608 23.424l247.416 247.904q23.424 23.424 23.424 56.608t-23.424 56.608l-242.536 242.536q-23.424 23.424 -56.608 23.424t-57.096 -23.424q-23.424 -23.424 -23.424 -56.608t23.912 -57.096l104.92 -104.92h-344.04q-32.696 0 -56.608 -23.912t-23.912 -56.608z';
        var wrapper = document.createElement('span');
        wrapper.className = 'cesium-navigationHelpButton-wrapper';
        container.appendChild(wrapper);

        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'cesium-button cesium-toolbar-button cesium-navigation-help-button';
        button.setAttribute('data-bind', '\
attr: { title: tooltip },\
click: command,\
cesiumSvgPath: { path: _svgPath, width: 1024, height: 1024 }');
        wrapper.appendChild(button);
        Cesium.knockout.applyBindings(viewModel, wrapper);

        this._container = container;
        this._viewModel = viewModel;
        this._wrapper = wrapper;

    };

    Cesium.defineProperties(LogoutButton.prototype, {
        container : {
            get : function() {
                return this._container;
            }
        },
        viewModel : {
            get : function() {
                return this._viewModel;
            }
        }
    });

    LogoutButton.prototype.isDestroyed = function() {
        return false;
    };

    LogoutButton.prototype.destroy = function() {
        Cesium.knockout.cleanNode(this._wrapper);
        this._container.removeChild(this._wrapper);
        return Cesium.destroyObject(this);
    };
	var logoutButton = new LogoutButton({
		container : $('.cesium-viewer-toolbar')[0]
	});

}

function InitLayerControl2D(viewer)
{
    var BaseLayerPickerViewModel = function(options) {
        options = Cesium.defaultValue(options, Cesium.defaultValue.EMPTY_OBJECT);

        var imageryProviderViewModels = Cesium.defaultValue(options.layers, []);
        this.imageryProviderViewModels = imageryProviderViewModels.slice(0);


        this.dropDownVisible = false;

        Cesium.knockout.track(this, ['imageryProviderViewModels', 'dropDownVisible']);

        this.buttonTooltip = undefined;
        Cesium.knockout.defineProperty(this, 'buttonTooltip', function() {
            var selectedImagery = this.selectedImagery;
            var imageryTip = Cesium.defined(selectedImagery) ? selectedImagery.name : undefined;
            if (Cesium.defined(imageryTip)) {
                return imageryTip;
            }
            return "";
        });

        this.buttonImageUrl = undefined;
        Cesium.knockout.defineProperty(this, 'buttonImageUrl', function() {
            var viewModel = this.selectedImagery;
            return Cesium.defined(viewModel) ? viewModel.iconUrl : undefined;
        });

        this.selectedImagery = undefined;
        var selectedImageryViewModel = Cesium.knockout.observable();

        this._currentImageryProviders = [];
        Cesium.knockout.defineProperty(this, 'selectedImagery', {
            get : function() {
                return selectedImageryViewModel();
            },
            set : function(value) {
                if (selectedImageryViewModel() === value) {
                    this.dropDownVisible = false;
                    return;
                }

                var imageryLayers = viewer.layers;
                for (var i in viewer.layers) {
					var layer = viewer.layers[i];
					if(viewer.hasLayer(layer))
					{
						viewer.removeLayer(layer);
						break;
					}
                }

                if (Cesium.defined(value)) 
				{
                    viewer.addLayer(value, true);
                }
                selectedImageryViewModel(value);
                this.dropDownVisible = false;
				
            }
        });


        var that = this;
        this._toggleDropDown = Cesium.createCommand(function() {
            that.dropDownVisible = !that.dropDownVisible;
        });

        this.selectedImagery = Cesium.defaultValue(options.selectedLayer, imageryProviderViewModels[0]);
    };

    Cesium.defineProperties(BaseLayerPickerViewModel.prototype, {
        toggleDropDown : {
            get : function() {
                return this._toggleDropDown;
            }
        }
    });
    var BaseLayerPicker = function(container, options) {
        if (!Cesium.defined(container)) {
            throw new Cesium.DeveloperError('container is required.');
        }

        container = Cesium.getElement(container);
        var viewModel = new BaseLayerPickerViewModel(options);

        var element = document.createElement('button');
        element.type = 'button';
        element.className = 'cesium-button cesium-toolbar-button';
        element.setAttribute('data-bind', '\
attr: { title: buttonTooltip },\
click: toggleDropDown');
        container.appendChild(element);

        var imgElement = document.createElement('img');
        imgElement.setAttribute('draggable', 'false');
        imgElement.className = 'cesium-baseLayerPicker-selected';
        imgElement.setAttribute('data-bind', '\
attr: { src: buttonImageUrl }');
        element.appendChild(imgElement);

        var dropPanel = document.createElement('div');
        dropPanel.className = 'cesium-baseLayerPicker-dropDown';
        dropPanel.setAttribute('data-bind', '\
css: { "cesium-baseLayerPicker-dropDown-visible" : dropDownVisible }');
        container.appendChild(dropPanel);

        var imageryTitle = document.createElement('div');
        imageryTitle.className = 'cesium-baseLayerPicker-sectionTitle';
        imageryTitle.setAttribute('data-bind', 'visible: imageryProviderViewModels.length > 0');
        imageryTitle.innerHTML = '选择地图';
        dropPanel.appendChild(imageryTitle);

        var imageryChoices = document.createElement('div');
        imageryChoices.className = 'cesium-baseLayerPicker-choices';
        imageryChoices.setAttribute('data-bind', 'foreach: imageryProviderViewModels');
        dropPanel.appendChild(imageryChoices);

        var imageryProvider = document.createElement('div');
        imageryProvider.className = 'cesium-baseLayerPicker-item';
        imageryProvider.setAttribute('data-bind', '\
css: { "cesium-baseLayerPicker-selectedItem" : $data === $parent.selectedImagery },\
attr: { title: tooltip },\
visible: true,\
click: function($data) { $parent.selectedImagery = $data; }');
        imageryChoices.appendChild(imageryProvider);

        var providerIcon = document.createElement('img');
        providerIcon.className = 'cesium-baseLayerPicker-itemIcon';
        providerIcon.setAttribute('data-bind', 'attr: { src: iconUrl }');
        providerIcon.setAttribute('draggable', 'false');
        imageryProvider.appendChild(providerIcon);

        var providerLabel = document.createElement('div');
        providerLabel.className = 'cesium-baseLayerPicker-itemLabel';
        providerLabel.setAttribute('data-bind', 'text: name');
        imageryProvider.appendChild(providerLabel);


        Cesium.knockout.applyBindings(viewModel, element);
        Cesium.knockout.applyBindings(viewModel, dropPanel);

        this._viewModel = viewModel;
        this._container = container;
        this._element = element;
        this._dropPanel = dropPanel;

        this._closeDropDown = function(e) {
            if (!(element.contains(e.target) || dropPanel.contains(e.target))) {
                viewModel.dropDownVisible = false;
            }
        };

        document.addEventListener('mousedown', this._closeDropDown, true);
        document.addEventListener('touchstart', this._closeDropDown, true);
    };

    Cesium.defineProperties(BaseLayerPicker.prototype, {
        container : {
            get : function() {
                return this._container;
            }
        },

        viewModel : {
            get : function() {
                return this._viewModel;
            }
        }
    });

    BaseLayerPicker.prototype.isDestroyed = function() {
        return false;
    };

    BaseLayerPicker.prototype.destroy = function() {
        document.removeEventListener('mousedown', this._closeDropDown, true);
        document.removeEventListener('touchstart', this._closeDropDown, true);
        Cesium.knockout.cleanNode(this._element);
        Cesium.knockout.cleanNode(this._dropPanel);
        this._container.removeChild(this._element);
        this._container.removeChild(this._dropPanel);
        return Cesium.destroyObject(this);
    };

	$.webgis.toolbar.BaseLayerPicker = new BaseLayerPicker($('.cesium-viewer-toolbar')[0], {layers:viewer.layers, selectedLayer:viewer.layers[0]});

}

function InitHomeButton2D(viewer)
{
    var viewHome = function() {
		var center = GetDefaultCenter($.webgis.db.db_name);
		var c = L.latLng(center[1], center[0]);
		viewer.setView(c, 10);
    }

    var HomeButtonViewModel = function(scene, duration) {
        
        duration = Cesium.defaultValue(duration, 1.5);

        this._scene = scene;
        this._duration = duration;

        var that = this;
        this._command = Cesium.createCommand(function() {
            viewHome();
        });

        this.tooltip = '默认视图';

        Cesium.knockout.track(this, ['tooltip']);
    };

    Cesium.defineProperties(HomeButtonViewModel.prototype, {
        scene : {
            get : function() {
                return this._scene;
            }
        },

        command : {
            get : function() {
                return this._command;
            }
        },

        duration : {
            get : function() {
                return this._duration;
            },
            set : function(value) {
                if (value < 0) {
                    throw new Cesium.DeveloperError('value must be positive.');
                }
                this._duration = value;
            }
        }
    });
	
    var HomeButton = function(container, scene, duration) {
        if (!Cesium.defined(container)) {
            throw new Cesium.DeveloperError('container is required.');
        }

        container = Cesium.getElement(container);

        var viewModel = new HomeButtonViewModel(scene, duration);

        viewModel._svgPath = 'M14,4l-10,8.75h20l-4.25-3.7188v-4.6562h-2.812v2.1875l-2.938-2.5625zm-7.0938,9.906v10.094h14.094v-10.094h-14.094zm2.1876,2.313h3.3122v4.25h-3.3122v-4.25zm5.8442,1.281h3.406v6.438h-3.406v-6.438z';

        var element = document.createElement('button');
        element.type = 'button';
        element.className = 'cesium-button cesium-toolbar-button cesium-home-button';
        element.setAttribute('data-bind', '\
attr: { title: tooltip },\
click: command,\
cesiumSvgPath: { path: _svgPath, width: 28, height: 28 }');

        container.appendChild(element);

        Cesium.knockout.applyBindings(viewModel, element);

        this._container = container;
        this._viewModel = viewModel;
        this._element = element;
    };

    Cesium.defineProperties(HomeButton.prototype, {
        container : {
            get : function() {
                return this._container;
            }
        },
        viewModel : {
            get : function() {
                return this._viewModel;
            }
        }
    });

    HomeButton.prototype.isDestroyed = function() {
        return false;
    };

    HomeButton.prototype.destroy = function() {
        Cesium.knockout.cleanNode(this._element);
        this._container.removeChild(this._element);

        return Cesium.destroyObject(this);
    };
	$.webgis.toolbar.HomeButton = new HomeButton($('.cesium-viewer-toolbar')[0]);

}


function InitNavigationHelp(viewer)
{
    var NavigationHelpButtonViewModel = function() {
        this.showInstructions = false;

        var that = this;
        this._command = Cesium.createCommand(function() {
            that.showInstructions = !that.showInstructions;
        });
        this._showClick = Cesium.createCommand(function() {
            that._touch = false;
        });
        this._showTouch = Cesium.createCommand(function() {
            that._touch = true;
        });

        this._touch = false;

        this.tooltip = '操作帮助';

        Cesium.knockout.track(this, ['tooltip', 'showInstructions', '_touch']);
    };

    Cesium.defineProperties(NavigationHelpButtonViewModel.prototype, {
        command : {
            get : function() {
                return this._command;
            }
        },

        showClick : {
            get : function() {
                return this._showClick;
            }
        },

        showTouch : {
            get: function() {
                return this._showTouch;
            }
        }
    });
	
    var NavigationHelpButton = function(options) {
        if (!Cesium.defined(options) || !Cesium.defined(options.container)) {
            throw new Cesium.DeveloperError('options.container is required.');
        }

        var container = Cesium.getElement(options.container);

        var viewModel = new NavigationHelpButtonViewModel();

        var showInsructionsDefault = Cesium.defaultValue(options.instructionsInitiallyVisible, false);
        viewModel.showInstructions = showInsructionsDefault;

        viewModel._svgPath = 'M16,1.466C7.973,1.466,1.466,7.973,1.466,16c0,8.027,6.507,14.534,14.534,14.534c8.027,0,14.534-6.507,14.534-14.534C30.534,7.973,24.027,1.466,16,1.466z M17.328,24.371h-2.707v-2.596h2.707V24.371zM17.328,19.003v0.858h-2.707v-1.057c0-3.19,3.63-3.696,3.63-5.963c0-1.034-0.924-1.826-2.134-1.826c-1.254,0-2.354,0.924-2.354,0.924l-1.541-1.915c0,0,1.519-1.584,4.137-1.584c2.487,0,4.796,1.54,4.796,4.136C21.156,16.208,17.328,16.627,17.328,19.003z';

        var wrapper = document.createElement('span');
        wrapper.className = 'cesium-navigationHelpButton-wrapper';
        container.appendChild(wrapper);

        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'cesium-button cesium-toolbar-button cesium-navigation-help-button';
        button.setAttribute('data-bind', '\
attr: { title: tooltip },\
click: command,\
cesiumSvgPath: { path: _svgPath, width: 32, height: 32 }');
        wrapper.appendChild(button);

        var instructionContainer = document.createElement('div');
        instructionContainer.className = 'cesium-navigation-help';
        instructionContainer.setAttribute('data-bind', 'css: { "cesium-navigation-help-visible" : showInstructions}');
        wrapper.appendChild(instructionContainer);

        var mouseButton = document.createElement('button');
        mouseButton.className = 'cesium-navigation-button cesium-navigation-button-left';
        mouseButton.setAttribute('data-bind', 'click: showClick, css: {"cesium-navigation-button-selected": !_touch, "cesium-navigation-button-unselected": _touch}');
        var mouseIcon = document.createElement('img');
        mouseIcon.src = Cesium.buildModuleUrl('Widgets/Images/NavigationHelp/Mouse.svg');
        mouseIcon.className = 'cesium-navigation-button-icon';
        mouseIcon.style.width = '25px';
        mouseIcon.style.height = '25px';
        mouseButton.appendChild(mouseIcon);
        mouseButton.appendChild(document.createTextNode('Mouse'));

        var touchButton = document.createElement('button');
        touchButton.className = 'cesium-navigation-button cesium-navigation-button-right';
        touchButton.setAttribute('data-bind', 'click: showTouch, css: {"cesium-navigation-button-selected": _touch, "cesium-navigation-button-unselected": !_touch}');
        var touchIcon = document.createElement('img');
        touchIcon.src = Cesium.buildModuleUrl('Widgets/Images/NavigationHelp/Touch.svg');
        touchIcon.className = 'cesium-navigation-button-icon';
        touchIcon.style.width = '25px';
        touchIcon.style.height = '25px';
        touchButton.appendChild(touchIcon);
        touchButton.appendChild(document.createTextNode('Touch'));

        instructionContainer.appendChild(mouseButton);
        instructionContainer.appendChild(touchButton);


        var clickInstructions = document.createElement('div');
        clickInstructions.className = 'cesium-click-navigation-help cesium-navigation-help-instructions';
        clickInstructions.setAttribute('data-bind', 'css: { "cesium-click-navigation-help-visible" : !_touch}');
        clickInstructions.innerHTML = '\
            <table>\
                <tr>\
                    <td><img src="' + Cesium.buildModuleUrl('Widgets/Images/NavigationHelp/MouseLeft.svg') + '" width="48" height="48" /></td>\
                    <td>\
                        <div class="cesium-navigation-help-pan">Pan view</div>\
                        <div class="cesium-navigation-help-details">Left click + drag</div>\
                    </td>\
                </tr>\
                <tr>\
                    <td><img src="' + Cesium.buildModuleUrl('Widgets/Images/NavigationHelp/MouseRight.svg') + '" width="48" height="48" /></td>\
                    <td>\
                        <div class="cesium-navigation-help-zoom">Zoom view</div>\
                        <div class="cesium-navigation-help-details">Right click + drag, or</div>\
                        <div class="cesium-navigation-help-details">Mouse wheel scroll</div>\
                    </td>\
                </tr>\
                <tr>\
                    <td><img src="' + Cesium.buildModuleUrl('Widgets/Images/NavigationHelp/MouseMiddle.svg') + '" width="48" height="48" /></td>\
                    <td>\
                        <div class="cesium-navigation-help-rotate">Rotate view</div>\
                        <div class="cesium-navigation-help-details">Middle click + drag, or</div>\
                        <div class="cesium-navigation-help-details">CTRL + Left click + drag</div>\
                    </td>\
                </tr>\
            </table>';

        instructionContainer.appendChild(clickInstructions);

        var touchInstructions = document.createElement('div');
        touchInstructions.className = 'cesium-touch-navigation-help cesium-navigation-help-instructions';
        touchInstructions.setAttribute('data-bind', 'css: { "cesium-touch-navigation-help-visible" : _touch}');
        touchInstructions.innerHTML = '\
            <table>\
                <tr>\
                    <td><img src="' + Cesium.buildModuleUrl('Widgets/Images/NavigationHelp/TouchDrag.svg') + '" width="70" height="48" /></td>\
                    <td>\
                        <div class="cesium-navigation-help-pan">Pan view</div>\
                        <div class="cesium-navigation-help-details">One finger drag</div>\
                    </td>\
                </tr>\
                <tr>\
                    <td><img src="' + Cesium.buildModuleUrl('Widgets/Images/NavigationHelp/TouchZoom.svg') + '" width="70" height="48" /></td>\
                    <td>\
                        <div class="cesium-navigation-help-zoom">Zoom view</div>\
                        <div class="cesium-navigation-help-details">Two finger pinch</div>\
                    </td>\
                </tr>\
                <tr>\
                    <td><img src="' + Cesium.buildModuleUrl('Widgets/Images/NavigationHelp/TouchTilt.svg') + '" width="70" height="48" /></td>\
                    <td>\
                        <div class="cesium-navigation-help-rotate">Tilt view</div>\
                        <div class="cesium-navigation-help-details">Two finger drag, same direction</div>\
                    </td>\
                </tr>\
                <tr>\
                    <td><img src="' + Cesium.buildModuleUrl('Widgets/Images/NavigationHelp/TouchRotate.svg') + '" width="70" height="48" /></td>\
                    <td>\
                        <div class="cesium-navigation-help-tilt">Rotate view</div>\
                        <div class="cesium-navigation-help-details">Two finger drag, opposite direction</div>\
                    </td>\
                </tr>\
            </table>';

        instructionContainer.appendChild(touchInstructions);

        Cesium.knockout.applyBindings(viewModel, wrapper);

        this._container = container;
        this._viewModel = viewModel;
        this._wrapper = wrapper;

        this._closeInstructions = function(e) {
            if (!wrapper.contains(e.target)) {
                viewModel.showInstructions = false;
            }
        };

        document.addEventListener('mousedown', this._closeInstructions, true);
        document.addEventListener('touchstart', this._closeInstructions, true);
    };

    Cesium.defineProperties(NavigationHelpButton.prototype, {
        container : {
            get : function() {
                return this._container;
            }
        },

        viewModel : {
            get : function() {
                return this._viewModel;
            }
        }
    });

    NavigationHelpButton.prototype.isDestroyed = function() {
        return false;
    };

    NavigationHelpButton.prototype.destroy = function() {
        document.removeEventListener('mousedown', this._closeInstructions, true);
        document.removeEventListener('touchstart', this._closeInstructions, true);

        Cesium.knockout.cleanNode(this._wrapper);
        this._container.removeChild(this._wrapper);

        return Cesium.destroyObject(this);
    };
	
	$.webgis.toolbar.NavigationHelpButton = new NavigationHelpButton({
		container : $('.cesium-viewer-toolbar')[0]
	});
	
}

function InitRuler(viewer)
{
    var RulerButtonViewModel = function() {
        var that = this;
        this._command = Cesium.createCommand(function() {
			if($.webgis.control.drawhelper_mode === undefined)
			{
				$.webgis.control.drawhelper_mode = 'ruler';
				$(that.button).css('background-color', 'rgba(0, 255, 0, 0.5)');
				if(!$.webgis.control.drawhelper.isVisible())
				{
					$.webgis.control.drawhelper.show(true);
				}
				
			}
			else
			{
				$.webgis.control.drawhelper_mode = undefined;
				$(that.button).css('background-color', 'rgba(38, 38, 38, 0.75)');
				if($.webgis.control.drawhelper.isVisible())
				{
					$.webgis.control.drawhelper.clearPrimitive();
					$.webgis.control.drawhelper.show(false);
				}
			}
        });
        this.tooltip = '测量';
    };

    Cesium.defineProperties(RulerButtonViewModel.prototype, {
        command : {
            get : function() {
                return this._command;
            }
        }
    });
	
    var RulerButton = function(options) {
        if (!Cesium.defined(options) || !Cesium.defined(options.container)) {
            throw new Cesium.DeveloperError('options.container is required.');
        }
        var container = Cesium.getElement(options.container);

        var viewModel = new RulerButtonViewModel();
        viewModel._svgPath = 'M21.828,0L0,21.418l5.414,5.517L27.24,5.517L21.828,0z M23.486,7.317l-0.748,0.735l-1.089-1.11l-0.691,0.679l1.089,1.109  l-1.028,1.008l-1.676-1.709l-0.692,0.679l1.677,1.708L19.58,11.15l-1.088-1.109l-0.691,0.678l1.087,1.11l-1.009,0.99l-1.853-1.888  l-0.693,0.679l1.854,1.888l-0.748,0.733l-1.265-1.289l-0.692,0.679l1.265,1.289l-1.026,1.007l-1.853-1.888l-0.692,0.679l1.854,1.888  l-0.748,0.734l-1.265-1.29l-0.691,0.679l1.265,1.29l-0.948,0.93L9.79,17.049l-0.692,0.679l1.854,1.889l-0.748,0.733l-1.265-1.289  L8.249,19.74l1.264,1.289l-1.026,1.008l-1.854-1.888l-0.691,0.678l1.853,1.889L7.046,23.45l-1.265-1.29l-0.69,0.679l1.265,1.29  l-0.924,0.906l-3.53-3.598L21.81,1.901l3.53,3.597L24.177,6.64L22.5,4.931l-0.691,0.678L23.486,7.317z';
        var wrapper = document.createElement('span');
        wrapper.className = 'cesium-navigationHelpButton-wrapper';
        container.appendChild(wrapper);

        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'cesium-button cesium-toolbar-button cesium-navigation-help-button';
        button.setAttribute('data-bind', '\
attr: { title: tooltip },\
click: command,\
cesiumSvgPath: { path: _svgPath, width: 28, height: 28 }');
        wrapper.appendChild(button);
		viewModel.button = button;
        Cesium.knockout.applyBindings(viewModel, wrapper);

        this._container = container;
        this._viewModel = viewModel;
        this._wrapper = wrapper;

    };

    Cesium.defineProperties(RulerButton.prototype, {
        container : {
            get : function() {
                return this._container;
            }
        },
        viewModel : {
            get : function() {
                return this._viewModel;
            }
        }
    });
	
	
    RulerButton.prototype.isDestroyed = function() {
        return false;
    };

    RulerButton.prototype.destroy = function() {
        Cesium.knockout.cleanNode(this._wrapper);
        this._container.removeChild(this._wrapper);
        return Cesium.destroyObject(this);
    };
	
	//console.log($('.cesium-viewer-toolbar'));
	$.webgis.toolbar.rulerButton = new RulerButton({
		container : $('.cesium-viewer-toolbar')[0]
	});
}

function InitAntiBird(viewer)
{
	$('#div_anti_bird_inform_icon').hide();
	InitAntiBirdEquipListData(viewer);
	InitAntiBirdWebsocket(viewer);
	InitAntiBirdTool(viewer);
}

function AntiBirdBadgeMessageListReload(data, filter)
{
	$('#anti_bird_msg_list_list').empty();
	$("#anti_bird_msg_list_list").append('<ul></ul>');
	var i;
	for(i = data.length - 1; i>-1; i--)
	{
		var item = data[i];
		//var liprefix = '<li id="' + item.uid + '@' + item.imei + '" class="ui-widget-content"><a id="anti_bird_msg_item_link_@' + item.imei + '" href="javascript:void(0);" class="anti-bird-msg-list-item">';
		var liprefix = '<li id="' + item.uid + '@' + item.imei + '" class="ui-widget-content"><a  href="javascript:void(0);" class="anti-bird-msg-list-item">';
		//var lipostfix = '</a><a id="anti_bird_msg_item_clear_@' + item.uid + '" href="javascript:void(0);" class="anti-bird-msg-list-item" style="float:right;">清除</a></li>';
		var lipostfix = '</a></li>';
		if(item.name)
		{
			if(filter && filter.length>0)
			{
				if(item.name.indexOf(filter)>-1 || item.imei.indexOf(filter)>-1)
				{
					//$('#anti_bird_msg_list_list ul').append(liprefix + item.imei + '(' + item.name + ')' + lipostfix);
					$('#anti_bird_msg_list_list ul').append(liprefix +  '(' + item.name + ')' + lipostfix);
				}
			}else
			{
				//$('#anti_bird_msg_list_list ul').append(liprefix + item.imei + '(' + item.name + ')' + lipostfix);
				$('#anti_bird_msg_list_list ul').append(liprefix +  '(' + item.name + ')' + lipostfix);
			}
		}else
		{
			if(filter && filter.length>0)
			{
				if(item.imei.indexOf(filter)>-1)
				{
					$('#anti_bird_msg_list_list ul').append(liprefix + item.imei  + lipostfix);
				}
			}else
			{
				$('#anti_bird_msg_list_list ul').append(liprefix + item.imei  + lipostfix);
			}
		}
	}
	
	$("#anti_bird_msg_list_list ul").selectable({
		selected: function( event, ui ) {
			if($(ui.selected).attr('id'))
			{
				var arr = $(ui.selected).attr('id').split('@');
				//console.log(arr);
				ShowAntiBirdInfoDialog($.webgis.viewer, arr[1], 200);
			}
		}
		//selecting: function( event, ui ) {
			//if( $(".ui-selected, .ui-selecting").length > 1){
                  //$(ui.selecting).removeClass("ui-selecting");
                  //$(ui.selecting).removeClass("ui-selected");
            //}
		//},
	});	
	
}
function AntiBirdBadgeMessageArrival(viewer, message)
{
	if($.webgis.data.antibird.unread_msg_queue === undefined)
	{
		$.webgis.data.antibird.unread_msg_queue = [];
	}
	var obj = {};
	if(message.imei)
	{
		if($.webgis.data.antibird.anti_bird_equip_tower_mapping === undefined)
		{
			$.webgis.data.antibird.anti_bird_equip_tower_mapping = {};
		}
		if($.webgis.data.antibird.anti_bird_equip_tower_mapping[message.imei])
		{
			obj = $.extend(true, {}, $.webgis.data.antibird.anti_bird_equip_tower_mapping[message.imei]);
		}
		obj.imei = message.imei;
		obj.uid = $.uuid();
		$.webgis.data.antibird.unread_msg_queue.push(obj);
		$('#button_anti_bird').show();
		if(obj.lng && obj.lat)
		{
			var pos;
			if($.webgis.config.map_backend === 'cesium')
			{
				pos = Cesium.SceneTransforms.wgs84ToWindowCoordinates(viewer.scene, Cesium.Cartesian3.fromDegrees(obj.lng, obj.lat));
			}
			if($.webgis.config.map_backend === 'leaflet')
			{
				pos = viewer.latLngToContainerPoint(L.latLng(obj.lat, obj.lng));
				//console.log(pos);
			}
			var x = Math.floor(pos.x), y = Math.floor(pos.y);
			$('#div_anti_bird_inform_icon').css('top', y + 'px').css('left', x + 'px');
			$('#div_anti_bird_inform_icon').show('shake', { percent: 100 }, 400, function(){
				$( "#div_anti_bird_inform_icon" ).effect( 'transfer', { to: "#button_anti_bird", className: "ui-effects-transfer" }, 1500, function(){
					AntiBirdBadgeIncrease($.webgis.data.antibird.unread_msg_queue.length);
					AntiBirdBadgeMessageListReload($.webgis.data.antibird.unread_msg_queue, '');
					$('#div_anti_bird_inform_icon').hide();
				});
			});
		}
		else
		{
			AntiBirdBadgeIncrease($.webgis.data.antibird.unread_msg_queue.length);
			AntiBirdBadgeMessageListReload($.webgis.data.antibird.unread_msg_queue, '');
		}
	}
}
function AntiBirdBadgeDecrease(content)
{
	//$("#button_anti_bird").empty();
	$("#button_anti_bird").iosbadge({ theme: 'green', size: 28, position:'bottom-right', content:content });
}
function AntiBirdBadgeIncrease(content)
{
	//theme:red,blue,green,grey,ios
	//size: `20`, `22`, `24`, `26`, `28`, `30`, `32`, `34` and `36`
	//position: `'top-left'`, `'top-right'`, `'bottom-left'` or `'bottom-right'`
	$("#button_anti_bird").iosbadge({ theme: 'green', size: 28, position:'bottom-right',content:content });
	//effect:shake, bounce
	$( "#button_anti_bird" ).effect( 'bounce', {}, 500 );
}
function InitAntiBirdTool(viewer)
{
	$("#button_anti_bird").hide();
	$("#anti_bird_msg_list_container").hide();
	$("#button_anti_bird").on('click', function(){
		if($("#anti_bird_msg_list_container").css('display') === 'none')
		{
			$("#anti_bird_msg_list_container").show('slide', {direction:'right'}, 500, function(){
				try{
					$('#button_anti_bird_msg_list_clear').button('destroy');
				}catch(e)
				{
					//console.log(e);
				}
				$('#button_anti_bird_msg_list_clear').button({label:'全部清除'});
				$('#button_anti_bird_msg_list_clear').on('click', function(){
					$.webgis.data.antibird.unread_msg_queue = [];
					$("#anti_bird_msg_list_container").hide('slide', {direction:'right'}, 500, function(){
						$("#button_anti_bird").hide();
					});
				});
			});
		}else
		{
			$("#anti_bird_msg_list_container").hide('slide', {direction:'right'}, 500, function(){
			});
		}
	});
	$('#anti_bird_msg_list_filter').on('keyup', function(e){
		var text = $(e.target).val();
		AntiBirdBadgeMessageListReload($.webgis.data.antibird.unread_msg_queue, text);
	});
	//if(true)
	//{
		//$("#button_anti_bird").show();
		//$("#anti_bird_msg_list_container").show();
		//$('#button_anti_bird_msg_list_clear').button({label:'全部清除'});
		//AntiBirdBadgeMessageListReload([{imei:1},{imei:2},{imei:3},{imei:4},{imei:5},{imei:6},{imei:7},{imei:8},{imei:9},{imei:10},{imei:11},{imei:12},{imei:13},{imei:14},{imei:15},{imei:16}], '');
	//}
}

function testheatmap(viewer)
{
	var randnum = function(min, max) {
		return Math.random() * (max - min) + min;
	}	
	var randint = function(min, max) {
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}
	var testdata = function(mapping){
		var ret = [];
		for(var k in mapping)
		{
			var obj = {};
			obj.radius = 3;
			obj.intensity = randnum(0.2, 100.0);
			obj.center = Cesium.Cartographic.fromDegrees(mapping[k].lng, mapping[k].lat, 0);
			ret.push(obj);
		}
		return ret;
	};
	var testdata1 = function(mapping){
		var ret = [];
		for(var k in mapping)
		{
			var obj = {};
			obj.radius = 100;
			obj.intensity = randnum(0, 200);
			obj.lng = mapping[k].lng;
			obj.lat = mapping[k].lat;
			obj.name = mapping[k].name;
			obj.tower_id = mapping[k].tower_id;
			ret.push(obj);
		}
		return ret;
	};
	var testdata2d = function(mapping){
		var ret = {};
		var data = [];
		for(var k in mapping)
		{
			var obj = {};
			obj.radius = 0.15;
			obj.value = randnum(0, 50);
			obj.lng = mapping[k].lng;
			obj.lat= mapping[k].lat;
			data.push(obj);
		}
		ret.max = data.length;
		ret.data = data;
		return ret;
	};
	if($.webgis.config.map_backend === 'cesium')
	{
		var points = testdata($.webgis.data.antibird.anti_bird_equip_tower_mapping);
		$.webgis.data.heatmap_layers['testheatmap'] = {
			layer: new HeatMapImageryProvider({
						name:'testheatmap',
						viewer:viewer,
						defaultAlpha:0.3,
						gradientStops:$.webgis.mapping.heat_map_gradient_stops,
						points:points
					}),
			type: 'heatmap'
		};
		//var points = testdata1($.webgis.data.antibird.anti_bird_equip_tower_mapping);
		//DrawHeatMapCircle(viewer, points);
	}
	if($.webgis.config.map_backend === 'leaflet')
	{	
		var cfg = {
		  // radius should be small ONLY if scaleRadius is true (or small radius is intended)
		  // if scaleRadius is false it will be the constant radius used in pixels
		  "radius": 2,
		  "maxOpacity": 0.6, 
		  // scales the radius based on map zoom
		  "scaleRadius": true, 
		  // if set to false the heatmap uses the global maximum for colorization
		  // if activated: uses the data maximum within the current map boundaries 
		  //   (there will always be a red spot with useLocalExtremas true)
		  "useLocalExtrema": false,
		  // which field name in your data represents the latitude - default "lat"
		  latField: 'lat',
		  // which field name in your data represents the longitude - default "lng"
		  lngField: 'lng',
		  // which field name in your data represents the data value - default "value"
		  valueField: 'value'
		};
		$.webgis.data.heatmap_layers['testheatmap']  = new HeatmapOverlay(cfg);
		viewer.addLayer($.webgis.data.heatmap_layers['testheatmap'], true);
		$.webgis.data.heatmap_layers['testheatmap'].setData(testdata2d($.webgis.data.antibird.anti_bird_equip_tower_mapping));
	}
}

function DrawHeatMapPixel(viewer, hid, list)
{
	var randnum = function(min, max) {
		return Math.random() * (max - min) + min;
	}	
	var randint = function(min, max) {
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}
	var get_max_min = function(list)
	{
		var ret = [99999, 0];
		for(var i in list)
		{
			var item = list[i];
			if(item.count > ret[1])
			{
				ret[1] = item.count;
			}
			if(item.count < ret[0])
			{
				ret[0] = item.count;
			}
		}
		return ret;
	};
	var add_geo_info = function(list, range, pixelsize){
		var ret = [];
		for(var i in list)
		{
			var item = list[i];
			if($.webgis.data.antibird.anti_bird_equip_tower_mapping[item.imei])
			{
				var o = $.webgis.data.antibird.anti_bird_equip_tower_mapping[item.imei];
				o.radius = pixelsize;
				//o.intensity = item.count;
				o.intensity = (item.count - range[0])/(range[1] - range[0]);
				o.text = item.text;
				o.center = Cesium.Cartographic.fromDegrees(o.lng, o.lat, 0);
				ret.push(o);
			}
		}
		return ret;
	};
	var add_geo_info2d = function(list, range, radius){
		var ret = {};
		var data = [];
		for(var i in list)
		{
			var item = list[i];
			if($.webgis.data.antibird.anti_bird_equip_tower_mapping[item.imei])
			{
				var o = $.webgis.data.antibird.anti_bird_equip_tower_mapping[item.imei];
				o.radius = radius;
				o.intensity = item.count;
				//o.intensity = (item.count - range[0])/(range[1] - range[0]);
				o.text = item.text;
				data.push(o);
			}
		}
		ret.max = data.length;
		ret.data = data;
		return ret;
	};
	var range = get_max_min(list);
	if($.webgis.config.map_backend === 'cesium')
	{
		var points = add_geo_info(list, range,  3);
		if($.webgis.data.heatmap_layers[hid])
		{
			$.webgis.data.heatmap_layers[hid].layer.destroy();
			delete $.webgis.data.heatmap_layers[hid];
			//$.webgis.data.heatmap_layers[hid] = undefined;
		}
		$.webgis.data.heatmap_layers[hid] = {
			layer: new HeatMapImageryProvider({
						name:hid,
						viewer:viewer,
						defaultAlpha:0.3,
						gradientStops:$.webgis.mapping.heat_map_gradient_stops,
						points:points
					}),
			type: 'heatmap'
		};
	}
	if($.webgis.config.map_backend === 'leaflet')
	{	
		var points = add_geo_info2d(list, range, 0.1);
		var cfg = {
		  // radius should be small ONLY if scaleRadius is true (or small radius is intended)
		  // if scaleRadius is false it will be the constant radius used in pixels
		  "radius": 2,
		  "maxOpacity": 0.6, 
		  // scales the radius based on map zoom
		  "scaleRadius": true, 
		  // if set to false the heatmap uses the global maximum for colorization
		  // if activated: uses the data maximum within the current map boundaries 
		  //   (there will always be a red spot with useLocalExtremas true)
		  "useLocalExtrema": false,
		  // which field name in your data represents the latitude - default "lat"
		  latField: 'lat',
		  // which field name in your data represents the longitude - default "lng"
		  lngField: 'lng',
		  // which field name in your data represents the data value - default "value"
		  valueField: 'intensity'
		};
		
		if(viewer.hasLayer($.webgis.data.heatmap_layers[hid]))
		{
			viewer.removeLayer($.webgis.data.heatmap_layers[hid]);
			delete $.webgis.data.heatmap_layers[hid];
			//$.webgis.data.heatmap_layers[hid] = undefined;
		}
		$.webgis.data.heatmap_layers[hid]  = new HeatmapOverlay(cfg);
		viewer.addLayer($.webgis.data.heatmap_layers[hid], true);
		$.webgis.data.heatmap_layers[hid].setData(points);
	}

}
function DrawHeatMapCircle(viewer, hid, list, height_magnifier)
{
	var get_max_min = function(list)
	{
		var ret = [99999, 0];
		for(var i in list)
		{
			var item = list[i];
			if(item.count > ret[1])
			{
				ret[1] = item.count;
			}
			if(item.count < ret[0])
			{
				ret[0] = item.count;
			}
		}
		return ret;
	};
	var get_gradient_list = function()
	{
		var ret = [];
		for(var k in $.webgis.mapping.heat_map_gradient_stops)
		{
			//ret.push(parseFloat(k));
			ret.push(k);
		}
		ret.sort();
		return ret;
	}
	var get_alpha = function(range, gradient_list, v)
	{
		var ret = '0.5';
		var vv = (v - range[0])/(range[1] - range[0]);
		for(var i=1;i< gradient_list.length; i++)
		{
			var min = gradient_list[i-1];
			var max = gradient_list[i];
			if(vv >= parseFloat(min) && vv <= parseFloat(max))
			{
				ret = max;
				break;
			}
		}
		return ret;
	};
	var num_to_color = function(num)
	{
		var hexStr = num.toString(16);
		while (hexStr.length < 6) 
		{ 
			hexStr = '0' + hexStr; 
		}
		return '#' + hexStr;
	};
	//var get_gradient_stop = function(range, gradient_list, v)
	//{
		//var ret = [255, 255, 255, 0];
		//var a = get_alpha(range, gradient_list, v);
		////console.log(a);
		//if($.webgis.mapping.heat_map_gradient_stops[a])
		//{
			//var c = $.webgis.mapping.heat_map_gradient_stops[a];
			//c = num_to_color(c);
			//c = c.substr(0, c.length-2);
			////console.log(c);
			//var rgba = tinycolor(c).toRgb();
			//rgba.a = Math.floor(parseFloat(a) * 256) -1;
			//ret = [rgba.r, rgba.g, rgba.b, rgba.a];
			////console.log(ret);
		//}
		//return ret;
	//};
	var get_gradient_stop = function(range, gradient_list, v)
	{
		var ret = 'rgba(255, 255, 255, 0)';
		var a = get_alpha(range, gradient_list, v);
		if($.webgis.mapping.heat_map_gradient_stops[a])
		{
			var c = $.webgis.mapping.heat_map_gradient_stops[a];
			c = num_to_color(c);
			c = c.substr(0, c.length-2);
			var rgba = tinycolor(c).toRgb();
			rgba.a = parseFloat(a) * 0.5;
			ret = 'rgba(' + rgba.r + ',' + rgba.g + ',' + rgba.b + ',' + rgba.a + ')';
		}
		return ret;
	};
	//var get_gradient_stop2 = function(range, gradient_list, v)
	//{
		//var ret = 0;
		//var a = get_alpha(range, gradient_list, v);
		////console.log(a);
		//if($.webgis.mapping.heat_map_gradient_stops[a])
		//{
			//ret = $.webgis.mapping.heat_map_gradient_stops[a];
		//}
		//return ret;
	//};
	
	var add_geo_info = function(list, radius){
		var ret = [];
		for(var i in list)
		{
			var item = list[i];
			if($.webgis.data.antibird.anti_bird_equip_tower_mapping[item.imei])
			{
				var o = $.webgis.data.antibird.anti_bird_equip_tower_mapping[item.imei];
				o.radius = radius;
				o.count = item.count;
				o.text = item.text;
				ret.push(o);
			}
		}
		return ret;
	};
	
	
	var range = get_max_min(list);
	var gradient_list = get_gradient_list();
	var ellipsoid = viewer.scene.globe.ellipsoid;
	var collection = new Cesium.PrimitiveCollection();
	var labels = new Cesium.LabelCollection();
	var points = add_geo_info(list, 500);
	for(var i in points)
	{
		var point = points[i];
		var rgba = get_gradient_stop(range, gradient_list, point.count);
		var alt = point.alt;
		if(!$.webgis.config.zaware) alt = 0;
		var pos = Cesium.Cartesian3.fromDegrees(point.lng, point.lat, alt);
		var pos_label = Cesium.Cartesian3.fromDegrees(point.lng, point.lat, alt + point.count * height_magnifier);
		var geometry = new Cesium.CircleGeometry({
				center : pos,
				radius: point.radius,
				ellipsoid: ellipsoid,
				extrudedHeight : point.count * height_magnifier,
				vertexFormat : Cesium.PerInstanceColorAppearance.VERTEX_FORMAT,
		});
		labels.add({
			position : pos_label,
			text : point.name + ' ' + point.text,
			font : 'bold 30px arial,sans-serif',
			fillColor : Cesium.Color.fromCssColorString(rgba),
			outlineColor : Cesium.Color.WHITE,
			style : Cesium.LabelStyle.FILL,
			pixelOffset : Cesium.Cartesian2.ZERO,
			eyeOffset : Cesium.Cartesian3.ZERO,
			horizontalOrigin : Cesium.HorizontalOrigin.LEFT,
			verticalOrigin : Cesium.VerticalOrigin.BOTTOM,
			scale : 1.0		  
		});		
		var primitive = new Cesium.Primitive({
			geometryInstances : new Cesium.GeometryInstance({
				id:	$.uuid(),
				geometry : geometry,
				attributes : {
					color : Cesium.ColorGeometryInstanceAttribute.fromColor(Cesium.Color.fromCssColorString(rgba))
				}
			}),
			appearance : new Cesium.PerInstanceColorAppearance({
				flat:true,
				closed : true,
				translucent : true,
				//material : Cesium.Material.fromType('Color', {
					//color : Cesium.Color.fromCssColorString(rgba)
				//}),
				renderState : {
					depthTest : {
						enabled : true
					}
				}
			})
		});
		collection.add(primitive);
	}
	if($.webgis.data.heatmap_primitive === undefined)
	{
		$.webgis.data.heatmap_primitive = {};
	}
	if($.webgis.data.heatmap_primitive[hid])
	{
		if(viewer.scene.primitives.contains($.webgis.data.heatmap_primitive[hid]))
		{
			viewer.scene.primitives.remove($.webgis.data.heatmap_primitive[hid]);
		}
		delete $.webgis.data.heatmap_primitive[hid];
		//$.webgis.data.heatmap_primitive[hid] = undefined;
	}
	if($.webgis.data.heatmap_primitive[hid + 'label'])
	{
		if(viewer.scene.primitives.contains($.webgis.data.heatmap_primitive[hid + 'label']))
		{
			viewer.scene.primitives.remove($.webgis.data.heatmap_primitive[hid + 'label']);
		}
		delete $.webgis.data.heatmap_primitive[hid + 'label'];
		//$.webgis.data.heatmap_primitive[hid + 'label'] = undefined;
	}
	viewer.scene.primitives.add(collection);
	viewer.scene.primitives.add(labels);
	$.webgis.data.heatmap_primitive[hid] = collection;
	$.webgis.data.heatmap_primitive[hid + 'label'] = labels;
}

function InitAntiBirdEquipListData(viewer)
{
	var url = '/anti_bird_equip_list';
	ShowProgressBar(true, 670, 200, '加载中', '正在加载驱鸟设备信息，请稍候...');
	$.get(url, {is_filter_used:true}, function( data1 ){
		ShowProgressBar(false);
		ret = JSON.parse(decodeURIComponent(data1));
		$.webgis.data.antibird.anti_bird_equip_list = ret;
		url = '/anti_bird_equip_tower_mapping';
		ShowProgressBar(true, 670, 200, '加载中', '正在加载驱鸟设备与杆塔绑定信息，请稍候...');
		$.get(url, {}, function( data1 ){
			ShowProgressBar(false);
			ret = JSON.parse(decodeURIComponent(data1));
			$.webgis.data.antibird.anti_bird_equip_tower_mapping = ret;
			//testheatmap(viewer);
		}, 'text');
	}, 'text');
}
function InitAntiBirdWebsocket(viewer)
{
	var wsurl =  $.webgis.websocket.antibird.WS_PROTOCOL + "://" + $.webgis.websocket.antibird.HOST + ":" + $.webgis.websocket.antibird.PORT + "/websocket";
	if($.webgis.websocket.antibird.websocket === undefined)
	{
		//$.webgis.websocket.antibird.websocket = new WebSocket(wsurl);
		$.webgis.websocket.antibird.websocket = new ReconnectingWebSocket(wsurl, null, {reconnectInterval: 4000});
	}
	if($.webgis.websocket.antibird.websocket)
	{
		$.webgis.websocket.antibird.websocket.onopen = function() 
		{
			$.webgis.websocket.antibird.websocket.send('');
		};
		$.webgis.websocket.antibird.websocket.onclose = function(e) 
		{
			console.log("websocket close");
		};
		$.webgis.websocket.antibird.websocket.onerror = function(e) 
		{
			console.log("websocket error:" + e);
		};
		$.webgis.websocket.antibird.websocket.onmessage = function(e) 
		{
			if(e.data.length>0)
			{
				var data1 = JSON.parse(e.data);
				
				if(data1 instanceof Array)
				{
				}
				if(data1 instanceof Object)
				{
					if(data1.result)
					{
						console.log(data1.result);
					}
					else
					{
						console.log(data1);
						AntiBirdBadgeMessageArrival(viewer, data1);
						$.webgis.websocket.antibird.websocket.send('');
					}
				}
				
			}else
			{
				$.webgis.websocket.antibird.websocket.send('');
			}
		};
	}		
}


function InitDrawHelper2D(viewer)
{
	$.webgis.control.drawhelper = new DrawHelper2D(viewer, 'drawhelpertoolbar');
	var toolbar = $.webgis.control.drawhelper.addToolbar($('#' + $.webgis.control.drawhelper.toolbar_container_id)[0], {
		buttons: ['marker', 'polyline', 'polygon', 'circle', 'extent']
	});
	
	toolbar.addListener('markerCreated', function(event) {
		console.log('Marker created at ' + GetDisplayLatLngString2D(event.position, 7));
		if($.webgis.control.drawhelper_mode != 'ruler')
		{
			var m = L.marker(event.position,{
				icon:L.icon({
					iconUrl: Cesium.buildModuleUrl('/img/marker30x48.png'),
					iconSize: [30, 48],
					iconAnchor: [15, 48]
				})
			});
			m.name = 'tmp_marker';
			m.addTo(viewer);
			ShowPoiInfoDialog(viewer, '添加兴趣点', 'point',  event.position);
		}
	});
	toolbar.addListener('polylineCreated', function(event) {
		//event.positions.pop();
		event.positions.pop();
		console.log('Polyline created with ' + event.positions.length + ' points');
		if($.webgis.control.drawhelper_mode != 'ruler')
		{
			ShowPoiInfoDialog(viewer, '添加线段或道路', 'polyline', event.positions);
		}
	});
	toolbar.addListener('polygonCreated', function(event) {
		//event.positions.pop();
		event.positions.pop();
		console.log('Polygon created with ' + event.positions.length + ' points');
		if($.webgis.control.drawhelper_mode != 'ruler')
		{
			ShowPoiInfoDialog(viewer, '添加多边形区域', 'polygon', event.positions);
		}
	});
	toolbar.addListener('circleCreated', function(event) {
		console.log('Circle created: center is ' + event.center.toString() + ' and radius is ' + event.radius.toFixed(1) + ' meters');
		//var circle = new DrawHelper.CirclePrimitive({
			//center: event.center,
			//radius: event.radius,
			//material: drawHelperCoverAreaMaterial
		//});
		//viewer.scene.primitives.add(circle);
		//$.webgis.control.drawhelper.addPrimitive(circle);
		if($.webgis.control.drawhelper_mode != 'ruler')
		{
			ShowPoiInfoCircleDialog(viewer, '添加圆形区域', event.center, event.radius);
		}
	});
	toolbar.addListener('extentCreated', function(event) {
		var positions = event.positions;
		console.log('Extent created (N: ' + positions[0].lat.toFixed(3) + ', E: ' + positions[2].lng.toFixed(3) + ', S: ' + positions[1].lat.toFixed(3) + ', W: ' + positions[0].lng.toFixed(3) + ')');
		if($.webgis.control.drawhelper_mode != 'ruler')
		{
			ShowPoiInfoDialog(viewer, '添加矩形区域', 'polygon', positions);
		}
	});

}


function InitDrawHelper(viewer)
{
	var ellipsoid = viewer.scene.globe.ellipsoid;
	$.webgis.control.drawhelper = new DrawHelper(viewer, 'drawhelpertoolbar');
	var toolbar = $.webgis.control.drawhelper.addToolbar($('#' + $.webgis.control.drawhelper.toolbar_container_id)[0], {
		buttons: ['marker', 'polyline', 'polygon', 'circle', 'extent']
	});
	
	
    var drawHelperCoverAreaMaterial = Cesium.Material.fromType('Color', {
		color : new Cesium.Color(1.0, 1.0, 0.0, 0.35)
	});
	
	
	toolbar.addListener('markerCreated', function(event) {
		console.log('Marker created at ' + GetDisplayLatLngString(ellipsoid, event.position, 7));
		// create one common billboard collection for all billboards
		if($.webgis.control.drawhelper_mode != 'ruler')
		{
			var b = new Cesium.BillboardCollection();
			viewer.scene.primitives.add(b);
			$.webgis.control.drawhelper.addPrimitive(b);
			var billboard = b.add({
				show : true,
				position : event.position,
				pixelOffset : new Cesium.Cartesian2(0, 0),
				eyeOffset : new Cesium.Cartesian3(0.0, 0.0, 0.0),
				horizontalOrigin : Cesium.HorizontalOrigin.CENTER,
				verticalOrigin : Cesium.VerticalOrigin.BOTTOM,
				scale : 0.15,
				//imageIndex : 0,
				image: 'img/location_marker.png',
				color : new Cesium.Color(1.0, 1.0, 1.0, 1.0)
			});
			//billboard.setEditable();
			ShowPoiInfoDialog(viewer, '添加兴趣点', 'point', event.position);
		}
	});
	toolbar.addListener('polylineCreated', function(event) {
		//maybe cesium1.7 fix this bug
		//event.positions.pop();
		//event.positions.pop();
		console.log('Polyline created with ' + event.positions.length + ' points');
		//console.log(event.positions);
		var polyline = new DrawHelper.PolylinePrimitive({
			positions: event.positions,
			width: 5,
			geodesic: true
		});
		viewer.scene.primitives.add(polyline);
		$.webgis.control.drawhelper.addPrimitive(polyline);
		if($.webgis.control.drawhelper_mode != 'ruler')
		{
			ShowPoiInfoDialog(viewer, '添加线段或道路', 'polyline', event.positions);
		}
		//polyline.setEditable();
		//polyline.addListener('onEdited', function(event) {
			//console.log('Polyline edited, ' + event.positions.length + ' points');
		//});
	});
	toolbar.addListener('polygonCreated', function(event) {
		//maybe cesium1.7 fix this bug
		//event.positions.pop();
		//event.positions.pop();
		console.log('Polygon created with ' + event.positions.length + ' points');
		var polygon = new DrawHelper.PolygonPrimitive({
			positions: event.positions,
			material : drawHelperCoverAreaMaterial
		});
		viewer.scene.primitives.add(polygon);
		$.webgis.control.drawhelper.addPrimitive(polygon);
		if($.webgis.control.drawhelper_mode != 'ruler')
		{
			ShowPoiInfoDialog(viewer, '添加多边形区域', 'polygon', event.positions);
		}
		//polygon.setEditable();
		//polygon.addListener('onEdited', function(event) {
			//console.log('Polygon edited, ' + event.positions.length + ' points');
		//});

	});
	toolbar.addListener('circleCreated', function(event) {
		console.log('Circle created: center is ' + event.center.toString() + ' and radius is ' + event.radius.toFixed(1) + ' meters');
		var circle = new DrawHelper.CirclePrimitive({
			center: event.center,
			radius: event.radius,
			material: drawHelperCoverAreaMaterial
		});
		viewer.scene.primitives.add(circle);
		$.webgis.control.drawhelper.addPrimitive(circle);
		if($.webgis.control.drawhelper_mode != 'ruler')
		{
			ShowPoiInfoCircleDialog(viewer, '添加圆形区域', event.center, event.radius);
		}
		//ShowPoiInfoDialog(viewer, '添加圆形区域', 'circle', null, null);
		//circle.setEditable();
		//circle.addListener('onEdited', function(event) {
			//console.log('Circle edited: radius is ' + event.radius.toFixed(1) + ' meters');
		//});
	});
	toolbar.addListener('extentCreated', function(event) {
		var extent = event.extent;
		console.log('Extent created (N: ' + Cesium.Math.toDegrees(extent.north).toFixed(3) + ', E: ' + Cesium.Math.toDegrees(extent.east).toFixed(3) + ', S: ' + Cesium.Math.toDegrees(extent.south).toFixed(3) + ', W: ' + Cesium.Math.toDegrees(extent.west).toFixed(3) + ')');
		var extentPrimitive = new DrawHelper.ExtentPrimitive({
			extent: extent,
			material: drawHelperCoverAreaMaterial
		});
		viewer.scene.primitives.add(extentPrimitive);
		$.webgis.control.drawhelper.addPrimitive(extentPrimitive);
		if($.webgis.control.drawhelper_mode != 'ruler')
		{
			var positions = [];
			//console.log(extent);
			var carto = Cesium.Cartographic.fromRadians(extent.west, extent.north, 0);
			var cart3 = ellipsoid.cartographicToCartesian(carto);
			positions.push(cart3);
			carto = Cesium.Cartographic.fromRadians(extent.east, extent.north, 0);
			cart3 = ellipsoid.cartographicToCartesian(carto);
			positions.push(cart3);
			carto = Cesium.Cartographic.fromRadians(extent.east, extent.south, 0);
			cart3 = ellipsoid.cartographicToCartesian(carto);
			positions.push(cart3);
			carto = Cesium.Cartographic.fromRadians(extent.west, extent.south, 0);
			cart3 = ellipsoid.cartographicToCartesian(carto);
			positions.push(cart3);
			ShowPoiInfoDialog(viewer, '添加矩形区域', 'polygon', positions);
		}
		//extentPrimitive.setEditable();
		//extentPrimitive.addListener('onEdited', function(event) {
			//console.log('Extent edited: extent is (N: ' + event.extent.north.toFixed(3) + ', E: ' + event.extent.east.toFixed(3) + ', S: ' + event.extent.south.toFixed(3) + ', W: ' + event.extent.west.toFixed(3) + ')');
		//});
	});
	$.webgis.control.drawhelper._tooltip.setVisible(false);
}

function ShowPoiInfoCircleDialog(viewer, title, center, radius)
{
	var ellipsoid;
	if($.webgis.config.map_backend === 'cesium')
	{
		ellipsoid = viewer.scene.globe.ellipsoid;
	}
	var g = {};
	g['geometry'] = {}
	g['geometry']['type'] = 'Point';
	//console.log(center);
	if($.webgis.config.map_backend === 'cesium')
	{
		var carto = ellipsoid.cartesianToCartographic(center);
		g['geometry']['coordinates'] = [Cesium.Math.toDegrees(carto.longitude), Cesium.Math.toDegrees(carto.latitude)];
	}
	if($.webgis.config.map_backend === 'leaflet')
	{
		g['geometry']['coordinates'] = [center.lng, center.lat];
	}
	var cond = {'db':$.webgis.db.db_name, 'collection':'-', 'action':'buffer', 'data':g, 'distance':radius, 'res':8};
	//ShowProgressBar(true, 670, 200, '生成缓冲区', '正在生成缓冲区，请稍候...');
	MongoFind(cond, function(data){
		//ShowProgressBar(false);
		if(data.length>0)
		{
			var geometry = data[0];
			var positions = [];
			for(var i in geometry['coordinates'][0])
			{
				var coord = geometry['coordinates'][0][i];
				if($.webgis.config.map_backend === 'cesium')
				{
					var carto = Cesium.Cartographic.fromDegrees(coord[0], coord[1], 0);
					var cart3 = ellipsoid.cartographicToCartesian(carto);
					positions.push(cart3);
				}
				if($.webgis.config.map_backend === 'leaflet')
				{
					positions.push(L.latLng(coord[1], coord[0]));
				}
			}
			ShowPoiInfoDialog(viewer, title, 'polygon', positions);
			
		}else
		{
			ShowMessage(null, 400, 250, '出错了', '服务器生成圆形错误:返回数据为空,请确认服务正在运行.');
		}
	});

}

function InitFileUploader(div_id, fileext,  bindcollection, key) 
{
	var width = parseInt($('#' + div_id).css('width').replace('px', ''));
	var height = parseInt($('#' + div_id).css('height').replace('px', ''));
	var container_id = div_id + '_container';
	var uploader_id = 'div_' + div_id + '_uploader';
	var toggle_id = 'div_' + div_id + '_toggle_view_upload';
	var toolbar_id = div_id + '_toolbar';
	var form_id = 'form_' + div_id + '_uploader_form';
	
	$('#' + toggle_id).off();
	$('#' + toggle_id).on('click', function(){
		$('#div_' + div_id + '_upload_desciption').css('display','none');
		if($('#' + uploader_id).is(':visible') )
		{
			$('#' + uploader_id).css('display', 'none');
			$('#' + container_id).css('display', 'block');
			$('#' + toolbar_id).css('display', 'block');
			$('#' + toggle_id).html('上传附件');
		}
		else
		{
			$('#' + uploader_id).css('display', 'block');
			$('#' + container_id).css('display', 'none');
			$('#' + toolbar_id).css('display', 'none');
			$('#' + toggle_id).html('附件浏览');
		}
	});

    $('#' + form_id).fileupload({
        // Uncomment the following to send cross-domain cookies:
        //xhrFields: {withCredentials: true},
        url: 'post',
		multipart:true,
		autoUpload: false,
		sequentialUploads:true,
		submit: function(e, data){
			//console.log('submit key=' +  key);
			//console.log(data);
			var category = '';
			if(data.files[0].type === 'image/jpeg'
			|| data.files[0].type === 'image/png'
			|| data.files[0].type === 'image/tiff'
			|| data.files[0].type === 'image/gif'
			|| data.files[0].type === 'image/bmp'
			|| data.files[0].type === 'image/svg+xml'
			) {
				category = 'image';
			}
			if(data.files[0].type === 'application/vnd.ms-excel'
			|| data.files[0].type === 'application/msword'
			|| data.files[0].type === 'text/plain'
			) {
				category = 'document';
			}
			if(category.length == 0) category = 'other';
			$(this).fileupload('option', 'url', 'post' + '?' 
				+ 'db=' + $.webgis.db.db_name 
				//+ '&collection=fs'
				+ '&bindcollection=' + bindcollection
				+ '&key=' + key 
				+ '&category=' + category
				+ '&mimetype=' + encodeURIComponent(data.files[0].type) 
				//+ '&filename=' + encodeURIComponent(data.files[0].name)
				//+ '&size=' + data.files[0].size
				+ '&description=' + encodeURIComponent($('#' + div_id + '_upload_desciption').val())
			);
		},
		change:function(){
			$('#div_' + div_id + '_upload_desciption').css('display','block');
		},
		done:function(e, data){
			//console.log(data.result);
			if(data.result)
			{
				//UpdateJssorSlider(div_id, bindcollection, key);
				UpdateFotoramaSlider(div_id, bindcollection, key, CreateFileBrowserAdditionalButton(div_id, bindcollection, key));
				$('#' + div_id + '_upload_desciption').val('');
			}
		},
		fail:function(e, data){
			console.log('fail');
			console.log(data);
		}
    });

    // Enable iframe cross-domain access via redirect option:
    $('#' + form_id).fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );


    if ($.webgis.config.max_file_size > 0) {
		var res = '';
		for(var i in fileext)
		{
			res += fileext[i] + '|';
		}
		res = res.slice(0, res.length-1);
		res = '(\.|\/)(' + res + ')$';
		var re = new RegExp(res, "i");
        // Demo settings:
        $('#' + form_id).fileupload('option', {
            url: '/post',
            // Enable image resizing, except for Android and Opera,
            // which actually support image resizing, but fail to
            // send Blob objects via XHR requests:
            disableImageResize: /Android(?!.*Chrome)|Opera/
                .test(window.navigator.userAgent),
            maxFileSize: $.webgis.config.max_file_size,
            //acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i
            acceptFileTypes: re
        });
        // Upload server status check for browsers with CORS support:
        if ($.support.cors) {
            $.ajax({
                url: 'post',
                type: 'HEAD'
            }).fail(function () {
                $('<div class="alert alert-danger"/>')
                    .text('文件上传服务不可用 ' +
                            new Date())
                    .appendTo('#' + form_id);
            });
        }
    } else {
        // Load existing files:
        $('#' + form_id).addClass('fileupload-processing');
        $.ajax({
            // Uncomment the following to send cross-domain cookies:
            //xhrFields: {withCredentials: true},
            url: $('#' + form_id).fileupload('option', 'url'),
            dataType: 'json',
            context: $('#' + form_id)[0]
        }).always(function () {
            $(this).removeClass('fileupload-processing');
        }).done(function (result) {
            $(this).fileupload('option', 'done')
                .call(this, $.Event('done'), {result: result});
        });
    }

}




function InitPoiInfoDialog()
{
	//$('#form_poi_info' ).webgisform("getvalidate");

}
//function InitTowerInfoDialog()
//{
	//var iframe = $('#tower_info_model').find('iframe');
	//iframe.load(function(){
		//var iframeDoc = iframe.contents().get(0);
		//$(iframeDoc).off();
		//$(iframeDoc).on('mousedown', function(e){
			//for (var i = 1; i < 99; i++)
			//{
				//iframe[0].contentWindow.clearInterval(i);
			//}
		//});
	//});
//}

function InitToolPanel(viewer)
{
	$('#control_toolpanel_kmgd_handle').css('z-index', '9');
	$('#control_toolpanel_kmgd_left').css('display', 'none');
	$('#control_toolpanel_kmgd_handle').on( 'mouseenter', function(e){
		$('#control_toolpanel_kmgd_left').show('slide',{}, 400, function(){
			$(e.target).css('display','none');
		});
	});
	$('#control_toolpanel_kmgd_left').on( 'mouseleave', function(e){
		$('#control_toolpanel_kmgd_left').hide('slide',{}, 400, function(){
			$('#control_toolpanel_kmgd_handle').css('display','block');
		});
	});
	$( "#accordion_tools" ).accordion({ 
		active: 0,
		animate: 20
	});
	
	$('input[id^=chb_show_label_]').iCheck({
		checkboxClass: 'icheckbox_flat-green'
	});
	$('input[id^=chb_show_geometry_]').iCheck({
		checkboxClass: 'icheckbox_flat-green'
	});
	$('input[id^=chb_show_icon_]').iCheck({
		checkboxClass: 'icheckbox_flat-green'
	});
	$('input[id^=chb_show_icon_]').iCheck('check');
	
	//$('#chb_show_label').on('click', function(){
	$('input[id^=chb_show_label_]').on("ifChanged", function(e){
		var webgis_type = $(this).attr('id').replace('chb_show_label_', '');
		if($(this).is(':checked'))
		{
			console.log('turn on label:' + webgis_type);
		}else
		{
			console.log('turn off label:' + webgis_type);
		}
		if($.webgis.config.map_backend === 'cesium')
		{
			ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
		}
	});
	$('input[id^=chb_show_geometry_]').on("ifChanged", function(e){
		var webgis_type = $(this).attr('id').replace('chb_show_geometry_', '');
		if(webgis_type === 'edge_tower')
		{
			if($(this).is(':checked'))
			{
				console.log('turn on edge:' + webgis_type);
				if($.webgis.config.map_backend === 'cesium')
				{
					for(var k in $.webgis.data.geojsons)
					{
						DrawEdgeBetweenTwoNode(viewer, 'edge_tower', $.webgis.data.geojsons[k]['properties']['start'], $.webgis.data.geojsons[k]['properties']['end'], false);
					}
				}
				if($.webgis.config.map_backend === 'leaflet')
				{
					UpdateEdges2D(viewer, webgis_type);
				}
			}else
			{
				console.log('turn off edge:' + webgis_type);
				if($.webgis.config.map_backend === 'cesium')
				{
					RemoveSegmentsByType(viewer, 'edge_tower');
				}
				if($.webgis.config.map_backend === 'leaflet')
				{
					ClearEdges2D(viewer, webgis_type);
				}
			}
		}
		else
		{
			if($(this).is(':checked'))
			{
				console.log('turn on geometry:' + webgis_type);
			}else
			{
				console.log('turn off geometry:' + webgis_type);
				if($.webgis.config.map_backend === 'leaflet')
				{
					ClearEdges2D(viewer, webgis_type);
				}
			}
			if($.webgis.config.map_backend === 'cesium')
			{
				ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
			}
		}
	});
	$('input[id^=chb_show_icon_]').on("ifChanged", function(e){
		if($(this).is(':checked'))
		{
			console.log('turn on icon:' + 'point');
		}else
		{
			console.log('turn off icon:' + 'point');
		}
		if($.webgis.config.map_backend === 'cesium')
		{
			ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
		}
	});
	
	$('#slider_heatmap_alpha').slider({ 
		min: 0.0,
		max: 1.0,
		step: 0.01,
		range:false,
		value:0.7,
		change: function( event, ui ) {
			//console.log(ui.value);
			$('#slider_heatmap_alpha').parent().find('label').html('透明度:' + Math.floor(ui.value*100) + '%');
			for(var k in $.webgis.data.heatmap_layers)
			{
				var hm = $.webgis.data.heatmap_layers[k];
				hm.layer.alpha = ui.value;
			}
		}
	});
	$('#but_heatmap_clear').button({label:'清除'});
	$('#but_heatmap_clear').on('click', function(){
		if($.webgis.config.map_backend === 'cesium')
		{
			while(Object.keys($.webgis.data.heatmap_layers).length>0)
			{
				var k = Object.keys($.webgis.data.heatmap_layers)[0];
				//console.log(k);
				var hm = $.webgis.data.heatmap_layers[k];
				//console.log(hm.type);
				if(hm && hm.type === 'heatmap')
				{
					hm.layer.destroy();
				}
				if(hm && hm.type === 'tile')
				{
					viewer.scene.imageryLayers.remove(hm.layer, true);
				}
				delete $.webgis.data.heatmap_layers[k];
				//$.webgis.data.heatmap_layers[k] = undefined;
			}
			while(Object.keys($.webgis.data.heatmap_primitive).length>0)
			{
				var k = Object.keys($.webgis.data.heatmap_primitive)[0];
				//console.log(k);
				if(viewer.scene.primitives.contains($.webgis.data.heatmap_primitive[k]))
				{
					viewer.scene.primitives.remove($.webgis.data.heatmap_primitive[k]);
				}
				delete $.webgis.data.heatmap_primitive[k];
				//$.webgis.data.heatmap_primitive[k] = undefined;
			}
		}
		if($.webgis.config.map_backend === 'leaflet')
		{
			//console.log($.webgis.data.heatmap_layers);
			while(Object.keys($.webgis.data.heatmap_layers).length>0)
			{
				k = Object.keys($.webgis.data.heatmap_layers)[0];
				var hm = $.webgis.data.heatmap_layers[k];
				if(viewer.hasLayer(hm))
				{
					viewer.removeLayer(hm);
					delete $.webgis.data.heatmap_layers[k];
					//$.webgis.data.heatmap_layers[k] = undefined;
				}
			}
		}
	});
	
	
	$('#but_add_poi').button({label:'添加兴趣点'});
	$('#but_add_poi').on('click', function(){
		if($.webgis.control.drawhelper.isVisible())
		{
			$.webgis.control.drawhelper.show(false);
		}
		else
		{
			$.webgis.control.drawhelper.show(true);
		}
	});
	$('#but_remove_poi').button({label:'清空兴趣点'});
	$('#but_remove_poi').on('click', function(){
		ClearPoi(viewer);
	});
	
	$('#but_line_edit').button({label:'查看列表'});
	$('#but_line_edit').on('click', function(){
		if(!CheckPermission('line_edit'))
		{
			return;
		}
		ShowLineDialog(viewer, 'edit');
	});
	$('#but_line_add').button({label:'新增'});
	$('#but_line_add').on('click', function(){
		if(!CheckPermission('line_save'))
		{
			return;
		}
		ShowLineDialog(viewer);
	});
	$('#but_line_delete').button({label:'删除'});
	$('#but_line_delete').on('click', function(){
		if(!CheckPermission('line_delete'))
		{
			return;
		}
		var arr = $('#line_choose').multipleSelect("getSelects");
		var textarr = $('#line_choose').multipleSelect("getSelects", 'text');
		if(arr.length>0 && $.webgis.data.lines[arr[0]])
		{
			ShowConfirm(null, 500, 200,
				'删除确认',
				'确认删除[' + textarr[0] + ']并保存吗? 确认的话数据将会提交到服务器上，以便所有人都能看到修改的结果。',
				function () {
					DeleteLine(viewer, arr[0], function(){
						LoadLineData($.webgis.db.db_name, function(){
							$('#line_choose').empty();
							for(var k in $.webgis.data.lines)
							{
								$('#line_choose').append('<option value="' + k + '">' + $.webgis.data.lines[k]['properties']['name'] + '</option>');
							}
							$('#line_choose').multipleSelect("refresh");
						});					
					});
				},
				function () {
					//$('#').dialog("close");
				}
			);
		}
	});
	
	$('#but_dn_add').button({label:'新增配电网络'});
	$('#but_dn_add').on('click', function(){
		if(!CheckPermission('dn_save'))
		{
			return;
		}
		ShowDNAddDialog(viewer);
	});
	$('#but_dn_remove').button({label:'清空配电网络'});
	$('#but_dn_remove').on('click', function(){
		if($.webgis.config.map_backend === 'cesium')
		{
			RemoveSegmentsByType(viewer, 'edge_dn');
		}
		if($.webgis.config.map_backend === 'leaflet')
		{
			ClearEdges2D(viewer, 'edge_dn');
		}
	});
	
	$('#but_sys_change_password').button({label:'修改密码'});
	$('#but_sys_change_password').on('click', function(){
		ShowChangePassword(viewer);
	});
	
	if($.webgis.current_userinfo['username'] === 'admin')
	{
		$('#but_sys_role').button({label:'权限控制'});
		$('#but_sys_role').on('click', function(){
			ShowRoleControl(viewer);
		});
	}else
	{
		$('#but_sys_role').hide();
	}
}

function ClearEdges2D(viewer, webgis_type)
{
	viewer.eachLayer(function (layer) {
		if(layer.name && layer.name.indexOf( webgis_type)>-1)
		{
			viewer.removeLayer(layer);
		}
	});
	$.webgis.geometry.segments.length = 0;
}


function AddEdgeBetweenTwoNode2D(viewer, webgis_type, start_obj, end_obj, isfresh)
{
	if(CheckSegmentsExist(start_obj, end_obj, webgis_type))
	{
		return;
	}
	
	//var polylinelayer;
	//viewer.eachLayer(function (layer) {
		//if(layer.name && layer.name === webgis_type)
		//{
			//polylinelayer = layer;
			//return;
		//}
	//});
	if(webgis_type === undefined)
	{
		return;
	}
	var pair = DrawEdgeBetweenTwoNode(viewer, webgis_type, start_obj['_id'], end_obj['_id'], isfresh);
	if(pair)
	{
		var o = {};
		o['_id'] = 'tmp_edge';
		o['type'] = 'Feature';
		o['properties'] = {webgis_type:webgis_type,start:start_obj['_id'], end:end_obj['_id']};
		var color = ColorArrayToHTMLColor([200,200,0,1]);
		if(isfresh)
		{
			color = ColorArrayToHTMLColor([255,255,0,1]);
		}
		var polyline = L.polyline(pair, {
			color: color,
			weight:5,
			fillOpacity:1.0,
			clickable:true
		});
		polyline.geojson = o;			
		var edgeobj = GetEdgeLeafletByWebgisType(viewer, webgis_type, polyline);
		if(edgeobj.exist)
		{
			edgeobj.polyline.addLayer(polyline);
			edgeobj.arrow._paths.push(pair);
			edgeobj.arrow.setPaths(edgeobj.arrow._paths);
		}
	}
}

function UpdateEdges2D(viewer, webgis_type)
{
	var pairlist = [];
	for(var k in $.webgis.data.geojsons)
	{
		
		if($.webgis.data.geojsons[k]['properties'] && $.webgis.data.geojsons[k]['properties']['start'] && $.webgis.data.geojsons[k]['properties']['end'])
		{
			var pair = DrawEdgeBetweenTwoNode(viewer, webgis_type, $.webgis.data.geojsons[k]['properties']['start'], $.webgis.data.geojsons[k]['properties']['end'], false);
			if(pair)
			{
				pair.push($.webgis.data.geojsons[k]);
				pairlist.push(pair);
			}
		}
	}
	
	if(pairlist.length>0)
	{
		//ClearEdges2D(viewer, webgis_type);
		var polylinelist = [];
		var pairlist1 = [];
		for(var i in pairlist)
		{
			var pair = [pairlist[i][0], pairlist[i][1]];
			pairlist1.push(pair);
			var polyline = L.polyline(pair, {
				color: 'yellow',
				weight:5,
				fillOpacity:1.0,
				clickable:true
			});
			polyline.geojson = pairlist[i][2];
			polylinelist.push(polyline);
		}
		
		if(polylinelist.length>0)
		{
			var edgeobj = GetEdgeLeafletByWebgisType(viewer, webgis_type, polylinelist[0]);
			for(var i in polylinelist)
			{
				if(i === 0 && !edgeobj.exist) continue;
				edgeobj.polyline.addLayer(polylinelist[i]);
			}
			edgeobj.arrow.setPaths(pairlist1);
		}
	}
	
}


function GetEdgeLeafletByWebgisType(viewer, webgis_type, initpolyline)
{
	var lyr_polylinegroup, lyr_arrow;
	viewer.eachLayer(function (layer) {
		if(layer.name && layer.name === webgis_type)
		{
			lyr_polylinegroup = layer;
			return;
		}
	});
	viewer.eachLayer(function (layer) {
		if(layer.name && layer.name === webgis_type + '_arrow')
		{
			lyr_arrow = layer;
			return;
		}
	});
	var exist = true;
	if(lyr_polylinegroup === undefined)
	{
		exist = false;
		var lyr_polylinegroup =  L.featureGroup([initpolyline]);
		lyr_polylinegroup.name = webgis_type;
		
		lyr_polylinegroup.on('click', function(e){
			ClearSelectColor2D(viewer);
			if($.webgis.select.selected_obj)
			{
				$.webgis.select.prev_selected_obj = $.webgis.select.selected_obj;
			}
			$.webgis.select.selected_obj = {};
			$.webgis.select.selected_obj.id = e.layer.geojson;
			console.log('edge:' + e.layer.geojson._id);
			$.webgis.mapping.leaflet_old_style[e.layer.geojson._id] = {color:e.layer.options.color, weight:e.layer.options.weight};
			e.layer.setStyle({color : 'green', weight:10});
			OnSelect(viewer, null);
		});		
		lyr_polylinegroup.addTo(viewer);
	}
	if(lyr_arrow === undefined)
	{
		exist = false;
		lyr_arrow = L.polylineDecorator([initpolyline], {
			patterns: [
				{offset: 100, repeat: 100, symbol: L.Symbol.arrowHead({pixelSize: 15, pathOptions: {fillOpacity: 1, weight: 0}})}
			]
		});
		lyr_arrow.name = webgis_type + '_arrow';
		lyr_arrow.addTo(viewer);
	}
	return {polyline:lyr_polylinegroup, arrow:lyr_arrow, exist:exist};
}

function ShowChangePassword(viewer)
{
	$('#dlg_change_password').dialog({
		width: 420,
		height: 320,
		minWidth:200,
		minHeight: 200,
		draggable: true,
		resizable: true, 
		modal: false,
		position:{at: "center"},
		title:'修改密码',
		close: function(event, ui){
		},
		show: {
			effect: "blind",
			//direction: "right",
			duration: 200
		},
		hide: {
			effect: "blind",
			//direction: "right",
			duration: 200
		},		
		buttons:[
			{ 	
				text: "确定", 
				click: function(e){
					if($('#form_change_password').valid())
					{
						var data = $('#form_change_password').webgisform('getdata');
						if(data['password_new'] != data['password_new1'])
						{
							$.jGrowl("两次输入的新密码不一致,请检查", { 
								life: 2000,
								position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
								theme: 'bubblestylefail',
								glue:'before'
							});
							return;
						}
						var that = this;
						var username;
						if($.webgis.current_userinfo['username'] === 'admin')
						{
							username = data['username'];
						}
						else
						{
							username = $.webgis.current_userinfo['username'];
							if(data['password_old'] != $.webgis.current_userinfo['password'])
							{
								$.jGrowl("旧密码不正确,请检查", { 
									life: 2000,
									position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
									theme: 'bubblestylefail',
									glue:'before'
								});
								return;
							}
						}
						if(username && username.length>0)
						{
							
							ShowConfirm(null, 500, 200,
								'保存确认',
								'确认保存新修改的密码吗? ',
								function(){
									var cond = {'db':$.webgis.db.db_name, 'collection':'userinfo', 'action':'update','data':{'password':data['password_new']}, 'username':username};
									ShowProgressBar(true, 670, 200, '保存用户信息', '正在保存用户信息，请稍候...');
									MongoFind(cond, function(data1){
										ShowProgressBar(false);
										$.jGrowl("保存成功", { 
											life: 2000,
											position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
											theme: 'bubblestylesuccess',
											glue:'before'
										});
										$( that ).dialog( "close" );
								});
							},function(){
								$( that ).dialog( "close" );
							});
						}else
						{
							$.jGrowl("请选择用户名", { 
								life: 2000,
								position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
								theme: 'bubblestylefail',
								glue:'before'
							});
						}
					}
				}
			},
			{ 	
				text: "关闭", 
				click: function(e){
					$( this ).dialog( "close" );
				}
			}
		]
	});
	var flds;
	if($.webgis.current_userinfo['username'] === 'admin')
	{
		var cond = {'db':$.webgis.db.db_name, 'collection':'userinfo'};
		ShowProgressBar(true, 670, 200, '获取用户信息', '正在获取用户信息，请稍候...');
		MongoFind(cond, function(data1){
			ShowProgressBar(false);
			var userlist = [];
			for(var i in data1)
			{
				userlist.push({'value':data1[i]['username'], 'label':data1[i]['displayname']});
			}
			flds = [
				{ display: "选择用户", id: "username", newline: true,  type: "select", editor:{data:userlist}, group:'用户信息', labelwidth:130, width:200, validate:{required:true}, change:function(selected){
					for(var i in data1)
					{
						if(data1[i]['username'] === selected)
						{
							$('#form_change_password').webgisform('set', 'password_old', data1[i]['password']);
							var password_old = $('#form_change_password').webgisform('get', 'password_old');
							//console.log(password_old[0]);
							$(password_old[0]).focus(function(){
								this.type = "text";
							}).blur(function(){
								this.type = "password";
							})							
							break;
						}
					}
				}},
				{ display: "旧密码", id: "password_old", newline: true,  type: "password",  group:'用户信息', labelwidth:130, width:200, validate:{required:true}},
				{ display: "新密码", id: "password_new", newline: true,  type: "password",  group:'用户信息', labelwidth:130, width:200, validate:{required:true}},
				{ display: "确认新密码", id: "password_new1", newline: true,  type: "password",  group:'用户信息', labelwidth:130, width:200, validate:{required:true}},
			];
			$('#form_change_password').webgisform(flds, {
					//divorspan: "div",
					prefix: "form_change_password_",
					maxwidth: 370
					//margin:10,
					//groupmargin:10
			});
		});
		
	}else
	{
		flds = [
			{display: "旧密码", id: "password_old", newline: true,  type: "password",  group:'用户信息', labelwidth:130, width:200, validate:{required:true}},
			{display: "新密码", id: "password_new", newline: true,  type: "password",  group:'用户信息', labelwidth:130, width:200, validate:{required:true}},
			{display: "确认新密码", id: "password_new1", newline: true,  type: "password",  group:'用户信息', labelwidth:130, width:200, validate:{required:true}},
		];
		$('#form_change_password').webgisform(flds, {
			//divorspan: "div",
			prefix: "form_change_password_",
			maxwidth: 370
			//margin:10,
			//groupmargin:10
		});
	}
}

function ShowRoleControl(viewer)
{
	$('#dlg_change_role').dialog({
		width: 420,
		height: 570,
		minWidth:200,
		minHeight: 200,
		draggable: true,
		resizable: true, 
		modal: false,
		position:{at: "center"},
		title:'权限设定',
		close: function(event, ui){
		},
		show: {
			effect: "blind",
			//direction: "right",
			duration: 200
		},
		hide: {
			effect: "blind",
			//direction: "right",
			duration: 200
		},		
		buttons:[
			{ 	
				text: "确定", 
				click: function(e){
					var that = this;
					if($('#form_change_role').valid())
					{
						ShowConfirm(null, 500, 200,
							'保存确认',
							'确认保存该角色权限设置吗? ',
							function(){
								var data = $('#form_change_role').webgisform('getdata');
								if(data['roleid'] && data['roleid'].length>0)
								{
									var cond = {'db':$.webgis.db.db_name, 'collection':'sysrole', 'action':'update','data':{'users':data['users'], 'permission':get_permission()}, '_id':data['roleid']};
									//console.log(cond);
									ShowProgressBar(true, 670, 200, '保存权限信息', '正在保存权限信息，请稍候...');
									MongoFind(cond, function(data1){
										ShowProgressBar(false);
										$.jGrowl("保存成功", { 
											life: 2000,
											position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
											theme: 'bubblestylesuccess',
											glue:'before'
										});
										$( that ).dialog( "close" );
									});
								}else
								{
									$.jGrowl("请选择权限名", { 
										life: 2000,
										position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
										theme: 'bubblestylefail',
										glue:'before'
									});
								}
						});
					}
				}
			},
			{ 	
				text: "关闭", 
				click: function(e){
					$( this ).dialog( "close" );
				}
			}
		]
	});
	var get_permission = function()
	{
		var ret = [];
		$.each($('input[id^=form_change_role_role_functions_]'), function(i, element){
			if($(element).is(':checked'))
			{
				ret.push($(element).attr('id').replace('form_change_role_role_functions_',''));
			}
		});
		return ret;
	};
	var update_form = function()
	{
		var userlist = [];
		var rolelist = [];
		var cond = {'db':$.webgis.db.db_name, 'collection':'userinfo'};
		ShowProgressBar(true, 670, 200, '获取用户信息', '正在获取用户信息，请稍候...');
		MongoFind(cond, function(data1){
			ShowProgressBar(false);
			for(var i in data1)
			{
				if(data1[i]['username'] != 'admin')
				{
					userlist.push({'value':data1[i]['_id'], 'label':data1[i]['displayname']});
				}
			}
			cond = {'db':$.webgis.db.db_name, 'collection':'sysrole'};
			ShowProgressBar(true, 670, 200, '获取权限信息', '正在获取权限信息，请稍候...');
			MongoFind(cond, function(data2){
				ShowProgressBar(false);
				for(var i in data2)
				{
					if(data2[i]['name'] != 'admin')
					{
						rolelist.push({'value':data2[i]['_id'], 'label':data2[i]['displayname']});
					}
				}
				
				var flds = [
					{display: "角色列表", id: "roleid", newline: true,  type: "select", editor:{data:rolelist},  group:'角色', labelwidth:130, width:200, validate:{required:true}, 
						change:function(selected){
							var users = $('#form_change_role').webgisform('get', 'users');
							
							$('input[id^=form_change_role_role_functions_]' ).iCheck('uncheck');
							for(var i in data2)
							{
								if(data2[i]['_id'] === selected)
								{
									
									$(users[0]).multipleSelect("setSelects", data2[i]['users']);
									for(var j in data2[i]['permission'])
									{
										$('#form_change_role_role_functions_' + data2[i]['permission'][j]).iCheck('check');
									}
									break;
								}
							}
						}
					},
					{display: "用户列表", id: "users", newline: true,  type: "multiselect", editor:{data:userlist},  group:'用户', labelwidth:130, width:200, validate:{required:true}},
				];
				
				
				for(var i in $.webgis.mapping.role_functions)
				{
					flds.push({display: $.webgis.mapping.role_functions[i]['label'], id: "role_functions_" + $.webgis.mapping.role_functions[i]['value'], newline: true,  type: "checkbox", defaultvalue:false,  group:'允许功能', labelwidth:270});
				}
				
				
				$('#form_change_role').empty();
				$('#form_change_role').webgisform(flds, {
					prefix: "form_change_role_",
					maxwidth: 370
					//margin:10,
					//groupmargin:10
				});
				
			});
		});
	};
	update_form();
}


function ClearPoi(viewer)
{
	var scene = viewer.scene;
	delete $.webgis.data.czmls;
	$.webgis.data.czmls = {};
	ReloadCzmlDataSource(viewer, $.webgis.config.zaware, true);
	for(var k in $.webgis.data.gltf_models)
	{
		var m = $.webgis.data.gltf_models[k];
		if(scene.primitives.contains(m))
		{
			var b = scene.primitives.remove(m);
			//console.log(b);
		}
	}
}

function TranslateToCN()
{
	$('.cesium-home-button').attr('title', '返回初始视角');
	$('.cesium-navigation-help-button').attr('title', '快速操作帮助');
	$($('.cesium-baseLayerPicker-sectionTitle')[0]).html('地表图源');
	//$($('.cesium-baseLayerPicker-sectionTitle')[0]).attr('imgtype', 'imagery');
	$($('.cesium-baseLayerPicker-sectionTitle')[1]).html('3D地型数据源');
	//$($('.cesium-baseLayerPicker-sectionTitle')[1]).attr('imgtype', 'terrain');
	$('.cesium-navigation-help-pan').html('平移');
	$('.cesium-navigation-help-pan').siblings().html('左键点击 + 拖动');
	$('.cesium-navigation-help-zoom').html('缩放');
	$($('.cesium-navigation-help-zoom').siblings()[0]).html('右键点击 + 拖动, 或');
	$($('.cesium-navigation-help-zoom').siblings()[1]).html('鼠标滚轮');
	$('.cesium-touch-navigation-help .cesium-navigation-help-zoom').next().html('两指滑动');
	$('.cesium-click-navigation-help .cesium-navigation-help-rotate').html('视角旋转');
	$($('.cesium-navigation-help-rotate').siblings()[0]).html('中键点击 + 拖动, 或');
	$($('.cesium-navigation-help-rotate').siblings()[1]).html('CTRL + 左键点击 + 拖动');
	$('.cesium-touch-navigation-help .cesium-navigation-help-rotate').html('视角翻转');
	$('.cesium-touch-navigation-help .cesium-navigation-help-rotate').next().html('两指同向滑动');
	$('.cesium-touch-navigation-help .cesium-navigation-help-tilt').html('视角旋转');
	$('.cesium-touch-navigation-help .cesium-navigation-help-tilt').next().html('两指反向滑动');
}

function InitModelList(viewer)
{
	//$('#tower_info_model_list_toggle').button();
	//$('#tower_info_model_list_toggle').on( 'mouseenter', function(e){
		//$(e.target).css('cursor', 'hand');
	//});
	//$('#tower_info_model_list_toggle').on( 'mouseleave', function(e){
		//$(e.target).css('cursor', 'pointer');
	//});
	$('#tower_info_model_list_toggle').on('click', function(e) {
		if($('#tower_info_model_list').css('display') == 'block')
		{
			$(e.target).html('>>显示列表');
			$('#tower_info_model_list').css('display', 'none');
			$('#tower_info_model').find('iframe').css('width', '99%');
		}
		else
		{
			$(e.target).html('<<隐藏列表');
			$('#tower_info_model_list').css('display', 'block');
			$('#tower_info_model').find('iframe').css('width', '79%');
		}
	});
	
	$('#tower_info_model_list_filter').on('keyup', function(e){
		var text = $(e.target).val();
		FilterModelList(text);
	});
}

function GetCheckedBoxList(prefix)
{
	var ret = [];
	$.each($( "input[id^=" + prefix + "]"), function(i, element){
		if($(element).is(':checked'))
		{
			ret.push($(element).attr('id').replace(prefix,''));
		}
	});
	return ret;
}
function InitSearchBox(viewer)
{
	//$('#control_search').css( 'z-index','9');
	$('#button_search_clear').on( 'click', function(){
		var v = $('#input_search').val();
		//console.log(v);
		if(v.length>0)
		{
			$('#input_search').val('');
			$('#text_search_waiting').css('display','block');
			$('#text_search_waiting').html('输入关键字拼音首字母');
			$('#input_search').focus();
		}
		else
		{
			$('#input_search').hide('slide',{}, 500, function(){
				$('#button_search_clear').css('display','none');
				$('#text_search_waiting').css('display','none');
				$('#div_search_option').css('display','none');
			});
			$('#button_search').css('background-color', '#FFFFFF');
		}

	});
	$( "input[id^=chb_search_webgis_type_]").iCheck({
		checkboxClass: 'icheckbox_flat-green'
	});
	$( "#chb_search_webgis_type_polyline_line").iCheck('check');
	$( "input[id^=chb_search_webgis_type_]").on("ifChanged", function(e){
	});
	
	//$( "#input_search" ).css("border", "1px 1px 0px 1px solid #00FF00");
	$( "#input_search" ).on('keyup',function(e){
		if($(e.target).val().length > 0)
		{
			$('#text_search_waiting').css('display','none');
		}
	});
	$( "#div_search_option_toggle label" ).on('mouseenter',function(e){
		if($("#div_search_option_toggle label").html() == "更多选项&gt;&gt;")
		{
			$('#div_search_option_panel').show({
				effect: "slide",
				direction: "up",
				duration: 400,
				complete:function(){
					$("#div_search_option_toggle label").html("");
					$('#div_search_option').css("border", "0px 1px 0px 1px solid #00FF00");
					$('#div_search_option_panel').css("border", "0px 1px 1px 1px solid #00FF00");
				}
			});
		}
	});
	$( "#div_search_option_panel" ).on('mouseleave',function(e){
		$('#div_search_option_panel').hide({
			effect: "slide",
			direction: "up",
			duration: 400,
			complete:function(){
				$( "#div_search_option_toggle label").html("更多选项&gt;&gt;");
			}
		});
	});
	
	
	$( "#input_search" ).autocomplete({
		autoFocus:true,
		minLength:1,
		delay: 500,
		_resizeMenu: function() {
			this.menu.element.outerHeight( 500 );
		},		
		source:function(request,  response)
		{
			var tylist = GetCheckedBoxList('chb_search_webgis_type_');
			var py_cond = {'db':$.webgis.db.db_name, 'collection':'features;network', 'action':'pinyin_search', 'py':request.term, 'type':tylist};
			$('#text_search_waiting').css('display','block');
			$('#text_search_waiting').html('正在查询，请稍候...');
			MongoFind( py_cond, 
				function(data){
					//console.log(data);
					$('#text_search_waiting').css('display','none');
					response(BuildSearchItemList(data));
			});
		},
		select: function( event, ui ) {
			//console.log(ui.item);
			if(ui.item.value === 'anti_bird_towers')
			{
				var cond = {'db':$.webgis.db.db_name, 'collection':'features', 'action':'anti_bird_towers'};
				ShowProgressBar(true, 670, 200, '载入中', '正在载入已安装驱鸟器杆塔数据，请稍候...');
				MongoFind( cond, 
					function(data){
						ShowProgressBar(false);
						for(var i in data)
						{
							var _id = data[i]['_id'];
							var geojson = data[i];
							if(!$.webgis.data.geojsons[_id])
							{
								$.webgis.data.geojsons[_id] = geojson;
							}
							if($.webgis.config.map_backend === 'cesium')
							{
								if(!$.webgis.data.czmls[_id])
								{
									$.webgis.data.czmls[_id] = CreateCzmlFromGeojson($.webgis.data.geojsons[_id]);
								}
							}
							if($.webgis.config.map_backend === 'leaflet')
							{
								//console.log(geojson);
								$.webgis.control.leaflet_geojson_layer.addData(geojson);
							}
						}
						var extent = GetExtentByCzml();
						FlyToExtent(viewer, extent['west'], extent['south'], extent['east'], extent['north']);
						if($.webgis.config.map_backend === 'cesium')
						{
							ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
						}
				});
			}
			else if(ui.item.geojson && ui.item.geojson.geometry)
			{
				var center = get_geojson_center(ui.item.geojson);
				if(center.length === 2)
				{
					FlyToPoint(viewer, center[0], center[1], 2000, 1.05, 4000);
				}
				ShowSearchResult(viewer, ui.item.geojson);
			}
			else if(ui.item.geojson && ui.item.geojson.properties && ui.item.geojson.properties.webgis_type && ui.item.geojson.properties.webgis_type === 'polyline_line')
			{
				var name = ui.item.geojson.properties.name;
				if(name)
				{
					LoadTowerByLineName(viewer, $.webgis.db.db_name, name, function(data){
						LoadLineByLineName(viewer, $.webgis.db.db_name, name, function(data1){
							var extent = GetExtentByCzml();
							FlyToExtent(viewer, extent['west'], extent['south'], extent['east'], extent['north']);
							if($.webgis.config.map_backend === 'cesium')
							{
								ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
							}
						});
					});
				}
			}
			else if(ui.item.geojson.type && ui.item.geojson.url && ui.item.geojson.name)
			{
				//console.log(ui.item.type + ',' + ui.item.name + ',' + ui.item.url);
				if(ui.item.geojson.type === 'heatmap_tile')
				{
					$.webgis.data.heatmap_layers[ui.item.geojson.name] = {
						layer: CreateTileHeatMap(viewer, {
									url: ui.item.geojson.url,
									maximumLevel: 11,
									name: ui.item.geojson.name
								}),
						type: 'tile'
					};
				}
			}
		}
	});
	$('#button_search').on( 'click', function(){
			if($('#input_search').css('display') == 'none')
			{
				$('#input_search').show('slide',{}, 400, function(){
					$('#button_search_clear').css('display','block');
					$('#text_search_waiting').css('display','block');
					$('#div_search_option').css('display','block');
					$('#input_search').focus();
				});
				$('#button_search').css('background-color', '#00FF00');
				
			}else
			{
				$('#input_search').hide('slide',{}, 500, function(){
					$('#button_search_clear').css('display','none');
					$('#text_search_waiting').css('display','none');
					$('#div_search_option').css('display','none');
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

}


function BuildSearchItemList(data)
{
	var ret = $.map( data, function( item, idx ) {
		var name = '', label = '';
		var pos;
		if(item.properties && item.properties.name) name = item.properties.name;
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
			if(item.geometry.type == 'Polygon')
			{
				var x=0, y=0;
				for(var i in item.geometry.coordinates)
				{
					x += item.geometry.coordinates[i][0];
					y += item.geometry.coordinates[i][1];
				}
				pos = [x / item.geometry.coordinates.length, y / item.geometry.coordinates.length];
			}
		}
		label = name;
		if(item.url && item.name)
		{
			name = item.name;
			pos = undefined;
			label = name.replace('YN_HEATMAP', '热度图');
		}
		if(item.action && item.action === 'anti_bird_towers')
		{
			name = 'anti_bird_towers';
			pos = undefined;
			label = '安装驱鸟器的杆塔';
		}
		return {
		  label: label,
		  value: name,
		  pos:pos,
		  geojson:item
		};
	});
	return ret;
}

function ShowSearchResult(viewer, geojson)
{
	//console.log(geojson);
	if(geojson['_id'])
	{
		if(geojson['properties'] )
		{
			var _id = geojson['_id'];
			if(!$.webgis.data.geojsons[_id])
			{
				$.webgis.data.geojsons[_id] = geojson; //AddTerrainZOffset(geojson);
			}
			if($.webgis.config.map_backend === 'cesium')
			{
				if(!$.webgis.data.czmls[_id])
				{
					if($.webgis.data.geojsons[_id]['properties']['webgis_type'].indexOf('point_')>-1)
						$.webgis.data.czmls[_id] = CreatePointCzmlFromGeojson($.webgis.data.geojsons[_id]);
					else if($.webgis.data.geojsons[_id]['properties']['webgis_type'].indexOf('polyline_')>-1)
						$.webgis.data.czmls[_id] = CreatePolyLineCzmlFromGeojson($.webgis.data.geojsons[_id]);
					else if($.webgis.data.geojsons[_id]['properties']['webgis_type'].indexOf('polygon_')>-1)
						$.webgis.data.czmls[_id] = CreatePolygonCzmlFromGeojson($.webgis.data.geojsons[_id]);
					ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
				}
			}
			if($.webgis.config.map_backend === 'leaflet')
			{
				if(geojson.type === undefined)
				{
					geojson.type = 'Feature';
				}
				//console.log(geojson);
				$.webgis.control.leaflet_geojson_layer.addData(geojson);
			}
		}
	}
}


function CreatePolygonCzmlFromGeojson(geojson)
{
	
	var get_center = function(positions){
		var x=0, y=0, z=0;
		for(var i in positions)
		{
			if(i%3 == 0) x += positions[i];
			if(i%3 == 1) y += positions[i];
			if(i%3 == 2) z += positions[i];
		}
		var len = positions.length/3;
		x = x/len;
		y = y/len;
		z = z/len;
		return [x, y, z];
	};
	var cz = {};
	var name = '';
	cz['id'] = geojson['_id'];
	cz['webgis_type'] = geojson['properties']['webgis_type'];
	cz['position'] = {};
	cz['polygon'] = {};
	cz['polygon']['positions'] = {};
	name = geojson['properties']['name'];
	var positions = GetVertexPositionsByGeojsonPolyline(geojson['geometry'], geojson['properties']['height']);
	cz['polygon']['positions']['cartographicDegrees'] = positions;
	var center = get_center(positions);
	cz['position']['cartographicDegrees'] = center;
	cz['name'] = name;
	cz['polygon']['material'] = {};
	cz['polygon']['material']['solidColor'] = {};
	var style = geojson['properties']['style'];
	var v;

	if(style && style.color) v = style.color;
	else v = GetDefaultStyleValue(cz['webgis_type'], 'color')
	cz['polygon']['material']['solidColor']['color'] = {'rgba':v};
	//if(style.image)
	//{
		//cz['polygon']['material']['image'] = {};
		//cz['polygon']['material']['image']['image'] = {'uri':style.image};
	//}
	cz['polygon']['perPositionHeight'] = {'boolean':false};
	cz['polygon']['height'] = {'number': 0};
	cz['polygon']['extrudedHeight'] = {'number': 0};
	if(cz['webgis_type'] === 'polygon_buffer')
	{
		cz['polygon']['extrudedHeight'] = {'number': 3000};
	}
	else
	{
		if(geojson['properties']['height'])
		{
			cz['polygon']['extrudedHeight'] = {'number': center[2] + geojson['properties']['height'] * 10};
		}
		else
		{
			cz['polygon']['extrudedHeight'] = {'number': center[2] * 2};
		}
	}
	cz['polygon']['fill'] = {'boolean':true};
	cz['polygon']['outline'] = {'boolean':true};
	if(style && style.outline_color) v = style.outline_color;
	else v = GetDefaultStyleValue(cz['webgis_type'], 'outlineColor')
	cz['polygon']['outlineColor'] = {'rgba': v};
	cz['polygon']['show'] = {'boolean':true};
	cz['label'] = {};
	if(style && style.label_fill_color) v = style.label_fill_color;
	else v = GetDefaultStyleValue(cz['webgis_type'], 'labelFillColor')
	cz['label']['fillColor'] = {'rgba': v};
	cz['label']['horizontalOrigin'] = 'LEFT';
	if(style && style.label_outline_color) v = style.label_outline_color;
	else v = GetDefaultStyleValue(cz['webgis_type'], 'labelOutlineColor')
	cz['label']['outlineColor'] = {'rgba': v};
	cz['label']['pixelOffset'] = {'cartesian2':[20.0, 0.0]};
	if(style && style.label_scale) v = style.label_scale;
	else v = GetDefaultStyleValue(cz['webgis_type'], 'labelScale')
	cz['label']['scale'] = {'number': v};
	cz['label']['show'] = {'boolean':false};
	cz['label']['style'] = 'FILL';
	cz['label']['font'] = 'normal normal bold 32px arial';
	cz['label']['text'] = name;
	cz['label']['verticalOrigin'] = 'CENTER';
	cz['description'] = '<!--HTML-->\r\n<p>' + name + '</p>';
	return cz;
}

function CreatePolyLineCzmlFromGeojson(geojson)
{
	var get_line_style = function(geojson){
		var ret = {};
		var color = '#000000';
		if(geojson.properties.voltage == '12')
		{
			color = '#AAF000';
		}
		if(geojson.properties.voltage == '13')
		{
			color = '#FF0000';
		}
		if(geojson.properties.voltage == '15')
		{
			color = '#0000FF';
		}
		var rgba = tinycolor(color).toRgb();
		rgba.a = Math.floor(0.5 * 256);
		ret['color'] = [ rgba.r , rgba.g , rgba.b , rgba.a ];
		ret['outline_color'] = [ 0, 0, 0, 255 ];
		ret['outline_width'] = 1;
		ret['label_fill_color'] = [255, 128, 0, 255];
		ret['label_outline_color'] = [0, 0, 0, 255];
		ret['label_scale'] = 1;
		ret['pixel_width'] = 5;
		return ret;
	};

	var get_center = function(positions){
		var i0 = Math.floor(positions.length/2);
		var i1 = i0+1;
		var i2 = i0+2;
		return [positions[i0], positions[i1], positions[i2]];
	};
	var cz = {};
	var name = geojson['properties']['name'];
	cz['id'] = geojson['_id'];
	cz['webgis_type'] = geojson['properties']['webgis_type'];
	cz['position'] = {};
	cz['polyline'] = {};
	cz['polyline']['positions'] = {};
	
	//console.log(geojson);
	if(cz['webgis_type']==='polyline_line')
	{
		
		var positions = GetVertexPositionsByGeojsonPolyline(geojson['geometry']);
		cz['polyline']['positions']['cartographicDegrees'] = positions;
		cz['position']['cartographicDegrees'] = get_center(positions);
	}
	else
	{
		var positions = GetVertexPositionsByGeojsonPolyline(geojson['geometry'], geojson['properties']['height']);
		cz['polyline']['positions']['cartographicDegrees'] = positions;
		cz['position']['cartographicDegrees'] = get_center(positions);
	}
	cz['name'] = name;
	cz['polyline']['material'] = {};
	cz['polyline']['material']['solidColor'] = {};
	var style;
	if(geojson['properties']['voltage'])
	{
		style = get_line_style(geojson);
	}else
	{
		style = geojson['properties']['style'];
	}
	var v;
	if(style && style.color) v = style.color;
	else v = GetDefaultStyleValue(cz['webgis_type'], 'color')
	cz['polyline']['material']['solidColor']['color'] = {'rgba':v};
	if(style && style.pixel_width) v = style.pixel_width;
	else v = GetDefaultStyleValue(cz['webgis_type'], 'pixelWidth')
	cz['polyline']['width'] = {'number':v};
	cz['polyline']['material']['polylineOutline'] = {};
	if(style && style.outline_color) v = style.outline_color;
	else v = GetDefaultStyleValue(cz['webgis_type'], 'outlineColor')
	cz['polyline']['material']['polylineOutline']['outlineColor'] = {'rgba': v};
	cz['polyline']['material']['polylineOutline']['outlineWidth'] = {'number': 1};
	cz['polyline']['show'] = {'boolean':true};
	cz['label'] = {};
	if(style && style.label_fill_color) v = style.label_fill_color;
	else v = GetDefaultStyleValue(cz['webgis_type'], 'labelFillColor')
	cz['label']['fillColor'] = {'rgba': v};
	cz['label']['horizontalOrigin'] = 'LEFT';
	if(style && style.label_outline_color) v = style.label_outline_color;
	else v = GetDefaultStyleValue(cz['webgis_type'], 'labelOutlineColor')
	cz['label']['outlineColor'] = {'rgba': v};
	cz['label']['pixelOffset'] = {'cartesian2':[20.0, 0.0]};
	if(style && style.label_scale) v = style.label_scale;
	else v = GetDefaultStyleValue(cz['webgis_type'], 'labelScale')
	cz['label']['scale'] = {'number': v};
	cz['label']['show'] = {'boolean':false};
	cz['label']['style'] = 'FILL';
	cz['label']['font'] = 'normal normal bold 32px arial';
	cz['label']['text'] = name;
	cz['label']['verticalOrigin'] = 'CENTER';
	cz['description'] = '<!--HTML-->\r\n<p>' + name + '</p>';
	return cz;
}

function CreatePointCzmlFromGeojson(geojson)
{
	var cz = {};
	cz['id'] = geojson['_id'];
	cz['webgis_type'] = geojson['properties']['webgis_type'];
	cz['billboard'] = {};
	cz['billboard']['color'] = {'rgba':[255, 255, 255, 255]};
	cz['billboard']['horizontalOrigin'] = 'CENTER';
	cz['billboard']['verticalOrigin'] = 'BOTTOM';
	cz['billboard']['scale'] = {'number':1.0};
	cz['billboard']['show'] = {'boolean':false};
	if(geojson['properties']['model'] === undefined)
	{
		cz['billboard']['show'] = {'boolean':true};
	}
	var name = geojson['properties']['name'];
	var subtype = cz['webgis_type'];
	if(geojson['properties']['function_type'] === 'PAE')
	{
		subtype = 'point_dn_switch'
	}
	if(geojson['properties']['function_type'] === 'PAB')
	{
		subtype = 'point_dn_transform'
	}
	if(geojson['properties']['function_type'] === 'PLM')
	{
		subtype = 'point_dn_link'
	}
	if(geojson['properties']['function_type'] === 'T')
	{
		subtype = 'point_dn_transformarea'
	}
	//console.log(subtype);
	var style = $.webgis.mapping.style_mapping[subtype];
	var v;
	var icon_img = 'img/marker30x48.png';
	if(subtype === 'point_tower')
	{
		icon_img = style['icon_img'];
	}
	else
	{
		cz['billboard']['show'] = {'boolean':true};
		style = geojson['properties']['style'];
		if(style && style.icon && style.icon.uri) 
		{
			icon_img = style.icon.uri;
		}
		else
		{
			icon_img = GetDefaultStyleValue(subtype, 'icon_img');
		}
	}
	cz['billboard']['image'] = {'uri':icon_img};
	cz['name'] = name;
	cz['position'] = {};
	cz['position']['cartographicDegrees'] = [geojson['geometry']['coordinates'][0], geojson['geometry']['coordinates'][1], geojson['geometry']['coordinates'][2]];
	cz['point'] = {};
	if(style && style.color) v = style.color;
	else v = GetDefaultStyleValue(subtype, 'color')
	cz['point']['color'] = {'rgba':v};
	if(style && style.outline_color) v = style.outline_color;
	else v = GetDefaultStyleValue(subtype, 'outlineColor')
	cz['point']['outlineColor'] = {'rgba': v};
	if(style && style.outline_width) v = style.outline_width;
	else v = GetDefaultStyleValue(subtype, 'outlineWidth')
	cz['point']['outlineWidth'] = {'number': v};
	if(style && style.pixel_size) v = style.pixel_size;
	else v = GetDefaultStyleValue(subtype, 'pixelSize')
	cz['point']['pixelSize'] = {'number': v};
	cz['point']['show'] = {'boolean':true};
	cz['label'] = {};
	if(style && style.label_fill_color) v = style.label_fill_color;
	else v = GetDefaultStyleValue(subtype, 'labelFillColor')
	cz['label']['fillColor'] = {'rgba': v};
	cz['label']['horizontalOrigin'] = 'LEFT';
	cz['label']['verticalOrigin'] = 'BOTTOM';
	cz['label']['outlineColor'] = {'rgba': 1};
	cz['label']['pixelOffset'] = {'cartesian2':[20.0, 0.0]};
	if(style && style.label_scale) v = style.label_scale;
	else v = GetDefaultStyleValue(subtype, 'labelScale')
	cz['label']['scale'] = {'number': v};
	cz['label']['show'] = {'boolean':false};
	cz['label']['style'] = 'FILL';
	cz['label']['font'] = 'normal normal bold 32px arial';
	cz['label']['text'] = name;
	cz['description'] = '<!--HTML-->\r\n<p>' + name + '</p>';
	return cz;
}


function FilterModelList(str)
{
	try{
		$('#tower_info_model_list_selectable').selectable("destroy");
		$('#tower_info_model_list_selectable').empty();
	}catch(e)
	{
	}
	$('#tower_info_model_list_selectable').append('<li class="ui-widget-content1">' + '(无)' + '</li>');
	for(var i in $.webgis.data.models_gltf_files)
	{
		if(str.length > 0)
		{
			if($.webgis.data.models_gltf_files[i].toLowerCase().indexOf(str.toLowerCase())>-1)
			{
				$('#tower_info_model_list_selectable').append('<li class="ui-widget-content1">' + $.webgis.data.models_gltf_files[i] + '</li>');
			}
		}else{
			$('#tower_info_model_list_selectable').append('<li class="ui-widget-content1">' + $.webgis.data.models_gltf_files[i] + '</li>');
		}
	}
	$("#tower_info_model_list_selectable").selectable({
		selected: function( event, ui ) {
			var model_code_height = $(ui.selected).html();
			var url = GetModelUrl(model_code_height, true);
			var iframe = $('#tower_info_model').find('iframe');
			if(url.length>0)
			{
				var obj = {};
				obj['url'] = '/' + url;
				if($.webgis.mapping.models_mapping[model_code_height])
				{
					obj['data'] = $.webgis.mapping.models_mapping[model_code_height];
				}else
				{
					obj['data'] = {};
					obj['data']['contact_points'] = [];
					obj['data']['model_code'] = GetMCByModelCode(model_code_height);
					obj['data']['model_code_height'] = model_code_height;
				}
				if($.webgis.select.selected_obj && $.webgis.select.selected_obj.id)
				{
					obj['tower_id'] = $.webgis.select.selected_obj.id;
				}
				if($.webgis.config.map_backend === 'cesium')
				{
					var json = encodeURIComponent(JSON.stringify(obj));
					iframe.attr('src', 'threejs/editor/index.html?' + json);
				}
				var get_code_height = function(code_height)
				{
					var idx = code_height.lastIndexOf("_");
					var num1 = code_height.substr(idx+1);
					var rest = code_height.slice(0, idx);
					idx = rest.lastIndexOf("_");
					var num2 = rest.substr(idx+1);
					var h = num2 + '.' + num1;
					var mc = rest.slice(0, idx);
					//console.log(h);
					//console.log(mc);
					return [mc, h];
				};
				var arr = get_code_height(model_code_height);
				$('#tower_info_title_model_code').html('杆塔型号：' + arr[0] + ' 呼称高：' + arr[1] + '米');
				if($.webgis.select.selected_geojson )
				{
					if($.webgis.mapping.models_mapping[model_code_height])
					{
						$.webgis.select.selected_geojson['properties']['model'] = $.webgis.mapping.models_mapping[model_code_height];
					}
					else
					{
						$.webgis.select.selected_geojson['properties']['model'] = {contact_points:[],model_code:arr[0], model_code_height:model_code_height};
					}
				}
			}else
			{
				if($.webgis.config.map_backend === 'cesium')
				{
					iframe.attr('src', 'threejs/editor/index.html' );
				}
				if($.webgis.select.selected_geojson)
				{
					delete $.webgis.select.selected_geojson['properties']['model'];
					$.webgis.select.selected_geojson['properties']['model'] = undefined;
				}
			}
			//console.log($.webgis.data.geojsons[$.webgis.select.selected_obj.id]);
		},
		selecting: function( event, ui ) {
			if( $(".ui-selected, .ui-selecting").length > 1){
                  $(ui.selecting).removeClass("ui-selecting");
            }
		}
	});
}

function LoadBorder(viewer, db_name, condition, callback)
{
	var cond = {'db':db_name, 'collection':'poi_border'};
	for(var k in condition)
	{
		cond[k] = condition[k];
	}
	MongoFind( cond, 
		function(data){
			if(data.length>0)
			{
				for(var i in data)
				{
					$.webgis.data.geojsons[data[i]['_id']] = data[i];
					//var dataSource = new Cesium.GeoJsonDataSource();
					//dataSource.load(data[0]);
					//dataSource.dsname = 'geojson';
					//viewer.dataSources.add(dataSource);
				}
				ReloadBorders(viewer, false);
			}
			ShowProgressBar(false);
			if(callback) callback();
	});
}

function RemoveBorders(viewer)
{
	var l = [];
	for(var k in $.webgis.data.borders)
	{
		l.push(k);
	}
	for(var i in l)
	{
		viewer.scene.primitives.remove($.webgis.data.borders[l[i]]);
		delete $.webgis.data.borders[l[i]];
	}
}
function ReloadBorders(viewer, forcereload)
{
	var ellipsoid = viewer.scene.globe.ellipsoid;
	if(forcereload)
	{
		RemoveBorders(viewer);
	}
	var extent = {'west':179, 'east':-179, 'south':89, 'north':-89};
	for(var k in $.webgis.data.geojsons)
	{
		if(!forcereload)
		{
			if($.webgis.data.borders[k])
			{
				continue;
			}
		}
		//console.log('load ' + k);
		var g = $.webgis.data.geojsons[k];
		if(g.properties.type && g.properties.type.indexOf('border')>-1)
		{
			var positions = [];
			//console.log(g.geometry.type);
			var arr;
			if(g.geometry.type === 'MultiPolygon')
				arr = g.geometry.coordinates[0][0];
			if(g.geometry.type === 'Polygon')
				arr = g.geometry.coordinates[0];
			//console.log(arr);
				
			for(var i=0; i < arr.length; i=i+10)
			{
				var x = arr[i][0],
					y = arr[i][1],
					z = 6000;
				if(g.properties.type === 'provinceborder')
				{
					z = 8000;
				}
				if(g.properties.type === 'cityborder')
				{
					z = 6000;
				}
				if(g.properties.type === 'countyborder')
				{
					z = 4000;
				}
				positions.push(ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(x, y, z)) );
				if (x < extent['west']) extent['west'] = x;
				if (x > extent['east']) extent['east'] = x;
				if (y < extent['south']) extent['south'] = y;
				if (y > extent['north']) extent['north'] = y;
				
			}
			//console.log(positions.length);
			if(positions.length > 20)
			{
				var color = Cesium.Color.fromCssColorString('rgba(0, 255, 0, 0.7)');
				if(g.properties.type === 'provinceborder')
				{
					color = Cesium.Color.fromCssColorString('rgba(255, 255, 0, 0.7)');
				}
				if(g.properties.type === 'cityborder')
				{
					color = Cesium.Color.fromCssColorString('rgba(255, 0, 0, 0.7)');
				}
				if(g.properties.type === 'countyborder')
				{
					color = Cesium.Color.fromCssColorString('rgba(0, 0, 255, 0.7)');
				}
				var wallInstance = new Cesium.GeometryInstance({
					id:k,
					geometry : new Cesium.WallGeometry({
						positions : positions,
					}),
					attributes : {
						//color : Cesium.ColorGeometryInstanceAttribute.fromColor(Cesium.Color.fromRandom({alpha : 1.0}))
						//color : Cesium.ColorGeometryInstanceAttribute.fromColor()
						color : Cesium.ColorGeometryInstanceAttribute.fromColor(color)
					}
				});
				
				var primitive = new Cesium.Primitive({
					geometryInstances : wallInstance,
					appearance : new Cesium.PerInstanceColorAppearance({
						flat:true,
						//closed : true,
						translucent : true,
						renderState : {
							depthTest : {
								enabled : true
							}
						}
					})
				});
				viewer.scene.primitives.add(primitive);
				$.webgis.data.borders[k] = primitive;
			}
			
		}
	}
	FlyToExtent(viewer, extent['west'], extent['south'], extent['east'], extent['north']);
}

function LoadSegments(db_name, callback)
{
	var segs_cond = {'db':db_name, 'collection':'segments'};
	MongoFind( segs_cond, 
		function(data){
			$.webgis.data.segments = data;
			ShowProgressBar(false);
			if(callback) callback();
	});
}
function LoadModelsList(db_name, callback)
{
	var cond = {'db':db_name, 'collection':'-', 'action':'models_list', 'data':{}};
	MongoFind( cond, 
		function(data){
			$.webgis.data.models_gltf_files = data;
			ShowProgressBar(false);
			if(callback) callback();
	});
}
function LoadModelsMapping(db_name, callback)
{
	var cond = {'db':db_name, 'collection':'models'};
	MongoFind( cond, 
		function(data){
			for(var i in data)
			{
				var model_code_height = data[i]['model_code_height'];
				if($.webgis.mapping.models_mapping[model_code_height] === undefined)
				{
					var d = data[i];
					delete d['_id'];
					$.webgis.mapping.models_mapping[model_code_height] = d;
				}
			}
			//console.log($.webgis.mapping.models_mapping);
			ShowProgressBar(false);
			if(callback) callback();
	});
}
function GetExtentByCzml()
{
	var ret;
	ret = {'west':179, 'east':-179, 'south':89, 'north':-89};
	//if($.webgis.config.map_backend === 'cesium')
	//{
		//if($.webgis.data.czmls)
		//{
			//ret = {'west':179, 'east':-179, 'south':89, 'north':-89};
			//for(var k in $.webgis.data.czmls)
			//{
				//if($.webgis.data.czmls[k] && $.webgis.data.czmls[k]['polyline'])
				//{
					//var positions = $.webgis.data.czmls[k]['polyline']['positions']['cartographicDegrees'];
					//for(var i in positions)
					//{
						//var p = positions[i];
						//if (i%3==0 && p < ret['west']) ret['west'] = p;
						//if (i%3==0 && p > ret['east']) ret['east'] = p;
						//if (i%3==1 && p < ret['south']) ret['south'] = p;
						//if (i%3==1 && p > ret['north']) ret['north'] = p;
					//}
				//}
				//else if($.webgis.data.czmls[k]['polygon'])
				//{
					//var positions = $.webgis.data.czmls[k]['polygon']['positions']['cartographicDegrees'];
					//for(var i in positions)
					//{
						//var p = positions[i];
						//if (i%3==0 && p < ret['west']) ret['west'] = p;
						//if (i%3==0 && p > ret['east']) ret['east'] = p;
						//if (i%3==1 && p < ret['south']) ret['south'] = p;
						//if (i%3==1 && p > ret['north']) ret['north'] = p;
					//}
				//}
				//else if($.webgis.data.czmls[k]['position'])
				//{
					//var pos = $.webgis.data.czmls[k]['position']['cartographicDegrees'];
					//if (pos[0] < ret['west']) ret['west'] = pos[0];
					//if (pos[0] > ret['east']) ret['east'] = pos[0];
					//if (pos[1] < ret['south']) ret['south'] = pos[1];
					//if (pos[1] > ret['north']) ret['north'] = pos[1];
				//}
			//}
		//}
	//}
	//if($.webgis.config.map_backend === 'leaflet')
	//{
	var gj = {type: "FeatureCollection",features:[]};
	for(var k in $.webgis.data.geojsons)
	{
		if ($.webgis.data.geojsons[k].geometry)
		{
			gj.features.push($.webgis.data.geojsons[k]);
		}
	}
	var arr = geojsonExtent(gj);
	ret['west'] = arr[0];
	ret['south'] = arr[1];
	ret['east'] = arr[2];
	ret['north'] = arr[3];
	//}
	//console.log(ret);
	return ret;
}


function LoadCodeData(db_name, callback)
{
	var cond = {'db':db_name, 'collection':'codes'};
	MongoFind( cond, 
		function(data){
			$.webgis.data.codes = data[0];
			ShowProgressBar(false);
			if (callback) callback();
	});
}


function LoadLineData(db_name, callback)
{
	var line_cond = {'db':db_name, 'collection':'network', 'properties.webgis_type':'polyline_line'};
	MongoFind( line_cond,function(linedatas){
		$.webgis.data.lines = {};
		for(var i in linedatas)
		{
			$.webgis.data.lines[linedatas[i]['_id']] = linedatas[i];
		}
		ShowProgressBar(false);
		if (callback) callback();
	});
}

function LoadSysRole(db_name, callback)
{
	var cond = {'db':db_name, 'collection':'-', action:'getsysrole', 'userid':$.webgis.current_userinfo['_id']};
	MongoFind( cond, 
		function(data){
			ShowProgressBar(false);
			$.webgis.data.sysrole = data;
			//console.log($.webgis.data.sysrole);
			if (callback) callback();
	});
}




function AddTerrainZOffset(geojson)
{
	var add_to_coord= function(coord)
	{
		if(coord instanceof Array && coord.length==3 && $.isNumeric(coord[0]))
		{
			coord[2] = coord[2] + $.webgis.config.terrain_z_offset;
		}
		else if(coord instanceof Array)
		{
			var l = [];
			for(var i in coord)
			{
				l.push(add_to_coord(coord[i]));
			}
			coord = l;
		}
		return coord;
	}
	if(geojson['geometry'] && geojson['geometry']['coordinates'])
	{
		geojson['geometry']['coordinates'] = add_to_coord(geojson['geometry']['coordinates']);
	}
	return geojson;
}

function RemoveTerrainZOffset(geojson)
{
	var remove_to_coord= function(coord)
	{
		if(coord instanceof Array && coord.length==3 && $.isNumeric(coord[0]))
		{
			coord[2] = coord[2] - $.webgis.config.terrain_z_offset;
		}
		else if(coord instanceof Array)
		{
			var l = [];
			for(var i in coord)
			{
				l.push(remove_to_coord(coord[i]));
			}
			coord = l;
		}
		return coord;
	}
	if(geojson['geometry'] && geojson['geometry']['coordinates'])
	{
		geojson['geometry']['coordinates'] = remove_to_coord(geojson['geometry']['coordinates']);
	}
	return geojson;
}

function UpdateGeojsonPos(geojson, lng, lat, height, rotate)
{
	if(geojson['geometry'] && geojson['geometry']['coordinates'])
	{
		var coord = geojson['geometry']['coordinates'];
		if(coord instanceof Array && coord.length==3 && $.isNumeric(coord[0]))
		{
			coord[0] = parseFloat(lng);
			coord[1] = parseFloat(lat);
			coord[2] = parseFloat(height);
			geojson['geometry']['coordinates'] = coord;
		}
	}
	if(geojson['properties'] )
	{
		geojson['properties']['rotate'] = parseFloat(rotate);
	}
	return geojson;
}

function LoadTowerByLineName(viewer, db_name,  name,  callback)
{
	var geo_cond = {'db':db_name, 'collection':'mongo_get_towers_by_line_name', 'properties.name':name};
	//var ext_cond = {'db':db_name, 'collection':'mongo_get_towers_by_line_name','get_extext':true, 'properties.name':name};
	ShowProgressBar(true, 670, 200, '载入中', '正在载入[' + name + ']数据，请稍候...');
	MongoFind( geo_cond, 
		function(data){
			//console.log(data);
			ShowProgressBar(false);
			for(var i in data)
			{
				var _id = data[i]['_id'];
				var geojson = data[i];
				
				if(!$.webgis.data.geojsons[_id])
				{
					$.webgis.data.geojsons[_id] = geojson;
				}
				if($.webgis.config.map_backend === 'cesium')
				{
					if(!$.webgis.data.czmls[_id])
					{
						$.webgis.data.czmls[_id] = CreateCzmlFromGeojson($.webgis.data.geojsons[_id]);
					}
				}
				if($.webgis.config.map_backend === 'leaflet')
				{
					//console.log(geojson);
					$.webgis.control.leaflet_geojson_layer.addData(geojson);
				}
			}
			if(callback) callback(data);
	});
}

function LoadLineByLineName(viewer, db_name, name, callback)
{
	var get_line_id = function(name){
		var ret;
		for(var k in $.webgis.data.lines)
		{
			if($.webgis.data.lines[k]['properties']['name'] === name)
			{
				ret = k;
				break;
			}
		}
		return ret;
	};
	var _id = get_line_id(name);
	
	
	LoadEdgeByLineId(viewer, db_name, _id, callback);
	if(true) return;
	
	var ellipsoid = viewer.scene.globe.ellipsoid;
	if(!_id)
	{
		console.log(name + " does not exist");
		return;
	}
	var cond = {'db':db_name, 'collection':'get_line_geojson', '_id':_id};
	MongoFind(cond, function(data){
		if(data.length>0)
		{
			if(!$.webgis.data.geojsons[_id])
			{
				$.webgis.data.geojsons[_id] = data[0]; //AddTerrainZOffset(data[0]);
			}
			if(!$.webgis.data.czmls[_id])
			{
				$.webgis.data.czmls[_id] = CreateCzmlFromGeojson($.webgis.data.geojsons[_id]);
			}
		}
		if(callback) callback(data);
	});
}

function GetVertexPositionsByGeojsonPolyline(geometry, height)
{
	var ret = [];
	var coordinates = geometry.coordinates;
	if(geometry.type === 'Polygon')
	{
		coordinates = geometry.coordinates[0];
	}
	for(var i in coordinates)
	{
		var coord = coordinates[i];
		ret.push(coord[0]);
		ret.push(coord[1]);
		if(height) 
			ret.push(coord[2] + height);
		else
			ret.push(coord[2]);
	}
	return ret;
}

function GetVertexPositionsByTowerPairs(towers_pair)
{
	var ret = [];
	var st = SortTowersByTowersPair(towers_pair);
	for(var i in st)
	{
		var _id = st[i];
		if($.webgis.data.czmls[_id])
		{
			ret.push($.webgis.data.czmls[_id]['position']['cartographicDegrees'][0]);
			ret.push($.webgis.data.czmls[_id]['position']['cartographicDegrees'][1]);
			ret.push($.webgis.data.czmls[_id]['position']['cartographicDegrees'][2]);
		}
	}
	return ret;
}


function GetIndexOfDataSourcesByName(viewer, name)
{
	var ret = -1;
	for(var i = 0; i < viewer.dataSources.length; i++)
	{
		var ds = viewer.dataSources.get(i);
		//console.log('ds.name=' + ds.name);
		if(ds.name == name)
		{
			viewer.dataSources.remove(ds);
			ret = i;
			break;
		}
	}
	return ret;
}
function GetDataSourcesByName(viewer, name)
{
	var ret;
	for(var i = 0; i < viewer.dataSources.length; i++)
	{
		var ds = viewer.dataSources.get(i);
		if(ds.name == name)
		{
			ret = ds;
			break;
		}
	}
	return ret;
}
function ReloadCzmlDataSource(viewer, z_aware, forcereload)
{
	
	var get_label_show_opt = function(){
		var r = {};
		$('input[id^=chb_show_label_]').each(function(){
			var t = $(this).attr('id').replace('chb_show_label_', '');
			r[t] = false;
			if($(this).is(':checked')) r[t] = true;
		});
		return r;
	};
	
	var get_geometry_show_opt = function(){
		var r = {};
		$('input[id^=chb_show_geometry_]').each(function(){
			var t = $(this).attr('id').replace('chb_show_geometry_', '');
			r[t] = false;
			if($(this).is(':checked')) r[t] = true;
		});
		return r;
	};
	
	var get_icon_show_opt = function(){
		var r = {};
		$('input[id^=chb_show_icon_]').each(function(){
			var t = $(this).attr('id').replace('chb_show_icon_', '');
			r[t] = false;
			if($(this).is(':checked')) r[t] = true;
		});
		return r;
	};
	
	//if($.webgis.config.map_backend === 'leaflet')
	//{
		//for(var id in $.webgis.data.geojsons)
		//{
			//var g = $.webgis.data.geojsons[id];
			//if(g.geometry)
			//{
				//$.webgis.control.leaflet_geojson_layer.addData(g);
			//}
		//}
		//return;
	//}
	
	
	
	var ellipsoid = viewer.scene.globe.ellipsoid;
	var arr = [];
	var pos;
	//console.log('z_aware=' + z_aware);
	arr.push({"id":"document", "version":"1.0"});
	for(var k in $.webgis.data.czmls)
	{
		var obj =  $.extend(true, {}, $.webgis.data.czmls[k]);
		if(!z_aware)
		{
			if(obj['position'])
			{
				obj['position']['cartographicDegrees'] = [
					obj['position']['cartographicDegrees'][0],  
					obj['position']['cartographicDegrees'][1], 
					0
				];
			}
			if(obj['polyline'] && obj['polyline']['positions'])
			{
				for(var i in obj['polyline']['positions']['cartographicDegrees'])
				{
					if(i % 3 == 2)
					{
						obj['polyline']['positions']['cartographicDegrees'][i] = 0;
					}
				}
			}
			if(obj['polygon'] && obj['polygon']['positions'])
			{
				for(var i in obj['polygon']['positions']['cartographicDegrees'])
				{
					if(i % 3 == 2)
					{
						obj['polygon']['positions']['cartographicDegrees'][i] = 0;
					}
				}
			}
			if(obj['polygon'] && obj['polygon']['extrudedHeight'])
			{
				obj['polygon']['extrudedHeight'] = {'number': 0};
			}
		
		}else
		{
			//if(obj['position'] && obj['position']['cartographicDegrees'][2] == 0)
			//{
				//var height = 0;
				//var carto = Cesium.Cartographic.fromDegrees(
					//obj['position']['cartographicDegrees'][0],  
					//obj['position']['cartographicDegrees'][1]
					//);
				//var h = viewer.scene.globe.getHeight(carto);
				//console.log(h);
				//if(h && h>0) height = h;
				//obj['position']['cartographicDegrees'] = [
					//obj['position']['cartographicDegrees'][0],  
					//obj['position']['cartographicDegrees'][1], 
					//height
				//];
				//$.webgis.data.czmls[k]['position']['cartographicDegrees'] = obj['position']['cartographicDegrees'];
			//}
			//if(obj['polyline'] && obj['polyline']['positions'] )
			//{
				//for(var i=2; i<obj['polyline']['positions']['cartographicDegrees'].length; i=i+3)
				//{
					//if(obj['polyline']['positions']['cartographicDegrees'][i] == 0)
					//{
						//var height = 0;
						//var h = viewer.scene.globe.getHeight(Cesium.Cartographic.fromDegrees(
								//obj['polyline']['positions']['cartographicDegrees'][i-2],  
								//obj['polyline']['positions']['cartographicDegrees'][i-1]
							//));
						//if(h && h>0) height = h;
						//obj['polyline']['positions']['cartographicDegrees'][i] = height;
						//$.webgis.data.czmls[k]['polyline']['positions']['cartographicDegrees'][i] = height;
					//}
				//}
			//}
		}
		var opt = get_label_show_opt();
		for(var kk in opt)
		{
			if(kk.indexOf('point_')>-1 && kk != 'point_tower' && obj['webgis_type'] != 'point_tower' && obj['webgis_type'] &&  obj['webgis_type'].indexOf('point_')>-1 )
			{
				if(opt[kk] === true)
					obj['label']['show'] = {'boolean':true};
				if(opt[kk] === false)
					obj['label']['show'] = {'boolean':false};
			}
			
			if(kk===obj['webgis_type'])
			{
				if(opt[kk] === true)
					obj['label']['show'] = {'boolean':true};
				if(opt[kk] === false)
					obj['label']['show'] = {'boolean':false};
			}
		}
		opt = get_icon_show_opt();
		for(var kk in opt)
		{
			if(kk.indexOf('point_')>-1 && obj['billboard'])
			{
				if(obj['webgis_type'] && obj['webgis_type'].indexOf('point_')>-1 && obj['webgis_type'] != 'point_tower')
				{
					if(opt[kk] === true)
						obj['billboard']['show'] = {'boolean':true};
					if(opt[kk] === false)
						obj['billboard']['show'] = {'boolean':false};
				}
				else if(obj['webgis_type'] && obj['webgis_type'] === 'point_tower')
				{
					//if(opt[kk] === true)
					//{
						//obj['billboard']['show'] = {'boolean':true};
					//}
					//if(opt[kk] === false)
					//{
					//console.log($.webgis.data.geojsons[k]);
					if($.webgis.data.geojsons[k] && $.webgis.data.geojsons[k]['properties'] && $.webgis.data.geojsons[k]['properties']['model'])
					{
						obj['billboard']['show'] = {'boolean':false};
					}else
					{
						obj['billboard']['show'] = {'boolean':true};					
					}
					//}
				}
			}
			else if(obj['webgis_type'] && kk===obj['webgis_type'] && obj['billboard'])
			{
				if(opt[kk] === true)
					obj['billboard']['show'] = {'boolean':true};
				if(opt[kk] === false)
					obj['billboard']['show'] = {'boolean':false};
			}
		}
		opt = get_geometry_show_opt();
		for(var kk in opt)
		{
			if(kk.indexOf('polyline_line')>-1 && obj['polyline'])
			{
				if(obj['webgis_type'] && obj['webgis_type'].indexOf('polyline_line')>-1)
				{
					if(opt[kk] === true)
						obj['polyline']['show'] = {'boolean':true};
					if(opt[kk] === false)
						obj['polyline']['show'] = {'boolean':false};
				}
			}
		}
		arr.push(obj);
		if(viewer.selectedEntity)
		{
			if(obj['position'] && obj['id'] === viewer.selectedEntity.id)
			{
				pos = obj['position']['cartographicDegrees'];
				//var h = viewer.scene.globe.getHeight(Cesium.Cartographic.fromDegrees(pos[0],  pos[1]));
				//if(h && h>0) pos[2] = h;
				//console.log(pos);
			}
		}
	}
	if($.webgis.data.czmls === {})
	{
		viewer.selectedEntity = undefined;
		$.webgis.select.selected_obj = undefined;
	}
	var dataSource = GetDataSourcesByName(viewer, 'czml');
	if(!dataSource)
	{
		dataSource = new Cesium.CzmlDataSource('czml');
		viewer.dataSources.add(dataSource);
	}
	dataSource.process(arr);
	if(forcereload)
	{
		console.log('czml forcereload');
		viewer.dataSources.remove(dataSource, true) ;
		dataSource = new Cesium.CzmlDataSource('czml');
		dataSource.load(arr);
		viewer.dataSources.add(dataSource);
	}
	
	
	if(viewer.selectedEntity && pos)
	{
		viewer.selectedEntity.position._value = ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(pos[0], pos[1], pos[2]));
	}
}
function LookAtTarget(viewer, id, zoom_factor)
{
	var scene = viewer.scene;
	//scene.camera.controller.lookAt(scene.camera.position, target, scene.camera.up);
	var ellipsoid = scene.globe.ellipsoid;
	
	if($.webgis.data.geojsons[id])
	{
		var g = $.webgis.data.geojsons[id];
		var x = g['geometry']['coordinates'][0];
		var y = g['geometry']['coordinates'][1];
		var z = g['geometry']['coordinates'][2];
		
		if(zoom_factor)
			FlyToPoint(viewer, x, y, z, zoom_factor, 4000);
		else
			FlyToPoint(viewer, x, y, z, 1.09, 4000);
	}
}
function LookAtTargetExtent(viewer, id, dx, dy)
{
	var scene = viewer.scene;
	var ellipsoid = scene.globe.ellipsoid;
	if($.webgis.data.geojsons[id])
	{
		var tower = $.webgis.data.geojsons[id];
		var x = tower['geometry']['coordinates'][0];
		var y = tower['geometry']['coordinates'][1];
		var west = Cesium.Math.toRadians(x - dx);
		var south = Cesium.Math.toRadians(y - dy);
		var east = Cesium.Math.toRadians(x + dx);
		var north = Cesium.Math.toRadians(y + dy);
		var extent = new Cesium.Extent(west, south, east, north);
		//scene.camera.controller.viewExtent(extent, ellipsoid);
		FlyToExtent(viewer, west, south, east, north);
	}
}
function ViewExtentByPos(viewer, lng, lat,  dx, dy)
{
	var scene = viewer.scene;
	var ellipsoid = scene.globe.ellipsoid;
	var west = Cesium.Math.toRadians(lng - dx);
	var south = Cesium.Math.toRadians(lat - dy);
	var east = Cesium.Math.toRadians(lng + dx);
	var north = Cesium.Math.toRadians(lat + dy);
	var extent = new Cesium.Extent(west, south, east, north);
	//scene.camera.controller.viewExtent(extent, ellipsoid);
	scene.camera.controller.viewExtent(extent, ellipsoid);

			
}


function FlyToPoint(viewer, x, y, z, factor, duration)
{
	if($.webgis.config.map_backend === 'cesium')
	{
		var scene = viewer.scene;
		var ellipsoid = scene.globe.ellipsoid;
		var destination = Cesium.Cartographic.fromDegrees(x,  y,  z * factor);
		//var flight = Cesium.CameraFlightPath.createAnimationCartographic(scene, {
			//destination : destination,
			//duration	:duration
		//});
		//scene.animations.add(flight);
		
		scene.camera.flyTo({
			destination : ellipsoid.cartographicToCartesian(destination),
			duration	:duration/1000.0
		});
	}
	if($.webgis.config.map_backend === 'leaflet')
	{
		var c = L.latLng(y, x);
		viewer.setView(c, 10);
	}
	
}

function FlyToPointCart3(viewer, cartopos, duration)
{
	var scene = viewer.scene;
	var ellipsoid = scene.globe.ellipsoid;
	//var flight = Cesium.CameraFlightPath.createAnimationCartographic(scene, {
		//destination	:	pos,
		//duration	:	duration
		////up			:	scene.camera.up,
		////direction	:	scene.camera.direction
	//});
	//scene.animations.add(flight);
	scene.camera.flyTo({
        destination : ellipsoid.cartographicToCartesian(cartopos),
		duration	:duration/1000.0
    });	
}

function FlyToExtent(viewer, west, south, east, north)
{
	if($.webgis.config.map_backend === 'cesium')
	{
		var scene = viewer.scene;
		var extent = Cesium.Rectangle.fromDegrees(west, south, east, north);
		//console.log(extent);
		//scene.camera.flyToRectangle({
			//destination : extent
		//});
		scene.camera.flyTo({
			destination : extent
		});
	}
	if($.webgis.config.map_backend === 'leaflet')
	{
		var southWest = L.latLng(south, west);
		var	northEast = L.latLng(north, east);		
		var bounds = L.latLngBounds(southWest, northEast);
		viewer.fitBounds(bounds);
	}
}

function GetTowerInfoByTowerId(id)
{
	var ret = null;
	if($.webgis.data.geojsons[id])
	{
		ret = $.webgis.data.geojsons[id];
	}
	return ret;
}


function LoadTowerModelByTower(viewer, tower)
{
	var scene = viewer.scene;
	var ellipsoid = scene.globe.ellipsoid;
	if(tower)
	{
		var id = tower['_id'];
		if(!$.webgis.data.gltf_models[id])
		{
			if(tower['properties']['model'] && tower['properties']['model']['model_code_height'])
			{
				var lng = parseFloat($('#form_tower_info_base').webgisform('get','lng').val()),
					lat = parseFloat($('#form_tower_info_base').webgisform('get','lat').val()),
					height = parseFloat($('#form_tower_info_base').webgisform('get','alt').val()),
					rotate = parseFloat($('#form_tower_info_base').webgisform('get','rotate').val());
				if(!$.webgis.config.zaware)
				{
					height = 0;
				}else
				{
					//var h = viewer.scene.globe.getHeight(Cesium.Cartographic.fromDegrees(lng,  lat));
					//if(h && h>0) 
					//{
						//height = h;
						//$('#form_tower_info_base').webgisform('get','alt').val(height);
					//}
				}
				if($.isNumeric(lng) && $.isNumeric(lat) && $.isNumeric(height) && $.isNumeric(rotate))
				{
					var url = GetModelUrl(tower['properties']['model']['model_code_height']);
					//console.log('cesium=' + url);
					if(CheckUrlExist(url))
					{
						var model = CreateTowerModel(
							viewer, 
							url, 
							lng,  
							lat, 
							height ,  
							rotate,
							10
						);
						if(model)
						{
							$.webgis.data.gltf_models[id] = model;
							console.log("load model for [" + id + "]");
						}
					}else
					{
						console.log("model " + url + " does not exist");
						$.webgis.data.czmls[id]['billboard']['show'] = {'boolean':true};
						ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
					}
				}
			}
		}
		else
		{
			console.log('model for [' + id + '] already loaded');
		}
	}
}



function GetNextTowerModelData(ids)
{
	var ret = [];
	for(var i in ids)
	{
		var id = ids[i];
		if($.webgis.data.geojsons[id])
		{
			var tower = $.webgis.data.geojsons[id];
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
		if($.webgis.data.geojsons[id])
		{
			var tower = $.webgis.data.geojsons[id];
			var url = GetModelUrl(tower['properties']['model']['model_code_height'], true);
			if(url.length>0)
			{
				ret.push(url);
			}
		}
		
	}
	return ret;
}


function GetModelUrl(model_code_height, check)
{
	if(!model_code_height)
	{
		return '';
	}
	if(model_code_height === '(无)')
	{
		return '';
	}
	//var url = "gltf1/" + model_code_height + ".json" ;
	var url = "gltf/" + model_code_height + ".gltf" ;
	if(check === true)
	{
		if(!CheckUrlExist(url)) url = '';
	}
	return url;
}

function CreateTowerModel(viewer, modelurl,  lng,  lat,  height, rotate, scale) 
{
	var scene = viewer.scene;
	var ellipsoid = scene.globe.ellipsoid;
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
	//console.log(mat4.toString());
	var column2Row2Index = Cesium.Matrix4.getElementIndex(2, 2);
	if(true)
	{
		mat4[column2Row2Index] = - mat4[column2Row2Index];
	}
	//console.log(mat4.toString());
	var m = Cesium.Matrix4.multiplyTransformation(modelMatrix, mat4, mat4);
	var primitive = Cesium.Model.fromGltf({
		url : modelurl,
		modelMatrix : m,
		scale:scale,
		asynchronous:false
	});
	
	//var instance = new Cesium.GeometryInstance({
		//geometry : new Cesium.BoxGeometry({
			//dimensions : new Cesium.Cartesian3(1000000.0, 1000000.0, 500000.0)
		//}),
		//modelMatrix : Cesium.Matrix4.multiplyByTranslation(Cesium.Transforms.eastNorthUpToFixedFrame(
			//Cesium.Cartesian3.fromDegrees(0.0, 0.0), new Cesium.Cartesian3(0.0, 0.0, 1000000.0), new Cesium.Matrix4()),
		//id : 'box',
		//attributes : {
			//color : new Cesium.ColorGeometryInstanceAttribute(1, 0, 0, 1)
		//}
	//});	
	
	
	var model = scene.primitives.add(primitive);
	
	//model.readyToRender.addEventListener(function(model) {
		//model.activeAnimations.addAll({
			//speedup : 0.5,
			//loop : Cesium.ModelAnimationLoop.REPEAT
		//});

		////// Zoom to model
		////var worldBoundingSphere = model.computeWorldBoundingSphere();
		////var center = worldBoundingSphere.center;
		////var transform = Cesium.Transforms.eastNorthUpToFixedFrame(center);
		////var camera = scene.camera;
		////camera.transform = transform;
		////camera.controller.constrainedAxis = Cesium.Cartesian3.UNIT_Z;
		////var controller = scene.screenSpaceCameraController;
		////controller.ellipsoid = Cesium.Ellipsoid.UNIT_SPHERE;
		////controller.enableTilt = true;
		////var r = 1.25 * Math.max(worldBoundingSphere.radius, camera.frustum.near);
		////controller.minimumZoomDistance = r * 0.25;
		////camera.controller.lookAt(new Cesium.Cartesian3(r, r, r), Cesium.Cartesian3.ZERO, Cesium.Cartesian3.UNIT_Z);
	//});
	return model;
}


function TowerInfoMixin(viewer) 
{
	var scene = viewer.scene;
	var ellipsoid = scene.globe.ellipsoid;
	//if (!Cesium.defined(viewer)) {
		//throw new Cesium.DeveloperError('viewer is required.');
	//}
	//if (viewer.hasOwnProperty('trackedEntity')) {
		//throw new Cesium.DeveloperError('trackedEntity is already defined by another mixin.');
	//}
	//if (viewer.hasOwnProperty('selectedEntity')) {
		//throw new Cesium.DeveloperError('selectedEntity is already defined by another mixin.');
	//}

	//var infoBox;// = viewer.infoBox;
	//var infoBoxViewModel = Cesium.defined(infoBox) ? infoBox.viewModel : undefined;

	//var selectionIndicator = viewer.selectionIndicator;
	//var selectionIndicatorViewModel = Cesium.defined(selectionIndicator) ? selectionIndicator.viewModel : undefined;
	//var enableInfoOrSelection = Cesium.defined(infoBox) || Cesium.defined(selectionIndicator);
	//enableInfoOrSelection = false;
	var eventHelper = new Cesium.EventHelper();
	//var entityView;

	function trackSelectedEntity() {
		viewer.trackedEntity = viewer.selectedEntity;
		var id = viewer.trackedEntity.id;
		LookAtTarget(viewer, id);
	}

	function clearTrackedEntity() {
		viewer.trackedEntity = undefined;
	}

	function clearSelectedEntity() {
		viewer.selectedEntity = undefined;
	}

	function clearObjects() {
		viewer.trackedEntity = undefined;
		viewer.selectedEntity = undefined;
	}

	//if (Cesium.defined(infoBoxViewModel)) {
		//eventHelper.add(infoBoxViewModel.cameraClicked, trackSelectedEntity);
		//eventHelper.add(infoBoxViewModel.closeClicked, clearSelectedEntity);
	//}

	//var scratchVertexPositions;
	//var scratchBoundingSphere;

	//function onTick(clock) {
		//var time = clock.currentTime;
		//if (Cesium.defined(entityView)) {
			//entityView.update(time);
		//}

		//var selectedEntity = viewer.selectedEntity;
		//if(selectedEntity && selectedEntity.isAvailable)
		//{
			//var showSelection = Cesium.defined(selectedEntity) && enableInfoOrSelection;
			//if (showSelection) {
				//var oldPosition = Cesium.defined(selectionIndicatorViewModel) ? selectionIndicatorViewModel.position : undefined;
				//var position;
				//var enableCamera = false;
	
				//if (selectedEntity.isAvailable(time)) {
					//if (Cesium.defined(selectedEntity.position)) {
						//position = selectedEntity.position.getValue(time, oldPosition);
						//enableCamera = Cesium.defined(position) && (viewer.trackedEntity !== viewer.selectedEntity);
					//} else if (Cesium.defined(selectedEntity.positions)) {
						//scratchVertexPositions = selectedEntity.positions.getValue(time, scratchVertexPositions);
						//scratchBoundingSphere = Cesium.BoundingSphere.fromPoints(scratchVertexPositions, scratchBoundingSphere);
						//position = scratchBoundingSphere.center;
						//// Can't track scratch positions: "enableCamera" is false.
					//}
					//// else "position" is undefined and "enableCamera" is false.
				//}
				//// else "position" is undefined and "enableCamera" is false.
	
				//if (Cesium.defined(selectionIndicatorViewModel)) {
					//selectionIndicatorViewModel.position = position;
				//}
	
				//if (Cesium.defined(infoBoxViewModel)) {
					//infoBoxViewModel.enableCamera = enableCamera;
					//infoBoxViewModel.isCameraTracking = (viewer.trackedEntity === viewer.selectedEntity);
	
					////if (Cesium.defined(selectedEntity.description)) {
						////infoBoxViewModel.descriptionRawHtml = Cesium.defaultValue(selectedEntity.description.getValue(time), '');
					////} else {
						////infoBoxViewModel.descriptionRawHtml = '';
					////}
				//}
			//}
	
			//if (Cesium.defined(selectionIndicatorViewModel)) {
				//selectionIndicatorViewModel.showSelection = showSelection;
				//selectionIndicatorViewModel.update();
			//}
	
			//if (Cesium.defined(infoBoxViewModel)) {
				//infoBoxViewModel.showInfo = showSelection;
			//}
		//}else
		//{
			//selectionIndicatorViewModel.showSelection = false;
			//selectionIndicatorViewModel.update();
		//}
	//}
	//eventHelper.add(viewer.clock.onTick, onTick);

	function pickEntity(e) {
		var picked = viewer.scene.pick(e.position);
		//var ellipsoid = viewer.scene.globe.ellipsoid;
		//var cartesian = viewer.scene.camera.pickEllipsoid(e.position, ellipsoid);
		//if (cartesian) {
			////var cartographic = ellipsoid.cartesianToCartographic(cartesian);
			////var lng = Cesium.Math.toDegrees(cartographic.longitude).toFixed(7),
				////lat = Cesium.Math.toDegrees(cartographic.latitude).toFixed(7);
			////var text = '(' + lng + ',' + lat + ')';
			////label.show = true;
			////label.text = text;
			////label.position = cartesian;
		//}
		
		
		if (Cesium.defined(picked)) {
			var id = Cesium.defaultValue(picked.id, picked.primitive.id);
			if (id instanceof Cesium.Entity) {
				return id;
			}
			
			//if (picked.primitive && picked.primitive instanceof Cesium.Primitive) {
			if (picked.primitive) {
				return picked;
			}
		}
	}

	function trackObject(trackedEntity) {
		if (Cesium.defined(trackedEntity) && Cesium.defined(trackedEntity.position)) {
			viewer.trackedEntity = trackedEntity;
		}
	}

	function pickAndTrackObject(e) {
		var trackedEntity = pickEntity(e);
		
		if (Cesium.defined(trackedEntity)) 
		{
			if (trackedEntity.primitive && trackedEntity.primitive instanceof Cesium.Primitive)
			{
			}
			else
			{
				trackObject(trackedEntity);
				var id = trackedEntity.id;
				LookAtTarget(viewer, id);
			}
		}
	}

	function moveOverObject(e) {
		var picked;
		try{
			picked = viewer.scene.pick(e.endPosition);
		}catch(e){}
		if (Cesium.defined(picked) && Cesium.defined($.webgis.select.selected_obj) && Cesium.defined(picked.id) && picked.id === $.webgis.select.selected_obj) 
		{
			var id = $.webgis.select.selected_obj.id;
			if($.webgis.data.geojsons[id] && $.webgis.data.geojsons[id]['properties']['name'])
			{
				ShowGeoTip(id, e.endPosition, $.webgis.data.geojsons[id]['properties']['name']);
			}else 
			{
				ShowGeoTip(false);
			}
		}else 
		{
			ShowGeoTip(false);
		} 
	}
	
	function pickAndSelectObject(e) {
		//viewer.selectedEntity = pickEntity(e);
		var selectedEntity = pickEntity(e);
		if(selectedEntity && selectedEntity.primitive === undefined)
		{
			viewer.selectedEntity = selectedEntity;
		}
		//console.log(selectedEntity);
		OnSelect(viewer, e, selectedEntity);
	}

	//event after terrain change
	$('.cesium-baseLayerPicker-choices').on('click', function(e){
		var db = $(e.target).parent().parent().attr('data-bind');
		if(db == 'foreach: terrainProviderViewModels')
		{
			if($(e.target).parent().attr('title') == 'no-terrain')
			{
				//console.log('no terrain');
				$.webgis.config.zaware = false;
			}
			else
			{
				$.webgis.config.zaware = true;
				//console.log('yes terrain');			
			}
			ReloadCzmlDataSource(viewer, $.webgis.config.zaware, true);
			ReloadModelPosition(viewer);
		}
	});


	if (Cesium.defined(viewer.homeButton)) {
		eventHelper.add(viewer.homeButton.viewModel.command.beforeExecute, function(commandInfo){
			clearTrackedEntity();
		});
		eventHelper.add(viewer.homeButton.viewModel.command.afterExecute, function(commandInfo){
			var extent = GetExtentByCzml();
			FlyToExtent(viewer, extent['west'], extent['south'], extent['east'], extent['north']);
		});
	}

	//if (Cesium.defined(viewer.geocoder)) {
		//eventHelper.add(viewer.geocoder.viewModel.search.beforeExecute, clearObjects);
	//}

	function ClearTrackedObj(viewer)
	{
		var vm = viewer.homeButton.viewModel;
		var transitioner = vm._transitioner;
		var ellipsoid = viewer.scene.globe.ellipsoid;
		//var ellipsoid = vm._ellipsoid;
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
			scene.camera.flyTo({
                destination : Cesium.Extent.MAX_VALUE,
                duration : flightDuration/1000.0,
                endReferenceFrame : new Cesium.Matrix4( 0, 0, 1, 0,
														1, 0, 0, 0,
														0, 1, 0, 0,
														0, 0, 0, 1)
			});			
        } else if (mode === Cesium.SceneMode.SCENE3D) {
            var defaultCamera = new Cesium.Camera(context);
			
			scene.camera.flyTo({
                destination : defaultCamera.position,
                duration : flightDuration/1000.0,
                up : defaultCamera.up,
                direction : defaultCamera.direction,
                endReferenceFrame : Cesium.Matrix4.IDENTITY
			});			
			
        } else if (mode === Cesium.SceneMode.COLUMBUS_VIEW) {
			scene.camera.flyTo({
                destination : position,
                duration : flightDuration/1000.0,
                up : up,
                direction : direction,
                endReferenceFrame : new Cesium.Matrix4( 0, 0, 1, 0,
														1, 0, 0, 0,
														0, 1, 0, 0,
														0, 0, 0, 1)
			});			
        }
	}

	//function onDynamicCollectionChanged(collection, added, removed) {
		//var length = removed.length;
		//for (var i = 0; i < length; i++) {
			//var removedObject = removed[i];
			//if (viewer.trackedEntity === removedObject) {
				////viewer.homeButton.viewModel.command();
			//}
			//if (viewer.selectedEntity === removedObject) {
				////viewer.selectedEntity = undefined;
			//}
		//}
	//}

	//function dataSourceAdded(dataSourceCollection, dataSource) {
		//var entities = dataSource.entities ;//.getDynamicObjectCollection();
		//entities.collectionChanged.addEventListener(onDynamicCollectionChanged);
	//}

	//function dataSourceRemoved(dataSourceCollection, dataSource) {
		//var entities = dataSource.entities ;//.getDynamicObjectCollection();
		//entities.collectionChanged.removeEventListener(onDynamicCollectionChanged);

		//if (Cesium.defined(viewer.trackedEntity)) {
			////if (entities.getById(viewer.trackedEntity.id) === viewer.trackedEntity) {
				//////viewer.homeButton.viewModel.command();
			////}
		//}

		//if (Cesium.defined(viewer.selectedEntity)) {
			////if (entities.getById(viewer.selectedEntity.id) === viewer.selectedEntity) {
				//////viewer.selectedEntity = undefined;
			////}
		//}
	//}

	//var dataSources = viewer.dataSources;
	//var dataSourceLength = dataSources.length;
	//for (var i = 0; i < dataSourceLength; i++) {
		//dataSourceAdded(dataSources, dataSources.get(i));
	//}

	//eventHelper.add(viewer.dataSources.dataSourceAdded, dataSourceAdded);
	//eventHelper.add(viewer.dataSources.dataSourceRemoved, dataSourceRemoved);

	viewer.screenSpaceEventHandler.setInputAction(pickAndSelectObject, Cesium.ScreenSpaceEventType.LEFT_CLICK);
	viewer.screenSpaceEventHandler.setInputAction(pickAndTrackObject, Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK);
	viewer.screenSpaceEventHandler.setInputAction(moveOverObject, Cesium.ScreenSpaceEventType.MOUSE_MOVE);

	viewer.trackedEntity = undefined;
	viewer.selectedEntity = undefined;

	//Cesium.knockout.track(viewer, ['trackedEntity', 'selectedEntity']);

	//var knockoutSubscriptions = [];

	//knockoutSubscriptions.push(Cesium.subscribeAndEvaluate(viewer, 'trackedEntity', function(value) {
		//var scene = viewer.scene;
		//var sceneMode = scene.frameState.mode;
		//var isTracking = Cesium.defined(value);
		//if (sceneMode === Cesium.SceneMode.COLUMBUS_VIEW || sceneMode === Cesium.SceneMode.SCENE2D) {
			//scene.screenSpaceCameraController.enableTranslate = !isTracking;
		//}

		//if (sceneMode === Cesium.SceneMode.COLUMBUS_VIEW || sceneMode === Cesium.SceneMode.SCENE3D) {
			//scene.screenSpaceCameraController.enableTilt = !isTracking;
		//}

		//if (isTracking &&  Cesium.defined(value.position)) {
			//entityView = new Cesium.EntityView(value, scene, viewer.scene.globe.ellipsoid);
		//} else {
			//entityView = undefined;
		//}
	//}));

	//knockoutSubscriptions.push(Cesium.subscribeAndEvaluate(viewer, 'selectedEntity', function(value) {
		//if (Cesium.defined(value)) {
			//if (Cesium.defined(infoBoxViewModel)) {
				//infoBoxViewModel.titleText = Cesium.defined(value.name) ? value.name : value.id;
			//}

			//if (Cesium.defined(selectionIndicatorViewModel)) {
				//selectionIndicatorViewModel.animateAppear();
			//}
		//} else {
			//if (Cesium.defined(selectionIndicatorViewModel)) {
				//selectionIndicatorViewModel.animateDepart();
			//}
		//}
	//}));

	//viewer.destroy = Cesium.wrapFunction(viewer, viewer.destroy, function() {
		//eventHelper.removeAll();

		//var i;
		//for (i = 0; i < knockoutSubscriptions.length; i++) {
			//knockoutSubscriptions[i].dispose();
		//}

		//viewer.screenSpaceEventHandler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_CLICK);
		//viewer.screenSpaceEventHandler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK);

		//var dataSources = viewer.dataSources;
		//var dataSourceLength = dataSources.length;
		//for (i = 0; i < dataSourceLength; i++) {
			//dataSourceRemoved(dataSources, dataSources.get(i));
		//}
	//});
}



function ReloadLinePosition(viewer)
{
	for(var k in $.webgis.data.lines)
	{
		var color = '#FF0000';
		if($.webgis.data.lines[k].properties.voltage == '13')
		{
			color = '#FF0000';
		}
		if($.webgis.data.lines[k].properties.voltage == '15')
		{
			color = '#0000FF';
		}
		if($.webgis.data.geojsons[k])
		{
			DrawLineModelByLine(viewer, $.webgis.data.lines[k], 4.0, color, null );
			//DrawBufferOfLine(viewer, 'test', $.webgis.data.lines[k], 1000, 3000, '#FF0000', 0.2);
		}
	}
}

function CheckIsTower(id)
{
	var ret = false;
	if($.webgis.data.geojsons[id] && $.webgis.data.geojsons[id]['properties']['webgis_type'] && $.webgis.data.geojsons[id]['properties']['webgis_type'] === 'point_tower')
	{
		ret = true;
	}
	return ret;
}

function ReloadModelPosition(viewer)
{
	var ellipsoid = viewer.scene.globe.ellipsoid;
	for(var k in $.webgis.data.czmls)
	{
		if($.webgis.data.gltf_models[k])
		{
			var t = GetTowerInfoByTowerId(k);
			if(t)
			{
				RemoveSegmentsTower(viewer, t);
				//}
				//var carto = Cesium.Cartographic.fromDegrees($.webgis.data.czmls[k]['position']['cartographicDegrees'][0], $.webgis.data.czmls[k]['position']['cartographicDegrees'][1], $.webgis.data.czmls[k]['position']['cartographicDegrees'][2]);
				//var cart3 = ellipsoid.cartographicToCartesian(carto);
				//var mat4 = Cesium.Matrix4.fromRotationTranslation(Cesium.Matrix3.IDENTITY, cart3);
				//var m = Cesium.Matrix4.multiplyTransformation($.webgis.data.gltf_models[k].modelMatrix, mat4, mat4);
				//$.webgis.data.gltf_models[k].modelMatrix = m;
				
				var lng = t['geometry']['coordinates'][0],
					lat = t['geometry']['coordinates'][1],
					height = t['geometry']['coordinates'][2],
					rotate = t['properties']['rotate'];
				
				if(!$.webgis.config.zaware) height = 0;
				PositionModel(ellipsoid, $.webgis.data.gltf_models[k], lng, lat, height, rotate);
			}
		}
	}
}

function GetNeighborTowers(ids)
{
	var ret = [];
	for(var j in ids)
	{
		var id = ids[j];
		if($.webgis.data.geojsons[id])
		{
			var tower = $.webgis.data.geojsons[id];
			ret.push(tower);
		}
	}
	return ret;
}

function GetSegmentPairsByTowTowerId(id0, id1)
{
	var ret = {};
	ret['contact_points'] = [];
	ret['t0'] = 0.9;
	ret['w'] = 0.001;
	
	for(var i in $.webgis.data.segments)
	{
		var seg = $.webgis.data.segments[i];
		if(seg['start_tower'] == id0 && seg['end_tower'] == id1)
		{
			ret['contact_points'] = seg['contact_points'];
			ret['t0'] = seg['t0'];
			ret['w'] = seg['w'];
			break;
		}
	}
	return ret;
}

function GetPhaseColor(phase)
{
	var ret = '#000000';
	if($.webgis.mapping.phase_color_mapping[phase])
	{
		ret = $.webgis.mapping.phase_color_mapping[phase];
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

function RemoveSegmentsByType(viewer, webgis_type)
{
	var scene = viewer.scene;
	var remove_one = function()
	{
		var ret = false;
		for(var i in $.webgis.geometry.segments)
		{
			var seg = $.webgis.geometry.segments[i];
			if(seg.webgis_type === webgis_type)
			{
				try{
					scene.primitives.remove(seg.primitive);
				}catch(e){}
				$.webgis.geometry.segments.splice(i,1);
				ret = true;
				break;
			}
		}
		return ret;
	};
	
	if(webgis_type===undefined)
	{
		scene.primitives.removeAll();
		$.webgis.geometry.segments.length = 0;
	}else
	{
		var ok = remove_one();
		while(ok)
		{
			ok = remove_one();
		}
	}
}

function RemoveSegmentsFromArray(node0, node1)
{
	var ret;
	var id0, id1;
	if(node0['_id'] && node1['_id'])
	{
		id0 = node0['_id'];
		id1 = node1['_id']
	}
	if(node0['id'] && node1['id'])
	{
		id0 = node0['id'];
		id1 = node1['id']
	}
	if(id0 && id1)
	{
		for(var i in $.webgis.geometry.segments)
		{
			var seg = $.webgis.geometry.segments[i];
			if(
				(seg['start'] == id0 && seg['end'] == id1)
			|| 	(seg['end'] == id0 && seg['start'] == id1)
			){
				ret = seg;
				$.webgis.geometry.segments.splice(i,1);
				break;
			}
		}
	}
	return ret;
}

function CheckSegmentsRing(node0, node1)
{
	var find_prev = function(id, list)
	{
		for(var i in list)
		{
			var seg = list[i];
			if(id == seg['end']) return seg['start'];
		}
		return undefined;
	};
	var ret = false;
	var id0, id1;
	if(node0['_id'] && node1['_id'])
	{
		id0 = node0['_id'];
		id1 = node1['_id']
	}
	if(node0['id'] && node1['id'])
	{
		id0 = node0['id'];
		id1 = node1['id']
	}
	if(id0 && id1)
	{
		var prev = id0;
		while(prev)
		{
			oldprev = prev;
			prev = find_prev(oldprev, $.webgis.geometry.segments);
			if(prev && prev == id1)
			{
				ret = true;
				break;
			}
		}
	}
	return ret;
}

function CheckSegmentsExist(node0, node1, webgis_type, callback)
{
	var ret = false;
	var id0, id1;
	if(node0['_id'] && node1['_id'])
	{
		id0 = node0['_id'];
		id1 = node1['_id']
	}
	if(node0['id'] && node1['id'])
	{
		id0 = node0['id'];
		id1 = node1['id']
	}
	if(callback === undefined)
	{
		if(id0 && id1)
		{
			for(var i in $.webgis.geometry.segments)
			{
				var seg = $.webgis.geometry.segments[i];
				if(webgis_type)
				{
					if(seg['webgis_type'] === webgis_type
						&& ( (seg['start'] == id0 && seg['end'] == id1) || (seg['end'] == id0 && seg['start'] == id1))
					) {
						ret = true;
						break;
					}
				}
				else
				{
					if(
							(seg['start'] == id0 && seg['end'] == id1)
						|| 	(seg['end'] == id0 && seg['start'] == id1)
					) {
						ret = true;
						break;
					}
				}
			}
		}
		return ret;
	}
	else
	{
		var cond = {'db':$.webgis.db.db_name, 'collection':'-', 'action':'check_edge_exist', 'id0':id0, 'id1':id1};
		MongoFind(cond, function(data){
			ret = false;
			if(data.length>0) ret = true;
			callback(ret);
		});
	}
}


function RemoveLineModel(viewer, line_id)
{
	var m;
	var l = [];
	for(var id in $.webgis.geometry.lines)
	{
		if(id.indexOf(line_id) > -1)
		{
			var model = $.webgis.geometry.lines[id];
			l.push({id:id, model:model});
		}
	}
	while(l.length>0)
	{
		var o = l.pop();
		delete $.webgis.geometry.lines[o.id];
		viewer.scene.primitives.remove(o.model);	
	}
}



function RemoveSegmentsBetweenTwoNode(viewer, node0, node1, webgis_type)
{
	var scene = viewer.scene;
	if(CheckSegmentsExist(node0, node1, webgis_type))
	{
		var seg = RemoveSegmentsFromArray(node0, node1);
		if(seg)
		{
			if($.webgis.config.map_backend === 'cesium')
			{
				while(!seg.primitive.isDestroyed())
				{
					var ret = scene.primitives.remove(seg.primitive);
				}
			}
		}
	}
}

function DrawBufferOfLine1(viewer, buf_id, line, width, height, color, alpha)
{
	var ellipsoid = viewer.scene.globe.ellipsoid;
	//console.log(line);
	var array = SortTowersByTowersPair(line['properties']['towers_pair']);
	//g = GetTowerGeojsonByTowerIdArray(st);
	
	var positions = GetPositions2DByCzmlArray(ellipsoid, array);
	DrawBufferCorridorGeometry(viewer, buf_id, positions, width, height, color, alpha);
}

function DrawBufferOfLine(viewer, buf_id, line, width, height, color, alpha, callback)
{
	var ellipsoid = viewer.scene.globe.ellipsoid;
	if($.webgis.data.geojsons[line['_id']])
	{
		//var array = SortTowersByTowersPair(line['properties']['towers_pair']);
		//g = GetTowerGeojsonByTowerIdArray(array);
		
		var cond = {'db':$.webgis.db.db_name, 'collection':'-', 'action':'buffer', 'data':$.webgis.data.geojsons[line['_id']], 'distance':width};
		MongoFind(cond, function(data){
			array = data[0]['coordinates'];
			
			var positions = GetPositionsByGeojsonCoordinatesArray(ellipsoid, array[0]);
			DrawBufferPolygon(viewer, buf_id, positions, width, height, color, alpha);
			if(callback) callback();
		});
	}
}

function SortTowersByTowersPair(pairlist)
{
	var ret = [];
	var find_prev = function(id, list)
	{
		for(var i in list)
		{
			var pair =  list[i];
			if(id == pair[1]) return pair[0];
		}
		return undefined;
	};
	var find_next = function(id, list)
	{
		var r = []
		for(var i in list)
		{
			var pair =  list[i];
			if(id == pair[0])
			{
				r.push(pair[1]);
			}
		}
		return r;
	};
	
	var find_order_list = function(list,  start, index)
	{
		var l = []
		l.push(start);
		var next = find_next(start, list);
		var startold;
		while(next.length>0)
		{
			if(next.length >= index+1)
			{
				startold = start;
				start = next[index];
				l.push(start);
				var idx = list.indexOf([startold, start]);
				if(idx>-1) list.splice(idx, 1);
				next = find_next(start, list);
			}
			else
			{
				break;
			}
		}
		return l;
	};

	var list  = pairlist.slice();
	
	if(pairlist.length>0)
	{
		pair0 = pairlist[0];
		var oldprev = pair0[0];
		var prev = find_prev(oldprev, list);
		while(prev)
		{
			oldprev = prev;
			prev = find_prev(oldprev, list);
		}
		//console.log(oldprev);
		ret = find_order_list(list,  oldprev, 0);
	}
	return ret;
}

function GetTowerGeojsonByTowerIdArray(array)
{
	var ret = {'type':'LineString', 'coordinates':[]};
	for(var i in array)
	{
		var id = array[i];
		if($.webgis.data.geojsons[id])
		{
			ret['coordinates'].push($.webgis.data.geojsons[id]['geometry']['coordinates']);
		}
	}
	return ret;
}
function DrawBufferOfLine2(viewer, buf_id, line, width, height, color, alpha, callback)
{
	var ellipsoid = viewer.scene.globe.ellipsoid;
	var st = SortTowersByTowersPair(line['properties']['towers_pair']);
	g = GetTowerGeojsonByTowerIdArray(st);
	//console.log(g);
		
	var cond = {'db':$.webgis.db.db_name, 'collection':'-', 'action':'buffer', 'data':g, 'distance':width};
	MongoFind(cond, function(data){
		array = data[0]['coordinates'];
		console.log(array[0]);
		var positions = GetPositionsByGeojsonCoordinatesArray(ellipsoid, array[0]);
		DrawBufferPolygon(viewer, buf_id, positions, width, height, color, alpha);
		if(callback) callback();
	});
		
}


function RemoveBuffer(viewer, buf_id)
{
	for(var i in $.webgis.data.buffers)
	{
		if(i === buf_id)
		{
			var primitive = $.webgis.data.buffers[i];
			viewer.scene.primitives.remove(primitive);
			delete $.webgis.data.buffers[i];
		}
	}
}

function DrawBufferCorridorGeometry(viewer, buf_id, positions, width, height, color, alpha)
{
	RemoveBuffer(viewer, buf_id);
	var ellipsoid = viewer.scene.globe.ellipsoid;
	var rgba = tinycolor(color).toRgb();
	rgba.a = 0.5;
	if(alpha) rgba.a = alpha;
	rgba = 'rgba(' + rgba.r + ',' + rgba.g + ',' + rgba.b + ',' + rgba.a + ')';
	
	if(!$.webgis.config.zaware) height = 0;
	
	var corridorGeometry = new Cesium.CorridorGeometry({
			positions : positions,
			width : width*2,
			extrudedHeight : height,
			vertexFormat : Cesium.PerInstanceColorAppearance.VERTEX_FORMAT,
			cornerType: Cesium.CornerType.ROUNDED
			//cornerType: Cesium.CornerType.BEVELED
			//cornerType: Cesium.CornerType.MITERED
	});
	var primitive = new Cesium.Primitive({
		geometryInstances : new Cesium.GeometryInstance({
			id:	buf_id,
			geometry : corridorGeometry,
			attributes : {
				color : Cesium.ColorGeometryInstanceAttribute.fromColor(Cesium.Color.fromCssColorString(rgba))
			}
		}),
		appearance : new Cesium.PerInstanceColorAppearance({
            flat:true,
            closed : true,
            translucent : true,
			//material : Cesium.Material.fromType('Color', {
				//color : Cesium.Color.fromCssColorString(rgba)
			//}),
			renderState : {
				depthTest : {
					enabled : true
				}
			}
		})
	});
	//console.log(corridorGeometry);
	viewer.scene.primitives.add(primitive);
	$.webgis.data.buffers[buf_id] = primitive;
}

function DrawBufferPolygon(viewer, buf_id, positions, width, height, color, alpha)
{
	RemoveBuffer(viewer, buf_id);
	var ellipsoid = viewer.scene.globe.ellipsoid;
	var rgba = tinycolor(color).toRgb();
	rgba.a = 0.5;
	if(alpha) rgba.a = alpha;
	rgba = 'rgba(' + rgba.r + ',' + rgba.g + ',' + rgba.b + ',' + rgba.a + ')';
	
	if(!$.webgis.config.zaware) height = 0;
	
	var geometry = new Cesium.PolygonGeometry.fromPositions({
			positions : positions,
			extrudedHeight : height,
			vertexFormat : Cesium.PerInstanceColorAppearance.VERTEX_FORMAT,
	});
	var primitive = new Cesium.Primitive({
		geometryInstances : new Cesium.GeometryInstance({
			id:	buf_id,
			geometry : geometry,
			attributes : {
				color : Cesium.ColorGeometryInstanceAttribute.fromColor(Cesium.Color.fromCssColorString(rgba))
			}
		}),
		appearance : new Cesium.PerInstanceColorAppearance({
            flat:true,
            closed : true,
            translucent : true,
			//material : Cesium.Material.fromType('Color', {
				//color : Cesium.Color.fromCssColorString(rgba)
			//}),
			renderState : {
				depthTest : {
					enabled : true
				}
			}
		})
	});
	//console.log(corridorGeometry);
	viewer.scene.primitives.add(primitive);
	$.webgis.data.buffers[buf_id] = primitive;
}

function GetPositionsByGeojsonCoordinatesArray(ellipsoid, arr, force2d)
{
	var ret = [];
	for(var i in arr)
	{
		var lng = arr[i][0];
		var lat = arr[i][1];
		var alt = 0;
		if(arr[i].length == 3)
			alt = arr[i][2];
		var pos = [];
		pos.push(lng);
		pos.push(lat);
		if(force2d)
		{
			pos.push(0);
		}else
		{
			if($.webgis.config.zaware)
			{
				pos.push(alt);
			}else
			{
				pos.push(0);
			}
		}
		var carto = Cesium.Cartographic.fromDegrees(pos[0],  pos[1],  pos[2]);
		var p = ellipsoid.cartographicToCartesian(carto);
		ret.push(p);
	}
	return ret;
}

function GetPositionsByCzmlArray(ellipsoid, arr, force2d)
{
	var ret = [];
	for(var i in arr)
	{
		var id = arr[i];
		if($.webgis.data.czmls[id])
		{
			var cz = $.webgis.data.czmls[id];
			var pos = [];
			pos.push(cz['position']['cartographicDegrees'][0]);
			pos.push(cz['position']['cartographicDegrees'][1]);
			if(force2d)
			{
				pos.push(0);
			}else
			{
				if($.webgis.config.zaware)
				{
					pos.push(cz['position']['cartographicDegrees'][2]);
				}else
				{
					pos.push(0);
				}
			}
			var carto = Cesium.Cartographic.fromDegrees(pos[0],  pos[1],  pos[2]);
			var p = ellipsoid.cartographicToCartesian(carto);
			ret.push(p);
		}
	}
	return ret;
}
function GetPositions2DByCzmlArray(ellipsoid, arr)
{
	return GetPositionsByCzmlArray(ellipsoid, arr, true);
}


function ReloadEdges(viewer)
{
	//RemoveSegmentsByType(viewer, 'edge_dn');
	for(var k in $.webgis.data.geojsons)
	{
		if($.webgis.data.geojsons[k] && $.webgis.data.geojsons[k]['properties']['webgis_type'] === 'edge_dn')
		{
			DrawEdgeBetweenTwoNode(viewer, 'edge_dn', $.webgis.data.geojsons[k]['properties']['start'],$.webgis.data.geojsons[k]['properties']['end'], false);
		}
	}
}

function DrawEdgeBetweenTwoNode(viewer, webgis_type, previd, nextid, fresh)
{
	if(!webgis_type)
	{
		return;
	}
	if($.webgis.config.map_backend === 'cesium')
	{
		var scene = viewer.scene;
		var ellipsoid = viewer.scene.globe.ellipsoid;
		var polylines = new Cesium.PolylineCollection({
			modelMatrix:Cesium.Matrix4.IDENTITY,
			depthTest : false
		});
		var positions = [];
		if($.webgis.data.czmls[previd])
		{
			var a = $.webgis.data.czmls[previd]['position']['cartographicDegrees'];
			if(!$.webgis.config.zaware) a[2] = 0;
			var carto = Cesium.Cartographic.fromDegrees(a[0], a[1], a[2]);
			var cart3 = ellipsoid.cartographicToCartesian(carto);
			positions.push(cart3);
		}
		if($.webgis.data.czmls[nextid])
		{
			var a = $.webgis.data.czmls[nextid]['position']['cartographicDegrees'];
			if(!$.webgis.config.zaware) a[2] = 0;
			var carto = Cesium.Cartographic.fromDegrees(a[0], a[1], a[2]);
			var cart3 = ellipsoid.cartographicToCartesian(carto);
			positions.push(cart3);
		}
		var color = Cesium.Color.fromCssColorString("rgba(255,255,0,1)");
		if(!fresh) color = Cesium.Color.fromCssColorString("rgba(200,200,0,1)");
		var polyline = polylines.add({
			positions : positions,
			material : Cesium.Material.fromType('PolylineArrow', {
			//material : Cesium.Material.fromType('Color', {
				color : color
			}),
			width : 10.0,
			id:{ properties:{'start':previd, 'end':nextid, webgis_type:'edge_dn'}}
		});
		scene.primitives.add(polylines);
		$.webgis.geometry.segments.push({'start':previd, 'end':nextid, 'primitive':polylines, webgis_type:webgis_type, properties:{'start':previd, 'end':nextid, webgis_type:webgis_type}});
	}
	if($.webgis.config.map_backend === 'leaflet')
	{
		if($.webgis.data.geojsons[previd] && $.webgis.data.geojsons[nextid])
		{
			var c1 = get_geojson_center($.webgis.data.geojsons[previd]);
			var c2 = get_geojson_center($.webgis.data.geojsons[nextid]);
			if(c1.length>0 && c2.length>0)
			{
				var latlng1 = L.latLng(c1[1], c1[0]);
				var latlng2 = L.latLng(c2[1], c2[0]);
				var o = {start:previd, end:nextid, webgis_type:webgis_type, properties:{start:previd, end:nextid, webgis_type:webgis_type}};
				$.webgis.geometry.segments.push(o);
				return [latlng1, latlng2];
			}
		}
		
	}
}

function DrawSegmentsBetweenTwoTower(viewer, tower0, tower1, prev_len, next_len, exist)
{
	
	var scene = viewer.scene;
	if(tower0 && tower1 && !CheckSegmentsExist(tower0, tower1, 'edge_tower'))
	{
		var ellipsoid = scene.globe.ellipsoid;
		var lng0 = tower0['geometry']['coordinates'][0],
			lat0 = tower0['geometry']['coordinates'][1],
			height0 = tower0['geometry']['coordinates'][2],
			rotate0 = Cesium.Math.toRadians(tower0['properties']['rotate'] - 90),
			lng1 = tower1['geometry']['coordinates'][0],
			lat1 = tower1['geometry']['coordinates'][1],
			height1 = tower1['geometry']['coordinates'][2],
			rotate1 = Cesium.Math.toRadians(tower1['properties']['rotate'] - 90);
		
		if(!$.webgis.config.zaware)
		{
			height0 = 0;
			height1 = 0;
		}else
		{
			//var h0 = viewer.scene.globe.getHeight(Cesium.Cartographic.fromDegrees(lng0,  lat0));
			//if(h0 && h0>0) height0 = h0;
			//var h1 = viewer.scene.globe.getHeight(Cesium.Cartographic.fromDegrees(lng1,  lat1));
			//if(h1 && h1>0) height1 = h1;
		
		}

		var cart3_0 = ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(lng0, lat0, height0));
		var	modelMatrix_0 = Cesium.Transforms.eastNorthUpToFixedFrame(cart3_0);
		var	quat_0 = Cesium.Quaternion.fromAxisAngle(Cesium.Cartesian3.UNIT_Z, rotate0);
		var	rot_mat3_0 = Cesium.Matrix3.fromQuaternion(quat_0);
		
		var cart3_1 = ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(lng1, lat1, height1));
		var	modelMatrix_1 = Cesium.Transforms.eastNorthUpToFixedFrame(cart3_1);
		var	quat_1 = Cesium.Quaternion.fromAxisAngle(Cesium.Cartesian3.UNIT_Z, rotate1);
		var	rot_mat3_1 = Cesium.Matrix3.fromQuaternion(quat_1);
		
		
		var obj = GetSegmentPairsByTowTowerId(tower0['_id'], tower1['_id']);
		var t0 = obj['t0'];
		//console.log(t0);
		var w = obj['w'];
		var arr = obj['contact_points'];
		var segpairs = [];
		//var counter = {};
		for(var i in arr)
		{
			var key = arr[i].start + '-' + arr[i].end;
			//if(!counter[key]) 
				//counter[key] = 1;
			//counter[key] += 1;
			if(!exist[tower0['_id']]) exist[tower0['_id']] = [];
			if(exist[tower0['_id']].indexOf(key)<0)
			{
				exist[tower0['_id']].push(key);
				segpairs.push(arr[i]);
			}
		}
		//console.log(tower0['_id']  + '-' + tower1['_id'] );
		
		var polylines = new Cesium.PolylineCollection({
			modelMatrix:Cesium.Matrix4.IDENTITY,
			depthTest : false
		});
		
		
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
				mat4_0 = Cesium.Matrix4.multiplyByTranslation(mat4_0, tran_vec3_0, mat4_0);
				var m_0 = Cesium.Matrix4.multiplyTransformation(modelMatrix_0, mat4_0, mat4_0);
				
				
				var tran_vec3_1 = new Cesium.Cartesian3(cp1['x'], cp1['z'], cp1['y']);
				var mat4_1 = Cesium.Matrix4.fromRotationTranslation(rot_mat3_1, Cesium.Cartesian3.ZERO);
				mat4_1 = Cesium.Matrix4.multiplyByTranslation(mat4_1, tran_vec3_1, mat4_1);
				var m_1 = Cesium.Matrix4.multiplyTransformation(modelMatrix_1, mat4_1, mat4_1);

				var p0 = Cesium.Matrix4.getTranslation(m_0, m_0),
					p1 = Cesium.Matrix4.getTranslation(m_1, m_1);
				
				var positions = CalcCatenary(ellipsoid, p0, p1, 15, t0, w);
				var polyline = polylines.add({
					positions : positions,
					material : Cesium.Material.fromType('Color', {
						color : color,
						translucent:true
					}),
					width : 1.0
				});
			}
		}
		
		scene.primitives.add(polylines);
		$.webgis.geometry.segments.push({'start':tower0['_id'], 'end':tower1['_id'], 'primitive':polylines, webgis_type:'edge_tower', properties:{'start':tower0['_id'], 'end':tower1['_id'], webgis_type:'edge_tower'}});
	}
	return exist;
}

function CalcCatenary(ellipsoid, p0, p1, segnum, t0, w)
{
	var ret = [];
	if($.webgis.config.use_catenary)
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
			var z = get_z(l, h, carto0.height, i*step, t0, w);
			var carto = new Cesium.Cartographic(carto0.longitude + i * dx,  carto0.latitude + i * dy,  z);
			var p = ellipsoid.cartographicToCartesian(carto);
			ret.push(p);
		}
	}else
	{
		ret = [	p0,p1];
	}
	return ret;
}


function RemoveSegmentsTower(viewer, tower)
{
	var scene = viewer.scene;
	var arr = GetPrevNextTowerIds(tower);

	var prev_towers = GetNeighborTowers(arr[0]);
	var next_towers = GetNeighborTowers(arr[1]);
	//console.log(prev_towers);
	//console.log(next_towers);
	for(var i in prev_towers)
	{
		var t = prev_towers[i];
		RemoveSegmentsBetweenTwoNode(viewer, t, tower, 'edge_tower');
	}
	for(var i in next_towers)
	{
		var t = next_towers[i];
		RemoveSegmentsBetweenTwoNode(viewer, tower, t, 'edge_tower');
	}
}

function GetPrevNextTowerIds(tower)
{
	var prevs = [];
	var nexts = [];
	for(var i in $.webgis.data.lines)
	{
		var towersid = $.webgis.data.lines[i]['properties']['nodes'];
		var j = 0;
		for(j=0; j<towersid.length; j++)
		{
			var tid = towersid[j];
			if(tid === tower['_id'])
			{
				if(j+1<towersid.length)
				{
					var id = towersid[j+1];
					if(nexts.indexOf(id)<0)
					{
						nexts.push(id);
					}
				}
				if(j>0)
				{
					var id = towersid[j-1];
					if(prevs.indexOf(id)<0)
					{
						prevs.push(id);
					}
				}
			}
		}
	}
	return [prevs, nexts];
}



function DrawSegmentsByTower(viewer, tower)
{
	//console.log(viewer);
	var scene = viewer.scene;
	var arr = GetPrevNextTowerIds(tower);
	var prev_towers = GetNeighborTowers(arr[0]);
	var next_towers = GetNeighborTowers(arr[1]);
	var lng = parseFloat($('#form_tower_info_base').webgisform('get','lng').val()),
		lat = parseFloat($('#form_tower_info_base').webgisform('get','lat').val()),
		height = parseFloat($('#form_tower_info_base').webgisform('get','alt').val()),
		rotate = parseFloat($('#form_tower_info_base').webgisform('get','rotate').val());
		
		
	if($.isNumeric(lng) && $.isNumeric(lat) && $.isNumeric(height) && $.isNumeric(rotate))
	{
		var tt = {};
		tt['_id'] = tower['_id'];
		tt['geometry'] = {};
		tt['geometry']['coordinates'] = [lng, lat, height];
		tt['properties'] = {};
		tt['properties']['rotate'] = rotate;
		tt['properties']['model'] = tower['properties']['model'];
		var exist = {};
		for(var i in prev_towers)
		{
			var t = prev_towers[i];
			exist = DrawSegmentsBetweenTwoTower(viewer, t, tt, prev_towers.length, 1, exist);
		}
		for(var i in next_towers)
		{
			var t = next_towers[i];
			exist = DrawSegmentsBetweenTwoTower(viewer, tt, t, 1, next_towers.length, exist);
		}
	}
}


function CheckTowerInfoModified()
{
	if(true)
	{
		return true;
	}
	var idobj = $('#form_tower_info_base').webgisform('get','id');
	if(idobj === undefined)
	{
		return false;
	}
	var id = idobj.val();
	var tower = GetTowerInfoByTowerId(id);
	if(tower)
	{
		var lng = parseFloat($('#form_tower_info_base').webgisform('get','lng').val()),
			lat = parseFloat($('#form_tower_info_base').webgisform('get','lat').val()),
			height = parseFloat($('#form_tower_info_base').webgisform('get','alt').val()),
			rotate = parseFloat($('#form_tower_info_base').webgisform('get','rotate').val());
		var mc = $('#form_tower_info_base').webgisform('get','model_code').val();
		if(lng != tower['geometry']['coordinates'][0].toFixed(6)
		|| lat != tower['geometry']['coordinates'][1].toFixed(6)
		|| height != tower['geometry']['coordinates'][2].toFixed(0)
		|| rotate != tower['properties']['rotate']
		|| mc != tower['properties']['model']['model_code']
		)
		{
			return true;
		}
		
		var ddd = $('#form_tower_info_base').webgisform('getdata');
		for(var k in tower['properties'])
		{
			//if(ddd[k])
			//if($('#form_tower_info_base').webgisform('get', k).length)
			//{
				//var v = $('#form_tower_info_base').webgisform('get', k).val();
				//if(v && tower['properties'][k] && v != tower['properties'][k] )
				//{
					//return true;
				//}
			//}
		}
	}
	return false;
}

function DeleteLine(viewer, id, callback)
{
	var cond = {'db':$.webgis.db.db_name, 'collection':'network', 'action':'remove', '_id':id};
	ShowProgressBar(true, 670, 200, '删除保存中', '正在删除数据，请稍候...');
	MongoFind(cond, function(data1){
		ShowProgressBar(false);
		if(data1.length>0)
		{
			if(data1[0]['ok'] === 0)
			{
				var msg = ''
				if(data1[0]['err'] === 'nodes_exist')
				{
					msg = '该线路工程或网络中还存在杆塔或其他类型的结点，请先将这些结点删除完全后再进行删除操作。';
				}
				ShowMessage(null, 400, 250, '无法删除', msg);
				//$.jGrowl("删除失败:" + data1[0]['err'], { 
					//life: 2000,
					//position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
					//theme: 'bubblestylefail',
					//glue:'before'
				//});
			}
			else
			{
				$.jGrowl("删除成功", { 
					life: 2000,
					position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
					theme: 'bubblestylesuccess',
					glue:'before'
				});
				if(callback) callback();
			}
		}
	});
}

function SaveLine(viewer, id)
{
	var data = {};
	if(id)
	{
		data['_id'] = id;
	}else
	{
		data['_id'] = null;
	}
	var prop = $('#form_line_info').webgisform('getdata');
	data['properties'] = {};
	data['properties']['webgis_type'] = 'polyline_line';
	for(var k in prop)
	{
		data['properties'][k] = prop[k];
	}
	if(data['properties']['nodes'] === undefined)
	{
		data['properties']['nodes'] = [];
	}
	var cond = {'db':$.webgis.db.db_name, 'collection':'network', 'action':'save', 'data':data};
	ShowProgressBar(true, 670, 200, '保存中', '正在保存数据，请稍候...');
	MongoFind(cond, function(data1){
		ShowProgressBar(false);
		if(data1.length>0)
		{
			if(data1[0].result)
			{
				$.jGrowl("保存失败" + data1[0].result, { 
					life: 2000,
					position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
					theme: 'bubblestylefail',
					glue:'before'
				});
				ShowMessage(null, 400, 200, '保存出错','保存出错:' + data1[0].result, callback);
			}
			else
			{
				$.webgis.data.lines[data1[0]['_id']] = data1[0];
				if(!$.webgis.data.geojsons[data1[0]['_id']])
				{
					$.webgis.data.geojsons[data1[0]['_id']] = {};
				}
				$.webgis.data.geojsons[data1[0]['_id']]['properties'] = data1[0]['properties'];
				$.jGrowl("保存成功", { 
					life: 2000,
					position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
					theme: 'bubblestylesuccess',
					glue:'before'
				});
			}
		}
	});
}
function SaveTower(viewer)
{
	if($.webgis.select.selected_geojson)
	{
		var data = $('#form_tower_info_base').webgisform('getdata');
		for(var k in data)
		{
			if(k === 'alt'
			|| k === 'id'
			|| k === 'lng'
			|| k === 'lat'
			|| k === 'model_code'
			){
				if(k === 'alt')
				{
					$.webgis.select.selected_geojson.geometry.coordinates[2] = parseInt(data[k]);
				}
				else if(k === 'lng')
				{
					$.webgis.select.selected_geojson.geometry.coordinates[0] = parseFloat(data[k]);
				}
				else if(k === 'lat')
				{
					$.webgis.select.selected_geojson.geometry.coordinates[1] = parseFloat(data[k]);
				}
				else
				{
					continue;
				}
			}
			if($.webgis.select.selected_geojson['properties'][k] === undefined)
			{}
			else
			{
				$.webgis.select.selected_geojson['properties'][k] = data[k];
			}
		}
		//if($.webgis.select.selected_geojson['properties']['model'])
		//{
			//$.webgis.select.selected_geojson['properties']['denomi_height'] = GetDenomiHeightByModelCode($.webgis.select.selected_geojson['properties']['model']['model_code_height']);
		//}
		var items = $("#listbox_tower_info_metal").ligerListBox().getSelectedItems();
		if(items && items[0])
		{
			var formdata = $('#form_tower_info_metal').webgisform('getdata');
			//console.log(formdata);
			var idx = items[0].idx - 1;
			if($.webgis.select.selected_geojson.properties.metals && $.webgis.select.selected_geojson.properties.metals.length>idx)
			{
				$.webgis.select.selected_geojson.properties.metals[idx] = formdata;
			}
		}
		//console.log($.webgis.select.selected_geojson);
		//if(true) return;
		SavePoi($.webgis.select.selected_geojson, function(data1){
			//console.log(data1);
			if(data1 && data1.length>0)
			{
				if(data1[0].result)
				{
					return;
				}
				$.webgis.control.drawhelper.clearPrimitive();
				$('#dlg_tower_info').dialog( "close" );
				ClearSelectEntity();
				for(var i in data1)
				{
					var geojson = data1[i];
					var id = geojson['_id'];
					$.webgis.data.geojsons[id] = geojson; //AddTerrainZOffset(geojson);
					
					if($.webgis.config.map_backend === 'cesium')
					{
						$.webgis.data.czmls[id] = CreateCzmlFromGeojson($.webgis.data.geojsons[id]);
						if(geojson['properties'] && geojson['properties']['model'])
						{
							LoadTowerModelByTower(viewer, $.webgis.data.geojsons[id]);
							RemoveSegmentsTower(viewer, $.webgis.data.geojsons[id]);
							DrawSegmentsByTower(viewer, $.webgis.data.geojsons[id]);
						}
					}
				}
				if($.webgis.config.map_backend === 'cesium')
				{
					ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
				}
			}
		});
	}
}

function SavePoi(data, callback)
{
	//console.log(data);
	//data = RemoveTerrainZOffset(data);
	if(data.point)
	{
		delete data.point;
	}
	if(data.polyline)
	{
		delete data.polyline;
	}
	if(data.polygon)
	{
		delete data.polygon;
	}
	if(data.id)
	{
		delete data.id;
	}
	if(data.type === undefined)
	{
		data.type = 'Feature';
	}
	var cond = {'db':$.webgis.db.db_name, 'collection':'features', 'action':'save', 'data':data};
	ShowProgressBar(true, 670, 200, '保存中', '正在保存数据，请稍候...');
	MongoFind(cond, function(data1){
		ShowProgressBar(false);
		if(data1.length>0)
		{
			if(data1[0].result)
			{
				//ShowMessage(null, 400, 200, '错误','保存出错:' + data1.result, callback);
				$.jGrowl("保存失败" + data1[0].result, { 
					life: 2000,
					position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
					theme: 'bubblestylefail',
					glue:'before'
				});
			}
			else
			{
				$.jGrowl("保存成功", { 
					life: 2000,
					position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
					theme: 'bubblestylesuccess',
					glue:'before'
				});
			}
		}
		if(callback) callback(data1);
	});
}



function ShowTowerInfo(viewer, id)
{
	var tower = GetTowerInfoByTowerId(id);
	if(tower)
	{
		$.webgis.select.selected_geojson = $.extend(true, {}, tower);
		FilterModelList('');
		ShowTowerInfoDialog(viewer, $.webgis.select.selected_geojson);
		if($.webgis.config.map_backend === 'cesium')
		{
			LoadTowerModelByTower(viewer, $.webgis.select.selected_geojson);
			DrawSegmentsByTower(viewer, $.webgis.select.selected_geojson);
		}
	}
	else
	{
		delete $.webgis.select.selected_geojson;
		$.webgis.select.selected_geojson = undefined;
	}

}

function UpdateFotoramaSlider(div_id, bindcollection, key, buttons)
{
	//var width = parseInt($('#' + div_id).css('width').replace('px', ''));
	//var height = parseInt($('#' + div_id).css('height').replace('px', ''));
	var width = $('#' + div_id).width();
	var height = $('#' + div_id).height();
	
	//console.log('width:' + width + ',height:' + height);
	var container_id = div_id + '_container';
	var toggle_id =  'div_' + div_id + '_toggle_view_upload';	
	var data = {op:'gridfs', db:$.webgis.db.db_name, width:64, height:64, bindcollection:bindcollection, key:key};
	GridFsFind(data, function(data1){
		if($.webgis.control.image_slider_fotorama)
		{
			$.webgis.control.image_slider_fotorama.destroy();
			delete $.webgis.control.image_slider_fotorama;
			$.webgis.control.image_slider_fotorama = undefined;
		}
		$('#' + container_id).empty();
		var img_data = [];
		for (var i in data1)
		{
			var item = { 
				id: data1[i]._id, 
				_id: data1[i]._id, 
				img:'/get?op=gridfs&db=' + $.webgis.db.db_name + '&_id=' + data1[i]._id , 
				full:'/get?op=gridfs&db=' + $.webgis.db.db_name + '&_id=' + data1[i]._id , 
				thumb:'data:' + data1[i].mimetype + ';base64,' + data1[i].data, 
				caption: data1[i].filename,
				filename:data1[i].filename,
				data:data1[i].data,
				mimetype:data1[i].mimetype,
				description:data1[i].description
			};
			img_data.push(item);
		}
		if(data1.length==0)
		{
			var s = '';
			s += '<div style="text-align: center;vertical-align: middle;line-height: 400px;">';
			s += '	无照片';
			s += '</div>';
			$('#' + container_id).html(s);
		}
		
		if(!$.webgis.control.image_slider_fotorama)
		{
			var options = {
				allowfullscreen: true,
				width: width,
				height:height - 100,
				margin:0,
				nav:'thumbs',
				navposition:'bottom',
				thumbwidth:64,
				thumbheight:64,
				thumbmargin:0,
				thumbborderwidth:0,
				fit:'scaledown', //contain, cover, scaledown, none
				thumbfit:'scaledown', //contain, cover, scaledown, none
				transition:'slide', //slide, crossfade, dissolve
				clicktransition:'slide',
				transitionduration:200,
				startindex:0,
				loop:false,
				autoplay:false,//10000,
				stopautoplayontouch:true,
				keyboard:false,
				arrows:true,
				click:false,
				direction:'ltr',
				hash:true,
				data:img_data
			};
			if(data1.length>0)
			{
				var $fotoramaDiv = $('#' + container_id).fotorama(options);
				$.webgis.control.image_slider_fotorama = $fotoramaDiv.data('fotorama');
			}
		}
		if(buttons instanceof Array && buttons.length>0)
		{
			//console.log();
			AddButtonToFotorama(container_id, $.webgis.control.image_slider_fotorama, buttons);
		}
		ShowProgressBar(false);
	});

}

function UpdateJssorSlider(div_id, bindcollection, key)
{
	var width = parseInt($('#' + div_id).css('width').replace('px', ''));
	var height = parseInt($('#' + div_id).css('height').replace('px', ''));
	var container_id = div_id + '_container';
	var toggle_id =  'div_' + div_id + '_toggle_view_upload';	
	var data = {op:'gridfs', db:$.webgis.db.db_name, width:150, height:150, bindcollection:bindcollection, key:key};
	GridFsFind(data, function(data1){
		if($.webgis.control.image_slider_fotorama)
		{
			delete $.webgis.control.image_slider_fotorama;
			$.webgis.control.image_slider_fotorama = undefined;
			$.webgis.data.image_thumbnail_tower_info.length = 0;
		}
		$.webgis.data.image_thumbnail_tower_info = data1;
		$('#' + container_id).empty();
		var s = '';
		if(data1.length>0)
		{
			s += '\
			<div u="loading" style=" position: absolute; top: 0px; left: 0px;">\
				<div style="filter: alpha(opacity=70); opacity:0.7; position: absolute; display: block;\
					background-color: #000; top: 0px; left: 0px;width: ' + width + 'px;height:' + height + 'px;">\
				</div>\
				<div style="position: absolute; display: block; background: url(img/loading.gif) no-repeat center center;\
					top: 0px; left: 0px;width: ' + width + 'px;height:' + (height-80) + 'px;">\
				</div>\
			</div>\
			';
		}
		s += '<div u="slides" style="cursor: default; position: absolute; left: 0px; top: 0px; width: ' + (width-20) + 'px; height: ' + (height-80) + 'px; overflow: hidden;">';
		for (var i in data1)
		{
			s += '\
			<div >\
				<img u="image" style="width: ' + (width-20) + 'px; height: ' + (height-80) + 'px;" id="' + data1[i]._id + '" src="get?op=gridfs&db=' + $.webgis.db.db_name + '&_id=' + data1[i]._id + '" >\
				<img u="thumb" src="data:' + data1[i].mimetype + ';base64,' + data1[i].data + '" >\
			</div>\
			';
		}
		if(data1.length==0)
		{
			s += '<div style="text-align: center;vertical-align: middle;line-height: 300px;">';
			s += '	<img u="image" style="display:none;"  src="">';
			s += '	<img u="thumb" style="display:none;"  src="">';
			s += '	无照片';
			s += '</div>';
		}
		
		s += '</div>\
		<div u="thumbnavigator" class="jssort07" style="position: absolute; width: ' + width + 'px; height: 100px; left: 0px; bottom: 0px; overflow: hidden; ">\
			<div style=" background-color: #000; filter:alpha(opacity=30); opacity:.3; width: 90%; height:100%;"></div>\
			<div u="slides" style="cursor: default;">\
				<div u="prototype" class="p" style="position: absolute; width: 99px; height: 66px; top: 0; left: 0;">\
					<thumbnailtemplate class="i" style="position:absolute;"></thumbnailtemplate>\
					<div class="o">\
					</div>\
				</div>\
			</div>\
			<span u="arrowleft" class="jssora11l" style="width: 37px; height: 37px; top: 123px; left: 8px;">\
			</span>\
			<span u="arrowright" class="jssora11r" style="width: 37px; height: 37px; top: 123px; right: 8px">\
			</span>\
		</div>\
		';
		$('#' + container_id).append(s);
		
		if(!$.webgis.control.image_slider_fotorama)
		{
			var options = {
				$AutoPlay: true,                                    //[Optional] Whether to auto play, to enable slideshow, this option must be set to true, default value is false
				$AutoPlayInterval: 10000,                            //[Optional] Interval (in milliseconds) to go for next slide since the previous stopped if the slider is auto playing, default value is 3000
				$SlideDuration: 500,                                //[Optional] Specifies default duration (swipe) for slide in milliseconds, default value is 500
				$DragOrientation: 3,                                //[Optional] Orientation to drag slide, 0 no drag, 1 horizental, 2 vertical, 3 either, default value is 1 (Note that the $DragOrientation should be the same as $PlayOrientation when $DisplayPieces is greater than 1, or parking position is not 0)

				$ArrowNavigatorOptions: {
					$Class: $JssorArrowNavigator$,              //[Requried] Class to create arrow navigator instance
					$ChanceToShow: 2,                               //[Required] 0 Never, 1 Mouse Over, 2 Always
					$AutoCenter: 2,                                 //[Optional] Auto center arrows in parent container, 0 No, 1 Horizontal, 2 Vertical, 3 Both, default value is 0
					$Steps: 1                                       //[Optional] Steps to go for each navigation request, default value is 1
				},
				$ThumbnailNavigatorOptions: {
					$Class: $JssorThumbnailNavigator$,              //[Required] Class to create thumbnail navigator instance
					$ChanceToShow: 2,                               //[Required] 0 Never, 1 Mouse Over, 2 Always

					$Loop: 2,                                       //[Optional] Enable loop(circular) of carousel or not, 0: stop, 1: loop, 2 rewind, default value is 1
					$SpacingX: 3,                                   //[Optional] Horizontal space between each thumbnail in pixel, default value is 0
					$SpacingY: 3,                                   //[Optional] Vertical space between each thumbnail in pixel, default value is 0
					$DisplayPieces: 6,                              //[Optional] Number of pieces to display, default value is 1
					$ParkingPosition: 204,                         //[Optional] The offset position to park thumbnail,

					$ArrowNavigatorOptions: {
						$Class: $JssorArrowNavigator$,              //[Requried] Class to create arrow navigator instance
						$ChanceToShow: 2,                               //[Required] 0 Never, 1 Mouse Over, 2 Always
						$AutoCenter: 2,                                 //[Optional] Auto center arrows in parent container, 0 No, 1 Horizontal, 2 Vertical, 3 Both, default value is 0
						$Steps: 1                                       //[Optional] Steps to go for each navigation request, default value is 1
					}
				}
			};
			if(data1.length>0)
			{
				$.webgis.control.image_slider_fotorama = new $JssorSlider$(container_id , options);
			}
		}
		ShowProgressBar(false);
		//responsive code begin
		//you can remove responsive code if you don't want the slider scales while window resizes
		function ScaleSlider() {
			//console.log($('#tower_info_photo').css('width'));
			if($.webgis.control.image_slider_fotorama)
			{
				var parentWidth = $.webgis.control.image_slider_fotorama.$Elmt.parentNode.parentNode.parentNode.parentNode.clientWidth;
				//console.log(parentWidth);
				if (parentWidth)
				{
					//$('#tower_info_photo_container').css('width', parentWidth)
					//$.webgis.control.image_slider_fotorama.$SetScaleWidth(Math.min(parentWidth, 550));
					var w = parentWidth - 20;
					$.webgis.control.image_slider_fotorama.$SetScaleWidth(w );
					$('#' + toggle_id).css('width', (w-20) + 'px' );
				}
			}
			//else
				//window.setTimeout(ScaleSlider, 30);
		}

		//ScaleSlider();

		//if (!navigator.userAgent.match(/(iPhone|iPod|iPad|BlackBerry|IEMobile)/)) {
			//$(window).bind('resize', ScaleSlider);
		//}

		
		//if (navigator.userAgent.match(/(iPhone|iPod|iPad)/)) {
		//    $(window).bind("orientationchange", ScaleSlider);
		//}
		//responsive code end

	});

}
function UpdateFileUploader(div_id)
{
	var width = parseInt($('#' + div_id).css('width').replace('px', ''));
	var height = parseInt($('#' + div_id).css('height').replace('px', ''));
	
	var upload_id = 'div_' + div_id + '_uploader'
	var form_id = 'form_' + div_id + '_uploader_form';
	try{
		$('#' + form_id).fileupload('destroy');
	}catch(e){}
	$('#' + upload_id).empty();
	$('#' + upload_id).append(
	'\
		<form id="' + form_id + '"  method="POST"  enctype="multipart/form-data">\
			<div class="row fileupload-buttonbar" >\
				<div class="col-lg-7" >\
					<!-- The fileinput-button span is used to style the file input field as button -->\
					<span class="btn-success fileinput-button" >\
						<!--<i class="glyphicon glyphicon-plus"></i>-->\
						<span >选择文件...</span>\
						<input type="file" name="files[]">  <!--multiple-->\
					</span>\
					<!--<button type="submit" class="btn btn-primary start">-->\
						<!--<!--<i class="glyphicon glyphicon-upload"></i>-->\
						<!--<span>上传</span>-->\
					<!--</button>-->\
					<!--<button type="reset" class="btn btn-warning cancel">-->\
						<!--<!--<i class="glyphicon glyphicon-ban-circle"></i>-->\
						<!--<span>取消</span>-->\
					<!--</button>-->\
					<!--<button type="button" class="btn btn-danger delete">-->\
						<!--<!--<i class="glyphicon glyphicon-trash"></i>-->\
						<!--<span>删除</span>-->\
					<!--</button>-->\
					<!--<input type="checkbox" class="toggle">-->\
					<span class="fileupload-process"></span>\
				</div>\
				<div class="col-lg-5 fileupload-progress fade">\
					<!-- The global progress bar -->\
					<div class="progress progress-striped active" role="progressbar" aria-valuemin="0" aria-valuemax="100" style="display:none;width:90%;height:5px;margin:10px;">\
						<div class="progress-bar progress-bar-success" style="width:0%;"></div>\
					</div>\
					<div class="progress-extended">&nbsp;</div>\
				</div>\
			</div>\
			<table role="presentation" class="table table-striped"><tbody class="files"></tbody></table>\
		</form>	\
	'
	);
}


function DestroyFileUploader(div_id)
{
	$('#form_' + div_id + '_uploader_form').fileupload('destroy');
	$('#div_' + div_id + '_uploader').empty();
	if($.webgis.control.image_slider_fotorama)
	{
		delete $.webgis.control.image_slider_fotorama;
		$.webgis.control.image_slider_fotorama = undefined;
		$('#' + div_id + '_container').empty();
		$.webgis.data.image_thumbnail_tower_info.length = 0;
	}
	delete $.webgis.select.selected_geojson;
	$.webgis.select.selected_geojson = undefined;
}

function BuildAntiBirdImageSlide(data1)
{
	$('#div_anti_bird_info_pics' ).empty();
	var img_data = [];
	if(data1.length == 0)
	{
		var s = '';
		s += '<div style="text-align: center;vertical-align: middle;line-height: 400px;">';
		s += '	无照片';
		s += '</div>';
		$('#div_anti_bird_info_pics').html(s);
		return;
	}
	var idx = 1;
	for (var i in data1)
	{
		var localtime = moment(data1[i].time).local().format('YYYY-MM-DD HH:mm:ss');
		for (var j in data1[i].picture)
		{
			var pic_url = data1[i].picture[j];
			var thumb_url = pic_url + '/thumbnail';
			var item = { 
				id: data1[i]._id + '_' + j, 
				_id: data1[i]._id + '_' + j, 
				img:pic_url , 
				full:pic_url , 
				thumb:thumb_url, 
				//caption: '第' + idx + '张 拍摄日期:' + localtime + ' 环境温度:' + data1[i].envTemp + '℃',
				caption: '拍摄日期:' + localtime + ' 环境温度:' + data1[i].envTemp + '℃',
				filename:data1[i].imei + '_' + j + '_' + localtime + '.jpg',
				data:data1[i],
				mimetype:'image/jpeg',
				description:'日期:' + localtime + ' 环境温度:' + data1[i].envTemp + '℃'
			};
			img_data.push(item);
			idx += 1;
		}
	}
	
	var options = {
		allowfullscreen: true,
		width: 550,
		height:400,
		margin:0,
		nav:'thumbs',//dots, thumbs, false
		navposition:'bottom',
		thumbwidth:64,
		thumbheight:64,
		thumbmargin:0,
		thumbborderwidth:0,
		fit:'scaledown', //contain, cover, scaledown, none
		thumbfit:'scaledown', //contain, cover, scaledown, none
		transition:'slide', //slide, crossfade, dissolve
		clicktransition:'slide',
		transitionduration:200,
		startindex:0,
		loop:false,
		autoplay:false,//10000,
		stopautoplayontouch:true,
		keyboard:false,
		arrows:true,
		click:false,
		direction:'ltr',
		hash:true,
		data:img_data
	};
	$('#div_anti_bird_info_pics' ).append('<div id="div_container_anti_bird_info_pics"></div>');
	var $fotoramaAntiBirdPicsDiv = $('#div_container_anti_bird_info_pics' ).fotorama(options);
	$.webgis.control.image_slider_anti_bird_pics = $fotoramaAntiBirdPicsDiv.data('fotorama');
	AddButtonToFotorama('div_container_anti_bird_info_pics',
		$.webgis.control.image_slider_anti_bird_pics,
		[{
			title:'下载', 
			className:'anti_bird_pic_toolbutton_download',
			click:function(v){
				console.log('download');
				//console.log(v);
			}
		},
		{
			title:'设置鸟类活动标记', 
			className:'anti_bird_pic_toolbutton_set_flag',
			click:function(v){
				ShowConfirm(null, 500, 200,
					'鸟类活动确认',
					'确定将该图片标记为鸟类活动依据吗? 确认的话数据将会提交到服务器上，以便所有人都能看到修改的结果。',
					function(){
						//console.log(v);
						SetAntiBirdPicFlag(v, true);
					},
					function(){
					
					}
				);
			}
		}
	]);
}	

function SetAntiBirdPicFlag(data,  yes_or_no)
{
	//var picid = data.img.substr(data.img.lastIndexOf('/')+1);
	var url = data.img + '/set_bird_flag/' + yes_or_no;
	console.log(url);
}

function AddButtonToFotorama(container_id, control, options)
{
	var stage = $('#' + container_id).find('div[class=fotorama__stage]');
	if(stage.length > 0 && control)
	{
		$.each(options, function(i, opt){
			$(stage[0]).append('<div class="' + opt.className + '" title="' + opt.title + '"></div>');
			$(stage[0]).find('div.' + opt.className ).off();
			$(stage[0]).find('div.' + opt.className ).on('click', function(){
				opt.click(control.activeFrame);
			});
		});
	}
}

function ShowAntiBirdInfoDialog(viewer,  imei, records_num)
{
	var title = imei;
	
	if($.webgis.data.antibird.anti_bird_equip_tower_mapping === undefined)
	{
		$.webgis.data.antibird.anti_bird_equip_tower_mapping = {};
	}
	if($.webgis.data.antibird.anti_bird_equip_tower_mapping[imei])
	{
		title = $.webgis.data.antibird.anti_bird_equip_tower_mapping[imei].name;
	}
	title = '驱鸟器信息:' + title;
	var buttons = [];
	buttons.push({	
		text: "定位到驱鸟器", 
		click: function(){
		
			if($.webgis.data.antibird.anti_bird_equip_tower_mapping[imei])
			{
				var lng = $.webgis.data.antibird.anti_bird_equip_tower_mapping[imei].lng;
				var lat = $.webgis.data.antibird.anti_bird_equip_tower_mapping[imei].lat;
				ShowProgressBar(true, 670, 200, '查询中', '正在查询该驱鸟器所在杆塔数据，请稍候...');
				var tower_id = $.webgis.data.antibird.anti_bird_equip_tower_mapping[imei].tower_id;
				var cond = {'db':$.webgis.db.db_name, 'collection':'features', '_id':tower_id};
				MongoFind(cond, function(data1){
					ShowProgressBar(false);
					//console.log( data1);
					//console.log(typeof data1);
					if(data1 instanceof Array)
					{
						if(data1.length>0)
						{
							$.webgis.data.geojsons[tower_id] = data1[0];
							if($.webgis.config.map_backend === 'cesium')
							{
								$.webgis.data.czmls[tower_id] = CreateCzmlFromGeojson($.webgis.data.geojsons[tower_id]);
								ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
							}
							if($.webgis.config.map_backend === 'leaflet')
							{
							}
							FlyToPoint(viewer, lng, lat, 6000, 1.05, 4000);
						}
					}
					if(data1 instanceof Object)
					{
						if(data1.result)
						{
							$.jGrowl("查询失败:" + data1.result, { 
								life: 2000,
								position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
								theme: 'bubblestylefail',
								glue:'before'
							});
						}
					}
				});
			}else
			{
				ShowProgressBar(true, 670, 200, '查询中', '正在查询驱鸟器GPS数据，请稍候...');
				var url = '/anti_bird_get_latest_records_by_imei';
				$.get(url, {imei:imei}, function( data1 ){
					ShowProgressBar(false);
					//console.log( data1);
					//console.log(typeof data1);
					if(data1 instanceof Array)
					{
						if(data1.length>0)
						{
							var lng = data1[0].location.longitude;
							var lat = data1[0].location.latitude;
							if(lng>0 && lat>0)
							{
								FlyToPoint(viewer, lng, lat, 6000, 1.05, 4000);
							}
						}
					}
					if(data1 instanceof Object)
					{
						if(data1.result)
						{
							$.jGrowl("查询失败:" + data1.result, { 
								life: 2000,
								position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
								theme: 'bubblestylefail',
								glue:'before'
							});
						}
					}	
					
				}, 'json');
			}
		}
	});
	buttons.push({	
		text: "关闭", 
		click: function(){ 
			$( this ).dialog( "close" );
		}
	});
	$('#dlg_anti_bird_info').dialog({
		width: 630,
		height: 730,
		minWidth:200,
		minHeight: 200,
		draggable: true,
		resizable: true, 
		modal: false,
		//position:{at: "right center"},
		position:{at: "center"},
		title:title,
		close: function(event, ui){
			delete $.webgis.control.image_slider_anti_bird_pics;
			$.webgis.control.image_slider_anti_bird_pics = undefined;
			$('#div_anti_bird_info_pics' ).empty();
		},
		show: {
			effect: "slide",
			direction: "right",
			duration: 500
		},
		hide: {
			effect: "slide",
			direction: "right",
			duration: 500
		},		
		buttons:buttons
	});
	
	var flds = [
		{display: "辨识速度范围", id:"slider_distinguish_speed", newline: true, is_range:true, is_show:false, type: "slider", group:'分布参数', labelwidth:120, width:300, defaultvalue:[3, 15],
			slide:function(value)
			{
				$('#form_anti_bird_info_heatmap').webgisform('setdata',{slider_distinguish_speed:value});
			}
		},
		{display: "起始日期", id:"start_date", dateFormat:"yymmdd", newline: true, is_range:true, type: "date", group:'分布参数',  width:300, validate:{required:true}},
		{display: "结束日期", id:"end_date", dateFormat:"yymmdd", newline: true, is_range:true, type: "date", group:'分布参数',  width:300, validate:{required:true}},
		{display: "生成热图", id: "button_create", newline: true,  type: "button", group:'操作', width:350, defaultvalue:'点击生成热度图', click:function(){
			var data = $('#form_anti_bird_info_heatmap').webgisform('getdata');
			console.log(data);
			AntiBirdHeatmap(viewer, {
				speed:data.slider_distinguish_speed, 
				start:moment(data.start_date).local().format('YYYYMMDD'), 
				end:moment(data.end_date).local().format('YYYYMMDD')
			});
		}}
	];
	var form = $('#form_anti_bird_info_heatmap').webgisform(flds,
	{
		prefix:'form_anti_bird_info_heatmap_',
		maxwidth:520
	});
	$('#form_anti_bird_info_heatmap').webgisform('setdata',{slider_distinguish_speed:[3,15], start_date:moment().local().format('YYYYMMDD'), end_date:moment().local().format('YYYYMMDD')});
	$('#tabs_anti_bird_info').tabs({ 
		collapsible: false,
		active: 0,
		beforeActivate: function( event, ui ) {
			var title = ui.newTab.context.innerText;
			if(title === '统计图表')
			{
				BuildAntiBirdStatisticsForm(imei)
			}
		}
	});
	//console.log(imei);
	if(records_num === undefined)
	{
		records_num = 10;
	}
	var url = '/anti_bird_get_latest_records_by_imei?imei=' + imei + '&records_num=' + records_num;
	//console.log(url);
	ShowProgressBar(true, 670, 200, '载入中', '正在载入最新' + records_num + '张图片数据，请稍候...');
	$.get(url, {is_filter_used:true}, function( data1 ){
		if($.webgis.websocket.antibird.latest_records === undefined)
		{
			$.webgis.websocket.antibird.latest_records = {};
		}
		$.webgis.websocket.antibird.latest_records[imei] = data1;
		ShowProgressBar(false);
		BuildAntiBirdImageSlide(data1);
	}, 'json');
	
}

function BuildAntiBirdStatisticsForm(imei)
{
	$('#form_anti_bird_info_chart').empty();
	$('#div_anti_bird_info_chart').empty();
	var flds = [
		{display: "统计类型", id:"type", newline: true,  type: "select", group:'统计参数',  width:350, defaultvalue:'D',
			editor:{data:[{'value':'Y','label':'按年统计'},{'value':'M','label':'按月统计'},{'value':'D','label':'按天统计'}]},
			change:function(value)
			{
			}
		},
		{display: "起始日期", id:"start_date", dateFormat:"yymmdd", newline: true, is_range:true, type: "date", group:'统计参数',  width:300, validate:{required:true}},
		{display: "结束日期", id:"end_date", dateFormat:"yymmdd", newline: true, is_range:true, type: "date", group:'统计参数',  width:300, validate:{required:true}},
		{display: "生成统计图", id: "button_create", newline: true,  type: "button", group:'操作', labelwidth:120, width:300, defaultvalue:'点击生成统计图', click:function(){
			var data = $('#form_anti_bird_info_chart').webgisform('getdata');
			//console.log(data);
			DrawAntiBirdChart({
				imei: imei,
				YMD: data.type,
				beginTime: moment(data.start_date).local().format('YYYYMMDD'),
				endTime: moment(data.end_date).local().format('YYYYMMDD'),
				minSpeed: '1',
				maxSpeed: '15'
			});
		}}
	];
	var form = $('#form_anti_bird_info_chart').webgisform(flds,
	{
		prefix:'form_anti_bird_info_chart_',
		maxwidth:520
	});
	$('#form_anti_bird_info_chart').webgisform('setdata',{type:'D', start_date:moment().local().format('YYYYMMDD'), end_date:moment().local().format('YYYYMMDD')});

}
function DrawAntiBirdChart(option)
{
	$('#div_anti_bird_info_chart').drawChart(option.imei,option.YMD, option.beginTime,option.endTime,option.minSpeed,option.maxSpeed);
}
function AntiBirdHeatmap(viewer, dict)
{
	//console.log(dict);
	if(dict.speed && dict.speed.length === 2 && dict.start && dict.start.length>0 && dict.end && dict.end.length>0)
	{
		var url= '/proxy/api/statistics/heatmap/' + dict.start + '/' + dict.end + '/' + dict.speed[0] + '/' + dict.speed[1]; 
		//console.log(url);
		ShowProgressBar(true, 670, 200, '载入中', '正在查询统计数据，请稍候...');
		$.get(url, {}, function( data1 ){
			//console.log(data1);
			if(data1 instanceof Array)
			{
				//var hid = 'heatmap_' + dict.start + '_' + dict.end + '_' + dict.speed[0] + '_' + dict.speed[1];
				var hid = 'heatmap_anti_bird';
				for(var i in data1)
				{
					data1[i].text = dict.start + '-' + dict.end + ' ' + data1[i].count + '次';
				}
				DrawHeatMapPixel(viewer, hid , data1);
				if($.webgis.config.map_backend === 'cesium')
				{
					DrawHeatMapCircle(viewer, hid, data1, 200);
				}
			}
			ShowProgressBar(false);
		}, 'json');
	}
}

function ShowTowerInfoDialog(viewer, tower)
{
	//var infoBox = viewer.infoBox;
	var title = '';
	title = tower['properties']['name'];
	var buttons = [];
	if($.webgis.config.map_backend === 'cesium')
	{
		buttons.push({
			text: "锁定视角", 
			click: function(e){
				$.webgis.config.is_tower_focus = !$.webgis.config.is_tower_focus;
				var selectedEntity = viewer.selectedEntity;
				if($.webgis.config.is_tower_focus)
				{
					$(e.target).css('background', '#00AA00 url(/css/black-green-theme/images/ui-bg_dots-medium_75_000000_4x4.png) 50% 50% repeat');
					$(e.target).html('解除锁定');
					
					if (Cesium.defined(selectedEntity)) 
					{
						viewer.trackedEntity = selectedEntity;
						var id = selectedEntity.id;
						LookAtTarget(viewer, id);
					}				
				}
				else
				{
					$(e.target).css('background', '#000000 url(/css/black-green-theme/images/ui-bg_dots-medium_75_000000_4x4.png) 50% 50% repeat');
					$(e.target).html('锁定视角');
					
					if(selectedEntity)
					{
						viewer.trackedEntity = undefined;
						//var vm = viewer.homeButton.viewModel;
						//vm.command();
						//var pos = viewer.scene.globe.ellipsoid.cartesianToCartographic(selectedEntity.position._value);
						//if(pos.height === 0.0) pos.height = 2000;
						//FlyToPoint(viewer, Cesium.Math.toDegrees(pos.longitude) , Cesium.Math.toDegrees(pos.latitude), pos.height, 2.8, 1);
					}
				}
			}
		});
	}
	buttons.push({
		text: "保存", 
		click: function(){ 
			if($('#form_tower_info_base').valid())
			{
				if(!CheckPermission('tower_save'))
				{
					return;
				}
				if(CheckTowerInfoModified())
				{
					ShowConfirm(null, 500, 200,
						'保存确认',
						'检测到数据被修改，确认保存吗? 确认的话数据将会提交到服务器上，以便所有人都能看到修改的结果。',
						function(){
							SaveTower(viewer);
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
	});
	
	buttons.push({	
		text: "关闭", 
		click: function(){ 
			$( this ).dialog( "close" );
		}
	});
	
	
	$('#dlg_tower_info').dialog({
		width: 630,
		height: 730,
		minWidth:200,
		minHeight: 200,
		draggable: true,
		resizable: true, 
		modal: false,
		position:{at: "right center"},
		title:title,
		close: function(event, ui){
			$('#form_tower_info_metal').empty();
			DestroyFileUploader('tower_info_photo');
		},
		show: {
			effect: "slide",
			direction: "right",
			duration: 500
		},
		//hide: {
			////effect: "blind",
			//effect: "slide",
			//direction: "right",
			//duration: 500
		//},		
		buttons:buttons
	});
	$('#tabs_tower_info').tabs({ 
		collapsible: false,
		active: 0,
		beforeActivate: function( event, ui ) {
			$('#form_tower_info_metal').empty();
			var title = ui.newTab.context.innerText;
			if(title == '杆塔模型')
			{
				$('#tower_info_model_list_filter').focus();
				var iframe = $(ui.newPanel.context).find('#tower_info_model').find('iframe');
				var url = '';
				if(tower['properties']['model'])
				{
					url = GetModelUrl(tower['properties']['model']['model_code_height'], true);
				}
				//console.log('threejs=' + url);
				$('#tower_info_model_list_toggle').find('a').html('>>显示列表');
				$('#tower_info_model_list').css('display', 'none');
				$('#tower_info_model').find('iframe').css('width', '99%');
				var obj = {};
				if(url.length==0)
				{
					obj['data'] = tower['properties']['model'];
					obj['tower_id'] = tower['_id'];
					obj['denomi_height'] = tower['properties']['denomi_height'];
					$('#tower_info_title_model_code').html('杆塔型号：' + '无' + ' 呼称高：' + '无');
				}
				else if(url.length>0)
				{
					obj['url'] = '/' + url;
					obj['data'] = tower['properties']['model'];
					obj['tower_id'] = tower['_id'];
					obj['denomi_height'] = tower['properties']['denomi_height'];
					$('#tower_info_title_model_code').html('杆塔型号：' + tower['properties']['model']['model_code'] + ' 呼称高：' + GetDenomiHeightByModelCode(tower['properties']['model']['model_code_height']) + '米');
				}
				if($.webgis.config.map_backend === 'cesium')
				{
					var json = encodeURIComponent(JSON.stringify(obj));
					iframe.attr('src', 'threejs/editor/index.html?' + json);
				}
				if($.webgis.config.map_backend === 'leaflet')
				{
					iframe.css('display', 'none');
					$('#tower_info_model_blank').html('<p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p>你的浏览器不支持HTML5的WEBGL标准，因此无法显示3D模型。请使用最新的Chrome浏览器或Chrome内核的浏览器');
					$('#tower_info_model_blank')
					.css('display', 'block')
					.css('width', '100%')
					.css('height', '440px');
				}
			}
			if(title == '架空线段')
			{
				var iframe = $(ui.newPanel.context).find('#tower_info_segment').find('iframe');
				var url = '';
				if(tower['properties']['model'])
				{
					url = GetModelUrl(tower['properties']['model']['model_code_height'], true);
				}
				var arr = GetPrevNextTowerIds(tower);
				var next_ids = arr[1]
				//console.log(next_ids);
				var url_next = GetNextModelUrl(next_ids);
				if(url.length>0 && url_next.length>0)
				{
					iframe.css('display', 'block');
					$('#tower_info_segment_blank').css('display', 'none');
					var obj = {};
					obj['url'] = '/' + url;
					for(var i in url_next)
					{
						url_next[i] = '/' + url_next[i];
					}
					obj['url_next'] = url_next;
					obj['tower_id'] = tower['_id'];
					obj['next_ids'] = next_ids;
					obj['segments'] = GetSegmentsByTowerStartEnd(tower['_id'], next_ids);
					var json = encodeURIComponent(JSON.stringify(obj));
					if($.webgis.config.map_backend === 'cesium')
					{
						iframe.attr('src', 'threejs/editor/index.html?' + json);
					}
					if($.webgis.config.map_backend === 'leaflet')
					{
						iframe.css('display', 'none');
						$('#tower_info_segment_blank').html('<p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p>你的浏览器不支持HTML5的WEBGL标准，因此无法显示3D模型。请使用最新的Chrome浏览器或Chrome内核的浏览器');
						$('#tower_info_segment_blank')
						.css('display', 'block')
						.css('width', '100%')
						.css('height', '400px');
					}
				}
				else
				{
					$('#tower_info_segment_blank').css('display', 'block');
					iframe.css('display', 'none');
				}
			}
			if(title == '照片文档')
			{
				ShowProgressBar(true, 670, 200, '载入中', '正在载入，请稍候...');
				CreateFileBrowser('tower_info_photo', 520, 480, ['jpg','jpeg','png', 'bmp', 'gif', 'doc', 'xls', 'xlsx', 'docx', 'pdf'], 'features', tower['_id']);
			}
		}
	});
	for(var i in $.webgis.form_fields.tower_baseinfo_fields)
	{
		var fld = $.webgis.form_fields.tower_baseinfo_fields[i];
		if(fld.id === 'line_names' && fld.type === 'multiselect')
		{
			$.webgis.form_fields.tower_baseinfo_fields[i].editor.data = CreateLineNamesSelectOption();
			$.webgis.form_fields.tower_baseinfo_fields[i].editor.position = 'top';
		}
	}
	var form = $('#form_tower_info_base').webgisform($.webgis.form_fields.tower_baseinfo_fields,
	{
		prefix:'tower_baseinfo_',
		maxwidth:520
	});
	if(tower)
	{
		var rotate = tower['properties']['rotate'];
		if(rotate===undefined || rotate===null || rotate===0 ) rotate = "0";
		var data = {
			'id':tower['_id'], 
			'lng':tower['geometry']['coordinates'][0].toFixed(6),
			'lat':tower['geometry']['coordinates'][1].toFixed(6),
			'alt':tower['geometry']['coordinates'][2],
			'rotate':rotate,
			'name':title,
			'tower_code':tower['properties']['tower_code'],
			'model_code':tower['properties']['model']?tower['properties']['model']['model_code']:null,
			'denomi_height':tower['properties']['denomi_height'],
			'grnd_resistance':tower['properties']['grnd_resistance'],
			'horizontal_span':tower['properties']['horizontal_span'],
			'vertical_span':tower['properties']['vertical_span'],
			'line_names':GetLineNamesListByTowerId(tower['_id']),
			'project':tower['properties']['project']
		};
		//console.log(data);
		$('#form_tower_info_base').webgisform('setdata', data);
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
	
	
	if(!$.webgis.control.contextmenu_metal)
	{
		$.webgis.control.contextmenu_metal = $.ligerMenu({ top: 100, left: 100, width: 150, items:
			[
			{ text: '增加金具', icon:'add',
				children:[
					{ text:'绝缘子串',click: AddMetal},
					{ text:'防振锤',click: AddMetal},
					{ text:'接地装置',click: AddMetal},
					{ text:'基础',click: AddMetal},
					{ text:'拉线',click: AddMetal},
					{ text:'防鸟刺',click: AddMetal}
				]
			},
			{ text: '增加附件', icon:'add',
				children:[
					{ text:'在线监测装置',click: AddMetal},
					{ text:'雷电计数器',click: AddMetal},
					{ text:'超声波驱鸟装置',click: AddMetal}
				]
			},
			{ text: '删除金具/附件', click: DeleteMetal,icon:'delete' }
			//{ line: true },
			//{ text: '查看', click: onclick11 },
			//{ text: '关闭', click: onclick112 }
			]
		});
	}
	
	$("#listbox_tower_info_metal").bind("contextmenu", function (e)
	{
		$.webgis.control.contextmenu_metal.show({ top: e.pageY, left: e.pageX });
		return false;
	});
	//try{
		//$("#listbox_tower_info_metal").ligerListBox().clearContent();
	//}catch(e){}
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
		width: 530,
		height:150,
		onSelected:function(idx, name, obj){
			if(obj)
			{
				$.webgis.select.selected_metal_item = obj;
				$.webgis.select.selected_imei = undefined;
				var o = obj;
				var flds = [];
				var formdata = {};
				if(o['type'] == '绝缘子串')
				{
					flds = $.webgis.form_fields.insulator_flds;
					var metal = tower['properties']['metals'][o['idx']-1];
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
				}
				if(o['type'] == '防振锤')
				{
					flds = $.webgis.form_fields.damper_flds;
					var metal = tower['properties']['metals'][o['idx']-1];
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
				}
				if(o['type'] == '接地装置')
				{
					flds = $.webgis.form_fields.grd_flds;
					var metal = tower['properties']['metals'][o['idx']-1];
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
				}
				if(o['type'] == '基础')
				{
					flds = $.webgis.form_fields.base_flds_1;
					var metal = tower['properties']['metals'][o['idx']-1];
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
				}
				if(o['type'] == '拉线' || o['type'] == '防鸟刺' || o['type'] == '在线监测装置' )
				{
					flds = $.webgis.form_fields.base_flds_2_3_4;
					var metal = tower['properties']['metals'][o['idx']-1];
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
				}
				if(o['type'] == '雷电计数器' )
				{
					flds = $.webgis.form_fields.base_flds_5;
					var metal = tower['properties']['metals'][o['idx']-1];
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
				}
				if(o['type'] == '超声波驱鸟装置')
				{
					var metal = {};
					if(tower['properties']['metals'] === undefined || tower['properties']['metals'].length == 0)
					{
					}else
					{
						metal = tower['properties']['metals'][o['idx']-1];
					}
					var enable_imei_select = true;
					if(metal && metal.imei && metal.imei.length>0)
					{
						enable_imei_select = false;
						$.webgis.select.selected_imei = metal.imei;
					}
					flds = UpdateBaseFields6(enable_imei_select);
					for(var k in metal)
					{
						formdata[k] = metal[k];
					}
					formdata['type'] = o['type'];
				}
				
				$('#form_tower_info_metal').webgisform(flds, {
					prefix:'tower_metal_',
					maxwidth:500
				});
				$('#form_tower_info_metal').webgisform('setdata', formdata);
			}
		}
	});
	
}

function UpdateBaseFields6(enable_imei_select)
{
	var ret = $.extend(true, [], $.webgis.form_fields.base_flds_6);
	
	var get_flds6_default = function(){
		var obj = {};
		obj.type = '超声波驱鸟装置';
		obj.imei = '';
		for(var i in $.webgis.form_fields.base_flds_6)
		{
			var item = $.webgis.form_fields.base_flds_6[i];
			if(item.id === 'manufacturer' && item.defaultvalue)
			{
				obj.manufacturer = item.defaultvalue;
			}
			if(item.id === 'model' && item.defaultvalue)
			{
				obj.model = item.defaultvalue;
			}
		}
		return obj;
	};
	
	for(var i in $.webgis.form_fields.base_flds_6)
	{
		var fld =  $.webgis.form_fields.base_flds_6[i];
		if(fld.id === 'imei')
		{
			var filter = false;
			if(fld.editor && fld.editor.filter === true) filter = true;
			if(enable_imei_select)
			{
				ret[i].editor.data = $.webgis.data.antibird.anti_bird_equip_list;
				ret[i].change = function(selval){
					var idx = $.webgis.select.selected_metal_item.idx - 1;
					if($.webgis.select.selected_geojson['properties']['metals'] === undefined)
					{
						$.webgis.select.selected_geojson['properties']['metals'] = [];
						$.webgis.select.selected_geojson['properties']['metals'].push(get_flds6_default());
					}
					if($.webgis.select.selected_geojson['properties']['metals'].length>idx)
					{
						$.webgis.select.selected_geojson['properties']['metals'][idx]['imei'] = selval;
					}
				};
			}else
			{
				ret[i].type = 'text';
				ret[i].editor = {readonly:true};
				delete ret[i].validate;
			}
		}
	}
	return ret;
}

function CreateFileBrowserAdditionalButton(div_id, collection, id)
{
	var ret = [
		{
			title:'下载', 
			className:'phototoolbar-download',
			click:function(v){
				if(v && v._id)
				{
					var url = '/get?' + 'op=gridfs' + '&db=' + $.webgis.db.db_name + '&_id=' + v._id +  '&attachmentdownload=true';
					window.open(url, '_blank');
				}
			}
		},
		{
			title:'删除', 
			className:'phototoolbar-delete',
			click:function(v){
				if(v && v._id)
				{
					ShowConfirm(null, 500, 350,
						'删除确认',
						'确认要删除文件[' + v.filename + ']吗?',
						function(){
							var data = {op:'gridfs_delete','db':$.webgis.db.db_name,_id:v._id};
							GridFsFind(data, function(){
								UpdateFotoramaSlider(div_id, collection, id, CreateFileBrowserAdditionalButton(div_id, collection, id));
							});
						},
						function(){
						},
						v
					);
				}
			}
		}
	];
	return ret;
}


function CreateFileBrowser(div_id, width, height, fileext, collection, id)
{
	$('#' + div_id).empty();
	if(id===undefined)
	{
		ShowProgressBar(false);
		$('#' + div_id).html('请先保存，再上传图片');
		return;
	}
	$('#' + div_id).css('width', width + 'px').css('height', height + 'px');
	var html = '';
	//html += '<div  id="' + div_id + '_toolbar">';
	//html += '	<span  class="phototoolbar-download" style="display:inline-block;z-index:9;width: 24px; height: 27px; bottom: 140px; right: 80px;" data-' + div_id + '-download="">';
	//html += '	</span>';
	//html += '	<span  class="phototoolbar-delete" style="display:inline-block;z-index:9;width: 24px; height: 24px; bottom: 144px; right: 50px;" data-' + div_id + '-delete="">';
	//html += '	</span>';
	//html += '</div>';
	html += '<div id="' + div_id + '_container"  style="opacity:1.0;">';
	html += '</div>';
	html += '<div id="div_' + div_id + '_toggle_view_upload" class="btn-primary" style="width:90%;margin:10px;text-align:center;cursor:default;">上传附件</div>';
	html += '<div id="div_' + div_id + '_uploader" style="display:none">';
	html += '</div>';
	html += '<div id="div_' + div_id + '_upload_desciption" style="display:none;margin:10px;">';
	html += '	<textarea id="' + div_id + '_upload_desciption" style="width:' + (width - 40) + 'px;height:100px;color:white;background-color:black;border:1px #00FF00 solid" rows="5" placeholder="在此输入备注..."></textarea>';
	html += '</div>';
	$('#' + div_id).append(html);
	
	$('#' + div_id + '_upload_desciption').resizable({
		minHeight:100,
		minWidth:400
	});

	UpdateFotoramaSlider(div_id, collection, id, CreateFileBrowserAdditionalButton(div_id, collection, id));
	UpdateFileUploader(div_id);
	InitFileUploader(div_id, fileext, collection, id);
}

function GetGeojsonFromPosition(ellipsoid, position, type)
{
	if(position instanceof Cesium.Cartesian3)
	{
		var carto = ellipsoid.cartesianToCartographic(position);
		position = [Cesium.Math.toDegrees(carto.longitude), Cesium.Math.toDegrees(carto.latitude)];
	}
	if(position instanceof L.LatLng)
	{
		position = [position.lng, position.lat];
	}
	if(position instanceof Array)
	{
		for(var i in position)
		{
			position[i] = GetGeojsonFromPosition(ellipsoid, position[i]);
		}
		if(type && type === 'Polygon')
		{
			var position1 = [];
			position.push(position[0]);
			position1.push(position);
			position = position1;
		}
	}
	return position;
}

function BufferCreate(viewer, type, position, distance, style, resolution, callback)
{

	var ellipsoid = viewer.scene.globe.ellipsoid;
	var t = 'Point';
	if(type.indexOf('polyline')>-1)
	{
		t = 'LineString';
	}
	if(type.indexOf('polygon')>-1) 
	{
		t = 'Polygon';
	}
	coordinates = GetGeojsonFromPosition(ellipsoid, position, t);
	//console.log(coordinates);
	var res = 4;
	if(resolution) res = resolution;
	var geojson = {type:'Feature',geometry:{type:t, coordinates: coordinates}};
	var cond = {'db':$.webgis.db.db_name, 'collection':'-', 'action':'buffer', 'data':geojson, 'distance':distance, 'res':res};
	ShowProgressBar(true, 670, 200, '生成缓冲区', '正在生成缓冲区，请稍候...');
	MongoFind(cond, function(data){
		ShowProgressBar(false);
		if(data.length>0)
		{
			var geometry = data[0];
			geojson['geometry'] = geometry;
			geojson['_id'] = 'tmp_buffer';
			if(!geojson['properties'])
			{
				geojson['properties'] = {};
			}
			geojson['properties']['webgis_type'] = 'polygon_buffer';
			if(style) geojson['properties']['style'] = style;
			$.webgis.data.geojsons[geojson['_id']] = geojson;
			$.webgis.data.czmls[geojson['_id']] = CreateCzmlFromGeojson($.webgis.data.geojsons[geojson['_id']]);
			ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
			if(callback) callback(geojson);
		}else
		{
			ShowMessage(null, 400, 250, '出错了', '服务器生成缓冲区错误:返回数据为空,请确认服务正在运行.');
		}
	});
}

function BufferAnalyze(viewer, geojson, webgis_type, callback)
{
	var cond = {'db':$.webgis.db.db_name, 'collection':'features', 'action':'within', 'data':geojson, 'webgis_type':webgis_type, 'limit':0};
	ShowProgressBar(true, 670, 200, '缓冲区分析中', '正在生成缓冲区分析，请稍候...');
	MongoFind(cond, function(data){
		ShowProgressBar(false);
		if(callback) callback(data);
	});
}

function ShowBufferAnalyzeDialog(viewer, type, position)
{
	var ellipsoid;
	if($.webgis.config.map_backend === 'cesium')
	{
		ellipsoid = viewer.scene.globe.ellipsoid;
	}
	var buffer_geojson;
	var switch_panel = function(formname, dialog)
	{
		$('form[id^=form_buffer_]').parent().css('display', 'none');
		$('#' + formname).parent().css('display', 'block');
		
		var buttons = bind_buttons(formname, dialog);
	};
	var get_style = function()
	{
		var data = $('#form_buffer_create').webgisform('getdata');
		return data['style'];
	};
	var get_distance = function()
	{
		var data = $('#form_buffer_create').webgisform('getdata');
		return data['distance'];
	};
	var get_analyze_option = function()
	{
		var r = [];
		$('#form_buffer_analyze').find('input[id^=form_buffer_analyze_]').each(function(){
			var t = $(this).attr('id').replace('form_buffer_analyze_', '');
			if($(this).is(':checked')) r.push(t);
		});
		return r;
	};
	var clear_tmp_buffer = function()
	{
		if($.webgis.data.geojsons['tmp_buffer']) 
		{
			delete $.webgis.data.geojsons['tmp_buffer'];
			$.webgis.data.geojsons['tmp_buffer'] = undefined;
		}
		if($.webgis.data.czmls['tmp_buffer']) 
		{
			delete $.webgis.data.czmls['tmp_buffer'];
			$.webgis.data.czmls['tmp_buffer'] = undefined;
			ReloadCzmlDataSource(viewer, $.webgis.config.zaware, true);
		}
	};
	var bind_buttons = function(formname, dialog)
	{
		if(formname === 'form_buffer_create')
		{
			buttons = [
				{ 	text: "下一步", 
					click: function(){ 
						if($('#form_buffer_create').valid())
						{
							var style = get_style();
							BufferCreate(viewer, type, position, get_distance(), style, 8,  function(geojson){
								//console.log(style);
								//console.log(geojson);
								buffer_geojson = geojson;
								switch_panel('form_buffer_analyze', dialog);
								
							});
						}
					}
				},
				//{ 	text: "清空", 
					//click: function(){
						//clear_tmp_buffer();
					//}
				//},
				{ 	text: "关闭", 
					click: function(){
						clear_tmp_buffer();
						$( dialog ).dialog( "close" );
					}
				}
			];
		}
		else if(formname === 'form_buffer_analyze')
		{
			buttons = [
				{ 	text: "上一步", 
					click: function(){
						clear_tmp_buffer();
						buffer_geojson = undefined;
						switch_panel('form_buffer_create', dialog);
					}
				},
				{ 	text: "分析", 
					click: function(){ 
						if(buffer_geojson)
						{
							//console.log(buffer_geojson);
							//console.log(get_analyze_option());
							BufferAnalyze(viewer, buffer_geojson, get_analyze_option(), function(data){
								//console.log(data);
								if(data.length>0)
								{
									for(var i in data)
									{
										var g = data[i];
										//console.log(g);
										if(!$.webgis.data.geojsons[g['_id']]) $.webgis.data.geojsons[g['_id']] = g;//AddTerrainZOffset(g);
										if(!$.webgis.data.czmls[g['_id']]) $.webgis.data.czmls[g['_id']] = CreateCzmlFromGeojson($.webgis.data.geojsons[g['_id']]);
									}
									ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
								}
							});
						}
					}
				},
				//{ 	text: "保存", 
					//click: function(){
						//ShowConfirm(null, 500, 200,
							//'保存确认',
							//'确认保存吗? 确认的话该缓冲区域将会提交到服务器上，以便所有人都能利用该缓冲区做分析。',
							//function(){
								//clear_tmp_buffer();
							//},
							//function(){
								//clear_tmp_buffer();
							//}
						//);
					//}
				//},
				{ 	text: "关闭", 
					click: function(){
						clear_tmp_buffer();
						$( dialog ).dialog( "close" );
					}
				}
			];
		}
		$('#dlg_buffer_analyze').dialog("option", "buttons", buttons);
	};
	
	
	var dialog = $('#dlg_buffer_analyze').dialog({
		width: 500,
		height: 550,
		minWidth:200,
		minHeight: 200,
		draggable: true,
		resizable: true, 
		modal: false,
		position:{at: "right center"},
		title:'缓冲区分析',
		close:function(event, ui){
		},
		show: {
			effect: "slide",
			direction: "right",
			duration: 400
		},
		hide: {
			effect: "slide",
			direction: "right",
			duration: 400
		}		
	});
	var flds = [	
		{ display: "距离(米)", id: "distance", defaultvalue:2000, newline: true,  type: "spinner", step:1, min:10,max:20000, group:'参数', width:250,labelwidth:90, validate:{required:true, number: true, range:[10, 20000]}},
		{ display: "填充颜色", id: "fill_color", defaultvalue:GetDefaultStyleValue('polygon_buffer', 'color'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
		{ display: "轮廓颜色", id: "outline_color", defaultvalue:GetDefaultStyleValue('polygon_buffer', 'outlineColor'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
		{ display: "标签颜色", id: "label_fill_color",  defaultvalue:GetDefaultStyleValue('polygon_buffer', 'labelFillColor'), newline: true,  type: "color", group:'样式', width:50, labelwidth:120 },
		//{ display: "标签尺寸", id: "label_scale", defaultvalue:GetDefaultStyleValue('polygon_buffer', 'labelScale'), newline: true,  type: "spinner", step:1, min:1,max:5, group:'样式', width:70, labelwidth:120, validate:{number: true, required:true} }
	];
	
	$('#form_buffer_create').webgisform(flds, 
		{
			prefix:'form_buffer_create_', 
			divorspan:'div',
			maxwidth:400
	});
	var flds1 = [	
		{ display: "杆塔", id: "point_tower", defaultvalue:true, newline: false,  type: "checkbox", group:'地标', width:32,labelwidth:90},
		{ display: "地标", id: "point_marker", defaultvalue:true, newline: false,  type: "checkbox", group:'地标', width:32,labelwidth:90},
		{ display: "隐患点", id: "point_hazard", defaultvalue:true, newline: false,  type: "checkbox", group:'地标', width:32,labelwidth:90},
		{ display: "地市", id: "point_subcity", defaultvalue:false, newline: false,  type: "checkbox", group:'地点', width:32,labelwidth:90},
		{ display: "区县", id: "point_county", defaultvalue:false, newline: false,  type: "checkbox", group:'地点', width:32,labelwidth:90},
		{ display: "乡镇", id: "point_town", defaultvalue:false, newline: true,  type: "checkbox", group:'地点', width:32,labelwidth:90},
		{ display: "村寨", id: "point_village", defaultvalue:false, newline: false,  type: "checkbox", group:'地点', width:32,labelwidth:90}
	];
	
	$('#form_buffer_analyze').webgisform(flds1, 
		{
			prefix:'form_buffer_analyze_', 
			divorspan:'span',
			maxwidth:400
	});
	switch_panel('form_buffer_create', dialog);

}


function ShowDNAddDialog(viewer)
{
	var ellipsoid = viewer.scene.globe.ellipsoid;
	$('#dlg_dn_create').dialog({
		width: 500,
		height: 550,
		minWidth:200,
		minHeight: 200,
		draggable: true,
		resizable: true, 
		modal: false,
		position:{at: "right center"},
		title:'创建配电网络',
		close:function(event, ui){
			delete $.webgis.select.selected_geojson;
			$.webgis.select.selected_geojson = undefined;
		},
		show: {
			effect: "slide",
			direction: "right",
			duration: 400
		},
		hide: {
			effect: "slide",
			direction: "right",
			duration: 400
		},		
		buttons:[
			{ 	text: "保存", 
				click: function(){ 
					if($('#form_dn_create').valid())
					{
						var that = this;
						ShowConfirm(null, 500, 200,
							'保存确认',
							'确认保存吗? 确认的话数据将会提交到服务器上，以便所有人都能看到修改的结果。',
							function(){
								SaveDN(viewer, function(){
									$( that ).dialog( "close" );
								});
							},
							function(){
								$( that ).dialog( "close" );
							}
						);
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
	
	var flds = [
		{ display: "名称", id: "name", newline: true,  type: "text", group:'信息', width:250,labelwidth:90, validate:{required:true,minlength: 1}}
	];
	$("#form_dn_create" ).webgisform(flds, {
			divorspan:"div",
			prefix:"form_dn_create_",
			maxwidth:400
			//margin:10,
			//groupmargin:10
	});
}

function GetPropertiesByTwoNodes(viewer, id0, id1)
{
	var ret;
	//var scene = viewer.scene;
	for(var i in $.webgis.geometry.segments)
	{
		var g = $.webgis.geometry.segments[i];
		if(g.start == id0 && g.end == id1)
		{
			ret = g.properties;
			break;
		}
	}
	return ret
}

function SaveEdge(viewer, id, callback)
{
	
	if($.webgis.config.map_backend === 'cesium')
	{
		if($.webgis.config.node_connect_mode 
		&& $.webgis.select.selected_obj 
		&& $.webgis.select.prev_selected_obj 
		&& $.webgis.data.czmls[$.webgis.select.selected_obj.id] 
		&& $.webgis.data.czmls[$.webgis.select.prev_selected_obj.id] 
		&& $.webgis.data.czmls[$.webgis.select.selected_obj.id]['webgis_type'] === $.webgis.data.czmls[$.webgis.select.prev_selected_obj.id]['webgis_type']
		)
		{
			var geojson = {};
			var webgis_type = $.webgis.data.czmls[$.webgis.select.selected_obj.id]['webgis_type'];
			geojson['_id'] = id;
			geojson['type'] = 'Feature';
			geojson['properties'] = GetPropertiesByTwoNodes(viewer, $.webgis.select.prev_selected_obj.id, $.webgis.select.selected_obj.id);
			var cond = {'db':$.webgis.db.db_name, 'collection':'edges', 'action':'save', 'data':geojson};
			ShowProgressBar(true, 670, 200, '保存中', '正在保存，请稍候...');
			MongoFind(cond, function(data1){
				ShowProgressBar(false);
				if(callback) callback(data1);
			});
		}
	}
	if($.webgis.config.map_backend === 'leaflet')
	{
		if($.webgis.config.node_connect_mode 
		&& $.webgis.select.selected_obj 
		&& $.webgis.select.prev_selected_obj 
		&& $.webgis.data.geojsons[$.webgis.select.selected_obj.id] 
		&& $.webgis.data.geojsons[$.webgis.select.prev_selected_obj.id] 
		&& $.webgis.data.geojsons[$.webgis.select.selected_obj.id] ['properties']
		&& $.webgis.data.geojsons[$.webgis.select.prev_selected_obj.id]['properties'] 
		&& $.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'] === $.webgis.data.geojsons[$.webgis.select.prev_selected_obj.id]['properties']['webgis_type']
		)
		{
			var geojson = {};
			//var webgis_type = $.webgis.data.geojsons[$.webgis.select.selected_obj.id]['properties']['webgis_type'];
			//webgis_type = webgis_type.replace('point', 'edge');
			geojson['_id'] = id;
			geojson['type'] = 'Feature';
			geojson['properties'] = GetPropertiesByTwoNodes(viewer, $.webgis.select.prev_selected_obj.id, $.webgis.select.selected_obj.id);
			var cond = {'db':$.webgis.db.db_name, 'collection':'edges', 'action':'save', 'data':geojson};
			ShowProgressBar(true, 670, 200, '保存中', '正在保存，请稍候...');
			MongoFind(cond, function(data1){
				ShowProgressBar(false);
				if(callback) callback(data1);
			});
		}
	
	}
}

function SaveDN(viewer, callback)
{
	var data = $("#form_dn_create" ).webgisform('getdata');
	var geojson = {};
	geojson['_id'] = null;
	geojson['properties'] = {};
	geojson['properties']['webgis_type'] = 'polyline_dn';
	for (var k in data)
	{
		geojson['properties'][k] = data[k];
	}
	var cond = {'db':$.webgis.db.db_name, 'collection':'network', 'action':'save', 'data':geojson};
	ShowProgressBar(true, 670, 200, '保存中', '正在保存，请稍候...');
	MongoFind(cond, function(data1){
		ShowProgressBar(false);
		if(data1.length>0)
		{
			$.jGrowl("保存成功", { 
				life: 2000,
				position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
				theme: 'bubblestylesuccess',
				glue:'before'
			});
		}else
		{
			$.jGrowl("保存失败", { 
				life: 2000,
				position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
				theme: 'bubblestylefail',
				glue:'before'
			});
		}
		if(callback) callback(data1);
	});
}

function ShowPoiInfoDialog(viewer, title, type, position, id)
{
	var ellipsoid;
	if($.webgis.config.map_backend === 'cesium')
	{
		ellipsoid = viewer.scene.globe.ellipsoid;
	}
	$('#dlg_poi_info').dialog({
		width: 540,
		height: 680,
		minWidth:200,
		minHeight: 200,
		draggable: true,
		resizable: true, 
		modal: false,
		position:{at: "right center"},
		title:title,
		close:function(event, ui){
			delete $.webgis.select.selected_geojson;
			$.webgis.select.selected_geojson = undefined;
		},
		show: {
			effect: "slide",
			direction: "right",
			duration: 400
		},
		hide: {
			effect: "slide",
			direction: "right",
			duration: 400
		},		
		buttons:[
			{ 	text: "缓冲区分析", 
				click: function(){ 
					if(!CheckPermission('buffer_analyze'))
					{
						return;
					}

					$( this ).dialog( "close" );
					if(id && $.webgis.data.geojsons[id])
					{
						
						if($.webgis.config.map_backend === 'cesium')
						{
							if(type === 'point')
							{
								var arr = $.webgis.data.geojsons[id]['geometry']['coordinates'];
								var carto =  Cesium.Cartographic.fromDegrees(arr[0], arr[1], arr[2]);
								position = ellipsoid.cartographicToCartesian(carto);
							}
							else if(type === 'polyline')
							{
								var arr = $.webgis.data.geojsons[id]['geometry']['coordinates'];
								position = [];
								for(var i in arr)
								{
									var carto =  Cesium.Cartographic.fromDegrees(arr[i][0], arr[i][1], arr[i][2]);
									position.push(ellipsoid.cartographicToCartesian(carto));
								}
							}
							else if(type === 'polygon')
							{
								var arr = $.webgis.data.geojsons[id]['geometry']['coordinates'][0];
								position = [];
								for(var i in arr)
								{
									var carto =  Cesium.Cartographic.fromDegrees(arr[i][0], arr[i][1], arr[i][2]);
									position.push(ellipsoid.cartographicToCartesian(carto));
								}
							}
						}
						if($.webgis.config.map_backend === 'leaflet')
						{
							if(type === 'point')
							{
								var arr = $.webgis.data.geojsons[id]['geometry']['coordinates']
								position = L.latLng(arr[1], arr[0]);
							}
							else if(type === 'polyline')
							{
								var arr = $.webgis.data.geojsons[id]['geometry']['coordinates'];
								position = [];
								for(var i in arr)
								{
									var lnglat =  L.latLng(arr[i][1], arr[i][0]);
									position.push(lnglat);
								}
							}
							else if(type === 'polygon')
							{
								var arr = $.webgis.data.geojsons[id]['geometry']['coordinates'][0];
								position = [];
								for(var i in arr)
								{
									var lnglat =  L.latLng(arr[i][1], arr[i][0]);
									position.push(lnglat);
								}
							}
						
						}
					}
					ShowBufferAnalyzeDialog(viewer, type, position);
				}
			},
			{ 	text: "保存", 
				click: function(){
					var that = $(this);
					var v = $('#select_poi_type').val();
					if($('#form_poi_info_' + v).valid())
					{
						if(!CheckPermission('feature_save'))
						{
							return;
						}
						ShowConfirm(null, 500, 200,
							'保存确认',
							'确认保存吗? 确认的话数据将会提交到服务器上，以便所有人都能看到修改的结果。',
							function(){
								var data = {};
								data['_id'] = id;
								if(!data['_id'] || data['_id'].length == 0) data['_id'] = null;
								var properties =  $('#form_poi_info_' + v).webgisform('getdata');
								delete properties.id;
								

								data['properties'] = properties;
								data['properties']['webgis_type'] = v;
								for(var k in data['properties'])
								{
									if(!data['properties'][k] || data['properties'][k].length == 0)
									{
										data['properties'][k] = null;
									}
								}
								var t = 'Point';
								if(v.indexOf('polyline')>-1)
								{
									t = 'LineString';
								}
								if(v.indexOf('polygon')>-1) 
								{
									t = 'Polygon';
								}
								if(id === undefined)
								{
									data['geometry'] = {type:t, coordinates:GetGeojsonFromPosition(ellipsoid, position, t)};
								}
								SavePoi(data, function(data1){
									ClearSelectEntity();
									that.dialog( "close" );
									
									if(id === undefined)
									{
										$.webgis.control.drawhelper.clearPrimitive();
										if(data1 && data1.length>0)
										{
											for(var i in data1)
											{
												var geojson = data1[i];
												var id = geojson['_id'];
												if(!$.webgis.data.geojsons[id])
												{
													$.webgis.data.geojsons[id] = geojson; //AddTerrainZOffset(geojson);
												}
												if($.webgis.config.map_backend === 'cesium')
												{
													if(!$.webgis.data.czmls[id])
													{
														$.webgis.data.czmls[id] = CreateCzmlFromGeojson($.webgis.data.geojsons[id]);
													}
												}
												if($.webgis.config.map_backend === 'leaflet')
												{
													$.webgis.control.leaflet_geojson_layer.addData(geojson);
												}
											}
											if($.webgis.config.map_backend === 'cesium')
											{
												ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
											}
										}
									}
								});
							},
							function(){
							
							}
						);
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
	
	
	var poitypelist = [];
	$('#select_poi_type').empty();
	if(type == 'point')
	{
		poitypelist = [
			{value:'point_marker',label:'普通地标'},
			{value:'point_hazard',label:'隐患点'},
			{value:'point_tower',label:'杆塔'},
			{value:'point_dn',label:'配电网设备'}
		];
	}
	if(type == 'polyline')
	{
		poitypelist = [{value:'polyline_marker',label:'路线'},{value:'polyline_hazard',label:'线状隐患源'}];
	}
	if(type == 'polygon')
	{
		poitypelist = [{value:'polygon_marker',label:'区域'},{value:'polygon_hazard',label:'区域隐患源'}];
		if(id === undefined)
		{
			if($.webgis.config.map_backend === 'cesium')
			{
				AddToCzml(ellipsoid, type, position);
			}
		}
	}
		
	for(var i in poitypelist)
	{
		$('#select_poi_type').append('<option value="' + poitypelist[i]['value'] + '">' + poitypelist[i]['label'] + '</option>');
	}
	var auto = $('#select_poi_type').autocomplete({
		//position: { my: "left top", at: "left bottom", collision: "none" },
		autoFocus: false,
		source:poitypelist,
	});
	
	$("form[id^=form_poi_info_]").empty();
	var webformlist = BuildPoiForms();
	$("form[id^=form_poi_info_]").parent().css('display','none');
	if(id && $.webgis.data.geojsons[id])
	{
		var wt = $.webgis.data.geojsons[id]['properties']['webgis_type'];
		$("#form_poi_info_" + wt).parent().css('display','block');
	}
	else
	{
		$("#form_poi_info_" + type + "_marker").parent().css('display','block');
	}
	$( "#select_poi_type" ).on( "change", function( event) {
		$("form[id^=form_poi_info_]").parent().css('display','none');
		var v = event.target.value;
		webformlist[v].parent().css('display','block');
	});
	if(id && $.webgis.data.geojsons[id])
	{
		var data = $.webgis.data.geojsons[id]['properties'];
		var wt = $.webgis.data.geojsons[id]['properties']['webgis_type'];
		$("#form_poi_info_" + wt).webgisform('setdata', data);
	}
	
	$('#tabs_poi_info').tabs({ 
		collapsible: false,
		active: 0,
		beforeActivate: function( event, ui ) {
			var title = ui.newTab.context.innerText;
			if(title == '基础信息')
			{
			}
			if(title == '照片文档')
			{
				ShowProgressBar(true, 670, 200, '载入中', '正在载入，请稍候...');
				CreateFileBrowser('poi_info_photo', 450, 480, ['jpg','jpeg','png', 'bmp', 'gif', 'doc', 'xls', 'xlsx', 'docx', 'pdf'], 'features', id);
			}
		}
	});
}

function ClearSelectEntity()
{
	$.webgis.viewer.trackedEntity = undefined;
	$.webgis.viewer.selectedEntity = undefined;
	delete $.webgis.select.selected_geojson;
	$.webgis.select.selected_geojson = undefined;
	$.webgis.select.selected_obj = undefined;
}

function AddToCzml(ellipsoid, type, positions)
{
	var cnt = 0;
	var id;
	var g = {};
	g['geometry'] = {};
	g['geometry']['type'] = '';
	g['geometry']['coordinates'] = [];
	g['properties'] = {};
	g['properties']['webgis_type'] = '';
	if(type === 'polyline')
	{
		for(var k in $.webgis.data.czmls)
		{
			if(k.indexOf('tmp_polyline_')>-1)
			{
				cnt += 1;
			}
		}
		id = 'tmp_polyline_' + cnt;
		g['geometry']['type'] = 'LineString';
		g['properties']['webgis_type'] = 'polyline_marker';
		for(var i in positions)
		{
			var cart3 = positions[i];
			var carto = ellipsoid.cartesianToCartographic(cart3);
			g['geometry']['coordinates'].push([Cesium.Math.toDegrees(carto.longitude), Cesium.Math.toDegrees(carto.latitude)]);
		}
		
	}
	if(type === 'polygon')
	{
		for(var k in $.webgis.data.czmls)
		{
			if(k.indexOf('tmp_polygon_')>-1)
			{
				cnt += 1;
			}
		}
		id = 'tmp_polygon_' + cnt;
		g['geometry']['type'] = 'Polygon';
		g['properties']['webgis_type'] = 'polygon_marker';
		g['geometry']['coordinates'].push([]);
		var carto_0;
		for(var i in positions)
		{
			var cart3 = positions[i];
			if($.webgis.config.map_backend === 'cesium')
			{
				var carto = ellipsoid.cartesianToCartographic(cart3);
				if(i == 0)
				{
					carto_0 = carto;
				}
				g['geometry']['coordinates'][0].push([Cesium.Math.toDegrees(carto.longitude), Cesium.Math.toDegrees(carto.latitude)]);
			}
			if($.webgis.config.map_backend === 'leaflet')
			{
				if(i == 0)
				{
					carto_0 = cart3;
				}
				g['geometry']['coordinates'][0].push([cart3.lng, cart3.lat]);
			}
		}
		if($.webgis.config.map_backend === 'cesium')
		{
			g['geometry']['coordinates'][0].push([Cesium.Math.toDegrees(carto_0.longitude), Cesium.Math.toDegrees(carto_0.latitude)]);
		}
		if($.webgis.config.map_backend === 'leaflet')
		{
			g['geometry']['coordinates'][0].push([carto_0.lng, carto_0.lat]);
		}
	}
	g['_id'] = id;
	if(!$.webgis.data.czmls[id])
	{
		$.webgis.data.czmls[id] = CreateCzmlFromGeojson(g);
		if(type === 'polygon')
		{
			$.webgis.data.czmls[id]['polygon']['extrudedHeight'] = {'number': 3000};
			$.webgis.data.czmls[id]['polygon']['material']['solidColor']['color'] = {'rgba':[255,255,0, 80]};
		}
	}
	
}

function CreateCzmlFromGeojson(geojson)
{
	var ret;
	var t = geojson['geometry']['type'];
	if(t === 'Point')
		ret = CreatePointCzmlFromGeojson(geojson);
	if(t === 'LineString' || t === 'MultiLineString')
		ret = CreatePolyLineCzmlFromGeojson(geojson);
	if(t === 'Polygon')
		ret = CreatePolygonCzmlFromGeojson(geojson);
	return ret;
}

function BuildPoiForms()
{
	var ret = {};
	var vlist = ['point_marker', 'point_hazard', 'point_tower', 'point_dn_switch','point_dn_link','point_dn_transform','point_dn_transformarea', 'polyline_marker', 'polyline_hazard', 'polygon_marker', 'polygon_hazard'];
	for(var i in vlist)
	{
		v = vlist[i];
		var fields;
		if(v === "point_tower")
		{
			fields = [
				//{ id: "id", type: "hidden" },
				{ display: "名称", id: "name", newline: true,  type: "text", group:'信息', width:250,labelwidth:90, validate:{required:true,minlength: 1}},
				{ display: "代码", id: "tower_code", newline: true,  type: "text", group:'信息', width:250,labelwidth:90 },
				//{ display: "塔型", id: "model_code", newline: false,  type: "text", group:'信息', width:80,labelwidth:90 },
				//{ display: "呼称高", id: "denomi_height", newline: false,  type: "spinner", step:0.1, min:0,max:100, group:'信息', width:40, validate:{number: true, range:[0, 100]}},
				//电气
				{ display: "接地电阻", id: "grnd_resistance", newline: true,  type: "spinner", step:0.1, min:0,max:9999, group:'电气', width:250, validate:{number: true, required:false, range:[0, 9999]}},
				//土木
				{ display: "水平档距", id: "horizontal_span", newline: false,  type: "spinner", step:0.1, min:0,max:9999, group:'土木', width:40, validate:{number: true, required:false, range:[0, 9999]} },
				{ display: "垂直档距", id: "vertical_span", newline: false,  type: "spinner", step:0.1, min:0,max:9999, group:'土木', width:40, validate:{number: true, required:false, range:[0, 9999]} },
				//工程
				{ display: "线路名称", id: "line_names", newline: true,  type: "select", editor:{data:[], position:'top'},  group:'工程', width:250 }
			];
			for(var i in fields)
			{
				if(fields[i].id === 'line_names')
				{
					fields[i].editor.data = CreateLineNamesSelectOption();
					break;
				}
			}
		}
		if(v === "point_marker")
		{
			fields = [	
				{ display: "显示图标", id: "icon", newline: true,  type: "icon", defaultvalue:"point_marker" ,iconlist:['point_marker', 'point_tower', 'point_hazard'], group:'信息'},
				{ display: "名称", id: "name", newline: true,  type: "text", group:'信息', width:250,labelwidth:90, validate:{required:true,minlength: 1}},
				{ display: "描述", id: "description", newline: true,  type: "text", group:'信息', width:250, labelwidth:90 },
				{ display: "填充颜色", id: "fill_color", defaultvalue:GetDefaultStyleValue(v, 'color'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "轮廓颜色", id: "outline_color", defaultvalue:GetDefaultStyleValue(v, 'outlineColor'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "标签颜色", id: "label_fill_color",  defaultvalue:GetDefaultStyleValue(v, 'labelFillColor'), newline: true,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "尺寸", id: "pixel_size", defaultvalue:GetDefaultStyleValue(v, 'pixelSize'), newline: false,  type: "spinner", step:1, min:1,max:50, group:'样式', width:30, labelwidth:120, validate:{number: true, required:true, range:[1, 50]} },
				{ display: "标签尺寸", id: "label_scale", defaultvalue:GetDefaultStyleValue(v, 'labelScale'), newline: false,  type: "spinner", step:0.1, min:0.1,max:10, group:'样式', width:30, labelwidth:90, validate:{number: true, required:true, range:[0.1, 10]} }
			];
		}
		if(v === "point_hazard")
		{
			fields = [	
				//{ id: "id", type: "hidden" },
				{ display: "显示图标", id: "icon", newline: true,  type: "icon", defaultvalue:"point_marker" ,iconlist:['point_marker', 'point_tower', 'point_hazard'], group:'信息'},
				{ display: "名称", id: "name", newline: true,  type: "text", group:'信息', width:250, validate:{required:true,minlength: 1}},
				{ display: "高度", id: "height", newline: true,  type: "spinner",step:1, min:0,max:9999, group:'信息', width:220, validate:{number: true, range:[0, 9999]} },
				{ display: "描述", id: "description", newline: true,  type: "text", group:'信息', width:250 },
				{ display: "联系人", id: "contact_person", newline: true,  type: "text", group:'信息', width:250 },
				{ display: "发现时间", id: "discover_date", newline: true,  type: "date", group:'信息', width:130 },
				{ display: "填充颜色", id: "fill_color", defaultvalue:GetDefaultStyleValue(v, 'color'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "轮廓颜色", id: "outline_color", defaultvalue:GetDefaultStyleValue(v, 'outlineColor'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "标签颜色", id: "label_fill_color",  defaultvalue:GetDefaultStyleValue(v, 'labelFillColor'), newline: true,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "尺寸", id: "pixel_size", defaultvalue:GetDefaultStyleValue(v, 'pixelSize'), newline: false,  type: "spinner", step:1, min:1,max:50, group:'样式', width:30, labelwidth:120, validate:{number: true, required:true, range:[1, 50]} },
				{ display: "标签尺寸", id: "label_scale", defaultvalue:GetDefaultStyleValue(v, 'labelScale'), newline: false,  type: "spinner", step:0.1, min:0.1,max:10, group:'样式', width:30, labelwidth:90, validate:{number: true, required:true, range:[0.1, 10]} }
			];
		}
		if(v.indexOf("point_dn_")>-1)
		{
			var function_list = [];
			//console.log($.webgis.data.codes['functional_type']);
			for(var k in $.webgis.data.codes['functional_type'])
			{
				
				if(k == 'PAE' || k == 'PAB' || k == 'PLM')
				{
					function_list.push({value:k, label:$.webgis.data.codes['functional_type'][k]});
				}
			}
			function_list.push({value:'T', label:'变压器区域'});
			fields = [	
				//{ id: "id", type: "hidden" },
				{ display: "显示图标", id: "icon", defaultvalue:"point_dn_switch", newline: true,  type: "icon", defaultvalue:"point_marker" ,iconlist:['point_marker', 'point_tower', 'point_hazard','point_dn_switch','point_dn_link','point_dn_transform','point_dn_transformarea'], group:'信息'},
				{ display: "名称", id: "name", newline: true,  type: "text", group:'信息', width:250, validate:{required:true,minlength: 1}},
				{ display: "功能分类", id: "function_type", newline: true,  type: "select",editor: {data:function_list}, group:'电气特性', width:250, validate:{required:true,minlength: 1}},
				{ display: "填充颜色", id: "fill_color", defaultvalue:GetDefaultStyleValue(v, 'color'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "轮廓颜色", id: "outline_color", defaultvalue:GetDefaultStyleValue(v, 'outlineColor'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "标签颜色", id: "label_fill_color",  defaultvalue:GetDefaultStyleValue(v, 'labelFillColor'), newline: true,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "尺寸", id: "pixel_size", defaultvalue:GetDefaultStyleValue(v, 'pixelSize'), newline: false,  type: "spinner", step:1, min:1,max:50, group:'样式', width:30, labelwidth:120, validate:{number: true, required:true, range:[1, 50]} },
				{ display: "标签尺寸", id: "label_scale", defaultvalue:GetDefaultStyleValue(v, 'labelScale'), newline: false,  type: "spinner", step:0.1, min:0.1,max:10, group:'样式', width:30, labelwidth:90, validate:{number: true, required:true, range:[0.1, 10]} }
			];
		}
		if(v === "polyline_marker")
		{
			fields = [	
				{ display: "名称", id: "name", newline: true,  type: "text", group:'信息', width:250,labelwidth:90, validate:{required:true,minlength: 1}},
				{ display: "描述", id: "description", newline: true,  type: "text", group:'信息', width:250, labelwidth:90 },
				{ display: "填充颜色", id: "fill_color", defaultvalue:GetDefaultStyleValue(v, 'color'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
				//{ display: "轮廓颜色", id: "outline_color", defaultvalue:GetDefaultStyleValue(v, 'outlineColor'), newline: true,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "标签颜色", id: "label_fill_color",  defaultvalue:GetDefaultStyleValue(v, 'labelFillColor'), newline: true,  type: "color", group:'样式', width:50, labelwidth:120 },
				//{ display: "宽度", id: "pixel_width", defaultvalue:GetDefaultStyleValue(v, 'pixelWidth'), newline: true,  type: "spinner", step:1, min:1,max:50, group:'样式', width:70, labelwidth:120, validate:{number: true, required:true, range:[1, 50]} },
				//{ display: "标签尺寸", id: "label_scale", defaultvalue:GetDefaultStyleValue(v, 'labelScale'), newline: true,  type: "spinner", step:0.1, min:0.1,max:10, group:'样式', width:70, labelwidth:120, validate:{number: true, required:true, range:[0.1, 10]} }
				{ display: "宽度", id: "pixel_width", defaultvalue:GetDefaultStyleValue(v, 'pixelWidth'), newline: false,  type: "spinner", step:1, min:1,max:50, group:'样式', width:30, labelwidth:120, validate:{number: true, required:true, range:[1, 50]} },
				{ display: "标签尺寸", id: "label_scale", defaultvalue:GetDefaultStyleValue(v, 'labelScale'), newline: false,  type: "spinner", step:0.1, min:0.1,max:10, group:'样式', width:30, labelwidth:90, validate:{number: true, required:true, range:[0.1, 10]} }
			];
		}
		if(v === "polyline_hazard")
		{
			fields = [	
				{ display: "名称", id: "name", newline: true,  type: "text", group:'信息', width:250, validate:{required:true,minlength: 1}},
				{ display: "高度", id: "height", newline: true,  type: "spinner",step:1, min:0,max:9999, group:'信息', width:220, validate:{number: true, range:[0, 9999]} },
				{ display: "描述", id: "description", newline: true,  type: "text", group:'信息', width:250 },
				{ display: "联系人", id: "contact_person", newline: true,  type: "text", group:'信息', width:250 },
				{ display: "发现时间", id: "discover_date", newline: true,  type: "date", group:'信息', width:130 },
				{ display: "填充颜色", id: "fill_color", defaultvalue:GetDefaultStyleValue(v, 'color'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
				//{ display: "轮廓颜色", id: "outline_color", defaultvalue:GetDefaultStyleValue(v, 'outlineColor'), newline: true,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "标签颜色", id: "label_fill_color",  defaultvalue:GetDefaultStyleValue(v, 'labelFillColor'), newline: true,  type: "color", group:'样式', width:50, labelwidth:120 },
				//{ display: "宽度", id: "pixel_width", defaultvalue:GetDefaultStyleValue(v, 'pixelWidth'), newline: true,  type: "spinner", step:1, min:1,max:50, group:'样式', width:70, labelwidth:120, validate:{number: true, required:true, range:[1, 50]} },
				//{ display: "标签尺寸", id: "label_scale", defaultvalue:GetDefaultStyleValue(v, 'labelScale'), newline: true,  type: "spinner", step:0.1, min:0.1,max:10, group:'样式', width:70, labelwidth:120, validate:{number: true, required:true, range:[0.1, 10]} }
				{ display: "宽度", id: "pixel_width", defaultvalue:GetDefaultStyleValue(v, 'pixelWidth'), newline: false,  type: "spinner", step:1, min:1,max:50, group:'样式', width:30, labelwidth:120, validate:{number: true, required:true, range:[1, 50]} },
				{ display: "标签尺寸", id: "label_scale", defaultvalue:GetDefaultStyleValue(v, 'labelScale'), newline: false,  type: "spinner", step:0.1, min:0.1,max:10, group:'样式', width:30, labelwidth:90, validate:{number: true, required:true, range:[0.1, 10]} }
			];
		}
		if(v === "polygon_marker")
		{
			fields = [	
				{ display: "名称", id: "name", newline: true,  type: "text", group:'信息', width:250,labelwidth:90, validate:{required:true,minlength: 1}},
				{ display: "描述", id: "description", newline: true,  type: "text", group:'信息', width:250, labelwidth:90 },
				{ display: "填充颜色", id: "fill_color", defaultvalue:GetDefaultStyleValue(v, 'color'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "轮廓颜色", id: "outline_color", defaultvalue:GetDefaultStyleValue(v, 'outlineColor'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "标签颜色", id: "label_fill_color",  defaultvalue:GetDefaultStyleValue(v, 'labelFillColor'), newline: true,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "标签尺寸", id: "label_scale", defaultvalue:GetDefaultStyleValue(v, 'labelScale'), newline: true,  type: "spinner", step:0.1, min:0.1,max:10, group:'样式', width:70, labelwidth:120, validate:{number: true, required:true, range:[0.1, 10]} }
			];
		}
		if(v === "polygon_hazard")
		{
			fields = [	
				{ display: "名称", id: "name", newline: true,  type: "text", group:'信息', width:250, validate:{required:true,minlength: 1}},
				{ display: "高度", id: "height", newline: true,  type: "spinner",step:1, min:0,max:9999, group:'信息', width:220, validate:{number: true, range:[0, 9999]} },
				{ display: "描述", id: "description", newline: true,  type: "text", group:'信息', width:250 },
				{ display: "联系人", id: "contact_person", newline: true,  type: "text", group:'信息', width:250 },
				{ display: "发现时间", id: "discover_date", newline: true,  type: "date", group:'信息', width:130 },
				{ display: "填充颜色", id: "fill_color", defaultvalue:GetDefaultStyleValue(v, 'color'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "轮廓颜色", id: "outline_color", defaultvalue:GetDefaultStyleValue(v, 'outlineColor'), newline: false,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "标签颜色", id: "label_fill_color",  defaultvalue:GetDefaultStyleValue(v, 'labelFillColor'), newline: true,  type: "color", group:'样式', width:50, labelwidth:120 },
				{ display: "标签尺寸", id: "label_scale", defaultvalue:GetDefaultStyleValue(v, 'labelScale'), newline: true,  type: "spinner", step:0.1, min:0.1,max:10, group:'样式', width:70, labelwidth:120, validate:{number: true, required:true, range:[0.1, 10]} }
			];
		}
		var webgis_type = v;
		if(v.indexOf('point_dn_')>-1)
		{
			webgis_type = 'point_dn';
		}
		if(!ret[webgis_type] && fields)
		{
			ret[webgis_type] = $("#form_poi_info_" + webgis_type).webgisform(fields, {
					//divorspan:"span",
					prefix:"form_poi_info_" + webgis_type + '_',
					maxwidth:400
					//margin:10,
					//groupmargin:10
				});
		}
		
	}
	return ret;
}


function CheckPoiInfoModified()
{
	
	return false;

}



function GetSegmentsByTowerStartEnd(start_id, end_ids)
{
	var ret = [];
	
	for(var i in end_ids)
	{
		var end_id = end_ids[i];
		for(var j in $.webgis.data.segments)
		{
			var seg = $.webgis.data.segments[j];
			if(seg['start_tower'] == start_id && seg['end_tower'] == end_id)
			{
				ret.push(seg);
				break;
			}
		}
	}
	
	return ret;
}

function CheckModelCode(modelcode)
{
	var ret = false;
	for(var i in $.webgis.data.models_gltf_files)
	{
		if ($.webgis.data.models_gltf_files[i] == modelcode)
		{
			ret = true;
			break;
		}
	}
	return ret;
}

function RePositionPoint(viewer, id, lng, lat, height, rotate)
{
	if($.webgis.data.czmls[id] && $.isNumeric(lng) && $.isNumeric(lat) && $.isNumeric(height) && $.isNumeric(rotate))
	{
		$.webgis.data.czmls[id]['position']['cartographicDegrees'] = [parseFloat(lng), parseFloat(lat), parseFloat(height)];
		ReloadCzmlDataSource(viewer, $.webgis.config.zaware);
	}
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
		var column2Row2Index = Cesium.Matrix4.getElementIndex(2, 2);
		if(true)
		{
			mat4[column2Row2Index] = - mat4[column2Row2Index];
		}
		var m = Cesium.Matrix4.multiplyTransformation(modelMatrix, mat4, mat4);
		model.modelMatrix = m;
	}

}


function GetLineNamesListByTowerId(id)
{
	var ret = [];
	for(var k in $.webgis.data.lines)
	{
		if($.webgis.data.lines[k]['properties']['nodes'].indexOf(id)>-1)
		{
			ret.push(k);
		}
	}
	return ret;
}

function AddMetal(e)
{
	if($.webgis.select.selected_geojson)
	{
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
		if(e.text == '超声波驱鸟装置')
		{
			o['imei'] = '';
			var get_model = function(){
				var ret = '';
				for(var i in $.webgis.form_fields.base_flds_6)
				{
					var item = $.webgis.form_fields.base_flds_6[i];
					if(item.id === 'model')
					{
						ret = item.defaultvalue;
						break;
					}
				}
				return ret;
			};
			o['model'] = get_model();
		}
		if($.webgis.select.selected_geojson['properties']['metals'] === undefined)
		{
			$.webgis.select.selected_geojson['properties']['metals'] = [];
		}
		$.webgis.select.selected_geojson['properties']['metals'].push(o);
		var data = [];
		var idx = 1;
		for(var i in $.webgis.select.selected_geojson['properties']['metals'])
		{
			data.push({
				'idx':idx, 
				'type':$.webgis.select.selected_geojson['properties']['metals'][i]['type'],
				'model':$.webgis.select.selected_geojson['properties']['metals'][i]['model']
				});
			idx += 1;
		}
		$.webgis.select.selected_metal_item = undefined;
		$("#listbox_tower_info_metal").ligerListBox().setData(data);
		$('#form_tower_info_metal').empty();
	}
}

function DeleteMetal()
{
	if($.webgis.select.selected_geojson)
	{
		if($.webgis.select.selected_geojson['properties']['metals'] && $.webgis.select.selected_geojson['properties']['metals'].length>0)
		{
			ShowConfirm(null, 500, 200,
				'删除确认',
				'确认删除该金具/附件吗? 删除后还需点击“保存”按钮以便所有人都能看到修改的结果。',
				function () {
					$('#form_tower_info_metal').empty();
					if($.webgis.select.selected_metal_item )
					{
						var o = $.webgis.select.selected_metal_item;
						//console.log(o);
						//console.log($.webgis.select.selected_geojson['properties']['metals']);
						$.webgis.select.selected_geojson['properties']['metals'].splice(o['idx']-1, 1);
						//console.log($.webgis.select.selected_geojson['properties']['metals']);
					}
					var data = [];
					var idx = 1;
					for(var i in $.webgis.select.selected_geojson['properties']['metals'])
					{
						data.push({
							'idx':idx, 
							'type':$.webgis.select.selected_geojson['properties']['metals'][i]['type'],
							'model':$.webgis.select.selected_geojson['properties']['metals'][i]['model']
							});
						idx += 1;
					}
					$.webgis.select.selected_metal_item = undefined;
					$("#listbox_tower_info_metal").ligerListBox().setData(data);
					if(data.length === 0)
					{
						//console.log(data);
						var items = $("#listbox_tower_info_metal").ligerListBox().getSelectedItems();
						//console.log(items);
						$("#listbox_tower_info_metal").ligerListBox().removeItems(items);
					}
					
				},
				function () {
					$('#form_tower_info_metal').empty();
				}
			);
		}
	}
	//if($.webgis.select.selected_geojson)
	//{
		//if($.webgis.select.selected_geojson['properties']['metals'] && $.webgis.select.selected_geojson['properties']['metals'].length>0)
		//{
			//if($.webgis.select.selected_metal_item )
			//{
				//var o = $.webgis.select.selected_metal_item;
				//$.webgis.select.selected_geojson['properties']['metals'].splice(o['idx']-1, 1);
			//}
			//var data = [];
			//var idx = 1;
			//for(var i in $.webgis.select.selected_geojson['properties']['metals'])
			//{
				//data.push({
					//'idx':idx, 
					//'type':$.webgis.select.selected_geojson['properties']['metals'][i]['type'],
					//'model':$.webgis.select.selected_geojson['properties']['metals'][i]['model']
					//});
				//idx += 1;
			//}
			//$.webgis.select.selected_metal_item = undefined;
			//$("#listbox_tower_info_metal").ligerListBox().setData(data);
		//}
	//}
}

function CreateLineNamesSelectOption()
{
	var ret = [];
	for(var k in $.webgis.data.lines)
	{
		ret.push({value:k, label:$.webgis.data.lines[k]['properties']['name']});
	}
	return ret;
}

function OnSelect(viewer, e, selectedEntity)
{
	var clearselcolor = function(){
		if($.webgis.select.prev_selected_obj && $.webgis.select.prev_selected_obj.primitive && $.webgis.select.primitive_material_unselect)
		{
			$.webgis.select.prev_selected_obj.primitive.material = $.webgis.select.primitive_material_unselect;
		}
		if($.webgis.select.prev_selected_obj && $.webgis.select.prev_selected_obj.polyline && $.webgis.select.polyline_material_unselect)
		{
			$.webgis.select.prev_selected_obj.polyline.material = $.webgis.select.polyline_material_unselect;
		}
		if($.webgis.select.prev_selected_obj && $.webgis.select.prev_selected_obj.polygon && $.webgis.select.polygon_material_unselect)
		{
			$.webgis.select.prev_selected_obj.polygon.material = $.webgis.select.polygon_material_unselect;
		}
	};
	clearselcolor();
	$('#btn_edge_save').attr('disabled','disabled');
	if($.webgis.config.map_backend === 'cesium')
	{
		$('#lnglat_indicator').html( '当前用户:' + $.webgis.current_userinfo['displayname'] + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + PickLngLatFromScreen(viewer, e.position));
		//if (Cesium.defined(viewer.selectedEntity)) 
		if (Cesium.defined(selectedEntity)) 
		{
			$.webgis.select.prev_selected_obj = $.webgis.select.selected_obj;
			//$.webgis.select.selected_obj = viewer.selectedEntity;
			$.webgis.select.selected_obj = selectedEntity;
			var id = $.webgis.select.selected_obj.id;
			if (id && id.properties && id.properties.webgis_type === 'edge_dn')
			{
				clearselcolor();
				$.webgis.select.primitive_material_unselect =  $.webgis.select.selected_obj.primitive.material;
				if($.webgis.select.primitive_material_unselect)
				{
					$.webgis.select.selected_obj.primitive.material = 
					//Cesium.Material.fromType('PolylineOutline',{
						//color:	$.webgis.select.primitive_material_unselect.uniforms.color,
						//outlineColor : Cesium.Color.fromCssColorString('rgba(0, 255, 0, 1.0)'),
						//outlineWidth: 1.0
					//});
					//Cesium.Material.fromType('Color', {
						//color : Cesium.Color.fromCssColorString('rgba(0, 255, 0, 1.0)')
					//});
					Cesium.Material.fromType('PolylineArrow', {
						color : Cesium.Color.fromCssColorString('rgba(0, 255, 0, 1.0)')
					});
				}
			}
			else if ($.webgis.select.selected_obj.polyline)
			{
				if($.webgis.select.prev_selected_obj===undefined || $.webgis.select.prev_selected_obj.id != id)
				{
					clearselcolor();
					console.log('selected polyline id=' + id);
					$.webgis.select.polyline_material_unselect = $.webgis.select.selected_obj.polyline.material;
					$.webgis.select.selected_obj.polyline.material = Cesium.ColorMaterialProperty.fromColor(Cesium.Color.fromCssColorString('rgba(0, 255, 255, 1.0)'));
					if($.webgis.data.czmls[id] &&  $.webgis.data.czmls[id]['webgis_type'] == 'polyline_line')
					{
						ShowLineDialog(viewer, id);
					}
				}
			}
			else if ($.webgis.select.selected_obj.polygon)
			{
				if($.webgis.select.prev_selected_obj===undefined || $.webgis.select.prev_selected_obj.id != id)
				{
					clearselcolor();
					console.log('selected polygon id=' + id);
					$.webgis.select.polygon_material_unselect = $.webgis.select.selected_obj.polygon.material;
					$.webgis.select.selected_obj.polygon.material = Cesium.ColorMaterialProperty.fromColor(Cesium.Color.fromCssColorString('rgba(0, 255, 0, 0.3)'));
				}
			}
			else if ($.webgis.select.selected_obj.point)
			{
				clearselcolor();
				//console.log('selected marker id=' + id);
				if($.webgis.select.prev_selected_obj && $.webgis.select.prev_selected_obj.id)
				{
					//console.log('prev selected id=' + $.webgis.select.prev_selected_obj.id);
				}
				if($.webgis.data.czmls[id] && $.webgis.data.czmls[id]['webgis_type'].indexOf('point_')>-1 && $.webgis.data.czmls[id]['webgis_type'] == 'point_tower')
				{
					try{
						//$('#dlg_tower_info').dialog("close");
						$('#dlg_poi_info').dialog("close");
					}catch(e)
					{
					}
				}
				if($.webgis.data.czmls[id] && $.webgis.data.czmls[id]['webgis_type'].indexOf('point_')>-1 && $.webgis.data.czmls[id]['webgis_type'] != 'point_tower')
				{
					try{
						$('#dlg_tower_info').dialog("close");
					}catch(e)
					{
					}
					ShowPoiInfoDialog(viewer, '编辑', 'point', [], id);
				}
				if($.webgis.data.czmls[id] && $.webgis.data.czmls[id]['webgis_type'].indexOf('point_')>-1)
				{
					var webgis_type_title = '';
					if($.webgis.data.czmls[id]['webgis_type'] === 'point_tower') webgis_type_title = '杆塔';
					if($.webgis.data.czmls[id]['webgis_type'] === 'point_dn') webgis_type_title = '配电网';
				}
				if(CheckIsTower(id) && ($.webgis.select.prev_selected_obj===undefined || $.webgis.select.prev_selected_obj.id != id))
				{
					if($.webgis.select.prev_selected_obj && $.webgis.select.prev_selected_obj.id)
					{
						//if(CheckTowerInfoModified())
						if(false)
						{
							
							ShowConfirm(null,500, 200,
								'保存确认',
								'检测到数据被修改，确认保存吗? 确认的话数据将会提交到服务器上，以便所有人都能看到修改的结果。',
								function(){
									SaveTower(viewer);
									ShowTowerInfo(viewer, id);
								},
								function(){
									ShowTowerInfo(viewer, id);
								}
							);
							
						}else{
							ShowTowerInfo(viewer, id);
						}
					}
					else{
						ShowTowerInfo(viewer, id);
					}
				}
				if($.webgis.data.czmls[id]  && $.webgis.select.prev_selected_obj && $.webgis.data.czmls[$.webgis.select.prev_selected_obj.id] && $.webgis.data.czmls[$.webgis.select.prev_selected_obj.id]['webgis_type'] === $.webgis.data.czmls[id]['webgis_type'])
				{
					var edgeexist = CheckSegmentsExist($.webgis.select.prev_selected_obj, $.webgis.select.selected_obj, $.webgis.data.czmls[id]['webgis_type']);
					if(edgeexist)
					{
						$.jGrowl("该两点间该方向已存在连接",{
							life: 2000,
							position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
							theme: 'bubblestylefail',
							glue:'before'
						});
					}
					if($.webgis.config.node_connect_mode && !edgeexist)
					{
						var ring = CheckSegmentsRing($.webgis.select.prev_selected_obj, $.webgis.select.selected_obj);
						if(ring)
						{
							$.jGrowl("不能形成环路",{
								life: 2000,
								position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
								theme: 'bubblestylefail',
								glue:'before'
							});
							
						}else
						{
							$('#btn_edge_save').removeAttr('disabled');
							$('#div_edge_instruction').html($.webgis.data.geojsons[$.webgis.select.prev_selected_obj.id].properties.name + '->' + $.webgis.data.geojsons[id].properties.name);
							var webgis_type;
							if($.webgis.data.czmls[id]['webgis_type'] === 'point_dn') webgis_type = 'edge_dn';
							if($.webgis.data.czmls[id]['webgis_type'] === 'point_tower') webgis_type = 'edge_tower';
							DrawEdgeBetweenTwoNode(viewer, webgis_type, $.webgis.select.prev_selected_obj.id, id, true);
						}
					}
				}
			}
		}
		else{
			clearselcolor();
			ShowGeoTip(false);
			$.webgis.select.prev_selected_obj = $.webgis.select.selected_obj;			
			$.webgis.select.selected_obj = undefined;
		}
	}
	if($.webgis.config.map_backend === 'leaflet')
	{
		$('#lnglat_indicator').html( '当前用户:' + $.webgis.current_userinfo['displayname'] );
		if($.webgis.select.selected_obj && $.webgis.select.selected_obj.id)
		{
			if(typeof $.webgis.select.selected_obj.id === 'string')
			{
				var id = $.webgis.select.selected_obj.id;
				if($.webgis.data.geojsons[id] && $.webgis.data.geojsons[id]['properties'] && $.webgis.data.geojsons[id]['properties']['webgis_type'] == 'point_tower')
				{
					try{
						$('#dlg_poi_info').dialog("close");
					}catch(e)
					{
					}
					if(CheckIsTower(id) && ($.webgis.select.prev_selected_obj===undefined || $.webgis.select.prev_selected_obj.id != id))
					{
						if(!$.webgis.config.node_connect_mode)
						{
							ShowTowerInfo(viewer, id);
						}
					}
				}
				if($.webgis.data.geojsons[id] && $.webgis.data.geojsons[id]['properties'] && $.webgis.data.geojsons[id]['properties']['webgis_type'].indexOf('point_')>-1 && $.webgis.data.geojsons[id]['properties']['webgis_type'] != 'point_tower')
				{
					try{
						$('#dlg_tower_info').dialog("close");
					}catch(e)
					{
					}
					if(!$.webgis.config.node_connect_mode)
					{
						ShowPoiInfoDialog(viewer, '编辑', 'point', [], id);
					}
				}
				if($.webgis.data.geojsons[id]  && $.webgis.select.prev_selected_obj && $.webgis.data.geojsons[$.webgis.select.prev_selected_obj.id] && $.webgis.data.geojsons[$.webgis.select.prev_selected_obj.id]['properties']['webgis_type'] === $.webgis.data.geojsons[id]['properties']['webgis_type'])
				{
					var edgeexist = CheckSegmentsExist($.webgis.select.prev_selected_obj, $.webgis.select.selected_obj);
					if(edgeexist)
					{
						$.jGrowl("该两点间该方向已存在连接",{
							life: 2000,
							position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
							theme: 'bubblestylefail',
							glue:'before'
						});
					}
					
					if($.webgis.config.node_connect_mode && !edgeexist)
					{
						var ring = CheckSegmentsRing($.webgis.select.prev_selected_obj, $.webgis.select.selected_obj);
						if(ring)
						{
							$.jGrowl("不能形成环路",{
								life: 2000,
								position: 'bottom-right', //top-left, top-right, bottom-left, bottom-right, center
								theme: 'bubblestylefail',
								glue:'before'
							});
							
						}else
						{
							$('#btn_edge_save').removeAttr('disabled');
							$('#div_edge_instruction').html($.webgis.data.geojsons[$.webgis.select.prev_selected_obj.id].properties.name + '->' + $.webgis.data.geojsons[id].properties.name);
							var webgis_type;
							if($.webgis.data.geojsons[id]['properties']['webgis_type'] === 'point_dn') webgis_type = 'edge_dn';
							if($.webgis.data.geojsons[id]['properties']['webgis_type'] === 'point_tower') webgis_type = 'edge_tower';
							AddEdgeBetweenTwoNode2D(viewer, webgis_type, $.webgis.select.prev_selected_obj, $.webgis.select.selected_obj, true);
						}
					}
				}
				
				
			}
			else
			{
				$.webgis.select.selected_geojson = $.webgis.select.selected_obj.id;
				//if($.webgis.select.selected_geojson._id === 'tmp_edge')
				//{
					//$.webgis.select.selected_geojson._id = null;
				//}
			}
		}
		
		
	}	

}

function ShowLineDialog(viewer, mode)
{
    $('#dlg_line_info').dialog({
        width: 540,
        height: 700,
        minWidth:200,
        minHeight: 200,
        draggable: true,
        resizable: true, 
        modal: false,
        position:{at: "right center"},
        title:'输电线路工程信息',
        close:function(event, ui){
		},
        show: {
            effect: "slide",
            direction: "right",
            duration: 400
        },
        hide: {
            effect: "slide",
            direction: "right",
            duration: 400
        },
        buttons: [
			{
			    text: "保存",
			    click: function () {
			        if ($('#form_line_info').valid()) {
			            var that = this;
						
						var id = null, text='';
						if($('#fld_line_edit_choose').is(':visible'))
						{
							var arr = $('#line_choose').multipleSelect("getSelects");
							var textarr = $('#line_choose').multipleSelect("getSelects", 'text');
							if(arr.length>0)
							{
								text = '[' + textarr[0] + ']';
								id = arr[0];
							}
						}
						
			            ShowConfirm(null, 500, 200,
							'保存确认',
							'确认保存' + text + '吗? 确认的话数据将会提交到服务器上，以便所有人都能看到修改的结果。',
							function () {
								SaveLine(viewer, id);
							},
							function () {
							    $(that).dialog("close");
							}
						);
			        }
			    }
			},
			{
			    text: "关闭",
			    click: function () {
			        $(this).dialog("close");
			    }
			}
        ]
    });
	var i;
    var list = ['08', '09', '10', '11', '12', '13', '15'];
    var voltagelist = [];
    for (i = 0; i < list.length; i++)
    {
        for (var key in $.webgis.data.codes['voltage_level']) {
            if (key == list[i]) 
			{
                voltagelist.push({ value: key, label: $.webgis.data.codes['voltage_level'][key] });
            }
        }
    }
    list = ['F000', 'A313'];
	var equipment_class = [];
    for (i = 0; i < list.length; i++)
    {
		for (var key in $.webgis.data.codes['equipment_class']) 
		{
            if (key == list[i]) 
			{
				equipment_class.push({ value: key, label: $.webgis.data.codes['equipment_class'][key] });
			}
		}
	}
    list = ['C', 'B', 'D', 'F', 'Q', 'P', 'S'];
	var object_class = []
    for (i = 0; i < list.length; i++)
    {
		for (var key in $.webgis.data.codes['object_class']) 
		{
            if (key == list[i]) 
			{
				object_class.push({ value: key, label: $.webgis.data.codes['object_class'][key] });
			}
		}
	}
	var line_status = [
		{ value: '00', label: '测试' },
		{ value: '20', label: '试运行' },
		{ value: '21', label: '运行' },
		{ value: '40', label: '检修' },
		{ value: '60', label: '故障' },
		{ value: '90', label: '停运' }
	];
    
    var flds = [
		{ display: "线路名称", id: "name", newline: true, type: "text", group: '信息', width: 250, labelwidth: 120, validate: { required: true, minlength: 1 } },
        { display: "管辖长度(km)", id: "manage_length", newline: true, type: "spinner", max: 1000, min: 0, step: 0.1, defaultvalue: 0, group: '信息', width: 200, labelwidth: 140, validate: { number: true,  range: [0, 1000] } },

        { display: "电压等级", id: "voltage", newline: true, type: "select", editor: { data: voltagelist }, defaultvalue: '13', group: '南网分类标准', width: 200, labelwidth: 140},
        { display: "设备类别", id: "category", newline: true, type: "select", defaultvalue: 'F000', editor: { data: equipment_class }, group: '南网分类标准', width: 200, labelwidth: 140},
        { display: "对象类别", id: "object_class", newline: true, type: "select", defaultvalue: 'S', editor: { data: object_class }, group: '南网分类标准', width: 200, labelwidth: 140},

        
        { display: "线路代码", id: "line_code", hide:true, newline: true, type: "text", group: '建设', width: 250, labelwidth: 120 },
        { display: "线路起点", id: "start_point", newline: true, type: "text", group: '建设', width: 250, labelwidth: 120 }, 
        { display: "线路终点", id: "end_point", newline: true, type: "text", group: '建设', width: 250, labelwidth: 120 },
        { display: "设计单位", id: "designer", newline: true, type: "text",  group: '建设', width: 250, labelwidth: 120 },
        { display: "监理单位", id: "supervisor", newline: true, type: "text", group: '建设', width: 250, labelwidth: 120 },
        { display: "运行单位", id: "operator", newline: true, type: "text", group: '建设', width: 250, labelwidth: 120 },
        { display: "所属单位", id: "owner", newline: true, type: "text", group: '建设', width: 250, labelwidth: 120 },
        { display: "运维单位", id: "maintenace", newline: true, type: "text", group: '建设', width: 250, labelwidth: 120 },
        { display: "建设单位", id: "investor", newline: true, type: "text", group: '建设', width: 250, labelwidth: 120 },
        { display: "施工单位", id: "constructor", newline: true, type: "text", group: '建设', width: 250, labelwidth: 120 },
        
        { display: "维护人", id: "responsible", hide:true, newline: true, type: "text", group: '运维', width: 250, labelwidth: 120 },
        { display: "维护班组", id: "team", newline: true, type: "text", group: '运维', width: 250, labelwidth: 120 },
        { display: "线路状态", id: "status", newline: true, type: "select", defaultvalue: '00', editor: { data: line_status }, group: '运维', width: 250, labelwidth: 120 },
        
        { display: "投产日期", id: "production_date", hide:true, newline: true, type: "date", group: '日期', width: 200, labelwidth: 120 },
        { display: "投运日期", id: "finish_date", newline: true, type: "date", group: '日期', width: 200, labelwidth: 120 },
        { display: "退役日期", id: "decease_date", newline: true, type: "date", group: '日期', width: 200, labelwidth: 120 }
    ];
	if(mode === 'edit')
	{
		$('#fld_line_edit_choose').css('display', 'block');
		$('#line_choose').empty();
		for(var k in $.webgis.data.lines)
		{
			$('#line_choose').append('<option value="' + k + '">' + $.webgis.data.lines[k]['properties']['name'] + '</option>');
		}
		
		var select = $('#line_choose').multipleSelect({
			selectAll: false,
			selectAllText: '全部',
			selectAllDelimiter: ['(', ')'],
			allSelected: '(全部)',
			countSelected: '(选择#个,共%个)',
			noMatchesFound: '(无匹配)',
			single: true,
			position: 'bottom',
			onClick:function(view){
				if(view.checked)
				{
					//console.log(view.value);
					var arr = $('#line_choose').multipleSelect("getSelects");
					if($.webgis.data.lines[view.value])
					{
						$("#form_line_info").webgisform('clear');
						$("#form_line_info").webgisform('setdata', $.webgis.data.lines[view.value]['properties']);
					}
				}
			},
			styler: function(value) {
				return 'color: #00FF00;background: #000000 url(/css/black-green-theme/images/ui-bg_diagonals-small_50_000000_40x40.png) 100% 100% repeat;';
			}
		});
	}
	else
	{
		$('#fld_line_edit_choose').css('display', 'none');
	}
	
    $("#form_line_info").webgisform(flds, {
        //divorspan: "div",
        prefix: "form_line_info_",
        maxwidth: 420
        //margin:10,
        //groupmargin:10
    });
	//if(id && $.webgis.data.lines[id])
	//{
		//$("#form_line_info").webgisform('setdata', $.webgis.data.lines[id]['properties']);
	//}
	$('#tabs_line_info').tabs({ 
		collapsible: false,
		active: 0,
		beforeActivate: function( event, ui ) {
			var title = ui.newTab.context.innerText;
			if(title == '基础信息')
			{
			}
			if(title == '照片文档')
			{
				var arr = $('#line_choose').multipleSelect("getSelects");
				//console.log(arr);
				if(arr.length>0)
				{
					var id = arr[0];
					ShowProgressBar(true, 670, 200, '载入中', '正在载入，请稍候...');
					CreateFileBrowser('line_info_photo', 450, 450, ['jpg','jpeg','png', 'bmp', 'gif', 'doc', 'xls', 'xlsx', 'docx', 'pdf'], 'network', id);
				}else
				{
					ShowMessage(null, 400, 200, '无法获取图片数据', '无法获取图片数据,请先选择输电线路.');
				}
			}
		}
	});

}

function GetParamsFromUrl() {
	var ret = {};
	if(location.search.length>0)
	{
		var decrypted = CryptoJS.AES.decrypt(location.search.substr(1),  $.webgis.config.encrypt_key);
		var s = decrypted.toString(CryptoJS.enc.Utf8);
		s = decodeURIComponent(s);
		ret = JSON.parse(s);
	}
	return ret;
}


function CheckPermission(funcname)
{
	if($.webgis.current_userinfo['username'] === undefined)
	{
		return true;
	}
	if($.webgis.current_userinfo['username'] === 'admin')
	{
		return true;
	}
	var ret = false;
	if($.webgis.data.sysrole.indexOf(funcname)>-1)
	{
		ret = true;
	}
	if(ret === false)
	{
		var s = '';
		for(var i in $.webgis.mapping.role_functions)
		{
			if($.webgis.mapping.role_functions[i]['value'] === funcname)
			{
				s = $.webgis.mapping.role_functions[i]['label'];
				break;
			}
		}
		ShowMessage(null, 400, 200, '权限检查', '当前登录用户[' + $.webgis.current_userinfo['displayname'] + ']无此操作权限:[' + s + ']');
	}
	return ret;
}
