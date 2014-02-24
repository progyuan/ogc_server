var g_tab_right;
var g_accordion_left;
var g_tree_servers;
var g_tree_example;
var area = null;
var g_tree_menu;
var g_selected_treenode_id;
var g_dlg_server_add;
var g_data_tree_server = [{id:"root",type: "root", text:"服务器列表", isexpand:false, children:[]}];
$(function ()
{
 	$.metadata.setType("attr", "validate");
    //window.addEventListener('message',function(e){
        ////console.log("e.source=" + e.source);
        //console.log("host=" + e.data.host + ", port=" + e.data.port);
        //AddServer(e.data);
    //},false);
 
    //布局
    $("#layout1").ligerLayout({ leftWidth: 190, height: '100%',heightDiff:-34,space:4, onHeightChanged: f_heightChanged });

    var height = $(".l-layout-center").height();

    //Tab
    $("#framecenter").ligerTab({ height: height });

    //面板
    $("#accordion1").ligerAccordion({ height: height - 24, speed: null });

    $(".l-link").hover(function ()
    {
        $(this).addClass("l-link-over");
    }, function ()
    {
        $(this).removeClass("l-link-over");
    });
    
    g_tree_menu = $.ligerMenu({ top: 100, left: 100, width: 120, items:
    [
        { id:'cxtmenu_treenode_server_add', text: '连接服务器', click: function(item){
            //f_addTab("add_server", "新增连接", 'pymongoadmin_add_server.html');
			if(g_dlg_server_add)
			{
				$("#input_server_add_host").val("localhost");
				$("#input_server_add_port").val("27017");
				g_dlg_server_add.show();
			}else
			{
				g_dlg_server_add = $.ligerDialog.open({title:"连接服务器", target: $("#dlg_server_add"),width:720,height:150, type:"question" });
			}
        }, icon: 'add'},
        { id:'cxtmenu_treenode_server_refresh', text: '刷新', click: function(item){
        
        }, icon: 'refresh'},
        { id:'cxtmenu_treenode_server_disconnect', text: '断开', click: function(item){
        
        }, icon: 'delete'},
        { line: true },
        { id:'cxtmenu_treenode_database_add', text: '新增数据库', click: function(item){
        }, icon: 'add'},
        { id:'cxtmenu_treenode_database_delete', text: '删除数据库', click: function(item){
        }, icon: 'delete'},
        { line: true },
        { id:'cxtmenu_treenode_collection_add', text: '新增集合', click: function(item){
        }, icon: 'add'},
        { id:'cxtmenu_treenode_collection_delete', text: '删除集合', click: function(item){
        }, icon: 'delete'}
    ]
    });
    
    //$("#toptoolbar").ligerToolBar({ items: [
        //{
            //text: '增加', 
            //click: function (item){
                //alert(item.text);
            //}, 
            //icon:'add'
        //},
        //{ line:true },
        //{ 
            //text: '刷新', 
            //click: function (item){
                //alert(item.text);
            //}, 
            //icon:'refresh' 
        //},
        //{ line:true },
        //{ 
            //text: '删除', 
            //click: function (item){
                //alert(item.text);
            //}, 
            //icon:'delete' 
        //}
        //]
    //});
    $("#tree_servers").ligerTree({
        //url:'/get?op=get_mongo_hirachy',
        data : g_data_tree_server,
        checkbox: false,
        slide: false,
        nodeWidth: 120,
        //attribute: ['id','line_code','line_name','voltage','category','length','manage_length','start_point','end_point','start_tower','end_tower','status','maintenace','management','owner','team','responsible','investor','designer','supervisor','constructor','operator','finish_date','production_date','decease_date'],
        onContextmenu: function (node, e)
        { 
            g_selected_treenode_id = node.data.id;
            var type = node.data.type;
            console.log("contextmenu=" + g_selected_treenode_id);
            g_tree_menu.show({ top: e.pageY, left: e.pageX });
            DisableAllTreeMenu();
            if(type == 'root')
            {
                g_tree_menu.setEnabled("cxtmenu_treenode_server_add");
                g_tree_menu.setEnabled("cxtmenu_treenode_server_refresh");
                g_tree_menu.setEnabled("cxtmenu_treenode_server_disconnect");
            }
            if(type == 'server')
            {
                g_tree_menu.setEnabled("cxtmenu_treenode_database_add");
                g_tree_menu.setEnabled("cxtmenu_treenode_database_delete");
            }
            if(type == 'database')
            {
                g_tree_menu.setEnabled("cxtmenu_treenode_collection_add");
                g_tree_menu.setEnabled("cxtmenu_treenode_collection_delete");
            }
            return false;
        },
        onSelect: function(node)
        {
            g_selected_treenode_id = node.data.id;
            console.log("select=" + g_selected_treenode_id);
        }
    });

    g_tree_servers = $("#tree_servers").ligerGetTreeManager();
    
    
    
    
    
    $("#tree1").ligerTree({
        data : indexdata,
        checkbox: false,
        slide: false,
        nodeWidth: 120,
        attribute: ['nodename', 'url'],
        onSelect: function (node)
        {
            if (!node.data.url) return;
            var tabid = $(node.target).attr("tabid");
            if (!tabid)
            {
                tabid = new Date().getTime();
                $(node.target).attr("tabid", tabid)
            } 
            f_addTab(tabid, node.data.text, node.data.url);
        }
    });
    
    

    g_tab_right = $("#framecenter").ligerGetTabManager();
    g_accordion_left = $("#accordion1").ligerGetAccordionManager();
    g_tree_example = $("#tree1").ligerGetTreeManager();
    $("#pageloading").hide();

	$("#btn_server_add").ligerButton({
		width:250,
		height:80,
		icon: "lib/ligerUI/skins/icons/ok.gif"
		//click: function ()
		//{
			//ValidateForm(g_dlg_server_add, "form_server_add", AddServer);
		//}
	});
	$("#btn_server_add_cancel").ligerButton({
		width:250,
		height:80,
		icon: "lib/ligerUI/skins/icons/candle.gif",
		click: function ()
		{
			g_dlg_server_add.hide();
		}
	});
	$("#form_server_add").ligerForm({
		validate:{
			debug: false,
			errorPlacement: function (lable, element) {
	
				if (element.hasClass("l-textarea")) {
					element.addClass("l-textarea-invalid");
				}
				else if (element.hasClass("l-text-field")) {
					element.parent().addClass("l-text-invalid");
				}
	
				var nextCell = element.parents("td:first").next("td");
				nextCell.find("div.l-exclamation").remove(); 
				$('<div class="l-exclamation" title="' + lable.html() + '"></div>').appendTo(nextCell).ligerTip(); 
			},
			success: function (lable) {
				var element = $("#" + lable.attr("for"));
				var nextCell = element.parents("td:first").next("td");
				if (element.hasClass("l-textarea")) {
					element.removeClass("l-textarea-invalid");
				}
				else if (element.hasClass("l-text-field")) {
					element.parent().removeClass("l-text-invalid");
				}
				nextCell.find("div.l-exclamation").remove();
			},
			submitHandler: function () {
				var o = {host:$("#input_server_add_host").val(), port:$("#input_server_add_port").val()};
				AddServer(o);
				g_dlg_server_add.hide();
			}
		
		}
	});

});



