$.auth_platform = {};
$.auth_platform.AUTH_HOST = 'yncaiyun.com';
$.auth_platform.AUTH_PROTOCOL = 'http';
$.auth_platform.AUTH_PORT = '8088';
$.auth_platform.DEBUG = true;

$.auth_platform.post_cors = function(action, data, callback)
{
    var url = $.auth_platform.AUTH_PROTOCOL + '://' + $.auth_platform.AUTH_HOST + ':' + $.auth_platform.AUTH_PORT + '/' + action;
    $.ajax({
        url: url,
        type: "post",
        data: encodeURIComponent(JSON.stringify(data)),
        crossDomain: true,
        xhrFields: {
            withCredentials: true
        },        
        dataType: "text",
        success: function(data1){
            if(callback)
            {
                callback(data1);
            }
        }
    });
};

$.auth_platform.login = function(data, callback)
{
    if(data.username === undefined || data.username.length == 0)
    {
        throw "data.username required";
    }
    if(data.password === undefined || data.password.length == 0)
    {
        throw "data.password required";
    }
    $.auth_platform.post_cors('login', data, callback)
};


$.auth_platform.logout = function(callback)
{
    $.auth_platform.post_cors('logout', {}, callback)
};


$.auth_platform.auth_check = function(data, callback)
{
    if(data.username === undefined || data.username.length == 0)
    {
        throw "data.username required";
    }
    $.auth_platform.post_cors('auth_check', data, callback)
};

$.auth_platform.register = function(data, callback)
{
    if(data.username === undefined || data.username.length == 0)
    {
        throw "data.username required";
    }
    if(data.password === undefined || data.password.length == 0)
    {
        throw "data.password required";
    }
    $.auth_platform.post_cors('register', data, callback)
};


$.auth_platform.unregister = function(data, callback)
{
    if(data.username === undefined || data.username.length == 0)
    {
        throw "data.username required";
    }
    $.auth_platform.post_cors('unregister', data, callback)
};


$.auth_platform.reset_password = function(data, callback)
{
    if(data.username === undefined || data.username.length == 0)
    {
        throw "data.username required";
    }
    if(data.password === undefined || data.password.length == 0)
    {
        throw "data.password required";
    }
    $.auth_platform.post_cors('reset_password', data, callback)
};

$.auth_platform.function_add = function(data, callback)
{
    if(data.name === undefined)
    {
        throw "data.name required";
    }
    if(data._id !== undefined)
    {
        throw "data._id DO NOT required";
    }
    $.auth_platform.post_cors('function_add', data, callback)
};

$.auth_platform.function_query = function(data, callback)
{
    //if(data.name === undefined || data.name.length == 0)
    //{
        //data.name = '';
    //}
    $.auth_platform.post_cors('function_query', data, callback)
};

$.auth_platform.function_update = function(data, callback)
{
    if(data._id === undefined || data._id.length == 0)
    {
        throw "data._id required";
    }
    $.auth_platform.post_cors('function_update', data, callback)
};

$.auth_platform.function_delete = function(data, callback)
{
    if(data._id === undefined || data._id.length == 0)
    {
        throw "data._id required";
    }
    $.auth_platform.post_cors('function_delete', data, callback)
};




$.auth_platform.role_add = function(data, callback)
{
    if(data.name === undefined)
    {
        throw "data.name required";
    }
    if(data._id !== undefined)
    {
        throw "data._id DO NOT required";
    }
    $.auth_platform.post_cors('role_add', data, callback)
};

$.auth_platform.role_query = function(data, callback)
{
    if(data.name === undefined || data.name.length == 0)
    {
        data.name = '';
    }
    $.auth_platform.post_cors('role_query', data, callback)
};

$.auth_platform.role_update = function(data, callback)
{
    if(data._id === undefined || data._id.length == 0)
    {
        throw "data._id required";
    }
    $.auth_platform.post_cors('role_update', data, callback)
};

$.auth_platform.role_delete = function(data, callback)
{
    if(data._id === undefined || data._id.length == 0)
    {
        throw "data._id required";
    }
    $.auth_platform.post_cors('role_delete', data, callback)
};

