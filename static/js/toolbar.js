//用户头像和昵称创建
function userInfo(msg) {
	var $info = $("<a href=\"javascript:;\">\n" +
		"<img src=\" " + msg.url + " \" class=\"layui-nav-img\">\n" +
		msg.name +
		"</a>");
	$("#navright").prepend($info);
}
//创建返回按钮
function createreturn() {
	var $return = $("<button id=\"return\" type=\"button\" class=\"layui-btn\">返回</button>");
	$("#toolbarleft").append($return);
}
//创建上传按钮--没有用到
function createupload() {
	var $upload = $("<button id=\"upload\" type=\"button\" class=\"layui-btn\">返回</button>");
	$("#toolbarright").append($upload);
}
//创建相册--接收后台数据的调用
function createAlbum(text, id, url) {
	var $album = $("<li id=\"" + id + "\" class=\"item\" >\n" +
		"<img src=\" " + url + "\" class=\"pic\">\n" +
		"<div class=\"label\">" + text +
		"</div>" +
		"</div>");
	return $album;
}

//传递相册信息，得到相册内照片的信息
$.ajax({
	type: "GET",
	url: "", //此处填入url
	data: {
		"albumID": this.id
	}, //相册ID
	success: function(msg) { //从此处返回该相册所有图片的url
		if (msg.status === "success") {
			var arr = msg.photoUrls;
			showphoto(arr);
			$("#all-album").lightGallery();
		} else {
			//填
		}

	},
	error: function(xhr) {
		alert(xhr.status);
	}
});

//登录后以创建相册显示
$.ajax({
	type: "GET",
	url: "", //此处填入url
	success: function(msg) {
		//生成所有相册
		$.each(msg.albumID, function(index, value) {
			var $currentalbumID = "albumID_" + value;
			var $currentalbum = msg[$currentalbumID];
			var $album = createAlbum($currentalbum.albumName, value, $currentalbum.cover);
			//插入相册
			$("#all-album").append($album);
		})

	},
	error: function(xhr) {
		alert(xhr.status);
	},

});

//得到头像,昵称和相册信息
$.ajax({
	type: "GET",
	url: "", //此处填入url
	success: function(msg) {
		if (msg.status === "success") {
			var $albumID = "albumID_" + msg.albumID;
			var $album = msg[$albumID];
			//创建用户所有相册()
			$.each($albumID)
			var $album = createAlbum(val, msg.albumID, newalbum.cover);
			//插入相册
			$("#all-album").append($album);
		} else {
			//tian
		}
	},
	error: function(xhr) {
		alert(xhr.status);
	}
});
