from flask import Flask, jsonify, request, render_template_string
import requests
import logging

app = Flask(__name__)

@app.route("/youga")
def youga():
    html = """
<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <title>Yoga Astri Yudistira</title>
  <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto'>
  <link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.css" rel="stylesheet">
<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css'>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
html {
  height: 100%;
}

body {
  overflow: hidden;
  background: black url("../img/bg.jpg") no-repeat center center fixed;
  background-size: cover;
  position: fixed;
  padding: 0px;
  margin: 0px;
  width: 100%;
  height: 100%;
  font: normal 14px/1.618em "Roboto", sans-serif;
  -webkit-font-smoothing: antialiased;
}

body:before {
  content: "";
  height: 0px;
  padding: 0px;
  border: 130em solid #313440;
  position: absolute;
  left: 50%;
  top: 100%;
  z-index: 2;
  display: block;
  -webkit-border-radius: 50%;
  border-radius: 50%;
  -webkit-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  -webkit-animation: puff 0.5s 1.8s cubic-bezier(0.55, 0.055, 0.675, 0.19) forwards, borderRadius 0.2s 2.3s linear forwards;
  animation: puff 0.5s 1.8s cubic-bezier(0.55, 0.055, 0.675, 0.19) forwards, borderRadius 0.2s 2.3s linear forwards;
}

h1,
h2 {
  font-weight: 500;
  margin: 0px 0px 5px 0px;
}

h1 {
  font-size: 24px;
}

h2 {
  font-size: 16px;
}

p {
  margin: 0px;
}

.profile-card {
  background: #FFB300;
  width: 56px;
  height: 56px;
  position: absolute;
  left: 50%;
  top: 50%;
  z-index: 2;
  overflow: hidden;
  opacity: 0;
  margin-top: 70px;
  -webkit-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  -webkit-border-radius: 50%;
  border-radius: 50%;
  -webkit-box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.16), 0px 3px 6px rgba(0, 0, 0, 0.23);
  box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.16), 0px 3px 6px rgba(0, 0, 0, 0.23);
  -webkit-animation: init 0.5s 0.2s cubic-bezier(0.55, 0.055, 0.675, 0.19) forwards, moveDown 1s 0.8s cubic-bezier(0.6, -0.28, 0.735, 0.045) forwards, moveUp 1s 1.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards, materia 0.5s 2.7s cubic-bezier(0.86, 0, 0.07, 1) forwards;
  animation: init 0.5s 0.2s cubic-bezier(0.55, 0.055, 0.675, 0.19) forwards, moveDown 1s 0.8s cubic-bezier(0.6, -0.28, 0.735, 0.045) forwards, moveUp 1s 1.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards, materia 0.5s 2.7s cubic-bezier(0.86, 0, 0.07, 1) forwards;
}

.profile-card header {
  width: 179px;
  height: 280px;
  padding: 40px 20px 30px 20px;
  display: inline-block;
  float: left;
  border-right: 2px dashed #EEEEEE;
  background: #FFFFFF;
  color: #000000;
  margin-top: 50px;
  opacity: 0;
  text-align: center;
  -webkit-animation: moveIn 1s 3.1s ease forwards;
  animation: moveIn 1s 3.1s ease forwards;
}

.profile-card header h1 {
  color: #FF5722;
}

.profile-card header a {
  display: inline-block;
  text-align: center;
  position: relative;
  margin: 25px 30px;
}

.profile-card header a:after {
  position: absolute;
  content: "";
  bottom: 3px;
  right: 3px;
  width: 20px;
  height: 20px;
  border: 4px solid #FFFFFF;
  -webkit-transform: scale(0);
  transform: scale(0);
  background: -webkit-linear-gradient(top, red 0%, red 50%, white 50%, white 100%);
  background: linear-gradient(red 0%, red 50%, white 50%, white 100%);
  -webkit-border-radius: 50%;
  border-radius: 50%;
  -webkit-box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
  -webkit-animation: scaleIn 0.3s 3.5s ease forwards;
  animation: scaleIn 0.3s 3.5s ease forwards;
}

.profile-card header a > img {
  width: 120px;
  max-width: 100%;
  -webkit-border-radius: 50%;
  border-radius: 50%;
  -webkit-transition: -webkit-box-shadow 0.3s ease;
  transition: box-shadow 0.3s ease;
  -webkit-box-shadow: 0px 0px 0px 8px rgba(0, 0, 0, 0.06);
  box-shadow: 0px 0px 0px 8px rgba(0, 0, 0, 0.06);
}

.profile-card header a:hover > img {
  -webkit-box-shadow: 0px 0px 0px 12px rgba(0, 0, 0, 0.1);
  box-shadow: 0px 0px 0px 12px rgba(0, 0, 0, 0.1);
}

.profile-card .profile-bio {
  width: 175px;
  height: 180px;
  display: inline-block;
  float: right;
  padding: 50px 20px 30px 20px;
  background: #FFFFFF;
  color: #333333;
  margin-top: 50px;
  text-align: center;
  opacity: 0;
  -webkit-animation: moveIn 1s 3.1s ease forwards;
  animation: moveIn 1s 3.1s ease forwards;
}

.profile-social-links {
  width: 218px;
  display: inline-block;
  float: right;
  margin: 0px;
  padding: 15px 20px;
  background: #FFFFFF;
  margin-top: 50px;
  text-align: center;
  opacity: 0;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  -webkit-animation: moveIn 1s 3.1s ease forwards;
  animation: moveIn 1s 3.1s ease forwards;
}

.profile-social-links li {
  list-style: none;
  margin: -5px 0px 0px 0px;
  padding: 0px;
  float: left;
  width: 25%;
  text-align: center;
}

.profile-social-links li a {
  display: inline-block;
  color: red;
  width: 24px;
  height: 24px;
  padding: 6px;
  position: relative;
  overflow: hidden!important;
  -webkit-border-radius: 50%;
  border-radius: 50%;
}

.profile-social-links li a i {
  position: relative;
  z-index: 1;
}

.profile-social-links li a img,
.profile-social-links li a svg {
  width: 24px;
}

@-webkit-keyframes init {
  0% {
    width: 0px;
    height: 0px;
  }
  100% {
    width: 56px;
    height: 56px;
    margin-top: 0px;
    opacity: 1;
  }
}

@keyframes init {
  0% {
    width: 0px;
    height: 0px;
  }
  100% {
    width: 56px;
    height: 56px;
    margin-top: 0px;
    opacity: 1;
  }
}

@-webkit-keyframes puff {
  0% {
    top: 100%;
    height: 0px;
    padding: 0px;
  }
  100% {
    top: 50%;
    height: 100%;
    padding: 0px 100%;
  }
}

@keyframes puff {
  0% {
    top: 100%;
    height: 0px;
    padding: 0px;
  }
  100% {
    top: 50%;
    height: 100%;
    padding: 0px 100%;
  }
}

@-webkit-keyframes borderRadius {
  0% {
    -webkit-border-radius: 50%;
  }
  100% {
    -webkit-border-radius: 0px;
  }
}

@keyframes borderRadius {
  0% {
    -webkit-border-radius: 50%;
  }
  100% {
    border-radius: 0px;
  }
}

@-webkit-keyframes moveDown {
  0% {
    top: 50%;
  }
  50% {
    top: 40%;
  }
  100% {
    top: 100%;
  }
}

@keyframes moveDown {
  0% {
    top: 50%;
  }
  50% {
    top: 40%;
  }
  100% {
    top: 100%;
  }
}

@-webkit-keyframes moveUp {
  0% {
    background: #FFB300;
    top: 100%;
  }
  50% {
    top: 40%;
  }
  100% {
    top: 50%;
    background: #E0E0E0;
  }
}

@keyframes moveUp {
  0% {
    background: #FFB300;
    top: 100%;
  }
  50% {
    top: 40%;
  }
  100% {
    top: 50%;
    background: #E0E0E0;
  }
}

@-webkit-keyframes materia {
  0% {
    background: #E0E0E0;
  }
  50% {
    -webkit-border-radius: 4px;
  }
  100% {
    width: 440px;
    height: 280px;
    background: #FFFFFF;
    -webkit-border-radius: 4px;
  }
}

@keyframes materia {
  0% {
    background: #E0E0E0;
  }
  50% {
    border-radius: 4px;
  }
  100% {
    width: 440px;
    height: 280px;
    background: #FFFFFF;
    border-radius: 4px;
  }
}

@-webkit-keyframes moveIn {
  0% {
    margin-top: 50px;
    opacity: 0;
  }
  100% {
    opacity: 1;
    margin-top: -20px;
  }
}

@keyframes moveIn {
  0% {
    margin-top: 50px;
    opacity: 0;
  }
  100% {
    opacity: 1;
    margin-top: -20px;
  }
}

@-webkit-keyframes scaleIn {
  0% {
    -webkit-transform: scale(0);
  }
  100% {
    -webkit-transform: scale(1);
  }
}

@keyframes scaleIn {
  0% {
    transform: scale(0);
  }
  100% {
    transform: scale(1);
  }
}

@-webkit-keyframes ripple {
  0% {
    transform: scale3d(0, 0, 0);
  }
  50%,
  100% {
    -webkit-transform: scale3d(1, 1, 1);
  }
  100% {
    opacity: 0;
  }
}

@keyframes ripple {
  0% {
    transform: scale3d(0, 0, 0);
  }
  50%,
  100% {
    transform: scale3d(1, 1, 1);
  }
  100% {
    opacity: 0;
  }
}

@media screen and (min-aspect-ratio: 4/3) {
  body {
    background-size: cover;
  }
  body:before {
    width: 0px;
  }
  @ -webkit-keyframes puff {
    0% {
      top: 100%;
      width: 0px;
      padding-bottom: 0px;
    }
    100% {
      top: 50%;
      width: 100%;
      padding-bottom: 100%;
    }
  }
  @keyframes puff {
    0% {
      top: 100%;
      width: 0px;
      padding-bottom: 0px;
    }
    100% {
      top: 50%;
      width: 100%;
      padding-bottom: 100%;
    }
  }
}

@media screen and (min-height: 480px) {
  .profile-card header {
    width: auto;
    height: auto;
    padding: 30px 20px;
    display: block;
    float: none;
    border-right: none;
  }
  .profile-card .profile-bio {
    width: auto;
    height: auto;
    padding: 15px 20px 30px 20px;
    display: block;
    float: none;
  }
  .profile-social-links {
    width: 100%;
    display: block;
    float: none;
  }
  @ -webkit-keyframes materia {
    0% {
      background: #E0E0E0;
    }
    50% {
      -webkit-border-radius: 4px;
    }
    100% {
      width: 280px;
      height: 440px;
      background: #FFFFFF;
      -webkit-border-radius: 4px;
    }
  }
  @keyframes materia {
    0% {
      background: #E0E0E0;
    }
    50% {
      border-radius: 4px;
    }
    100% {
      width: 280px;
      height: 440px;
      background: #FFFFFF;
      border-radius: 4px;
    }
  }
}
</style>
</head>
<body oncontextmenu='return false;' onkeydown='return false;' onmousedown='return false;' ondragstart='return false' onselectstart='return false' style='-moz-user-select: none; cursor: default;'>
<!-- partial:index.partial.html -->
<aside class="profile-card">
  <header>
    <!-- here’s the avatar -->
    <a target="_blank" href="/">
      <img src="https://raw.githubusercontent.com/Astri96/databse/main/database/yoga.jpg" class="hoverZoomLink">
    </a>

    <!-- the username -->
    <h1>
            Yoga Astri Yudistira
          </h1>

    <!-- and role or location -->
    <h2>
            Pemuda P.T.C
          </h2>

  </header>

  <!-- bit of a bio; who are you? -->
  <div class="profile-bio">

    <p>
      My name is Yoga Astri Yudistira, you can call me Yoga. I was born in Jakarta, Indonesia. I'm 19 years old. This is an API website and i was the one who created.
    </p>

  </div>

  <!-- some social links to show off -->
  <ul class="profile-social-links">
    <li>
      <a target="_blank" href="https://www.facebook.com/people/Yoga-Astri-Yudistira/100010847747394/">
        <i class="fab fa-facebook"></i>
      </a>
    </li>
    <li>
      <a target="_blank" href="https://instagram.com/yoga.ptc">
        <i class="fab fa-instagram"></i>
      </a>
    </li>
    <li>
      <a target="_blank" href="https://wa.me/6288225888058">
        <i class="fab fa-whatsapp"></i>
      </a>
    </li>
    <li>
      <a target="_blank" href="/status">
       
        <i class="fa fa-link"></i>
      </a>
    </li>
  </ul>
</aside>
<!-- partial -->
  
</body>
<script type='text/javascript'>
  shortcut={all_shortcuts:{},add:function(a,b,c){var d={type:"keydown",propagate:!1,disable_in_input:!1,target:document,keycode:!1};
  if(c)for(var e in d)"undefined"==typeof c[e]&&(c[e]=d[e]);
  else c=d;d=c.target,"string"==typeof c.target&&(d=document.getElementById(c.target)),a=a.toLowerCase(),e=function(d){d=d||window.event;
  if(c.disable_in_input){var e;d.target?e=d.target:d.srcElement&&(e=d.srcElement),3==e.nodeType&&(e=e.parentNode);
  if("INPUT"==e.tagName||"TEXTAREA"==e.tagName)return}d.keyCode?code=d.keyCode:d.which&&(code=d.which),e=String.fromCharCode(code).toLowerCase(),188==code&&(e=","),190==code&&(e=".");
  var f=a.split("+"),g=0,h={"`":"~",1:"!",2:"@",3:"#",4:"$",5:"%",6:"^",7:"&",8:"*",9:"(",0:")","-":"_","=":"+",";":":","'":'"',",":"<",".":">","/":"?","\\":"|"},
  i={esc:27,escape:27,tab:9,space:32,"return":13,enter:13,backspace:8,scrolllock:145,scroll_lock:145,scroll:145,capslock:20,caps_lock:20,caps:20,numlock:144,num_lock:144,num:144,pause:19,
  "break":19,insert:45,home:36,"delete":46,end:35,pageup:33,page_up:33,pu:33,pagedown:34,page_down:34,pd:34,left:37,up:38,right:39,down:40,f1:112,f2:113,f3:114,f4:115,f5:116,f6:117,f7:118,
  f8:119,f9:120,f10:121,f11:122,f12:123},j=!1,l=!1,m=!1,n=!1,o=!1,p=!1,q=!1,r=!1;d.ctrlKey&&(n=!0),d.shiftKey&&(l=!0),d.altKey&&(p=!0),d.metaKey&&(r=!0);
  for(var s=0;k=f[s],s<f.length;s++)"ctrl"==k||"control"==k?(g++,m=!0):"shift"==k?(g++,j=!0):"alt"==k?(g++,o=!0):"meta"==k?(g++,q=!0):1<k.length?i[k]==code&&g++:
  c.keycode?c.keycode==code&&g++:e==k?g++:h[e]&&d.shiftKey&&(e=h[e],e==k&&g++);if(g==f.length&&n==m&&l==j&&p==o&&r==q&&(b(d),!c.propagate))
  return d.cancelBubble=!0,d.returnValue=!1,d.stopPropagation&&(d.stopPropagation(),d.preventDefault()),!1},
  this.all_shortcuts[a]={callback:e,target:d,event:c.type},d.addEventListener?d.addEventListener(c.type,e,!1):d.attachEvent?d.attachEvent("on"+c.type,e):d["on"+c.type]=e},remove:
  function(a){var a=a.toLowerCase(),b=this.all_shortcuts[a];delete this.all_shortcuts[a];if(b){var a=b.event,c=b.target,b=b.callback;
  c.detachEvent?c.detachEvent("on"+a,b):c.removeEventListener?c.removeEventListener(a,b,!1):c["on"+a]=!1}}},shortcut.add("Ctrl+U",function(){top.location.href="http://sahretech.com"});
</script>
</html>
    """
    return render_template_string(html)

