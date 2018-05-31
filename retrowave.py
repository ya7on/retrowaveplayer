import requests
import vlc
from random import randint
from datetime import timedelta, datetime
from sys import stdout
import os

class RetroWaveRadio:
    current_track = {}
    playlist = []

    def __init__(self):
        self.playlist = self._getPlayList()

        self.INSTANCE = vlc.Instance(['-q'])
        self.PLAYER = self.INSTANCE.media_player_new()

        print("\033[31mS T A R T I N G\033[0m")
        self.newTrack()
        while self.playlist:
            if round( self.PLAYER.get_position() , 3 ) >= 0.999:
                stdout.write( "\r%s" % ( " " * int( os.popen('stty size', 'r').read().split()[1] ) ) )
                stdout.write( "\r[%s]\033[104m%s\033[0m\n" % ( datetime.now().strftime('%x'), self.current_track['title'] ) )
                self.newTrack()
                continue
            stdout.write("\rNOW PLAYING:\t%s" % self.output() )
    
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
            return "\033[31mL O A D I N G\033[0m"
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
        i = randint( 0 , len(self.playlist) - 1 )
        track = self.playlist[ i ]
        if delete:
            del self.playlist[ i ]
        return track
    def _getPlayList(self):
        """Returns playlist"""
        r = requests.get('http://retrowave.ru/api/v1/tracks?limit=400')
        return r.json()['body']['tracks']

RetroWaveRadio()