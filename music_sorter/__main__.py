#!/usr/bin/python3

import click
import common
import dotenv
import os
import sys

from database import Database
from files import Files
from spotify import Spotify

dotenv.load_dotenv()

parser = common.MyParser()
parser.add_argument('--read', type=str, required=False, default=os.getenv('UNSORTED_MUSIC_DIR'),
                    help='Path to parse. Overrides UNSORTED_MUSIC_DIR in .env')
parser.add_argument('--write', type=str, required=False, default=os.getenv('SORTED_MUSIC_DIR'),
                    help='Where to save parsed music to. Overrides SORTED_MUSIC_DIR in .env')
parser.add_argument('--manage', type=str, required=False, default='copy', help='<move/copy/symlink> default:copy')
parser.add_argument('--convert', type=common.str2bool, nargs='?', const=True, default=True,
                    help='Convert WAV to FLAC while parsing. Other formats will be handled by the --manage flag')
parser.add_argument('--practise', type=common.str2bool, nargs='?', const=True, default=True,
                    help='Echo actions instead of doing them')
args = parser.parse_args()

# @todo: check .env file exists

if not args.read:
    parser.error('--read flag or UNSORTED_MUSIC_DIR in an .env file is required')
elif args.read == os.getenv('UNSORTED_MUSIC_DIR'):
    if click.confirm('Do you want to import from ' + args.read, default=False) is False:
        exit(1)

if not args.write:
    parser.error('--write flag or SORTED_MUSIC_DIR in an .env file is required')
elif args.write == os.getenv('SORTED_MUSIC_DIR'):
    if click.confirm('Do you want to export to ' + args.write, default=False) is False:
        sys.exit(1)

db = Database(args=args)
files = Files(args=args)
spotify = Spotify(args=args)

unsorted_music = files.scan(args.read)
insert_count = db.insert_unsorted_music(unsorted_music)

# @todo: check if song already exists in sorted music, if so, skip it
for unsortedSong in unsorted_music:
    old_path = unsortedSong[0]
    new_path = files.manage(old_path)
    extension = files.get_extension(new_path)
    search_term = files.get_filename(new_path)

    db.move_unsorted_to_sorted_db(old_path, new_path, extension)

    track = spotify.search_track(search_term)
    # @todo: tag file in new location

db.commit()
