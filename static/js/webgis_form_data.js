//绝缘子串
var g_insulator_type_list = [
	{'value':'导线绝缘子','label':'导线绝缘子', 'py':'dxjyzc'},
	{'value':'跳线绝缘子','label':'跳线绝缘子', 'py':'txjyzc'},
	{'value':'地线绝缘子','label':'地线绝缘子', 'py':'dxjyzc'},
	{'value':'OPGW绝缘子','label':'OPGW绝缘子', 'py':'opgwjyzc'}
];
var g_mat_type_list = [
	{'value':'陶瓷','label':'陶瓷', 'py':'tc'},
	{'value':'玻璃','label':'玻璃', 'py':'bl'},
	{'value':'合成','label':'合成', 'py':'hc'},
	{'value':'未知','label':'未知', 'py':'wz'}
];
var g_insulator_flds = [
	{display: "类型", id: "tower_metal_type", newline: true,  type: "text", editor:{readonly:true}, group:'绝缘子', width:350, labelwidth:105},
	{display: "绝缘子类型", id: "tower_metal_insulator_type", newline: true,  type: "select", editor: {data:g_insulator_type_list}, group:'绝缘子',  width:350, labelwidth:105},
	{display: "绝缘子材料", id: "tower_metal_material", newline: true,  type: "select", editor: {data:g_mat_type_list}, group:'绝缘子',  width:350, labelwidth:105},
	{display: "绝缘子型号", id: "tower_metal_model", newline: true,  type: "text", group:'绝缘子', width:350, labelwidth:105},
	{display: "串数", id: "tower_metal_strand", newline: true,  type: "spinner", step:1, min:0,max:100, group:'绝缘子', width:90, validate:{number: true}, labelwidth:105},
	{display: "片数", id: "tower_metal_slice", newline: false,  type: "spinner", step:1, min:0,max:500, group:'绝缘子', width:90, validate:{number: true}, labelwidth:105},
	{display: "生产厂家", id: "tower_metal_manufacturer", newline: true,  type: "text", group:'绝缘子', width:350, labelwidth:105},
	{display: "组装图号", id: "tower_metal_assembly_graph", newline: true,  type: "text", group:'绝缘子', width:350, labelwidth:105}
];
//防振锤
var g_damper_list = [
	{'value':'导线大号侧','label':'导线大号侧'},
	{'value':'导线小号侧','label':'导线小号侧'},
	{'value':'地线大号侧','label':'地线大号侧'},
	{'value':'地线小号侧','label':'地线小号侧'}
];
var g_damper_flds = [
	{display: "类型", id: "tower_metal_type", newline: true,  type: "text", editor:{readonly:true}, group:'防振锤',  width:275},
	{display: "安装部位", id: "tower_metal_side", newline: true,  type: "select", editor: {data:g_damper_list}, group:'防振锤',  width:275},
	{display: "防振锤型号", id: "tower_metal_model", newline: true,  type: "text", group:'防振锤', width:275},
	{display: "防振锤数量", id: "tower_metal_count", newline: true,  type: "spinner", step:1, min:0,max:100, group:'防振锤', width:70, validate:{number: true}},
	{display: "安装距离", id: "tower_metal_distance", newline: false,  type: "spinner", step:0.1, min:0,max:100, group:'防振锤', width:80, validate:{number: true}},
	{display: "生产厂家", id: "tower_metal_manufacturer", newline: true,  type: "text", group:'防振锤', width:275},
	{display: "组装图号", id: "tower_metal_assembly_graph", newline: true,  type: "text", group:'防振锤', width:275}
];

var g_grd_flds = [
	{display: "类型", id: "tower_metal_type", newline: true,  type: "text", editor:{readonly:true}, group:'接地装置',  width:275},
	{display: "型号", id: "tower_metal_model", newline: true,  type: "text", group:'接地装置', width:275},
	{display: "数量", id: "tower_metal_count", newline: true,  type: "spinner", step:1, min:0,max:100, group:'接地装置', width:70, validate:{number: true}},
	{display: "埋深", id: "tower_metal_depth", newline: false,  type: "spinner", step:0.1, min:0,max:100, group:'接地装置', width:80, validate:{number: true}},
	{display: "生产厂家", id: "tower_metal_manufacturer", newline: true,  type: "text", group:'接地装置', width:275},
	{display: "组装图号", id: "tower_metal_assembly_graph", newline: true,  type: "text", group:'接地装置', width:275}
];

