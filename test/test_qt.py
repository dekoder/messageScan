import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtWebKit import QWebSettings
from PyQt4.QtNetwork import QNetworkAccessManager
import urllib

class MyView(QtWebKit.QWebView):
    def __init__(self):
        QtWebKit.QWebView.__init__(self)
    def urlChanged(self, url):
        print 1
        pass

def browser_main():
    app = QtGui.QApplication(sys.argv)
    web = QtWebKit.QWebView()#MyView()
    web.settings().setAttribute(QWebSettings.PluginsEnabled, True) # Enables flash player
    #web.load(QUrl("http://127.0.0.1/static/test/alert.html"))
    web.load(QtCore.QUrl(QtCore.QString(urllib.unquote_plus(
        r"http://user.baidu.com/public/Friend/ZeroClipboard.swf?id=\%22))}catch(e){location.href='http://www.baidu.com';}//&width=500&height=500&.swf"))))
    web.show()
    print web.page().mainFrame().url()
    sys.exit(app.exec_())

if __name__ == "__main__":
    browser_main()