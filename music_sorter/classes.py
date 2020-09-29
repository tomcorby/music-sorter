#!/usr/bin/env python3

import argparse
import common
import glob
import os
import shutil

from fuzzywuzzy import fuzz
from pathlib import Path
from pydub import AudioSegment


class Paths:
    def __init__(self, args):
        self.args = args
        self.scanned_paths = []

    def scan(self, path):
        paths = []

        for filename in glob.iglob(path + '**/**', recursive=True):
            if os.path.isfile(filename):
                paths.append([filename])

        self.scanned_paths = paths

        return paths

    def get_path_minus_read_dir(self, path):
        return Strings.remove_prefix(path, self.args.read)

    def get_path_minus_write_dir(self, path):
        return Strings.remove_prefix(path, self.args.write)

    # This feels really messy but it does what i need for now
    @staticmethod
    def split(path):
        split = os.path.split(path)
        splitext = os.path.splitext(split[-1])
        path_parts = split[0].split(os.path.sep)
        file_name = splitext[0]
        ext = splitext[-1]

        if not path_parts[0]:
            del path_parts[0]

        return {
            'path': path,
            'path_parts': path_parts,
            'filename': file_name,
            'extension': ext
        }


class Files:
    def __init__(self, args):
        self.args = args

    # move or copy or convert or symlink, depending on filetype and args passed in to __main__
    def manage(self, path):
        unprefixed_path = Strings.remove_prefix(path, self.args.read)
        split_path = Paths.split(path)
        new_path = self.args.write + os.path.sep + unprefixed_path

        if self.args.practise:
            print('Creating directory', Strings.remove_suffix(new_path, split_path['filename'] + split_path['extension']))
        else:
            Path(Strings.remove_suffix(new_path, split_path['filename'] + split_path['extension'])).mkdir(parents=True, exist_ok=True)

        if split_path['extension'].lower() == '.wav' and self.args.convert == True and self.args.manage != 'symlink':
            new_path = Strings.remove_suffix(new_path, '.wav') + '.flac'

            return self.flac_to_wav(existing_path=path, new_path=new_path)
        elif self.args.manage == 'copy':
            return self.copy(existing_path=path, new_path=new_path)
        elif self.args.manage == 'move':
            return self.move(existing_path=path, new_path=new_path)
        elif self.args.manage == 'symlink':
            return self.symlink(existing_path=path, new_path=new_path)

    def move(self, existing_path, new_path):
        if self.args.practise:
            print('Moving', existing_path, 'to', new_path)
            return new_path
        else:
            return shutil.move(existing_path, new_path)

    def copy(self, existing_path, new_path):
        if self.args.practise:
            print('Copying', existing_path, 'to', new_path)
            return new_path
        else:
            return shutil.copy(existing_path, new_path)

    def flac_to_wav(self, existing_path, new_path):
        if self.args.practise:
            if self.args.manage == 'copy':
                print('Converting', existing_path, 'to', new_path, 'and keeping original')
            elif self.args.manage == 'move':
                print('Converting', existing_path, 'to', new_path, 'and removing original')
            return new_path
        else:
            song = AudioSegment.from_wav(existing_path)
            song.export(new_path, format = "flac")

            if self.args.manage == 'move':
                # @todo: remove original file
                print('remove original file')

            return new_path

    # @todo: once symlinks are created in original dir structure, we can sort the symlinks to save time,
    #           then convert the symlinks to real files with cp --remove-destination "$(readlink <symlink>)" <symlink>
    def symlink(self, existing_path, new_path):
        if self.args.practise:
            print('Creating symlink pointing to', existing_path, 'from', new_path)
            return new_path
        else:
            os.symlink(existing_path, new_path)
            return new_path

    def tag(self, path, tags):
        # @todo: pass tags in. add either mp3 or flac tags depending on path extension
        return 0


class Strings:
    @staticmethod
    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    @staticmethod
    def remove_prefix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text

    @staticmethod
    def remove_suffix(text, suffix):
        if text.endswith(suffix):
            return text[:-len(suffix):]
        return text

    @staticmethod
    def fuzzy_match(a, b):
        return fuzz.ratio(a.lower(), b.lower())