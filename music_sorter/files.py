#!/usr/bin/python3

import common
import glob
import os
import shutil

from pathlib import Path
from pydub import AudioSegment

class Files:
    def __init__(self, args):
        self.args = args


    def scan(self, path):
        paths = []

        for filename in glob.iglob(path + '**/**', recursive=True):
            if os.path.isfile(filename):
                paths.append([filename])

        self.scannedPaths = paths
        return paths


    # This feels really messy but it does what i need for now
    def split_path(self, path):
        split = os.path.split(path)
        splitext = os.path.splitext(split[-1])
        pathParts = split[0].split(os.path.sep)
        fileName = splitext[0]
        ext = splitext[-1]

        if not pathParts[0]:
            del pathParts[0]

        return {
            'path': path,
            'pathParts': pathParts,
            'filename': fileName,
            'extension': ext
        }


    def get_extension(self, pathOrFilename):
        return split_path(pathOrFilename)['extension']


    def get_filename(self, pathOrFilename):
        return split_path(pathOrFilename)['filename']


    def get_path_minus_read_dir(self, path):
        return common.remove_prefix(path, self.args.read)


    def get_path_minus_write_dir(self, path):
        return common.remove_prefix(path, self.args.write)


    # move or copy or convert or symlink, depending on filetype and args passed in to __main__
    def manage(self, path):
        unprefixedPath = common.remove_prefix(path, self.args.read)
        splitPath = self.split_path(unprefixedPath)
        newPath = self.args.write + os.path.sep + unprefixedPath

        if self.args.practise:
            print('Creating directory', common.remove_suffix(newPath, splitPath['filename'] + splitPath['extension']))
        else:
            Path(common.remove_suffix(newPath, splitPath['filename'] + splitPath['extension'])).mkdir(parents=True, exist_ok=True)


        if splitPath['extension'].lower() == '.wav' and self.args.convert == True and self.args.manage != 'symlink':
            newPath = common.remove_suffix(newPath, '.wav') + '.flac'

            return self.flac_to_wav(existingPath=path, newPath=newPath)
        elif (self.args.manage == 'copy'):
            return self.copy(existingPath=path, newPath=newPath)
        elif (self.args.manage == 'move'):
            return self.move(existingPath=path, newPath=newPath)
        elif (self.args.manage == 'symlink'):
            return self.symlink(existingPath=path, newPath=newPath)


    def move(self, existingPath, newPath):
        if self.args.practise:
            print('Moving', existingPath, 'to', newPath)
            return newPath
        else:
            return shutil.move(existingPath, newPath)


    def copy(self, existingPath, newPath):
        if self.args.practise:
            print('Copying', existingPath, 'to', newPath)
            return newPath
        else:
            return shutil.copy(existingPath, newPath)


    def flac_to_wav(self, existingPath, newPath):
        if self.args.practise:
            if self.args.manage == 'copy':
                print('Converting', existingPath, 'to', newPath, 'and keeping original')
            elif self.args.manage == 'move':
                print('Converting', existingPath, 'to', newPath, 'and removing original')
            return newPath
        else:
            song = AudioSegment.from_wav(existingPath)
            song.export(newPath, format = "flac")

            if self.args.manage == 'move':
                # @todo: remove original file
                print('remove original file')

            return newPath


    # @todo: once symlinks are created in original dir structure, we can sort the symlinks to save time,
    #           then convert the symlinks to real files with cp --remove-destination "$(readlink <symlink>)" <symlink>
    def symlink(self, existingPath, newPath):
        if self.args.practise:
            print('Creating symlink pointing to', existingPath, 'from', newPath)
            return newPath
        else:
            os.symlink(existingPath, newPath)
            return newPath

    def tag(self, path, tags):
        # @todo: pass tags in. add either mp3 or flac tags depending on path extension
        return 0