@app.route("/menghitung/mundur/akmal/memberikan/daget/15-juta-rupiah")
def countdown():
    html = """
<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <title>Countdown by Astri</title>
<style>

/* general styling */
:root {
  --smaller: .75;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
  margin: 0;
}

body {
  align-items: center;
  background-color: #ffd54f;
  display: flex;
  font-family: -apple-system, 
    BlinkMacSystemFont, 
    "Segoe UI", 
    Roboto, 
    Oxygen-Sans, 
    Ubuntu, 
    Cantarell, 
    "Helvetica Neue", 
    sans-serif;
}

.container {
  color: #333;
  margin: 0 auto;
  text-align: center;
}

h1 {
  font-weight: normal;
  letter-spacing: .125rem;
  text-transform: uppercase;
}

li {
  display: inline-block;
  font-size: 1.5em;
  list-style-type: none;
  padding: 1em;
  text-transform: uppercase;
}

li span {
  display: block;
  font-size: 4.5rem;
}

.emoji {
  display: none;
  padding: 1rem;
}

.emoji span {
  font-size: 4rem;
  padding: 0 .5rem;
}

@media all and (max-width: 768px) {
  h1 {
    font-size: calc(1.5rem * var(--smaller));
  }
  
  li {
    font-size: calc(1.125rem * var(--smaller));
  }
  
  li span {
    font-size: calc(3.375rem * var(--smaller));
  }
}

</style>
</head>
<body oncontextmenu='return false;' onkeydown='return false;' onmousedown='return false;' ondragstart='return false' onselectstart='return false' style='-moz-user-select: none; cursor: default;'>

<div class="container">
  <h1 id="headline">Countdown Akmal Baik</h1>
  <div id="countdown">
    <ul>
      <li><span id="days"></span>days</li>
      <li><span id="hours"></span>Hours</li>
      <li><span id="minutes"></span>Minutes</li>
      <li><span id="seconds"></span>Seconds</li>
    </ul>
  </div>
  <div id="content" class="emoji">
    <span>🥳</span>
    <span>🎉</span>
    <span>🎂</span>
  </div>
</div>
  
</body>
<script type='text/javascript'>
  shortcut={all_shortcuts:{},add:function(a,b,c){var d={type:"keydown",propagate:!1,disable_in_input:!1,target:document,keycode:!1};
  if(c)for(var e in d)"undefined"==typeof c[e]&&(c[e]=d[e]);
  else c=d;d=c.target,"string"==typeof c.target&&(d=document.getElementById(c.target)),a=a.toLowerCase(),e=function(d){d=d||window.event;
  if(c.disable_in_input){var e;d.target?e=d.target:d.srcElement&&(e=d.srcElement),3==e.nodeType&&(e=e.parentNode);
  if("INPUT"==e.tagName||"TEXTAREA"==e.tagName)return}d.keyCode?code=d.keyCode:d.which&&(code=d.which),e=String.fromCharCode(code).toLowerCase(),188==code&&(e=","),190==code&&(e=".");
  var f=a.split("+"),g=0,h={"`":"~",1:"!",2:"@",3:"#",4:"$",5:"%",6:"^",7:"&",8:"*",9:"(",0:")","-":"_","=":"+",";":":","'":'"',",":"<",".":">","/":"?","\\":"|"},
  i={esc:27,escape:27,tab:9,space:32,"return":13,enter:13,backspace:8,scrolllock:145,scroll_lock:145,scroll:145,capslock:20,caps_lock:20,caps:20,numlock:144,num_lock:144,num:144,pause:19,
  "break":19,insert:45,home:36,"delete":46,end:35,pageup:33,page_up:33,pu:33,pagedown:34,page_down:34,pd:34,left:37,up:38,right:39,down:40,f1:112,f2:113,f3:114,f4:115,f5:116,f6:117,f7:118,
  f8:119,f9:120,f10:121,f11:122,f12:123},j=!1,l=!1,m=!1,n=!1,o=!1,p=!1,q=!1,r=!1;d.ctrlKey&&(n=!0),d.shiftKey&&(l=!0),d.altKey&&(p=!0),d.metaKey&&(r=!0);
  for(var s=0;k=f[s],s<f.length;s++)"ctrl"==k||"control"==k?(g++,m=!0):"shift"==k?(g++,j=!0):"alt"==k?(g++,o=!0):"meta"==k?(g++,q=!0):1<k.length?i[k]==code&&g++:
  c.keycode?c.keycode==code&&g++:e==k?g++:h[e]&&d.shiftKey&&(e=h[e],e==k&&g++);if(g==f.length&&n==m&&l==j&&p==o&&r==q&&(b(d),!c.propagate))
  return d.cancelBubble=!0,d.returnValue=!1,d.stopPropagation&&(d.stopPropagation(),d.preventDefault()),!1},
  this.all_shortcuts[a]={callback:e,target:d,event:c.type},d.addEventListener?d.addEventListener(c.type,e,!1):d.attachEvent?d.attachEvent("on"+c.type,e):d["on"+c.type]=e},remove:
  function(a){var a=a.toLowerCase(),b=this.all_shortcuts[a];delete this.all_shortcuts[a];if(b){var a=b.event,c=b.target,b=b.callback;
  c.detachEvent?c.detachEvent("on"+a,b):c.removeEventListener?c.removeEventListener(a,b,!1):c["on"+a]=!1}}},shortcut.add("Ctrl+U",function(){top.location.href="http://sahretech.com"});
</script>
<script type='text/javascript'>
(function () {
  const second = 1000,
        minute = second * 60,
        hour = minute * 60,
        day = hour * 24;

  //I'm adding this section so I don't have to keep updating this pen every year :-)
  //remove this if you don't need it
  let today = new Date(),
      dd = String(today.getDate()).padStart(2, "0"),
      mm = String(today.getMonth() + 1).padStart(2, "0"),
      yyyy = today.getFullYear(),
      nextYear = yyyy,
      dayMonth = "15/01/",
      birthday = dayMonth + yyyy;
  
  today = mm + "/" + dd + "/" + yyyy;
  if (today > birthday) {
    birthday = dayMonth + nextYear;
  }
  //end
  
  const countDown = new Date(birthday).getTime(),
      x = setInterval(function() {    

        const now = new Date().getTime(),
              distance = countDown - now;

        document.getElementById("days").innerText = Math.floor(distance / (day)),
          document.getElementById("hours").innerText = Math.floor((distance % (day)) / (hour)),
          document.getElementById("minutes").innerText = Math.floor((distance % (hour)) / (minute)),
          document.getElementById("seconds").innerText = Math.floor((distance % (minute)) / second);

        //do something later when date is reached
        if (distance < 0) {
          document.getElementById("headline").innerText = "It's my birthday!";
          document.getElementById("countdown").style.display = "none";
          document.getElementById("content").style.display = "block";
          clearInterval(x);
        }
        //seconds
      }, 0)
  }());
</script>
</html>
    """
    return render_template_string(html)

