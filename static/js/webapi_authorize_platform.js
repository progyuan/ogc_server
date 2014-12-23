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
    if(data.name === undefined || data.name.length == 0)
    {
        data.name = '';
    }
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

$.auth_platform.role_func_template_save = function(data, callback)
{
    $.auth_platform.post_cors('role_func_template_save', data, callback)
};

$.auth_platform.role_func_template_get = function(callback)
{
    $.auth_platform.post_cors('role_func_template_get', data, callback)
};


if($.auth_platform.DEBUG)
{

function beforeDrag(treeId, treeNodes) {
	for (var i=0,l=treeNodes.length; i<l; i++) {
		if (treeNodes[i].drag === false) {
			return false;
		}
	}
	return true;
}
function beforeDrop(treeId, treeNodes, targetNode, moveType) {
	return targetNode ? targetNode.drop !== false : true;
}

function BeforeRemoveTemplate(treeId, treeNode)
{
}
function BeforeRenameTemplate(treeId, treeNode, newName, isCancelBoolean)
{
	console.log(treeNode._id);
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
			showRemoveBtn: false,
			showRenameBtn: false
		},
		callback: {
			beforeDrag: beforeDrag,
			beforeDrop: beforeDrop
		}
	};

    var nodes = [];
    for(var i=0; i<10; i++)
    {
        nodes.push({_id:i.toString(), name:"功能" + i});
    }
    $.fn.zTree.init($("#funclist"), setting, nodes);
}
function init_right()
{
	var setting = {
		edit: {
			enable: true,
			showRemoveBtn: true,
			showRenameBtn: true
		},
		callback: {
			beforeDrag: beforeDrag,
			beforeDrop: beforeDrop,
			beforeRemove:BeforeRemoveTemplate,
			beforeRename:BeforeRenameTemplate
		},
		check:{
			enable : true,
			autoCheckTrigger: true,
			chkStyle : "checkbox",
			chkboxType: { "Y": "ps", "N": "ps" }
		}
	};
    var nodes = [];
    for(var i=0; i<3; i++)
    {
        nodes.push({_id:"cat_" + i, name:"类别" + i});
    }
    $.fn.zTree.init($("#roletemplate"), setting, nodes);

}

    
$(function() {
    
});
}

