var register_flag = false,
	reg_user_isEmpty = true,
	reg_pwd_isEmpty = true,
	reg_email_isEmpty = true,
	reg_confirm_isEmpty = true;
	
var login_flag = false,
	login_user_isEmpty = true,
	login_pwd_isEmpty = true;
window.onload=function () {
    var inputArray = document.getElementsByClassName("input");
    var login_user = inputArray[0],
        login_pass = inputArray[1],
        reg_user = inputArray[2],
        reg_pass = inputArray[3],
        confirm_pass = inputArray[4],
        emailInfo = inputArray[5];
    var errmsg = document.getElementsByClassName("right");
    var msg1 = errmsg[0],
        msg2 = errmsg[1],
        msg3 = errmsg[2],
        msg4 = errmsg[3],
        msg5 = errmsg[4],
        msg6 = errmsg[5];
	
	check();
    //登录用户名
    login_user.onblur = function () {
      if (this.value == "")
      {
          msg1.innerHTML = "<b>用户名不能为空</b>";
          login_user_isEmpty = true;
		  check();
      }
      else{
        msg1.innerHTML = "";
        login_user_isEmpty = false;
		check();

      }

    };
    //登入密码
    login_pass.onblur = function () {
      if (this.value == ""){
           msg2.innerHTML = "<b>密码不能为空</b>";
           login_pwd_isEmpty = true;
		   check();
      }
      else{
           msg2.innerHTML = "";
           login_pwd_isEmpty = false;
		   check();
      }
    };
    //注册用户名
    reg_user.onblur = function () {
      if (this.value == "")
      {
          msg3.innerHTML = "<b>用户名不能为空</b>";
          reg_user_isEmpty = true;
		  check();
      }
      else{
          msg3.innerHTML = "";
          reg_user_isEmpty = false;
		  check();
      }

    };
    //注册密码
    reg_pass.onblur = function () {
      if (this.value == ""){
          msg4.innerHTML = "<b>密码不能为空</b>";
          reg_pwd_isEmpty = true;
		  check();
      }
      else if (this.value.length < 6)
      {
          msg4.innerHTML = "<b>密码不能少于6位数</b>";
          reg_pwd_isEmpty = true;
		  check();
      }
      else{
          msg4.innerHTML = "";
          reg_pwd_isEmpty = false;
		  check();
      }
    };
    //确认密码
    confirm_pass.onblur = function () {
      if (this.value != reg_pass.value){
          msg5.innerHTML = "<b>前后密码不一致</b>";
          reg_confirm_isEmpty = true;
		  check();
      }
      else if (this.value == ""){
           msg5.innerHTML = "<b>密码不能为空</b>";
           reg_confirm_isEmpty = true;
		   check();
      }
      else{
           msg5.innerHTML = "";
           reg_confirm_isEmpty = false;
		   check();
      }

    };
    //邮箱检验
    emailInfo.onblur = function () {
      var emailReg=/^[A-Za-z\d]+([-_\.][A-Za-z\d]+)*@([A-Za-z\d]+[-\.])+[A-Za-z\d]{2,5}$/;
      if (this.value == ""){
          msg6.innerHTML = "<b>邮箱不能为空</b>";
          reg_email_isEmpty = true;
      }
      else if (!emailReg.test(this.value)){
          msg6.innerHTML = "<b>邮箱格式不正确</b>";
          reg_email_isEmpty = true;
      }
      else{
          msg6.innerHTML = "";
          reg_email_isEmpty = false;
      }

    };
	gundong();
	var gundong_div = document.getElementsByClassName("gundong")[0];
	gundong_div.onmouseover = function(){
		window.clearInterval(timer);
	};
	gundong_div.onmouseleave = function(){
		gundong();
	};
	window.onmousewheel = function(e){
		ee = e || window.event;
		var btn = document.getElementsByClassName("layui-carousel-arrow");
		var btn_sub = btn[0],
			btn_add  = btn[1];
		(ee.wheelDelta < 0)?btn_add.click():btn_sub.click();
	}
	
	
};


layui.use('carousel', function(){
	var carousel = layui.carousel;
	
	carousel.render({
		elem:'#login_main',
		full:true,
		anim:'updown',
		autoplay:false,
		arrow:'hover'		
	})
	
})
function check()
{
	
	if(login_pwd_isEmpty||login_user_isEmpty)
	{
		login_flag = false;
	}else{
		login_flag = true;
	}
	if(reg_confirm_isEmpty||reg_email_isEmpty||reg_pwd_isEmpty||reg_user_isEmpty)
	{
		register_flag = false;
	}else{
		register_flag = true;
	}
	var btn = document.getElementsByClassName("button");
	var btn1 = btn[0],
        btn2 = btn[1],
		btn3 = btn[2];
	btn1.disabled = !login_flag;
	btn2.disabled = !reg_email_isEmpty;
	btn3.disabled = !register_flag;
}
var timer;
function gundong(){
	window.clearInterval();
	var gundong_div = document.getElementsByClassName("gundong")[0];
	
	timer = this.setInterval(function(){
		left = parseInt(gundong_div.style.left);
		if(Math.abs(left) > 1950) left = 0;
		gundong_div.style.left = left - 1 + "px";
	},10);	
}

