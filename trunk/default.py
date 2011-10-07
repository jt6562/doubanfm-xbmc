# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,os,xbmcaddon
import DoubanFM



# Plugin constants 
__addonname__ = "豆瓣电台"
__addonid__ = "plugin.audio.DoubanFM"
__addon__ = xbmcaddon.Addon(id=__addonid__)

class MyPlayer(xbmc.Player):
    __url = ""
    def __init__(self):
        xbmc.Player.__init__(self)
        
    def onPlayBackEnded( self ):
        xbmc.sleep( 200 )
        print '*** CALLBACK: onPlayBackSEnded'
        PlayList(url)
        
    def onPlayBackStarted( self ):
        xbmc.sleep( 200 )
        tag = self.getMusicInfoTag()
        artist = tag.getArtist()
        title = tag.getTitle()

        print 'Playing: ' + artist + ' - ' + title
        

    def onPlayBackStopped( self ):
        xbmc.sleep( 2 )
        print '*** CALLBACK: onPlayBackStopped'
        PlayList(url)
        
def CATEGORIES():
    chs = DoubanFM.GetListChannel()
    for ch in chs:
        churl = DoubanFM.PlayListUrlPre+str(ch['channel_id'])
        addLink(ch['name'], churl, 1, '')

def PlayList(url):
    playlist=xbmc.PlayList(0) 
    playlist.clear()  
    songs = DoubanFM.GetListSongInfo(url)
    
    #add song to playlist
    num = 0
    for song in songs:
        listitem=xbmcgui.ListItem(song['title'])
        listitem.setInfo( type="Music", infoLabels={ "Title": song['title'], "Artist": song['artist']} )
        listitem.setThumbnailImage(song['pic'])
        playlist.add(song['url'], listitem)
        
    player = MyPlayer()
    print 'Added '+str(playlist.size()) + ' songs'
    
    player.play(playlist)
    while True:
        xbmc.sleep(3000)
   
             
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                    params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                    splitparams={}
                    splitparams=pairsofparams[i].split('=')
                    if (len(splitparams))==2:
                            param[splitparams[0]]=splitparams[1]
                            
    return param

def addLink(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=os.getcwd()+'\\Default.tbn', thumbnailImage=iconimage)
    liz.setInfo( type="Music", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
    return ok


params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Current select: "+"Mode: "+str(mode) + "  URL: "+str(url) + "  Name: "+str(name)

if mode==None:
        print "CATEGORIES()"
        CATEGORIES()

elif mode==1:
        print "PlayList()"
        PlayList(url) 

xbmcplugin.endOfDirectory(int(sys.argv[1]))
