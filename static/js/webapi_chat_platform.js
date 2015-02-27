$.chat_platform = {};
$.chat_platform.HOST = 'yncaiyun1.com';
$.chat_platform.PROTOCOL = 'http';
$.chat_platform.PORT = '8091';
$.chat_platform.DEBUG = true;
$.chat_platform.test_user = 'aaa';


$.chat_platform.post_cors = function(action, data, callback)
{
    var url = $.chat_platform.PROTOCOL + '://' + $.chat_platform.HOST + ':' + $.chat_platform.PORT + '/' + action;
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
                callback(ret);
            }
        }
    });
};

$.chat_platform.user_add = function(data, callback)
{
    if(data['username'] === undefined)
    {
        throw "username_required";
    }
    if(data['password'] === undefined)
    {
        throw "password_required";
    }
	$.chat_platform.post_cors('user_add', data, callback);
};

$.chat_platform.user_update = function(data, callback)
{
    if(data['_id'] === undefined)
    {
        throw "user_id_required";
    }
	$.chat_platform.post_cors('user_update', data, callback);
};
$.chat_platform.user_remove = function(data, callback)
{
    if(data['_id'] === undefined)
    {
        throw "user_id_required";
    }
    if(data['password'] === undefined)
	$.chat_platform.post_cors('user_remove', data, callback);
};

//$.chat_platform.offline = function(data, callback)
//{
    //if(data['_id'] === undefined)
    //{
        //throw "user_id_required";
    //}
    //$.chat_platform.post_cors('offline', data, callback)
//};

$.chat_platform.user_contact_get = function(data, callback)
{
    if(data['_id'] === undefined)
    {
        throw "user_id_required";
    }
	data['user_detail'] = true;
    $.chat_platform.post_cors('user_contact_get', data, callback)
};

$.chat_platform.user_group_get = function(data, callback)
{
    if(data['_id'] === undefined)
    {
        throw "user_id_required";
    }
	data['user_detail'] = true;
    $.chat_platform.post_cors('user_group_get', data, callback)
};
$.chat_platform.group_get = function(data, callback)
{
    //if(data['_id'] === undefined)
    //{
        //throw "user_id_required";
    //}
    $.chat_platform.post_cors('group_get', data, callback)
};
$.chat_platform.group_add = function(data, callback)
{
    if(data['found_user_id'] === undefined)
    {
        throw "found_user_id_required";
    }
    if(data['group_name'] === undefined)
    {
        throw "group_name_required";
    }
    $.chat_platform.post_cors('group_add', data, callback)
};

$.chat_platform.group_remove = function(data, callback)
{
    if(data['_id'] === undefined)
    {
        throw "group_id_required";
    }
    $.chat_platform.post_cors('group_remove', data, callback)
};

$.chat_platform.group_update = function(data, callback)
{
    if(data['_id'] === undefined)
    {
        throw "group_id_required";
    }
	$.chat_platform.post_cors('group_update', data, callback);
};


$.chat_platform.offline = function(data,  offline_callback)
{
	if($.chat_platform.websocket)
	{
		if(data.username)
		{
			$.chat_platform.websocket.send(JSON.stringify({op:'chat/offline',username:data.username}));
		}
		else if(data._id)
		{
			$.chat_platform.websocket.send(JSON.stringify({op:'chat/offline',_id:data._id}));
		}
		$.chat_platform.websocket.close();
		$.chat_platform.websocket = undefined;
		offline_callback();
	}
};

$.chat_platform.init_websocket = function(username, online_callback,  offline_callback, error_callback, message_callback)
{
	var wsurl =  "ws://" + $.chat_platform.HOST + ":" + $.chat_platform.PORT + "/websocket";
	if($.chat_platform.websocket === undefined)
	{
		$.chat_platform.websocket = new WebSocket(wsurl);
	}
	if($.chat_platform.websocket)
	{
		$.chat_platform.websocket.onopen = function() 
		{
			$.chat_platform.websocket.send(JSON.stringify({op:'chat/online',username:username}));
		};
		$.chat_platform.websocket.onclose = function(e) 
		{
			console.log("websocket close");
			offline_callback();
		};
		$.chat_platform.websocket.onerror = function(e) 
		{
			console.log("websocket error:" + e);
			$.chat_platform.websocket.close();
			error_callback(e);
		};
		$.chat_platform.websocket.onmessage = function(e) 
		{
			if(e.data.length>0)
			{
				var obj = JSON.parse(e.data);
				if(obj instanceof Array)
				{
				}
				if(obj instanceof Object)
				{
					if(obj.result)
					{
						error_callback(obj.result);
					}
					if(obj.op === 'chat/online')
					{
						online_callback(obj);
					}
					if(obj.op === 'chat/chat')
					{
						message_callback(obj);
					}
					
				}
				
			}
			$.chat_platform.websocket.send(JSON.stringify({}));
		};
	}		
};



