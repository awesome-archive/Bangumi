function upload(k, w, h, url) {
    $("#upload_" + k).click(function () {
        var img = $("#file_" + k)[0].files[0];
        var filepath = img.name;
        var point = filepath.lastIndexOf(".");
        var type = filepath.substr(point);
        if (type != ".jpg" && type != ".gif" && type != ".jpeg" && type != ".png") {
            alert("您上传图片的类型不符合(.jpg|.jpeg|.gif|.png)！");
            return;
        }

        if (img.size >= (2 * 1024 * 1024)) {
            alert("请上传小于2M的图片！");
            return;
        }

        if (img) {
            var formData = new FormData();
            formData.append("img", img);
            $.ajax({
                url: url,
                type: "POST",
                dataType: "json",
                cache: false,
                contentType: false,
                processData: false,
                data: formData,
                success: function (res) {
                    if (res.code == 1) {
                        var img = res.image;
                        var content = "<img src='/static/uploads/" + img + "' style='width: " + w + "px;height: " + h + "px;'>";
                        $("#image_" + k).empty();
                        $("#image_" + k).append(content);
                        $("#input_" + k).attr("value", img);
                    } else if (res.code == 2) {
                        alert("您上传图片的类型不符合(.jpg|.jpeg|.gif|.png)！");
                    } else if (res.code == 3) {
                        alert("请上传小于2M的图片！");
                    }
                }
            });
        }
    });
}