$(document).ready(function () {

        var wait = 60;
        var Timestamp;
        function time(o) {
            if (wait == 0) {
                o.value = "获取验证码";
                o.removeAttribute("disabled");
                wait = 60;
                return;
            }
            if (wait == 60) {
                o.setAttribute("disabled", true);
                o.value = "获取验证码";
                htmlobj = $.ajax({ type: "POST",
                    url: "BankCardAction",
                    datatype: "xml",
                    data: { acc_no: $.trim($("#acc_no").val()),
                            type: "authApplyUrl",
                            id_card: $.trim($("#id_card").val()),
                            id_holder: $.trim($("#id_holder").val()),
                            mobile: $.trim($("#mobile").val()),
                            card_type: $.trim($("#card_type").val()),
                            acc_no: $.trim($("#acc_no").val()),
                            card_type: $.trim($("#card_type").val())
                            },
                    success: function (data) {
                    	var parsedJson = jQuery.parseJSON(data); 
                        if (parsedJson.success) {
                        	$("#trade_no").val(parsedJson.data.trade_no);
                            alert("短信发送成功！交易流水号："+parsedJson.data.trade_no);
                        } else {
                            alert("短信发送失败!错误码："+ parsedJson.errorCode +"错误信息:【 "+parsedJson.errorMsg+" 】");
                        }
                    },
                    complete: function(XMLHttpRequest, textStatus){
                        alert("请求短信成功！" + textStatus);
                    }, 
                    error: function () {
                        alert("请求数据加密异常！");
                    } 
                });
                wait = 59;
                setTimeout(function () { time(o); }, 1000);
            } else {
                o.value = "重新发送(" + wait + ")";
                wait--;
                setTimeout(function () { time(o); }, 1000);
            }
        }
        $("#btn").click(function () { time(this); });
        $("#R01").submit(function (e) {
            if ($.trim($("#sms_code").val()) == "") {
                alert("请输入验证码！");
                return false;
            }
        });

    });
