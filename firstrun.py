import os
import yaml
import shutil
from pathlib import Path
from pprint import pprint
from wfConfigLib import *


apply = True
appApply = True

# pretty print data structures for debugging
showPPrint = False


def loadYaml(fN):
	try:
		with open(fN, 'r') as f:
			y = yaml.safe_load(f)
		return y
	except yaml.YAMLError:
			return False

# copies files/dirs in files_dir onto $HOME: files_dir/exam.ple -> $HOME/exam.ple
def copyFilesToHome(files_dir: str):
	source_root = Path(files_dir).resolve()
	home_root = Path.home().resolve()
	if not source_root.is_dir():
		print(f"Error: Source directory '{source_root}' does not exist.")
		return
	for source_item in source_root.rglob("*"):
		if source_item.is_file():
			relative_path = source_item.relative_to(source_root)
			target_item = home_root / relative_path
			try:
				target_item.parent.mkdir(parents=True, exist_ok=True)
				shutil.copy2(source_item, target_item)	
			except PermissionError:
				print(f"Permission Error: Could not write to {target_item}. Check home directory permissions.")
			except Exception as e:
				print(f"Failed to copy {relative_path}: {e}")

# processes variables in files copied to home directory
#     - takes a string for a root-relative file path (/home/user/file.txt) 
#       and a dict of vars and values. {"$HOME": winfinity.userHome, etc}
def process_document_env_vars(file_path: str, replacements) -> None:
	try:
		with open(file_path, 'r', encoding='utf-8') as file:
			content = file.read()
		for target, replacement in replacements.items():
			content = content.replace(target, str(replacement))
		with open(file_path, 'w', encoding='utf-8') as file:
			file.write(content)
		#print(f"Successfully updated document: {file_path}")
	except FileNotFoundError:
		#print(f"Error: The file at '{file_path}' was not found.")
		return False
	except Exception as e:
		#print(f"An error occurred: {e}")
		return False


				
# initialize winfinity object, allow verbose output
winfinity = Winfinity()
if winfinity.winfinityVerbose:
	showPPrint = True

# define variables to replace in copied files if needed
wfEnvVars = {
	"$HOME": winfinity.userHome,
	"$WINF_USER_PREFIX": winfinity.userWfDir
}

# ======================= DEV TOOLS ====================
if winfinity.winfinityDevTools:
	devOptions = str(winfinity.sourceDir) + '/dev-tools.yml'
	with open(devOptions, "r") as f:
		data = yaml.safe_load(f)
		if data is not None:
			winfinity.tdeConfig.applyDict(data["changes"])
	
# ======================= OPTIONS ====================

# build list of options, use hardcoded dir for now
dN = winfinity.sourceDir + "/tde-options"
dP = Path(dN)
changeList = []
for file in dP.glob("*.yml"):
	with open(file, "r") as f:
		data = yaml.safe_load(f)
		if data is not None:
			changeList.append(data)

# pretty print dataset if enabled
if showPPrint:
	pprint.pprint(changeList)

# ===== manualy select changes for dev purposes =====
#changesToApply = []
#changesToApply = ["test"]
#changesToApply = ["test", "test2"]

# apply all changes until GUI is created
changesToApply = []
#changesToApply = ["dev-tools"] #install dev tools automatically

for c in changeList:
	changesToApply.append(c['id'])

for c in changeList:
	if c['id'] in changesToApply:
		if apply:
			winfinity.tdeConfig.applyDict(c["changes"])

# ======================= APPS ====================

appsDir = winfinity.sourceDir + "/appConfigs"
aDP = Path(appsDir)
appDict = {}

for path in aDP.iterdir():
	if path.is_dir():
		metaFile = path / "preset.yml"
		if metaFile.is_file():
			try:
				with open(metaFile, "r") as f:
					appData = yaml.safe_load(f) or {}
					appDict[path.name] = appData
			except yaml.YAMLError as exc:
				print(f"Error parsing YAML in {path.name}: {exc}")
			except Exception as e:
				print(f"Failed to read file in {path.name}: {e}")

# pretty print dataset if enabled
if showPPrint:
	pprint.pprint(appDict)


# ===== manualy select apps for dev purposes =====
#presetsToApply = []
#presetsToApply = ['test']

# apply all app presets until GUI is created
presetsToApply = []

for preset in appDict:
	presetsToApply.append(preset)

# use data['id'] for directory name instead of data['app'], 
#     data['app'] used to match different presets to same app
for preset, data in appDict.items():
	if preset in presetsToApply:
		filesDir = appsDir + '/' + preset + '/files'
		if appApply:
			copyFilesToHome(filesDir)
			# add any TDE config changes to config registry
			if data.get('changes') is not None:
				winfinity.tdeConfig.applyDict(data["changes"])
			if data.get('processFiles') is not None:
				for file in data['processFiles']:
					f = str(Path.home()) + file
					#print(str(f))
					process_document_env_vars(str(f), wfEnvVars)
				