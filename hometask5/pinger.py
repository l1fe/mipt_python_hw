import sys
from PySide.QtCore import *
from PySide.QtGui import *
import threading

class HelloWorldApp(QWidget):
    def __init__(self):
        super(HelloWorldApp, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(300, 300)
        self.setWindowTitle('Pinger')

        self.input_editor = QTextEdit(self)
        self.input_editor.setFixedSize(150, 200)
        self.input_editor.move(0, 75)

        self.output_editor = QTextEdit(self)
        self.output_editor.setFixedSize(150, 200)
        self.output_editor.move(150, 75)

        self.prompt = QLabel(self)
        self.prompt.setText('List IP\'s there:')
        self.prompt.move(15, 60)

        self.buttonPing = QPushButton(self)
        self.buttonPing.move(105, 0)
        self.buttonPing.setFixedSize(40, 40)
        self.buttonPing.setText('Ping!')
        self.buttonPing.clicked.connect(self.ping)

        self.buttonFileDialog = QPushButton(self)
        self.buttonFileDialog.setFixedSize(80, 40)
        self.buttonFileDialog.setText('Output file')
        self.buttonFileDialog.clicked.connect(self.buttonPress)


        self.dialog = QFileDialog(self)

        self.show()

    def ping(self):
        text = self.input_editor.toPlainText()

        print(text)
        print('Checking IP\'s...')

        self.check_args(text)
        try:
           file = QFileDialog.getOpenFileName()
        except IOError as e:
            print(e)

        self.pinger(file, text)

    def check_args(self, text):
        if not text.strip():
            self.abort_prg('Input prompt is empty')

        print(text)
        ips = text.split()

        for cur_ip in ips:
            import re
            ip_expression = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
            if not(ip_expression.match(cur_ip)):
                print('Wrong ip: ' + cur_ip)
                self.abort_prg('Incorrect ip:', cur_ip)

    def pinger(self, file, args):
        file_lock = threading.Lock()
        threads = []
        for current_ip in args:
            threads.append(threading.Thread(target=self.ping_ip, args=(current_ip, file_lock, file)))
            threads[-1].start()

        for current_ip in threads:
            current_ip.join()

    def ping_ip(self, ip, file_lock, file):
        import subprocess
        result = subprocess.call(["ping", '-n', '1', ip], stdout = subprocess.PIPE)

        file_lock.acquire()
        try:
            if result == 0:
                file.write(ip + '\n')
        finally:
            file_lock.release()

    def abort_prg(self, err_msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('ERROR!')
        msgBox.setText(err_msg)
        msgBox.setInformativeText("Retry?")

        ret = msgBox.exec_()

def main():
    app = QApplication(sys.argv)
    ex = HelloWorldApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
