$.webgis.editor = {};
$.webgis.editor.elapsed_time = 0.0;
$.webgis.editor.is_add_seg = false;
$.webgis.editor.cp_pair = [];

$.webgis.editor.segments = [];
$.webgis.editor.segments_editting = [];
$.webgis.editor.off_x = 15;
$.webgis.editor.off_z = 30;
$.webgis.editor.contact_points = [];


$(function() {
	InitWebGISFormDefinition();
	ShowProgressBar(true, 400, 150, '载入中', '正在载入，请稍候...');
	var param = GetParamsFromUrl();
	if(param['url_next'])
	{
		$.webgis.editor.mode = 'segs';
		$.webgis.editor.next_ids = param['next_ids'];
		$.webgis.editor.segments = param['segments'];
		for(var i in $.webgis.editor.segments)
		{
			$.webgis.editor.segments_editting.push( $.extend(true, {}, $.webgis.editor.segments[i]));
		}
		
	}else
	{
		$.webgis.editor.mode = 'tower';
	}

	window.URL = window.URL || window.webkitURL;
	window.BlobBuilder = window.BlobBuilder || window.WebKitBlobBuilder || window.MozBlobBuilder;

	var editor = new Editor();
	var viewport = new Viewport( editor );
	var viewportdom = viewport.container.setId( 'viewport' );
	document.body.appendChild( viewportdom.dom );

	//var toolbar = new Toolbar( editor ).setId( 'toolbar' )
	//document.body.appendChild( toolbar.dom );

	//var menubar = new Menubar( editor ).setId( 'menubar' );
	//document.body.appendChild( menubar.dom );

	//var sidebar = new Sidebar( editor ).setId( 'sidebar' );
	//document.body.appendChild( sidebar.dom );

	//

	//editor.setTheme( editor.config.getKey( 'theme' ) );
	editor.setTheme( 'css/dark.css' );

	if(false)
	{
		editor.storage.init( function () {
	
			editor.storage.get( function ( state ) {
	
				if ( state !== undefined ) {
	
					var loader = new THREE.ObjectLoader();
					var scene = loader.parse( state );
	
					editor.setScene( scene );
	
				}
	
				var selected = editor.config.getKey( 'selected' );
	
				if ( selected !== undefined ) {
	
					editor.selectByUuid( selected );
	
				}
	
			} );
	
			
	
			var timeout;
			var exporter = new THREE.ObjectExporter();
	
			var saveState = function ( scene ) {
	
				clearTimeout( timeout );
	
				timeout = setTimeout( function () {
	
					editor.storage.set( exporter.parse( editor.scene ) );
	
				}, 1000 );
	
			};
			

			var signals = editor.signals;
	
			signals.objectAdded.add( saveState );
			signals.objectChanged.add( saveState );
			signals.objectRemoved.add( saveState );
			signals.materialChanged.add( saveState );
			signals.sceneGraphChanged.add( saveState );
	
		});
	}
	

	var OnSelected = function(obj)
	{
		ShowLabelBySelected(editor);
		if($.webgis.editor.mode == 'tower')
		{
			$('[id^="button_"]').css('display','none');
			if(obj && obj['userData'] && obj['userData']['type'] && obj['userData']['type'] == 'contact_point')
			{
				$('#div_contact_point_coords').css('display','block');
				$('#button_cp_del').css('display','block');
			}else
			{
				$('#div_contact_point_coords').css('display','none');
				$('#button_cp_add').css('display','block');
				$('#button_cp_save').css('display','block');
				$('#button_cp_side').css('display','block');
			}
		}
		if($.webgis.editor.mode == 'segs')
		{
			if($.webgis.editor.is_add_seg)
			{
				if(obj && obj['userData'] && obj['userData']['type'] && obj['userData']['type'] == 'contact_point')
				{
					$.webgis.editor.cp_pair.push({'tower_id':obj['userData']['tower_id'],'data':obj['userData']['data']});
					if($.webgis.editor.cp_pair.length == 2)
					{
						var side1 = $.webgis.editor.cp_pair[0].data.side,
							side2 = $.webgis.editor.cp_pair[1].data.side;
						var t1 = $.webgis.editor.cp_pair[0].tower_id,
							t2 = $.webgis.editor.cp_pair[1].tower_id;
						var i1 = $.webgis.editor.cp_pair[0].data.contact_index,
							i2 = $.webgis.editor.cp_pair[1].data.contact_index;
						if(side1 != side2 && t1 != t2)
						{
							var b = CheckSegExist(t1, t2, side1, side2, i1, i2);
							console.log(b);
							if(!b)
							{
								var phase = $('#button_phase :radio:checked').attr('id');
								phase = phase.substr(phase.indexOf('_') + 1);
								console.log(t1 + ':side(' + side1 + '):index(' + i1 + '):phase(' + phase + ')<--->' + t2 + ':side(' + side2 + '):index(' + i2 + '):phase(' + phase + ')');
								var color = parseInt(tinycolor($.webgis.mapping.phase_color_mapping[phase]).toHex(), 16);
								var seg = {start_tower:t1, end_tower:t2, start_side:side1, end_side:side2},
									cp = {start:i1, end:i2, phase:phase};
								var start,  end, end1, end2;
								var offset_x = $.webgis.editor.off_x, offset_z = $.webgis.editor.off_z;
								if(side1 === 1)
								{
									start = GetDrawInfoFromContactPoint(1, i1, $.webgis.editor.cpdata, 0, offset_z);
									if($.webgis.editor.cpdata_next.length==1)
									{
										end = GetDrawInfoFromContactPoint(0, i2, $.webgis.editor.cpdata_next[0], 0, -offset_z);
									}
									if($.webgis.editor.cpdata_next.length==2)
									{
										for(var j in $.webgis.editor.next_ids)
										{
											if(t2 == $.webgis.editor.next_ids[j])
											{
												if(j==0) end1 = GetDrawInfoFromContactPoint(0, i2, $.webgis.editor.cpdata_next[0], -offset_x, -offset_z);
												if(j==1) end2 = GetDrawInfoFromContactPoint(0, i2, $.webgis.editor.cpdata_next[1], offset_x, -offset_z);
											}
										}
									}
								}
								if(side1 === 0)
								{
									seg = {start_tower:t2, end_tower:t1, start_side:side2, end_side:side1};
									cp = {start:i2, end:i1, phase:phase};
									start = GetDrawInfoFromContactPoint(1,  i2,  $.webgis.editor.cpdata, 0, offset_z);
									if($.webgis.editor.cpdata_next.length==1)
									{
										end = GetDrawInfoFromContactPoint(0, i1, $.webgis.editor.cpdata_next[0], 0, -offset_z);
									}
									if($.webgis.editor.cpdata_next.length==2)
									{
										for(var j in $.webgis.editor.next_ids)
										{
											if(t1 == $.webgis.editor.next_ids[j])
											{
												if(j==0) end1 = GetDrawInfoFromContactPoint(0, i1, $.webgis.editor.cpdata_next[0], -offset_x, -offset_z);
												if(j==1) end2 = GetDrawInfoFromContactPoint(0, i1, $.webgis.editor.cpdata_next[1], offset_x, -offset_z);
											}
										}
									}
								}
								if(start && end)
									DrawLine(editor, start, end, color, seg, cp);
								if(start && end1)
									DrawLine(editor, start, end1, color, seg, cp);
								if(start && end2)
									DrawLine(editor, start, end2, color, seg, cp);
								AddSeg(t1, t2, side1, side2, i1, i2, phase);
							}else
							{
								ShowMessage(null, 400, 150, '已存在','所连接的线段已经存在');
							}
						}
						$.webgis.editor.cp_pair.length = 0;
					}
				}
			}
		}
		
	};
	
	editor.signals.objectSelected.add( OnSelected );

	
	document.addEventListener( 'dragover', function ( event ) {

		event.preventDefault();
		event.dataTransfer.dropEffect = 'copy';

	}, false );

	
	$(document).mousedown(function() {
		ClearRoundCamera(viewport);
	});
	//$(window).on('message',function(e) {
		//console.log('recv:' + e.originalEvent.data);
		//console.log($.webgis.editor.camera_move_around_int);
		//ClearRoundCamera();
	//});
	
	//document.addEventListener( 'drop', function ( event ) {

		//event.preventDefault();
		//editor.loader.loadFile( event.dataTransfer.files[ 0 ] );

	//}, false );

	document.addEventListener( 'keydown', function ( event ) {
		//console.log(event.keyCode);
		switch ( event.keyCode ) {

			case 8: // prevent browser back 
				event.preventDefault();
				break;
			//case 46: // delete
				//editor.removeObject( editor.selected );
				//editor.deselect();
				//break;
			case 27: // esc
				ClearRoundCamera(viewport);
				ClearAllLabels(editor);
				break;
		}

	}, false );

	var onWindowResize = function ( event ) {
		//ClearRoundCamera();
		editor.signals.windowResize.dispatch();
	};

	window.addEventListener( 'resize', onWindowResize, false );

	onWindowResize();
	
	AddHemisphereLight(editor);
	var off_x = $.webgis.editor.off_x, off_z = $.webgis.editor.off_z;

	if($.webgis.editor.mode == 'segs')
	{
		//console.log(param['url_next']);
		param['data_next'] = [];
		var ids = [];
		ids.push(param['tower_id']);
		for(var i in param['next_ids']) ids.push(param['next_ids'][i]);
		var cond = {'db':$.webgis.db.db_name, 'collection':'features','_id':ids};
		MongoFind(cond, function(data){
			
			for(var i in data)
			{
				var d = data[i];
				if(d['_id'] === param['tower_id'])
				{
					param['data'] = d['properties']['model'];
				}
				if(d['_id'] === param['next_ids'][0])
				{
					param['data_next'].push(d['properties']['model']);
				}
				if(param['next_ids'][1] && d['_id'] === param['next_ids'][1])
				{
					param['data_next'].push(d['properties']['model']);
				}
				
			}
			
			
			$.webgis.editor.cpdata = param['data'];
			$.webgis.editor.cpdata_next = param['data_next'];
			if(param['data_next'].length==1)
			{
				LoadContactPoint(editor, param['next_ids'][0], param['data_next'][0]['contact_points'], [0, 0, -off_z], param['data_next'][0]['model_code_height']);
			}
			if(param['data_next'].length==2)
			{
				LoadContactPoint(editor, param['next_ids'][0], param['data_next'][0]['contact_points'], [-off_x, 0, -off_z], param['data_next'][0]['model_code_height']);
				LoadContactPoint(editor, param['next_ids'][1], param['data_next'][1]['contact_points'], [off_x, 0, -off_z], param['data_next'][1]['model_code_height']);
			}
			if(param['data'])
			{
				LoadContactPoint(editor, param['tower_id'], param['data']['contact_points'], [0, 0, off_z], param['data']['model_code_height']);
			}
			if(param['url'])
			{
				LoadGltfFromUrl(editor, viewport,  param['url'], [0, 0, off_z], [-90,0,0], [10,10,10], '#00FF00',
					function(target){
						if(window.parent)
						{
							if(param['data_next'].length==1)
							{
								DrawSegments(editor, param['tower_id'], param['next_ids'],  param['data'], param['data_next'], 0, off_z);
							}
							if(param['data_next'].length==2)
							{
								DrawSegments(editor, param['tower_id'], param['next_ids'], param['data'], param['data_next'], off_x, off_z);
							}
						}
						
						if(param['url_next'].length==1)
						{
							LoadGltfFromUrl(editor, viewport,  param['url_next'][0], [0, 0, -off_z], [-90,0,0], [10,10,10], '#CCFFCC');
						}
						if(param['url_next'].length==2)
						{
							LoadGltfFromUrl(editor, viewport,  param['url_next'][0], [-off_x, 0, -off_z], [-90,0,0], [10,10,10], '#CCFFCC');
							LoadGltfFromUrl(editor, viewport,  param['url_next'][1], [off_x, 0, -off_z], [-90,0,0], [10,10,10], '#BBFFBB');
						}
						
						SetupRoundCamera(editor.scene, viewport.renderer, viewport.camera, 90.0);
						ShowProgressBar(false);
				});
			}
		}, '../../');
	}else if($.webgis.editor.mode == 'tower')
	{
		if(param['url'])
		{
			LoadGltfFromUrl(editor, viewport,  param['url'], [0, 0, 0], [-90,0,0], [10,10,10], '#00FF00', 
				function(target){
					SetupRoundCamera(editor.scene, viewport.renderer, viewport.camera, 90.0, target);
					ShowProgressBar(false);
			});
		}
		if(param['data'])
		{
			$.webgis.editor.contact_points =  param['data']['contact_points'];
			LoadContactPoint(editor, param['tower_id'], param['data']['contact_points'], [0, 0, 0]);
		}
		if(!param['url'])
		{
			ShowProgressBar(false);
		}
	}
	
	$('[id^="button_"]').css('display','none');
	$('#div_contact_point_coords').css('display','none');
	if($.webgis.editor.mode == 'tower')
	{
		$('#button_cp_add').css('display','block');
		$('#button_cp_save').css('display','block');
		$('#button_cp_side').css('display','block');
		
		$('#button_cp_add').button();
		$('#button_cp_add').on('click', function() {
			AddContactPoint(editor, param['tower_id'], param['data']);
		});
		
		$('#button_cp_save').button();
		$('#button_cp_save').on('click', function() {
			ShowConfirm(null, 400, 200,
				'保存', 
				'你希望保存该杆塔的挂线点位置吗？保存将提交到服务器上以便所有人都能看到结果.', 
				function(){
					SaveContactPoint(editor, param['tower_id'], param['data']);
			});
		});
		
		
		$('#button_cp_del').button();
		$('#button_cp_del').on('click', function() {
			DelContactPoint(editor, param['tower_id'], param['data']);
		});
		$('#button_cp_side').buttonset();
		
		$('#contact_point_coords_x').spinner({
			step: 0.01,
			max:200.0,
			min:-200.0,
			change:function( event, ui ) {
				var pos = GetObjectPos();
				if(event.currentTarget)
				{
					pos['x'] = event.currentTarget.value;
					SetSelectObjectPosition(editor, pos);
				}
				event.preventDefault();
			},
			spin:function( event, ui ) {
				var pos = GetObjectPos();
				pos['x'] = ui.value;
				SetSelectObjectPosition(editor, pos);
				//event.preventDefault();
			}
		});
		$('#contact_point_coords_y').spinner({
			step: 0.01,
			max:200.0,
			min:-200.0,
			change:function( event, ui ) {
				var pos = GetObjectPos();
				if(event.currentTarget)
				{
					pos['y'] = event.currentTarget.value;
					SetSelectObjectPosition(editor, pos);
				}
				event.preventDefault();
			},
			spin:function( event, ui ) {
				var pos = GetObjectPos();
				pos['y'] = ui.value;
				SetSelectObjectPosition(editor, pos);
				//event.preventDefault();
			}
		});
		$('#contact_point_coords_z').spinner({
			step: 0.01,
			max:200.0,
			min:-200.0,
			change:function( event, ui ) {
				var pos = GetObjectPos();
				if(event.currentTarget)
				{
					pos['z'] = event.currentTarget.value;
					SetSelectObjectPosition(editor, pos);
				}
				event.preventDefault();
			},
			spin:function( event, ui ) {
				var pos = GetObjectPos();
				pos['z'] = ui.value;
				SetSelectObjectPosition(editor, pos);
				//event.preventDefault();
			}
		});
	}
	if($.webgis.editor.mode == 'segs')
	{
		$('#button_del_seg').css('display','block');
		$('#button_add_seg').css('display','block');
		$('#button_save_seg').css('display','block');
		$('#button_save_seg_form').css('display','block');
		$('#button_del_seg').button();
		$('#button_del_seg').on('click', function() {
			DeleteSegment(editor);
		});
		
		$('#checkbox_add_segment').button();
		$('#checkbox_add_segment').on('click', function() {
			$.webgis.editor.is_add_seg = !$.webgis.editor.is_add_seg;
			if($.webgis.editor.is_add_seg)
			{
				$('#button_phase').css('display', 'block');
				$('#button_save_seg').css('display', 'none');
				$('#button_save_seg_form').css('display', 'none');
			}
			else
			{
				$('#button_phase').css('display', 'none');
				$('#button_save_seg').css('display', 'block');
				$('#button_save_seg_form').css('display', 'block');
			}
			
		});
		
		$('#button_save_seg').button();
		$('#button_save_seg').on('click', function() {
			ShowSegSave();
		});
		$('#button_save_seg_form').button();
		$('#button_save_seg_form').on('click', function() {
			ShowSegDialog();
		});
		
		$('#button_phase').buttonset();
		
		
	}
	
	
});


