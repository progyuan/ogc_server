$.auth_platform = {};
$.auth_platform.AUTH_HOST = 'yncaiyun1.com';
$.auth_platform.AUTH_PROTOCOL = 'http';
$.auth_platform.AUTH_PORT = '8088';
$.auth_platform.DEBUG = true;
$.auth_platform.FUNCTION_LIST = [];
$.auth_platform.FUNCTION_MAP = {};
$.auth_platform.ROLE_LIST = [];
$.auth_platform.ROLE_MAP = {};
$.auth_platform.ROLE_TEMPLATE = {};
$.auth_platform.USER_LIST = [];
$.auth_platform.selected_session_mapping = {};

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
                var ret = JSON.parse(decodeURIComponent(data1));
				if(action === 'role_template_get')
				{
					$.auth_platform.ROLE_TEMPLATE = ret;
				}
				if(action === 'function_query')
				{
					$.auth_platform.FUNCTION_LIST = ret;
					for(var i in ret)
					{
						$.auth_platform.FUNCTION_MAP[ret[i]._id] = ret[i];
					}
				}
				if(action === 'role_query')
				{
					$.auth_platform.ROLE_LIST = ret;
					for(var i in ret)
					{
						$.auth_platform.ROLE_MAP[ret[i]._id] = ret[i];
					}
				}
				if(action === 'user_query')
				{
					$.auth_platform.USER_LIST = ret;
				}
                callback(ret);
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
    $.auth_platform.post_cors('login', data, callback);
};


$.auth_platform.logout = function(callback)
{
    $.auth_platform.post_cors('logout', {}, callback);
};

$.auth_platform.user_check = function(data, callback)
{
    if(data.username === undefined || data.username.length == 0)
    {
        throw "data.username required";
    }
    if(data.functions === undefined || data.functions.length == 0)
    {
        throw "data.functions required";
    }
    $.auth_platform.post_cors('user_check', data, callback);
}

$.auth_platform.auth_check = function(data, callback)
{
    if(data.username === undefined || data.username.length == 0)
    {
        throw "data.username required";
    }
    $.auth_platform.post_cors('auth_check', data, callback);
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
    $.auth_platform.post_cors('register', data, callback);
};


$.auth_platform.unregister = function(data, callback)
{
    if(data.username === undefined || data.username.length == 0)
    {
        throw "data.username required";
    }
    $.auth_platform.post_cors('unregister', data, callback);
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
    $.auth_platform.post_cors('reset_password', data, callback);
};

$.auth_platform.user_query = function( callback)
{
    $.auth_platform.post_cors('user_query', {}, callback);
};

$.auth_platform.user_update = function(data, callback)
{
    if(data.username === undefined || data.username.length == 0)
    {
        throw "data.username required";
    }
    if(data.password === undefined || data.password.length == 0)
    {
        throw "data.password required";
    }
    $.auth_platform.post_cors('user_update', data, callback);
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
    $.auth_platform.post_cors('function_add', data, callback);
};

$.auth_platform.function_query = function(callback)
{
    $.auth_platform.post_cors('function_query', {}, callback);
};

$.auth_platform.function_update = function(data, callback)
{
    if(data._id === undefined || data._id.length == 0)
    {
        throw "data._id required";
    }
    $.auth_platform.post_cors('function_update', data, callback);
};

$.auth_platform.function_delete = function(data, callback)
{
    if(data._id === undefined || data._id.length == 0)
    {
        throw "data._id required";
    }
    $.auth_platform.post_cors('function_delete', data, callback);
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
    $.auth_platform.post_cors('role_add', data, callback);
};

$.auth_platform.role_query = function(callback)
{
    $.auth_platform.post_cors('role_query', {}, callback);
};

$.auth_platform.role_update = function(data, callback)
{
    if(data._id === undefined || data._id.length == 0)
    {
        throw "data._id required";
    }
    $.auth_platform.post_cors('role_update', data, callback);
};

$.auth_platform.role_delete = function(data, callback)
{
    if(data._id === undefined || data._id.length == 0)
    {
        throw "data._id required";
    }
    $.auth_platform.post_cors('role_delete', data, callback);
};

$.auth_platform.role_template_save = function(data, callback)
{
    if(data.name === undefined || data.name !== 'template')
    {
        throw "data.name must be 'template'";
    }
    $.auth_platform.post_cors('role_template_save', data, callback);
};

