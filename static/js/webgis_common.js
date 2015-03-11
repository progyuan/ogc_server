$.webgis = {};
$.webgis.arcserver_host = 'yncaiyun1.com';//10.181.160.72
$.webgis.host = 'yncaiyun1.com';//10.181.160.72
//$.webgis.arcserver_host = '192.168.1.107';//10.181.160.72
//$.webgis.host = '192.168.1.107';//10.181.160.72
$.webgis.port = 8088;
$.webgis.tiles_host = 'yncaiyun1.com';
$.webgis.tiles_port = 8088;
//var $.webgis.db.db_name = 'kmgd';
$.webgis.db = {};
$.webgis.db.db_name = 'kmgd';
//$.webgis.db.db_name = 'ztgd';
$.webgis.zaware = false;

$.webgis.encrypt_key = 'kmgd111';
$.webgis.phase_color_mapping = {
	'A':'#FFFF00',
	'B':'#FF0000',
	'C':'#00FF00',
	'G':'#000000',
	'G1':'#000000',
	'L':'#000000',
	'R':'#000000'
};
$.webgis.style_mapping = {
	'point_tower' :		{icon_img:'img/features/powerlinepole.png', color:[255, 255, 0, 255],outlineColor:[0, 0, 0, 255], outlineWidth:1, pixelSize:10, labelFillColor:[128, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_hazard' :	{icon_img:'img/features/radiation.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_marker' :	{icon_img:'img/marker30x48.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_dn_switch' :	{icon_img:'img/features/metronetwork.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:8, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_dn_link'	:			{icon_img:'img/features/linedown.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:8, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_dn_transform' :		{icon_img:'img/features/factory.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:8, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_dn_transformarea' :	{icon_img:'img/features/expert.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:8, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_hotel':		{icon_img:'img/features/hotel_0star.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_restaurant': {icon_img:'img/features/restaurant.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_mall':		{icon_img:'img/features/mall.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_exitentrance': {icon_img:'img/features/entrance.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_village':	{icon_img:'img/features/windmill-2.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_building':	{icon_img:'img/features/office-building.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_subcity':	{icon_img:'img/features/citysquare.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_busstop':	{icon_img:'img/features/busstop.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_park':		{icon_img:'img/features/wetlands.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_provincecapital': {icon_img:'img/features/arch.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_rollstop':	{icon_img:'img/features/accesdenied.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_parker':		{icon_img:'img/features/parking-meter-export.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_county':		{icon_img:'img/features/ghosttown.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_school':		{icon_img:'img/features/school.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_chemistsshop': {icon_img:'img/features/', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_hospital':	{icon_img:'img/features/hospital-building.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_bank':		{icon_img:'img/features/hospital-building.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
	'point_town':		{icon_img:'img/features/cathedral.png', color:[64, 128, 255, 255],outlineColor:[255, 255, 255, 255], outlineWidth:1, pixelSize:3, labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale: 0.6},
//};
//var g_style_polyline_mapping = {
	'polyline_marker':{color:[0, 64, 255, 255], pixelWidth:1, outlineColor:[255, 64, 255, 255], outlineWidth:1, labelFillColor:[0, 64, 255, 255], labelOutlineColor:[255, 255, 255, 255], labelScale:1},
	'polyline_hazard':{color:[255, 64, 0, 255], pixelWidth:1, outlineColor:[255, 64, 255, 255], outlineWidth:1, labelFillColor:[255, 64, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale:1},
	'polyline_speedway':{color:[255, 128, 0, 255], pixelWidth:1, outlineColor:[255, 64, 255, 255], outlineWidth:1, labelFillColor:[255, 128, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale:1},
	'polyline_heighway':{color:[255, 128, 0, 255], pixelWidth:1, outlineColor:[255, 64, 255, 255], outlineWidth:1, labelFillColor:[255, 128, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale:1},
	'polyline_nationalroad':{color:[255, 128, 0, 255], pixelWidth:1, outlineColor:[255, 64, 255, 255], outlineWidth:1, labelFillColor:[255, 128, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale:1},
	'polyline_provinceroad':{color:[255, 128, 0, 255], pixelWidth:1, outlineColor:[255, 64, 255, 255], outlineWidth:1, labelFillColor:[255, 128, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale:1},
	'polyline_railway':{color:[255, 128, 0, 255], pixelWidth:1, outlineColor:[255, 64, 255, 255], outlineWidth:1, labelFillColor:[255, 128, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale:1},
//};
//var g_style_polygon_mapping = {
	'polygon_marker':{color:[0, 64, 255, 100], outlineColor:[255, 255, 0, 255],  labelFillColor:[255, 255, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale:1},
	'polygon_hazard':{color:[255, 64, 0, 100], outlineColor:[255, 64, 0, 255],  labelFillColor:[255, 64, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale:1},
	'polygon_buffer':{color:[255, 0, 0, 50], outlineColor:[255, 64, 0, 255],  labelFillColor:[255, 0, 0, 255], labelOutlineColor:[255, 255, 255, 255], labelScale:1}
};

$.webgis.role_functions = [
	{value:'line_edit', label:'线路工程查看'},
	{value:'line_save', label:'线路工程创建与保存'},
	{value:'line_delete', label:'线路工程删除'},
	{value:'edge_save', label:'节点连接关系创建与保存'},
	{value:'edge_delete',label:'节点连接关系删除'},
	{value:'tower_save', label:'杆塔创建与保存'},
	{value:'tower_delete', label:'杆塔删除'},
	{value:'feature_save', label:'地标创建与保存'},
	{value:'feature_delete', label:'地标删除'},
	{value:'buffer_analyze', label:'缓冲区分析'},
];

function GetDefaultExtent(db_name)
{
	if(db_name == 'kmgd')
	{
		return {'west':101.69184, 'south':24.04067, 'east':103.71404, 'north':26.06087};
	}
	if(db_name == 'ztgd')
	{
		return {'west':102.7013, 'south':26.32388, 'east':104.7235, 'north':28.34408};
	}
}
function GetDefaultCenter(db_name)
{
	var ext = GetDefaultExtent(db_name);
	return [(ext['west'] + ext['east'])/2.0, (ext['south'] + ext['north'])/2.0];
}

function InitWebGISFormDefinition()
{
	var methods = 
	{
		init : function(fields, options) 
		{
			
			if(!fields) return this;
			this.fields = fields;
			if(!$.fn.webgisform.fields) $.fn.webgisform.fields = {}
			$.fn.webgisform.fields[this.attr('id')] = fields;
			this.groups = [];
			this.options = $.extend({}, $.fn.webgisform.defaults, options);
			if(!$.fn.webgisform.options) $.fn.webgisform.options = {}
			$.fn.webgisform.options[this.attr('id')] = this.options;
			this.empty();
			var prefix = '';
			if($.fn.webgisform.options[this.attr('id')].prefix) prefix = $.fn.webgisform.options[this.attr('id')].prefix;
			var maxwidth = 400;
			if($.fn.webgisform.options[this.attr('id')].maxwidth) maxwidth = $.fn.webgisform.options[this.attr('id')].maxwidth;
			var divorspan = this.options.divorspan;
			var debug = true;
			if($.fn.webgisform.options[this.attr('id')].debug) debug = $.fn.webgisform.options[this.attr('id')].debug;
			
			for(var i in fields)
			{
				var fld = fields[i];
				var fldid = prefix + fld.id;
				if(fld.type == 'hidden')
				{
					this.append('<input type="hidden" id="' + fldid + '">');
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
				var g = this.append('<fieldset id="fieldset_' + uid + '" style="min-height:50px;color:#00FF00;border:1px solid #00FF00;margin:' + this.options.groupmargin + 'px;"><legend style="font-weight:bolder;color:#00FF00;">' + group + '</legend>');
				this.append('</fieldset>');
				this.append('<p></p>');
				
				
				for(var i in fields)
				{
					var fld = fields[i];
					var fldid = prefix + fld.id;
					
					if(fld.labelwidth) this.options.labelwidth = fld.labelwidth;
					var newline = '';
					var stylewidth = '';
					if(fld.newline === false)
					{
						newline = 'float:left;';
					}
					if(fld.newline === true)
					{
						stylewidth = 'width:' + maxwidth + 'px;';
						newline = 'display:block;';
					}
					var required = '';
					if(fld.validate && fld.validate.required)
					{
						required = '<span  style="color:#FF0000;">*</span>';
					}
					if(fld.type == 'spinner' && fld.group == group)
					{
						
						//console.log(fldid + ' ' + newlinepara);
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="' + stylewidth + 'margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px; ">' + fld.display + ':' + '</label><input  style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '">' + required + '</' + divorspan + '>');
						var spin = 	$('#' + fldid).spinner({
							step: fld.step,
							max:fld.max,
							min:fld.min,
							change:fld.change,
							spin:fld.spin
						});
						if(fld.defaultvalue) $('#' + fldid).val(fld.defaultvalue);
					}
					if(fld.type == 'geographic' && fld.group == group)
					{
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="' + stylewidth + 'margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input  style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '">' + required + '</' + divorspan + '>');
						var spin = 	$('#' + fldid).spinner({
							step: 0.00001,
							max:179.0,
							min:-179.0,
							change: fld.change,
							spin: fld.spin
						});
						if(fld.defaultvalue) $('#' + fldid).val(fld.defaultvalue);
					}
					if(fld.type == 'text' && fld.group == group)
					{
						var readonly = '';
						if(fld.editor && fld.editor.readonly == true)
						{
							readonly = ' readonly="readonly"';
						}
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="' + stylewidth + 'margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input type="text" class="ui-widget" style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '" ' + readonly + '>' + required + '</' + divorspan + '>');
						if(fld.defaultvalue) $('#' + fldid).val(fld.defaultvalue);
					}
					if(fld.type == 'password' && fld.group == group)
					{
						var readonly = '';
						if(fld.editor && fld.editor.readonly == true)
						{
							readonly = ' readonly="readonly"';
						}
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="' + stylewidth + 'margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input type="password" class="ui-widget" style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '" ' + readonly + '>' + required + '</' + divorspan + '>');
						if(fld.defaultvalue) $('#' + fldid).val(fld.defaultvalue);
					}
					if(fld.type == 'select' && fld.group == group)
					{
						var source = [];
						if(fld.editor && fld.editor.data) source = fld.editor.data;
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="' + stylewidth + 'margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><select  style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '"></select>' + required + '</' + divorspan + '>');
						for(var ii in source)
						{
							$('#' + fldid).append('<option value="' + source[ii]['value'] + '">' + source[ii]['label'] + '</option>');
						}
						//var auto = $('#' + fldid).autocomplete({
							////appendTo:'#' + fldid,
							////position: { my: "left top", at: "left bottom", collision: "none" },
							//autoFocus: false,
							//source:source
						//});
						var position = 'bottom';
						if(fld.editor && fld.editor.position) position = fld.editor.position;
						var fld1 = fld;
						var auto = $('#' + fldid).multipleSelect({
							selectAll: false,
							selectAllText: '全部',
							selectAllDelimiter: ['(', ')'],
							allSelected: '(全部)',
							//minumimCountSelected: 3,
							countSelected: '(选择#个,共%个)',
							noMatchesFound: '(无匹配)',
							single: true,
							position: position,
							onClick:function(view){
								if(view.checked)
								{
									//console.log(fld1);
									if(fld1.change)
									{
										fld1.change(view.value);
									}
								}
							},
							styler: function(value) {
								return 'color: #00FF00;background: #000000 url(/css/black-green-theme/images/ui-bg_diagonals-small_50_000000_40x40.png) 100% 100% repeat;';
							}
						});
						//if(fld.defaultvalue) $('#' + fldid).val(fld.defaultvalue);
						if(fld.defaultvalue)
						{
							$('#' + fldid).multipleSelect("setSelects", [fld.defaultvalue]);
						}
						//$('#' + fldid).css('display', 'none');
						auto.css('border', '1px #00FF00 solid');
						//auto.css('display', 'inline-block');
						auto.css('color', '#00FF00');
						auto.css('background', '#000000 url(/css/black-green-theme/images/ui-bg_diagonals-small_50_000000_40x40.png) 100% 100% repeat');
						//auto.find('option').css('background', '#000000 url(/css/black-green-theme/images/ui-bg_diagonals-small_50_000000_40x40.png) 100% 100% repeat');
					}
					if(fld.type == 'multiselect' && fld.group == group)
					{
						var source = [];
						if(fld.editor && fld.editor.data) source = fld.editor.data;
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="' + stylewidth + 'margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><select  style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '"></select>' + required + '</' + divorspan + '>');
						for(var ii in source)
						{
							$('#' + fldid).append('<option value="' + source[ii]['value'] + '">' + source[ii]['label'] + '</option>');
						}
						var position = 'bottom';
						if(fld.editor && fld.editor.position) position = fld.editor.position;
						var selectAll = false;
						if(fld.selectall) selectAll = true;
						var auto = $('#' + fldid).multipleSelect({
							selectAll: selectAll,
							selectAllText: '全部',
							selectAllDelimiter: ['(', ')'],
							allSelected: '(全部)',
							//minumimCountSelected: 3,
							countSelected: '(选择#个,共%个)',
							noMatchesFound: '(无匹配)',
							single: false,
							position: position,
							styler: function(value) {
								return 'color: #00FF00;background: #000000 url(/css/black-green-theme/images/ui-bg_diagonals-small_50_000000_40x40.png) 100% 100% repeat;';
							}
						});
						if(fld.defaultvalue && fld.defaultvalue instanceof Array && fld.defaultvalue.length>0)
						{
							$('#' + fldid).multipleSelect("setSelects", fld.defaultvalue);
						}
						
					}
					if(fld.type == 'date' && fld.group == group)
					{
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="' + stylewidth + 'margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input type="text" class="ui-widget" style="padding:7px 0px 0px 0px;width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '" ' + readonly + '>'  + required + '</' + divorspan + '>');
						$('#' + fldid ).datepicker({
							//appendText: "(yyyy-mm-dd)",
							dateFormat:  "yy-mm-dd",
							autoSize: false,
							//altField: "#" + fldid,
							buttonImage: "img/datepicker.png",
							buttonImageOnly:true,
							currentText: "今天",
							monthNames: ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'],  
							dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],  
							dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],  
							dayNamesMin: ['日','一','二','三','四','五','六'],  
							showOn: "button",
							duration: "slow",
							showButtonPanel: false,
							showAnim:"slideDown",
							//showOptions: { 
								////effect: "slide",
								////direction: "down",
								//duration: 100
							//},
							yearSuffix: '年'
						});
						if(fld.defaultvalue) $('#' + fldid).datepicker("setDate", fld.defaultvalue);
					}
					if(fld.type == 'icon' && fld.group == group)
					{
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="' + stylewidth + 'margin:' + this.options.margin + 'px;' + newline 
						+ '"><label for="input_' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display 
						+ ':' 
						+ '</label><' + divorspan + ' style="display:inline-block;width:32px;height:32px;border:1px #00FF00 solid;" id="' + fldid + '" name="' + fldid + '" ></' + divorspan + '>' + required 
						+ '<ol class="kmgd-icon-selectable"  id="ol_' + fldid + '"></ol></' + divorspan + '>');
						$('#ol_' + fldid ).css('display', 'none');
						var defaultvalue = 'point_marker';
						if(fld.defaultvalue) defaultvalue = fld.defaultvalue;
						$('#' + fldid ).addClass('icon-selector-' + defaultvalue);
						
						$('#ol_' + fldid ).empty();
						for(var i in fld.iconlist)
						{
							//$('#ol_' + fldid ).append('<li class="ui-state-default"><' + divorspan + ' class="icon-selector-' + fld.iconlist[i] + '"></' + divorspan + '></li>');
							$('#ol_' + fldid ).append('<li class="icon-selector-' + fld.iconlist[i] + '"></li>');
						}
						var fldid2 = fldid ;
						var v = fld.iconvalue;
						$('#ol_' + fldid2 ).selectable({
							appendTo: '#' + fldid2,
							selected: function( event, ui ){
								$(ui.selected).removeClass('ui-selected');
								$('#' + fldid2).attr('class', '');
								var cls = $(ui.selected).attr('class');
								//console.log('[' + cls + ']');
								//cls = cls.replace('ui-selectee', '');
								//console.log(fldid2 + '[' + cls + ']');
								$('#' + fldid2 ).addClass(cls);
								$('#ol_' + fldid2 ).css('display', 'none');
							}
						});
						var widget = $('#ol_' + fldid ).selectable("widget");
						$('#' + fldid ).off();
						var fldid3 = fldid ;
						$('#' + fldid ).on('click', function(e){
							if($('#ol_' + fldid3 ).css('display') === 'none')
							{
								$('#ol_' + fldid3 ).css('display', 'block');
							}
							else
							{
								$('#ol_' + fldid3 ).css('display', 'none');
							}
						});
						$('#' + fldid ).on('mouseenter', function(e){
							$(this).css("background-color", "#005500");
						});
						$('#' + fldid ).on('mouseleave', function(e){
							$(this).css("background-color", "#000000");
						});
						$('#ol_' + fldid ).on('mouseleave', function(e){
							$('#ol_' + fldid3 ).css('display', 'none');
						});
						
					}
					
					if(fld.type == 'color' && fld.group == group)
					{
						var colorarr = [255, 0, 0, 128];
						if(fld.defaultvalue) colorarr = fld.defaultvalue;
						var color = ColorArrayToRgba(colorarr);
						//console.log(fldid + ' ' + color);
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="' + stylewidth + 'margin:' + this.options.margin + 'px;' + newline 
						+ '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display 
						+ ':</label>'
						+ '<' + divorspan + '  style="display:inline-block;width:42px;height:32px;border:0px #00FF00 solid;">'
						+ '<input type="color" id="' + fldid + '" name="' + fldid + '" >' + required 
						+ '</' + divorspan + '>'
						+ '</' + divorspan + '>');
						var id = fldid;
						$('#' + id).spectrum({
							color: color,
							allowEmpty: true,
							flat: false,
							showAlpha: true,
							showInitial: true,
							showPalette: false,
							showInput: true,
							cancelText: '取消',
							chooseText: '确定',
							showButtons: false,
							preferredFormat: "rgb",
							clickoutFiresChange: true,
							replacerClassName: 'webgis-colorpicker',
							containerClassName: 'webgis-colorpicker'
						});
						$('#' + id).next().css('display', 'inline-block');
						$('#' + id).next().children().css('display', 'inline-block');
						$('#' + id).next().find('.sp-preview-inner').css('display', 'inline-block');
						$('#' + id).next().css('width', '32px');
						$('#' + id).next().css('height', '22px');
						$('#' + id).next().find('.sp-preview-inner').css('background-color', color);
						//console.log($('#' + fldid).next().children().css('display'));
					}
					
					if(fld.type == 'checkbox' && fld.group == group)
					{
						var checked = false;
						if(fld.defaultvalue) checked = true;
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="' + stylewidth + 'margin:' + this.options.margin + 'px;' + newline + '">'
						+ '<' + divorspan + '  style="display:inline-block;width:24px;height:24px;border:0px #00FF00 solid;">'
						+ '<input type="checkbox" id="' + fldid + '" name="' + fldid + '" >' + required 
						+ '</' + divorspan + '>'
						+ '<label for="' + fldid + '" style="display:inline-block;text-align:left;width:' + this.options.labelwidth + 'px;">' + fld.display + '</label>'
						+ '</' + divorspan + '>');
						var id = fldid;
						$('#' + id).iCheck({
							checkboxClass: 'icheckbox_flat-green'
						});
						if(checked) $('#' + id).iCheck('check');
					}
				}
			}
			var hide = false;
			var hideparentlist = [];
			for(var i in this.fields)
			{
				var fld = this.fields[i];
				var fldid = prefix + fld.id;
				if(fld.hide && fld.hide === true)
				{
					hide = true;
					var group = $('#' + fldid ).parent().parent();
					group.hide();
					if(hideparentlist.indexOf(group) < 0)
					{
						hideparentlist.push(group);
					}
				}
			}
			if(hide)
			{
				this.append('<' + divorspan + ' id="' + prefix + '_more_info" style="float:right"><a href="#">更多信息&gt;&gt;</a></' + divorspan + '>');
				$('#' + prefix + '_more_info').off();
				//$('#' + prefix + '_more_info').hover( function(){
					//$(this).css('cursor', 'hand');
				//});
				$('#' + prefix + '_more_info').find('a').on('click', function(){
					for(var i in hideparentlist)
					{
						var group = hideparentlist[i];
						if(group.is(':visible'))
						{
							group.hide();
							$(this).html('更多信息&gt;&gt;');
						}
						else
						{
							group.show();
							$(this).html('更多信息&lt;&lt;');
						}
					}
					
				});
			}
			
			
			var fields = this.fields;
			this.validate({
				errorPlacement: function(error, element) {
					//element.html(error.html()).css('color', '#FF0000').css('width', '130px').css('height', '20px').css('background-image', 'none');
					element.tooltipster('update', error.text());
					element.tooltipster('show');				
				},
				success:function(label, element) {
					$(element).tooltipster('hide');
				}
				//success:'valid'
			});
			for(var i in fields)
			{
				var fld = fields[i];
				var fldid = prefix + fld.id;
				if(fld.validate)
				{
					$('#' + fldid ).rules('add',fld.validate);
					$('#' + fldid ).tooltipster({ 
						trigger: 'custom',
						onlyOne: false, 
						position: 'right'
					});					
					
				}
			}
			
			return this;
		},
		clear : function()
		{
			var data = {};
			var prefix = '';
			var id = this.attr('id')
			if($.fn.webgisform.options[id] && $.fn.webgisform.options[id].prefix) prefix = $.fn.webgisform.options[id].prefix;
			//for(var k in data)
			//{
				//this.find('#' + prefix + k).val(data[k]);
			//}
			var fields = $.fn.webgisform.fields[this.attr('id')];
			for(var k in fields)
			{
				var id = fields[k]['id'];
				var typ = fields[k]['type'];
				var editor = fields[k]['editor'];
				if(typ === 'icon')
				{
					//data = 
					////console.log(data);
					//if(data['style'] && data['style']['icon'] && data['style']['icon']['uri'])
					//{
						////this.find('#' + prefix + id).css('background', '#000000 url(/' + data['style']['icon']['uri'] + ') 100% 100% no-repeat' );
						//var cls = 'icon-selector-' + data['webgis_type'] + ' ui-selectee';
						//this.find('#' + prefix + id).attr('class', '');
						//this.find('#' + prefix + id).addClass(cls);
					//}
				
				}
				else if(typ === 'color')
				{
					//if(data['style'] && data['style'][id])
					//{
						this.find('#' + prefix + id).spectrum("set", ColorArrayToRgba([255, 255, 255, 255]));
					//}
				}
				else if(typ === 'date')
				{
					//if(data[id])
					//{
						//this.find('#' + prefix + id).datepicker("setDate",  data[id]);
					//}
				}
				else if(typ === 'select')
				{
					//if(editor && editor.data && editor.data.length>0 && data[id])
					//{
						this.find('#' + prefix + id).multipleSelect("setSelects", []);
					//}
				}
				else if(typ === 'multiselect')
				{
					//if(editor && editor.data && editor.data.length>0 && data[id] && data[id] instanceof Array)
					//{
						this.find('#' + prefix + id).multipleSelect("setSelects", []);
					//}
				}
				else
				{
					if(id==='pixel_size' || id==='pixel_width' || id==='label_scale')
					{
						//if(data['style'] && data['style'][id])
						//{
							this.find('#' + prefix + id).val(0);
						//}
					}
					else
						this.find('#' + prefix + id).val('');
				}
			}
			return this;
		},
		setdata : function(data)
		{
			var prefix = '';
			var id = this.attr('id')
			if($.fn.webgisform.options[id] && $.fn.webgisform.options[id].prefix) prefix = $.fn.webgisform.options[id].prefix;
			//for(var k in data)
			//{
				//this.find('#' + prefix + k).val(data[k]);
			//}
			var fields = $.fn.webgisform.fields[this.attr('id')];
			for(var k in fields)
			{
				var id = fields[k]['id'];
				var typ = fields[k]['type'];
				var editor = fields[k]['editor'];
				if(typ === 'icon')
				{
					//console.log(data);
					if(data['style'] && data['style']['icon'] && data['style']['icon']['uri'])
					{
						//this.find('#' + prefix + id).css('background', '#000000 url(/' + data['style']['icon']['uri'] + ') 100% 100% no-repeat' );
						var cls = 'icon-selector-' + data['webgis_type'] + ' ui-selectee';
						this.find('#' + prefix + id).attr('class', '');
						this.find('#' + prefix + id).addClass(cls);
					}
				
				}
				else if(typ === 'color')
				{
					if(data['style'] && data['style'][id])
					{
						this.find('#' + prefix + id).spectrum("set", ColorArrayToRgba(data['style'][id]));
					}
				}
				else if(typ === 'date')
				{
					if(data[id])
					{
						this.find('#' + prefix + id).datepicker("setDate",  data[id]);
					}
				}
				else if(typ === 'select')
				{
					if(editor && editor.data && editor.data.length>0 && data[id])
					{
						this.find('#' + prefix + id).multipleSelect("setSelects", [data[id]]);
					}
				}
				else if(typ === 'multiselect')
				{
					if(editor && editor.data && editor.data.length>0 && data[id] && data[id] instanceof Array)
					{
						this.find('#' + prefix + id).multipleSelect("setSelects", data[id]);
					}
				}
				else if(data[id])
				{
					if(id==='pixel_size' || id==='pixel_width' || id==='label_scale')
					{
						if(data['style'] && data['style'][id])
						{
							this.find('#' + prefix + id).val(data['style'][id]);
						}
					}
					else
						this.find('#' + prefix + id).val(data[id]);
				}
			}
			return this;
		},
		getdata:function()
		{
			var isInt = function(n){
				return typeof n== "number" && isFinite(n) && n%1===0;
			}			
			var prefix = '';
			if($.fn.webgisform.options[this.attr('id')].prefix) prefix = $.fn.webgisform.options[this.attr('id')].prefix;
			var fields = $.fn.webgisform.fields[this.attr('id')];
			var ret = {};
			for(var k in fields)
			{
				var id = fields[k]['id'];
				//if(id === 'icon')
				//{
					//ret[id] = this.find('#' + prefix + id).attr('class').replace('icon-selector-', '').replace(' ui-selectee', '');
				//}
				//else
				//{
				
				//}
				var typ = fields[k]['type'];
				if(typ === 'icon')
				{
					if(!ret['style']) ret['style'] = {};
					if(!ret['style']['icon']) ret['style']['icon'] = {};
					var c = this.find('#' + prefix + id).attr('class').replace('icon-selector-', '').replace(' ui-selectee', '');
					var icon_img = GetDefaultStyleValue(c, 'icon_img');
					ret['style']['icon']['uri'] = icon_img;
				}
				else if(typ === 'color')
				{
					if(!ret['style']) ret['style'] = {};
					ret['style'][id] = ColorRgbaToArray(this.find('#' + prefix + id).spectrum("get").toRgbString());
				}
				else if(typ === 'date')
				{
					ret[id] = this.find('#' + prefix + id).datepicker("getDate");
				}
				else if(typ === 'spinner')
				{
					if(id==='pixel_size' || id==='pixel_width' || id==='label_scale')
					{
						var v = this.find('#' + prefix + id).val();
						if(v>0)
						{
							if(isInt(v)) 
							{
								ret['style'][id]  = parseInt(v);
							}else
							{
								ret['style'][id] = parseFloat(v);
							}
						}
					}
					else
					{
						ret[id] = this.find('#' + prefix + id).val();
						if(ret[id].length>0)
						{
							if(isInt(ret[id])) 
							{
								ret[id] = parseInt(ret[id]);
							}else
							{
								ret[id] = parseFloat(ret[id]);
							}
						}else
							delete ret[id] ;
					}
				}
				else if(typ === 'select')
				{
					ret[id] = null;
					var arr = this.find('#' + prefix + id).multipleSelect("getSelects");
					if(arr.length>0)
					{
						ret[id] = arr[0];
					}
				}
				else if(typ === 'multiselect')
				{
					ret[id] = this.find('#' + prefix + id).multipleSelect("getSelects");
				}
				else
				{
					ret[id] = this.find('#' + prefix + id).val();
				}
			}
			return ret;
		},
		get:function(id)
		{
			var prefix = '';
			var ret ;
			if($.fn.webgisform.options[this.attr('id')] && $.fn.webgisform.options[this.attr('id')].prefix)
			{
				prefix = $.fn.webgisform.options[this.attr('id')].prefix;
				ret = this.find('#' + prefix + id);
			}
			return ret;
		},
		set:function(id, value)
		{
			var prefix = '';
			if($.fn.webgisform.options[this.attr('id')].prefix) prefix = $.fn.webgisform.options[this.attr('id')].prefix;
			var ret = this.find('#' + prefix + id);
			if(ret.length>0)
			{
				ret.val(value);
			}
			return this;
		}
		//getdefaultvalue:function(fld_id)
		//{
			//var id = this.attr('id');
			//var prefix = '';
			//if($.fn.webgisform.options[id].prefix) prefix = $.fn.webgisform.options[id].prefix;
			//var ret = null;
			//for(var i in $.fn.webgisform.fields[id])
			//{
				//var fld = $.fn.webgisform.fields[id][i];
				//if(fld.id === fld_id)
				//{
					//if(fld.type === 'text')
					//{
						//ret = '(无)';
					//}
					//if(fld.type === 'spinner')
					//{
						//ret = fld.min;
					//}
					//if(fld.type === 'date')
					//{
						
					//}
					//break;
				//}
			//}
			//return ret;
		//}
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
		divorspan:"div",
		labelwidth : 90,
		margin : 10.0/2,
		groupmargin : 18.0/2,
		iconsource:[]
	};
}

function ColorArrayToRgba(array)
{
	var ret = 'rgba(255,255,255,1)';
	if(array.length == 4 && Math.floor(array[0])<256  && Math.floor(array[1])<256  && Math.floor(array[2])<256  && Math.floor(array[3])<256 )
	{
		ret = 'rgba(' + Math.floor(array[0]) + ', ' +  Math.floor(array[1]) + ', ' +  Math.floor(array[2]) + ', ' +  (array[3]/256) + ')';
	}
	return ret;
}


function GetDefaultStyleValue(type, stylename)
{
	var mapping = $.webgis.style_mapping[type];
	//if(type.indexOf('point_')>-1) mapping = g_style_point_mapping[type];
	//if(type.indexOf('polyline_')>-1) mapping = g_style_polyline_mapping[type];
	//if(type.indexOf('polygon_')>-1) mapping = g_style_polygon_mapping[type];
	var ret = [255, 0, 0, 128];
	if(stylename==='pixelSize' ) ret = 3;
	if(stylename==='outlineWidth') ret = 1;
	if(stylename==='labelScale') ret = 1;
	if(stylename==='width') ret = 1;
	if(mapping[stylename]) ret = mapping[stylename];
	return ret;
}

function ColorRgbaToArray(rgbastr)
{
	var c = tinycolor(rgbastr);
	//var a = Math.floor(c.getAlpha()*256-1);
	var rgba = c.toRgb();
	return [rgba.r, rgba.g, rgba.b, Math.floor(rgba.a*256-1)];
}

function ColorArrayToHTMLColor(array)
{
	var rgbastr = ColorArrayToRgba(array)
	var c = tinycolor(rgbastr);
	var ret = c.toHexString();
	return ret;
}


function MongoFind(data, success, host)
{
	//$.ajaxSetup( { "async": true, scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8" } );
	var h = '';
	if(host) h = host;
	var url = h + 'post';
	if(data.url) url = h + data.url;
	//console.log(data);
	$.post(url, encodeURIComponent(JSON.stringify(data)), function( data1 ){
		//console.log(data1);
		//if(data.redirect) return;
		ret = JSON.parse(decodeURIComponent(data1));
		if(success)
		{
			success(ret);
		}
	}, 'text');
}

function GridFsFind(data, success, isdownload)
{
	//$.ajaxSetup( { "async": true, scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8" } );
	//console.log(data);
	if(isdownload)
	{
		$.get('get', data, function( data1 ){
			success(data1);
		});
	}else
	{
		$.getJSON('get', data, function( data1 ){
			success(data1);
		});
	}
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


function ShowProgressBar(show, width, height, title, msg)
{
	$('#dlg_progress_bar').remove();
	if(show)
	{
		$('body').append('<div id="dlg_progress_bar"></div>');
		$('#dlg_progress_bar').append('<div id="div_progress_msg"></div>').html(msg);
		$('#dlg_progress_bar').append('<div id="div_progress_bar"><span class="progressbartext" style="width:95%;"></span></div>');
		$('#dlg_progress_bar').dialog({
			width: width,
			height: height,
			draggable: false,
			resizable: false, 
			modal: true,
			title:title
		});
		$.webgis.progress_value = 0;
		$('#div_progress_bar').progressbar({
			max:100,
			value:0
		});
		$.webgis.progress_interval = setInterval(function(){
			$.webgis.progress_value += 1;
			if($.webgis.progress_value > 100) $.webgis.progress_value = 100;
			try
			{
				$('#div_progress_bar').progressbar('value', $.webgis.progress_value);
				$("#div_progress_bar span.progressbartext").text($.webgis.progress_value + "%");
			}catch(e)
			{
				clearInterval($.webgis.progress_interval);
			}
		}, 100);
	}
	else{
		//document.body.className = document.body.className.replace(/(?:\s|^)loading(?:\s|$)/, ' ');
		clearInterval($.webgis.progress_interval);
		try
		{
			$('#div_progress_bar').progressbar('destroy');
			$('#dlg_progress_bar').dialog('close');
		}catch(e)
		{
		}
	}
}

function ShowConfirm(id, width, height, title, msg, ok, cancel, thumbnail)
{
	if(thumbnail)
	{
		var s = '<div style="vertical-align: middle;line-height: ' + 40 + 'px;">' + msg  + '</div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + '<img  src="data:' + thumbnail.mimetype + ';base64,' + thumbnail.data + '" />';
		if(id)
		{
			$('#' + id ).empty();
			$('#' + id ).append('<div></div>');
			$('#' + id + ' div').html(s);
		}else
		{
			id = 'dlgconfirmdynamic';
			$('body').append('<div id="' + id + '"><div></div></div>');
			$('#' + id + ' div').html(s);
		}
	}else
	{
		if(id)
		{
			$('#' + id ).empty();
			$('#' + id ).append('<div></div>');
			$('#' + id + ' div').html(msg);
		}else
		{
			id = 'dlgconfirmdynamic';
			$('body').append('<div id="' + id + '"><div></div></div>');
			$('#' + id + ' div').html(msg);
		}
	}
	$('#' + id).dialog({
		title:title,
		closeOnEscape: false,
		modal:true,
		draggable:true,
		width:width,
		height:height,
		buttons: [ 
			{  	text: "确定", 
				click: function() { 
					$( this ).dialog( "close" ); 
					$('#dlgconfirmdynamic').remove();
					 if(ok) ok();
				}
			},
			{	text: "取消", 
				click: function() { 
					$( this ).dialog( "close" );
					$('#dlgconfirmdynamic').remove();
					if(cancel) cancel();
				} 
			}]
	});
}

function GetDisplayLatLngString(ellipsoid, cartesian, precision) 
{
	if(!cartesian) return "";
	var cartographic = ellipsoid.cartesianToCartographic(cartesian);
	if(cartographic.longitude &&  cartographic.latitude)
	{
		var height = 0;
		if(Math.abs(cartographic.height) > Cesium.Math.EPSILON1) height =  Math.floor(cartographic.height);
		var s = "(" + Cesium.Math.toDegrees(cartographic.longitude).toFixed(precision || 3) + ", " + Cesium.Math.toDegrees(cartographic.latitude).toFixed(precision || 3) + ")";
		if(g_zaware)
		{
			s =  "(" + Cesium.Math.toDegrees(cartographic.longitude).toFixed(precision || 3) + ", " + Cesium.Math.toDegrees(cartographic.latitude).toFixed(precision || 3) + ", " + height + ")";
		}
		return s;
	}else
	{
		return "";
	}
}


function GetDisplayLatLngString2D(latlng, precision) 
{
	if(!latlng) return "";
	var s = "(" + latlng.lng.toFixed(precision || 3) + ", " + latlng.lat.toFixed(precision || 3) + ")";
	return s;
}

function ShowMessage(id, width, height, title, msg, ok)
{
	if(id)
	{
		$('#' + id ).empty();
		$('#' + id ).append('<div></div>');
		$('#' + id + ' div').html(msg);
	}else
	{
		id = 'dlgmsgdynamic';
		$('body').append('<div id="' + id + '"><div></div></div>');
		$('#' + id + ' div').html(msg);
	}
	console.log(msg);

	$('#' + id).dialog({
		title:title,
		closeOnEscape: false,
		modal:true,
		draggable:true,
		width:width,
		height:height,
		buttons: [ 
			{  	text: "确定", 
				click: function() { 
					$( this ).dialog( "close" );
					$('#dlgmsgdynamic').remove();
					if(ok) ok();
				}
			}]
	});
}

function GetZfromXY(lng, lat, callback)
{
	//$.ajaxSetup( { "async": true, scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8" } );
	var data = {op:'alt', lng:lng, lat:lat};
	$.post('post', encodeURIComponent(JSON.stringify(data)), function( data1 ){
		ret = JSON.parse(decodeURIComponent(data1));
		callback(ret);
	}, 'text');
}

function GetZListfromXYList(list, callback)
{
	//$.ajaxSetup( { "async": true, scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8" } );
	var data = {op:'alt', data:list};
	$.post('post', encodeURIComponent(JSON.stringify(data)), function( data1 ){
		ret = JSON.parse(decodeURIComponent(data1));
		callback(ret);
	}, 'text');
}

function ShowGeoTip(id, position, msg)
{
	//try{
		//$('div[id^=geotipinfo_]').tooltipster('destroy');
	//}catch(e) {}
	$('div[id^=geotipinfo_]').remove();
	
	if(id)
	{
		//$('body').append('<div class="twipsy right" style="position: absolute;top:' + position.y + 'px;left:' + position.x + 'px" id="geotipinfo_' + id + '"><div class="twipsy-arrow"></div><div class="twipsy-inner">' + msg + '</div></div>');
		//$('#geotipinfo_' + id ).tooltipster({ 
			//contentAsHTML: true,
			//animation: 'fade',//fade, grow, swing, slide, fall
			//trigger: 'custom',
			//onlyOne: true, 
			//position: 'top-right',//right, left, top, top-right, top-left, bottom, bottom-right, bottom-left
			////theme: 'tooltipster-noir',
			//offsetX: 0,
			//offsetY: 0
		//});
		
		$('body').append('<div class="qtip-content ui-widget-content" style="position: absolute;top:' + position.y + 'px;left:' + (position.x + 20) + 'px" id="geotipinfo_' + id + '">' + msg + '</div>');
		//$('#geotipinfo_' + id ).qtip({ 
			//content: {
				//text: msg
			//}
		//});
	}
}

function PickLngLatFromScreen(viewer, screen_position)
{
	var ellipsoid = viewer.scene.globe.ellipsoid;
	var scene = viewer.scene;
	var ray = scene.camera.getPickRay(screen_position);
	var cartesian = scene.globe.pick(ray, scene);
	//var carto = ellipsoid.cartesianToCartographic(cartesian);
	var s = GetDisplayLatLngString(ellipsoid, cartesian, 6);
	//console.log(s);
	return s;
}

function ToWebMercator(cartographic)
{
    if (Math.abs(cartographic.longitude) > 180 * 0.017453292519943295 || Math.abs(cartographic.latitude) > 90 * 0.017453292519943295)
	{
        return [0.0, 0.0];
	}
    var x = 6378137.0 * cartographic.longitude;
    var y = 3189068.5 * Math.log((1.0 + Math.sin(cartographic.latitude)) / (1.0 - Math.sin(cartographic.latitude)));
    return [x, y];
}


function GetDenomiHeightByModelCode(model_code_height)
{
	var ret;
	if(model_code_height && model_code_height.length>0)
	{
		var idx = model_code_height.lastIndexOf("_");
		var num1 = model_code_height.substr(idx+1);
		var rest = model_code_height.slice(0, idx);
		idx = rest.lastIndexOf("_");
		var num2 = rest.substr(idx+1);
		var h = num2 + '.' + num1;
		ret = parseFloat(h);
	}
	return ret;
}
function GetMCByModelCode(model_code_height)
{
	var ret;
	if(model_code_height && model_code_height.length>0)
	{
		var idx = model_code_height.lastIndexOf("_");
		var rest = model_code_height.slice(0, idx);
		idx = rest.lastIndexOf("_");
		ret= rest.slice(0, idx);
	}
	return ret;
}

function CheckInternetConnection()
{
	return CheckUrlExist('http://www.baidu.com');
}
function CheckIntranetConnection()
{
	return CheckUrlExist('http://' + $.webgis.host + ':' + $.webgis.port);
}


function CheckUrlExist(url)
{
	var ret = false;
	try
	{
		var http = new XMLHttpRequest();
		http.open('HEAD', url, false);
		http.send();
		if(http.status>= 200 && http.status < 304)
		{
			ret = true;
		}else
		{
			ret = false;
		}
	}catch(e){
        ret = false;
    }
	return ret;
}


function get_geojson_center(geojson)
{
	var ret = [];
	if(geojson.geometry.type === 'Point')
	{
		ret.push(geojson.geometry.coordinates[0]);
		ret.push(geojson.geometry.coordinates[1]);
	}
	else if(geojson.geometry.type === 'LineString')
	{
		var idx = Math.floor(geojson.geometry.coordinates.length/2);
		ret.push(geojson.geometry.coordinates[idx][0]);
		ret.push(geojson.geometry.coordinates[idx][1]);
	}
	else if(geojson.geometry.type === 'Polygon')
	{
		var x=0, y=0;
		for(var i in geojson.geometry.coordinates[0])
		{
			x += geojson.geometry.coordinates[0][i][0];
			y += geojson.geometry.coordinates[0][i][1];
		}
		ret.push(x/geojson.geometry.coordinates[0].length);
		ret.push(y/geojson.geometry.coordinates[0].length);
	}
	return ret;
}

