var g_drawhelper;
var g_selected_obj_id;
var g_prev_selected_id;
var g_prev_selected_pos;
var g_czmls = {};
//var g_geojson_towers = {"type": "FeatureCollection","features": []};
var g_geojsons = {};
var g_lines = {};
var g_segments = [];
var g_gltf_models = {};
var g_dlg_tower_info;
var g_contextmenu_metal;
var g_selected_metal_item;
var g_geometry_segments = [];
var g_geometry_lines = {};
var g_use_catenary = true;
var g_validates = {};
var g_models = [];
var g_is_tower_focus = false;
var g_primitive_appearance;
var g_buffers = {};
var g_borders = {};


$(function() {
	ShowProgressBar(true, 670, 200, '载入中', '正在载入，请稍候...');
	//if(true) return;
	var viewer = InitCesiumViewer();
	$.viewer = viewer;
	InitWebGISFormDefinition();
	InitDrawHelper(viewer);
	g_drawhelper.close();
	InitPoiInfoDialog();
	InitTowerInfoDialog();
	//$(window).on('message',function(e) {
		////console.log('recv:' + text);
		//var text = e.originalEvent.data;
		//console.log('recv:' + text);
		//var obj = JSON.parse(text);
		//console.log(obj);
		
	//});
	InitSearchBox(viewer);
	InitToolPanel(viewer);
	InitModelList(viewer);
	
	//var line_name = '七罗I回';
	var line_name = '永发I回线';
	LoadTowerByLineName(viewer, g_db_name,  line_name);
	//line_name = '永发II回线';
	//LoadTowerByLineName(viewer, g_db_name,  line_name);
	LoadSegments(viewer, g_db_name);
	LoadModelsList(g_db_name);
	//LoadBorder(viewer, g_db_name, {'properties.name':'云南省'});
	//LoadBorder(viewer, g_db_name, {'properties.type':'cityborder'});
	//LoadBorder(viewer, g_db_name, {'properties.type':'countyborder'});
	//GetZfromXY(103.036471, 25.599314, function(alt){
		//console.log('103.036471, 25.599314 alt=' + alt);
	//});
	//GetZfromXY(102.803284, 26.555857, function(alt){
		//console.log('102.803284, 26.555857 alt=' + alt);
	//});
	//GetZListfromXYList([{lng:103.036471, lat:25.599314},{lng:102.803284, lat:26.555857}], function(list){
		//console.log(list);
	//});	
	
});

function InitWebGISFormDefinition()
{
	var methods = 
	{
		init : function(fields, options) 
		{
			if(!fields) return this;
			this.fields = fields;
			this.groups = [];
			this.options = $.extend({}, $.fn.webgisform.defaults, options);
			this.empty();
			
			for(var i in fields)
			{
				var fld = fields[i];
				if(fld.type == 'hidden')
				{
					this.append('<input type="hidden" id="' + fld.id + '">');
				}
				if(fld.group)
				{
					if(this.groups.indexOf(fld.group) < 0)
					{
						this.groups.push(fld.group);
					}
				}
			}
			
			
			for(var j in this.groups)
			{
				var group = this.groups[j];
				var uid = $.uuid();
				var g = this.append('<fieldset id="fieldset_' + uid + '" style="color:#00FF00;border:1px solid #00FF00;margin:' + this.options.groupmargin + 'px;"><legend style="font-weight:bolder;color:#00FF00;">' + group + '</legend>');
				this.append('</fieldset>');
				this.append('<p></p>');
				
				for(var i in fields)
				{
					var fld = fields[i];
					if(fld.labelwidth) this.options.labelwidth = fld.labelwidth;
					var newline = "float:left;";
					if(fld.newline == false) newline = "";
					var validate = '';
					if(fld.validate)
					{
						validate = '<span style="color:#FF0000">*</span>';
					}
					if(fld.type == 'spinner' && fld.group == group)
					{
						$('#' + 'fieldset_' + uid).append('<div style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fld.id + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input  style="width:' + fld.width + 'px;" id="' + fld.id + '" name="' + fld.id + '">' + validate + '</div>');
						var spin = 	$('#' + fld.id).spinner({
							step: fld.step,
							max:fld.max,
							min:fld.min,
							change:fld.change,
							spin:fld.spin
						});
					}
					if(fld.type == 'geographic' && fld.group == group)
					{
						$('#' + 'fieldset_' + uid).append('<div style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fld.id + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input  style="width:' + fld.width + 'px;" id="' + fld.id + '" name="' + fld.id + '">' + validate + '</div>');
						var spin = 	$('#' + fld.id).spinner({
							step: 0.00001,
							max:179.0,
							min:-179.0,
							change: fld.change,
							spin: fld.spin
						});
					}
					if(fld.type == 'text' && fld.group == group)
					{
						var readonly = '';
						if(fld.editor && fld.editor.readonly == true)
						{
							readonly = ' readonly="readonly"';
						}
						$('#' + 'fieldset_' + uid).append('<div style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fld.id + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input type="text" class="ui-widget" style="width:' + fld.width + 'px;" id="' + fld.id + '" name="' + fld.id + '" ' + readonly + '>' + validate + '</div>');
					}
					if(fld.type == 'select' && fld.group == group)
					{
						var source = [];
						if(fld.editor && fld.editor.data) source = fld.editor.data;
						$('#' + 'fieldset_' + uid).append('<div style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fld.id + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><select  style="width:' + fld.width + 'px;" id="' + fld.id + '" name="' + fld.id + '"></select>' + validate + '</div>');
						for(var ii in source)
						{
							$('#' + fld.id).append('<option value="' + source[ii]['value'] + '">' + source[ii]['label'] + '</option>');
						}
						//$('#' + 'fieldset_' + uid).append('<div style="margin:' + margin + 'px;' + newline + '"><label for="' + fld.id + '" style="display:inline-block;text-align:right;width:' + labelwidth + 'px;">' + fld.display + ':' + '</label><input type="text"  style="width:' + fld.width + 'px;" id="' + fld.id + '" name="' + fld.id + '">' + validate + '</div>');
						var auto = $('#' + fld.id).autocomplete({
							//appendTo:'#' + fld.id,
							//position: { my: "left top", at: "left bottom", collision: "none" },
							autoFocus: false,
							source:source
						});
						
					}
					
				}
			}
			
			var fields = this.fields;
			for(var i in fields)
			{
				var fld = fields[i];
				if(fld.validate)
				{
					if($('input[name="' + fld.id + '"]').length>0)
					{
						$('input[name="' + fld.id + '"]').rules('add',fld.validate);
					}
					if($('select[name="' + fld.id + '"]').length>0)
					{
						$('select[name="' + fld.id + '"]').rules('add',fld.validate);
					}
				}
			}
			return this;
		},
		setdata : function(data, prefix)
		{
			for(var k in data)
			{
				if(prefix)
				{
					this.find('#' + prefix + k).val(data[k]);
				}
				else
				{
					this.find('#' + k).val(data[k]);
				}
			}
			return this;
		}
    };	
	$.fn.webgisform = function(fields, options) 
	{
		if ( methods[fields] ) {
			return methods[ fields ].apply( this, Array.prototype.slice.call( arguments, 1 ));
		} else if ( typeof fields === 'object' || ! fields ) {
			return methods.init.apply( this, arguments );
		} else {
			$.error( 'Method ' +  fields + ' does not exist on $.webgisform');
        }		
		
	};
	$.fn.webgisform.defaults = {
		labelwidth : 90,
		margin : 10.0/2,
		groupmargin : 18.0/2
	};
}

