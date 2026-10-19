#!/bin/bash

if [ $SUDO_USER ]; then user=$SUDO_USER; else user=`whoami`; fi

# user-configurable variables
kdeGlobals="/home/$user/.trinity/share/config/kdeglobals"
defaultGtk3CssFile="/usr/share/themes/Redmond9x/gtk-3.0/gtk-main.css"
defaultGtk32CssFile="/usr/share/themes/Redmond9x/gtk-3.20/gtk-main.css"


#
# ===================================== functions =====================================
#
# Source for color fns: https://github.com/majjoha/color-converter/blob/master/color-converter

# Check that a value is in range 0-255.
valueInRange() {
  if [[ $1 =~ ^([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])$ ]]; then
    return 0
  else
    return 1
  fi
}

# Convert a color in RGB to a hexadecimal value.
rgbToHex() {
  if valueInRange $1 && valueInRange $2 && valueInRange $3; then
    local tst=$(printf "rgb($1, $2, $3) -> #%02X%02X%02X" $1 $2 $3 | cut -d' ' -f 5)
	echo $tst
  else
    rangeError
  fi
}
inputError() {
  echo "Bad input format. You should apply an argument like ff0000 or 255 255 0."
  exit 1
}

rangeError() {
  echo "Range input error. The input provided was out of range."
  exit 1
}

# extract RGB colors fn

getColors() {
	local rgbVals=$(echo $1 | cut -d'=' -f 2 | tr ',' ' ')
	rgbToHex $rgbVals
}


#
# ===================================================================================
#


# Check to see if required args are set

if [ "$#" -lt "8" ] && [ "$1" != "use-tde" ]
then
	echo "GTK3 Redmond Color Switcher"
	echo 'Command: gtk3-colors.sh "path to gtk-main.css" "background" "foreground" "window base" "text" "highlight bg" "highlight text" "tooltip bg"'
	echo "Color values must be enclosed in double quotes and can be any valid CSS color value, include the hash for hex values"
	exit 1;
fi

if [ "$1" = "use-tde" ]
then
	# use TDE system colors	
	bgClr=$(cat $kdeGlobals | grep "background")
	clr2=$(getColors $bgClr)

	fgClr=$(cat $kdeGlobals | grep "windowForeground")
	clr3=$(getColors $fgClr)

	wbgClr=$(cat $kdeGlobals | grep "windowBackground")
	clr4=$(getColors $wbgClr)

	txtClr=$(cat $kdeGlobals | grep "windowForeground")
	clr5=$(getColors $txtClr)

	selBgClr=$(cat $kdeGlobals | grep "selectBackground")
	clr6=$(getColors $selBgClr)

	selFgClr=$(cat $kdeGlobals | grep "selectForeground")
	clr7=$(getColors $selFgClr)

	clr8="#FFFFBF"
	
	declare -a gtkFiles=("$defaultGtk3CssFile" "$defaultGtk32CssFile")
fi

if [ "$#" -eq "8" ]
then
	# use colors and gtk-main.css passed on command line
	declare -a gtkFiles=("$1")
	clr2=$2
	clr3=$3
	clr4=$4
	clr5=$5
	clr6=$6
	clr7=$7
	clr8=$8
fi


# set vars
tbg="@define-color theme_bg_color $clr2;"
tfg="@define-color theme_fg_color $clr3;"
twinBase="@define-color theme_base_color $clr4;"
ttext="@define-color theme_text_color $clr5;"
tselectedBg="@define-color theme_selected_bg_color $clr6;"
tselectedFg="@define-color theme_selected_fg_color $clr7;"
ttooltip="@define-color theme_tooltip_bg_color $clr8;"

bg="@define-color bg_color $clr2;"
fg="@define-color fg_color $clr3;"
winBase="@define-color base_color $clr4;"
text="@define-color text_color $clr5;"
selectedBg="@define-color selected_bg_color $clr6;"
selectedFg="@define-color selected_fg_color $clr7;"
tooltip="@define-color tooltip_bg_color $clr8;"
insInnerBox="@define-color insensitive_inner_box $clr2;"

# set vars
#~ echo "@define-color theme_bg_color $clr2;"
#~ echo "@define-color theme_fg_color $clr3;"
#~ echo "@define-color theme_base_color $clr4;"
#~ echo "@define-color theme_text_color $clr5;"
#~ echo "@define-color theme_selected_bg_color $clr6;"
#~ echo "@define-color theme_selected_fg_color $clr7;"
#~ echo "@define-color theme_tooltip_bg_color $clr8;"
#~ echo "@define-color insensitive_inner_box $clr2;"

# replace lines
for gtkFile in "${gtkFiles[@]}"
do
	echo $gtkFile
	sed -i "/define-color bg_color/c\\$bg" $gtkFile
	sed -i "/define-color fg_color/c\\$fg" $gtkFile
	sed -i "/define-color base_color/c\\$winBase" $gtkFile
	sed -i "/define-color text_color/c\\$text" $gtkFile
	sed -i "/define-color selected_bg_color/c\\$selectedBg" $gtkFile
	sed -i "/define-color selected_fg_color/c\\$selectedFg" $gtkFile
	sed -i "/define-color tooltip_bg_color/c\\$tooltip" $gtkFile
	sed -i "/define-color insensitive_inner_box/c\\$insInnerBox" $gtkFile
	
	sed -i "/define-color theme_bg_color/c\\$tbg" $gtkFile
	sed -i "/define-color theme_fg_color/c\\$tfg" $gtkFile
	sed -i "/define-color theme_base_color/c\\$twinBase" $gtkFile
	sed -i "/define-color theme_text_color/c\\$ttext" $gtkFile
	sed -i "/define-color theme_selected_bg_color/c\\$tselectedBg" $gtkFile
	sed -i "/define-color theme_selected_fg_color/c\\$tselectedFg" $gtkFile
	sed -i "/define-color theme_tooltip_bg_color/c\\$ttooltip" $gtkFile
done

# Win95 colors: ./gtk3-colors.sh /usr/share/themes/Redmond9x/gtk-3.0/gtk-main.css "#c3c3c3" "#000000" "#FFFFFF" "#000000" "#000082" "#FFFFFF" "#FFFFBF"