function UpdateContactPoint(obj, pos)
{
	if(obj && obj['userData'] && obj['userData']['type'] && obj['userData']['type'] == 'contact_point')
	{
		for(var i in $.webgis.editor.contact_points)
		{
			var cp = $.webgis.editor.contact_points[i];
			var txt = '';
			if(cp.side === 1 ) txt = '小号端';
			if(cp.side === 0 ) txt = '大号端';
			txt += '#' + cp.contact_index;
			if(obj.name === txt)
			{
				$.webgis.editor.contact_points[i].x = pos.x;
				$.webgis.editor.contact_points[i].y = pos.y;
				$.webgis.editor.contact_points[i].z = pos.z;
				break;
			}
		}
	}
}

function AddSeg(tower_id0, tower_id1, side0, side1, index0, index1, phase)
{
	for(var i in $.webgis.editor.segments_editting)
	{
		var seg = $.webgis.editor.segments_editting[i];
		if(	(seg['start_tower'] == tower_id0 && seg['end_tower'] == tower_id1 && seg['start_side'] == 1 && seg['end_side'] == 0)
		//||	(seg['start_tower'] == tower_id1 && seg['end_tower'] == tower_id0 && seg['start_side'] == 0 && seg['end_side'] == 1)
		){
			if(seg['start_tower'] == tower_id0 && seg['end_tower'] == tower_id1 && seg['start_side'] == 1 && seg['end_side'] == 0)
				seg['contact_points'].push({start:index0, end:index1, phase:phase});
			//if(seg['start_tower'] == tower_id1 && seg['end_tower'] == tower_id0 && seg['start_side'] == 0 && seg['end_side'] == 1)
				//seg['contact_points'].push({start:index1, end:index0, phase:phase});
			$.webgis.editor.segments_editting[i] = seg;
			break;
		}
	}
	//console.log('--add--tower_id0=' + tower_id0 + ',tower_id1=' + tower_id1 + ',side0=' + side0 + ',side1=' + side1 + ',index0=' + index0 + ',index1=' + index1 );
	if($.webgis.editor.segments_editting.length == 0)
	{
		if(tower_id0 != tower_id1 && side0 != side1)
		{
			var seg = {};
			seg['_id'] = null;
			seg['start_tower'] = tower_id0;
			seg['end_tower'] = tower_id1;
			seg['start_side'] = side0;
			seg['end_side'] = side1;
			seg['contact_points'] = [];
			seg['contact_points'].push({start:index0, end:index1, phase:phase});
			seg['t0'] = 0.9;
			seg['w'] = 0.001;
			$.webgis.editor.segments_editting.push(seg);
		}
	}
}
function DelSeg(data)
{
	for(var i in $.webgis.editor.segments_editting)
	{
		var seg = $.webgis.editor.segments_editting[i];
		var tower_id0 = data['start_tower'],
			tower_id1 = data['end_tower'],
			side0 = data['start_side'],
			side1 = data['end_side'],
			index0 = data['start'],
			index1 = data['end'];
			
		if(	(seg['start_tower'] == tower_id0 && seg['end_tower'] == tower_id1 && seg['start_side'] == 1 && seg['end_side'] == 0)
		||	(seg['start_tower'] == tower_id1 && seg['end_tower'] == tower_id0 && seg['start_side'] == 0 && seg['end_side'] == 1)
		){
			if(seg['start_tower'] == tower_id0 && seg['end_tower'] == tower_id1 && seg['start_side'] == 1 && seg['end_side'] == 0)
			{
				for(var j in seg['contact_points'])
				{
					var cp = seg['contact_points'][j];
					if(cp['start'] == index0 && cp['end'] == index1)
					{
						seg['contact_points'].splice(j, 1);
						$.webgis.editor.segments_editting[i] = seg;
						break;
					}
				}
			}
			if(seg['start_tower'] == tower_id1 && seg['end_tower'] == tower_id0 && seg['start_side'] == 0 && seg['end_side'] == 1)
			{
				for(var j in seg['contact_points'])
				{
					var cp = seg['contact_points'][j];
					if(cp['start'] == index1 && cp['end'] == index0)
					{
						seg['contact_points'].splice(j, 1);
						$.webgis.editor.segments_editting[i] = seg;
						break;
					}
				}
			}
			
		}
	}
}

