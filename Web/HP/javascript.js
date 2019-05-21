//--------------------------------------------------------------------------------------------------------//

var googleUser = {};
var startApp = function() {
	gapi.load('auth2', function(){
		auth2 = gapi.auth2.init({
  			client_id: '631346372917-b3i922ftm6vgocktgqeijh9jbvjqfd8v.apps.googleusercontent.com',
  			cookiepolicy: 'single_host_origin'
		});
	attachSignin(document.getElementById('login_google'));
	});
};

function attachSignin(element) {
	console.log(element.id);
	auth2.attachClickHandler(element, {},
  	function(googleUser) {
		var name = googleUser.getBasicProfile().getName();
		setLocalStorage(name, "google");
		document.getElementById("userName").innerText = localStorage.getItem("UserName");
		document.getElementById('loginButton').value = "登 出";
		window.location.assign("http://isla.shu.edu.tw:8066/gt2017/MFDR/aboutPage.html");
	}, function(error) { 
		//alert(JSON.stringify(error, undefined, 2));
	});
}

function signOut() {
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(function () {});
}/*-
function onLoad() {
	gapi.load('auth2', function() {
		gapi.auth2.init();
	});
}*/

//--------------------------------------------------------------------------------------------------------//

window.fbAsyncInit = function() {
	FB.init({
		appId      : '116532302365831',
		cookie     : true,
		xfbml      : true,
		version    : 'v2.10'
	});
	
	FB.AppEvents.logPageView();  
	
	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});
};

(function(d, s, id) {
	var js, fjs = d.getElementsByTagName(s)[0];
	if (d.getElementById(id)) return;
	js = d.createElement(s); js.id = id;
	js.src = "//connect.facebook.net/zh_TW/sdk.js#xfbml=1&version=v2.10&appId=116532302365831";
	fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function statusChangeCallback(response) {
	if(response.status === 'connected') {
		FB.api('/me', function(response) {
			var name = response.name;
			setLocalStorage(name, "facebook");
			document.getElementById("userName").innerText = localStorage.getItem("UserName");
			document.getElementById('loginButton').value = "登 出";
		});
	}
	else {
	}
}

function checkLoginState() {
	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});
}

function login() {
	FB.login(function(response) {
		if(response.status === 'connected') {
			window.location.assign("http://isla.shu.edu.tw:8066/gt2017/MFDR/aboutPage.html");
		}
	}, {scope: 'public_profile,email'});
}

//--------------------------------------------------------------------------------------------------------//

function setLocalStorage(username, loginmode) {
	localStorage.setItem("UserName", username);
	localStorage.setItem("LoginMode", loginmode);
}
function logOutChangeUserName() {
	document.getElementById('userName').value = "訪客";
	document.getElementById("loginButton").innerText = "登 入";
}

function loginORlogout() {
	var loginbtn = document.getElementById('loginButton');
	if(loginbtn.value == "登 入") {
		window.location.assign("http://isla.shu.edu.tw:8066/gt2017/MFDR/logInPage.php");
		document.getElementById("login_pleaseDiv").style.display = "none"
	}
	else if(localStorage.getItem("LoginMode") == "google"){
		//signOut();
		localStorage.clear();
		logOutChangeUserName();
		window.location.assign("http://isla.shu.edu.tw:8066/gt2017/MFDR/aboutPage.html");
	}
	else if(localStorage.getItem("LoginMode") == "facebook"){
		FB.logout(function(response) {
			localStorage.clear();
			logOutChangeUserName();
			window.location.assign("http://isla.shu.edu.tw:8066/gt2017/MFDR/aboutPage.html");
		});
	}
}

//--------------------------------------------------------------------------------------------------------//

function getUserName() {
	if(!localStorage.getItem("UserName")) {
		document.getElementById("userName").innerText = "訪客";
		document.getElementById("loginButton").value = "登 入";
		document.getElementById("login_pleaseDiv").style.display = "none";
		document.getElementById("editPage").style.display = "none";
		if(localStorage.getItem("pleaseDiv") == "display") {
			document.getElementById("login_pleaseDiv").style.display = "inline";
			localStorage.removeItem("pleaseDiv");
		}
	}
	else {
		document.getElementById("userName").innerText = localStorage.getItem("UserName");
		document.getElementById("loginButton").value = "登 出";
		document.getElementById("editPage").style.display = "inline";
	}
}

//--------------------------------------------------------------------------------------------------------//

function EditMap() {
	document.getElementById("editUDMapDiv").style.display="inline";
	document.getElementById("editIMapDiv").style.display="none";
	document.getElementById("editUDRobotDiv").style.display="none";
	document.getElementById("editIRobotDiv").style.display="none";
	document.getElementById("editMapBtn").style.background="linear-gradient(to right,#000,#CDCDCD 50%,#CDCDCD 50%,#000)";
	document.getElementById("editRobotBtn").style.background="linear-gradient(to right,#000,#525252 50%,#525252 50%,#000)";
}
function EditRobot() {
	document.getElementById("editUDRobotDiv").style.display="inline";
	document.getElementById("editUDMapDiv").style.display="none";
	document.getElementById("editIMapDiv").style.display="none";
	document.getElementById("editIRobotDiv").style.display="none";
	document.getElementById("editRobotBtn").style.background="linear-gradient(to right,#000,#CDCDCD 50%,#CDCDCD 50%,#000)";
	document.getElementById("editMapBtn").style.background="linear-gradient(to right,#000,#525252 50%,#525252 50%,#000)";
}
function ChangeWidthB(btn) {
	document.getElementById(btn).style.width="30%";
}
function ChangeWidthM(btn) {
	document.getElementById(btn).style.width="20%";
}
function ChangeWidthS(btn) {
	document.getElementById(btn).style.width="10%";
}

function InsertMap() {
	document.getElementById("editUDMapDiv").style.display="none";
	document.getElementById("editIMapDiv").style.display="inline";
}
function CheckInsertMap() {
	document.getElementById("editIMapDiv").style.display="none";
	document.getElementById("editUDMapDiv").style.display="inline";
	RefreshPage();
}
function InsertRobot() {
	document.getElementById("editIRobotDiv").style.display="inline";
	document.getElementById("editRobotInsert").style.display="none";
}
function CheckInsertRobot() {
	document.getElementById("editIRobotDiv").style.display="none";
	document.getElementById("editRobotInsert").style.display="inline";
	RefreshPage();
}
function RefreshPage() {
	window.location.reload();
}

//--------------------------------------------------------------------------------------------------------//
function checkAccount() {
	var account =  document.getElementById("login_account");
	var password =  document.getElementById("logIn_password");
	//if(account.value == "" || password.value == "")
}

var x=0;
function checkPassword() {
	var pwd = document.getElementById("pwd").value;
	var checkpwd = document.getElementById("checkPwd").value;
	var hideCheck = document.getElementById("register_hideCheck");
	var check = document.getElementById("register_check");
	if(checkpwd == pwd) {
		hideCheck.style.marginLeft = x + "px";
		if(x <= 50) {
			check.src = "img/check.png";
			x++;
			hideCheck.style.marginLeft = x + "px";
			setTimeout(checkPassword, 10);
		}
	}
	else {
		x = 0;
		check.src = "img/nocheck.png";
		hideCheck.style.marginLeft = 50 + "px";
	}
}