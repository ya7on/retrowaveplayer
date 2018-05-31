import requests
import vlc
from random import randint
from datetime import timedelta
from sys import stdout

class RetroWaveRadio:
    current_track = {}
    playlist = []

    def __init__(self):
        self.playlist = self._getPlayList()

        self.INSTANCE = vlc.Instance(['-q'])
        self.PLAYER = self.INSTANCE.media_player_new()

        while self.playlist:
            if self.PLAYER.get_position() in (1.0, -1.0):
                stdout.write("\r%s\n" % self.output() )
                self.newTrack()
                continue
            stdout.write("\rNOW PLAYING: %s" % self.output() )
    
    def newTrack(self):
        """turns on next track"""
        self.current_track = self._randomTrack()
        self.MEDIA = self.INSTANCE.media_new('http://retrowave.ru' + self.current_track['streamUrl'])
        self.MEDIA.get_mrl()
        self.PLAYER.set_media(self.MEDIA)
        self.PLAYER.play()
    def output(self):
        """formatting output"""
        if not self.current_track:
            return "\033[31mS T A R T I N G\033[0m"
        return "#%s %s \033[45m%s\033[0m" % (
            self.current_track['id'][:10],
            self._getTime(),
            self.current_track['title']
            )

    def _getTime(self):
        """formatting time"""
        while not self.PLAYER.get_length():
            continue
        length = int( self.PLAYER.get_length() / 1000 )
        now_time = int( self.PLAYER.get_position() * length )
        length = timedelta( seconds = length )
        now_time = timedelta( seconds = now_time )
        return "%s / %s" % (now_time, length)
    def _randomTrack(self, delete=True):
        """Returns random track from playlist"""
        i = randint( 0 , len(self.playlist) )
        track = self.playlist[ i ]
        if delete:
            del self.playlist[ i ]
        return track
    def _getPlayList(self):
        """Returns playlist"""
        r = requests.get('http://retrowave.ru/api/v1/tracks?limit=400')
        return r.json()['body']['tracks']

RetroWaveRadio()