#!/usr/bin/env python
import urllib2,urllib
import minjson as json
from urllib import FancyURLopener

__UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:6.0.2) Gecko/20100101 Firefox/6.0.2'
__ChannelUrl = 'http://www.douban.com/j/app/radio/channels'
PlayListUrlPre = 'http://douban.fm/j/mine/playlist?type=n&channel='

def GetListSongInfo(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', __UserAgent)
    response = urllib2.urlopen(req)
    
    SongCtx = response.read()
    response.close()

    SongJson = json.read(SongCtx)['song']

    ListSongInfo = []
    for song in SongJson:
        if 'rda' in song['url']:
            continue
        SongInfo = {'pic':song['picture'].replace('\\',''), 'album':song['albumtitle'], 'artist':song['artist'], 'url':song['url'].replace('\\',''), 'title':song['title']}
        ListSongInfo.append(SongInfo.copy())
    return ListSongInfo

def GetListChannel():
    url = __ChannelUrl
    req = urllib2.Request(url)
    req.add_header('User-Agent', __UserAgent)
    response = urllib2.urlopen(req)
    
    ChannelCtx = response.read()
    response.close()
    ChannelJson = json.read(ChannelCtx)['channels']

    ListChannelInfo = []
    for ch in ChannelJson:
        ChInfo = {'channel_id':str(ch['channel_id']), 'name':ch['name']}
        ListChannelInfo.append(ChInfo.copy())
    return ListChannelInfo

#chs = GetListChannel()
#for ch in chs:
#    print 'channel name:'+ch['name']
#    print 'channel id:'+ch['channel_id']

#list = GetListSongInfo(PlayListUrlPre+str('4'))
#for song in list:
#    print 'name:'+song['title']
#    print 'url:'+song['url']

#print len(list)
