#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function

import argparse
import eyed3
import os
import string
import shutil
import re


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        __doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("file", nargs='+',
                        help="files to read the tags from")
    args = parser.parse_args()
    album_template = u"BWV {0:04d} (cantata)"
    inchars = "ФБД"
    outchars = "öüä"
    table = string.maketrans(inchars, outchars)
    ss = "с"
    bwv_re = "BWV ([0-9]{1,4})"
    compiled_re = re.compile(bwv_re)
    last_known_bwv_number = 0
    for mp3file_name in args.file:
        if not ".mp3" in mp3file_name:
            continue
        new_name = mp3file_name.translate(table)
        new_name = new_name.replace(ss, "ss")
        os.rename(mp3file_name, new_name)
        mp3file = eyed3.load(new_name.decode("utf-8"))
        title = mp3file.tag.title
        match = re.search(compiled_re, title)
        if not match:
            match = re.search(compiled_re, new_name)
        if not match:
            bwv_number = last_known_bwv_number
        else:
            bwv_number = int(match.group(1))
            last_known_bwv_number = bwv_number
        mp3file.tag.album = album_template.format(bwv_number)
        mp3file.tag.save()
