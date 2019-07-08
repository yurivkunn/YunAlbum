//加载
layui.use(['element', 'layer'], function () {
    var $ = layui.jquery,
        element = layui.element;
    layer = layui.layer;

    //用户自己创建相册
    $("#addalbum").click(function () {
        //得到信息
        layer.prompt({
                title: '创建相册-输入标签',
                formType: 0
            },
            function (val, index) {

                layer.close(index);
                //信息传给服务器
                $.ajax({
                    type: "GET",
                    url: "addAlbum/", //此处填入url
                    data: {
                        "name": val
                    },
                    success: function (msg) {
                        if (msg.status == 'success') {
                            var $newalbum = msg['albumID'];
                            //创建相册
                            var $album = createalbum(val, msg.albumID, msg.cover);
                            //插入相册
                            $album.click(function () {
                                var arr = ["../static/img/bg1.jpg", "../static/img/111.jpg", "../static/img/222.jpg"];
                                showphoto(arr);
                                $("#all-album").lightGallery();
                            })
                            $("#all-album").append($album);

                        } else {
                            alert(msg.reason);
                        }


                    },
                    error: function (xhr) {
                        alert(xhr.status);
                    },

                });

            });
    })
    //创建相册的函数

});

function showphoto(arr) {
        $("#all-album").empty();
        $("#toolbarleft").empty();
        $("#addalbum").remove();
        createreturn();
        $.each(arr, function (index, value) {
            var $showdocument = "<li class=\"item\" data-src=\"" + value + "\">\n" +
                "<img class=\"pic\" src=\"" + value + "\" alt=\"\" />\n" +
                "</li>";

            $("#all-album").append($showdocument);
        })
    }
function createalbum(text, id, url) {
    var $album = $("<li id=\"" + id + "\" class=\"item\" >\n" +
        "<img src=\" " + url + "\" class=\"pic\">\n" +
        "<div class=\"label\">" + text +
        "</div>" +
        "</div>");
    return $album;
}

$(function () {

    //从相册界面转到相册里面的图片展示界面
    //将图片与查看事件绑定
    $(".gallery .item").click(function () {
        var arr = ["../static/img/bg1.jpg", "../static/img/111.jpg", "../static/img/222.jpg"];
        showphoto(arr);
        $("#all-album").lightGallery();
    });


    //传递相册信息，得到相册内图片并展示



})
//创建返回按钮
    function createreturn() {
        var $return = $("<button id=\"return\" type=\"button\" class=\"layui-btn\">返回</button>");
        $("#toolbarleft").append($return);
    }

    //创建上传按钮--没有用到
    function createupload() {
        var $upload = $("<button id=\"upload\" type=\"button\" class=\"layui-btn\">上传</button>");
        $("#toolbarright").append($upload);
    }
// $(function() {
// 	
// 	//从相册界面转到相册里面的图片展示界面
// 	//事件绑定
// 	$(".gallery .item").click(function() {
// 		var arr = [1, 3, 5];
// 		showphoto(arr);
// 		$("#all-album").lightGallery();
// 	})
// 	//传递相册信息，得到相册内图片并展示
// 	function showphoto(arr) {
// 		$("#addalbum").remove();
// 		$("#all-album").empty();
// 		$.each(arr, function(index, value) {
// 			var $showdocument = "<li class=\"item\" data-src=\"" + value + "\">\n" +
// 				"<img class=\"pic\" src=\"" + value + "\" alt=\"\" />\n" +
// 				"</li>";
// 
// 			$("#all-album").append($showdocument);
// 		})
// 	}
// 	
// 	
// 	
// })

$(document).ready(function () {
    $.ajax({
        url: "getAlbum/", //此处填入url
        success: function (msg) {
            //生成所有相册
            if (msg['status'] == 'success') {
                $.each(msg.albumID, function (index, value) {
                    var $currentalbumID = "albumID_" + value;
                    var $currentalbum = msg[$currentalbumID];
                    var $album = createalbum($currentalbum.albumName, value, $currentalbum.cover);
                    //插入相册
                    $album.click(function () {
                                var arr = ["../static/img/bg1.jpg", "../static/img/111.jpg", "../static/img/222.jpg"];
                                showphoto(arr);
                                $("#all-album").lightGallery();
                    })
                    $("#all-album").append($album);
                })
            } else {
                alert(msg['reason']);
            }

        },
        error: function (xhr) {
            alert(xhr.status);
        }
    });
    $("#logout").click(function () {

    })
});
//登录后以创建相册显示

