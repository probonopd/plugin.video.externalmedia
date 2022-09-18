# plugin.video.externalmedia

Play media on KODI from external drives without the need for library updates nor databases. Displays metadata from files stored in the directories. Metadata can be added e.g., by using [tinyMediaManager](https://www.tinymediamanager.org/).

## Installation (Kodi 19 and later: Python 3)

While you could install the plugin through the KODI graphical user interface, it may be quicker to ssh into the box and do:

```
cd /storage/.kodi/addons/
wget -c https://github.com/probonopd/plugin.video.externalmedia/archive/refs/heads/python3.zip -O plugin.video.externalmedia.zip
unzip plugin.video.externalmedia.zip
mv plugin.video.externalmedia-python3/ plugin.video.externalmedia

# Restart Kodi

# In the Kodi GUI, ensure that all dependencies are installed (especially `future`)
```
