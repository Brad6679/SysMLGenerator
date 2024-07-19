import sys
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer
import json
import base64
import requests
import glob
import os
from openai import OpenAI
import time
from sysmlGPT import sysmlGPT
#from JupyterSandbox import JupyterSandbox
from jupyterBook import JupyterBook
import cairosvg

#from PyQt6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GPT UI")
        self.resize(300, 100)
        # Line edit with a parent widget
        self.sys = sysmlGPT('Default')

                
        self.txt = QLineEdit(self)
        #self.txt.setValidator(QIntValidator())
        #self.txt.setMaxLength(4)
        self.txt.setAlignment(Qt.AlignLeft)
        self.txt.setFont(QFont("Arial",12))
        self.txt.move(50, 75)
        self.txt.editingFinished.connect(self.enterPress)
        # Line edit with a parent widget and a default text
        layout = QVBoxLayout()
        layout.addWidget(self.txt)


        self.btn1 = QPushButton("Upload Image", self)
        self.btn1.move(50, 50)
        self.btn1.clicked.connect(self.getfile)
        
        layout.addWidget(self.btn1)
        


        self.setLayout(layout)

    def enterPress(self):
        # send gpt prompt by text
        out = self.sys.run(self.txt.text(), None)
        print(out)
        code = self.sys.extract_code_blocks(out)
        self.runCode(code)
        
        #print(text)

    def getfile(self):
      #self.img = True
      self.imgFname = QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"Image files (*.jpg *.gif)")
      #self.img = fname
      #print(self.imgFname[0])
      out = self.sys.run(None, self.imgFname[0])
      code = self.sys.extract_code_blocks(out)
      print(out)
      self.runCode(code)

    def runCode(self, code):
        book = JupyterBook()
        #sandbox = JupyterSandbox(kernel_name='sysml')
        #sandbox.start_kernel()
        pind = code.find("package")
        bind = code.find("{", pind)
        name = code[pind + len("package"):bind].strip()
        viz = f'%viz --view=tree {name}'
        
        #errors = sandbox.execute_both(code, viz)
        #errors = sandbox.execute_code(code)
        #sandbox.save_image(name=f'{name}.png')
        errors = book.runCode(code, viz)
        
        #sandbox.stop_kernel
        print(errors[0]['outputs'][0]['name'] + " " + errors[0]['outputs'][0]['text'])
        if len(errors) > 1:
            keys = errors[1]['outputs'][0]['data'].keys()
            if 'image/svg+xml' in keys:
                svg_content = errors[1]['outputs'][0]['data']['image/svg+xml']

            #print(svg_content)

                cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to='output/output.png')

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
