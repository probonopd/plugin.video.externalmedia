# plugin.video.externalmedia

Play media on KODI from external drives without the need for library updates nor databases. Displays metadata from files stored in the directories. Metadata can be added e.g., by using [tinyMediaManager](https://www.tinymediamanager.org/).

## Installation

While you could install the plugin through the KODI graphical user interface, it may be quicker to ssh into the box and do:

```
cd /storage/.kodi/addons/
wget -c https://github.com/probonopd/plugin.video.externalmedia/archive/master.zip -O plugin.video.externalmedia.zip
unzip plugin.video.externalmedia.zip
mv plugin.video.externalmedia-master plugin.video.externalmedia
killall kodi.bin
```
