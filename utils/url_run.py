import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtWebKit import QWebSettings
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import *
import urllib

from threading import Thread
import time

import config


UA_STRING = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.2 Safari/537.13"


class PageOpen(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
    def run(self):
        """
        #   
        """
        number = 1

        while True:
            config.db.reconnect()
            items = config.db.query(  "SELECT id, PoC FROM flash_test_link order by id asc limit %s", number)
            if not items:
                time.sleep(30)
            else:
                config.db.executemany("DELETE FROM flash_test_link WHERE id = %s", [[item.id] for item in items])
                for item in items:
                    self.sendurl(item.PoC)
                time.sleep(10)

    def sendurl(self, url):
        self.emit(QtCore.SIGNAL("open"), url)




class YWebPage(QtWebKit.QWebPage):
    def __init__(self):
        super(YWebPage, self).__init__()

    def userAgentForUrl(self, url):
        return UA_STRING


class Browser(QtGui.QMainWindow): # "Browser" window
    def __init__(self, main, url):
        QtGui.QMainWindow.__init__(self)
        self.main = main
        self.webView = QtWebKit.QWebView()
        self.setCentralWidget(self.webView)
        self.yPage = YWebPage()
        self.webView.setPage(self.yPage)
        self.url = QtCore.QUrl(url)
        self.webView.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True) # Enables flash player
        self.webView.load(self.url)

        self.page = self.webView.page()
        self.page.networkAccessManager().sslErrors.connect(lambda reply, errors: self.handleSslErrors(reply, errors))

    def closeEvent(self, event):
        self.main.browsers.remove(self)
        super(Browser, self).closeEvent(event)

    def handleSslErrors(self, reply, errors):
        # ignore SSL errors on Windows (yes a uggly workaround, don't know how to fix it yet)
        #for error in errors:
            #print error.errorString()
        reply.ignoreSslErrors(errors)

class MainWindow:
    def __init__(self):
        self.browsers = []
        self.thread = PageOpen()
        QtCore.QObject.connect(self.thread, QtCore.SIGNAL("open"), self.open)
        self.thread.start()

    def open(self, url):
        url = QtCore.QString(urllib.unquote_plus(url))
        b = Browser(self, url)
        b.show()
        self.browsers.append(b)




def start():
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()