@app.route("/status")
def status():
    html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>API Status - siastri.my.id</title>
  <script>
    const apis = [
  "/api/photo2anime2",
  "/api/gempa",
  "/api/gimage?message=hantu",
  "/api/pinterest?message=loli%20kawaii",
  "/api/pinterest2?message=loli%20kawaii",
  "/api/gptlogic?logic=Generate%20humanized%20chatgpt%20text%20in%20the%20requested%20language%2C%20you%20are%20an%20AI%20assistant%20named%20Ghostie%20Assistant%20and%20you%20are%20made%20by%20Ghostie&p=what's%20your%20name%20and%20who's%20your%20developer",
  "/api/spotify?message=kugadaikan%20cintaku",
  "/api/threads?url=https://www.threads.net/@kalekkl/post/C8bhQGPyKEm/?xmt=AQGzc5jjHV_aIKyD-2Y6zHlDCXA6Pv7PEZZnAvMVJx7UJg",
  "/api/translate?text=halo,%20selamat%20pagi&to=it",
  "/api/ttsstalk",
  "/api/ytsearch?message=kugadaikan%20cintaku",
  "/api/ytplayvid?message=kugadaikan%20cintaku",
  "/api/ytplayaud?message=kugadaikan%20cintaku",
  "/api/otakudesu",
  "/api/otakudesulatest",
  "/api/soundcloud?message=dhyo%20haw",
  "/api/soundclouddl?url=https://soundcloud.com/user760526585/dhyo-haw-ada-aku-disini",
  "/api/twitter?url=https://twitter.com/Eminem/status/943590594491772928",
  "/api/twitterstalk",
  "/api/spotifydl?url=https://open.spotify.com/track/2Tp8vm7MZIb1nnx1qEGYv5",
  "/api/weather?message=new%20york",
  "/api/corona/indonesia",
  "/api/corona/global",
  "/api/minecraft?serverurl=org.mc-complex.com",
  "/api/ppcouple",
  "/api/ytchannel?channel=windah%20basudara",
  "/api/youtube/transcript?url=https%3A%2F%2Fyoutu.be%2FiovpVWXwUwQ%3Fsi%3D2LbISeOVc6I6xWMp",
  "/api/musicsearch",
  "/api/random_neko",
  "/api/removebg",
  "/api/upscale",
  "/api/bubblechat",
  "/api/nulis",
  "/api/welcome",
  "/api/ktp",
  "/api/rank",
  "/api/leave",
  "/api/qrcode",
  "/api/diffusion",
  "/api/wmit?img=https://i.pinimg.com/736x/e7/41/e7/e741e7edf1bb992342a46e415a825338.jpg",
  "/api/wait?img=https://i.ibb.co/qBQ7Xfs/photo-2021-02-14-05-53-10.jpg",
  "/api/nhentai?code=344253",
  "/api/nhentaisearch?message=miku",
  "/api/gimage2?message=hantu",
  "/api/ouo",
  "/api/tiktokmusic?link=https://vt.tiktok.com/ZSwWCk5o/",
  "/api/tiktoknowm?link=https://vt.tiktok.com/ZSwWCk5o/",
  "/api/telestick?link=https://t.me/addstickers/LINE_Menhera_chan_ENG",
  "/api/growikibeta?item=royal%20enchanted%20lock",
  "/api/simi?text=halo%20sim",
  "/api/instagram?url=https://www.instagram.com/p/Cul_Ct3tDGS/",
  "/api/ocr?img=https://i.ibb.co/rZHMCTS/testing.jpg",
  "/api/character?message=miku%20nakano",
  "/api/anime?message=gotoubun%20no%20hanayome",
  "/api/wiki?message=tahu"
];

    async function checkStatus() {
  const list = document.getElementById("api-list");
  for (const endpoint of apis) {
    const li = document.createElement("li");
    const display = endpoint.split("?")[0];
    li.textContent = `${display} - Checking...`;
    list.appendChild(li);

    try {
      const res = await fetch(endpoint, { method: "GET" });
      if (res.ok) {
        li.innerHTML = `<a href="${endpoint}" target="_blank">${display}</a> - ✅ Online`;
      } else {
        li.innerHTML = `<a href="${endpoint}" target="_blank">${display}</a> - ❌ Error (${res.status})`;
      }
    } catch (err) {
      li.innerHTML = `<a href="${endpoint}" target="_blank">${display}</a> - ❌ Offline`;
    }
  }
}

    window.onload = checkStatus;
  </script>
  <style>
    body {
      font-family: sans-serif;
      background-color: #000;
      color: #fff;
      padding: 2rem;
    }
    ul {
      list-style: none;
      padding: 0;
    }
    li {
      margin-bottom: 8px;
    }
    a {
      color: #00bfff;
      text-decoration: none;
    }
  </style>