function CheckSegExist(tower_id0, tower_id1, side0, side1, index0, index1)
{
	var ret = false;
	for(var i in $.webgis.editor.segments_editting)
	{
		var seg = $.webgis.editor.segments_editting[i];
		if(seg['start_tower'] == tower_id0 && seg['end_tower'] == tower_id1 
			&& seg['start_side'] == side0 && seg['end_side'] == side1
		){
			for(var j in seg['contact_points'])
			{
				var cp = seg['contact_points'][j];
				if(cp['start'] == index0 && cp['end'] == index1)
				{
					return true;
				}
			}
		}
		if(seg['start_tower'] == tower_id1 && seg['end_tower'] == tower_id0 
			&& seg['start_side'] == side1 && seg['end_side'] == side0
		){
			for(var j in seg['contact_points'])
			{
				var cp = seg['contact_points'][j];
				if(cp['start'] == index1 && cp['end'] == index0)
				{
					return true;
				}
			}
		}
	}
	return ret;
}

function GetObjectPos()
{
	var ret = {};
	ret['x'] = parseFloat($('#contact_point_coords_x').spinner()[0].value);
	ret['y'] = parseFloat($('#contact_point_coords_y').spinner()[0].value);
	ret['z'] = parseFloat($('#contact_point_coords_z').spinner()[0].value);
	return ret;
}

