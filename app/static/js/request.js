function request(url, rurl, fields, msg) {
    $("#btn-sub").click(function () {
        var data = $("#form-data").serialize();
        $.ajax({
            url: url,
            data: data,
            dataType: "json",
            type: "POST",
            success: function (res) {
                if (res.code == 1) {
                    alert(msg);
                    location.href = rurl;
                } else {
                    for (var k in fields) {
                        if (typeof res[fields[k]] == "undefined") {
                            $("#error_" + fields[k]).empty();
                        } else {
                            $("#error_" + fields[k]).empty();
                            $("#error_" + fields[k]).append(res[fields[k]]);
                        }
                    }
                }
            }
        });
    });
}