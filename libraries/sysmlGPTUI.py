import sys
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer
import json
import os
from openai import OpenAI
import time
from sysmlGPT import sysmlGPT
from jupyterBook import JupyterBook
import cairosvg
import cv2

"""
Frontend UI Class
"""
class MainWindow(QWidget):
    """ 
      Initializes MainWindow Object to enable user interaction with backend
    """
    def __init__(self, parent=None):
                
        super().__init__(parent)
        self.setWindowTitle("GPT UI")
        self.resize(300, 100)
        self.sys = sysmlGPT('Default')

                
        self.txt = QLineEdit(self)
        self.txt.setAlignment(Qt.AlignLeft)
        self.txt.setFont(QFont("Arial",12))
        self.txt.move(50, 75)
        self.txt.editingFinished.connect(self.enterPress)

        layout = QVBoxLayout()
        layout.addWidget(self.txt)


        self.btn1 = QPushButton("Upload Image", self)
        self.btn1.move(50, 50)
        self.btn1.clicked.connect(self.getfile)
        
        layout.addWidget(self.btn1)
        


        self.setLayout(layout)
    """ 
      Function mapped to text box, runs when user presses enter on their query.
      Sends text request to GPT.
    """
    def enterPress(self):
        # send gpt prompt by text
        self.sys = sysmlGPT('Default')
        out = self.sys.run(self.txt.text(), None)
        print(out)
        code = self.sys.extract_code_blocks(out)
        self.runCode(code)
        
        #print(text)

    """ 
      Function mapped to file input button, runs when user selects an image as a query.
      Sends image request to GPT.
    """
    def getfile(self):

      self.imgFname = QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"Image files (*.jpg *.gif)")
      self.sys = sysmlGPT('Image')
      out = self.sys.run(None, self.imgFname[0])
      code = self.sys.extract_code_blocks(out)
      print(out)
      if len(code) > 0:
          self.runCode(code)
      else:
          print("ERROR: GPT did not output parseable code or did not output any code at all")
      
    """ 
      Interfaces with JupyterBook to run code and retrieve output.

      code : str
          SysMLv2 code to run
    """
    def runCode(self, code):
        book = JupyterBook()
        #print(code)
        if len(code) == 0:
            print("Unable to parse GPT output. Try again")
            return
        pind = code.find("package")
        bind = code.find("{", pind)
        name = code[pind + len("package"):bind].strip()
        viz = f'%viz --view=tree {name}'

        errors = book.runCode(code, viz)
        if 'name' in errors[0]['outputs'][0].keys():
            print(errors[0]['outputs'][0]['name'] + " " + errors[0]['outputs'][0]['text'])

        if len(errors) > 1:
            keys = errors[1]['outputs'][0]['data'].keys()
            if 'image/svg+xml' in keys:
                svg_content = errors[1]['outputs'][0]['data']['image/svg+xml']

            #print(svg_content)

                cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to='output/output.png')
                cv2.imshow("GPT Diagram Output", cv2.imread('output/output.png'))
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
