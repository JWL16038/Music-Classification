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
composition_pattern = r"Sonata|Concerto|String|Quartet|Quintet|Symphony|Trio|Fugue|Variations|Overture|Rondo|Fantasy|Opera|Divermento|Serenade|Ballet"
composition_number = r"((?:No)(?:.)?\s?\d+)|((?:Nos)(?:.)?\s?\d+\sand\s\d+)"
worknumber_pattern = r"((?:K|KV|OP|Opus)(?:.)?\s?\d+[a-z]?)"
worknumber_number_pattern = r"((?:No)(?:.)?\s?\d+)"
movement_pattern = r"\d{1,2}(?:st|nd|rd|th)\sMov(?:ement)?.*|(First|Second|Third|Forth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth)\sMov(?:ement).*|(IX|IV|V?I{1,3})(\.\s|\s-\s).*|Mov(?:ement)?(?:s)?\s(IX|IV|V?I{1,3}).*|Act\s\d{1,2}(?:.)?.*|((?<=:\s)|(?<=-\s))(Allegro|Andante|Andantino|Adagio|Allegretto|Moderato|Presto|Assai|Menuetto|Rondo|Vivace|Molto|Largo|Larghetto|Romance|Finale|Scherzo|(?:Un\s)?Poco|Grave|Pastorale|Maestoso|Overture|Introduction).*"
movement_number_pattern = r"([0-9][0-9](\.\s|\s-\s).*)"
key_pattern = r"(?<=in)(?:\s)?\b[A-G]\b(?:-Flat|\sFlat|b|-Sharp|\sSharp|#)?(?:\sMajor|\sMinor)?"
instrument_pattern = r"\b(Piano|Keyboard|Organ|Guitar|Violin|Viola|Cello|Double Bass|Piccolo|(?<!Magic\s)Flute|Oboe|Clarinet|Bassoon|Trumpet|Horn|Trombone|Tuba|Saxophone|Timpani|Harp|Recorder|Bagpipes|Ukulele)(?:s)?\b"

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
    logging.warning(f"No composer found for {file.title}")
    return None

def extract_composition(title):
    """
    Extracts the composition from the title entry.

    """
    composition_result = re.search(composition_pattern, title, re.IGNORECASE)
    if composition_result is not None:
        return composition_result.group(0)
    logging.warning(f"No composition found for {title}")
    return None

def extract_composition_no(title):
    """
    Extracts the composition number from the title entry.

    """
    composition_result = re.search(composition_pattern, title, re.IGNORECASE)
    start_position = 0
    if composition_result:
        start_position = composition_result.end()
    else:
        instrument_result = re.search(instrument_pattern, title, re.IGNORECASE)
        if instrument_result:
            start_position = instrument_result.end()
    composition_no_result = re.search(composition_number, title[start_position:], re.IGNORECASE)
    if composition_no_result is not None:
        return composition_no_result.group(0)
    logging.warning(f"No composition number found for {title}")
    return None

def extract_workno(title):
    """
    Extract work number (opus) information from the file metadata.

    """
    # Get all possible entires from the file to search for the work number.
    matches = []
    result = re.search(worknumber_pattern, title, re.IGNORECASE)
    if result is not None:
        matches = []
        number_result = re.search(worknumber_number_pattern, title[result.end():], re.IGNORECASE)
        if number_result:
            return f"{result.group(0)}, {number_result.group(0)}"
        return result.group(0)
    logging.warning(f"No work number found for {title}")
    return None
    

def extract_movement(title):
    """
    Extracts movement information from the title entry

    """
    # Find all movements that begins with a number. First filter all results that contain the work number then find the movement.
    title_search = title
    workno_last_match = list(re.finditer(worknumber_pattern, title, re.IGNORECASE))
    if workno_last_match:
        start_position = workno_last_match[-1].end()
        title_search = title[start_position:]
    movement_result = re.search(movement_number_pattern, title_search, re.IGNORECASE)
    if movement_result is not None:
        return movement_result.group(0)
    movement_result = re.search(movement_pattern, title, re.IGNORECASE)
    if movement_result is not None:
        return movement_result.group(0)
    logging.warning(f"No movement found for {title}")
    return None

def extract_key(title):
    """
    Extracts key information from the title.

    """
    key_result = re.search(key_pattern, title, re.IGNORECASE)
    if key_result is not None:
        return key_result.group(0)
    logging.warning(f"No key found for {title}")
    return None

def extract_instruments(title):
    """
    Extracts instrument information (if applicable) from the title

    """
    result = re.findall(instrument_pattern, title, re.IGNORECASE)
    if result is not None:
        matches = list(map(lambda s: s.capitalize(), result))
        matches = list(dict.fromkeys(matches))
        return ", ".join(matches)
    logging.warning(f"No instrument(s) found for {title}")
    return None

def label_data():
    """
    Label the audio files
    """
    columns = ["path","filename","title","composer","composition","composition_number","workno","key","movement","instruments"]
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
        composition_number = extract_composition_no(file.title)
        worknumber = extract_workno(file.title)
        key = extract_key(file.title)
        movement = extract_movement(file.title)
        instruments = extract_instruments(file.title)
        new_row = {"path": file_path,"filename": filename,"title": file.title,"composer": composer,"composition": composition,"composition_number": composition_number, "workno": worknumber,"key": key,"movement": movement,"instruments": instruments}
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