var g_platform_model_list = [
	{'value':'铁塔','label':'铁塔'},
	{'value':'水泥塔','label':'水泥塔'}
];
var g_base_flds_1 = [//基础
	{display: "类型", id: "tower_metal_type", newline: true,  type: "text", editor:{readonly:true}, group:'基础',  width:275},
	{display: "平台类型", id: "tower_metal_platform_model", newline: true,  type: "select", editor: {data:g_platform_model_list}, group:'基础', width:275},
	{display: "数量", id: "tower_metal_count", newline: true,  type: "spinner", step:1, min:0,max:100, group:'基础', width:70, validate:{number: true}},
	{display: "埋深", id: "tower_metal_depth", newline: false,  type: "spinner", step:0.1, min:0,max:100, group:'基础', width:80, validate:{number: true}},
	{display: "生产厂家", id: "tower_metal_manufacturer", newline: true,  type: "text", group:'基础', width:275},
	{display: "组装图号", id: "tower_metal_assembly_graph", newline: true,  type: "text", group:'基础', width:275}
];
var g_base_flds_2_3_4 = [//拉线  防鸟刺  在线监测装置
	{display: "类型", id: "tower_metal_type", newline: true,  type: "text", editor:{readonly:true}, group:'在线监测装置',  width:275},
	{display: "型号", id: "tower_metal_model", newline: true,  type: "text", group:'在线监测装置', width:275},
	{display: "数量", id: "tower_metal_count", newline: true,  type: "spinner", step:1, min:0,max:999, group:'在线监测装置', width:70, validate:{number: true}},
	{display: "生产厂家", id: "tower_metal_manufacturer", newline: true,  type: "text", group:'在线监测装置', width:275},
	{display: "组装图号", id: "tower_metal_assembly_graph", newline: true,  type: "text", group:'在线监测装置', width:275}
];
var g_base_flds_5 = [ //雷电计数器
	{display: "类型", id: "tower_metal_type", newline: true,  type: "text", editor:{readonly:true}, group:'雷电计数器',  width:275},
	{display: "型号", id: "tower_metal_model", newline: true,  type: "text", group:'雷电计数器', width:275},
	{display: "读数", id: "tower_metal_counter", newline: true,  type: "spinner", step:1, min:0,max:999, group:'雷电计数器', width:70, validate:{number: true}},
	{display: "生产厂家", id: "tower_metal_manufacturer", newline: true,  type: "text", group:'雷电计数器', width:275},
	{display: "组装图号", id: "tower_metal_assembly_graph", newline: true,  type: "text", group:'雷电计数器', width:275}
];


var g_tower_baseinfo_fields = [
	{ id: "tower_baseinfo_id", type: "hidden" },
	//地理信息
	{ display: "经度", id: "tower_baseinfo_lng", newline: true,  type: "geographic", group:'地理信息', width:300 , validate:{required:true, number: true}},
	{ display: "纬度", id: "tower_baseinfo_lat", newline: true, type: "geographic",  group:'地理信息', width:300 , validate:{required:true, number: true}},
	{ display: "海拔(米)", id: "tower_baseinfo_alt", newline: true, type: "spinner", step:0.5, min:0,max:9999, group:'地理信息', width:300 , validate:{required:true, number: true}},
	{ display: "旋转角度", id: "tower_baseinfo_rotate", newline: true, type: "spinner", step:0.5, min:-180,max:180, group:'地理信息', width:300 , validate:{required:true, number: true}},
	//信息
	{ display: "名称", id: "tower_baseinfo_tower_name", newline: true,  type: "text", group:'信息', width:330, validate:{required:true}},
	{ display: "代码", id: "tower_baseinfo_tower_code", newline: true,  type: "text", group:'信息', width:330 },
	{ display: "塔型", id: "tower_baseinfo_model_code", newline: true,  type: "text", group:'信息', width:100 },
	{ display: "呼称高", id: "tower_baseinfo_denomi_height", newline: true,  type: "spinner", step:0.1, min:0,max:9999, group:'信息', width:90, validate:{number: true}},
	//电气
	{ display: "接地电阻", id: "tower_baseinfo_grnd_resistance", newline: true,  type: "spinner", step:0.1, min:0,max:9999, group:'电气', width:300, validate:{number: true}},
	//土木
	{ display: "水平档距", id: "tower_baseinfo_horizontal_span", newline: true,  type: "spinner", step:0.1, min:0,max:9999, group:'土木', width:85, validate:{number: true} },
	{ display: "垂直档距", id: "tower_baseinfo_vertical_span", newline: true,  type: "spinner", step:0.1, min:0,max:9999, group:'土木', width:85, validate:{number: true} },
	//工程
	{ display: "所属工程", id: "tower_baseinfo_project", newline: true,  type: "text", group:'工程', width:330 }
];