function SaveContactPoint(editor, tower_id, data)
{
	//console.log($.webgis.editor.contact_points);
	//if(true) return;
	data['contact_points'] = $.webgis.editor.contact_points;
	var cond = {'db':$.webgis.db.db_name, 'collection':'features', 'action':'update', 'data':{'properties.model':data}, '_id':tower_id};
	ShowProgressBar(true, 400, 200, '保存中', '正在保存数据，请稍候...');
	MongoFind(cond, function(data1){
		ShowProgressBar(false);
		window.parent.IFrameUpdateTower(tower_id, data1);
		ShowConfirm(null, 400, 200,
			'保存模板', 
			'你希望保存为该塔型的挂线点模板吗？保存为模板将影响所有使用该塔型的杆塔.', 
			function(){
				var cond = {'db':$.webgis.db.db_name, 'collection':'models', 'action':'update', 'data':{'contact_points':data['contact_points']}, 'model_code_height':data['model_code_height']};
				ShowProgressBar(true, 400, 200, '保存中', '正在保存数据，请稍候...');
				MongoFind(cond, function(data2){
					ShowProgressBar(false);
					window.parent.IFrameUpdateModel(tower_id, data2);
				}, '/');
		});
		
	}, '/');
}


function AddContactPoint(editor, tower_id, data)
{
	if(data === undefined || data === null)
	{
		return;
	}
	var side = parseInt($("#button_cp_side :radio:checked").attr('id').replace('side', ''));
	var side0_index = 0, side1_index = 0;
	for(var i in $.webgis.editor.contact_points)
	{
		var cp = $.webgis.editor.contact_points[i];
		if(cp.side === 0)
		{
			side0_index += 1;
		}
		if(cp.side === 1)
		{
			side1_index += 1;
		}
	}
	
	var contact_index = side0_index;
	if(side === 1) contact_index = side1_index;
	
	$.webgis.editor.contact_points.push({
		side:side,
		contact_index:contact_index,
		position:'',
		x:0, 
		y:30,
		z:0
	});
	var last = $.webgis.editor.contact_points.slice(-1);
	LoadContactPoint(editor, tower_id, last, [0,0,0]);
}

