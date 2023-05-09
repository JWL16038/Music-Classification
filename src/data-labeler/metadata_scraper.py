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

# Extracts metadata information from the audio file
def extract_metadata(file_path):
    with open(file_path) as f:
        audiofile = eyed3.load(file_path)
    title = audiofile.tag.title
    artist = audiofile.tag.artist
    album = audiofile.tag.album
    return title, artist, album 

# Process all files and to the file list
def processfiles():
    file_paths = []
    audio_files = []
    for file_path in full_path.glob("**/*"):
        if file_path.suffix.lower() in audio_extensions:
            file_paths.append(file_path)

    print(f"Total number of files: {len(file_paths)}")
    for file in file_paths:
        title, artist, album = extract_metadata(file)
        audio_files.append((MusicFile(title, artist, album)))
    return audio_files