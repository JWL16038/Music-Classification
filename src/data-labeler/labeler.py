import os
import pandas as pd
import re
from pathlib import Path
from metadata_scraper import processfiles

composer_pattern = r"Mozart|Beethoven|Bach|Ravel"
composition_pattern = r"Piano|Sonata|Concerto|Violin|Oboe|Flute|Bassoon|String|Quartet|Quintet|Symphony|Trio|Fugue|Variations|Overture"
worknumber_pattern = r"K.\s*\d+|Op.\s*\d+|No.\s*\d+"
key_pattern = r"\b[A-G]\b(?:-Flat|\sFlat|b|-Sharp|\sSharp|#)?(?:\sMajor|\sMinor)?"

def extract_composer(file):
    """
    Extracts composer information from the artist entry

    """
    # Get all possible entires from the file to search for the composer.
    entires = [file.artist,file.title,file.album]
    for entry in entires:
        composer_result = re.search(composer_pattern, entry, re.IGNORECASE)
        if composer_result is not None:
            return composer_result.group(0).lower().capitalize()
    print("No composer found")
    return None

def extract_composition(title):
    """
    Extracts the composition and the work number from the title entry

    """
    #Join all patterns relating to the composition and perform a find all search
    search_pattern = "|".join([worknumber_pattern, composition_pattern, key_pattern])
    composition_result = re.findall(search_pattern, title, re.IGNORECASE)
    if composition_result is not None:
        return composition_result
    else:
        return None

# Extracts the instrument (if applicable) from the title entry
def extract_instruments():
    return

def label_data():
    """
    Label the audio files
    """
    columns = ["composer","composition","movement","instruments"]
    files_df = pd.DataFrame(columns=columns)    
    audio_files = processfiles()
    for index, file in enumerate(audio_files):
        # If the metadata of an audio file is completely empty, we will skip it
        if any(v is None for v in [file.artist, file.title, file.album]):
            continue
        composer = extract_composer(file)
        composition = extract_composition(file.title)
        print(f"Original file: {file.artist},{file.title}")
        print(f"Detected composer: {composer}")
        print(f"Detected composition: {composition}")
        movement = None
        instruments = None
        new_row = {"composer": composer,"composition": composition,"movement": movement,"instruments": instruments}
        files_df = pd.concat([files_df, pd.DataFrame([new_row])], ignore_index=True)

if __name__ == "__main__":
    print("Loading data labeler")
    label_data()