# -*- coding: utf-8 -*-

import threading
import requests

import checker

from utils import config

from golink import goolinks


def start_process(processer_id):
    t = threading.Thread(target=hacking, args=([processer_id]))
    t.start()


def hacking(processer_id):

    config.db.reconnect()
    processer = config.db.get("select * from processer where id = %s", int(processer_id))
    if not processer:
        print processer_id, "not exsits"
        return
    #print processer
    links = goolinks(processer.dork, 10000)

    config.db.reconnect()
    config.db.executemany(
                "INSERT INTO result (url,processer_id,result) VALUES (%s,%s,%s)",
                [(link, processer_id, 'unknow') for link in links])

    checker_id = config.db.get("select checker_id from processer where id = %s", int(processer_id))
    PoC_Addr = config.db.get("select PoC_Addr from checker where id = %s", int(checker_id.checker_id))
    func = checker.ChooseFunc(PoC_Addr.PoC_Addr)
    results = config.db.query("select * from result where processer_id = %s", int(processer_id))
    func(results)
    #start_check(processer_id)


#废弃函数
def checking(processer_id):
    processer = config.db.get("select * from processer where id = %s", int(processer_id))
    pass
    #todo

def start_check(processer_id):
    t = threading.Thread(target=test_check, args=([processer_id]))
    t.start()

def test_check(processer_id):
    processer = config.db.get("select * from processer where id = %s", int(processer_id))
    if not processer:
        print processer_id, "not exsits"
        return
    checker_id = config.db.get("select checker_id from processer where id = %s", int(processer_id))
    PoC_Addr = config.db.get("select PoC_Addr from checker where id = %s", int(checker_id.checker_id))
    func = checker.ChooseFunc(PoC_Addr.PoC_Addr)
    results = config.db.query("select * from result where processer_id = %s", int(processer_id))
    func(results)

    return 
    checker_id = config.db.get("select checker_id from processer where id = %s", int(processer_id))
    PoC_Addr = config.db.get("select PoC_Addr from checker where id = %s", int(checker_id.checker_id))
    func = checker.ChooseFunc(PoC_Addr.PoC_Addr)
    #print func
    items = config.db.query("select url, id from result where processer_id = %s", int(processer_id))
    for item in items:
        func(item.url, item.id)
        #这里需要建立一个线程池来启动线程
        #可能不需要了,因为只是入库


if __name__ == "__main__":
    test_check(40)