$.auth_platform.role_template_get = function(callback)
{
    $.auth_platform.post_cors('role_template_get', {}, callback);
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
	if(ret)
	{
		$.auth_platform.function_delete({_id:treeNode._id}, function(data1){
			if(data1.result)
			{
				alert(data1.result);
			}
		});
	}
	return ret;
}
function OnRemoveFunc(e, treeId, treeNode)
{
	$('#func_id').val("");
	$('#func_name').val("");
	$('#func_desc').val("");
}
function OnClickFunc(e, treeId, treeNode)
{
	if(treeNode._id)
	{
		$('#func_id').val(treeNode._id);
		$('#func_name').val(treeNode.name);
		$('#func_desc').val(treeNode.desc);
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


function init_test(result)
{
	try{
		$.fn.zTree.destroy('userfunctiontest');
	}catch(e)
	{
	}
	
	var setting = {
		check:{
			enable : true,
			autoCheckTrigger: true,
			chkStyle : "checkbox",
			chkboxType: { "Y": "ps", "N": "ps" }
		}
	};
	var list = [];
	var nodes = $.auth_platform.FUNCTION_LIST;
	var maap = {};
	if(result)
	{
		for(var i in result)
		{
			maap[result[i]._id] = result[i].enable;
		}
	}
	
	if(!$.isEmptyObject(nodes))
	{
		for(var i in nodes)
		{
			var enable = false;
			if(maap[nodes[i]._id] === true)
			{
				enable = true;
			}
			list.push({_id:nodes[i]._id, name:nodes[i].name, checked:enable});
		}
	}
	//console.log(list);
	$.fn.zTree.init($("#userfunctiontest"), setting, list);
}

function init_functions()
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

	//if($.auth_platform.FUNCTION_MAP.result)
	//{
		//alert($.auth_platform.FUNCTION_MAP.result);
		//return;
	//}

	var nodes = $.auth_platform.FUNCTION_LIST;
	$.fn.zTree.init($("#funclist"), setting, nodes);
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



function init_role_template()
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
	
	$.auth_platform.role_template_get( function(node){
		if(node.result)
		{
			alert(node.result);
			return;
		}
		if($.isEmptyObject(node))
		{
			node = {name:"template", type:"root", children:[]};
		}else
		{
			node = BuildTreeHirachy(node);
		}
		var ztree = $.fn.zTree.init($("#roletemplate"), setting, node);
		ztree.expandAll(true);
		
	});
}

function CheckIsLeaf(treeId, treeNode)
{
	var ret = false;
	if(!treeNode.isParent)
	{
		ret = true;
	}
	return ret;
}


function BeforeRemoveUserRole(treeId, treeNode)
{
	var username = $('#user_username').val();
	var password = $('#user_password').val();
	if(username.length>0 && password.length>0)
	{
		var ret = confirm("确定删除该用户的角色[" + treeNode.name + "]吗?");
		if(ret)
		{
			$.auth_platform.user_update({username:username,password:password, roles:ExtractRolesFromTree(treeNode._id)}, function(data1){
				if(data1.result)
				{
					alert(data1.result);
				}
			});
		}
	}
	return ret;
}
function OnRemoveUserRole(e, treeId, treeNode)
{
}

function init_users(nodes)
{
	try{
		$.fn.zTree.destroy("userrole");
	}catch(e)
	{
	}
	var setting = {
		edit: {
			enable: true,
			showRenameBtn: false,
			showRemoveBtn: CheckIsLeaf
		},
		callback: {
			beforeRemove:BeforeRemoveUserRole,
			onRemove: OnRemoveUserRole
		},
	};
	
	var ztree = $.fn.zTree.init($("#userrole"), setting, nodes);
	ztree.expandAll(true);
}

function init_roles(nodes)
{
	try{
		$.fn.zTree.destroy("roles");
	}catch(e)
	{
	}
	var setting = {
		check:{
			enable : true,
			autoCheckTrigger: true,
			chkStyle : "checkbox",
			chkboxType: { "Y": "ps", "N": "ps" }
		}
	};
	
	var ztree = $.fn.zTree.init($("#roles"), setting, nodes);
	ztree.expandAll(true);
}

function UpdateRolesData(node)
{
	for(var i in $.auth_platform.ROLE_LIST)
	{
		var item = $.auth_platform.ROLE_LIST[i];
		if(item._id === node._id)
		{
			$.auth_platform.ROLE_LIST[i] = node;
			break;
		}
	}
}

function DeleteUsersData(_id)
{
	for(var i in $.auth_platform.USER_LIST)
	{
		var item = $.auth_platform.USER_LIST[i];
		if(item._id === _id)
		{
			$.auth_platform.USER_LIST.splice(i,1);
			break;
		}
	}
}

function DeleteRolesData(_id)
{
	for(var i in $.auth_platform.ROLE_LIST)
	{
		var item = $.auth_platform.ROLE_LIST[i];
		if(item._id === _id)
		{
			$.auth_platform.ROLE_LIST.splice(i,1);
			break;
		}
	}
	delete $.auth_platform.ROLE_MAP[_id];
}



function RefreshRoleTree(_id)
{
	for(var i in $.auth_platform.ROLE_LIST)
	{
		var item = $.auth_platform.ROLE_LIST[i];
		if(item._id === _id)
		{
			init_roles([BuildTreeHirachy(item)]);
			break;
		}
	}

}

function FillRoleForm(_id)
{
	for(var i in $.auth_platform.ROLE_LIST)
	{
		var item = $.auth_platform.ROLE_LIST[i];
		if(item._id === _id)
		{
			$('#role_name').val(item.name);
			$('#role_desc').val(item.desc);
			break;
		}
	}
}

function BuildTreeHirachy(node)
{
	
	if(node._id) 
	{
		if($.auth_platform.FUNCTION_MAP[node._id] && $.auth_platform.FUNCTION_MAP[node._id]._id === node._id)
		{
			node.name = $.auth_platform.FUNCTION_MAP[node._id].name;
		}else
		{
			node.type = 'root';
		}
	}
	if(node._id === undefined) 
	{
		node.type = 'category';
	}
	if(node.children)
	{
		for(var i in node.children)
		{
			node.children[i] = BuildTreeHirachy(node.children[i]);
		}
	}
	return node;
}

function NodeToObject(node, istemplate)
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
	if(istemplate && istemplate === true)
	{
		ret.checked = false;
	}else
	{
		if(node.checked === 'true' || node.checked === true)
		{
			ret.checked = true;
		}else
		{
			ret.checked = false;
		}
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
					if(istemplate && istemplate === true)
					{
						ret.children.push({_id:o._id, checked:false});
					}
					else
					{
						if(o.checked === true || o.checked === 'true')
						{
							ret.children.push({_id:o._id, checked:true});
						}else
						{
							ret.children.push({_id:o._id, checked:false});
						}
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
		ret = NodeToObject(nodes[0], true);
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
			$.auth_platform.function_add({name:func_name, desc:func_desc}, function(data1){
				if(data1.result)
				{
					alert(data1.result);
				}else
				{
					$.fn.zTree.getZTreeObj("funclist").addNodes(null, data1);
				}
			});
		}
	});
	$('#func_update').on('click', function(){
		var func_name = $('#func_name').val();
		var func_id = $('#func_id').val();
		var func_desc = $('#func_desc').val();
		if(func_name.length>0 && func_id.length>0)
		{
			$.auth_platform.function_update({_id: func_id, name:func_name, desc:func_desc}, function(data1){
				if(data1.result)
				{
					alert(data1.result)
				}
				else
				{
					$.fn.zTree.getZTreeObj("funclist").updateNode(data1);
				}
			});
		}
	});
	$('#template_update').on('click', function(){
		var o = NodesToTemplateJson($.fn.zTree.getZTreeObj("roletemplate").getNodes());
		if(o)
		{
			$.auth_platform.role_template_save(o, function(data1){
				if(data1.result)
				{
					alert(data1.result)
				}
				console.log(data1);
			});
		}
		
	});
	
	$('#template_copy').on('click', function(){
		var o = NodesToTemplateJson($.fn.zTree.getZTreeObj("roletemplate").getNodes());
		if(o && $('#role_name').val().length>0)
		{
			o.name = $('#role_name').val();
			if($('#role_list').val() &&  $('#role_list').val().length>0)
			{
				o._id = $('#role_list').val();
			}
			else
			{
				o._id = undefined;
			}
			init_roles([BuildTreeHirachy(o)]);
		}else
		{
			alert('role name required');
		}
	});
	
	
	$('#role_new').on('click', function(){
		var role_name = $('#role_name').val();
		var role_desc = $('#role_desc').val();
		if( role_name.length>0 && $.fn.zTree.getZTreeObj("roles").getNodes().length>0)
		{
			var node = $.fn.zTree.getZTreeObj("roles").getNodes()[0];
			var data = NodeToObject(node, false);
			data._id = undefined;
			data.name = role_name;
			data.desc = role_desc;
			$.auth_platform.role_add(data, function(data1){
				if(data1.result)
				{
					alert(data1.result);
				}else
				{
					UpdateRolesData(data1);
					RefreshRoleTree(data1._id);
					var html = $('#role_list').html();
					html += '<option value="' + data1._id + '">' + data1.name + '</option>';
					$('#role_list').html(html);
					$('#role_list').val(data1._id);
				}
			});
		}
	});
	$('#role_update').on('click', function(){
		var role_name = $('#role_name').val();
		var role_desc = $('#role_desc').val();
		if( $('#role_list').val() && $('#role_list').val().length>0 && role_name.length>0 && $.fn.zTree.getZTreeObj("roles").getNodes().length>0)
		{
			var node = $.fn.zTree.getZTreeObj("roles").getNodes()[0];
			var data = NodeToObject(node, false);
			data._id = $('#role_list').val();
			data.name = role_name;
			data.desc = role_desc;
			//console.log(node);
			//console.log(data);
			$.auth_platform.role_update(data, function(data1){
				if(data1.result)
				{
					alert(data1.result);
				}else
				{
					UpdateRolesData(data1);
					RefreshRoleTree(data1._id);
				}
			});
		}
	});
	$('#role_delete').on('click', function(){
		if( $('#role_list').val() && $('#role_list').val().length>0)
		{
			if(confirm("确定删除角色[" + $('#role_name').val() + "]吗?"))
			{
				$.auth_platform.role_delete({_id:$('#role_list').val()}, function(data1){
					if(data1.result)
					{
						alert(data1.result);
					}else
					{
						$('#role_name').val("");
						$('#role_desc').val("");
						DeleteRolesData(data1._id);
						$.fn.zTree.destroy("roles");
						$('#role_list option[value="'+ data1._id + '"]').remove();
						$('#role_list').val('');
					}
				});
			}
		}
	
	});
	
	$('#role_name').on('blur', function(){
		if($.fn.zTree.getZTreeObj("roles") && $.fn.zTree.getZTreeObj("roles").getNodes().length>0)
		{
			var o = NodeToObject($.fn.zTree.getZTreeObj("roles").getNodes()[0], false);
			if(o)
			{
				o.name = $(this).val();
				init_roles([BuildTreeHirachy(o)]);
			}
		}
	});
	
	$('#login_admin').on('click', function(){
		$.auth_platform.login({username:'admin', password:'admin'}, function(data1){
			if(data1.result)
			{
				alert(data1.result);
			}		
		});
	});
	
	$('#user_new').on('click', function(){
		if($('#user_username').val().length>0 && $('#user_password').val().length>0)
		{
			$.auth_platform.register({username:$('#user_username').val(), password:$('#user_password').val(), roles:ExtractRolesFromTree()}, function(data1){
				if(data1.result)
				{
					alert(data1.result);
				}else
				{
					var html = $('#user_list').html();
					html += '<option value="' + data1._id + '">' + data1.username + '</option>';
					$('#user_list').html(html);
					$('#user_list').val(data1._id);
				
				}
			});
		}else
		{
			alert('username or password cannot be null');
		}
	});
	$('#user_update').on('click', function(){
		if($('#user_username').val().length>0 && $('#user_password').val().length>0)
		{
			$.auth_platform.user_update({username:$('#user_username').val(), password:$('#user_password').val(), roles:ExtractRolesFromTree()}, function(data1){
				if(data1.result)
				{
					alert(data1.result);
				}		
			});
		}else
		{
			alert('username or password cannot be null');
		}
	});
	$('#user_delete').on('click', function(){
		if($('#user_username').val().length>0 )
		{
			if(confirm('确定要删除用户[' + $('#user_username').val() + ']吗?'))
			{
				$.auth_platform.unregister({username:$('#user_username').val()}, function(data1){
					if(data1.result)
					{
						alert(data1.result);
					}else
					{
						$('#user_username').val('');
						$('#user_password').val('');
						DeleteUsersData(data1._id);
						$.fn.zTree.destroy("userrole");
						$('#user_list option[value="'+ data1._id + '"]').remove();
						$('#user_list').val('');
					}
				});
			}
		}else
		{
			alert('username  cannot be null');
		}
	});
	
	$('#add_role_to_user').on('click', function(){
		if($('#role_list').val().length>0 && $('#user_username').val().length>0)
		{
			var roots = $.fn.zTree.getZTreeObj("userrole").getNodes();
			if(roots.length === 0)
			{
				$.fn.zTree.getZTreeObj("userrole").addNodes(null,{name:$('#user_username').val()});
				roots = $.fn.zTree.getZTreeObj("userrole").getNodes();
			}
			var root = roots[0];
			var o = {};
			var roleid = $('#role_list').val();
			if($.auth_platform.ROLE_MAP[roleid])
			{
				o._id = roleid;
				o.name = $.auth_platform.ROLE_MAP[roleid].name;
				$.fn.zTree.getZTreeObj("userrole").addNodes(root,o);
			}
		}
	});
	$('#test').on('click', function(){
		if($('#user_username').val().length>0)
		{
			var nodes = $.fn.zTree.getZTreeObj("userfunctiontest").getNodes();
			var list = [];
			for(var i in nodes)
			{
				list.push(nodes[i]._id);
			}
			$.auth_platform.user_check({username:$('#user_username').val(), functions:list}, function(data1){
				if(data1.result)
				{
					alert(data1.result);
					return;
				}else
				{
					var s = '';
					
					init_test(data1);
					$('#test_username').html($('#user_username').val());
					//for(var i in data1)
					//{
						//if( $.auth_platform.FUNCTION_MAP[data1[i].id])
						//{
							//s += $.auth_platform.FUNCTION_MAP[data1[i].id].name + ':' + data1[i].enable + '\n';
						//}
					//}
					//alert(s);
				}
			});
		}
	});
	$('#btn_session_list').on('click', function(){
		if($.auth_platform.websocket)
		{
			//console.log($.auth_platform.websocket);
			$.auth_platform.websocket.send(JSON.stringify({op:'session_list'}));
		}		
	});
	$('#btn_logout').on('click', function(){
		if($.auth_platform.table_session_list)
		{
			var table = $.auth_platform.table_session_list;
			var list = [];
			for(var k in $.auth_platform.selected_session_mapping)
			{
				if($.auth_platform.selected_session_mapping[k] === true)
				{
					list.push(k);
				}
			}
			console.log($.auth_platform.selected_session_mapping);
			if(list.length>0)
			{
				$.auth_platform.websocket.send(JSON.stringify({op:'session_remove',id:list}));
				table.api().rows(function ( idx, data, node ) {
					return $.auth_platform.selected_session_mapping[data._id] === true ;
				}).remove().draw();
			}
		}
	});
	$('#btn_ip_add').on('click', function(){
		
	});
	
	$('#chb_session_refresh').on('click', function(){
		if($(this).is(":checked"))
		{
			$.auth_platform.websocket.send(JSON.stringify({op:'subscribe/session_list'}));
		}else
		{
			if($.auth_platform.websocket)
			{
				$.auth_platform.websocket.send(JSON.stringify({op:'unsubscribe/session_list'}));
			}
		}
	});
	
	
}


