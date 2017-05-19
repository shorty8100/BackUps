import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os", "SMComm", "PIL", "moviepy.editor", "imageio", "cherrypy", "BaseHTTPServer"], "excludes": ["tkinter"]}

setup( name = "S-HTML",
		version = "0.1",
		description = "S-Monitor HTML Server",
		options = {"build_exe": build_exe_options},
		executables = [Executable("HTMLonFLY.py", base = "Win32GUI")])
