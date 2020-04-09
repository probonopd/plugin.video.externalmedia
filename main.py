# encoding=utf8

# Debug with
# cat /storage/.kodi/temp/kodi.log

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
from urllib import urlencode
from urlparse import parse_qsl

import xbmcgui
import xbmcplugin
import xml.etree.ElementTree

from glob import glob
import json
from datetime import datetime

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def list_videos(start_path):
    """
    Create the list of directories and/or playable videos in the Kodi interface.

    :param path: Directory path
    :type category: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, os.path.basename(start_path))
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')

        # list_item.setArt({'thumb': "http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg",
        #                  'icon': "http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg",
        #                  'fanart': "http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg"})
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        # Note: If title is too long without spaces, it is not shown, hence replacing underscores with spaces
        

    paths = glob(start_path+"/*")
    # paths = sorted(glob(start_path+"/*"), key=os.path.getmtime)
    paths.sort(key=os.path.basename)

    # Go through all the files in the current directory and either add them or don't add them
    # to the listing to be shown on the screen
    for path in paths:
        list_item = xbmcgui.ListItem(label=os.path.basename(path))

        do_not_show = False
        do_not_show_suffixes = [".jpg", ".nfo", ".png", ".srt", ".srt", ".txt"]
        for suffix in do_not_show_suffixes:
            if path.endswith(suffix) == True:
                do_not_show = True

        url=''
        if os.path.isdir(path):
            url = get_url(action='listing', path=path)
            is_folder = True

            # For TV series, interpret tvshow.nfo
            if os.path.exists(path + "/tvshow.nfo"):
                list_item = xbmcgui.ListItem(path)
                list_item.setProperty('IsPlayable', 'false')
                tree = xml.etree.ElementTree.parse(path + "/tvshow.nfo")
                root = tree.getroot()
                for tag in ["genre", "country", "year", "rating", "title", "plot", "studio"]:
                    plotelement = root.find(tag)
                    if(plotelement != None ):
    	                list_item.setInfo('video', {tag: plotelement.text})

            if os.path.exists(path + "/poster.jpg"):
                 list_item.setArt({'thumb': path + "/poster.jpg"})

            if os.path.basename(path).startswith("Season "):
                 episode = os.path.basename(path).replace("Season ", "").zfill(2)
                 if os.path.exists(os.path.dirname(path) + "/season" + episode + "-poster.jpg"):
                     list_item.setArt({'thumb': os.path.dirname(path) + "/season" + episode + "-poster.jpg"})

        else:
            url = get_url(action='play', path=path)
            list_item.setProperty('IsPlayable', 'true')
            is_folder = False

        # If the directory contains an nfo file with the same name as the video file but the nfo suffix,
        # use that to enrich the metadata for the corresponding video file
        if path.endswith(".mp4") or path.endswith(".avi") or path.endswith(".mkv"):
            nfo_file = ""
            if os.path.exists(os.path.splitext(path)[0]+".nfo"):
                nfo_file = os.path.splitext(path)[0]+".nfo"
            elif os.path.exists(os.path.dirname(path)+"/movie.nfo"):
                nfo_file = os.path.dirname(path)+"/movie.nfo"
            if nfo_file != "":
                list_item = xbmcgui.ListItem(path)
                list_item.setProperty('IsPlayable', 'true')
                tree = xml.etree.ElementTree.parse(nfo_file)
                root = tree.getroot()
                for tag in ["genre", "country", "year", "rating", "plot", "studio", "trailer", "mpaa", "outline", "tagline", "runtime"]:
                    plotelement = root.find(tag)
                    if(plotelement != None ):
    	                list_item.setInfo('video', {tag: plotelement.text})
            # If the directory contains an image with the same name as the video file but a different suffix,
            # use that to enrich the metadata for the corresponding video file. For whatever reason,
            # it seems like this needs to be done AFTER populating setInfo('video'...)
            for suffix in [".jpg", ".png", "-poster.jpg", "-thumb.jpg"]:
                found = glob(os.path.splitext(path)[0]+suffix)
                if len(found) > 0:
                    list_item.setArt({'thumb': found[0]})
                else:
                    # We have not found an image with the same name as the video file but a differet suffix,
                    # so take the first best image we can find in this directory
                    for suffix in [".jpg", ".png"]:
                        found = glob(os.path.basename(path)[0]+"/*" + suffix)
                        if len(found) > 0:
                            list_item.setArt({'thumb': found[0]})

        # Note: If title is too long without spaces, it is not shown, hence replacing underscores with spaces
        list_item.setInfo('video', {'title': os.path.basename(path).replace("_", " "),
                                    'mediatype': 'video'})
        
        #############################################################################
        # TODO: Insert an example for how to use custom metadata files        
        #############################################################################

        # Add this file to the listing if it is not one of the metadata files
        # that we already handled and do not want to show in the file browser
        if do_not_show == False:
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided path.
            list_videos(start_path=params['path'])
        elif params['action'] == 'play':
            # Play a video from a provided path.
            play_video(params['path'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display all mounted partitions, if multiple
        # or the one mounted partition, if only one
        mountpoint = "/var/media"
        mounted_disks = glob(mountpoint + "/*")
        if len(mounted_disks) == 1:
            mountpoint = mounted_disks[0]
        list_videos(mountpoint)


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