function ExtractRolesFromTree(deleteId)
{
	var ret = [];
	var roots = $.fn.zTree.getZTreeObj("userrole").getNodes();
	if(roots.length>0)
	{
		var root = roots[0];
		if(root.children && root.children.length>0)
		{
			for(var i in root.children)
			{
				if(deleteId)
				{
					if(root.children[i]._id && root.children[i]._id != deleteId)
					{
						ret.push(root.children[i]._id);
					}
				}else
				{
					if(root.children[i]._id)
					{
						ret.push(root.children[i]._id);
					}
				}
			}
		}
	}
	return ret;
}

function RefreshUserTree(_id)
{
	var root = {}
	for(var i in $.auth_platform.USER_LIST)
	{
		if($.auth_platform.USER_LIST[i]._id === _id)
		{
			var user = $.auth_platform.USER_LIST[i];
			root.name = user.username;
			root.children = [];
			var roles = user.roles;
			for(var j in roles)
			{
				if($.auth_platform.ROLE_MAP[roles[j]])
				{
					root.children.push({_id:roles[j], name:$.auth_platform.ROLE_MAP[roles[j]].name});
				}
			}
			break;
		}
	}
	if(!$.isEmptyObject(root))
	{
		init_users([root]);
	}
}

function FillUserForm(_id)
{
	for(var i in $.auth_platform.USER_LIST)
	{
		var user = $.auth_platform.USER_LIST[i];
		if(user._id === _id)
		{
			$('#user_username').val(user.username);
			$('#user_password').val(user.password);
			break;
		}
	}
	
}

