$.pay_platform = {};
$.pay_platform.PAY_HOST = 'yncaiyun1.com';
$.pay_platform.PAY_PROTOCOL = 'http';
$.pay_platform.PAY_PORT = '8089';
$.pay_platform.DEBUG = true;
$.pay_platform.plot = null;
$.pay_platform.queue = [];
$.pay_platform.PLOT_RANGE = 20;


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

	function init_websocket()
	{
		var wsurl =  "ws://" + $.pay_platform.PAY_HOST + ":" + $.pay_platform.PAY_PORT + "/websocket";
		if($.pay_platform.websocket === undefined)
		{
			$.pay_platform.websocket = new WebSocket(wsurl);
		}
		if($.pay_platform.websocket)
		{
			$.pay_platform.websocket.onopen = function() 
			{
				//$.pay_platform.websocket.send(JSON.stringify({}));
				$.pay_platform.websocket.send(JSON.stringify({op:'queue_size'}));
			};
			$.pay_platform.websocket.onclose = function(e) 
			{
				console.log("websocket close");
			};
			$.pay_platform.websocket.onerror = function(e) 
			{
				console.log("websocket error:" + e);
				$.pay_platform.websocket.close();
			};
			$.pay_platform.websocket.onmessage = function(e) 
			{
				if(e.data.length>0)
				{
					var obj = JSON.parse(e.data);
					if(obj instanceof Array)
					{
					}
					if(obj instanceof Object)
					{
						if($.pay_platform.queue.length >= $.pay_platform.PLOT_RANGE)
						{
							$.pay_platform.queue.shift();
						}
						var d = [(new Date()).getTime(), obj.queue_size]
						$.pay_platform.queue.push(d);
						$('#qsize').html(obj.queue_size);
						//console.log($.pay_platform.queue);
						$.pay_platform.plot.setData([{label:'支付队列交易量', data:$.pay_platform.queue}]);
						$.pay_platform.plot.setupGrid();
						$.pay_platform.plot.draw();
						
					}
					
				}
				$.pay_platform.websocket.send(JSON.stringify({op:'queue_size'}));
			};
		}		
	}


    $(function() {
	
		var initdata = [[(new Date()).getTime(), 0]];
		$.pay_platform.plot = $.plot("#placeholder", [ initdata ], {
			series: {
				shadowSize: 0,
				lines: {
					show: true,
				},
				points: {
					show: true,
					radius: 4,
					fill: true,
					symbol: "circle"
				}
				//bars: {
					//show: true
				//}
			},
			yaxis: {
				min: 0,
				max: 50
			},
			xaxis: {
				mode: "time",
				minTickSize: [1, "second"]
			},legend: {
				show: true
			}
		});	
	
	
		init_websocket();
		
		
		
		
		
		
		
		
		
        $('#out_trade_no').val('1');
        $('#total_fee').val('100.0'),
    
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
                //console.log(data1);
            });
            $('#out_trade_no').val(parseInt($('#out_trade_no').val()) + 1);
            $('#total_fee').val(parseFloat($('#total_fee').val()) + 10);
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