function InitCesiumViewer()
{
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
	//providerViewModels.push(new Cesium.ProviderViewModel({
				//name : 'YNCFT',
				//iconUrl : 'img/wmts-map.png',
				//tooltip : 'YNCFT',
				//creationFunction : function() {
					//return new ArcgisTileImageryProvider({
						//url : g_host + 'arcgistile',
						//is_esri:true
					//});
				//}
			//}));
	providerViewModels.push(new Cesium.ProviderViewModel({
				name : 'YN_SAT',
				iconUrl : 'img/wmts-sat.png',
				tooltip : 'YN_SAT',
				creationFunction : function() {
					return new Cesium.ArcGisMapServerImageryProvider({
						url : 'http://localhost:6080/arcgis/rest/services/YN_SAT/ImageServer'
						//usePreCachedTilesIfAvailable:false
					});
				}
			}));
	providerViewModels.push(new Cesium.ProviderViewModel({
				name : '卫星图',
				iconUrl : 'img/wmts-sat.png',
				tooltip : '卫星图',
				creationFunction : function() {
					return new WMTSImageryProvider({
						url :  g_host + 'wmts',
						imageType:'google_sat'
					});
				}
			}));
	providerViewModels.push(new Cesium.ProviderViewModel({
				name : '地图',
				iconUrl : 'img/wmts-map.png',
				tooltip : '地图',
				creationFunction : function() {
					return new WMTSImageryProvider({
						url :  g_host + 'wmts',
						//url :  "http://cf-storage:88/" + 'wmts',
						imageType:'google_map'
					});
				}
			}));
	//providerViewModels.push(new Cesium.ProviderViewModel({
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
		name : 'STK 世界地形',
		iconUrl : Cesium.buildModuleUrl('Widgets/Images/TerrainProviders/STK.png'),
		tooltip : 'High-resolution, mesh-based terrain for the entire globe. Free for use on the Internet. Closed-network options are available.\nhttp://www.agi.com',
		creationFunction : function() {
			return new Cesium.CesiumTerrainProvider({
				url : '//cesiumjs.org/stk-terrain/tilesets/world/tiles',
				credit : 'Terrain data courtesy Analytical Graphics, Inc.'
			});
		}
	}));

	terrainProviderViewModels.push(new Cesium.ProviderViewModel({
		name : 'ASTER-30 GDEM 中国云南',
		iconUrl : Cesium.buildModuleUrl('/img/aster-gdem.png'),
		tooltip : 'ASTER - 30 中国云南',
		creationFunction : function() {
			return new Cesium.CesiumTerrainProvider({
				url : "http://cf-storage:88/" + "terrain",
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
	
	var viewer = new Cesium.Viewer('cesiumContainer',{
		animation:false,
		baseLayerPicker:true,
		geocoder:false,
		timeline:false,
		selectionIndicator:true,
		sceneModePicker:true,
		navigationInstructionsInitiallyVisible:false,
		infoBox:true,
		imageryProviderViewModels:providerViewModels,
		terrainProviderViewModels:terrainProviderViewModels
		//terrainProvider:new Cesium.CesiumTerrainProvider({
			////url: g_host + "terrain"
			//url: "http://cf-storage:88/" + "terrain"
		//})
	});
	TranslateToCN();
	//viewer.extend(Cesium.viewerDynamicObjectMixin);
	TowerInfoMixin(viewer);
	//viewer.extend(Cesium.viewerCesiumInspectorMixin);

    //viewer.scene.globe.depthTestAgainstTerrain = false;
	
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
	return viewer;
}

function InitDrawHelper(viewer)
{
	g_drawhelper = new DrawHelper(viewer, 'drawhelpertoolbar');
	var toolbar = g_drawhelper.addToolbar($('#' + g_drawhelper.toolbar_container_id)[0], {
		buttons: ['marker', 'polyline', 'polygon', 'circle', 'extent']
	});
	
	
    var drawHelperCoverAreaMaterial = Cesium.Material.fromType('Color', {
		color : new Cesium.Color(1.0, 1.0, 0.0, 0.5)
	});
	
	
	toolbar.addListener('markerCreated', function(event) {
		console.log('Marker created at ' + event.position.toString());
		// create one common billboard collection for all billboards
		var b = new Cesium.BillboardCollection();
		//var a = viewer.scene.context.createTextureAtlas();
		var a = new Cesium.TextureAtlas({scene:viewer.scene});
		b.textureAtlas = a;
		viewer.scene.primitives.add(b);
		g_drawhelper.addPrimitive(b);
		var image = new Image();
		image.onload = function() {
			a.addImage(image);
		};
		image.src = 'img/location_marker.png';
		var billboard = b.add({
			show : true,
			position : event.position,
			pixelOffset : new Cesium.Cartesian2(0, 0),
			eyeOffset : new Cesium.Cartesian3(0.0, 0.0, 0.0),
			horizontalOrigin : Cesium.HorizontalOrigin.CENTER,
			verticalOrigin : Cesium.VerticalOrigin.CENTER,
			scale : 0.15,
			imageIndex : 0,
			color : new Cesium.Color(1.0, 1.0, 1.0, 1.0)
		});
		//billboard.setEditable();
		ShowPOIDialog(viewer, 'point', event.position);
	});
	toolbar.addListener('polylineCreated', function(event) {
		console.log('Polyline created with ' + event.positions.length + ' points');
		var polyline = new DrawHelper.PolylinePrimitive({
			positions: event.positions,
			width: 5,
			geodesic: true
		});
		viewer.scene.primitives.add(polyline);
		g_drawhelper.addPrimitive(polyline);
		//polyline.setEditable();
		//polyline.addListener('onEdited', function(event) {
			//console.log('Polyline edited, ' + event.positions.length + ' points');
		//});

	});
	toolbar.addListener('polygonCreated', function(event) {
		console.log('Polygon created with ' + event.positions.length + ' points');
		var polygon = new DrawHelper.PolygonPrimitive({
			positions: event.positions,
			material : drawHelperCoverAreaMaterial
		});
		viewer.scene.primitives.add(polygon);
		g_drawhelper.addPrimitive(polygon);
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
		g_drawhelper.addPrimitive(circle);
		//circle.setEditable();
		//circle.addListener('onEdited', function(event) {
			//console.log('Circle edited: radius is ' + event.radius.toFixed(1) + ' meters');
		//});
	});
	toolbar.addListener('extentCreated', function(event) {
		var extent = event.extent;
		console.log('Extent created (N: ' + extent.north.toFixed(3) + ', E: ' + extent.east.toFixed(3) + ', S: ' + extent.south.toFixed(3) + ', W: ' + extent.west.toFixed(3) + ')');
		var extentPrimitive = new DrawHelper.ExtentPrimitive({
			extent: extent,
			material: drawHelperCoverAreaMaterial
		});
		viewer.scene.primitives.add(extentPrimitive);
		g_drawhelper.addPrimitive(extentPrimitive);
		//extentPrimitive.setEditable();
		//extentPrimitive.addListener('onEdited', function(event) {
			//console.log('Extent edited: extent is (N: ' + event.extent.north.toFixed(3) + ', E: ' + event.extent.east.toFixed(3) + ', S: ' + event.extent.south.toFixed(3) + ', W: ' + event.extent.west.toFixed(3) + ')');
		//});
	});

}
function InitPoiInfoDialog()
{
	g_validates['form_poi_info'] = $('#form_poi_info' ).validate({
		debug:true,
		errorElement:'div'
	});

}
function InitTowerInfoDialog()
{
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
	g_validates['form_tower_info_base'] = $('#form_tower_info_base' ).validate({
		debug:true,
		errorElement:'div'
	});
	g_validates['form_tower_info_metal'] = $('#form_tower_info_metal' ).validate({
		debug:true,
		errorElement:'div'
	});

}
function InitToolPanel(viewer)
{
	$('#control_toolpanel_kmgd').css('display', 'none');
	$('#control_toolpanel_kmgd_handle').on( 'mouseenter', function(e){
		$('#control_toolpanel_kmgd').show('slide',{}, 400, function(){
			$(e.target).css('display','none');
		});
	});
	$('#control_toolpanel_kmgd').on( 'mouseleave', function(e){
		$('#control_toolpanel_kmgd').hide('slide',{}, 400, function(){
			$('#control_toolpanel_kmgd_handle').css('display','block');
		});
	});
	$( "#accordion_tools" ).accordion({ active: 0 });
	
	$('#chb_show_label').on('click', function(){
		if($(this).is(':checked'))
		{
			console.log('turn on label');
			ReloadCzmlDataSource(viewer, g_zaware, true);
		}else
		{
			console.log('turn off label');
			ReloadCzmlDataSource(viewer, g_zaware, false);
		}
	});
	
	$('#but_add_poi').button({label:'添加兴趣点'});
	$('#but_add_poi').on('click', function(){
		if(g_drawhelper.isVisible())
		{
			g_drawhelper.close();
		}
		else
		{
			g_drawhelper.show();
		}
	});
}
function TranslateToCN()
{
	$($('.cesium-baseLayerPicker-sectionTitle')[0]).html('地表图源');
	//$($('.cesium-baseLayerPicker-sectionTitle')[0]).attr('imgtype', 'imagery');
	$($('.cesium-baseLayerPicker-sectionTitle')[1]).html('3D地型数据源');
	//$($('.cesium-baseLayerPicker-sectionTitle')[1]).attr('imgtype', 'terrain');
	$('.cesium-navigation-help-pan').html('平移');
	$('.cesium-navigation-help-pan').siblings().html('左键点击 + 拖动');
	$('.cesium-navigation-help-zoom').html('缩放');
	$($('.cesium-navigation-help-zoom').siblings()[0]).html('右键点击 + 拖动, 或');
	$($('.cesium-navigation-help-zoom').siblings()[1]).html('鼠标滚轮');
	$('.cesium-navigation-help-rotate').html('视角旋转');
	$($('.cesium-navigation-help-rotate').siblings()[0]).html('中键点击 + 拖动, 或');
	$($('.cesium-navigation-help-rotate').siblings()[1]).html('CTRL + 左键点击 + 拖动');
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
			$(e.target).find('a').html('>>显示列表');
			$('#tower_info_model_list').css('display', 'none');
			$('#tower_info_model').find('iframe').css('width', '99%');
		}
		else
		{
			$(e.target).find('a').html('<<隐藏列表');
			$('#tower_info_model_list').css('display', 'block');
			$('#tower_info_model').find('iframe').css('width', '79%');
		}
	});
	
	$('#tower_info_model_list_filter').on('keyup', function(e){
		var text = $(e.target).val();
		FilterModelList(text);
	});
}
function InitSearchBox(viewer)
{
	$('#button_search_clear').on( 'click', function(){
		$('#input_search').val('');
		$('#text_search_waiting').css('display','block');
		$('#text_search_waiting').html('输入关键字拼音首字母');
		$('#input_search').focus();
	});
	$( "#input_search" ).on('keyup',function(e){
		if($(e.target).val().length > 0)
		{
			$('#text_search_waiting').css('display','none');
		}
	});
	$( "#input_search" ).autocomplete({
		autoFocus:true,
		minLength:2,
		delay: 500,
		_resizeMenu: function() {
			this.menu.element.outerHeight( 500 );
		},		
		source:function(request,  response)
		{
			var py_cond = {'db':g_db_name, 'collection':'*', 'action':'pinyinsearch', 'data':{'py':request.term}};
			$('#text_search_waiting').css('display','block');
			$('#text_search_waiting').html('正在查询，请稍候...');
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
			//console.log(ui.item.geojson);
			if(ui.item.geojson && ui.item.geojson.geometry && ui.item.geojson.geometry.type == 'Point')
			{
				FlyToPoint(viewer, ui.item.pos[0], ui.item.pos[1], 2000, 1.05, 4000);
				ShowSearchResult(viewer, ui.item.geojson);
			}
			else if(ui.item.geojson && ui.item.geojson.properties && ui.item.geojson.properties.category && ui.item.geojson.properties.category == '架空线')
			{
				//var line_cond = {'db':g_db_name, 'collection':'lines', 'properties.line_name':line_name};
				if(ui.item.geojson.properties.line_name)
				{
					ShowProgressBar(true, 670, 200, '载入中', '正在载入，请稍候...');
					LoadTowerByLineName(viewer, g_db_name, ui.item.geojson.properties.line_name);
				}
			}
		}
	});
	$('#button_search').on( 'click', function(){
			if($('#input_search').css('display') == 'none')
			{
				$('#input_search').show('slide',{}, 500, function(){
					$('#button_search_clear').css('display','block');
					$('#text_search_waiting').css('display','block');
					$('#input_search').focus();
				});
				$('#button_search').css('background-color', '#00FF00');
				
			}else
			{
				$('#input_search').hide('slide',{}, 500, function(){
					$('#button_search_clear').css('display','none');
					$('#text_search_waiting').css('display','none');
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
				ReloadCzmlDataSource(viewer, g_zaware);
			}
		}
	}
}

function ShowPOIDialog(viewer, type, positions)
{
	
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

//function GetLineIdFromLineName(line_name)
//{
	//var ret = null;
	//for(var i in g_lines)
	//{
		//if(g_lines[i]['properties']['line_name'] == line_name)
		//{
			//ret = g_lines[i]['_id'];
			//break;
		//}
	//}
	//return ret;
//}

function FilterModelList(str)
{
	try{
		$('#tower_info_model_list_selectable').selectable("destroy");
		$('#tower_info_model_list_selectable').empty();
	}catch(e)
	{
	}
	//console.log('str=' + str + ', len=' + g_models.length);
	for(var i in g_models)
	{
		if(str.length > 0)
		{
			if(g_models[i].toLowerCase().indexOf(str.toLowerCase())>-1)
			{
				$('#tower_info_model_list_selectable').append('<li class="ui-widget-content1">' + g_models[i] + '</li>');
			}
		}else{
			$('#tower_info_model_list_selectable').append('<li class="ui-widget-content1">' + g_models[i] + '</li>');
		}
	}
	$("#tower_info_model_list_selectable").selectable({
		selected: function( event, ui ) {
			var model_code_height = $(ui.selected).html();
			//var id = $('input[id="tower_baseinfo_id"]').val();
			//var tower = GetTowerInfoByTowerId(id);
			var url = GetModelUrl(model_code_height);
			if(url.length>0)
			{
				var iframe = $('#tower_info_model').find('iframe');
				var obj = {};
				obj['url'] = '/' + url;
				//obj['data'] = {};
				//obj['tower_id'] = id;
				//obj['denomi_height'] = tower['properties']['denomi_height'];
				var json = encodeURIComponent(JSON.stringify(obj));
				iframe.attr('src', g_host + 'threejs/editor/index.html?' + json);
			}
			
			
			
			
		},
		selecting: function( event, ui ) {
			if( $(".ui-selected, .ui-selecting").length > 1){
                  $(ui.selecting).removeClass("ui-selecting");
            }
		}
	});
}

function LoadBorder(viewer, db_name, condition)
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
					g_geojsons[data[i]['_id']] = data[i];
					//var dataSource = new Cesium.GeoJsonDataSource();
					//dataSource.load(data[0]);
					//dataSource.dsname = 'geojson';
					//viewer.dataSources.add(dataSource);
				}
				ReloadBorders(viewer, false);
			}
			ShowProgressBar(false);
	});
}