function init_select()
{
	$.auth_platform.role_query(function(data1){
		if(data1.result)
		{
			alert(data1.result);
			return;
		}
		var html = '<option value=""></option>';
		var data = $.auth_platform.ROLE_LIST;
		//console.log(data);
		for(var i in data)
		{
			html += '<option value="' + data[i]._id + '">' + data[i].name + '</option>';
		}
		$('#role_list').append(html);
		
		$('#role_list').on('change', function(e){
			
			if(e.target.value.length>0)
			{
				RefreshRoleTree(e.target.value);
				FillRoleForm(e.target.value);
			}else
			{
				try{
					$.fn.zTree.destroy("roles");
				}catch(e)
				{
				}
				$('#role_name').val('');
				$('#role_desc').val('');
			}
		});
		init_roles([]);
	});
	$.auth_platform.user_query(function(data1){
		if(data1.result)
		{
			alert(data1.result);
			return;
		}
		var html = '<option value=""></option>';
		var data = $.auth_platform.USER_LIST;
		//console.log(data);
		for(var i in data)
		{
			html += '<option value="' + data[i]._id + '">' + data[i].username + '</option>';
		}
		$('#user_list').append(html);
		
		$('#user_list').on('change', function(e){
			
			if(e.target.value.length>0)
			{
				RefreshUserTree(e.target.value);
				FillUserForm(e.target.value);
			}else
			{
				try{
					$.fn.zTree.destroy("userrole");
				}catch(e)
				{
				}
				$('#user_username').val('');
			}
		});
		init_users([]);
	});
}