$.auth_platform.role_template_save = function(data, callback)
{
    if(data.name === undefined || data.name !== 'template')
    {
        throw "data.name must be 'template'";
    }
    $.auth_platform.post_cors('role_template_save', data, callback)
};

$.auth_platform.role_template_get = function(callback)
{
    $.auth_platform.post_cors('role_template_get', data, callback)
};


if($.auth_platform.DEBUG)
{

function BeforeDragFunc(treeId, treeNodes) {
	for (var i=0,l=treeNodes.length; i<l; i++) {
		if (treeNodes[i].drag === false) {
			return false;
		}
	}
	return true;
}
function BeforeDropFunc(treeId, treeNodes, targetNode, moveType) {
	return CheckIsCategory(treeId, targetNode);
}

function BeforeDragTemplate(treeId, treeNodes) {
	ret = true;
	return ret;
}

function BeforeDropTemplate(treeId, treeNodes, targetNode, moveType) {
	console.log(moveType);
	return CheckIsSible(treeId, targetNode) && moveType !== 'inner';
}

function BeforeRemoveTemplate(treeId, treeNode)
{
	var ret = CheckIsCategory(treeId, treeNode) || CheckIsSible(treeId, treeNode);
	if(ret)
	{
		ret = confirm("确定删除[" + treeNode.name + "]及其下属功能吗?");
	}
	return ret;
}

function BeforeRemoveFunc(treeId, treeNode)
{
	ret = confirm("确定删除功能[" + treeNode.name + "]吗?");
	
	return ret;
}
function OnRemoveFunc(e, treeId, treeNode)
{
	$('#func_id').val("");
	$('#func_name').val("");
	
	$.auth_platform.function_delete({_id:treeNode._id}, function(data){
		console.log(data);
	});
	
}
function OnClickFunc(e, treeId, treeNode)
{
	if(treeNode._id)
	{
		$('#func_id').val(treeNode._id);
		$('#func_name').val(treeNode.name);
	}
}

function ShowRemoveTemplate(treeId, treeNode)
{
	return CheckIsCategory(treeId, treeNode) || CheckIsSible(treeId, treeNode);
}
function ShowRenameTemplate(treeId, treeNode)
{
	return CheckIsCategory(treeId, treeNode) ;
}

function BeforeRenameTemplate(treeId, treeNode, newName, isCancelBoolean)
{
	return CheckIsCategory(treeId, treeNode);
}

function OnRemoveTemplate(e, treeId, treeNode)
{
	console.log(treeNode.name);
}

function CheckIsCategory(treeId, treeNode)
{
	var ret = false;
	if(treeId === 'roletemplate' && treeNode.type && treeNode.type === 'category')
	{
		ret = true;
	}
	return ret;
}

function CheckIsRoot(treeId, treeNode)
{
	var ret = false;
	if(treeId === 'roletemplate' && treeNode.type && treeNode.type === 'root')
	{
		ret = true;
	}
	return ret;
}

function CheckIsSible(treeId, treeNode)
{
	var ret = false;
	if(treeId === 'roletemplate' && treeNode && treeNode._id  && treeNode.getParentNode()  && treeNode.getParentNode().type && treeNode.getParentNode().type === 'category')
	{
		ret = true;
	}
	return ret;
}

function init_left()
{
	var setting = {
		edit: {
			drag:{
				isCopy:true,
				isMove : false
			},
			enable: true,
			showRemoveBtn: true,
			showRenameBtn: false
		},
		callback: {
			beforeDrag: BeforeDragFunc,
			beforeDrop: BeforeDropFunc,
			beforeRemove:BeforeRemoveFunc,
			onClick: OnClickFunc,
			onRemove: OnRemoveFunc
		}
	};

    var nodes = [];
    for(var i=0; i<10; i++)
    {
        nodes.push({_id:i.toString(), name:"功能" + i, title:"功能" + i + "描述"});
    }
	$.auth_platform.function_query( {}, function(nodes){
		$.fn.zTree.init($("#funclist"), setting, nodes);
	});
	
}

function AddHoverDom(treeId, treeNode) {
	var sObj = $("#" + treeNode.tId + "_span");
	if (treeNode.editNameFlag || $("#addBtn_"+treeNode.tId).length>0) return;
	var addStr = "<span class='button add' id='addBtn_" + treeNode.tId
		+ "' title='add node' onfocus='this.blur();'></span>";
	sObj.after(addStr);
	var btn = $("#addBtn_"+treeNode.tId);
	if (btn) btn.bind("click", function(){
		var zTree = $.fn.zTree.getZTreeObj("roletemplate");
		zTree.addNodes(treeNode, {type:"category", name:"类别" });
		return false;
	});
}
function RemoveHoverDom(treeId, treeNode) {
	$("#addBtn_"+treeNode.tId).unbind().remove();
}



function init_right()
{
	var setting = {
	
		view: {
			addHoverDom: AddHoverDom,
			removeHoverDom: RemoveHoverDom,
			selectedMulti: false
		},	
		edit: {
			enable: true,
			showRemoveBtn: ShowRemoveTemplate,
			showRenameBtn: ShowRenameTemplate
		},
		callback: {
			beforeDrag: BeforeDragTemplate,
			beforeDrop: BeforeDropTemplate,
			beforeRemove:BeforeRemoveTemplate,
			beforeRename:BeforeRenameTemplate,
			onRemove: OnRemoveTemplate
		},
		check:{
			enable : true,
			autoCheckTrigger: true,
			chkStyle : "checkbox",
			chkboxType: { "Y": "ps", "N": "ps" }
		}
	};
    //var nodes = [];
    //for(var i=0; i<3; i++)
    //{
        //nodes.push({type:"category", name:"类别" + i});
    //}
	
	$.auth_platform.role_template_get( {}, function(node){
		if(node === {})
		{
			node = {name:"template", type:"root", children:[]};
		}
		$.fn.zTree.init($("#roletemplate"), setting, node);
		ztree.expandAll(true);
	});
}


function NodeToObject(node)
{
	var ret = {};
	if(node._id)
	{
		ret._id = node._id
	}
	if(node.name)
	{
		ret.name = node.name
	}
	if(node.desc)
	{
		ret.desc = node.desc
	}
	if(node.children && node.children.length>0)
	{
		ret.children = [];
		for(var i in node.children)
		{
			var o = NodeToObject(node.children[i]);
			if(o != {})
			{
				if(o._id)
				{
					if(o.checked === undefined)
					{
						ret.children.push({_id:o._id, checked:false});
					}
					else
					{
						ret.children.push({_id:o._id, checked:o.checked});
					}
				}
				else
				{
					ret.children.push(o);
				}
			}
		}
		if(ret.children.length===0)
		{
			ret.children = undefined;
		}
	}
	return ret;
}

function NodesToTemplateJson(nodes)
{
	var ret;
	if(nodes.length>0)
	{
		nodes[0].name = 'template';
		ret = NodeToObject(nodes[0])
	}
	return ret;
}


function init_button()
{
	$('#func_new').on('click', function(){
		var func_name = $('#func_name').val();
		var func_desc = $('#func_desc').val();
		$('#func_id').val('');
		if(func_name.length>0)
		{
			$.auth_platform.function_add({name:func_name, desc:func_desc}, function(data){
				$.fn.zTree.getZTreeObj("funclist").addNodes(null, data);
			});
		}
	});
	$('#func_update').on('click', function(){
		var func_name = $('#func_name').val();
		var func_id = $('#func_id').val();
		var func_desc = $('#func_desc').val();
		if(func_name.length>0 && func_id.length>0)
		{
			$.auth_platform.function_update({_id: func_id, name:func_name, desc:func_desc}, function(data){
				$.fn.zTree.getZTreeObj("funclist").updateNode(data);
			});
		}
	});
	$('#template_update').on('click', function(){
		var o = NodesToTemplateJson($.fn.zTree.getZTreeObj("roletemplate").getNodes());
		console.log(o);
	});
}

function init()
{
	init_left();
	init_right();
	init_button();
}

    
$(function() {
    init();
});
}

