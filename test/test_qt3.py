import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import *
import logging

class WebPage(QWebPage):
    """
    Makes it possible to use a Python logger to print javascript console messages
    """
    def __init__(self, logger=None, parent=None):
        super(WebPage, self).__init__(parent)
        if not logger:
            logger = logging
        self.logger = logger

    def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):
        self.logger.warning("JsConsole(%s:%d): %s" % (sourceID, lineNumber, msg))

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.view = QWebView(self)

        self.setupInspector()

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)

        layout = QVBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self.splitter)

        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.webInspector)

    def setupInspector(self):
        page = self.view.page()
        page.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        self.webView = QWebView()
        self.webView.settings().setAttribute(QWebSettings.PluginsEnabled, True) # Enables flash player

        page.networkAccessManager().sslErrors.connect(lambda reply, errors: self.handleSslErrors(reply, errors))

        self.webInspector = QWebInspector(self)
        self.webInspector.setPage(page)

        shortcut = QShortcut(self)
        shortcut.setKey(Qt.Key_F12)
        shortcut.activated.connect(self.toggleInspector)
        self.webInspector.setVisible(False)

    def handleSslErrors(self, reply, errors):
        for error in errors:
            print "handle1",error.errorString()
            reply.ignoreSslErrors(errors)

    def toggleInspector(self):
        self.webInspector.setVisible(not self.webInspector.isVisible())

def main():
    url = 'http://www.baidu.com' #'https://www.alipay.com'#
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.view.load(QUrl(url)) # V
    app.exec_()

if __name__ == "__main__":
    main()