import os
import pandas as pd
import eyed3
import re
from pathlib import Path

absolute_path = Path().resolve().parent.parent
relative_path = Path('data/raw/classical_music_files')
full_path = absolute_path / relative_path

audio_extensions = [".mp3",".wav"]

# Class to record each file information
class MusicFile:
    def __init__(self,title,artist,album):
        self.title = title
        self.artist = artist
        self.album = album

    def gettitle():
        return self.title

    def getartist():
        return self.artist

    def getalbum():
        return self.album

def parse_longpath(path):
    """
    Converts the current path to a long path. Function was taken from here: https://stackoverflow.com/questions/55815617/pathlib-path-rglob-fails-on-long-file-paths-in-windows
    """
    normalized = os.fspath(path.resolve())
    if not normalized.startswith('\\\\?\\'):
        normalized = '\\\\?\\' + normalized
    return Path(normalized)

# Extracts metadata information from the audio file
def extract_metadata(file_path):
    try:
        combined_path = full_path / file_path
        modified_path = parse_longpath(combined_path)
        audiofile = eyed3.load(modified_path)
        tag = audiofile.tag
        return tag.title, tag.artist, tag.album 
    except OSError as e:
        return None, None, None

# Process all files and to the file list
def processfiles():
    file_paths = []
    audio_files = []
    for path in full_path.glob("**/*"):
        if path.suffix.lower() in audio_extensions:
            file_path = path.relative_to(full_path)
            file_paths.append(file_path)

    print(f"Total number of files: {len(file_paths)}")
    for file in file_paths:
        title, artist, album = extract_metadata(file)
        audio_files.append((MusicFile(title, artist, album)))
    return audio_files