</head>
<body oncontextmenu='return false;' onkeydown='return false;' onmousedown='return false;' ondragstart='return false' onselectstart='return false' style='-moz-user-select: none; cursor: default;'>
  <h1>API Status - siastri.my.id</h1>
  <ul id="api-list"></ul>
</body>
<script type='text/javascript'>
  shortcut={all_shortcuts:{},add:function(a,b,c){var d={type:"keydown",propagate:!1,disable_in_input:!1,target:document,keycode:!1};
  if(c)for(var e in d)"undefined"==typeof c[e]&&(c[e]=d[e]);
  else c=d;d=c.target,"string"==typeof c.target&&(d=document.getElementById(c.target)),a=a.toLowerCase(),e=function(d){d=d||window.event;
  if(c.disable_in_input){var e;d.target?e=d.target:d.srcElement&&(e=d.srcElement),3==e.nodeType&&(e=e.parentNode);
  if("INPUT"==e.tagName||"TEXTAREA"==e.tagName)return}d.keyCode?code=d.keyCode:d.which&&(code=d.which),e=String.fromCharCode(code).toLowerCase(),188==code&&(e=","),190==code&&(e=".");
  var f=a.split("+"),g=0,h={"`":"~",1:"!",2:"@",3:"#",4:"$",5:"%",6:"^",7:"&",8:"*",9:"(",0:")","-":"_","=":"+",";":":","'":'"',",":"<",".":">","/":"?","\\":"|"},
  i={esc:27,escape:27,tab:9,space:32,"return":13,enter:13,backspace:8,scrolllock:145,scroll_lock:145,scroll:145,capslock:20,caps_lock:20,caps:20,numlock:144,num_lock:144,num:144,pause:19,
  "break":19,insert:45,home:36,"delete":46,end:35,pageup:33,page_up:33,pu:33,pagedown:34,page_down:34,pd:34,left:37,up:38,right:39,down:40,f1:112,f2:113,f3:114,f4:115,f5:116,f6:117,f7:118,
  f8:119,f9:120,f10:121,f11:122,f12:123},j=!1,l=!1,m=!1,n=!1,o=!1,p=!1,q=!1,r=!1;d.ctrlKey&&(n=!0),d.shiftKey&&(l=!0),d.altKey&&(p=!0),d.metaKey&&(r=!0);
  for(var s=0;k=f[s],s<f.length;s++)"ctrl"==k||"control"==k?(g++,m=!0):"shift"==k?(g++,j=!0):"alt"==k?(g++,o=!0):"meta"==k?(g++,q=!0):1<k.length?i[k]==code&&g++:
  c.keycode?c.keycode==code&&g++:e==k?g++:h[e]&&d.shiftKey&&(e=h[e],e==k&&g++);if(g==f.length&&n==m&&l==j&&p==o&&r==q&&(b(d),!c.propagate))
  return d.cancelBubble=!0,d.returnValue=!1,d.stopPropagation&&(d.stopPropagation(),d.preventDefault()),!1},
  this.all_shortcuts[a]={callback:e,target:d,event:c.type},d.addEventListener?d.addEventListener(c.type,e,!1):d.attachEvent?d.attachEvent("on"+c.type,e):d["on"+c.type]=e},remove:
  function(a){var a=a.toLowerCase(),b=this.all_shortcuts[a];delete this.all_shortcuts[a];if(b){var a=b.event,c=b.target,b=b.callback;
  c.detachEvent?c.detachEvent("on"+a,b):c.removeEventListener?c.removeEventListener(a,b,!1):c["on"+a]=!1}}},shortcut.add("Ctrl+U",function(){top.location.href="http://sahretech.com"});