function DelContactPoint(editor, tower_id, data)
{
	var obj = editor.selected;
	if(obj && obj['userData'] && obj['userData']['type'] && obj['userData']['type'] == 'contact_point')
	{
		ShowConfirm(null, 400, 200,
			'你确定要删除此挂线点吗?', 
			'删除挂线点后，你可以重新创建挂线点，方法是选择该挂线点的类型(大号端,小号端),然后点击"添加挂线点"按钮，即可完成添加.', 
			function(){
				if($.webgis.editor.contact_points && $.webgis.editor.contact_points.length>0)
				{
					for(var i in $.webgis.editor.contact_points)
					{
						var cp = $.webgis.editor.contact_points[i];
						var txt = '';
						if(cp.side === 1 ) txt = '小号端';
						if(cp.side === 0 ) txt = '大号端';
						txt += '#' + cp.contact_index;
						if(obj.name === txt)
						{
							$.webgis.editor.contact_points.splice(i,1);
							editor.removeObject(obj);
							editor.select( null );
							break;
						}
					}
				}
		});
	}
}

function DeleteSegment(editor)
{
	var obj = editor.selected;
	if(obj && obj['userData'] && obj['userData']['type'] && obj['userData']['type'] == 'line')
	{
		ShowConfirm(null, 400, 200,
			'你确定要删除此线段吗?', 
			'删除线段后，你可以重新创建线段，方法是,确认“添加线段”按钮按下,然后在右边选择该线段的类型,然后先点击一个杆塔的挂线端点，再点击另一个杆塔的挂线端点，即可完成添加.', 
			function(){
				DelSeg(obj['userData']['data']);
				DelLine(editor);
		});
	}
}
function ShowSegSave()
{
	var b = CheckSegsModified();
	if(b)
	{
		ShowConfirm(null, 400, 200,
			'发现已修改', 
			'确认保存吗? 确认的话数据将会提交到服务器上，以便所有人都能看到修改的结果。', 
			function(){
				SaveSeg();
		});
	}
}

function CheckSegsModified()
{
	var ret = false;
	
	if($.webgis.editor.segments.length != $.webgis.editor.segments_editting.length)
	{
		return true;
	}
	
	for(var i in $.webgis.editor.segments)
	{
		if($.webgis.editor.segments[i]['t0'] != $.webgis.editor.segments_editting[i]['t0'])
		{
			return true;
		}
		if($.webgis.editor.segments[i]['w'] != $.webgis.editor.segments_editting[i]['w'])
		{
			return true;
		}
		if($.webgis.editor.segments[i].contact_points.length != $.webgis.editor.segments_editting[i].contact_points.length)
		{
			return true;
		}
		for(var j in $.webgis.editor.segments[i].contact_points)
		{
			var cp1 = $.webgis.editor.segments[i].contact_points[j];
			var cp2 = $.webgis.editor.segments_editting[i].contact_points[j];
			for(var k in cp1)
			{
				//console.log(cp1[k] + '<==>' + cp2[k]);
				if(cp1[k] != cp2[k])
				{
					return true;
				}
			}
		}
	}
	return ret;
}
function SaveSeg()
{
	var data = {'db':$.webgis.db.db_name, 'collection':'segments','action':'save', 'data':$.webgis.editor.segments_editting};
	//console.log(data);
	ShowProgressBar(true, 400, 150, '保存中', '正在保存, 请稍候...');
	MongoFind(data, function(data1){
		ShowProgressBar(false);
		window.parent.IFrameUpdateSegments(data1);
	}, '/');
	
	
}



