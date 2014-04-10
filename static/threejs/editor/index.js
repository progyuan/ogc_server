var g_camera_move_around_int;
var g_elapsedTime = 0.0;
var g_editor;
$(function() {
	window.URL = window.URL || window.webkitURL;
	window.BlobBuilder = window.BlobBuilder || window.WebKitBlobBuilder || window.MozBlobBuilder;

	var editor = new Editor();
	g_editor = editor;
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
		if(obj && obj.name.indexOf('tower/')==-1)
		{
			//window.postMessage(JSON.stringify({'contact_point':obj.name}), '*');
			$(window.parent.document).find('#title_contact_point').html(obj.name);
			$(window.parent.document).find('#contact_point_coords').css('display','inline-block');
			
			$(window.parent.document).find('#contact_point_coords_x').spinner()[0].value = obj.position.x.toFixed(2);
			$(window.parent.document).find('#contact_point_coords_y').spinner()[0].value = obj.position.y.toFixed(2);
			$(window.parent.document).find('#contact_point_coords_z').spinner()[0].value = obj.position.z.toFixed(2);
			//$(window.parent.document).find('#contact_point_coords_x').spinner().value(obj.position.x);
			//$(window.parent.document).find('#contact_point_coords_y').spinner().value(obj.position.y);
			//$(window.parent.document).find('#contact_point_coords_z').spinner().value(obj.position.z);
		}
		else
		{
			$(window.parent.document).find('#contact_point_coords').css('display','none');
		}
	};
	
	editor.signals.objectSelected.add( OnSelected );

	//console.log(viewport.renderer);
	//console.log(viewport.camera);

	
	document.addEventListener( 'dragover', function ( event ) {

		event.preventDefault();
		event.dataTransfer.dropEffect = 'copy';

	}, false );

	//document.addEventListener( 'mousedown', function ( event ) {
		//ClearRoundCamera();
	//}, false );
	
	$(document).mousedown(function() {
		ClearRoundCamera();
	});
	//$(window).on('message',function(e) {
		//console.log('recv:' + e.originalEvent.data);
		//console.log(g_camera_move_around_int);
		//ClearRoundCamera();
	//});
	//$(window).on('mouseup',function(event) {
		//if(editor.selected && editor.selected.name.indexOf('tower/')==-1)
		//{
			////console.log(editor.selected.position.x);
			////console.log(editor.selected.position.y);
			////console.log(editor.selected.position.z);
			////$(window.parent.document).find('#contact_point_coords_x').spinner()[0].value = editor.selected.position.x.toFixed(2);
			////$(window.parent.document).find('#contact_point_coords_y').spinner()[0].value = editor.selected.position.y.toFixed(2);
			////$(window.parent.document).find('#contact_point_coords_z').spinner()[0].value = editor.selected.position.z.toFixed(2);
		//}
		//event.preventDefault();
		
	//});
	
	document.addEventListener( 'drop', function ( event ) {

		event.preventDefault();
		editor.loader.loadFile( event.dataTransfer.files[ 0 ] );

	}, false );

	document.addEventListener( 'keydown', function ( event ) {
		console.log(event.keyCode);
		switch ( event.keyCode ) {

			case 8: // prevent browser back 
				event.preventDefault();
				break;
			case 46: // delete
				editor.removeObject( editor.selected );
				editor.deselect();
				break;
			case 27: // esc
				ClearRoundCamera();
				ClearAllLabels(editor);
				break;
		}

	}, false );

	var onWindowResize = function ( event ) {
		ClearRoundCamera();
		editor.signals.windowResize.dispatch();
	};

	window.addEventListener( 'resize', onWindowResize, false );

	onWindowResize();
	
	AddHemisphereLight(editor);
	
	var param = GetParamsFromUrl();
	if(param['url'])
	{
		LoadGltfFromUrl(editor, viewport,  param['url'], [-90,0,0], [10,10,10], '#00FF00');
	}
	//LoadGltfFromUrl(editor, viewport, 'http://localhost:88/gltf/BJ1_25_0.json', [-90,0,0], [10,10,10], '#00FF00');
	if(param['data'])
	{
		for(var i in param['data']['contact_points'])
		{
			var cp = param['data']['contact_points'][i];
			var side = '';
			var color;
			var size;
			if(cp['side']==0)
			{
				side = '小号端' ;
				color = '#FF0000';
				size = 0.2;
			}
			if(cp['side']==1)
			{
				side = '大号端' ;
				color = '#0000FF';
				size = 0.5;
			}
			side = side + '#' + cp['contact_index'];
			AddSphere(editor, [cp['x'], cp['y'], cp['z']], size, side, color);
		}
	}
	
});

