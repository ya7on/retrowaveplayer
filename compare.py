"""
unloads tracks into music/ dir
"""

import requests
from urllib import parse
from os import path, mkdir

print(" S T A R T E D ")

if not path.exists('music'):
    mkdir('music')

i = 0
not_null = True
while not_null:
    r = requests.get( 'http://retrowave.ru/api/v1/tracks?limit=500&cursor=%s' % i )
    for track in r.json()['body']['tracks']:
        if track is None:
            not_null = False
            print('N o n e')
            continue
        filename = track['title'].replace('/', '')
        if path.exists("music/%s.mp3" % filename):
            print(">>>EXISTS<<<\t%s" % filename)
            continue
        print('request')
        r = requests.get("http://retrowave.ru%s" % track['streamUrl'])
        print('writing')
        try:
            f = open('music/%s.mp3' % filename, 'wb')
            f.write(r.content)
        except:
            f = open('music/%s.mp3' % parse.quote( filename ), 'wb')
            f.write(r.content)
        print(track['title'])