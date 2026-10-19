##########

# TDEConfig: a python class to work with TDE config files
# 
# Main class init takes a root-relative path for your TDE config directory
#
# TDEConfig (self):
#     logBrokenFiles BOOL - set logBrokenFiles to true to output a list of unreadable config files
#                           Class is set to fail silently as there are typically a few non-ini files
#                           in the TDE config dir
#     confDir STR - The root-relative directory path passed to the class on init
#     configs DICT - A dictionary of ConfigParser objects indexed to the filename (str)
#     configsDict DICT - A multidimensional dictionary storing all config settings as strings
#         {'file1': {'section1': {'key1': 'value1',
#                                'key2': 'value2'},
#                   'section2': {'key1': 'value1',
#                               'key2': 'value2'}},
#	      'file2': {'section1': {'key1': 'value1',
#                                'key2': 'value2'},
#                   'section2': {'key1': 'value1',
#                               'key2': 'value2'}}}
#     
# Functions:
#     loadYAML(filename) STR: loads a YAML file to apply changes to config directory, returns a 
#                             multidimensional dict. returns False if error.
#     applyDict(changes) DICT: applies all the changes in the dict to the loaded config directory
#     getValue(filename, section, key): returns a string with the value of the preference. Returns None if error
#     setValue(filename, section, key, value): sets the value of the preference. Returns None if error
import configparser
import os
from os import listdir
from os.path import isfile, join
import yaml

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

# Main TDEConfig class
class TDEConfig:
	def __init__(self, confDir, logBrokenFiles=False):
		self.logBrokenFiles = logBrokenFiles
		self.confDir = confDir
		self.configs = self.getConfig(confDir)
		self.configsDict = self.getConfigsDict(self.configs)
		self.logBrokenFiles = logBrokenFiles

	# get config files as a dict of ConfigParser objects
	def getConfig(self, confDir):
		# get list of config files in config dir
		try:
			files = [os.path.join(confDir, f) for f in os.listdir(confDir) if 
			os.path.isfile(os.path.join(confDir, f))]
		except:
			# directory does not exist or is empty, return empty dict
			return {};
		
		configs = {}
		brokenFiles = []
		for f in files:
			p = GrumpyConfigParser(interpolation=None)
			p.optionxform = str
			try:
				p.read(f)
			except:
				brokenFiles.append(f)
				continue
			name = f.split('/')[-1]
			configs.update({name: p})
		if self.logBrokenFiles and len(brokenFiles) > 0:
			with open(self.logBrokenFiles, "w") as logFile:
				for i in brokenFiles:
					logFile.write(i + "\n")
		return configs
	
	# get recursive dictionary of config settings
	def getConfigsDict(self, configs):
		files = {}
		for f in configs:
			sections = {}
			for s in configs[f].sections():
				items = configs[f].items(s)
				sections.update({s: dict(items)})
			files.update({f: sections})
		return files
	
	def reloadConfigsDict(self):
		self.configs = self.getConfig(self.confDir)
		self.configsDict = self.getConfigsDict(self.configs)
		
	# load yaml from file, returns false if improper syntax
	def loadYaml(self, fN):
		try:
			with open(fN, 'r') as f:
				y = yaml.safe_load(f)
			return y
		except yaml.YAMLError:
			return False
	
	# export configuration to yaml
	def exportYaml(self, oF):
		self.reloadConfigsDict()
		configsDict = self.configsDict
		with open(oF, 'w') as outfile:
			yaml.dump(configsDict, outfile, default_flow_style=False)
			
	# apply yaml directly from file
	def importYamlFromFile(self, yamlFile):
		y = self.loadYaml(yamlFile)
		self.applyDict(y)

	# applies a dict of new settings to the dict of ConfigParser objects, writes to disk
	def applyDict(self, changes):
		for f in changes:
			try:
				c = self.configs[f]
				for s in changes[f]:
					for k in changes[f][s]:
						self.setValue(f, s, k, changes[f][s][k], True) # delay write until all file ops are done
				with open(self.confDir + '/' + f, "w") as file:
					c.write(file)
				self.reloadConfigsDict()
			except KeyError:
				#no file
				os.makedirs(self.confDir, exist_ok=True)
				i = 0
				for s in changes[f]:
					for k in changes[f][s]:
						#c.set(s, k, changes[f][s][k])
						if i == 0:
							self.newFile(f, s, k, changes[f][s][k], True) # delay write until all file ops are done
							i += 1
						else:
							self.setValue(f, s, k, changes[f][s][k], True) # delay write until all file ops are done
				c = self.configs[f]
				with open(self.confDir + '/' + f, "w") as file:
					c.write(file)
				self.reloadConfigsDict()

	
	# returns string of value of preference (or None if not set)
	def getValue(self, file, section, key):
		self.reloadConfigsDict()
		try:
			v = self.configsDict[file][section][key]
			return str(v)
		except:
			return None
	
	# sets preference
	def setValue(self, file, section, key, value, delayWrite=False):
		try:
			c = self.configs[file]
			c.set(section, key, value)
		except configparser.NoSectionError:
			c.add_section(section)
			c.set(section, key, value)
		except KeyError:
			self.newFile(file, section, key, value)
			return
		except:
			print('uncaught')
		if not delayWrite:
			with open(self.confDir + '/' + file, "w") as f:
					c.write(f)
			self.reloadConfigsDict()
	
	# new config file
	def newFile(self, file, section, key, value, delayWrite=False):
		p = GrumpyConfigParser(interpolation=None)
		p.optionxform = str
		p.add_section(section)
		p.set(section, key, value)
		self.configs.update({file: p})
		if not delayWrite:
			with open(self.confDir + '/' + file, "w") as f:
					p.write(f)
			self.reloadConfigsDict()