function SetSelectObjectPosition(pos)
{
	if(g_editor.selected && g_editor.selected.name.indexOf('tower/')==-1)
	{
		//console.log(pos);
		//g_editor.selected.position = new THREE.Vector3(parseFloat(pos.x), parseFloat(pos.y), parseFloat(pos.z));
		g_editor.selected.position.set(parseFloat(pos.x),parseFloat(pos.y),parseFloat(pos.z));
	}
}

function ClearRoundCamera()
{
	//console.log(g_camera_move_around_int);
	if(g_camera_move_around_int)
	{
		clearInterval(g_camera_move_around_int);
		g_camera_move_around_int = undefined;
		g_elapsedTime = 0.0;
	}
}
function SetupRoundCamera(scene, renderer, camera,  target)
{
	var radius = 60.0;
	var constant = 0.5;
	var inteval = 0.05;
	var height = 60.0;
	var ret = setInterval(function(){
		camera.position.y = height;
		camera.position.x = target.position.x + radius * Math.cos( constant * g_elapsedTime );         
		camera.position.z = target.position.z + radius * Math.sin( constant * g_elapsedTime );
		camera.lookAt( target.position );
		renderer.render( scene, camera );
		g_elapsedTime += inteval;
	}, 1000 * inteval);
	return ret;
}

function LoadGltfFromUrl(editor, viewport,  url, rotation, scale, color)
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
		//console.log(obj);
		editor.addObject( obj );
		editor.select( obj );
		editor.select( null );
		obj.scale.set( scale[0], scale[1], scale[2] );
		obj.rotation.set( rotation[0] * Math.PI /180.0, rotation[1] * Math.PI /180.0, rotation[2] * Math.PI /180.0 );
		g_camera_move_around_int = SetupRoundCamera(editor.scene, viewport.renderer, viewport.camera, obj);
	});

}
function AddHemisphereLight(editor)
{
	var skyColor = 0xffffff;
	var groundColor = 0xffffff;
	var intensity = 1;
	var light = new THREE.HemisphereLight( skyColor, groundColor, intensity );
	light.name = 'HemisphereLight';
	light.position.set( 0, -1, 0 ).multiplyScalar( 500 );
	editor.addObject( light );
}

function AddSphere(editor, position, radius, name, color)
{
	var c = tinycolor(color).toRgb();
	var widthSegments = 32;
	var heightSegments = 16;

	var geometry = new THREE.SphereGeometry( radius, widthSegments, heightSegments );
	var mesh = new THREE.Mesh( geometry, new THREE.MeshPhongMaterial() );
	mesh.name = name ;
	mesh.material.color.setRGB(c['r']/255.0, c['g']/255.0, c['b']/255.0);
	editor.addObject( mesh );
	//editor.select( mesh );
	mesh.position.set( position[0], position[1], position[2] );
	
	////var sprite = makeTextSprite( name, { fontsize: 16, backgroundColor: {r:0, g:255, b:0, a:1} } );
	//var sprite = MakeLabel( name, { fontsize: 32, backgroundColor: {r:0, g:255, b:0, a:1} } );
	//editor.addObject( sprite );
	//sprite.position = mesh.position;

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
	editor.scene.traverse( function ( child )
	{
		if ( child instanceof THREE.Sprite )
		{
			editor.removeObject(child);
		}
	});		
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
	console.log(ret);
	return ret;
}
