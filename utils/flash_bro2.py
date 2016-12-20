import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtWebKit import QWebSettings
from PyQt4.QtNetwork import QNetworkAccessManager
import urllib

from threading import Thread
import time


UA_STRING = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.2 Safari/537.13"


class UrlCheck(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
    def run(self):
        while True:
            time.sleep(20)
            self.emit(QtCore.SIGNAL("check"))


class YWebPage(QtWebKit.QWebPage):
    def __init__(self):
        super(YWebPage, self).__init__()

    def userAgentForUrl(self, url):
        return UA_STRING


class Browser: # "Browser" window
    def __init__(self):
        self.webView = QtWebKit.QWebView()
        self.show = self.webView.show
        self.url = QtCore.QUrl(QtCore.QString(urllib.unquote_plus(
            r'http://127.0.0.1/checker/func/1?action=start_page')))#

        self.webView.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True) # Enables flash player

        self.webView.load(self.url)

        self.page = self.webView.page()
        self.page.networkAccessManager().sslErrors.connect(lambda reply, errors: self.handleSslErrors(reply, errors))

        self.thread = UrlCheck()
        QtCore.QObject.connect(self.thread, QtCore.SIGNAL("check"), self.check)
        self.thread.start()

    def check(self):
        self.webView.load(self.url)

    def handleSslErrors(self, reply, errors):
        reply.ignoreSslErrors(errors)




def _start():
    app = QtGui.QApplication(sys.argv)
    b = Browser()
    #b.show()
    sys.exit(app.exec_())

def start_bro():
    Thread(target=_start).start()

if __name__ == '__main__':
    _start()