# -*- coding: utf-8 -*-


import markdown
import os.path
import re
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
import json

from utils import config
from utils import flash_bro2
import Action

from utils import google_check
from threading import Thread

ipbox = None

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/process", ProcesserHandler),            
            (r"/checker", CheckerHandler),
            (r"/singlepro/(\d+)", SingerProHandler),
            (r"/GoogleIP", GoogleIPHandler),

            #action
            (r"/action/singlepro/add", AddProHandler),
            (r"/action/singlepro/del", DelProHandler),

            #check
            (r"/checker/func/1", Check1Handler),
        ]
        settings = dict(
            blog_title=u"dorkoo",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = config.db


class GoogleIPHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><p>Google IP: '+str(ipbox.get("ip"))+\
                '</p><p>Google Proxy: '+str(ipbox.get("proxy"))+'</p></body></html>')

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def initialize(self):
        self.db.reconnect()

class HomeHandler(BaseHandler):
    def get(self):
        #print 1
        self.render("home.html")

class ProcesserHandler(BaseHandler):
    def get(self):
        processers = self.db.query("SELECT * FROM processer")
        #print processers
        self.render("processer.html", entrys=processers)


class CheckerHandler(BaseHandler):
    def get(self):
        checkers = self.db.query("SELECT * FROM checker")
        self.render("checker.html", checkers = checkers)

class SingerProHandler(BaseHandler):
    def get(self, num):
        processer = self.db.get("SELECT * FROM processer where id = %s", int(num))
        results = self.db.query("SELECT * FROM result where processer_id = %s", int(num))
        self.render("singlepro.html", results=results, num=num, processer = processer)



#handle action
class AddProHandler(BaseHandler):
    def post(self):
        dork = self.get_argument("dork")
        checker_id = self.get_argument("checker_id")
        time = self.get_argument("time")
        status = self.get_argument("status", default= "stop")
        if status != "stop":
            status = "run"
        id = self.db.execute(
                "INSERT INTO processer (dork,checker_id,status,interval_time) VALUES (%s,%s,%s,%s)",
                dork,int(checker_id), status, int(time))
        if status == "run":
            Action.start_process(id)
        self.redirect('/process', permanent=True)

class DelProHandler(BaseHandler):
    def post(self):
        id = self.get_argument("id")
        self.db.execute("DELETE FROM processer WHERE id = %s", int(id))
        self.db.execute("DELETE FROM result WHERE processer_id = %s", int(id))
        self.db.execute("DELETE FROM flash_test_link WHERE pid = %s", int(id))
        self.render("home.html")




# used for check thread

class Check1Handler(BaseHandler):
    #iframe集合页面，接收url，发起Flash requests
    def get(self):
        action = self.get_argument("action")
        if action == "get_url":
            nodes = self.get_argument("nodes")
            items = self.db.query(  "SELECT id, PoC FROM flash_test_link order by id asc limit %s", int(nodes))
            if not items:
                self.write(json.dumps({"urls":[]}))
                self.finish()
                return
            self.db.executemany("DELETE FROM flash_test_link WHERE id = %s", [[item.id] for item in items])
            self.write(json.dumps({"urls":[item.PoC for item in items]}))
            self.finish()
        elif action == "start_page":
            self.render("flash_fuzz.html")
        elif action == "check_xss":
            #there is a xss
            url = self.get_argument("url")
            f = open("a.txt", "a+")
            f.write(url+"\n")
            f.close()
            print '#'*10
            print url
            print '#'*10
            #todo

# end check


def main():
    global ipbox
    ipbox = google_check.IPBox()
    browser = flash_bro2.start_bro()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
