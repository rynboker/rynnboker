from flask import Flask, jsonify, request
import requests
import logging

app = Flask(__name__)

@app.route("/status")
def status():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>API Status - siastri.my.id</title>
  <script>
    const apis = [
      "/api/photo2anime2", "/api/gempa", "/api/gimage", "/api/pinterest", "/api/pinterest2",
      "/api/gptlogic", "/api/shorturl", "/api/spotify", "/api/threads", "/api/translate",
      "/api/ttsstalk", "/api/ytsearch", "/api/ytplayvid", "/api/ytplayaud", "/api/otakudesu",
      "/api/otakudesulatest", "/api/soundcloud", "/api/soundclouddl", "/api/twitter",
      "/api/twitterstalk", "/api/spotifydl", "/api/weather", "/api/corona/indonesia",
      "/api/corona/global", "/api/minecraft", "/api/ppcouple", "/api/ytchannel",
      "/api/youtube/transcript", "/api/musicsearch", "/api/random_neko", "/api/removebg",
      "/api/upscale", "/api/bubblechat", "/api/nulis", "/api/welcome", "/api/ktp", "/api/rank",
      "/api/leave", "/api/qrcode", "/api/diffusion", "/api/wmit", "/api/wait", "/api/nhentai",
      "/api/nhentaisearch", "/api/gimage2", "/api/ouo", "/api/tiktokmusic", "/api/tiktoknowm",
      "/api/telestick", "/api/growikibeta", "/api/simi", "/api/instagram", "/api/ocr",
      "/api/character", "/api/anime", "/api/wiki"
    ];

    async function checkStatus() {
      const list = document.getElementById("api-list");
      for (const endpoint of apis) {
        const li = document.createElement("li");
        li.textContent = `${endpoint} - Checking...`;
        list.appendChild(li);

        try {
          const res = await fetch(endpoint, { method: "GET" });
          if (res.ok) {
            li.innerHTML = `<a href="${endpoint}" target="_blank">${endpoint}</a> - ✅ Online`;
          } else {
            li.innerHTML = `<a href="${endpoint}" target="_blank">${endpoint}</a> - ❌ Error (${res.status})`;
          }
        } catch (err) {
          li.innerHTML = `<a href="${endpoint}" target="_blank">${endpoint}</a> - ❌ Offline`;
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
  <p>Berikut daftar API yang tersedia dan statusnya:</p>
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
return Response(html, mimetype='text/html')

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
