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

	//搜索功能
	$.ajax({
		type: "GET",
		url: "", //此处填入url
		// data: {
		// 	"content": text
		// },
		success: function(msg) {
			if (msg.status === "success") {
				$("#back").html("< 搜索结果");
				//此处添加回收站为空的事件：$("#all-album").html("<img src=\"img/none.png\">")
				showphoto(msg.urlarr, msg.idarr);
				$("#all-album").lightGallery();//查看事件
			} else {
				alert("凉凉");
			}
		},
		error: function(xhr) {
			alert(xhr.status);
		}
	})
});
function userInfo(url, name) {
    var $info = $("<a href=\"javascript:;\">\n" +
        "<img src=\" " + url + " \" class=\"layui-nav-img\">\n" +
        name +
        "</a>");
    $("#navright").prepend($info);
}

//图片展示--接收后台数据调用
function showphoto(urlarr, idarr) {
	$("#all-album").remove();
	createUL();
	$.each(urlarr, function(index, value) {
		var $currentphoto = $("<li class=\"item\" data-src=\"" + value + "\">\n" +
								"<img id=\""+ idarr[index] + "\" class=\"pic\" src=\"" + value + "\" alt=\"\" />\n" +
								"<img class=\"delete\" src=\"img/delete.png\" alt=\"\">" +
							  "</li>");
		$("#all-album").append($currentphoto);
	});
	$(".item .delete").click(function() {
		deletephoto();
		this.parentElement.remove();
		event.cancelBubble = true;
	});
}
//删除照片时把数据传给数据库
function deletephoto() {
	$.ajax({
		type: "GET",
		url: "", //此处填入url
		data: {
			"id": this.parentElement.children[0].id
		},
		success: function(msg) {
			//删除成功的提示
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