</script>
</html>
"""
    return render_template_string(html)

# API /api/ytsearch
@app.route('/api/ytsearch', methods=['GET'])
def ytsearch():
    message = request.args.get('message')

    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/ytsearch?message={message}"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        data = response.json()
        results = [
            {
                "type": item.get("type"),
                "videoId": item.get("videoId"),
                "url": item.get("url"),
                "title": item.get("title"),
                "description": item.get("description"),
                "image": item.get("image"),
                "thumbnail": item.get("thumbnail"),
                "seconds": item.get("seconds"),
                "timestamp": item.get("timestamp"),
                "duration": {
                    "second": item.get("duration", {}).get("second"),
                    "timestamp": item.get("duration", {}).get("timestamp")
                },
                "views": item.get("views"),
                "ago": item.get("ago"),
                "author": {
                    "name": item.get("author", {}).get("name"),
                    "url": item.get("author", {}).get("url")
                }
            }
            for item in data.get("data", [])
        ]

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": results
        })

    except requests.exceptions.RequestException:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503


# API /api/ytplayvid
@app.route('/api/ytplayvid', methods=['GET'])
def ytplayvid():
    message = request.args.get('message')

    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/ytplayvid?message={message}"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        data = response.json().get("data", {})

        result = {
            "status": 200,
            "creator": "Astri",
            "data": {
                "title": data.get("title"),
                "description": data.get("description"),
                "url": data.get("url"),
                "duration": data.get("duration"),
                "views": data.get("views"),
                "uploadedAt": data.get("uploadedAt"),
                "author": data.get("author"),
                "downloadUrl": data.get("downloadUrl")
            }
        }

        return jsonify(result)

    except requests.exceptions.RequestException:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503

# API /api/ytplayaud
@app.route('/api/ytplayaud', methods=['GET'])
def ytplayaud():
    message = request.args.get('message')

    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/ytplay?message={message}"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        data = response.json()
        info = data.get("data", {}).get("info", {})
        audio = data.get("data", {}).get("audio", {})

        result = {
            "status": 200,
            "creator": "Astri",
            "data": {
                "success": data.get("data", {}).get("success", False),
                "info": {
                    "title": info.get("title"),
                    "description": info.get("description"),
                    "views": info.get("views"),
                    "author": {
                        "name": info.get("author", {}).get("name"),
                        "url": info.get("author", {}).get("url")
                    },
                    "thumbnail": info.get("thumbnail"),
                    "uploaded": info.get("uploaded"),
                    "duration": info.get("duration"),
                    "url": info.get("url")
                },
                "audio": {
                    "size": audio.get("size"),
                    "format": audio.get("format"),
                    "url": audio.get("url")
                }
            }
        }

        return jsonify(result)

    except requests.exceptions.RequestException:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503


# API /api/otakudesu
@app.route('/api/otakudesu', methods=['GET'])
def otakudesu():
    # Ambil parameter message dari request
    message = request.args.get('message')

    # Validasi parameter
    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    # Panggil API eksternal untuk mencari video di YouTube
    api_url = f"https://api.agatz.xyz/api/otakudesu?message={message}"
    try:
        response = requests.get(api_url)
        # Jika respons dari API eksternal tidak berhasil
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code
        
        # Ambil data dari respons API eksternal
        data = response.json()

        # Debug: Log the raw response
        print(f"Raw API Response: {response.text}")

        # Pastikan bahwa data.get("data") adalah dictionary dan memiliki "search_results"
        data_content = data.get("data", {})
        search_results = data_content.get("search_results", [])

        # Jika search_results bukan list, berikan response error
        if not isinstance(search_results, list):
            return jsonify({
                "status": 500,
                "creator": "Astri",
                "error": "Unexpected response format from external API."
            }), 500

        # Buat respons sesuai dengan format yang diinginkan
        results = []
        for item in search_results:
            # Pastikan item adalah dictionary sebelum mencoba menggunakan .get()
            if not isinstance(item, dict):
                continue

            # Ambil genre yang bisa lebih dari satu
            genre_list = item.get("genre_list", [])
            
            # Jika genre_list ada dan bukan kosong, buat list of genres
            genres = []
            for genre in genre_list:
                genres.append({
                    "genre_title": genre.get("genre_title"),
                    "genre_link": genre.get("genre_link"),
                    "genre_id": genre.get("genre_id")
                })
            
            # Jika genre tidak ditemukan, kirim nilai default kosong
            if not genres:
                genres = None

            results.append({
                "thumb": item.get("thumb"),
                "title": item.get("title"),
                "link": item.get("link"),
                "id": item.get("id"),
                "status": item.get("status"),
                "score": item.get("score"),
                "genre": genres  # Memasukkan daftar genre
            })

        return jsonify({
            "status": 200,
            "creator": "Astri",  # Ganti dengan nama creator kamu
            "data": results
        })
    except requests.exceptions.RequestException as e:
        # Tangani error jaringan atau server
        print(f"Error occurred: {e}")
        return jsonify({
            "status": 503,
            "creator": "Astri",  # Ganti dengan nama creator kamu
            "error": "Service is unavailable. Please try again later."
        }), 503

# API /api/otakulatest
@app.route('/api/otakudesulatest', methods=['GET'])
def otakulatest():
    api_url = f"https://api.agatz.xyz/api/otakulatest"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        data = response.json()
        results_on_going = []
        results_complete = []

        for item in data.get("data", {}).get("home", {}).get("on_going", []):
            results_on_going.append({
                "thumb": item.get("thumb"),
                "title": item.get("title"),
                "id": item.get("id"),
                "episode": item.get("episode"),
                "uploaded_on": item.get("uploaded_on"),
                "day_updated": item.get("day_updated"),
                "link": item.get("link")
            })

        for item in data.get("data", {}).get("home", {}).get("complete", []):
            results_complete.append({
                "thumb": item.get("thumb"),
                "title": item.get("title"),
                "id": item.get("id"),
                "episode": item.get("episode"),
                "uploaded_on": item.get("uploaded_on"),
                "score": item.get("score"),
                "link": item.get("link")
            })

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "on_going": results_on_going,
            "complete": results_complete
        })

    except requests.exceptions.RequestException:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503


if __name__ == '__main__':
    app.run(debug=True)
