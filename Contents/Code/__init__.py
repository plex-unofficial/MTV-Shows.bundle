#!/usr/bin/env python2.3
#
#  _MTVSHOWS__.py
#  
#


from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

MTV_PLUGIN_PREFIX   = "/video/MTVSHOWS"

MTV_ROOT            = "http://www.mtv.com"
MTV_SHOWS_LIST      = "http://www.mtv.com/ontv/"

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(MTV_PLUGIN_PREFIX, ShowList, "MTV Shows", "icon-default.png", "art-default.jpg")
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.art = R('art-default.jpg')
  MediaContainer.title1 = 'MTV Shows'
  DirectoryItem.thumb=R("icon-default.png")
  
####################################################################################################
def MainMenu():
    dir = MediaContainer(mediaType='video')
    dir.Append(Function(DirectoryItem(ShowList, "Full Episodes"), pageUrl = MTV_SHOWS_LIST, pageAppend = "video.jhtml?filter=fulleps"))
    #dir.Append(Function(DirectoryItem(ShowList, "Clips"), pageUrl = MTV_SHOWS_LIST, pageAppend = "video.jhtml?filter=clips"))
    #dir.Append(Function(DirectoryItem(ShowList, "Seasons"), pageUrl = MTV_SHOWS_LIST, pageAppend = "seasons.jhtml"))
    return dir

####################################################################################################
def MeatList(sender, pageUrl):
    dir = MediaContainer(title2=sender.itemTitle)
    list = XML.ElementFromURL(pageUrl, True).xpath('//meta[@name="mtvn_fullep_lnk"]')
    url = list[0].get('content')
    url = MTV_ROOT + url
    content = XML.ElementFromURL(url, True)
    c = 0
    for item in content.xpath('//ol[@id="vid_mod_1"]/li//li/a'):
    	image = MTV_ROOT + content.xpath(".//ol/li/ul/li[5]/img")[c].get('src')
        Log(image)
        c += 1
        link = MTV_ROOT + item.get('href')
        title = item.text
        dir.Append(WebVideoItem(link, title=title, thumb=image))
    return dir
	
####################################################################################################
def ShowList():
    dir = MediaContainer(mediaType='video')
    content = XML.ElementFromURL(MTV_SHOWS_LIST, isHTML=True)
    for test in content.xpath('//div[@class="mdl mdl-main"]//div[3]//li/div'):
    	for item in content.xpath('//div[@class="mdl mdl-main"]//div[3]//li/div/a'):
            link = MTV_ROOT + item.get('href')
            #link = link.replace("series.jhtml", "seasons.jhtml")
            Log(link)
            title = item.text
            if "seasons.jhtml" in link:
                dir.Append(Function(DirectoryItem(SeasonList, title), pageUrl = link))
                continue
            else:
                dir.Append(Function(DirectoryItem(MeatList, title), pageUrl = link))
 	return dir	
####################################################################################################
def SeasonList(sender, pageUrl):
    dir = MediaContainer(title2=sender.itemTitle)
    test = HTTP.Request(pageUrl)
    Log(test)
    content = XML.ElementFromURL(pageUrl, isHTML=True)
    for item in content.xpath('//div[@class="mdl "]/ol//li'):
        link = MTV_ROOT + item.xpath('.//a')[0].get('href')
        link = link.replace("series.jhtml", "video.jhtml?filter=fulleps")
        Log(link)
        title = item.xpath('.//a/text()[2]')[0]
        title = str(title)
        dir.Append(Function(DirectoryItem(MeatList, title), pageUrl = link))
    return dir