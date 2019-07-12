var $flag = 0;
var $albumid = 0;
layui.use(['element', 'layer', 'upload'], function () {
    var $ = layui.jquery,
        element = layui.element,
        layer = layui.layer,
        upload = layui.upload;


    //多图片上传
    $("#upload").click(function () {
        var a = document.createEvent("MouseEvents");//FF的处理   
        a.initEvent("click", true, true);
        document.getElementById("image-upload").dispatchEvent(a);
    });
    $("#image-upload").on('change', function () {
        var fileObj = document.getElementById("image-upload"); // js 获取文件对象
        if (typeof (fileObj.files[0]) == "undefined" || fileObj.size <= 0) {
            alert("请选择图片");
            return;
        }
        var formFile = new FormData();
        for (var i = 0; i < fileObj.files.length; i++) {
            formFile.append("id", $albumid);
            formFile.append("file", fileObj.files[i]); //加入文件对象
        }


        var data = formFile;
        $.ajax({
            url: "upload/",
            data: data,
            type: "Post",
            dataType: "json",
            cache: false,//上传文件无需缓存
            processData: false,//用于对data参数进行序列化处理 这里必须false
            contentType: false, //必须
            success: function (res) {
                if ($albumid == 0) {
                    $.ajax({
                        type: "GET",
                        url: "getInfo_Album/", //此处填入url
                        success: function (msg) {
                            if (msg.status === "success") {
                                $('#all-album').empty();
                                //相册显示
                                $.each(msg.albumID, function (index, value) {
                                    var $currentalbumID = "albumID_" + value;
                                    var $currentalbum = msg[$currentalbumID];
                                    var $album = createAlbum($currentalbum.albumName, value, $currentalbum.cover.path);
                                });
                                alert('上传成功！');
                            } else {
                                alert(msg.reason);
                            }
                        },
                        error: function (xhr) {
                            alert(xhr.status);
                        }
                    });
                } else {
                    $.ajax({
                        type: "GET",
                        url: "getPictByAlbum/", //此处填入url
                        data: {
                            "albumID": $albumid
                        }, //相册ID
                        success: function (msg) { //从此处返回该相册所有图片的url
                            if (msg.status === "success") {
                                var arr = [];
                                var pictName = [];
                                for (var i = 0; i < msg.pictID.length; i++) {
                                    arr[i] = msg[msg.pictID[i]].path;
                                    pictName[i] = msg[msg.pictID[i]].pict_name;
                                }
                                showphoto(arr, pictName);
                                $("#all-album").lightGallery();//查看事件

                                $("#back").html("<" + self.children[1].innerHTML);

                            } else if (msg.status === "no-picture") {
                                showphoto([], []);
                                $("#all-album").html("<img src=\"../static/img/none.png\">")
                                $("#back").html("<" + self.children[1].innerHTML);
                            } else {
                                alert("凉凉");
                            }
                        },
                        error: function (xhr) {
                            alert(xhr.status);
                        }
                    });
                }

            },
        })
    });
    // upload.render({
    //     elem: '#upload',
    //     url: 'upload/',//填入url
    //     multiple: true,
    //     data: {id: $albumid},
    //     accept: 'images',
    //     acceptMime: 'images/',
    //     done: function (res) {
    //         //上传完毕后图片显示
    //         $.ajax({
    //             type: "GET",
    //             url: "getInfo_Album/", //此处填入url
    //             success: function (msg) {
    //                 if (msg.status === "success") {
    //                     $('#all-album').empty();
    //                     //相册显示
    //                     $.each(msg.albumID, function (index, value) {
    //                         var $currentalbumID = "albumID_" + value;
    //                         var $currentalbum = msg[$currentalbumID];
    //                         var $album = createAlbum($currentalbum.albumName, value, $currentalbum.cover.path);
    //                     });
    //                         alert('上传成功！');
    //                     }else {
    //                     alert(msg.reason);
    //                 }
    //             },
    //             error: function (xhr) {
    //                 alert(xhr.status);
    //             }
    //         });
    //     }
    // });
    //隐藏返回按钮
    $("#back").hide();
    //返回按钮的事件绑定
    $("#back").click(back);
    //创建相册的事件绑定
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

                                $.ajax({
                                    type: "GET",
                                    url: "getInfo_Album/", //此处填入url
                                    success: function (msg) {
                                        if (msg.status === "success") {
                                            $('#all-album').empty();
                                            //相册显示

                                            $.each(msg.albumID, function (index, value) {
                                                var $currentalbumID = "albumID_" + value;
                                                var $currentalbum = msg[$currentalbumID];
                                                var $album = createAlbum($currentalbum.albumName, value, $currentalbum.cover.path);
                                            });
                                            $(".item .delete").click(function () {
                                                deletealbum(this.parentElement.id);
                                                this.parentElement.remove();
                                                event.cancelBubble = true;
                                            });
                                            $(".item .edit").click(function () {
                                                var parent = this.parentElement;
                                                edit(self);
                                                event.cancelBubble = true;
                                            });
                                            alert('创建成功');
                                        } else {
                                            alert(msg.reason);
                                        }
                                    },
                                    error: function (xhr) {
                                        alert(xhr.status);
                                    }
                                })}


                        else {
                            alert(msg.reason);
                        }


                    },
                    error: function (xhr) {
                        alert(xhr.status);
                    },

                });

            });
    });
    //相册点击的事件绑定
    $(".gallery .item").click(albumevent);
    //最近图片的事件绑定
    $("#recent").click(recent);
    //登录后的显示头像，昵称和相册
    $.ajax({
        type: "GET",
        url: "getInfo_Album/", //此处填入url
        success: function (msg) {
            userInfo(msg.pict.path, msg.userName);
            //msg返回风格设置
            $(".layui-header").css("background-color", msg.settings[0]);
            $(".layui-side").css("background-color", msg.settings[1]);
            if (msg.status === "success") {
                //相册显示
                $.each(msg.albumID, function (index, value) {
                    var $currentalbumID = "albumID_" + value;
                    var $currentalbum = msg[$currentalbumID];
                    var $album = createAlbum($currentalbum.albumName, value, $currentalbum.cover.path);

                });
                $(".item .delete").click(function () {
                    deletealbum(this.parentElement.id);
                    this.parentElement.remove();
                    event.cancelBubble = true;
                });
                $(".item .edit").click(function () {
                    var parent = this.parentElement;
                    edit(parent);
                    event.cancelBubble = true;
                });
                //msg返回头像和昵称

            } else {
                alert(msg.reason);
            }
        },
        error: function (xhr) {
            alert(xhr.status);
        }
    });
});
$(document).ready(function () {
    //搜索事件绑定
    $("#search").click(function () {
            if ($("#content").val().trim().length > 0) {
                window.location.href = 'search/' + $("#content").val();
            }else{
                alert("搜索内容不能为空！");
            }
        });
});

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

