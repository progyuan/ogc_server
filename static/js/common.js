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
			$.fn.webgisform.fields = fields;
			this.groups = [];
			this.options = $.extend({}, $.fn.webgisform.defaults, options);
			$.fn.webgisform.options = this.options;
			this.empty();
			var prefix = '';
			if($.fn.webgisform.options.prefix) prefix = $.fn.webgisform.options.prefix;
			
			
			var debug = true;
			if($.fn.webgisform.options.debug) debug = $.fn.webgisform.options.debug;
			this.validate({
				debug:debug,
				errorElement:'div'
			});
			
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
				var g = this.append('<fieldset id="fieldset_' + uid + '" style="color:#00FF00;border:1px solid #00FF00;margin:' + this.options.groupmargin + 'px;"><legend style="font-weight:bolder;color:#00FF00;">' + group + '</legend>');
				this.append('</fieldset>');
				this.append('<p></p>');
				
				for(var i in fields)
				{
					var fld = fields[i];
					var fldid = prefix + fld.id;
					
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
						
						$('#' + 'fieldset_' + uid).append('<div style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input  style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '">' + validate + '</div>');
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
						$('#' + 'fieldset_' + uid).append('<div style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input  style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '">' + validate + '</div>');
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
						$('#' + 'fieldset_' + uid).append('<div style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><input type="text" class="ui-widget" style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '" ' + readonly + '>' + validate + '</div>');
					}
					if(fld.type == 'select' && fld.group == group)
					{
						var source = [];
						if(fld.editor && fld.editor.data) source = fld.editor.data;
						$('#' + 'fieldset_' + uid).append('<div style="margin:' + this.options.margin + 'px;' + newline + '"><label for="' + fldid + '" style="display:inline-block;text-align:right;width:' + this.options.labelwidth + 'px;">' + fld.display + ':' + '</label><select  style="width:' + fld.width + 'px;" id="' + fldid + '" name="' + fldid + '"></select>' + validate + '</div>');
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
					
				}
			}
			
			var fields = this.fields;
			for(var i in fields)
			{
				var fld = fields[i];
				var fldid = prefix + fld.id;
				if(fld.validate)
				{
					if($('input[name="' + fldid + '"]').length>0)
					{
						$('input[name="' + fldid + '"]').rules('add',fld.validate);
					}
					if($('select[name="' + fldid + '"]').length>0)
					{
						$('select[name="' + fldid + '"]').rules('add',fld.validate);
					}
				}
			}
			return this;
		},
		setdata : function(data)
		{
			var prefix = '';
			if($.fn.webgisform.options.prefix) prefix = $.fn.webgisform.options.prefix;
			for(var k in data)
			{
				this.find('#' + prefix + k).val(data[k]);
			}
			return this;
		},
		getdata:function()
		{
			var prefix = '';
			if($.fn.webgisform.options.prefix) prefix = $.fn.webgisform.options.prefix;
			var fields = $.fn.webgisform.fields;
			var ret = {};
			for(var i in fields)
			{
				var id = fields[i]['id'];
				ret[id] = this.find('#' + prefix + id).val();
				if(id === 'tower_name')
				{
					ret[id] = ret[id].split(',')[0]; 
				}
				
			}
			return ret;
		},
		get:function(id)
		{
			var prefix = '';
			if($.fn.webgisform.options.prefix) prefix = $.fn.webgisform.options.prefix;
			var ret = this.find('#' + prefix + id);
			return ret;
		}
		//getvalidate:function(ad)
		//{
			//var debug = true;
			//if(ad) debug = ad;
			//var ret = this.validate({
				//debug:debug,
				//errorElement:'div'
			//});
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
		labelwidth : 90,
		margin : 10.0/2,
		groupmargin : 18.0/2
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
