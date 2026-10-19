"""
Winfinity-CLI

Usage:
  winfinity-cli theme list
  winfinity-cli theme enable <themename>
  winfinity-cli theme install <themefile>
  winfinity-cli (-h | --help)
  winfinity-cli --version
  
Options:
  -h --help       Show this screen.
  --version       Show version.
  
Manual:
  winfinity-cli theme list:
    List all installed Winfinity themes
  winfinity-cli theme enable <themename>:
    Enable an installed theme
  winfinity-cli theme install <themefile>:
    Install a Microsoft .theme file

"""
from themeparser import *
from vendor.docopt import docopt
import sys

if __name__ == '__main__':
	a = docopt(__doc__, version='winfinity-cli 0.2 alpha')
	
	if a['theme']:
		#initialize themeparser
		themeParser = ThemeParser()
		themes = themeParser.getThemeList

			# continue parsing cli
			if a['install']:
				if a['<themefile>'] is not None:
					#install theme
					f = a['<themefile>']
					t = themeParser.parseMsTheme(f)
					themes[sanStr(t['displayName'])] = t
					themeParser.saveThemeList(themes)
					print('Theme has been installed. Run "winfinity-cli theme enable ' + sanStr(t['displayName']) + '" to enable your theme.')
				else:
					sys.exit("No theme file provided.")
			elif a['enable']:
				if a['<themename>'] is not None:
					#enable theme
					n = a['<themename>']
					themeParser.enableTheme(n)
					print('Theme ' + n + ' has been enabled. You must log out for all changes to be applied.')
				else:
					sys.exit('No theme name provided. Run "winfinity-cli theme list" to show installed themes.')
			elif a['list']:
				#list themes
				print('')
				print('Name:                 Display Name:')
				print('')
				for n, t in themes.items():
					print(n.ljust(22, '.') + t['displayName'])
				print('')