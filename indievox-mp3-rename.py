#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import re
import os


MP3_REGEX = \
    r'^(?P<author>.+?)-(?P<album>.+?)-(?P<track>\d+)-(?P<song>.+?\.mp3)$'


class IndievoxSong(object):
    track = None
    song = None

    def __init__(self, track, song):
        self.track = track
        self.song = song

    def make_filename(self):
        return "%02d %s" % (int(self.track), self.song)


class IndievoxSongMeta(object):
    indievox_song = None
    author = None
    album = None
    filename = None

    def __init__(self, author, album, indievox_song, filename):
        self.author = author
        self.album = album
        self.indievox_song = indievox_song
        self.filename = filename

    @classmethod
    def match(cls, filename):
        return re.match(MP3_REGEX, unicode(filename, 'utf-8'),
                        flags=re.UNICODE)

    @classmethod
    def from_filename(cls, filename):
        mp3file = cls.match(filename)
        if not mp3file:
            return None

        author, album, track, song = (mp3file.group('author'),
                                      mp3file.group('album'),
                                      mp3file.group('track'),
                                      mp3file.group('song'))

        indievox_song = IndievoxSong(track, song)
        instance = cls(author, album, indievox_song, filename)

        return instance


def indievox_renamer(music_dir):
    def rename(mp3files):
        for mp3file in mp3files:
            dirname = os.path.join(music_dir, mp3file.author, mp3file.album)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            filename = mp3file.filename
            source = os.path.join(music_dir, filename)
            target = os.path.join(dirname,
                                  mp3file.indievox_song.make_filename())

            os.rename(source, target)

    mp3files = (IndievoxSongMeta.from_filename(filename)
                for filename in os.listdir(music_dir)
                if IndievoxSongMeta.from_filename(filename))
    rename(mp3files)


def main():
    parser = argparse.ArgumentParser(
        description='Rename Indievox MP3 files to iTunes style')
    parser.add_argument('directory',
                        help='indievox mp3 directory', action='store')
    args = parser.parse_args()

    indievox_renamer(args.directory)


if __name__ == '__main__':
    main()
