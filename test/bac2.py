import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtWebKit import QWebSettings
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import *
import urllib

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
        self.resize(800,600) # Viewport size
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

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browsers = []

        #self.resize(200, 450)
        #self.setFixedSize(200, 350)
        #self.move(300, 300)
        #self.setWindowTitle('U-bot 0.1')

        # Setup GUI

        # Start Button
        #self.__button = QtGui.QPushButton('Start')
        #self.__button.clicked.connect(self.open)

        # Text area
        #self.__qle = QtGui.QLineEdit()
        #self.__qle.setText("https://www.alipay.com/")

        # Images
        #pixmap1 = QtGui.QPixmap("ubot.png")
        #lbl1 = QtGui.QLabel()
        #lbl1.resize(200, 150)
        #lbl1.setPixmap(pixmap1)
        #lbl1.setScaledContents(True)

        #layout = QtGui.QVBoxLayout()
        #layout.addStretch(1)

        #layout.addWidget(self.__qle)
        #layout.addWidget(self.__button)

        #self.setLayout(layout)

    def open(self, url):
        url = QtCore.QString(urllib.unquote_plus(url))
        #url = QtCore.QString(urllib.unquote_plus(str(self.__qle.text())))
        b = Browser(self, url)
        b.show()
        self.browsers.append(b)


def main():
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    w.open("https://www.alipay.com")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()