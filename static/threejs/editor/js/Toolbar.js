var Toolbar = function ( editor ) {

	var signals = editor.signals;

	var container = new UI.Panel();

	var buttons = new UI.Panel();
	container.add( buttons );

	// translate / rotate / scale

	var translate = new UI.Button( 'translate' ).onClick( function () {

		signals.transformModeChanged.dispatch( 'translate' );

	} );
	buttons.add( translate );

	var rotate = new UI.Button( 'rotate' ).onClick( function () {

		signals.transformModeChanged.dispatch( 'rotate' );

	} );
	buttons.add( rotate );

	var scale = new UI.Button( 'scale' ).onClick( function () {

		signals.transformModeChanged.dispatch( 'scale' );

	} );
	buttons.add( scale );

	// grid

	var grid = new UI.Number( 25 ).onChange( update );
	grid.dom.style.width = '42px';
	buttons.add( new UI.Text( 'Grid: ' ) );
	buttons.add( grid );

	var snap = new UI.Checkbox( false ).onChange( update );
	buttons.add( snap );
	buttons.add( new UI.Text( 'snap' ) );

	var local = new UI.Checkbox( false ).onChange( update );
	buttons.add( local );
	buttons.add( new UI.Text( 'local' ) );
	
	
	//var add_cp = new UI.Button( '添加挂线点' ).onClick( function () {
		//console.log( 'add_cp' );
	//});
	//var cp_side = new UI.Select();
	//cp_side.setOptions({
		//'0':'大号端',
		//'1':'小号端'
	//});
	//var delete_seg = new UI.Button( '删除线段' ).onClick( function () {

		//console.log( 'delete_seg' );

	//} );
	//var add_seg = new UI.Button( '添加线段' ).onClick( function () {
		//console.log( 'add_seg' );
	//} );
	//var seg_phase = new UI.Select();
	//seg_phase.setOptions({
		//'G':'地线(黑)',
		//'A':'A相(黄)',
		//'B':'B相(红)',
		//'C':'C相(绿)'
	//});
	//if(g_mode=='tower')
	//{
		//buttons.add( add_cp );
		//buttons.add( cp_side );
	//}
	//if(g_mode=='segs')
	//{
		//buttons.add( delete_seg );
		//buttons.add( add_seg );
		//buttons.add( seg_phase );
	//}
	
	

	function update() {

		signals.snapChanged.dispatch( snap.getValue() === true ? grid.getValue() : null );
		signals.spaceChanged.dispatch( local.getValue() === true ? "local" : "world" );

	}

	update();

	return container;

}