function DisableAllTreeMenu()
{
    g_tree_menu.setDisabled("cxtmenu_treenode_server_add");
    g_tree_menu.setDisabled("cxtmenu_treenode_server_refresh");
    g_tree_menu.setDisabled("cxtmenu_treenode_server_disconnect");
    g_tree_menu.setDisabled("cxtmenu_treenode_database_add");
    g_tree_menu.setDisabled("cxtmenu_treenode_database_delete");
    g_tree_menu.setDisabled("cxtmenu_treenode_collection_add");
    g_tree_menu.setDisabled("cxtmenu_treenode_collection_delete");
}

function AddServer(param)
{
    if(param && param.host && param.port )
	{
		$.ajax({
			async:true,
			type: "GET",
			url: "/get?op=get_mongodb_server_tree",
			dataType: "json",
			data:param,
			success: function(data)
			{ 
				if(data.result)
				{
					if(data.result.data)
					{
						g_tree_servers.setData(data.result.data);
					}
				}
				//var treedata = [];
				//for(var i in data)
				//{
					//var tnode = {id:data[i]['id'], pid:data[i]['line_id'],text:data[i]['tower_name']};
					//treedata.push(tnode);
				//}
				//treeobj.append(node.target, treedata);
			},
			error: function (e)
			{
				console.log(e);
			}
		});
	}

}

function f_heightChanged(options)
{
    if (g_tab_right)
        g_tab_right.addHeight(options.diff);
    if (g_accordion_left && options.middleHeight - 24 > 0)
        g_accordion_left.setHeight(options.middleHeight - 24);
}
function f_addTab(tabid, text, url)
{ 
    g_tab_right.addTabItem({ tabid : tabid,text: text, url: url });
}

function getJsonFromUrl() {
  var query = location.search.substr(1);
  var data = query.split("&");
  var result = {};
  for(var i=0; i<data.length; i++) {
    var item = data[i].split("=");
    result[item[0]] = item[1];
  }
  return result;
}