//相册的点击事件
    function albumevent() {
        var self = this;
        $albumid = this.id;
        $.ajax({
            type: "GET",
            url: "getPictByAlbum/", //此处填入url
            data: {
                "albumID": this.id
            }, //相册ID
            success: function (msg) { //从此处返回该相册所有图片的url
                if (msg.status === "success") {
                    var arr = [];
                    var pictName = [];
                    for (var i = 0; i < msg.pictID.length; i++) {
                        arr[i] = msg[msg.pictID[i]].path;
                        pictName[i] = msg.pictID[i];
                    }
                    showphoto(arr, pictName);
                    $("#all-album").lightGallery();//查看事件

                    $("#back").html("<" + self.children[3].innerHTML);

                } else if (msg.status === "no-picture") {
                    showphoto([], []);
                    $("#all-album").html("<img src=\"../static/img/none.png\">");
                    $("#back").html("<" + self.children[3].innerHTML);
                } else {
                    alert("凉凉");
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
        $("#back").show();
        $("#addalbum").hide();
        createUL();
        $.each(urlarr, function (index, value) {
            var $currentphoto = $("<li class=\"item\" data-src=\"" + value + "\">\n" +
                "<img id=\"" + idarr[index] + "\" class=\"pic\" src=\"" + value + "\" alt=\"\" />\n" +
                "<img class=\"delete\" src=\"../static/img/delete.png\" alt=\"\">" +
                "</li>");
            $("#all-album").append($currentphoto);
        });
        $(".item .delete").click(function () {
            deletephoto(this.parentElement.children[0].id);
            this.parentElement.remove();
            event.cancelBubble = true;
        });
    }

//用户头像和昵称创建
    function userInfo(url, name) {
        var $info = $("<a href=\"javascript:;\">\n" +
            "<img src=\" " + url + " \" class=\"layui-nav-img\">\n" +
            name +
            "</a>");
        $("#navright").prepend($info);
    }

//创建相册--接收后台数据的调用
    function createAlbum(text, id, url) {
        var $album = $("<li id=\"" + id + "\" class=\"item\" >\n" +
            "<img src=\" " + url + "\" class=\"pic\">\n" +
            "<img class=\"delete\" src=\"../static/img/delete.png\" alt=\"\">" +
            "<img class=\"edit\" src=\"../static/img/edit.png\" alt=\"\">" +
            "<div class=\"label\">" + text + "</div>" +
            "</div>");
        //插入相册
        $("#all-album").append($album);
        //新建相册的按钮绑定
        $album.click(albumevent);
    }

//返回按钮的事件
    function back() {
        $("#all-album").empty(); 		//移除照片
        $("#back").hide(); 				//隐藏返回
        $("#addalbum").show(); 			//显示新建相册
        $albumid = 0;
        $.ajax({
            type: "GET",
            url: "getInfo_Album/", //此处填入url
            success: function (msg) {
                if (msg.status === "success") {
                    //相册显示
                    $.each(msg.albumID, function (index, value) {
                        var $currentalbumID = "albumID_" + value;
                        var $currentalbum = msg[$currentalbumID];
                        var $album = createAlbum($currentalbum.albumName, value, $currentalbum.cover.path);
                    });
                    $(".item .delete").click(function () {
                        deletealbum(this.parentElement.id);
                        this.parentElement.remove();
                        event.cancelBubble = true;
                    });
                    $(".item .edit").click(function () {
                        var parent = this.parentElement;
                        edit(parent);
                        event.cancelBubble = true;
                    });
                } else {
                    alert(msg.reason);
                }
            },
            error: function (xhr) {
                alert(xhr.status);
            }
        });
    }

//创建ul
    function createUL() {
        var $ul = $("<ul id=\"all-album\" class=\"gallery\">" +
            "</ul>");
        $("#main").append($ul);
    }

//删除照片时把数据传给数据库
    function deletephoto(id) {
        $.ajax({
            type: "GET",
            url: "deletePhoto/", //此处填入url
            data: {
                "id": id
            },
            success: function (msg) {
                //删除成功的提示
            },
            error: function (xhr) {
                alert(xhr.status);
            }
        })
    }

//删除相册时把数据传给数据库
    function deletealbum(id) {
        $.ajax({
            type: "GET",
            url: "deleteAlbum/", //此处填入url
            data: {
                "id": id
            },
            success: function (msg) {
                if (msg.status === 'success') {
                    alert("删除成功! 相册内图片可在回收站内查看。");
                }
            },
            error: function (xhr) {
                alert(xhr.status);
            }
        })
    }

//更改标签
    function edit(element) {
        layer.prompt({ //弹窗
                title: '相册-修改标签',
                formType: 0
            },
            function (val, index) {
                layer.close(index);
                //信息传给服务器
                $.ajax({
                    type: "GET",
                    url: "editTag/", //此处填入url
                    data: {
                        "id": element.id,
                        "name": val
                    },
                    success: function (msg) {
                        if (msg.status === "success") {
                            element.children[3].innerHTML = val;
                        } else {
                            alert("系统相册无法修改");
                        }
                    },
                    error: function (xhr) {
                        alert(xhr.status);
                    }
                });
            });
    }