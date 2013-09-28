#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import re
import os


MP3_REGEX = \
    r'^(?P<author>.+?)-(?P<album>.+?)-(?P<track>\d+)-(?P<song>.+?\.mp3)$'


def indievox_renamer(music_dir):
    def make_mp3files(filenames):
        def match(file):
            return re.match(MP3_REGEX, unicode(filename, 'utf-8'),
                            flags=re.UNICODE)
        return [(match(filename), filename)
                for filename in filenames if match(filename)]

    def make_mp3data(mp3files):
        mp3data = {}
        for mp3file, filename in mp3files:
            author, album, track, song = (mp3file.group('author'),
                                          mp3file.group('album'),
                                          int(mp3file.group('track')),
                                          mp3file.group('song'))

            mp3data.setdefault(author, {})
            mp3data[author].setdefault(album, [])
            mp3data[author][album].append((track, song, filename))

        return mp3data

    def rename(mp3data):
        def make_filename(song_info):
            return "%02d %s" % song_info[0:2]

        for (author, album_data) in mp3data.iteritems():
            for (album, song_infos) in album_data.iteritems():
                dirname = os.path.join(music_dir, author, album)

                if not os.path.exists(dirname):
                    os.makedirs(dirname)

                for song_info in song_infos:
                    filepath = song_info[2]
                    source = os.path.join(music_dir, filepath)
                    target = os.path.join(dirname, make_filename(song_info))

                    os.rename(source, target)

    mp3files = make_mp3files(os.listdir(music_dir))
    mp3data = make_mp3data(mp3files)
    rename(mp3data)


def main():
    parser = argparse.ArgumentParser(
        description='Rename Indievox MP3 files to iTunes style')
    parser.add_argument('directory',
                        help='indievox mp3 directory', action='store')
    args = parser.parse_args()

    indievox_renamer(args.directory)


if __name__ == '__main__':
    main()
