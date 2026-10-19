#!/bin/bash

# must be run as the user wishing to install

# this script will delete the autorun file if present on each run
# copy cpanel-install.desktop to ~/.trinity/Autostart to re-enable

#color theme installer
mkdir -p "$HOME/.themes/Redmond9x/gtk-2.0/"
mkdir -p "$HOME/.themes/Redmond9x/gtk-3.0/"
mkdir -p "$HOME/.themes/Redmond9x/gtk-3.24/"
cp /usr/share/themes/Redmond9x/gtk-2.0/gtkrc "$HOME/.themes/Redmond9x/gtk-2.0/"
cp /usr/share/themes/Redmond9x/gtk-3.0/gtk.css "$HOME/.themes/Redmond9x/gtk-3.0/"
cp /usr/share/themes/Redmond9x/gtk-3.24/gtk.css "$HOME/.themes/Redmond9x/gtk-3.24/"
#mkdir -p "$TDE_USERPROFILE/.local/share/applications/"
#p ./cpanel.desktop $TDE_USERPROFILE/.local/share/applications/

rm -f "$HOME/.trinity/Autostart/cpanel-install.desktop"

# temporary testing line
echo "OK" > ~/CPANEL-AUTOSTART.txt