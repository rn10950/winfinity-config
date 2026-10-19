import configparser
import os
import pprint
import fileinput
import sys
import uuid
import shutil
import json
import errno
from wfConfigLib import *


# TDE does not have spaces surrounding the "=" in the config files, patch ConfigParser
# TY to rchang on stack overflow for below class:
class GrumpyConfigParser(configparser.ConfigParser):
	#"""Virtually identical to the original method, but delimit keys and values with '=' instead of ' = '"""
	def write(self, fp):
		if self._defaults:
			fp.write("[%s]\n" % DEFAULTSECT)
			for (key, value) in self._defaults.items():
				fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
			fp.write("\n")
		for section in self._sections:
			fp.write("[%s]\n" % section)
			for (key, value) in self._sections[section].items():
				if key == "__name__":
					continue
				if (value is not None) or (self._optcre == self.OPTCRE):
					# This is the important departure from ConfigParser for what you are looking for
					key = "=".join((key, str(value).replace('\n', '\n\t')))
				fp.write("%s\n" % (key))
			fp.write("\n")


def sanStr(s):
	return ''.join(e for e in s if e.isalnum()).lower()

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
	
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# convert RGB tuple to string
def cT(t):
	return str(t)[1:-1]
# convert hex to RGB string
def cH(h):
	return str(hex_to_rgb(h))[1:-1]




#===================
# ThemeParser Class
#===================
class ThemeParser:
	def __init__(self):
		self.Winfinity = Winfinity()

	def getThemeList(self):
		conffile = self.Winfinity.themeJson
		if os.path.exists(conffile):
			f = open(conffile, 'r')
			l = json.load(f)
			f.close()
		else: # no theme config file, return empty dict
			l = dict()
			#l = []
		return l
	
	def saveThemeList(self, data):
		with open(self.Winfinity.themeJson, 'w') as w:
			json.dump(data, w, indent=4)
	
	def parseMsTheme(self, themefile):
		d = dict()
		c = dict()
		config = ConfigParser.ConfigParser()
		config.read(themefile)
		d['displayName'] = config.get("Theme", "DisplayName")
		for (k, v) in config.items("Control Panel\\Colors"):
			mT = tuple(map(int, v.split(' ')))
			c[k] = '#%02x%02x%02x' % mT
		d['colors'] = c
		return d
	
	def setGtk3Colors(self, colors, cssFile):
		sourceDir = self.Winfinity.sourceDir
		#"path to gtk-main.css" "background" "foreground" "window base" "text" "highlight bg" "highlight text" "tooltip bg"
		# win95 colors:          "#c3c3c3"    "#000000"     "#FFFFFF" "#000000"   "#000082"       "#FFFFFF"      "#FFFFBF"

		command = sourceDir + '/gtk3-colors.sh ' + cssFile + ' "' + \
			colors['buttonface'] + '" "' + \
			colors['buttontext'] + '" "' + \
			colors['window'] + '" "' + \
			colors['windowtext'] + '" "' + \
			colors['hilight'] + '" "' + \
			colors['hilighttext'] + '" "' + \
			colors['infowindow'] + '"'

		#print(command)
		os.system(command)
	
	def setGtk2Colors(self, c, gtk2dir):
		rcfile = gtk2dir + "/gtkrc"
		# gtk_color_scheme = "fg_color:#000000\nbg_color:#c0c0c0\nbase_color:#ffffff\ntext_color:#000000\nselected_bg_color:#000080\nselected_fg_color:#ffffff"
		s = 'gtk_color_scheme = "fg_color:' + c['buttontext'] + \
		'\\nbg_color:' + c['buttonface'] + \
		'\\nbase_color:' + c['window'] + \
		'\\ntext_color:' + c['windowtext'] + \
		'\\nselected_bg_color:' + c['hilight'] + \
		'\\nselected_fg_color:' + c['hilighttext'] + '"'
		tFN = str(uuid.uuid1())
		tF = open(gtk2dir + '/' + tFN, 'w')

		with open(rcfile, 'r') as oldFile:
			lines = oldFile.read().splitlines()

		oldFile.close()

		for line in lines:
			if line.strip().startswith('gtk_color_scheme'):
				line = s
			tF.write(line + '\n')
		tF.close()
		os.remove(rcfile)
		os.rename(gtk2dir + '/' + tFN, rcfile)

	def setTrinityColors(self, c):
		# General
		self.Winfinity.tdeConfig.setValue("kdeglobals", "General", "background", cH(c['buttonface']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "General", "buttonBackground", cH(c['buttonface']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "General", "buttonForeground", cH(c['buttontext']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "General", "foreground", cH(c['buttontext']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "General", "linkColor", cH(c['hottrackingcolor']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "General", "selectBackground", cH(c['hilight']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "General", "selectForeground", cH(c['hilighttext']), True)
		#self.Winfinity.tdeConfig.setValue("kdeglobals", "General", "visitedLinkColor", cH(c['hilighttext']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "General", "windowBackground", cH(c['window']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "General", "windowForeground", cH(c['windowtext']), True)
		# WM	
		self.Winfinity.tdeConfig.setValue("kdeglobals", "WM", "activeBackground", cH(c['activetitle']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "WM", "activeBlend", cH(c['gradientactivetitle']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "WM", "activeForeground", cH(c['titletext']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "WM", "activeTitleBtnBg", cH(c['buttonface']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "WM", "frame", cH(c['buttonface']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "WM", "handle", cH(c['buttonface']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "WM", "inactiveBackground", cH(c['inactivetitle']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "WM", "inactiveBlend", cH(c['gradientinactivetitle']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "WM", "inactiveForeground", cH(c['inactivetitletext']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "WM", "inactiveTitleBtnBg", cH(c['buttonface']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "WM", "inactiveFrame", cH(c['buttonface']), True)
		self.Winfinity.tdeConfig.setValue("kdeglobals", "WM", "inactiveHandle", cH(c['buttonface']))

		# kdesktoprc
		self.Winfinity.tdeConfig.setValue("kdesktoprc", "Desktop0", "Color1", cH(c['background']))

		# konquerorrc
		self.Winfinity.tdeConfig.setValue("konquerorrc", "Settings", "BgColor", cH(c['window']))

	def enableTheme(self, tN):
		tl = self.getThemeList()
		t = tl[tN]
		c = t['colors']
		self.setGtk2Colors(c, self.Winfinity.gtkThemeDir + '/gtk-2.0')
		self.setGtk3Colors(c, self.Winfinity.gtkThemeDir + '/gtk-3.0/gtk.css')
		self.setGtk3Colors(c, self.Winfinity.gtkThemeDir + '/gtk-3.24/gtk.css')
		self.setTrinityColors(c)
