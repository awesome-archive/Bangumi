$(document).ready(function () {
    var conn = null;
    var name = $("#input_name").val();

    function getQueryString(name) {
        var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
        var r = window.location.search.substr(1).match(reg);
        if (r != null) {
            return unescape(r[2]);
        }
        return null;
    }

    function append_msg(name, data) {
        var html = "";
        if (data.code == 2) {
            if (data.vsb == getQueryString("vsb")) {
                html += "<div class=\"row\">\n" +
                    "<div class=\"col-md-12\">\n" +
                    "<div class=\"media\">\n" +
                    "<div class=\"media-body\">\n" +
                    "<h6 class=\"user-nickname text-right\">" + data.name + "[" + data.datenow + "]</h6>\n" +
                    "<div style=\"padding: 0rem\" class=\"alert alert-success\" role=\"alert\">\n" +
                    "" + data.content + "\n" +
                    "</div>\n" +
                    "</div>\n" +
                    "<img class=\"ml-3 rounded-circle\" src=\"" + data.face + "\" style='width:50px;height: 50px;'>\n" +
                    "</div>\n" +
                    "</div>\n" +
                    "</div>";

                $(".chat-list").append(html);
                SyntaxHighlighter.highlight();

                $(".chat-list").scrollTop(
                    $(".chat-list").scrollTop() + 99999999
                );
            }
        } else {
            if (data.vsb == getQueryString("vsb")) {
                $(".chat-list").append("<p class='text-center text-success'>欢迎" + data.name + "进入房间！<img src='/static/images/rorse.gif'><img src='/static/images/rorse.gif'><img src='/static/images/rorse.gif'></p>");
            }
        }
    }

    function update_ui(event) {
        var recv_msg = event.data;
        append_msg(name, JSON.parse(recv_msg))
    }

    function user_enter_tip() {
        var enter_data = {
            code: 1,
            name: name,
            vid: getQueryString("vid"),
            vsb: getQueryString("vsb"),
        };
        conn.send(JSON.stringify(enter_data))
    }

    function connect() {
        disconnect();
        var transports = ["websocket"];
        conn = new SockJS('http://' + window.location.host + '/chatroom', transports);
        conn.onopen = function () {
            $.ajax({
                data: {"vid": $("#vid").val(), "vsb": $("#vsb").val()},
                url: "/msg/",
                type: "POST",
                dataType: "json",
                success: function (res) {
                    var msg_arr = res.data;
                    for (var k in msg_arr) {
                        append_msg(name, msg_arr[k])
                    }
                    user_enter_tip();
                }
            });
        };
        conn.onmessage = function (event) {
            update_ui(event);
        };
        conn.onclose = function () {
            conn = null;
        };
    }

    function disconnect() {
        if (conn != null) {
            conn.close();
            conn = null;
        }
    }

    if (conn == null) {
        connect()
    } else {
        disconnect();
    }

    function getFormData() {
        var data = $("#form-data").serializeArray();
        var result = {};
        $.map(data, function (v, i) {
            result[v['name']] = v['value'];
        });
        return result;
    }

    $("#send_msg").click(function () {
        var msg = getFormData();
        if (msg.content) {
            if (msg.content.length > 500) {
                alert("留言长度过长！");
            } else {
                msg.code = 2;
                ue.setContent('');
                conn.send(JSON.stringify(msg));
            }
        } else {
            alert("发送消息不能为空！");
        }
    });
});