function GetDrawInfoFromContactPoint(side, idx, data, offset_x, offset_z)
{
	var ret = null;
	if(data instanceof Object)
	{
		for(var i in data['contact_points'])
		{
			var cp = data['contact_points'][i];
			if(cp['contact_index'] == idx && cp['side'] == side)
			{
				ret = {};
				ret['model_code'] = data['model_code_height'];
				ret['index'] =  cp['contact_index'];
				ret['x'] = cp['x'] + offset_x;
				ret['y'] = cp['y'];
				ret['z'] = cp['z'] + offset_z;
				break;
			}
		}
	}
	if(data instanceof Array)
	{
		for(var i in data)
		{
			var info = GetDrawInfoFromContactPoint(side, idx, data[i], offset_x, offset_z);
			if(info)
			{
				ret = info;
				break;
			}
		}
	}
	return ret;
}
function DrawSegments(editor, tower_id, next_ids, data, data_next, offset_x, offset_z)
{
	var get_seg = function(segments, startid, endid)
	{
		var ret;
		for(var j in segments)
		{
			var seg = segments[j];
			if(seg['start_tower'] == startid && seg['end_tower'] == endid)
			{
				ret = seg;
				break;
			}
		}
		return ret;
	};
	var seg;
	if(next_ids.length === 1)
	{
		seg = get_seg($.webgis.editor.segments, tower_id, next_ids[0]);
		if(seg)
		{
			for(var k in seg['contact_points'])
			{
				var cp = seg['contact_points'][k];
				var start = GetDrawInfoFromContactPoint(1, cp['start'], data, 0, offset_z);
				var end = GetDrawInfoFromContactPoint(0, cp['end'], data_next[0], 0, -offset_z);
				if(end )
				{
					var color = parseInt(tinycolor($.webgis.mapping.phase_color_mapping[cp['phase']]).toHex(), 16);
					DrawLine(editor, start, end, color, seg, cp);
				}
				
			}
		}
	}
	if(next_ids.length === 2)
	{
		seg = get_seg($.webgis.editor.segments, tower_id, next_ids[0]);
		if(seg)
		{
			for(var k in seg['contact_points'])
			{
				var cp = seg['contact_points'][k];
				var start = GetDrawInfoFromContactPoint(1, cp['start'], data, 0, offset_z);
				var end = GetDrawInfoFromContactPoint(0, cp['end'], data_next[0], -offset_x, -offset_z);
				if(end)
				{
					var color = parseInt(tinycolor($.webgis.mapping.phase_color_mapping[cp['phase']]).toHex(), 16);
					DrawLine(editor, start, end, color, seg, cp);
				}
			}
		}
		seg = get_seg($.webgis.editor.segments, tower_id, next_ids[1]);
		if(seg)
		{
			for(var k in seg['contact_points'])
			{
				var cp = seg['contact_points'][k];
				var start = GetDrawInfoFromContactPoint(1, cp['start'], data, 0, offset_z);
				var end = GetDrawInfoFromContactPoint(0, cp['end'], data_next[1], offset_x, -offset_z);
				if(end)
				{
					var color = parseInt(tinycolor($.webgis.mapping.phase_color_mapping[cp['phase']]).toHex(), 16);
					DrawLine(editor, start, end, color, seg, cp);
				}
			}
		}
	}
		
		//for(var k in seg['contact_points'])
		//{
			//var cp = seg['contact_points'][k];
			//var start = GetDrawInfoFromContactPoint(1, cp['start'], data, 0, offset_z);
			//var end, end1, end2;
			//if(data_next.length==1)
			//{
				//end = GetDrawInfoFromContactPoint(0, cp['end'], data_next[0], 0, -offset_z);
			//}
			//if(data_next.length==2)
			//{
				//end1 = GetDrawInfoFromContactPoint(0, cp['end'], data_next[0], -offset_x, -offset_z);
				//end2 = GetDrawInfoFromContactPoint(0, cp['end'], data_next[1], offset_x, -offset_z);
			//}
			//var color = parseInt(tinycolor($.webgis.mapping.phase_color_mapping[cp['phase']]).toHex(), 16);
			//if(end )
			//{
				//DrawLine(editor, start, end, color, seg, cp);
			//}
			//if(end1)
			//{
				//DrawLine(editor, start, end1, color, seg, cp);
			//}
			//if(end2)
			//{
				//DrawLine(editor, start, end2, color, seg, cp);
			//}
		//}
}
function DelLine(editor)
{
	editor.removeObject(editor.selected);
	editor.deselect();
}
function DrawLine(editor, start, end, color, seg, cp)
{
	var geometry = new THREE.Geometry();
	var p = new THREE.Vector3(start.x, start.y, start.z);
	geometry.vertices.push( p );
	p = new THREE.Vector3(end.x, end.y, end.z);
	geometry.vertices.push( p );
	var line = new THREE.Line( geometry, new THREE.LineBasicMaterial( { color: color, opacity: 1.0, linewidth:2.0 } ) );
	line.name = start.index + ','+ end.index;
	line['userData']['type'] = 'line';
	line['userData']['data'] = {
		'start_tower':seg['start_tower'],
		'end_tower':seg['end_tower'],
		'start_side':seg['start_side'],
		'end_side':seg['end_side'],
		'start':cp['start'],
		'end':cp['end'],
		'phase':cp['phase']
	};
	editor.addObject( line );
}



function LoadContactPoint(editor, tower_id, contact_points, offset, model_code_height)
{
	for(var i in contact_points)
	{
		var cp = contact_points[i];
		var title = '';
		var color;
		var size;
		if(cp['side']==1)
		{
			title = '小号端' ;
			color = '#FF0000';
			size = 0.2;
		}
		if(cp['side']==0)
		{
			title = '大号端' ;
			color = '#0000FF';
			size = 0.5;
		}
		if($.webgis.editor.mode=='tower')
		{
			title = title + '#' + cp['contact_index'];
		}
		if($.webgis.editor.mode=='segs')
		{
			if(model_code_height === undefined) model_code_height = '未知塔型';
			title = model_code_height + '#' + title + '#' + cp['contact_index'];
		}
		AddSphere(editor, tower_id, [cp['x'] + offset[0], cp['y'] + offset[1], cp['z'] + offset[2]], size, title, color, cp);
	}

}
function SetSelectObjectPosition(editor, pos)
{
	if(editor.selected && editor.selected.name.indexOf('tower/')==-1)
	{
		//console.log(pos);
		//editor.selected.position = new THREE.Vector3(parseFloat(pos.x), parseFloat(pos.y), parseFloat(pos.z));
		var p = {x:parseFloat(pos.x),y:parseFloat(pos.y),z:parseFloat(pos.z)};
		editor.selected.position.set(p.x, p.y, p.z);
		UpdateContactPoint(editor.selected, p);
	}
}

function ClearRoundCamera(viewport)
{
	//console.log(viewport);
	if($.webgis.editor.camera_move_around_int)
	{
		clearInterval($.webgis.editor.camera_move_around_int);
		$.webgis.editor.camera_move_around_int = undefined;
		$.webgis.editor.elapsed_time = 0.0;
		viewport.camera.position.set( 120, 120, 120 );
		//camera.up = new THREE.Vector3(0,1,0);
		viewport.camera.lookAt(new THREE.Vector3(0,0,0));
	}
}
function SetupRoundCamera(scene, renderer, camera, radius, target)
{
	var constant = 0.5;
	var inteval = 0.05;
	var height = 60.0;
	$.webgis.editor.camera_move_around_int  = setInterval(function(){
		if(target)
		{
			camera.position.y = height;
			camera.position.x = target.position.x + radius * Math.cos( constant * $.webgis.editor.elapsed_time );         
			camera.position.z = target.position.z + radius * Math.sin( constant * $.webgis.editor.elapsed_time );
			camera.lookAt( target.position );
		}else{
			camera.position.y = height;
			camera.position.x = radius * Math.cos( constant * $.webgis.editor.elapsed_time );         
			camera.position.z = radius * Math.sin( constant * $.webgis.editor.elapsed_time );
			camera.lookAt( new THREE.Vector3(0, 0, 0) );
		}
		renderer.render( scene, camera );
		$.webgis.editor.elapsed_time += inteval;
	}, 1000 * inteval);
}

