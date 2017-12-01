# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 10:13:38 2017

@author: Jules
"""

from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = "D:\\WinPython-64bit-3.5.3.1Qt5\\python-3.5.3.amd64\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "D:\\WinPython-64bit-3.5.3.1Qt5\\python-3.5.3.amd64\\tcl\\tk8.6"

base = None


executables = [Executable("Iguana.py", base=base, icon = "C:\\Users\\Jules\\Desktop\\pappl-master\\Iguane.ico")]

packages = ['PyQt5.QtWidgets','PyQt5.QtGui','PyQt5.QtCore','sys','os','py2cytoscape.data.cyrest_client','psutil','networkx','numpy','igraph']
files = ['optimizationComponent.lp','clingo.exe','interface_ui.py','componentIdentification.py','processASP.py', 'Iguane.ico']
options = {
    'build_exe': {
        'packages':packages,
        "include_files": files,
    },

}

setup(
    name = "Iguana",
    options = options,
    version = "2.4",
    description = 'Iguana (feat. iggy-POC)',
    executables = executables
)
