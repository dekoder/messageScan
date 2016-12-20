import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtWebKit import QWebSettings
from PyQt4.QtNetwork import QNetworkAccessManager
import urllib
from threading import Thread


def browser():
    app = QtGui.QApplication(sys.argv)
    web = QtWebKit.QWebView()
    web.settings().setAttribute(QWebSettings.PluginsEnabled, True) # Enables flash player
    #web.load(QUrl("http://127.0.0.1/static/test/alert.html"))
    web.load(QtCore.QUrl(QtCore.QString(urllib.unquote_plus(
        r'http://127.0.0.1/checker/func/1?action=start_page'))))
    #web.show()

    sys.exit(app.exec_())

def start_bro():
    Thread(target=browser).start()

if __name__ == "__main__":
    browser()