function RemoveBorders(viewer)
{
	var l = [];
	for(var k in g_borders)
	{
		l.push(k);
	}
	for(var i in l)
	{
		viewer.scene.primitives.remove(g_borders[l[i]]);
		delete g_borders[l[i]];
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
	for(var k in g_geojsons)
	{
		if(!forcereload)
		{
			if(g_borders[k])
			{
				continue;
			}
		}
		//console.log('load ' + k);
		var g = g_geojsons[k];
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
				
			for(var i=0; i < arr.length; i=i+5)
			{
				var x = arr[i][0],
					y = arr[i][1],
					z = 6000;
				//if(!g_zaware) z = 3000;
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
				g_borders[k] = primitive;
			}
			
		}
	}
	FlyToExtent(viewer, extent['west'], extent['south'], extent['east'], extent['north']);
}

function LoadSegments(viewer, db_name)
{
	var segs_cond = {'db':db_name, 'collection':'segments'};
	MongoFind( segs_cond, 
		function(data){
			g_segments = data;
			ShowProgressBar(false);
	});
}
function LoadModelsList(db_name)
{
	var cond = {'db':db_name, 'collection':'-', 'action':'modelslist', 'data':{}};
	MongoFind( cond, 
		function(data){
			g_models = data;
			//console.log(g_models);
	});
}
function GetExtentByCzml()
{
	var ret;
	if(g_czmls)
	{
		ret = {'west':179, 'east':-179, 'south':89, 'north':-89};
		for(var k in g_czmls)
		{
			var pos = g_czmls[k]['position']['cartographicDegrees'];
			if (pos[0] < ret['west']) ret['west'] = pos[0];
			if (pos[0] > ret['east']) ret['east'] = pos[0];
			if (pos[1] < ret['south']) ret['south'] = pos[1];
			if (pos[1] > ret['north']) ret['north'] = pos[1];
		}
	}
	return ret;
}
function LoadTowerByLineName(viewer, db_name,  line_name)
{
	var geo_cond = {'db':db_name, 'collection':'mongo_get_towers_by_line_name', 'properties.line_name':line_name};
	var line_cond = {'db':db_name, 'collection':'lines', 'properties.line_name':line_name};
	//var ext_cond = {'db':db_name, 'collection':'mongo_get_towers_by_line_name','get_extext':true, 'properties.line_name':line_name};
	
	MongoFind( geo_cond, 
		function(data){
			ShowProgressBar(false);
			//var ddd = [];
			for(var i in data)
			{
				if(!g_geojsons[data[i]['_id']])
				{
					g_geojsons[data[i]['_id']] = data[i];
				}
				//var cz = CreateTowerCzmlFromGeojson(data[i]);
				if(!g_czmls[data[i]['_id']])
				{
					g_czmls[data[i]['_id']] = CreateTowerCzmlFromGeojson(data[i]);
					//arr.push(cz);
				}
				//ddd.push({lng:data[i]['geometry']['coordinates'][0], lat:data[i]['geometry']['coordinates'][1]});
			}
			//GetZListfromXYList(ddd,function(dd){
				//console.log(dd);
			//});
			//viewer.dataSources.removeAll();
			ReloadCzmlDataSource(viewer, g_zaware);
			var extent = GetExtentByCzml();
			console.log(extent);
			FlyToExtent(viewer, extent['west'], extent['south'], extent['east'], extent['north']);
			
			MongoFind( line_cond, 
				function(linedatas){
					if(linedatas.length>0)
					{
						g_lines[linedatas[0]['_id']] = linedatas[0];
						var color = '#FF0000';
						if(linedatas[0].properties.voltage == '13')
						{
							color = '#FF0000';
						}
						if(linedatas[0].properties.voltage == '15')
						{
							color = '#0000FF';
						}
						DrawLineModelByLine(viewer, linedatas[0], 4.0, color);
						//DrawBufferOfLine(viewer, linedatas[0], 5000, 3000, '#00FF00', 0.2);
					}
			});
	});
				
				
			//var line_id = GetLineIdFromLineName(line_name);
			//if(line_id)
			//{
				//MongoFind( ext_cond, 
					//function(data){
						//g_view_extent = data;
						//FlyToExtent(viewer, g_view_extent['west'], g_view_extent['south'], g_view_extent['east'], g_view_extent['north']);
						//console.log(g_view_extent);
				//});
}


