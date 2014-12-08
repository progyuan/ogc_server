$.auth_platform = {};
$.auth_platform.AUTH_HOST = 'yncaiyun.com';
$.auth_platform.AUTH_PROTOCOL = 'http';
$.auth_platform.AUTH_PORT = '88';




$.auth_platform.login = function(data, callback)
{
    var url = $.auth_platform.AUTH_PROTOCOL + '://' + $.auth_platform.AUTH_HOST + ':' + $.auth_platform.AUTH_PORT + '/login';
    $.post( url, encodeURIComponent(JSON.stringify(data)),  function(data1) {
        var ret = JSON.parse(decodeURIComponent(data1));
        if(callback)
        {
            callback(ret);
        }
    }, 'text');
};


$.auth_platform.logout = function(callback)
{
    var url = $.auth_platform.AUTH_PROTOCOL + '://' + $.auth_platform.AUTH_HOST + ':' + $.auth_platform.AUTH_PORT + '/logout';
    $.get( url,   function(data1) {
        var ret = JSON.parse(decodeURIComponent(data1));
        if(callback)
        {
            callback(ret);
        }
    }, 'text');
};


$.auth_platform.auth_check = function(username, callback)
{
    var url = $.auth_platform.AUTH_PROTOCOL + '://' + $.auth_platform.AUTH_HOST + ':' + $.auth_platform.AUTH_PORT + '/auth_check';
    var data = {username:username};
    $.post( url, data, function(data1) {
        var ret = JSON.parse(decodeURIComponent(data1));
        if(callback)
        {
            callback(ret);
        }
    }, 'text');
};

$.auth_platform.register = function(username, password, callback)
{
    var url = $.auth_platform.AUTH_PROTOCOL + '://' + $.auth_platform.AUTH_HOST + ':' + $.auth_platform.AUTH_PORT + '/register';
    var data = {username:username, password:password};
    $.post( url, data, function(data1) {
        var ret = JSON.parse(decodeURIComponent(data1));
        if(callback)
        {
            callback(ret);
        }
    }, 'text');
};






$(function() {
    var data = {username:'aaa', password:'123'};
    $.auth_platform.login(data, function(data1){
        console.log(data1);    
    });

});

