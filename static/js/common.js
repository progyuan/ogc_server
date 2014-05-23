//var g_host = "http://localhost:88/";
var g_host = "";
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


function MongoFind(data, success)
{
	//$.ajaxSetup( { "async": true, scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8" } );
	$.post(g_host + 'post', JSON.stringify(data), function( data1 ){
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
			$('#div_progress_bar').progressbar('value', g_progress_value);
			$("#div_progress_bar span.progressbartext").text(g_progress_value + "%");
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

function ShowConfirm(width, height, title, msg, ok, cancel)
{
	$('#dlg_confirm div').html(msg);
	$('#dlg_confirm').dialog({
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

function ShowMessage(width, height, title, msg, ok)
{
	$('#dlg_message div').html(msg);
	console.log(msg);

	$('#dlg_message').dialog({
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

