import os
import pandas as pd
import re
from pathlib import Path
from metadata_scraper import processfiles

composer_pattern = r"Mozart|Beethoven|Bach|Ravel"
composition_pattern = r"Piano|Sonata|Concerto|Violin|Oboe|Flute|Bassoon|String|Quartet|Quintet|Symphony|Trio|Fugue|Variations"
worknumber_pattern = r"K.\s*\d+|Op.\s*\d+|No.\s*\d+"
key_pattern = r"Major|Minor"


# Extracts composer information from the artist entry
def extract_composer(artist):
    composer_result = re.search(composer_pattern, artist, re.IGNORECASE)
    if composer_result is not None:
        return composer_result.group(0)
    else:
        print("No composer found")
        return None

# Extracts the composition and the work number from the title entry
def extract_composition(title):
    #Join all patterns relating to the composition
    search_pattern = "|".join([worknumber_pattern,compositional_pattern])
    composition_result = re.findall(search_pattern, title, re.IGNORECASE)
    print(composition_result)
    if composition_result is not None:
        return composition_result
    else:
        print("No composition found")
        return None

# Extracts the instrument (if applicable) from the title entry
def extract_instruments():
    return

# Label the audio files
def label_data():
    columns = ["composer","composition","movement","instruments"]
    files_df = pd.DataFrame(columns=columns)    
    audio_files = processfiles()
    for index, file in enumerate(audio_files):
        if any(v is None for v in [file.artist, file.title, file.album]):
            continue
        print(file.artist,file.title,file.album)
        composer = extract_composer(file.artist)
        composition = extract_composition(file.title)
        movement = None
        instruments = None
        new_row = {"composer": composer,"composition": composition,"movement": movement,"instruments": instruments}
        files_df = pd.concat([files_df, pd.DataFrame([new_row])], ignore_index=True)

if __name__ == "__main__":
    print("Loading data labeler")
    label_data()