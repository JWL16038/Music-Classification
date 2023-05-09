import os
import pandas as pd
import re
from pathlib import Path
from metadata_scraper import processfiles

composer_patten = r"Mozart|Beethoven|Bach|Ravel"
title_pattern = r"Piano|Concerto|Violin|Oboe|Flute|Bassoon|String|Quartet|Quintet|Symphony|Trio|Fugue"

# Extracts composer information from the artist entry
def extract_composer():
    composer_result = re.search(composer_patten, artist, re.IGNORECASE)
    if composer_result is not None:
        return composer_result.group(0)
    else:
        print("No composer found")
        return None

# Extracts the title of the work from the title entry
def extract_title():
    title_result = re.search(title_pattern, title, re.IGNORECASE)
    if title_result is not None:
        return title_result.group(0)
    else:
        print("No title found")
        return None

# Extracts the instrument (if applicable) from the title entry
def extract_instrument():
    return

# Label the audio files
def label_data():
    columns = ["composer","title","artist","album"]
    files_df = pd.DataFrame(columns=columns)    
    audio_files = processfiles()

if __name__ == "__main__":
    print("Loading data labeler")
    label_data()