# Winfinity-config
This is the submodule that contains the Winfinity config system. It also contains the DESK.CPL clone that allows you to apply Windows color themes to Winfinity apps. This is provided as a submodule to allow for easy updating after Winfinity installation. Winfinity-config is primarily written in Python and is intended to be distro independent given Winfinity is already installed.

## Updating a prior Winfinity installation
### If Winfinity is installed system-wide:
    sudo git -C /opt/winfinity/winfinity-config pull

## Known Bugs
- Qt5, Qt6, and GTK+ 4.x color support is not implemented
- Font support is not implemented

## Future Plans
- Look into possibly forking Chicago95's PLUS and adding TDE and GTK+ 4 support (in order to fix above bugs)
- Adding Windows XP themes once Winfinity does