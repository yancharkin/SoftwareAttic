# There is much better way to do what this script trying to do: [this fork of innoextact](https://github.com/immi101/innoextract/tree/gogextract). I'm not going to maintain this script anymore.

~~Script for unpacking new GOG installers (2018) that can't be unpacked with innoextact or innounp (yet?).~~

## ~~Installation~~
- ~~download script or [binaries build with pyinstaller](https://github.com/yancharkin/gogiunpack/releases/latest)~~
- ~~**for Linux:** download prebuild binary or build yourself and (*optionally*) install [this version of innoextract](https://github.com/yancharkin/innoextract/)~~
- ~~**for Windows:** download [innounp](http://innounp.sourceforge.net/)~~
- ~~put gogiunpack script/binary and innoextract/innounp in the same directory OR in $PATH~~

## ~~Usage~~
~~**python(.exe) gogiunpack.py**~~
~~or~~
~~**gogiunpack(.exe)** - try to unpack all installers in the same directory as gogiunpack (script assumes that every file that contains "setup_" and ".exe" in their name is installer)~~


~~**python(.exe) gogiunpack.py (path to installer) (destination directory)**~~
~~or~~
~~**gogiunpack(.exe) (path to installer) (destination directory)** - unpack specified installer to specified direcotory~~
