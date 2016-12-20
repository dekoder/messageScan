import requests

header=   {
                  "Content-Type":"application/x-www-form-urlencoded",
                  "Connection":"Keep-Alive",
                  "Referer":'http://www.taobao.com',
                  "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.2 Safari/537.13",  
                }

r = requests.get("http://218.176.242.234", headers =header, timeout= 4)
print r.text