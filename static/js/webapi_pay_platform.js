$.pay_platform = {};
$.pay_platform.PAY_HOST = 'yncaiyun.com';
$.pay_platform.PAY_PROTOCOL = 'http';
$.pay_platform.PAY_PORT = '8089';
$.pay_platform.DEBUG = true;


$.pay_platform.post_cors = function(action, data, callback)
{
    var url = $.pay_platform.PAY_PROTOCOL + '://' + $.pay_platform.PAY_HOST + ':' + $.pay_platform.PAY_PORT + '/' + action;
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

$.pay_platform.pay = function(data, callback)
{
    if(data['pay_channel'] === undefined)
    {
        throw "pay_channel_required";
    }
    if(data['buyer_email'] === undefined)
    {
        throw "buyer_email_required";
    }
    if(data['out_trade_no'] === undefined)
    {
        throw "out_trade_no_required";
    }
    if(data['seller_email'] === undefined)
    {
        throw "seller_email_required";
    }
    if(data['subject'] === undefined)
    {
        throw "subject_required";
    }
    if(data['total_fee'] === undefined)
    {
        throw "total_fee_required";
    }
    $.pay_platform.post_cors('pay', data, callback)
};

$.pay_platform.refund = function(data, callback)
{
    if(data['pay_channel'] === undefined)
    {
        throw "pay_channel_required";
    }
    if(data['out_trade_no'] === undefined)
    {
        throw "out_trade_no_required";
    }
    if(data['refund_desc'] === undefined)
    {
        throw "refund_desc_required";
    }
    if(data['refund_fee'] === undefined)
    {
        throw "refund_fee_required";
    }
    $.pay_platform.post_cors('refund', data, callback)
};

$.pay_platform.query = function(data, callback)
{
    if(data['q'] === undefined)
    {
        throw "query_type_required";
    }
    $.pay_platform.post_cors('query', data, callback)
};




if($.pay_platform.DEBUG)
{
    $(function() {
        $('#submit_pay').on('click', function(){
            var data = {
                out_trade_no:$('#out_trade_no').val(),
                total_fee:$('#total_fee').val(),
                pay_channel:'alipay',
                subject:'测试付款',
                buyer_email:'a@a.com',
                seller_email:'b@b.com'
            };
            $.pay_platform.pay(data, function(data1){
                console.log(data1);
            });
        });
        $('#submit_refund').on('click', function(){
            var data = {
                out_trade_no:$('#refund_out_trade_no').val(),
                refund_fee:$('#refund_fee').val(),
                pay_channel:'alipay',
                refund_desc:'我要退款'
            };
            $.pay_platform.refund(data, function(data1){
                console.log(data1);
            });
        });
        $('#submit_query').on('click', function(){
            var data = {
                bank_code:$('#bank_code').val(),
                q:'bank_info'
            };
            $.pay_platform.query(data, function(data1){
                console.log(data1);
                $('#return_json').html(JSON.stringify(data1));
            });
        });
    
    });
}

