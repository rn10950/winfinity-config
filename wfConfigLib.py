'''
Winfinity-config core library
=============================
provides all core functions for the winfinity-config sysyem
'''
import configparser
import os
import pprint
import fileinput
import sys
import uuid
import shutil
import json
import errno
from pathlib import Path
from dotenv import load_dotenv
from tdeconfig import TDEConfig

	
# TY to tzot on stack overflow for below function:
def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:  # Python >= 2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise


#===================
# Main System Class
#===================
class Winfinity:
	def __init__(self):
		h = str(Path.home())
		self.userHome = h
		self.userWfDir = h + '/.winfinity'
		self.wfConfDir = self.userWfDir + '/config'
		self.tdeConfDir = h + '/.trinity/share/config'
		self.sourceDir = os.path.dirname(os.path.realpath(__file__))
		
		# Winfinity color themes
		self.themeDir = self.userWfDir + '/themes'
		self.themeJson = self.themeDir + '/themes.json'
		if not os.path.exists(self.themeJson):
			mkdir_p(self.themeDir)
			shutil.copyfile(self.sourceDir + '/default/themes.json', self.themeDir + '/themes.json')
		
		# set up GTK themes
		self.gtkThemeDir = h + '/.themes/Redmond9x'
		if not os.path.exists(self.gtkThemeDir):
			try:
				shutil.copytree('/usr/share/themes/Redmond9x', self.gtkThemeDir)
			except Exception:
				# copy failed, placeholder for later, do nothing for now
				pass
		# make config directory if does not exist
		if not os.path.exists(self.wfConfDir):
			mkdir_p(self.wfConfDir)
		
		# initialize TDEConfig object for config management
		self.tdeConfig = TDEConfig(self.tdeConfDir)
		
		# locate winfinity-vars, set
		defRootWV = Path("/opt/winfinity/winfinity-vars")
		defHomeWV = Path.home() / ".winfinity/winfinity-vars"
		if defRootWV.is_file():
			self.winfinityVars = str(defRootWV)
		elif defHomeWV.is_file():
			self.winfinityVars = str(defHomeWV)
		else:
			self.winfinityVars = None
		load_dotenv(dotenv_path=self.winfinityVars)
		
		# set vars from winfinity-vars
		self.winfinityVerbose = os.getenv("winfinityVerbose")
		self.winfinityDevTools = os.getenv("WINF_DEV_TOOLS")