if($.chat_platform.DEBUG)
{

	function update_user_list(data)
	{
		$('select[id^=current_user_]').empty();
		$('select[id^=user_list_]').empty();
		var s = '';
		for(var i in data)
		{
			s += '<option value="' + data[i]['_id'] + '">' + data[i]['display_name'] + '</option>';
		}
		$('select[id^=current_user_]').append(s);
		$('select[id^=user_list_]').append(s);
		
        $('#current_user_2').off();
        $('#current_user_2').on('change', function(){
			$.chat_platform.user_contact_get({_id:$(this).val()}, function(data1){
				//console.log(data1);
				$('#current_contact_2').empty();
				var s = '';
				for(var i in data1)
				{
					s += '<option value="' + data1[i]['_id'] + '">' + data1[i]['display_name'] + '</option>';
				}
				$('#current_contact_2').append(s);
			});
        });
		$('#current_user_2').trigger('change');
	}
	
	function update_group_list(data)
	{
		$('select[id^=current_group_]').empty();
		$('select[id^=group_list_]').empty();
		var s = '';
		for(var i in data)
		{
			s += '<option value="' + data[i]['_id'] + '">' + data[i]['group_name'] + '</option>';
		}
		$('select[id^=current_group_]').append(s);
		$('select[id^=group_list_]').append(s);
		
        $('#current_group_4').off();
        $('#current_group_4').on('change', function(){
			$.chat_platform.group_get({_id:$(this).val(),user_detail:true}, function(data1){
				//console.log(data1);
				if(data1.result)
				{
					alert(data1.result);
				}
				else if(data1.length>0)
				{
					members = data1[0]['members'];
					$('#user_group_4').empty();
					var s = '';
					for(var i in members)
					{
						s += '<option value="' + members[i]['_id'] + '">' + members[i]['display_name'] + '</option>';
					}
					$('#user_group_4').append(s);
				}
			});
        });
		$('#current_group_4').trigger('change');
		
	}
	
    $(function() {
	
	
		$.chat_platform.post_cors('user_get', {}, function(data1){
			if(data1.result)
			{
				alert(data1.result);
			}else
			{
				update_user_list(data1);
			}
		});
		$.chat_platform.post_cors('group_get', {}, function(data1){
			if(data1.result)
			{
				alert(data1.result);
			}else
			{
				update_group_list(data1);
			}
		});
		
		//$.chat_platform.init_websocket($.chat_platform.test_user, function(data1){
				//console.log('online_callback');
				//console.log(data1);
			//},
			//function(data1){
				//console.log('offline_callback');
				//console.log(data1);
			//},
			//function(data1){
				//console.log('error_callback');
				//console.log(data1);
			//},
			//function(data1){
				//console.log('message_callback');
				//console.log(data1);
			//}
		//);
		
		
    
        $('#btn_user_add').on('click', function(){
			var username = $('#username').val();
			var password = $('#password').val();
			if(username.length>0 && password.length>0 )
			{
				$.chat_platform.user_add({username:username, password:password}, function(data1){
					console.log(data1);
				});
			}
        });
        $('#btn_user_remove').on('click', function(){
			if(confirm("确定删除用户[" + $('#user_list_1').val() + "]吗?"))
			{
				$.chat_platform.user_remove({_id:$('#user_list_1').val()}, function(data1){
					console.log(data1);
				});
			}
        });
		
        $('#btn_contact_add').on('click', function(){
			var v = $('#user_list_2').val();
			var s = $('#user_list_2 option:selected').text();
			if(v)
			{
				//console.log(s);
				//console.log(v);
				var s = '<option value="' + v + '">' + s + '</option>';
				$('#current_contact_2').append(s);
			}
        });
        $('#btn_contact_remove').on('click', function(){
			//var sel = $('#current_contact_2').val();
			$('#current_contact_2 option:selected').remove();
        });
        $('#btn_contact_save').on('click', function(){
			var sel = $('#current_user_2').val();
			if(sel)
			{
				if(confirm("确定保存好友列表吗?"))
				{
					var contacts = [];
					$('#current_contact_2 option').each(function(){
						contacts.push($(this).val());
					});
					$.chat_platform.user_update({_id:sel,contacts:contacts}, function(data1){
						console.log(data1);
					});
				}
			}
        });
        $('#btn_group_add').on('click', function(){
			if($('#group_name').val().length>0 && $('#current_user_3').val() && $('#current_user_3').val().length>0)
			{
				$.chat_platform.group_add({group_name:$('#group_name').val(), found_user_id:$('#current_user_3').val(),description:$('#group_description').val()}, function(data1){
					console.log(data1);
				});
			}
        });
        $('#btn_group_remove').on('click', function(){
			var sel = $('#group_list_3').val();
			if(sel)
			{
				$.chat_platform.group_remove({_id:sel}, function(data1){
					console.log(data1);
				});
			}
        });
        $('#btn_user_group_add').on('click', function(){
			var v = $('#user_list_4').val();
			var s = $('#user_list_4 option:selected').text();
			if(v)
			{
				var s = '<option value="' + v + '">' + s + '</option>';
				$('#user_group_4').append(s);
			}
        });
        $('#btn_user_group_remove').on('click', function(){
			$('#user_group_4 option:selected').remove();
        });
        $('#btn_user_group_save').on('click', function(){
			var sel = $('#current_group_4').val();
			if(sel)
			{
				if(confirm("确定保存该用户组用户列表吗?"))
				{
					var members = [];
					$('#user_group_4 option').each(function(){
						members.push($(this).val());
					});
					$.chat_platform.group_update({_id:sel,members:members}, function(data1){
						console.log(data1);
					});
				}
			}
        });
		
	});
}

