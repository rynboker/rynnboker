import random
import string
from datetime import datetime, timedelta
import json
import requests
from flask import Flask, jsonify, request, redirect, Response
import os

app = Flask(__name__)

# Define the path for persistent storage (e.g., in Vercel's file system)
DATABASE_FILE = "/tmp/listurl.json"

# Function to load URL mappings from the file
def load_url_mappings():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

# Function to save URL mappings to the file
def save_url_mappings(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Function to generate short URL codes
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/")
def index():
    html = """
<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <title>Putri Amelia</title>
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
    <a target="_blank" href="#">
      <img src="https://avatars.githubusercontent.com/u/81070831?v=4" class="hoverZoomLink">
    </a>

    <!-- the username -->
    <h1>
            Putri Amelia
          </h1>

    <!-- and role or location -->
    <h2>
            A.D.I Family
          </h2>

  </header>

  <!-- bit of a bio; who are you? -->
  <div class="profile-bio">

    <p>
      My name is Putri Amelia, you can call me Lia. I was born in Bandung, Indonesia. I'm 24 years old and still in collage. This is an API website, you can join my discord server.
    </p>

  </div>

  <!-- some social links to show off -->
  <ul class="profile-social-links">
    <li>
      <a target="_blank" href="https://github.com/nomel2837">
        <i class="fab fa-github"></i>
      </a>
    </li>
    <li>
      <a target="_blank" href="https://discord.com/users/826098988725829662">
        <i class="fab fa-discord discord-icon"></i>
      </a>
    </li>
    <li>
      <a target="_blank" href="https://instagram.com/_matchaamel">
        <i class="fab fa-instagram"></i>
      </a>
    </li>
    <li>
      <a target="_blank" href="https://discord.gg/nHm2ZwvqC8">
       
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
    return Response(html, mimetype='text/html')

@app.route('/api/shorturl', methods=['POST'])
def create_short_url():
    try:
        data = request.get_json()
        original_url = data.get('originalUrl')
        custom_name = data.get('customName')

        if not original_url:
            return jsonify({
                "status": 400,
                "error": "Parameter 'originalUrl' is required."
            }), 400

        url_mapping = load_url_mappings()

        if custom_name:
            short_code = custom_name
            if short_code in url_mapping:
                return jsonify({
                    "status": 400,
                    "error": "Custom name already taken."
                }), 400
        else:
            short_code = generate_short_code()
            while short_code in url_mapping:
                short_code = generate_short_code()

        expiration_date = datetime.now() + timedelta(days=30)
        url_mapping[short_code] = {
            "originalUrl": original_url,
            "expirationDate": expiration_date.isoformat()
        }

        save_url_mappings(url_mapping)

        short_url = f"https://www.youga.my.id/{short_code}"

        return jsonify({
            "status": "success",
            "data": {
                "originalUrl": original_url,
                "shortUrl": short_url,
                "customName": custom_name or short_code,
                "expirationDate": expiration_date.isoformat()
            }
        })

    except Exception as e:
        print(f"Error occurred")
        return jsonify({
            "status": "error",
            "error": "Error occurred"
        }), 500

@app.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    try:
        url_mapping = load_url_mappings()
        url_data = url_mapping.get(short_code)

        if not url_data:
            return jsonify({
                "status": 404,
                "error": "Short URL not found."
            }), 404

        expiration_date = datetime.fromisoformat(url_data["expirationDate"])
        if datetime.now() > expiration_date:
            del url_mapping[short_code]
            save_url_mappings(url_mapping)
            return jsonify({
                "status": 410,
                "error": "This short URL has expired."
            }), 410

        return redirect(url_data["originalUrl"])

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": "Error occurred"
        }), 500

@app.route('/api/spotify', methods=['GET'])
def spotify():
    message = request.args.get('message')

    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/spotify?message={message}"
    try:
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        external_data = response.json().get("data", [])
        formatted_data = [
            {
                "trackNumber": item.get("trackNumber"),
                "trackName": item.get("trackName"),
                "artistName": item.get("artistName"),
                "albumName": item.get("albumName"),
                "duration": item.get("duration"),
                "previewUrl": item.get("previewUrl"),
                "externalUrl": item.get("externalUrl")
            }
            for item in external_data
        ]

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred"
        }), 500

@app.route('/api/threads', methods=['GET'])
def threads():
    url = request.args.get('url')

    if not url:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'url' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/threads?url={url}"
    try:
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        external_data = response.json().get("data", {})
        image_urls = external_data.get("image_urls", [])
        video_urls = external_data.get("video_urls", [])

        formatted_data = {
            "image_urls": image_urls,
            "video_urls": video_urls
        }

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": "An unexpected error occurred"
        }), 500

@app.route('/api/translate', methods=['GET'])
def translate_text():
    text = request.args.get('text')
    to_language = request.args.get('to', 'en')

    if not text:
        return jsonify({
            "status": 400,
            "error": "Parameter 'text' is required."
        }), 400

    popcat_url = "https://api.popcat.xyz/translate"
    try:
        response = requests.get(popcat_url, params={"to": to_language, "text": text})

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "error": "Failed to retrieve translation API."
            }), response.status_code

        popcat_data = response.json()
        translated_text = popcat_data.get("translated")

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "result": translated_text
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred"
        }), 500

@app.route('/api/ttstalk', methods=['GET'])
def ttstalk():
    name = request.args.get('name')

    if not name:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'name' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/ttstalk?name={name}"
    try:
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        try:
            external_data = response.json()
            
            # Check if the response is a dictionary and contains the "data" field
            if isinstance(external_data, dict) and "data" in external_data:
                external_data = external_data["data"]
            else:
                return jsonify({
                    "status": 404,
                    "creator": "Astri",
                    "error": "No valid data found for the specified name."
                }), 404

        except ValueError as e:
            app.logger.error(f"Error parsing JSON")
            return jsonify({
                "status": 500,
                "creator": "Astri",
                "error": "Failed to parse the response from the external service."
            }), 500

        # Format data as expected
        formatted_data = {
            "photo": external_data.get("photo"),
            "username": external_data.get("username"),
            "name": external_data.get("name"),
            "bio": external_data.get("bio"),
            "followers": external_data.get("followers"),
            "following": external_data.get("following"),
            "likes": external_data.get("likes"),
            "posts": external_data.get("posts")
        }

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })

    except requests.exceptions.RequestException as e:
        app.logger.error(f"RequestException")
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable"
        }), 503

    except Exception as e:
        app.logger.error(f"Unexpected error")
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred"
        }), 500
        
if __name__ == "__main__":
    app.run(debug=True)