function LoadGltfFromUrl(editor, viewport,  url, offset, rotation, scale, color, callback)
{
	var loader = new THREE.glTFLoader();
	loader.useBufferGeometry = false;
	loader.load( url, function(data, mat) {
		var obj = data.scene;
		//for(var  i in obj.children)
		//{
			//obj.children[i].material = new THREE.MeshBasicMaterial( { color: 0x00FF00, shading: THREE.FlatShading, wireframe: true, transparent: true } );
		//}
		var c = tinycolor(color).toRgb();
		//console.log(c);
		obj.traverse( function ( child )
		{
			if ( child instanceof THREE.Mesh )
			{
				child.material.color.setRGB(c['r']/255.0, c['g']/255.0, c['b']/255.0);
			}
		});		
		
		//obj.material = new THREE.MeshBasicMaterial( { color: 0x00FF00, shading: THREE.FlatShading, wireframe: true, transparent: true, needsUpdate: true } );
		//obj.material = new THREE.MeshLambertMaterial( { color: 0x00ff00, shading: THREE.FlatShading, vertexColors: THREE.VertexColors } );
		obj['name'] = url.substr(url.lastIndexOf('/')+1);
		obj['name'] = obj['name'].substr(0, obj['name'].indexOf('.'));
		obj['name'] = 'tower/' + obj['name'];
		obj['userData']['type'] = 'tower';
		//console.log(obj);
		editor.addObject( obj );
		editor.select( obj );
		editor.select( null );
		obj.position.set( offset[0], offset[1], offset[2] );
		obj.scale.set( scale[0], scale[1], scale[2] );
		obj.rotation.set( rotation[0] * Math.PI /180.0, rotation[1] * Math.PI /180.0, rotation[2] * Math.PI /180.0 );
		if(callback)
		{
			callback(obj);
		}
	});

}
function AddHemisphereLight(editor)
{
	var skyColor = 0xffffff;
	var groundColor = 0xffffff;
	var intensity = 1;
	var light = new THREE.HemisphereLight( skyColor, groundColor, intensity );
	light.name = 'HemisphereLight';
	light.position.set( 0, 1, 0 ).multiplyScalar( 900 );
	editor.addObject( light );
}

function AddSphere(editor, tower_id, position, radius, name, color, data)
{
	var c = tinycolor(color).toRgb();
	var widthSegments = 32;
	var heightSegments = 16;

	var geometry = new THREE.SphereGeometry( radius, widthSegments, heightSegments );
	var mesh = new THREE.Mesh( geometry, new THREE.MeshPhongMaterial() );
	mesh.name = name ;
	mesh['userData']['type'] = 'contact_point';
	mesh['userData']['data'] = data;
	mesh['userData']['tower_id'] = tower_id;
	mesh.material.color.setRGB(c['r']/255.0, c['g']/255.0, c['b']/255.0);
	editor.addObject( mesh );
	//editor.select( mesh );
	mesh.position.set( position[0], position[1], position[2] );
}

function ShowLabelBySelected(editor)
{
	ClearAllLabels(editor);
	if(editor.selected)
	{
		if(editor.selected.name && editor.selected.name.length>0 && editor.selected.name.indexOf('tower/')==-1)
		{
			var sp = MakeLabel(editor.selected.name, {fontsize: 48, color:'#00FFFF'});
			editor.addObject( sp );
			sp.position = editor.selected.position;
		}
	}
}

function ClearAllLabels(editor)
{
	//editor.scene.traverse( function ( child )
	for(var i in editor.scene.children)
	{
		var child = editor.scene.children[i];
		if ( child instanceof THREE.Sprite )
		{
			editor.removeObject(child);
		}
		if(child && child['name'].length==0 && child.parent instanceof THREE.Scene)
		{
			editor.removeObject(child);
		}
	}		
}


function MakeLabel(text, parameters) {
	if ( parameters === undefined ) parameters = {};
	
	var fontface = parameters.hasOwnProperty("fontface") ? 
		parameters["fontface"] : "Arial";
	
	var fontsize = parameters.hasOwnProperty("fontsize") ? 
		parameters["fontsize"] : 18;
	
	var borderThickness = parameters.hasOwnProperty("borderThickness") ? 
		parameters["borderThickness"] : 4;
	
	var borderColor = parameters.hasOwnProperty("borderColor") ?
		parameters["borderColor"] : { r:0, g:0, b:0, a:1.0 };
		
	var color = parameters.hasOwnProperty("color") ?
		parameters["color"] : "#00FF00";
	
	var backgroundColor = parameters.hasOwnProperty("backgroundColor") ?
		parameters["backgroundColor"] : { r:255, g:255, b:255, a:1.0 };


    var font = parameters["fontface"],
        size = parameters["fontsize"];
        //color = "#00FF00";

    font = "bold " + size + "px " + font;

    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    context.font = font;
	
	
	//context.fillStyle   = "rgba(" + backgroundColor.r + "," + backgroundColor.g + ","
								  //+ backgroundColor.b + "," + backgroundColor.a + ")";
	//// border color
	context.strokeStyle = "rgba(" + borderColor.r + "," + borderColor.g + ","
								  + borderColor.b + "," + borderColor.a + ")";
	

    // get size data (height depends only on font size)
    var metrics = context.measureText(text),
        textWidth = metrics.width;

    canvas.width = textWidth + 6;
    canvas.height = size + 66;
	
    context.font = font;
    context.fillStyle = color;
	context.lineWidth = borderThickness;
	
	
	//roundRect(context, borderThickness/2, borderThickness/2, textWidth + borderThickness, fontsize * 1.4 + borderThickness, 6);
	
    context.fillText(text, 0, size + 63);

    // canvas contents will be used for a texture
    var texture = new THREE.Texture(canvas);
    texture.needsUpdate = true;


	var spriteMaterial = new THREE.SpriteMaterial( 
		{ map: texture , useScreenCoordinates: true, alignment: 4 } );
		
	//spriteMaterial.map.offset.set( -0.2, -0.2 );
	var sprite = new THREE.Sprite( spriteMaterial );
	sprite.scale.set(10.,5.,1.0);
	return sprite;	
}


