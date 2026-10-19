# This file installs the inital config for the new user profile
# must be start from within the winfinity install system
from tdeconfig import TDEConfig
import sys
import json

def getVars():
	v = sys.stdin.read()
	return json.loads(v)

vars = getVars()
mD = vars['mD']
configPath = vars['configPath']

tdeConf = TDEConfig(configPath)
tdeConf.importYamlFromFile(mD + "/winfinity-config/configs/full-default-config.yml")