# -*- coding: utf-8 -*-
import sys
import argparse
from ui_server import Ui_server 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Server import *

class MyWindow(QMainWindow,Ui_server):
    def __init__(self): 
        super(MyWindow,self).__init__()
        self.setupUi(self)
        self.pushButton_On_And_Off.clicked.connect(self.on_and_off_server)
        self.server=Server()
    def on_and_off_server(self):
        if self.pushButton_On_And_Off.text() == 'On':
            self.pushButton_On_And_Off.setText('Off')
            self.states.setText('On')
            self.server.turn_on_server()
            self.server.tcp_flag=True
            self.video=threading.Thread(target=self.server.transmission_video)
            self.video.start()
            self.instruction=threading.Thread(target=self.server.receive_instruction)
            self.instruction.start()
        else:
            self.pushButton_On_And_Off.setText('On')
            self.states.setText('Off')
            self.server.tcp_flag=False
            try:
                stop_thread(self.video)
                stop_thread(self.instruction)
            except Exception as e:
                print(e)
            self.server.turn_off_server()
            print("close")
    def closeEvent(self,event):
        try:
            stop_thread(self.video)
            stop_thread(self.instruction)
        except:
            pass
        try:
            self.server.server_socket.shutdown(2)
            self.server.server_socket1.shutdown(2)
            self.server.turn_off_server()
        except:
            pass
        QCoreApplication.instance().quit()
        os._exit(0)


def handle_server():
    try:
        server = Server()
        server.turn_on_server()
        server.tcp_flag=True
        video=threading.Thread(target=server.transmission_video)
        video.start()
        instruction=threading.Thread(target=server.receive_instruction)
        instruction.start()
    except KeyboardInterrupt:
        try:
            stop_thread(video)
            stop_thread(instruction)
        except Exception as e:
            print(e)
        server.turn_off_server()


def main(args):
    if args.gui:
        app = QApplication(sys.argv)
        myshow = MyWindow()
        myshow.show();  
        sys.exit(app.exec_())
    else:
        handle_server()

        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--gui", action="store_true", help="Start GUI")
    args = parser.parse_args()
    main(args)