function init_websocket()
{
	var wsurl =  "ws://" + $.auth_platform.AUTH_HOST + ":" + $.auth_platform.AUTH_PORT + "/websocket";
	if($.auth_platform.websocket === undefined)
	{
		$.auth_platform.websocket = new WebSocket(wsurl);
	}
	if($.auth_platform.websocket)
	{
		$.auth_platform.websocket.onopen = function() 
		{
			//$.auth_platform.websocket.send(JSON.stringify({op:'session_list'}));
			$.auth_platform.websocket.send(JSON.stringify({}));
		};
		$.auth_platform.websocket.onclose = function(e) 
		{
			console.log("websocket close");
		};
		$.auth_platform.websocket.onerror = function(e) 
		{
			console.log("websocket error:" + e);
			$.auth_platform.websocket.close();
		};
		$.auth_platform.websocket.onmessage = function(e) 
		{
			//console.log("websocket onmessage:" + e.data);
			if(e.data.length>0)
			{
				var obj = JSON.parse(e.data);
				if(obj instanceof Array)
				{
					init_table(obj);
				}
				
			}
		};
	}		

}

function init_table(array)
{
	if($.auth_platform.table_session_list === undefined)
	{
		$.auth_platform.table_session_list = $('#table_session_list').dataTable( {
			className:"dt-body-center",
			data: array,
			columns: [
				//{ title: "选择", data: "_selected", className: "dt-body-center" , render: function ( data, type, row ) {
					//return '<input type="checkbox" class="editor-active">';
				//}},
				{ title: "选择", data: "_selected", className: "dt-body-center" , defaultContent:'<input type="checkbox" class="editor-active">'},
				{ title: "ID", data: "_id", className: "dt-body-center" ,  defaultContent:""},
				{ title: "IP地址", data: "ip" , className: "dt-body-center",  defaultContent:""},
				{ title: "用户名", data: "username" , className: "dt-body-center",  defaultContent:""},
				{ title: "最新活动时间", data: "session_timestamp" , className: "dt-body-center",  defaultContent:""}
			]
		} );
		
		$('#table_session_list').on( 'change', 'input.editor-active', function () {
			var id = $(this).parent().next().html();
			if($(this).is(":checked"))
			{
				$.auth_platform.selected_session_mapping[id] = true;
			}else
			{
				//if($.auth_platform.selected_session_mapping[id])
				//{
					delete $.auth_platform.selected_session_mapping[id];
				//}
			}
		} );		
		
	}else
	{
		//if($('#chb_session_refresh').is(":checked"))
		//{
			$.auth_platform.table_session_list.fnClearTable();
			$.auth_platform.table_session_list.fnAddData(array);
			$.auth_platform.selected_session_mapping = {};
		//}
	}
	//$.auth_platform.table_session_list.fnDraw();
}

function init()
{

	$.auth_platform.function_query(  function(nodes){
		init_functions();
		init_test();
		init_role_template();
		init_button();
		init_select();
		init_websocket();
		
	});
}

    
$(function() {
    init();
});
}

