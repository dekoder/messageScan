# -*- coding: utf-8 -*-
import httplib,re,urllib

def geturl(url,*arg,**kwarg):
    # geturl("[http[s]://]www.baidu.com[/asdedee?ssddd]","id=aa&edd=fff",method="post")
    # return [text.decode,r_header,status]
    # que:httplib
    
    method="get"
    is_ssl=0
    div=""
    header=   {
                  "Content-Type":"application/x-www-form-urlencoded",
                  "Connection":"Keep-Alive",
                  "Referer":'http://www.taobao.com',
                  "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.2 Safari/537.13",  
                }
    re_turn=""
    if arg:
        params=arg[0]
    if kwarg:
        for name in kwarg:
            if name=="method":
                method=kwarg[name]
            if name=="header":
                header=kwarg[name]
            if name=="return":
                re_turn=kwarg[name]
    
    ind_div=url.find("://")
    if ind_div!=-1:
        div=url[:ind_div]
        url=url[ind_div+3:]
    
    if div=="https":
        is_ssl=1
    
    ind_host=url.find('/')
    if ind_host!=-1:
        host=url[:ind_host]
        urlpath=url[ind_host:]
    else:
        host=url
        urlpath="/"
    try:
        if is_ssl==1:
            conn=httplib.HTTPSConnection(host)
        else :
            conn = httplib.HTTPConnection(host) 
        if method.lower()=="post":
            conn.request(method="POST",url=urlpath,body=params,headers=header)
        else:
            conn.request("GET",urlpath,headers=header)
        respon=conn.getresponse()
        r_header=respon.getheaders()
        status=respon.status  
        text=respon.read()
    except:
        if re_turn=="list":
            return []
        return ""       
    decodes=0
    for k in r_header:
        if k[0]=='content-type':
            ss=k[1].find('charset')
            if ss!=-1:
                charset=k[1][ss+8:]
                #print charset
                if charset=='utf-8' or charset=='UTF-8':
                    text=text.decode('utf-8')
                    decodes=1
                    break
                else:
                    try:
                        #print "decode by ",charset   #debug
                        text=text.decode(charset)                         # not useful
                        decodes=1
                    except:
                        print "error"
                        break
    if decodes==0:
        try:
            text=text.decode('utf-8')
        except:
            try:
                text=text.decode('gbk')
            except:
                print "can't decode"  #fix
    conn.close();
    if re_turn=="list":
        return [text,r_header,status]
    return text

def google(search_str,total=False):
    #total_num: -1 not use

    print "Search Msg:",search_str
    try:
        data=geturl(search_str)
    except:
        print "Error Massage:google dont retrun data"
        links=[]
    if 1:
        comp=re.compile(r'<h3 class="r"><a href="([\s\S]*?)"')
        comp2=re.compile('<div\sid="resultStats">.*?([,\d]+)\sresults<nobr>')
        tmp_links=comp.findall(data)
        #print tmp_links
        up_num = comp2.search(data)
        total_num = -1
        if up_num:
            print up_num.group(0)
            total_num = int(up_num.group(1).replace(",",""))

        links = tmp_links
        """
        links = []
        for x in tmp_links:
            od = x.find("http://")
            if od != 0:
                links.append(x[od:])
            else:
                links.append(x)
        """
    print "len:", len(links)
    if total:
        print "total:", total_num
        return links, total_num
    return links

def goolinks(in_str,num=400,start=0):
        #in_str ='baidu.com'
        inc=50
        links=[]

        while len(links)<num:
            _start=str(start)
            params=urllib.urlencode({'q':in_str,'start':_start,})
            search="http://91.213.30.150/search?filter=0&"+params+"&num="+str(inc)
            g_links, total_num = google(search,total=True)
            if total_num > 0:
                num = total_num                                                   #change num when page changed
            start+=inc
            if len(g_links)<1:
                print "google failed ----->in webconnect.py"
                break
            if len(g_links)<inc*9/10:
                print "google end ----->in webconnect.py"
                for link in g_links:
                    links.append(link) 
                    break
            for link in g_links:
                links.append(link) 

        return links

def test():
    print "##### test geturl ####"
    #data = geturl("www.baidu.com")
    data = geturl("https://www.google.com.hk/search?q=aaaa")
    print data[:100]
    print "##### test google ####"
    data = google("https://www.google.com.hk/search?q=aaaa")
    print data[:4]
    if not data:
        print "failed"
        exit()
    print "##### test goolinks ####"
    print goolinks("aabb")[:5]
if __name__ == "__main__":
    test()
