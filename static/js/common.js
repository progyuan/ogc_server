//var g_host = "http://localhost:88/";
var g_host = "";
//var g_db_name = 'kmgd';
var g_db_name = 'ztgd';
var g_progress_interval;
var g_progress_value;
var g_phase_color_mapping = {
	'A':'#FFFF00',
	'B':'#FF0000',
	'C':'#00FF00',
	'G':'#000000',
	'G1':'#000000',
	'L':'#000000',
	'R':'#000000'
};

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
					var newline = "float:left;";
					if(fld.newline == false) newline = "";
					var required = '';
					if(fld.validate && fld.validate.required)
					{
						required = '<span  style="color:#FF0000;">*</span>';
					}
					if(fld.type == 'spinner' && fld.group == group)
					{
						
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input  style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '">' + required + '</' + divorspan + '>');
						var spin = 	$('#' + fldid).spinner({
							step: fld.step,
							max:fld.max,
							min:fld.min,
							change:fld.change,
							spin:fld.spin
						});
					}
					if(fld.type == 'geographic' && fld.group == group)
					{
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input  style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '">' + required + '</' + divorspan + '>');
						var spin = 	$('#' + fldid).spinner({
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
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input type="text" class="ui-widget" style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '" ' + readonly + '>' + required + '</' + divorspan + '>');
					}
					if(fld.type == 'select' && fld.group == group)
					{
						var source = [];
						if(fld.editor && fld.editor.data) source = fld.editor.data;
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><select  style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '"></select>' + required + '</' + divorspan + '>');
						for(var ii in source)
						{
							$('#' + fldid).append('<option value="' + source[ii]['value'] + '">' + source[ii]['label'] + '</option>');
						}
						var auto = $('#' + fldid).autocomplete({
							//appendTo:'#' + fldid,
							//position: { my: "left top", at: "left bottom", collision: "none" },
							autoFocus: false,
							source:source
						});
						
					}
					if(fld.type == 'date' && fld.group == group)
					{
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input type="text" class="ui-widget" style="padding:7px 0px 0px 0px;width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '" ' + readonly + '>'  + required + '</' + divorspan + '>');
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
					}
					if(fld.type == 'icon' && fld.group == group)
					{
						$('#' + 'fieldset_' + uid).append('<' + divorspan + ' style="margin:' + this.options.margin + 'px;' + newline 
						+ '"><label for="input_' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display 
						+ ':' 
						+ '</label><' + divorspan + ' style="display:inline-block;width:64px;height:64px;border:1px #00FF00 solid;" id="' + fldid + '" name="' + fldid + '" ></' + divorspan + '>' + required 
						+ '<ol class="kmgd-icon-selectable"  id="ol_' + fldid + '"></ol></' + divorspan + '>');
						$('#ol_' + fldid ).css('display', 'none');
						$('#' + fldid ).addClass('icon-selector-' + fld.iconvalue);
						
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
					
				}
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
		setdata : function(data)
		{
			var prefix = '';
			if($.fn.webgisform.options[this.attr('id')].prefix) prefix = $.fn.webgisform.options[this.attr('id')].prefix;
			for(var k in data)
			{
				this.find('#' + prefix + k).val(data[k]);
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
				if(id === 'icon')
				{
					ret[id] = this.find('#' + prefix + id).attr('class').replace('icon-selector-', '').replace(' ui-selectee', '');
				}
				else
				{
					ret[id] = this.find('#' + prefix + id).val();
				}
				var typ = fields[k]['type'];
				if(typ === 'spinner')
				{
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
						ret[id] = 0;
				}
			}
			return ret;
		},
		get:function(id)
		{
			var prefix = '';
			if($.fn.webgisform.options[this.attr('id')].prefix) prefix = $.fn.webgisform.options[this.attr('id')].prefix;
			var ret = this.find('#' + prefix + id);
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

function MongoFind(data, success, host)
{
	//$.ajaxSetup( { "async": true, scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8" } );
	var h = '';
	if(host) h = host;
	$.post(h + 'post', encodeURIComponent(JSON.stringify(data)), function( data1 ){
		ret = JSON.parse(decodeURIComponent(data1));
		if(ret.result)
		{
			//ShowMessage(400, 250, '信息', ret.result);
			success([]);
		}
		else
		{
			success(ret);
		}
	}, 'text');
}
function GridFsFind(data, success)
{
	//$.ajaxSetup( { "async": true, scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8" } );
	$.getJSON(g_host + 'get', data, function( data1 ){
		success(data1);
	});
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
	if(show)
	{
		$('#div_progress_msg').html(msg);
		$('#dlg_progress_bar').dialog({
			width: width,
			height: height,
			draggable: false,
			resizable: false, 
			modal: true,
			title:title
		});
		g_progress_value = 0;
		$('#div_progress_bar').progressbar({
			max:100,
			value:0
		});
		g_progress_interval = setInterval(function(){
			g_progress_value += 1;
			if(g_progress_value > 100) g_progress_value = 100;
			try
			{
				$('#div_progress_bar').progressbar('value', g_progress_value);
				$("#div_progress_bar span.progressbartext").text(g_progress_value + "%");
			}catch(e)
			{
				clearInterval(g_progress_interval);
			}
		}, 100);
	}
	else{
		//document.body.className = document.body.className.replace(/(?:\s|^)loading(?:\s|$)/, ' ');
		clearInterval(g_progress_interval);
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
		$('#' + id + ' div').html(s);
	}else
	{
		$('#' + id + ' div').html(msg);
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
					 if(ok) ok();
				}
			},
			{	text: "取消", 
				click: function() { 
					$( this ).dialog( "close" );
					if(cancel) cancel();
				} 
			}]
	});
}

function GetDisplayLatLngString(ellipsoid, cartesian, precision) 
{
	var cartographic = ellipsoid.cartesianToCartographic(cartesian);
	if(cartographic.longitude &&  cartographic.latitude)
	{
		var height = 0;
		if(Math.abs(cartographic.height) > Cesium.Math.EPSILON1) height =  Math.floor(cartographic.height);
		return "(" + Cesium.Math.toDegrees(cartographic.longitude).toFixed(precision || 3) + ", " + Cesium.Math.toDegrees(cartographic.latitude).toFixed(precision || 3) + ", " + height + ")";
	}else
	{
		return "";
	}
}

function ShowMessage(id, width, height, title, msg, ok)
{
	$('#' + id + ' div').html(msg);
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
					 if(ok) ok();
				}
			}]
	});
}

function GetZfromXY(lng, lat, callback)
{
	//$.ajaxSetup( { "async": true, scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8" } );
	var data = {op:'alt', lng:lng, lat:lat};
	$.post(g_host + 'post', encodeURIComponent(JSON.stringify(data)), function( data1 ){
		ret = JSON.parse(decodeURIComponent(data1));
		callback(ret);
	}, 'text');
}

function GetZListfromXYList(list, callback)
{
	//$.ajaxSetup( { "async": true, scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8" } );
	var data = {op:'alt', data:list};
	$.post(g_host + 'post', encodeURIComponent(JSON.stringify(data)), function( data1 ){
		ret = JSON.parse(decodeURIComponent(data1));
		callback(ret);
	}, 'text');
}
