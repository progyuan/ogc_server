/**
 * Created by satan on 2014/8/8.
 */
;(function ($) {
    //jQuery.getScript("javascripts/highcharts.js", function(data, status, jqxhr) {
        //jQuery('body').append('<script src="javascripts/highcharts.js"></script>')
        Highcharts.setOptions({
            lang: {
                months: ['一月', '二月', '三月', '四月', '五月', '六月',  '七月', '八月', '九月', '十月', '十一月', '十二月'],
                shortMonths:['一', '二', '三', '四', '五', '六',  '七', '八', '九', '十', '十一', '十二'],
                weekdays: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
                noDate:'没有数据',
                loading:'加载中...'
            }
        });


        var container;
        jQuery.fn.extend({
            drawChart:function(imei,view,beginTime,endTime,minSpeed,maxSpeed){
                container=this;
                var url="/proxy/api/statistics/linechart/"+imei+"/"+view+"/"+beginTime+"/"+endTime+"/"+minSpeed+"/"+maxSpeed ;//+"?token="+token;
                //console.log(url);
                $.ajax({
                    type: "GET",
                    url: url,
                    success: function(result){
                        //console.log(result);
                        if(result.success){
                            //console.log(view);
                            switch(view){
                                case "Y":
                                    draw_year(result.series)
                                    break
                                case "M":
                                    draw_month(result.series)
                                    break
                                case "D":
                                    draw_day(result.series)
                                    break
                            }
                        }
                    },
                    error:function(obj,err){
                        console.log(err);
                    }
                });

            }
        });

        function draw_year(data){//年统计
            //console.log(data);
            container.empty();
            container.highcharts({
                chart: {
                    type: 'spline',
                    backgroundColor:""
                },
                title: {
                    text: '年度活动情况'
                },
                xAxis: {
                    type:'linear',
                    minTickInterval: 1
                },
                yAxis: {

                },
                series: [{
                    name: '鸟类活动',
                    data: data
                }]
            });
        };
        function draw_month(data){
            container.empty();
            var x=new Array(),y=new Array();
            for(i in data){
                var e=data[i];
                x.push(e.x);
                y.push(e.y);
            }
            container.highcharts({
                chart: {
                    type: 'spline',
                    //zoomType:'x',
                    backgroundColor:""
                },
                title: {
                    text: '月度活动情况'
                },
                xAxis: {
                    labels:{
                        //rotation:-90,
                        formatter: function () {
                           var value=this.value;
                           var year=value.substr(0,4);
                           var month=value.substr(4,2);
                           if(month=='01'){
                               return year;
                           }
                           else{
                               return month;
                           }
                        }
                    },
                    categories:x,
                    title: {
                        enabled: true,
                        text: '年月'
                    }
                },
                yAxis: {
                    title: {
                        enabled: true,
                        text: '活动次数'
                    }
                },
                series: [{
                    name: '鸟类活动',
                    data: y
                }]
            });
        }
    function draw_day(data){
        container.empty();
        var x=new Array(),y=new Array();
        for(i in data){
            var e=data[i];
            x.push([Date.UTC(e.x.toString().substr(0,4),parseInt(e.x.toString().substr(4,2))-1,e.x.toString().substr(6,2)), e.y]);
            //console.log(e.x.toString().substr(0,4));
            //console.log(e.x.toString().substr(4,2));
            //console.log(e.x.toString().substr(6,2));
            //y.push(e.y);
        }
        container.highcharts({
            chart: {
                type: 'column',
                //zoomType:'x',
                backgroundColor:""
            },
            title: {
                text: '日活动情况'
            },
            xAxis: {
                labels:{
                    //rotation:-90,

                },
                type:'datetime',
                //categories:x,
                title: {
                    enabled: true,
                    text: '日期'
                }
            },
            yAxis: {
                title: {
                    enabled: true,
                    text: '活动次数'
                }
            },
            series: [{
                name: '鸟类活动',
                data:x
            }]
        });
    }
    //});

})(jQuery);