$.chat_platform = {};
$.chat_platform.HOST = 'yncaiyun1.com';
$.chat_platform.PROTOCOL = 'http';
$.chat_platform.WS_PROTOCOL = 'ws';
$.chat_platform.PORT = '8092';
$.chat_platform.DEBUG = true;
$.chat_platform.ME_PREFIX = '我';
$.chat_platform.SYSTEM_PREFIX = '[系统]';
$.chat_platform.chat_options = {};
$.chat_platform.security = {};
$.chat_platform.security.url_hash_enable = true;
$.chat_platform.security.md5prefix = 'ruyvnvkjfgdgfs';

$.chat_platform.hash_object = function(obj)
{
	var plain = $.chat_platform.security.md5prefix + '_|_' + moment().format('YYYYMMDDHH');
	var hash = CryptoJS.MD5(plain);
	var token = hash.toString(CryptoJS.enc.Hex);
	obj._token = token;
	return obj;
};

$.chat_platform.post_cors = function(action, data, callback)
{
    var url = $.chat_platform.PROTOCOL + '://' + $.chat_platform.HOST + ':' + $.chat_platform.PORT + '/' + action;
    if($.chat_platform.security.url_hash_enable)
	{
		data = $.chat_platform.hash_object(data);
	}
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

$.chat_platform.user_get = function(data, callback)
{
	$.chat_platform.post_cors('user_get', data, callback);
};

$.chat_platform.group_get = function(data, callback)
{
	$.chat_platform.post_cors('group_get', data, callback);
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


$.chat_platform.user_contact_get = function(data, callback)
{
    if(data['_id'] === undefined)
    {
        throw "user_id_required";
    }
	//data['user_detail'] = true;
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
    if(data['owner_id'] === undefined)
    {
        throw "owner_id_required";
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


$.chat_platform.offline = function()
{
	if($.chat_platform.websocket)
	{
		$.chat_platform.websocket.close();
		$.chat_platform.websocket = undefined;
	}
};

$.chat_platform.chat = function(data){
	if($.chat_platform.websocket)
	{
		var d = {};
		d.op = 'chat/chat';
		d.msg = data.msg;
		if (data.to)
		{
			d.to = data.to;
		}
		if (data.to_group)
		{
			d.to_group = data.to_group;
		}
		if($.chat_platform.current_user_id)
		{
			d.from = $.chat_platform.current_user_id;
		}else if($.chat_platform.current_username)
		{
			d.from = $.chat_platform.current_username;
		}else
		{
			throw "$.chat_platform.current_user_id or $.chat_platform.current_username must be set";
		}
		
		if(d.to || d.to_group)
		{
			if(data.msg)
			{
				$.chat_platform.websocket.send(JSON.stringify(d));
			}else
			{
				throw "data.msg must not be null";
			}
		}else
		{
			throw "data.to or data.to_group must be set";
		}
	}else
	{
		throw "you must call $.chat_platform.online first.";
	}
};

$.chat_platform.online = function(options){
	if($.chat_platform.current_username === undefined && $.chat_platform.current_user_id === undefined )
	{
		var s =  "$.chat_platform.current_username or $.chat_platform.current_user_id must be set.\n";
		s += "For example:\n";
		s += "$.chat_platform.current_username = 'user1';\n";
		s += "Or:\n";
		s += "$.chat_platform.current_user_id = '1234567890';\n";
		throw s;
	}
	if(! (options.on_error instanceof Function))
	{
		var s = "options.on_error must be defined as function.\n ";
		s += "options.on_error = function(data){\n";
		s += "	data//error message. \n";
		s += "};\n";
		throw s;
	}
	if(! (options.on_online instanceof Function))
	{
		var s = "options.on_online must be defined as function.\n ";
		s += "options.on_online = function(data){\n";
		s += "	data._id //current user's id(string)\n";
		s += "	data.username //current user's unique username(string)\n";
		s += "	data.display_name //current user's display name(string)\n";
		s += "	data.person_info //current user's personal info(object)\n";
		s += "	data.avatar //current user's head icon(string)\n";
		s += "	data.contacts //current user's contacts list(list)\n";
		s += "	data.groups //current user's groups list(list) which contains it\n";
		s += "	data.op //it is 'chat/online' in this case\n";
		s += "};\n";
		throw s;
	}
	//if(! options.on_offline instanceof Function)
	//{
		//var s = "options.on_online must be defined.\n ";
		//s += "options.on_online = function(data){\n";
		//s += "	data._id //current user's id(string)\n";
		//s += "	data.op //it is 'chat/online' in this case\n";
		//s += "};\n";
		//throw s;
	//}
	if(! (options.on_info_online instanceof Function))
	{
		var s = "options.on_info_online must be defined as function.\n ";
		s += "options.on_info_online = function(data){\n";
		s += "	data.from //user's id who inform this online event(string)\n";
		s += "	data.op //it is 'chat/info/online' in this case\n";
		s += "};\n";
		throw s;
	}
	if(! (options.on_info_offline instanceof Function))
	{
		var s = "options.on_info_offline must be defined as function.\n ";
		s += "options.on_info_offline = function(data){\n";
		s += "	data.from //user's id who inform this offline event(string)\n";
		s += "	data.op //it is 'chat/info/offline' in this case\n";
		s += "};\n";
		throw s;
	}
	if(! (options.on_chat instanceof Function))
	{
		var s = "options.on_chat must be defined as function.\n ";
		s += "options.on_chat = function(data){\n";
		s += "	data.from //user's id who send this message(string).\n";
		s += "	data.to //user's id who recv this message(string).\n";
		s += "	data.timestamp //message timestamp(datetime).\n";
		s += "	data.msg //message body(string or object).\n";
		s += "	data.op //it is 'chat/chat' in this case.\n";
		s += "};\n";
		throw s;
	}
	if(! (options.on_request_contact_add instanceof Function))
	{
		var s = "options.on_request_contact_add must be defined as function.\n ";
		s += "options.on_request_contact_add = function(data){\n";
		s += "	data.from //user's id who send this request(string).\n";
		s += "	data.to //user's id who recv this request(string).\n";
		s += "	data._id //sender's id(string)\n";
		s += "	data.username //sender's unique username(string)\n";
		s += "	data.display_name //sender's display name(string)\n";
		s += "	data.person_info //sender's personal info(object)\n";
		s += "	data.avatar //sender's head icon(string)\n";
		s += "	data.op //it is 'chat/request/contact/add' in this case.\n";
		s += "};\n";
		throw s;
	}
	if(! (options.check_contact_add instanceof Function))
	{
		var s = "options.check_contact_add must be defined as function which return boolean value.\n ";
		s += "options.check_contact_add = function(data){\n";
		s += "	if(...)//this should block UI mainloop.\n";
		s += "		return true;\n";
		s += "	else\n";
		s += "		return false;\n";
		s += "};\n";
		throw s;
	}
	if(! (options.on_response_contact_add_accept instanceof Function))
	{
		var s = "options.on_response_contact_add_accept must be defined as function .\n ";
		s += "Both receiver and sender will trigger this event.\n";
		s += "options.on_response_contact_add_accept = function(data){\n";
		s += "	data.from //user's id who send this request(string).\n";
		s += "	data.to //user's id who recv this request(string).\n";
		s += "	data._id //sender's id(string)\n";
		s += "	data.op //it is 'chat/response/contact/add/accept' in this case.\n";
		s += "	data.contacts //receiver(or sender)'s contacts list(list).\n";
		s += "};\n";
		throw s;
	}
	if(! (options.on_response_contact_add_reject instanceof Function))
	{
		var s = "options.on_response_contact_add_reject must be defined as function .\n ";
		s += "Only  sender will trigger this event.\n";
		s += "options.on_response_contact_add_reject = function(data){\n";
		s += "	data.from //user's id who send this request(string).\n";
		s += "	data.to //user's id who recv this request(string).\n";
		s += "	data._id //sender's id(string)\n";
		s += "	data.username //sender's unique username(string)\n";
		s += "	data.display_name //sender's display name(string)\n";
		s += "	data.person_info //sender's personal info(object)\n";
		s += "	data.avatar //sender's head icon(string)\n";
		s += "	data.op //it is 'chat/response/contact/add/reject' in this case.\n";
		s += "	data.reject_reason //receiver's reject reason(string).\n";
		s += "};\n";
		throw s;
	}
	if(! (options.on_request_contact_remove instanceof Function))
	{
		var s = "options.on_request_contact_remove must be defined as function.\n ";
		s += "Both receiver and sender will trigger this event.\n";
		s += "options.on_request_contact_remove = function(data){\n";
		s += "	data.from //user's id who send this request(string).\n";
		s += "	data.to //user's id who recv this request(string).\n";
		s += "	data._id //sender's id(string)\n";
		s += "	data.op //it is 'chat/request/contact/remove' in this case.\n";
		s += "	data.contacts //receiver(or sender)'s contacts list(list).\n";
		s += "};\n";
		throw s;
	}
	if(! (options.on_request_group_join instanceof Function))
	{
		var s = "options.on_request_group_join must be defined as function.\n ";
		s += "options.on_request_group_join = function(data){\n";
		s += "	data.from //user's id who send this request(string).\n";
		s += "	data.to //user's id who own this group(string).\n";
		s += "	data._id //user's id who own this group(string)\n";
		s += "	data.username //owner's unique username(string)\n";
		s += "	data.display_name //owner's display name(string)\n";
		s += "	data.person_info //owner's personal info(object)\n";
		s += "	data.avatar //sender's head icon(string)\n";
		s += "	data.op //it is 'chat/request/group/join' in this case.\n";
		s += "	data.request_src //user's id who send this request(string).\n";
		s += "	data.to_group //group's id sender want join(string).\n";
		s += "};\n";
		throw s;
	}
	if(! (options.check_group_join instanceof Function))
	{
		var s = "options.check_group_join must be defined as function which return boolean value.\n ";
		s += "options.check_group_join = function(data){\n";
		s += "	if(...)//this should block UI mainloop.\n";
		s += "		return true;\n";
		s += "	else\n";
		s += "		return false;\n";
		s += "};\n";
		throw s;
	}
	if(! (options.on_response_group_join_accept instanceof Function))
	{
		var s = "options.on_response_group_join_accept must be defined as function .\n ";
		s += "All the group members will trigger this event.\n";
		s += "options.on_response_group_join_accept = function(data){\n";
		s += "	data.from //user's id who send this request(string).\n";
		s += "	data.request_src //user's id who send this request(string).\n";
		s += "	data.to_group //group's id sender want join(string).\n";
		s += "	data.op //it is 'chat/response/group/join/accept' in this case.\n";
		s += "};\n";
		throw s;
	}
	if(! (options.on_response_group_join_reject instanceof Function))
	{
		var s = "options.on_response_group_join_reject must be defined as function .\n ";
		s += "Only  sender will trigger this event.\n";
		s += "options.on_response_group_join_reject = function(data){\n";
		s += "	data.from //group owner's id(string).\n";
		s += "	data.to //sender's id(string).\n";
		s += "	data._id //group owner's id(string)\n";
		s += "	data.username //group owner's unique username(string)\n";
		s += "	data.display_name //group owner's display name(string)\n";
		s += "	data.person_info //group owner's personal info(object)\n";
		s += "	data.avatar //group owner's head icon(string)\n";
		s += "	data.op //it is 'chat/response/group/join/reject' in this case.\n";
		s += "	data.to_group //group's id sender want join(string).\n";
		s += "	data.reject_reason //group owner's reject reason(string).\n";
		s += "};\n";
		throw s;
	}
	if(! (options.on_request_group_quit instanceof Function))
	{
		var s = "options.on_request_group_quit must be defined as function.\n ";
		s += "All the group members will trigger this event.\n";
		s += "options.on_request_group_quit = function(data){\n";
		s += "	data.from //user's id who send this request(string).\n";
		s += "	data.to //user's id who recv this request(string).\n";
		s += "	data.op //it is 'chat/request/group/quit' in this case.\n";
		s += "};\n";
		throw s;
	}
	data = {};
	if($.chat_platform.current_username)
	{
		data.username = $.chat_platform.current_user;
	}
	else if($.chat_platform.current_user_id)
	{
		data._id = $.chat_platform.current_user_id;
	}
	data['op'] = 'chat/online';
	data['inform_contact'] = true;
	var wsurl =  $.chat_platform.WS_PROTOCOL + "://" + $.chat_platform.HOST + ":" + $.chat_platform.PORT + "/websocket";
	if($.chat_platform.websocket === undefined)
	{
		$.chat_platform.websocket = new WebSocket(wsurl);
	}
	if($.chat_platform.websocket)
	{
		$.chat_platform.websocket.onopen = function() 
		{
			$.chat_platform.websocket.send(JSON.stringify(data));
		};
		$.chat_platform.websocket.onclose = function(e) 
		{
			console.log("websocket close");
		};
		$.chat_platform.websocket.onerror = function(e) 
		{
			console.log("websocket error:" + e);
			$.chat_platform.offline();
		};
		$.chat_platform.websocket.onmessage = function(e) 
		{
			if(e.data.length>0)
			{
				var data1 = JSON.parse(e.data);
				
				if(data1 instanceof Array)
				{
				}
				if(data1 instanceof Object)
				{
					if(data1.result)
					{
						var callback = options.on_error;
						callback(data1.result);
					}
					else
					{
						if(data1.op === 'chat/online')
						{
							var callback = options.on_online;
							callback(data1);
						}
						
						if(data1.op === 'chat/info/online')
						{
							var callback = options.on_info_online;
							callback(data1);
						}
						
						if( data1.op === 'chat/info/offline')
						{
							var callback = options.on_info_offline;
							callback(data1);
						}
						if(data1.op === 'chat/chat')
						{
							var callback = options.on_chat;
							callback(data1);
						}
						if(data1.op === 'chat/request/contact/add')
						{
							var callback = options.on_request_contact_add;
							callback(data1);
							var check_contact_add = options.check_contact_add;
							var o = {from:data1.to, to:data1.from};
							if(check_contact_add(data1))
							{
								o.op = 'chat/response/contact/add/accept';
								if($.chat_platform.websocket)
								{
									$.chat_platform.websocket.send(JSON.stringify(o));
								}
							}else
							{
								o.op = 'chat/response/contact/add/reject';
								if($.chat_platform.websocket)
								{
									$.chat_platform.websocket.send(JSON.stringify(o));
								}
							}
						}
						if(data1.op === 'chat/response/contact/add/reject')
						{
							var callback = options.on_response_contact_add_reject;
							callback(data1);
						}
						if(data1.op === 'chat/response/contact/add/accept')
						{
							var callback = options.on_response_contact_add_accept;
							callback(data1);
						}
						if(data1.op === 'chat/request/contact/remove')
						{
							var callback = options.on_request_contact_remove;
							callback(data1);
						}
						if(data1.op === 'chat/request/group/join')
						{
							var callback = options.on_request_group_join;
							callback(data1);
							var check_group_join = options.check_group_join;
							if(check_group_join(data1))
							{
								if($.chat_platform.websocket)
								{
									$.chat_platform.websocket.send(JSON.stringify({op:'chat/response/group/join/accept',from:data1.to, to:data1.from, to_group:data1.to_group, request_src:data1.request_src}));
								}
							}else
							{
								if($.chat_platform.websocket)
								{
									$.chat_platform.websocket.send(JSON.stringify({op:'chat/response/group/join/reject',from:data1.to, to:data1.from, to_group:data1.to_group, request_src:data1.request_src}));
								}
							}
						}
						if(data1.op === 'chat/response/group/join/accept')
						{
							var callback = options.on_response_group_join_accept;
							callback(data1);
						}
						if(data1.op === 'chat/response/group/join/reject')
						{
							var callback = options.on_response_group_join_reject;
							callback(data1);
						}
						if(data1.op === 'chat/request/group/quit')
						{
							var callback = options.on_request_group_quit;
							callback(data1);
						}
					}
				}
				
			}else
			{
				$.chat_platform.websocket.send('');
			}
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
			$.chat_platform.user_contact_get({_id:$(this).val(), user_detail:true}, function(data1){
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
		$('#group_list_7').off();
        $('#group_list_7').on('change', function(){
			$.chat_platform.group_get({_id:$(this).val(),user_detail:true}, function(data1){
				if(data1.result)
				{
					alert(data1.result);
				}
				else if(data1.length>0)
				{
					members = data1[0]['members'];
					$('#user_group_7').empty();
					var s = '';
					for(var i in members)
					{
						s += '<option value="' + members[i]['_id'] + '">' + members[i]['display_name'] + '</option>';
					}
					$('#user_group_7').append(s);
				}
			});
		});
	}
	
	function update_online_list()
	{
		$.chat_platform.post_cors('user_get', {user_detail:true}, function(data1){
			if(data1.result)
			{
				alert(data1.result);
			}else
			{
				$('#online_list_5').empty();
				var s = '';
				for(var i in data1)
				{
					if(data1[i].online_status === 'online')
					{
						s += '<option value="' + data1[i]._id + '">' + data1[i].display_name + '</option>';
					}
				}
				$('#online_list_5').append(s);
			}
		});
	}
	
	function update_contact_list(data)
	{
		
		if(data.result)
		{
			alert(data.result);
			return;
		}
		if((data.op === 'chat/online' || data.op === 'chat/response/contact/add/accept' || data.op === 'chat/request/contact/remove') && data.contacts)
		{
			$('#current_contact_6').empty();
			var s = '';
			for(var i in data.contacts)
			{
				var status = '';
				if(data['contacts'][i]['online_status'] === 'online')
				{
					status = '(在线)';
				}
				s += '<option value="' + data['contacts'][i]['_id'] + '">' + data['contacts'][i]['display_name'] + status + '</option>';
			}
			$('#current_contact_6').append(s);
		}
		if(data.op === 'chat/info/online' && data['from'])
		{
			var id = data['from'];
			var text = $('#current_contact_6 option[value="' + id + '"]').text();
			if(text && text.indexOf('(在线)') < 0)
			{
				$('#current_contact_6 option[value="' + id + '"]').text(text + '(在线)');
			}
		}
		if(data.op === 'chat/info/offline' && data['from'])
		{
			var id = data['from'];
			var text = $('#current_contact_6 option[value="' + id + '"]').text();
			if(text && text.indexOf('(在线)') > -1)
			{
				text = text.replace('(在线)', '');
				$('#current_contact_6 option[value="' + id + '"]').text(text);
			}
		}
	}
	
	function get_select_text(sel_id, value)
	{
		var ret = value;
		var text = $('#' + sel_id + ' option[value="' + value + '"]').text();
		if(text)
		{
			if(text.indexOf('(在线)') > -1)
			{
				text = text.replace('(在线)', '');
			}
			ret = text;
		}
		return ret;
	}
	
	
	
	
    $(function() {
	
		$.chat_platform.user_get( {}, function(data1){
			if(data1.result)
			{
				alert(data1.result);
			}else
			{
				update_user_list(data1);
			}
		});
		$.chat_platform.group_get( {}, function(data1){
			if(data1.result)
			{
				alert(data1.result);
			}else
			{
				update_group_list(data1);
			}
		});
    
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
				$.chat_platform.group_add({group_name:$('#group_name').val(), owner_id:$('#current_user_3').val(),description:$('#group_description').val()}, function(data1){
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
        $('#btn_user_online').on('click', function(){
			$(this).attr('disabled', 'disabled');
			$('#btn_user_offline').removeAttr('disabled');
			$('#btn_send').removeAttr('disabled');
			var sel = $('#user_list_5').val();
			$('#user_list_5').attr('disabled', 'disabled');
			
			if(sel)
			{
				$.chat_platform.current_user_id = sel;
				var options = {
					on_error:function(data1){
						console.log(data1);
					},
					on_online: function(data1){
						
						update_online_list();
						update_contact_list(data1);
					},
					on_info_online: function(data1){
						
						update_online_list();
						update_contact_list(data1);
					},
					on_info_offline: function(data1){
						update_online_list();
						update_contact_list(data1);
					},
					on_chat: function(data1){
						var from_user = get_select_text('current_contact_6', data1.from);
						$('#recv_msg').text(  $('#recv_msg').text() + '\n' + from_user + ':' + data1.msg);
					},
					check_contact_add: function(data1){
						return confirm('[' + data1.display_name + ']请求你加他(她)为好友,是否同意?');
					},
					on_request_contact_add: function(data1){
						console.log('[' + data1.display_name + ']请求你加他(她)为好友');
					},
					on_response_contact_add_accept: function(data1){
						update_contact_list(data1);
						var id = data1.from;
						var text = get_select_text('current_contact_6', id);
						$('#recv_msg').text(  $('#recv_msg').text() + '\n' + $.chat_platform.SYSTEM_PREFIX + ':' + '[' + text + ']已将你添加为好友');
					},
					on_response_contact_add_reject: function(data1){
						var reason = '';
						if(data1.reject_reason)
						{
							reason = ',原因是:[' + data1.reject_reason + ']';
						}
						$('#recv_msg').text(  $('#recv_msg').text() + '\n' + $.chat_platform.SYSTEM_PREFIX + ':' + '[' + data1.display_name + ']已将你拒绝' + reason);
					},
					on_request_contact_remove: function(data1){
						var id = data1.from;
						var text = get_select_text('current_contact_6', id);
						$('#recv_msg').text(  $('#recv_msg').text() + '\n' + $.chat_platform.SYSTEM_PREFIX + ':' + '[' + text + ']已将你从好友列表中移除');
						update_contact_list(data1);
					},
					on_request_group_join: function(data1){
						var group_name = get_select_text('group_list_7', data1.to_group);
						console.log('[' + data1.display_name + ']请求你加他(她)进组[' + group_name + ']');
					},
					check_group_join: function(data1){
						var group_name = get_select_text('group_list_7', data1.to_group);
						return confirm('[' + data1.display_name + ']请求你加他(她)进组[' + group_name + '],是否同意?');
					},
					on_response_group_join_accept: function(data1){
						var group_name = get_select_text('group_list_7', data1.to_group);
						var new_name = get_select_text('user_list_5', data1.request_src);
						$('#recv_msg').text(  $('#recv_msg').text() + '\n' + $.chat_platform.SYSTEM_PREFIX + ':' + '[' + new_name + ']已成功加入组[' + group_name + ']' );
					},
					on_response_group_join_reject: function(data1){
						var reason = '';
						if(data1.reject_reason)
						{
							reason = ',原因是:[' + data1.reject_reason + ']';
						}
						var group_name = get_select_text('group_list_7', data1.to_group);
						$('#recv_msg').text(  $('#recv_msg').text() + '\n' + $.chat_platform.SYSTEM_PREFIX + ':' + '[' + data1.display_name + ']已将你拒绝加入组[' + group_name + ']' + reason);
					},
					on_request_group_quit: function(data1){
						var id = data1.from;
						var gid = data1.to_group;
						var text = get_select_text('user_group_7', id);
						var gtext = get_select_text('group_list_7', gid);
						$('#recv_msg').text(  $('#recv_msg').text() + '\n' + $.chat_platform.SYSTEM_PREFIX + ':' + '[' + text + ']已退出组[' + gtext + ']');
						$('#user_group_7 option:selected').remove();
					}
				};
				$.chat_platform.online(options);
			}
			
        });
		$('#btn_user_offline').attr('disabled', 'disabled');
		$('#btn_send').attr('disabled', 'disabled');
		
        $('#btn_user_offline').on('click', function(){
			$('#btn_user_online').removeAttr('disabled');
			$(this).attr('disabled', 'disabled');
			$('#btn_send').attr('disabled', 'disabled');
			$('#user_list_5').removeAttr('disabled');
			$.chat_platform.offline();
			update_online_list();
			$('#current_contact_6').empty();
        });
        $('#btn_clear_recv').on('click', function(){
			$('#recv_msg').text('');
        });
		
        $('#btn_send').on('click', function(){
			var sel = $('#current_contact_6').val();
			var v = $('#send_msg').val();
			if(sel && v && v.length>0 && $.chat_platform.websocket)
			{
				$('#recv_msg').text(  $('#recv_msg').text() + '\n' + $.chat_platform.ME_PREFIX + ':' + v);
				$.chat_platform.chat({to:sel, msg:v});
			}
			$('#send_msg').val('');
        });
        $('#btn_request_contact_add').on('click', function(){
			var to = $('#online_list_5').val();
			var from = $('#user_list_5').val();
			var text = $('#online_list_5 option:selected').text();
			if(from && to && from.length>0 && to.length>0 && $.chat_platform.websocket)
			{
				$('#recv_msg').text(  $('#recv_msg').text() + '\n' + $.chat_platform.ME_PREFIX + ':' + '请求添加[' + text + ']为好友,等待对方回复...');
				$.chat_platform.websocket.send(JSON.stringify({op:'chat/request/contact/add',from:from,to:to}));
			}
        });
        $('#btn_request_contact_remove').on('click', function(){
			var from = $('#user_list_5').val();
			var to = $('#current_contact_6').val();
			var text = $('#current_contact_6 option:selected').text();
			if(from && to && from.length>0 && to.length>0 && $.chat_platform.websocket)
			{
				if(confirm('你确定要从好友列表移除[' + text + ']吗?'))
				{
					$('#recv_msg').text(  $('#recv_msg').text() + '\n' + $.chat_platform.ME_PREFIX + ':' + '从好友列表移除[' + text + ']');
					$.chat_platform.websocket.send(JSON.stringify({op:'chat/request/contact/remove',from:from,to:to}));
				}
			}
        });
        $('#btn_group_add_request').on('click', function(){
			var from = $('#user_list_5').val();
			var to_group = $('#group_list_7').val();
			var text = $('#group_list_7 option:selected').text();
			if(from && to_group && from.length>0 && to_group.length>0 && $.chat_platform.websocket)
			{
				if(confirm('你确定要加入组[' + text + ']吗?'))
				{
					$('#recv_msg').text(  $('#recv_msg').text() + '\n' + $.chat_platform.ME_PREFIX + ':' + '请求加入组[' + text + '],等待确认中...');
					$.chat_platform.websocket.send(JSON.stringify({op:'chat/request/group/join',from:from,to_group:to_group}));
				}
			}
        });
        $('#btn_group_quit').on('click', function(){
			var from = $('#user_list_5').val();
			var to_group = $('#group_list_7').val();
			var text = $('#group_list_7 option:selected').text();
			if(from && to_group && from.length>0 && to_group.length>0 && $.chat_platform.websocket)
			{
				if(confirm('你确定要退出组[' + text + ']吗?'))
				{
					$('#recv_msg').text(  $('#recv_msg').text() + '\n' + $.chat_platform.ME_PREFIX + ':' + '退出组[' + text + ']');
					$.chat_platform.websocket.send(JSON.stringify({op:'chat/request/group/quit',from:from, to_group:to_group}));
				}
			}
        });
		
		
		
	});
}

