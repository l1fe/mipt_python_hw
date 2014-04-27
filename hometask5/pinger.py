import sys
from PySide.QtCore import *
from PySide.QtGui import *
import threading

class Pinger(QWidget):
    def __init__(self):
        super(Pinger, self).__init__()

        self.initUI()

    def initUI(self):
        self.setFixedSize(500, 500)
        self.setWindowTitle('Pinger')

        self.inputFile = None
        self.outputFile = None

        self.inputEditor = QTextEdit(self)
        self.inputEditor.setFixedSize(250, 250)
        self.inputEditor.move(0, 75)

        self.outputEditor = QTextEdit(self)
        self.outputEditor.setFixedSize(250, 250)
        self.outputEditor.move(250, 75)

        self.inputPrompt = QLabel(self)
        self.inputPrompt.setText('List IP\'s there:')
        self.inputPrompt.move(50, 60)

        self.outputPrompt = QLabel(self)
        self.outputPrompt.setText('Result:')
        self.outputPrompt.move(350, 60)

        self.pingButton = QPushButton(self)
        self.pingButton.setText('Ping!')
        self.pingButton.clicked.connect(self.ping)

        self.inputFileButton = QPushButton(self)
        self.inputFileButton.setText('Input File')
        self.inputFileButton.clicked.connect(self.showFileDialogInput)

        self.outputFileButton = QPushButton(self)
        self.outputFileButton.setText('Output File')
        self.outputFileButton.clicked.connect(self.showFileDialogOutput)

        self.toolbar = QToolBar(self)
        self.toolbar.setFixedSize(500, 30)

        self.toolbar.addWidget(self.inputFileButton)
        self.toolbar.addWidget(self.outputFileButton)
        self.toolbar.addWidget(self.pingButton)

        self.show()

    def showFileDialogInput(self):
        self.inputFile = open(QFileDialog.getOpenFileName(self, 'Input', '', 'Text files (*txt)')[0], 'r')
        if not self.inputFile is None:
            self.inputEditor.append(self.inputFile.read())
        return

    def showFileDialogOutput(self):
        self.outputFile = open(QFileDialog.getOpenFileName(self, 'Input', '', 'Text files (*txt)')[0], 'w')
        return

    def ping(self):
        text = None
        if self.inputFile is None:
            text = self.inputEditor.toPlainText()
        else:
            text = self.inputFile.read()

        if text is None:
            return

        print('Checking IP\'s...')

        self.check_args(text)

        self.pinger(file, text)

    def check_args(self, text):
        if not text.strip():
            return

        print(text)
        ips = text.split()

        for cur_ip in ips:
            import re
            ip_expression = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
            if not(ip_expression.match(cur_ip)):
                print('Wrong ip: ' + cur_ip)
                self.showNotification('Incorrect ip:', cur_ip)

    def pinger(self, output, args):
        file_lock = threading.Lock()
        threads = []
        for current_ip in args:
            threads.append(threading.Thread(target=self.ping_ip, args=(current_ip, file_lock, output)))
            threads[-1].start()

        for current_ip in threads:
            current_ip.join()

    def ping_ip(self, ip, file_lock, output):
        import subprocess
        result = subprocess.call(["ping", '-n', '1', ip], stdout = subprocess.PIPE)

        file_lock.acquire()
        try:
            if result == 0:
                output += (ip + '\n')
        finally:
            file_lock.release()

    def showNotification(self):
        return 0


def main():
    app = QApplication(sys.argv)
    ex = Pinger()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
