import os
import pandas as pd
import re
import logging
from pathlib import Path
from metadata_scraper import processfiles

absolute_path = Path().resolve().parent.parent
relative_path = Path('data/processed/classical_music_files')
full_path = absolute_path / relative_path

composer_pattern = r"Mozart|Beethoven|Bach|Ravel"
composition_pattern = r"Sonata|Concerto|String|Quartet|Quintet|Symphony|Trio|Fugue|Variations|Overture|Rondo|Fantasy|Opera"
worknumber_pattern = r"(K|KV|Op|OP|No)(?:.)?\s?\d+"
movement_pattern = r"0[0-9](?:\.\s|\s-\s)?.*|\d{1,2}(?:st|nd|rd|th)\sMovement.*|(IX|IV|V?I{1,3})(\.\s|\s-\s).*|(Allegro|Andante|Adagio|Allegretto|Moderato|Presto|Menuetto|Rondo|Vivace|Molto|Largo|Larghetto|Romance|Finale|Scherzo).*"
key_pattern = r"(?<=in)(?:\s)?\b[A-G]\b(?:-Flat|\sFlat|b|-Sharp|\sSharp|#)?(?:\sMajor|\sMinor)?"
instrument_pattern = r"Piano|Keyboard|Organ|Guitar|Violin|Viola|Cello|Double Bass|Piccolo|Flute|Oboe|Clarinet|Bassoon|Trumpet|Horn|Trombone|Tuba|Saxophone|Timpani|Harp|Recorder|Bagpipes|Ukulele"

def extract_composer(file):
    """
    Extracts composer information from the file metadata.

    """
    # Get all possible entires from the file to search for the composer.
    entires = [file.artist,file.title,file.album]
    for entry in entires:
        composer_result = re.search(composer_pattern, entry, re.IGNORECASE)
        if composer_result is not None:
            return composer_result.group(0).lower().capitalize()
    logging.warn(f"No composer found for {file.title}")
    return None

def extract_composition(title):
    """
    Extracts the composition from the title entry.

    """
    #Join all patterns relating to the composition and perform a find all search
    composition_result = re.findall(composition_pattern, title, re.IGNORECASE)
    if composition_result is not None:
        return composition_result
    logging.warning(f"No composition found for {title}")
    return None

def extract_workno(file):
    """
    Extract work number (opus) information from the file metadata.

    """
    # Get all possible entires from the file to search for the work number.
    entires = [file.artist,file.title,file.album]
    for entry in entires:
        workno_result = re.search(worknumber_pattern, entry, re.IGNORECASE)
        if workno_result is not None:
            return workno_result.group(0)
    logging.warning(f"No work number found for {file.title}")
    return None
    

def extract_movement(title):
    """
    Extracts movement information from the title entry

    """
    movement_result = re.search(movement_pattern, title, re.IGNORECASE)
    if movement_result is not None:
        return movement_result.group(0)
    logging.warning(f"No movement found for {title}")
    return None

def extract_key(file):
    """
    Extracts key information from the file metadata.

    """
    # Get all possible entires from the file to search for the key.
    entires = [file.artist,file.title,file.album]
    for entry in entires:
        key_result = re.search(key_pattern, entry, re.IGNORECASE)
        if key_result is not None:
            return key_result.group(0)
    logging.warning(f"No key found for {file.title}")
    return None

def extract_instruments(file):
    """
    Extracts instrument information (if applicable) from the file metadata

    """
    # Get all possible entires from the file to search for the instruments.
    entires = [file.artist,file.title,file.album]
    for entry in entires:
        instrument_result = re.search(instrument_pattern, entry, re.IGNORECASE)
        if instrument_result is not None:
            return instrument_result.group(0).lower().capitalize()
    logging.warning(f"No instrument(s) found for {file.title}")
    return None

def label_data():
    """
    Label the audio files
    """
    columns = ["path","filename","title","composer","composition","workno","key","movement","instruments"]
    files_df = pd.DataFrame(columns=columns)    
    audio_files = processfiles()
    for index, (path, file) in enumerate(audio_files):
        file_path = path.parent.__str__()
        filename = path.name.__str__()
        # If the metadata of an audio file is completely empty, we will skip it
        if all(v is None for v in [file.artist, file.title, file.album]):
            logging.warning(f"Skipping {filename} because its metadata is empty")
            continue
        composer = extract_composer(file)
        composition = extract_composition(file.title)
        worknumber = extract_workno(file)
        key = extract_key(file)
        movement = extract_movement(file.title)
        instruments = extract_instruments(file)
        new_row = {"path": file_path,"filename": filename,"title": file.title,"composer": composer,"composition": composition,"workno": worknumber,"key": key,"movement": movement,"instruments": instruments}
        files_df = pd.concat([files_df, pd.DataFrame([new_row])], ignore_index=True)
    files_df = files_df.fillna('')
    logging.info(f"Processed {len(files_df)} music files")
    return files_df

def save_csv(df):
    try:
        df.to_csv(os.path.join(full_path,"metadata.csv"),index=False)
        logging.info(f"Metadata saved successfully to {full_path}/metadata.csv")
    except Exception as e:
        logging.error(f"Saving metadata failed! {str(e)}")
    return

if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)
    logging.info("Loading music data labeler")
    df = label_data()
    save_csv(df)