function GetIndexCzmlDataSources(viewer)
{
	var ret = -1;
	for(var i = 0; i < viewer.dataSources.length; i++)
	{
		var ds = viewer.dataSources.get(i);
		//console.log('ds.name=' + ds.name);
		if(ds.dsname == 'czml')
		{
			viewer.dataSources.remove(ds);
			ret = i;
			break;
		}
	}
	return ret;
}
function GetCzmlDataSources(viewer)
{
	var ret;
	for(var i = 0; i < viewer.dataSources.length; i++)
	{
		var ds = viewer.dataSources.get(i);
		if(ds.dsname == 'czml')
		{
			ret = ds;
			break;
		}
	}
	return ret;
}
function ReloadCzmlDataSource(viewer, z_aware, show_label)
{
	var ellipsoid = viewer.scene.globe.ellipsoid;
	//var idx = GetIndexCzmlDataSources(viewer);
	//while(idx > -1)
	//{
		//viewer.dataSources.remove(idx);
		//idx = GetIndexCzmlDataSources(viewer);
	//}
	var arr = [];
	var pos;
	//console.log('z_aware=' + z_aware);
	for(var k in g_czmls)
	{
		var obj =  $.extend(true, {}, g_czmls[k]);
		if(!z_aware)
		{
			obj['position']['cartographicDegrees'] = [g_czmls[k]['position']['cartographicDegrees'][0],  g_czmls[k]['position']['cartographicDegrees'][1], 0];
		}
		if(!show_label)
		{
			delete obj['label'];
		}
		arr.push(obj);
		if(viewer.selectedObject)
		{
			if(obj['id'] === viewer.selectedObject.id)
			{
				pos = obj['position']['cartographicDegrees'];
				//console.log(pos);
			}
		}
	}
	if(g_czmls === {})
	{
		viewer.selectedObject = undefined;
		g_selected_obj_id = undefined;
	}
	//var dataSource = new Cesium.CzmlDataSource();
	//dataSource.load(arr);
	//dataSource.dsname = 'czml';
	//viewer.dataSources.add(dataSource);
	//if(viewer.selectedObject && pos)
	//{
		//viewer.selectedObject.position._value = ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(pos[0], pos[1], pos[2]));
	//}
	var dataSource = GetCzmlDataSources(viewer);
	if(dataSource)
	{
		dataSource.load(arr);
		if(viewer.selectedObject && pos)
		{
			viewer.selectedObject.position._value = ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(pos[0], pos[1], pos[2]));
		}
	}else
	{
		dataSource = new Cesium.CzmlDataSource();
		dataSource.load(arr);
		dataSource.dsname = 'czml';
		viewer.dataSources.add(dataSource);
	}
}
function LookAtTarget(viewer, id, zoom_factor)
{
	var scene = viewer.scene;
	//scene.camera.controller.lookAt(scene.camera.position, target, scene.camera.up);
	var ellipsoid = scene.globe.ellipsoid;
	
	if(g_geojsons[id])
	{
		var tower = g_geojsons[id];
		var x = tower['geometry']['coordinates'][0];
		var y = tower['geometry']['coordinates'][1];
		var z = tower['properties']['geo_z'];
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
	var scene = viewer.scene;
	var destination = Cesium.Cartographic.fromDegrees(x,  y,  z * factor);
	var flight = Cesium.CameraFlightPath.createAnimationCartographic(scene, {
		destination : destination,
		duration	:duration
	});
	scene.animations.add(flight);
}

function FlyToPointCart3(viewer, pos, duration)
{
	var scene = viewer.scene;
	//var destination = scene.globe.ellipsoid.cartesianToCartographic(cart3);
	var flight = Cesium.CameraFlightPath.createAnimationCartographic(scene, {
		destination	:	pos,
		duration	:	duration
		//up			:	scene.camera.up,
		//direction	:	scene.camera.direction
	});
	scene.animations.add(flight);
}

function FlyToExtent(viewer, west, south, east, north)
{
	var scene = viewer.scene;
	var extent = Cesium.Rectangle.fromDegrees(west, south, east, north);
	var flight = Cesium.CameraFlightPath.createAnimationRectangle(scene, {
		destination : extent
	});
	scene.animations.add(flight);
	//scene.camera.viewRectangle(extent, scene.globe.ellipsoid);
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
	var ellipsoid = scene.globe.ellipsoid;
	
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
				if(!g_zaware) height = 0;
				if($.isNumeric(lng) && $.isNumeric(lat) && $.isNumeric(height) && $.isNumeric(rotate))
				{
					var model = CreateTowerModel(
						viewer, 
						GetModelUrl(tower['properties']['model']['model_code_height']), 
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
		else
		{
		}
	}
}

//function LoadTowerModelByLineId(viewer, ellipsoid, line_id)
//{
	//var scene = viewer.scene;
	//scene.primitives.removeAll(); // Remove previous model
	
	//var idx = 0;
	//var labels = new Cesium.LabelCollection();
	
	//var cond = {'db':'kmgd', 'collection':'towers', 'properties.line_id':line_id};
	//MongoFind( cond, 
		//function(data){
			//for(var i in data)
			//{
				//var t = data[i];
				//var label = labels.add({
					//position : ellipsoid.cartographicToCartesian(Cesium.Cartographic.fromDegrees(t['geometry']['coordinates'][0],  t['geometry']['coordinates'][1],  t['properties']['geo_z'])),
					//text     : t['properties']['tower_name'],
					//fillColor : { red : 0.0, blue : 1.0, green : 0.0, alpha : 1.0 }
				//});
				
				//var model = CreateTowerModel(viewer, GetModelUrl(t['properties']['model_code_height']), t['geometry']['coordinates'][0],  t['geometry']['coordinates'][1], t['properties']['geo_z'] ,  t['properties']['rotate'] );
				//if(idx > 10)
				//{
					//FlyToPoint(viewer, t['geometry']['coordinates'][0],  t['geometry']['coordinates'][1],  t['properties']['geo_z'] );
					//var controller = scene.screenSpaceCameraController;
					////controller.ellipsoid = Cesium.Ellipsoid.UNIT_SPHERE;
					////controller.enableTilt = true;
					//var r = t['properties']['geo_z'];
					////controller.minimumZoomDistance = r ;
					//break;
				//}
				//idx++;
			//}
			//scene.primitives.add(labels);
	//});
//}




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
	var scene = viewer.scene;
	var ellipsoid = scene.globe.ellipsoid;
	if (!Cesium.defined(viewer)) {
		throw new Cesium.DeveloperError('viewer is required.');
	}
	if (viewer.hasOwnProperty('trackedObject')) {
		throw new Cesium.DeveloperError('trackedObject is already defined by another mixin.');
	}
	if (viewer.hasOwnProperty('selectedObject')) {
		throw new Cesium.DeveloperError('selectedObject is already defined by another mixin.');
	}

	var infoBox;// = viewer.infoBox;
	var infoBoxViewModel = Cesium.defined(infoBox) ? infoBox.viewModel : undefined;

	var selectionIndicator = viewer.selectionIndicator;
	var selectionIndicatorViewModel = Cesium.defined(selectionIndicator) ? selectionIndicator.viewModel : undefined;
	var enableInfoOrSelection = Cesium.defined(infoBox) || Cesium.defined(selectionIndicator);
	//enableInfoOrSelection = false;
	var eventHelper = new Cesium.EventHelper();
	var dynamicObjectView;

	function trackSelectedObject() {
		viewer.trackedObject = viewer.selectedObject;
		var id = viewer.trackedObject.id;
		//console.log('track id=' + id);
		LookAtTarget(viewer, id);
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
		if(selectedObject && selectedObject.isAvailable)
		{
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
		}else
		{
			selectionIndicatorViewModel.showSelection = false;
			selectionIndicatorViewModel.update();
		}
	}
	eventHelper.add(viewer.clock.onTick, onTick);

//----test pick only-----
	//var labels = new Cesium.LabelCollection();
	//label = labels.add();
	//viewer.scene.primitives.add(labels);
//------------------
	function pickDynamicObject(e) {
		var picked = viewer.scene.pick(e.position);
		var ellipsoid = viewer.scene.globe.ellipsoid;
		var cartesian = viewer.scene.camera.pickEllipsoid(e.position, ellipsoid);
		if (cartesian) {
			//var cartographic = ellipsoid.cartesianToCartographic(cartesian);
			//var lng = Cesium.Math.toDegrees(cartographic.longitude).toFixed(7),
				//lat = Cesium.Math.toDegrees(cartographic.latitude).toFixed(7);
			//var text = '(' + lng + ',' + lat + ')';
			//label.show = true;
			//label.text = text;
			//label.position = cartesian;
		}
		
		
		
		if (Cesium.defined(picked)) {
			var id = Cesium.defaultValue(picked.id, picked.primitive.id);
			if (id instanceof Cesium.DynamicObject) {
				return id;
			}
			
			if (picked.primitive && picked.primitive instanceof Cesium.Primitive) {
				return picked;
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
		if (Cesium.defined(dynamicObject)) 
		{
			if (dynamicObject.primitive && dynamicObject.primitive instanceof Cesium.Primitive)
			{
			}
			else
			{
				trackObject(dynamicObject);
				var id = dynamicObject.id;
				LookAtTarget(viewer, id);
			}
		}
	}

	function pickAndSelectObject(e) {
	
		viewer.selectedObject = pickDynamicObject(e);
		if (Cesium.defined(viewer.selectedObject)) 
		{
			if (viewer.selectedObject.primitive && viewer.selectedObject.primitive instanceof Cesium.Primitive)
			{
				var id = viewer.selectedObject.id;
				g_primitive_appearance =  viewer.selectedObject.primitive.appearance;
				if(g_primitive_appearance.material)
				{
					console.log('selected line id=' + id);
					viewer.selectedObject.primitive.appearance = new Cesium.PolylineMaterialAppearance({
							//material : Cesium.Material.fromType(Cesium.Material.PolylineGlowType)
							material : Cesium.Material.fromType('PolylineOutline',{
								color:	g_primitive_appearance.material.uniforms.color,
								outlineColor : Cesium.Color.fromCssColorString('rgba(0, 255, 0, 1.0)'),
								outlineWidth: 3.0
							})
							//material : Cesium.Material.fromType('Color', {
								//color : Cesium.Color.fromCssColorString(rgba)
							//})
						});
					g_prev_selected_id = viewer.selectedObject;
				}
			}
			else
			{
				
				if(g_prev_selected_id && g_prev_selected_id.primitive && g_prev_selected_id.primitive instanceof Cesium.Primitive && g_primitive_appearance)
				{
					g_prev_selected_id.primitive.appearance = g_primitive_appearance;
				}
				//g_prev_selected_id = undefined;
				//g_selected_obj_id = undefined;
				
				var id = viewer.selectedObject.id;
				g_prev_selected_pos = viewer.selectedObject.position;
				g_prev_selected_id = g_selected_obj_id;
				g_selected_obj_id = id;
				//console.log('selected id=' + id);
				//console.log('prev selected id=' + g_prev_selected_id);
				if(g_prev_selected_id != g_selected_obj_id)
				{
					if(g_prev_selected_id)
					{
						if(CheckTowerInfoModified())
						{
							
							ShowConfirm('dlg_confirm',500, 200,
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
		}
		else{
			if(g_selected_obj_id && g_selected_obj_id.primitive && g_selected_obj_id.primitive instanceof Cesium.Primitive && g_primitive_appearance)
			{
				g_selected_obj_id.primitive.appearance = g_primitive_appearance;
			}
			g_prev_selected_id = g_selected_obj_id;
			g_selected_obj_id = undefined;
		}
	}

	//event after terrain change
	$('.cesium-baseLayerPicker-choices').on('click', function(e){
		var db = $(e.target).parent().parent().attr('data-bind');
		if(db == 'foreach: terrainProviderViewModels')
		{
			if($(e.target).parent().attr('title') == 'no-terrain')
			{
				//console.log('no terrain');
				g_zaware = false;
			}
			else
			{
				g_zaware = true;
				//console.log('yes terrain');			
			}
			ReloadCzmlDataSource(viewer, g_zaware);
			for(var k in g_czmls)
			{
				if(g_gltf_models[k])
				{
					var t = GetTowerInfoByTowerId(k);
					if(t)
					{
						RemoveSegmentsTower(viewer, t);
						//DrawSegmentsByTower(viewer, t);
						
						var lng = t['geometry']['coordinates'][0],
							lat = t['geometry']['coordinates'][1],
							height = t['properties']['geo_z'],
							rotate = t['properties']['rotate'];
						
						if(!g_zaware) height = 0;
						var scene = viewer.scene;
						var ellipsoid = scene.globe.ellipsoid;
						PositionModel(ellipsoid, g_gltf_models[k], lng, lat, height, rotate);
					}
				}
			}
			for(var k in g_lines)
			{
				var color = '#FF0000';
				if(g_lines[k].properties.voltage == '13')
				{
					color = '#FF0000';
				}
				if(g_lines[k].properties.voltage == '15')
				{
					color = '#0000FF';
				}
				DrawLineModelByLine(viewer, g_lines[k], 4.0, color);
				//DrawBufferOfLine(viewer, 'test', g_lines[k], 1500, 2300, '#00FF00', 0.3);
			}
		}
	});
	//console.log(viewer.baseLayerPicker.viewModel.selectedImagery.command.afterExecute);
	//eventHelper.add(viewer.scene.globe.imageryLayers.layerShownOrHidden, function(commandInfo){
		//console.log(commandInfo);
	//});


	if (Cesium.defined(viewer.homeButton)) {
		eventHelper.add(viewer.homeButton.viewModel.command.beforeExecute, function(commandInfo){
			clearTrackedObject();
		});
		eventHelper.add(viewer.homeButton.viewModel.command.afterExecute, function(commandInfo){
			var extent = GetExtentByCzml();
			FlyToExtent(viewer, extent['west'], extent['south'], extent['east'], extent['north']);
			//if(g_prev_selected_pos)
			//{
				////var vm = viewer.homeButton.viewModel;
				////vm.flightDuration = 1;
				////vm.command();
				////ClearTrackedObj(viewer);
				////ReloadCzmlDataSource(viewer);
				//var pos = viewer.scene.globe.ellipsoid.cartesianToCartographic(g_prev_selected_pos._value);
				//FlyToPoint(viewer, Cesium.Math.toDegrees(pos.longitude) , Cesium.Math.toDegrees(pos.latitude), pos.height, 2.8, 1);
				//g_prev_selected_pos = null;
			//}
			
			//if (Cesium.defined(g_selected_obj_id))
			//{
				//g_selected_obj_id = undefined;
			//}
		});
	}

	if (Cesium.defined(viewer.geocoder)) {
		eventHelper.add(viewer.geocoder.viewModel.search.beforeExecute, clearObjects);
	}

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
				//viewer.homeButton.viewModel.command();
			}
			if (viewer.selectedObject === removedObject) {
				//viewer.selectedObject = undefined;
			}
		}
	}

	function dataSourceAdded(dataSourceCollection, dataSource) {
		var dynamicObjectCollection = dataSource.dynamicObjects ;//.getDynamicObjectCollection();
		dynamicObjectCollection.collectionChanged.addEventListener(onDynamicCollectionChanged);
	}

	function dataSourceRemoved(dataSourceCollection, dataSource) {
		var dynamicObjectCollection = dataSource.dynamicObjects ;//.getDynamicObjectCollection();
		dynamicObjectCollection.collectionChanged.removeEventListener(onDynamicCollectionChanged);

		if (Cesium.defined(viewer.trackedObject)) {
			if (dynamicObjectCollection.getById(viewer.trackedObject.id) === viewer.trackedObject) {
				//viewer.homeButton.viewModel.command();
			}
		}

		if (Cesium.defined(viewer.selectedObject)) {
			if (dynamicObjectCollection.getById(viewer.selectedObject.id) === viewer.selectedObject) {
				//viewer.selectedObject = undefined;
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
			dynamicObjectView = new Cesium.DynamicObjectView(value, scene, viewer.scene.globe.ellipsoid);
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
	for(var i in g_geometry_segments)
	{
		var seg = g_geometry_segments[i];
		if(
			(seg['start'] == tower0['_id'] && seg['end'] == tower1['_id'])
		|| 	(seg['end'] == tower0['_id'] && seg['start'] == tower1['_id'])
		){
			ret = seg['primitive'];
			break;
		}
	}
	return ret;
}
function RemoveSegmentsFromArray(tower0, tower1)
{
	var ret = null;
	for(var i in g_geometry_segments)
	{
		var seg = g_geometry_segments[i];
		if(
			(seg['start'] == tower0['_id'] && seg['end'] == tower1['_id'])
		|| 	(seg['end'] == tower0['_id'] && seg['start'] == tower1['_id'])
		){
			ret = seg;
			g_geometry_segments.splice(i,1);
			break;
		}
	}
	return ret;
}

function CheckSegmentsExist(tower0, tower1)
{
	var ret = false;
	for(var i in g_geometry_segments)
	{
		var seg = g_geometry_segments[i];
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


function RemoveLineModel(viewer, line_id)
{
	var m;
	var l = [];
	for(var id in g_geometry_lines)
	{
		if(id.indexOf(line_id) > -1)
		{
			var model = g_geometry_lines[id];
			l.push({id:id, model:model});
		}
	}
	while(l.length>0)
	{
		var o = l.pop();
		delete g_geometry_lines[o.id];
		viewer.scene.primitives.remove(o.model);	
	}
}



function RemoveSegmentsBetweenTow(viewer, tower0, tower1)
{
	var scene = viewer.scene;
	if(CheckSegmentsExist(tower0, tower1))
	{
		var seg = RemoveSegmentsFromArray(tower0, tower1);
		if(seg)
		{
			while(!seg['primitive'].isDestroyed())
			{
				var ret = scene.primitives.remove(seg['primitive']);
			}
		}
	}
}

function DrawBufferOfLine(viewer, buf_id, line, width, height, color, alpha)
{
	var ellipsoid = viewer.scene.globe.ellipsoid;
	var array = line['properties']['towers'];
	if(array.length>0)
	{
		if(array[0] instanceof Array)
		{
		}
		else if(typeof(array[0]) == 'string')
		{
			var positions = GetPositions2DByCzmlArray(ellipsoid, array);
			DrawBufferPointPolyLine(viewer, buf_id, positions, width, height, color, alpha);
		}
	}
}
function RemoveBuffer(viewer, buf_id)
{
	for(var i in g_buffers)
	{
		if(i === buf_id)
		{
			var primitive = g_buffers[i];
			viewer.scene.primitives.remove(primitive);
			delete g_buffers[i];
		}
	}
}
function DrawBufferPointPolyLine(viewer, buf_id, positions, width, height, color, alpha)
{
	RemoveBuffer(viewer, buf_id);
	var ellipsoid = viewer.scene.globe.ellipsoid;
	var rgba = tinycolor(color).toRgb();
	rgba.a = 0.5;
	if(alpha) rgba.a = alpha;
	rgba = 'rgba(' + rgba.r + ',' + rgba.g + ',' + rgba.b + ',' + rgba.a + ')';
	
	if(!g_zaware) height = 0;
	
	var corridorGeometry = new Cesium.CorridorGeometry({
			positions : positions,
			width : width,
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
	viewer.scene.primitives.add(primitive);
	g_buffers[buf_id] = primitive;
	
	
}

function GetPositionsByCzmlArray(ellipsoid, arr, force2d)
{
	var ret = [];
	for(var i in arr)
	{
		var id = arr[i];
		if(g_czmls[id])
		{
			var cz = g_czmls[id];
			var pos = [];
			pos.push(cz['position']['cartographicDegrees'][0]);
			pos.push(cz['position']['cartographicDegrees'][1]);
			if(force2d)
			{
				pos.push(0);
			}else
			{
				if(g_zaware)
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


function DrawLineModelByLine(viewer, line, width, color, alpha)
{
	RemoveLineModel(viewer, line['_id']);
	var ellipsoid = viewer.scene.globe.ellipsoid;
	
	var rgba = tinycolor(color).toRgb();
	rgba.a = 0.5;
	if(alpha) rgba.a = alpha;
	rgba = 'rgba(' + rgba.r + ',' + rgba.g + ',' + rgba.b + ',' + rgba.a + ')';
	//console.log(rgba);
	
	var array = line['properties']['towers'];
	if(array.length>0)
	{
		//var polylines = new Cesium.PolylineCollection();
		
		if(array[0] instanceof Array)
		{
			for(var i in array)
			{
				var poss = GetPositionsByCzmlArray(ellipsoid, array[i]);
				var primitive = new Cesium.Primitive({
					geometryInstances : new Cesium.GeometryInstance({
						id:	line['_id'] + '_' + i,
						geometry : new Cesium.PolylineGeometry({
							positions : poss,
							width : width,
							vertexFormat : Cesium.PolylineMaterialAppearance.VERTEX_FORMAT
						})
					}),
					appearance : new Cesium.PolylineMaterialAppearance({
						//material : Cesium.Material.fromType(Cesium.Material.PolylineGlowType)
						material : Cesium.Material.fromType('Color', {
							color : Cesium.Color.fromCssColorString(rgba)
						}),
						renderState : {
							depthTest : {
								enabled : false
							}
						}
					})
				});
				viewer.scene.primitives.add(primitive);
				g_geometry_lines[line['_id'] + '_' + i] = primitive;
			}
		}
		else if(typeof(array[0]) == 'string')
		{
			var poss = GetPositionsByCzmlArray(ellipsoid, array);
			var primitive = new Cesium.Primitive({
				geometryInstances : new Cesium.GeometryInstance({
					id:	line['_id'],
					geometry : new Cesium.PolylineGeometry({
						positions : poss,
						width : width,
						vertexFormat : Cesium.PolylineMaterialAppearance.VERTEX_FORMAT
					})
				}),
				appearance : new Cesium.PolylineMaterialAppearance({
					material : Cesium.Material.fromType('Color', {
						color : Cesium.Color.fromCssColorString(rgba)
					}),
					renderState : {
						depthTest : {
							enabled : false
						}
					}
				})
			});
			viewer.scene.primitives.add(primitive);
			g_geometry_lines[line['_id']] = primitive;
			
			
		}
		//viewer.scene.primitives.add(polylines);
		//viewer.scene.primitives.add(polylines);
		//g_geometry_segments.push({'line_id': line['_id'], 'model':polylines});
	}
}
function DrawSegmentsBetweenTowTower(viewer, tower0, tower1)
{
	var scene = viewer.scene;
	if(tower0 && tower1 && !CheckSegmentsExist(tower0, tower1))
	{
		var ellipsoid = scene.globe.ellipsoid;
		var lng0 = tower0['geometry']['coordinates'][0],
			lat0 = tower0['geometry']['coordinates'][1],
			height0 = tower0['properties']['geo_z'],
			rotate0 = Cesium.Math.toRadians(tower0['properties']['rotate'] - 90),
			lng1 = tower1['geometry']['coordinates'][0],
			lat1 = tower1['geometry']['coordinates'][1],
			height1 = tower1['properties']['geo_z'],
			rotate1 = Cesium.Math.toRadians(tower1['properties']['rotate'] - 90);
		
		if(!g_zaware)
		{
			height0 = 0;
			height1 = 0;
		}

			
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
				mat4_0 = Cesium.Matrix4.multiplyByTranslation(mat4_0, tran_vec3_0);
				var m_0 = Cesium.Matrix4.multiplyTransformation(modelMatrix_0, mat4_0);
				
				
				var tran_vec3_1 = new Cesium.Cartesian3(cp1['x'], cp1['z'], cp1['y']);
				var mat4_1 = Cesium.Matrix4.fromRotationTranslation(rot_mat3_1, Cesium.Cartesian3.ZERO);
				mat4_1 = Cesium.Matrix4.multiplyByTranslation(mat4_1, tran_vec3_1);
				var m_1 = Cesium.Matrix4.multiplyTransformation(modelMatrix_1, mat4_1);

				var p0 = Cesium.Matrix4.getTranslation(m_0),
					p1 = Cesium.Matrix4.getTranslation(m_1);
				
				var positions = CalcCatenary(ellipsoid, p0, p1, 15);
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
		g_geometry_segments.push({'start':tower0['_id'], 'end':tower1['_id'], 'primitive':polylines});
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


function RemoveSegmentsTower(viewer, tower)
{
	var scene = viewer.scene;
	var prev_towers = GetNeighborTowers(tower['properties']['prev_ids']);
	var next_towers = GetNeighborTowers(tower['properties']['next_ids']);
	for(var i in prev_towers)
	{
		var t = prev_towers[i];
		RemoveSegmentsBetweenTow(viewer, t, tower);
	}
	for(var i in next_towers)
	{
		var t = next_towers[i];
		RemoveSegmentsBetweenTow(viewer, tower, t);
	}
}
function DrawSegmentsByTower(viewer, tower)
{
	var scene = viewer.scene;
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
			DrawSegmentsBetweenTowTower(viewer, t, tt);
		}
		for(var i in next_towers)
		{
			var t = next_towers[i];
			DrawSegmentsBetweenTowTower(viewer, tt, t);
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
function SavePoi(id)
{
	if(id)
	{
		console.log('save poi ' + id);
	}else
	{
		var id = $('input[id="poi_info_id"]').val();
		console.log('save form poi ' + id);
	}
}



function ShowTowerInfo(viewer, id)
{
	var tower = GetTowerInfoByTowerId(id);
	if(tower)
	{
		FilterModelList('');
		ShowTowerInfoDialog(viewer, tower);
		LoadTowerModelByTower(viewer, tower);
		DrawSegmentsByTower(viewer, tower);
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
		height: 720,
		minWidth:200,
		minHeight: 200,
		draggable: true,
		resizable: true, 
		modal: false,
		position:{at: "right center"},
		title:title,
		
		show: {
			effect: "blind",
			duration: 500
		},
		//hide: {
			//effect: "blind",
			//duration: 500
		//},		
		buttons:[
			{ 	
				//type: "checkbox",
				text: "锁定视角", 
				click: function(e){
					//console.log(e.target);
					g_is_tower_focus = !g_is_tower_focus;
					var dynamicObject = viewer.selectedObject;
					if(g_is_tower_focus)
					{
						$(e.target).css('background', '#00AA00 url(/css/black-green-theme/images/ui-bg_dots-medium_75_000000_4x4.png) 50% 50% repeat');
						$(e.target).html('解除锁定');
						
						if (Cesium.defined(dynamicObject)) 
						{
							viewer.trackedObject = dynamicObject;
							var id = dynamicObject.id;
							//console.log('track id=' + id);
							LookAtTarget(viewer, id);
						}				
					}
					else
					{
						$(e.target).css('background', '#000000 url(/css/black-green-theme/images/ui-bg_dots-medium_75_000000_4x4.png) 50% 50% repeat');
						$(e.target).html('锁定视角');
						
						//var extent = GetExtentByCzml();
						//FlyToExtent(viewer, extent['west'], extent['south'], extent['east'], extent['north']);
						if(dynamicObject)
						{
							var vm = viewer.homeButton.viewModel;
							//vm.flightDuration = 1;
							vm.command();
							var pos = viewer.scene.globe.ellipsoid.cartesianToCartographic(dynamicObject.position._value);
							if(pos.height === 0.0) pos.height = 2000;
							//console.log('pos.height=' + pos.height);
							FlyToPoint(viewer, Cesium.Math.toDegrees(pos.longitude) , Cesium.Math.toDegrees(pos.latitude), pos.height, 2.8, 1);
						}
						
						
						
						
					}
				}
			},
			{ 	text: "保存", 
				click: function(){ 
					if($('#form_tower_info_base').valid())
					{
						if(CheckTowerInfoModified())
						{
							ShowConfirm('dlg_confirm', 500, 200,
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
				$('#tower_info_model_list_filter').focus();
				var iframe = $(ui.newPanel.context).find('#tower_info_model').find('iframe');
				var url = GetModelUrl(tower['properties']['model']['model_code_height']);
				$('#tower_info_model_list_toggle').find('a').html('>>显示列表');
				$('#tower_info_model_list').css('display', 'none');
				$('#tower_info_model').find('iframe').css('width', '99%');
				var obj = {};
				if(!CheckModelCode(tower['properties']['model']['model_code_height']) || url.length==0)
				{
					//var id = $('input[id="tower_baseinfo_id"]').val();
					//obj['url'] = null;
					obj['data'] = tower['properties']['model'];
					obj['tower_id'] = tower['_id'];
					obj['denomi_height'] = tower['properties']['denomi_height'];
					$('#tower_info_title_model_code').html('杆塔型号：' + '无' + ' 呼称高：' + '无');
					//$('#tower_info_model_list_toggle').find('a').html('<<隐藏列表');
					//$('#tower_info_model_list').css('display', 'block');
					//$('#tower_info_model').find('iframe').css('width', '79%');
				}
				else if(url.length>0)
				{
					obj['url'] = '/' + url;
					obj['data'] = tower['properties']['model'];
					obj['tower_id'] = tower['_id'];
					obj['denomi_height'] = tower['properties']['denomi_height'];
					$('#tower_info_title_model_code').html('杆塔型号：' + tower['properties']['model']['model_code'] + ' 呼称高：' + tower['properties']['denomi_height']);
				}
				var json = encodeURIComponent(JSON.stringify(obj));
				iframe.attr('src', g_host + 'threejs/editor/index.html?' + json);
			}
			if(title == '架空线段')
			{
				var iframe = $(ui.newPanel.context).find('#tower_info_segment').find('iframe');
				var url = GetModelUrl(tower['properties']['model']['model_code_height']);
				var url_next = GetNextModelUrl(tower['properties']['next_ids']);
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
					obj['data'] = tower['properties']['model'];
					obj['tower_id'] = tower['_id'];
					obj['next_ids'] = tower['properties']['next_ids'];
					obj['data_next'] = GetNextTowerModelData(tower['properties']['next_ids']);
					obj['segments'] = GetSegmentsByTowerStartEnd(tower['_id'], tower['properties']['next_ids']);
					var json = encodeURIComponent(JSON.stringify(obj));
					iframe.attr('src', g_host + 'threejs/editor/index.html?' + json);
				}
				else
				{
					$('#tower_info_segment_blank').css('display', 'block');
					iframe.css('display', 'none');
				}
			}
		}
		//threejs/editor/index.html
	});
		
	//BuildForm(viewer, 'form_tower_info_base', g_tower_baseinfo_fields);
	//console.log($.viewer);
	var form = $('#form_tower_info_base').webgisform(g_tower_baseinfo_fields);
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
		//SetFormData('form_tower_info_base', data);
		//var SetFormData = $('#form_tower_info_base').webgisform.SetFormData;
		//console.log(SetFormData);
		//SetFormData(data);
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
				
				//BuildForm(viewer, 'form_tower_info_metal', flds);
				//SetFormData('form_tower_info_metal', formdata, 'tower_metal_');
				$('#form_tower_info_metal').webgisform(flds);
				$('#form_tower_info_metal').webgisform('setdata', formdata, 'tower_metal_');
			}
		}
	});
	
}




function ShowPoiInfoDialog(viewer, title, poi)
{
	$('#dlg_poi_info').dialog({
		width: 500,
		height: 600,
		minWidth:200,
		minHeight: 200,
		draggable: true,
		resizable: true, 
		modal: false,
		position:{at: "right center"},
		title:title,
		
		show: {
			effect: "blind",
			duration: 400
		},
		hide: {
			effect: "blind",
			duration: 400
		},		
		buttons:[
			{ 	text: "保存", 
				click: function(){ 
					if($('#form_poi_info').valid())
					{
						if(CheckPoiInfoModified())
						{
							ShowConfirm('dlg_confirm_poi', 500, 200,
								'保存确认',
								'检测到数据被修改，确认保存吗? 确认的话数据将会提交到服务器上，以便所有人都能看到修改的结果。',
								function(){
									SavePoi();
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
	
	var form;
	if(title == 'marker')
		form = $('#form_poi_info').webgisform(g_poi_info_fields);
	if(title == 'marker')
		form = $('#form_poi_info').webgisform(g_poi_info_fields);
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
		//SetFormData('form_tower_info_base', data);
		//var SetFormData = $('#form_tower_info_base').webgisform.SetFormData;
		//console.log(SetFormData);
		//SetFormData(data);
		$('#form_tower_info_base').webgisform('setdata', data);
	}
	
	
	
}

function GetPoiInfoById(id)
{
}
function CheckPoiInfoModified()
{
	var id = $('input[id="poi_info_id"]').val();
	console.log('poi_info_id=' + id);
	if(id && id.length>0)
	{
		var poi = GetPoiInfoById(id);
		if(poi)
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
	}
	return false;

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

function CheckModelCode(modelcode)
{
	var ret = false;
	for(var i in g_models)
	{
		if (g_models[i] == modelcode)
		{
			ret = true;
			break;
		}
	}
	return ret;
}
function RePositionPoint(viewer, id, lng, lat, height, rotate)
{
	if(g_czmls[id] && $.isNumeric(lng) && $.isNumeric(lat) && $.isNumeric(height) && $.isNumeric(rotate))
	{
		g_czmls[id]['position']['cartographicDegrees'] = [parseFloat(lng), parseFloat(lat), parseFloat(height)];
		ReloadCzmlDataSource(viewer, g_zaware);
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
			if(g_lines[i]['properties']['towers'][j] === id)
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



