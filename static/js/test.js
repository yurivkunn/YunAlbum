layui.use(['element', 'layer'], function() {
			var $ = layui.jquery,
				element = layui.element,
				layer = layui.layer;

			//用户自己创建相册
			$("#addalbum").click(function() {
				// 得到信息
				layer.prompt({
						title: '创建相册-输入标签',
						formType: 0
					},
					function(val, index) {

						layer.close(index);
						//信息传给服务器 此处应有ajax调用
						
						//创建相册
						var $album = createAlbum(val);
						//插入相册
						$("#all-album").append($album);

					});
			});

			//创建相册--测试用的
			function createAlbum(text) {
				var $album = $("<li class=\"item\" >\n" +
					"<img src=\"img/bg2.jpg\" class=\"pic\">\n" +
					"<div class=\"label\">" + text +
					"</div>" +
					"</div>");
				return $album;
			}
			
		})//最顶部的括弧


//图片显示
$(function() {
	
	//从相册界面转到相册里面的图片展示界面
	//将图片与查看事件绑定
	$(".gallery .item").click(function() {
		
		//此处接收数据
		var arr = ["img/bg1.jpg", "img/22.jpg", "img/33.jpg"];
		showphoto(arr);
		$("#all-album").lightGallery();
	})
	//传递相册信息，得到相册内图片并展示
	function showphoto(arr) {
		$("#all-album").empty();
		$("#toolbarleft").empty();
		$("#addalbum").remove();
		createreturn();
		$.each(arr, function(index, value) {
			var $showdocument = "<li class=\"item\" data-src=\"" + value + "\">\n" +
				"<img class=\"pic\" src=\"" + value + "\" alt=\"\" />\n" +
				"</li>";

			$("#all-album").append($showdocument);
		})
	}
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
})
