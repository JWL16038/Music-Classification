import os
import pandas as pd
import re
from pathlib import Path
from metadata_scraper import processfiles

composer_pattern = r"Mozart|Beethoven|Bach|Ravel"
composition_pattern = r"Sonata|Concerto|String|Quartet|Quintet|Symphony|Trio|Fugue|Variations|Overture"
worknumber_pattern = r"K.\s*\d+|Op.\s*\d+|No.\s*\d+"
movement_pattern = r"0[0-9](?:\.\s|\s-\s)?.*|\d{1,2}(?:st|nd|rd|th)\sMovement.*|(IX|IV|V?I{1,3})(\.\s|\s-\s).*|(Allegro|Andante|Adagio|Allegretto|Moderato|Presto|Menuetto|Rondo|Vivace|Molto|Largo|Larghetto|Romance|Overture|Finale|Scherzo).*"
key_pattern = r"\b[A-G]\b(?:-Flat|\sFlat|b|-Sharp|\sSharp|#)?(?:\sMajor|\sMinor)?"
instrument_pattern = r"Piano|Keyboard|Organ|Guitar|Violin|Viola|Cello|Double Bass|Piccolo|Flute|Oboe|Clarinet|Bassoon|Trumpet|Horn|Trombone|Tuba|Saxophone|Timpani|Harp|Recorder|Bagpipes|Ukulele"

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

def extract_movement(title):
    """
    Extracts movement information from the title entry

    """
    movement_result = re.search(movement_pattern, title, re.IGNORECASE)
    if movement_result is not None:
        return movement_result.group(0)
    print("No movement found")
    return None

# Extracts the instrument (if applicable) from the title entry
def extract_instruments(file):
    """
    Extracts instrument information from the title entry

    """
    # Get all possible entires from the file to search for the instruments.
    entires = [file.artist,file.title,file.album]
    for entry in entires:
        instrument_result = re.search(instrument_pattern, entry, re.IGNORECASE)
        if instrument_result is not None:
            return instrument_result.group(0)
    print("No instrument(s) found")
    return None

def label_data():
    """
    Label the audio files
    """
    columns = ["filename","composer","composition","movement","instruments"]
    files_df = pd.DataFrame(columns=columns)    
    audio_files = processfiles()
    for index, (path, file) in enumerate(audio_files):
        # If the metadata of an audio file is completely empty, we will skip it
        if any(v is None for v in [file.artist, file.title, file.album]):
            continue
        filename = path.name.__str__()
        composer = extract_composer(file)
        composition = extract_composition(file.title)
        movement = extract_movement(file.title)
        instruments = extract_instruments(file)
        print(f"Original file: {file.title}")
        print(f"Detected composer: {composer}")
        print(f"Detected composition: {composition}")
        print(f"Detected movement: {movement}")
        print(f"Detected instruments: {instruments}")
        new_row = {"filename": filename,"composer": composer,"composition": composition,"movement": movement,"instruments": instruments}
        files_df = pd.concat([files_df, pd.DataFrame([new_row])], ignore_index=True)
    return files_df

if __name__ == "__main__":
    print("Loading data labeler")
    label_data()