function makeTextSprite( message, parameters )
{
	if ( parameters === undefined ) parameters = {};
	
	var fontface = parameters.hasOwnProperty("fontface") ? 
		parameters["fontface"] : "Arial";
	
	var fontsize = parameters.hasOwnProperty("fontsize") ? 
		parameters["fontsize"] : 18;
	
	var borderThickness = parameters.hasOwnProperty("borderThickness") ? 
		parameters["borderThickness"] : 4;
	
	var borderColor = parameters.hasOwnProperty("borderColor") ?
		parameters["borderColor"] : { r:0, g:0, b:0, a:1.0 };
	
	var backgroundColor = parameters.hasOwnProperty("backgroundColor") ?
		parameters["backgroundColor"] : { r:255, g:255, b:255, a:1.0 };

	//var spriteAlignment = parameters.hasOwnProperty("alignment") ?
	//	parameters["alignment"] : THREE.SpriteAlignment.topLeft;

	//var spriteAlignment = THREE.SpriteAlignment.topLeft;
		

	var canvas = document.createElement('canvas');
	var context = canvas.getContext('2d');
	context.font = "Bold " + fontsize + "px " + fontface;
    
	// get size data (height depends only on font size)
	var metrics = context.measureText( message );
	var textWidth = metrics.width;
	
	// background color
	context.fillStyle   = "rgba(" + backgroundColor.r + "," + backgroundColor.g + ","
								  + backgroundColor.b + "," + backgroundColor.a + ")";
	// border color
	context.strokeStyle = "rgba(" + borderColor.r + "," + borderColor.g + ","
								  + borderColor.b + "," + borderColor.a + ")";

	context.lineWidth = borderThickness;
	roundRect(context, borderThickness/2, borderThickness/2, textWidth + borderThickness, fontsize * 1.4 + borderThickness, 6);
	// 1.4 is extra height factor for text below baseline: g,j,p,q.
	
	// text color
	context.fillStyle = "rgba(0, 1, 0, 1.0)";

	context.fillText( message, borderThickness, fontsize + borderThickness);

	//canvas.width = canvas.width*2;
	//canvas.height = canvas.height*2;
	//console.log(canvas.width);
	//console.log(canvas.height);
	// canvas contents will be used for a texture
	var texture = new THREE.Texture(canvas) 
	texture.needsUpdate = true;

	var spriteMaterial = new THREE.SpriteMaterial( 
		{ map: texture} );//, useScreenCoordinates: true, alignment: 4 } );
	//spriteMaterial.map.offset.set( -0.5, 0.5 );
	var sprite = new THREE.Sprite( spriteMaterial );
	sprite.scale.set(6.,2.,1.0);
	return sprite;	
}

// function for drawing rounded rectangles
function roundRect(ctx, x, y, w, h, r) 
{
    ctx.beginPath();
    ctx.moveTo(x+r, y);
    ctx.lineTo(x+w-r, y);
    ctx.quadraticCurveTo(x+w, y, x+w, y+r);
    ctx.lineTo(x+w, y+h-r);
    ctx.quadraticCurveTo(x+w, y+h, x+w-r, y+h);
    ctx.lineTo(x+r, y+h);
    ctx.quadraticCurveTo(x, y+h, x, y+h-r);
    ctx.lineTo(x, y+r);
    ctx.quadraticCurveTo(x, y, x+r, y);
    ctx.closePath();
    ctx.fill();
	ctx.stroke();   
}


function GetParamsFromUrl() {
	var ret = {};
	if(location.search.length>0)
	{
		var data = decodeURIComponent(location.search.substr(1));
		ret = JSON.parse(decodeURIComponent(data));
	}
	//console.log(ret);
	return ret;
}


function ShowSegDialog()
{
	var height = 270;
	if($.webgis.editor.segments_editting.length === 2) height = 420;
	$('#dlg_seg_info').dialog({
		width: 400,
		height: height,
		minWidth:200,
		minHeight: 200,
		draggable: false,
		resizable: false, 
		modal: true,
		position:{at: "center"},
		title:"属性",
		close: function(event, ui){
		},
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
				text: "保存", 
				click: function(){
					var i;
					for(i=0; i < $.webgis.editor.segments_editting.length; i++)
					{
						var data = $('#form_seg_info_' + i).webgisform('getdata');
						$.webgis.editor.segments_editting[i]['t0'] = data['t0'];
						$.webgis.editor.segments_editting[i]['w'] = data['w'];
					}
					$( this ).dialog( "close" );
				}
			}
		]
	});
	var field = [
		{display: "应力", id: "t0", newline: true,  type: "spinner", step:0.1, min:0.4,max:1.5, width:150, labelwidth:50,  group:'弧垂参数', validate:{number: true}},
		{display: "比载", id: "w", newline: true,  type: "spinner", step:0.001, min:0.001,max:0.01, width:150, labelwidth:50,  group:'弧垂参数', validate:{number: true}}
	];
	
	
	var i;
	for(i=0; i < $.webgis.editor.segments_editting.length; i++)
	{
		$('#dlg_seg_info').append('<form id="form_seg_info_' + i + '"></form>');
		$('#form_seg_info_' + i).webgisform( field,{
			prefix:'seg_info_' + i + '_',
			maxwidth:300
		});
		var data = {t0:0.9, w:0.001};
		var seg = $.webgis.editor.segments_editting[i];
		if(seg['t0']) data['t0'] = seg['t0'];
		if(seg['w']) data['w'] = seg['w'];
		$('#form_seg_info_' + i).webgisform('setdata', data);
		//$('#dlg_seg_info').dialog("option", "hide", {
			//effect: "blind",
			//duration: 1
		//});
	}
}