function BuildForm(viewer, id, fields)
{
	var scene = viewer.scene;
	var ellipsoid = scene.globe.ellipsoid;
	$('#' + id).empty();
	var labelwidth = 90;
	var margin = 10/2;
	var groupmargin = 18/2;
	//var donegroups = {};
	var groups = [];
	for(var i in fields)
	{
		var fld = fields[i];
		if(fld.type == 'hidden')
		{
			$('#' + id).append('<input type="hidden" id="' + fld.id + '">');
		}
		if(fld.group)
		{
			if(groups.indexOf(fld.group)==-1)
			{
				groups.push(fld.group);
			}
		}
	}
	
	
	for(var j in groups)
	{
		var group = groups[j];
		var uid = $.uuid();
		var g = $('#' + id).append('<fieldset id="fieldset_' + uid + '" style="color:#00FF00;border:1px solid #00FF00;margin:' + groupmargin + 'px;"><legend style="font-weight:bolder;color:#00FF00;">' + group + '</legend>');
		$('#' + id).append('</fieldset>');
		$('#' + id).append('<p></p>');
		
		for(var i in fields)
		{
			var fld = fields[i];
			if(fld.labelwidth) labelwidth = fld.labelwidth;
			var newline = "float:left;";
			if(fld.newline == false) newline = "";
			var validate = '';
			if(fld.validate)
			{
				validate = '<span style="color:#FF0000">*</span>';
			}
			if(fld.type == 'spinner' && fld.group == group)
			{
				$('#' + 'fieldset_' + uid).append('<div style="margin:' + margin + 'px;' + newline + '"><label for="' + fld.id + '" style="display:inline-block;text-align:right;width:' + labelwidth + 'px;">' + fld.display + ':' + '</label><input  style="width:' + fld.width + 'px;" id="' + fld.id + '" name="' + fld.id + '">' + validate + '</div>');
				var spin = 	$('#' + fld.id).spinner({
					step: fld.step,
					max:fld.max,
					min:fld.min,
					change:function( event, ui ) {
						if(event.currentTarget)
						{
							var fid = $(event.target).attr('id');
							if(fid.indexOf('_alt')>-1 || fid.indexOf('_rotate')>-1)
							{
								var id = $('input[id="tower_baseinfo_id"]').val();
								var lng = $('input[id="tower_baseinfo_lng"]').val(),
									lat = $('input[id="tower_baseinfo_lat"]').val(),
									height = $('input[id="tower_baseinfo_alt"]').val(),
									rotate = $('input[id="tower_baseinfo_rotate"]').val();
								if(g_gltf_models[id])
								{
									if(fid.indexOf('_alt')>-1) height = event.currentTarget.value;
									if(fid.indexOf('_rotate')>-1) rotate = event.currentTarget.value;
									PositionModel(ellipsoid, g_gltf_models[id], lng, lat, height, rotate);
									var tower = GetTowerInfoByTowerId(id);
									if(tower)
									{
										RemoveSegmentsTower(scene, tower);
										DrawSegmentsByTower(scene, tower);
										RePositionPoint(viewer, id, lng, lat, height, rotate);
									}
								}
							}
						}
						event.preventDefault();
					},
					spin:function( event, ui ) {
						var fid = $(event.target).attr('id');
						if(fid.indexOf('_alt')>-1 || fid.indexOf('_rotate')>-1)
						{
							var id = $('input[id="tower_baseinfo_id"]').val();
							var lng = $('input[id="tower_baseinfo_lng"]').val(),
								lat = $('input[id="tower_baseinfo_lat"]').val(),
								height = $('input[id="tower_baseinfo_alt"]').val(),
								rotate = $('input[id="tower_baseinfo_rotate"]').val();
							if(g_gltf_models[id]) 
							{
								if(fid.indexOf('_alt')>-1)		height = ui.value;
								if(fid.indexOf('_rotate')>-1)	rotate = ui.value;
								//RePositionPoint(viewer, id, lng, lat, height, rotate);
								PositionModel(ellipsoid, g_gltf_models[id], lng, lat, height, rotate);	
							}
						}
					}
				});
			}
			if(fld.type == 'geographic' && fld.group == group)
			{
				$('#' + 'fieldset_' + uid).append('<div style="margin:' + margin + 'px;' + newline + '"><label for="' + fld.id + '" style="display:inline-block;text-align:right;width:' + labelwidth + 'px;">' + fld.display + ':' + '</label><input  style="width:' + fld.width + 'px;" id="' + fld.id + '" name="' + fld.id + '">' + validate + '</div>');
				var spin = 	$('#' + fld.id).spinner({
					step: 0.00001,
					max:179.0,
					min:-179.0,
					change:function( event, ui ) {
						var fid = $(event.target).attr('id');
						if(fid.indexOf('_lng')>-1 || fid.indexOf('_lat')>-1)
						{
							var id = $('input[id="tower_baseinfo_id"]').val();
							if(g_gltf_models[id])
							{
								if(event.currentTarget)
								{
									var lng = $('input[id="tower_baseinfo_lng"]').val(),
										lat = $('input[id="tower_baseinfo_lat"]').val(),
										height = $('input[id="tower_baseinfo_alt"]').val(),
										rotate = $('input[id="tower_baseinfo_rotate"]').val();
									if(fid.indexOf('_lng')>-1) lng = event.currentTarget.value;
									if(fid.indexOf('_lat')>-1) lat = event.currentTarget.value;
									PositionModel(ellipsoid, g_gltf_models[id], lng, lat, height, rotate);
									var tower = GetTowerInfoByTowerId(id);
									if(tower)
									{
										RemoveSegmentsTower(scene, tower);
										DrawSegmentsByTower(scene, tower);
										RePositionPoint(viewer, id, lng, lat, height, rotate);
									}
								}
							}
						}
						event.preventDefault();
					},
					spin:function( event, ui ) {
						var fid = $(event.target).attr('id');
						if(fid.indexOf('_lng')>-1 || fid.indexOf('_lat')>-1)
						{
							var id = $('input[id="tower_baseinfo_id"]').val();
							if(g_gltf_models[id])
							{
								var lng = $('input[id="tower_baseinfo_lng"]').val(),
									lat = $('input[id="tower_baseinfo_lat"]').val(),
									height = $('input[id="tower_baseinfo_alt"]').val(),
									rotate = $('input[id="tower_baseinfo_rotate"]').val();
								if(fid.indexOf('_lng')>-1) lng = ui.value;
								if(fid.indexOf('_lat')>-1) lat = ui.value;
								//RePositionPoint(viewer, id, lng, lat, height, rotate);
								PositionModel(ellipsoid, g_gltf_models[id], lng, lat, height, rotate);
							}
						}
					}
				});
			}
			if(fld.type == 'text' && fld.group == group)
			{
				var readonly = '';
				if(fld.editor && fld.editor.readonly == true)
				{
					readonly = ' readonly="readonly"';
				}
				$('#' + 'fieldset_' + uid).append('<div style="margin:' + margin + 'px;' + newline + '"><label for="' + fld.id + '" style="display:inline-block;text-align:right;width:' + labelwidth + 'px;">' + fld.display + ':' + '</label><input type="text" class="ui-widget" style="width:' + fld.width + 'px;" id="' + fld.id + '" name="' + fld.id + '" ' + readonly + '>' + validate + '</div>');
			}
			if(fld.type == 'select' && fld.group == group)
			{
				var source = [];
				if(fld.editor && fld.editor.data) source = fld.editor.data;
				$('#' + 'fieldset_' + uid).append('<div style="margin:' + margin + 'px;' + newline + '"><label for="' + fld.id + '" style="display:inline-block;text-align:right;width:' + labelwidth + 'px;">' + fld.display + ':' + '</label><select  style="width:' + fld.width + 'px;" id="' + fld.id + '" name="' + fld.id + '"></select>' + validate + '</div>');
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
	ValidateForm(id, fields);
}

function ValidateForm(id, fields)
{
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
}


function SetFormData(id, data, prefix)
{
	for(var k in data)
	{
		if(prefix)
		{
			$('#' + id).find('#' + prefix + k).val(data[k]);
		}
		else
		{
			$('#' + id).find('#' + k).val(data[k]);
		}
	}
}

