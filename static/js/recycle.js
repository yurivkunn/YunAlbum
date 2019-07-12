layui.use(['element'], function() {
	var $ = layui.jquery,
		element = layui.element;
	$.ajax({
        type: "GET",
        url: "../getInfo_Album/", //此处填入url
        success: function (msg) {
            userInfo(msg.pict.path, msg.userName);

        },
        error: function (xhr) {
            alert(xhr.status);
        }
    });

	$.ajax({
		type: "GET",
		url: "../showRecycle/", //此处填入url
		success: function(msg) { //从此处返回该相册所有图片的url
			if (msg.status === "success") {
				//此处添加搜索为空的事件：$("#all-album").html("<img src=\"img/none.png\">")
				showphoto(msg.pict, msg.pictID);
				$("#all-album").lightGallery();//查看事件
			} else if(msg.status === "no-picture"){
				showphoto([], []);
                $("#all-album").html("<img src=\"../../static/img/none.png\">");
                $("#back").html("< 回收站");
			}
		},
		error: function(xhr) {
			alert(xhr.status);
		}
	});
	$("#search").click(function () {
            if ($("#content").val().trim().length > 0) {
                window.location.href = 'search/' + $("#content").val();
            }else{
                alert("搜索内容不能为空！");
            }
        });
});
//图片按钮的事件
$("#")
function recent() {
        $.ajax({
            type: "GET",
            url: "getAllPict/", //此处填入url
            data: {id: 0}, //判断是否智能分类
            success: function (msg) { //从此处返回所有图片的url
                if (msg.status === "success") {
                    $("#back").html("< 最近上传");
                    showphoto(msg.pict, msg.pictID);
                    $("#all-album").lightGallery();//查看事件
                } else {
                    alert("尚未上传图片");
                }
            },
            error: function (xhr) {
                alert(xhr.status);
            }
        });
    }

//图片展示--接收后台数据调用
function showphoto(urlarr, idarr) {
	$("#all-album").remove();
	createUL();
	$.each(urlarr, function(index, value) {
		var $currentphoto = $("<li class=\"item\" data-src=\"" + value + "\">\n" +
								"<img id=\""+ idarr[index] + "\" class=\"pic\" src=\"" + value + "\" alt=\"\" />\n" +
								"<img class=\"delete\" src=\"../../static/img/delete.png\" alt=\"\">" +
							  "</li>");
		$("#all-album").append($currentphoto);
	});
	$(".item .delete").click(function() {
		deletephoto(this.parentElement.children[0].id);
		this.parentElement.remove();
		event.cancelBubble = true;
	});
}
//删除照片时把数据传给数据库
function deletephoto(id) {
	$.ajax({
		type: "GET",
		url: "../deleteComplete/", //此处填入url
		data: {
			"id": id
		},
		success: function(msg) {
			//删除成功的提示
			if(msg.status === "success"){
				alert("删除成功！");
			}
		},
		error: function(xhr) {
			alert(xhr.status);
		}
	})
}
//创建ul
function createUL() {
	var $ul = $("<ul id=\"all-album\" class=\"gallery\">" +
				"</ul>");
	$("#main").append($ul);
}

function userInfo(url, name) {
    var $info = $("<a href=\"javascript:;\">\n" +
        "<img src=\" " + url + " \" class=\"layui-nav-img\">\n" +
        name +
        "</a>");
    $("#navright").prepend($info);
}