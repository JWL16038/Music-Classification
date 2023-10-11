# Music Classification

The of this project is to classify audio files of musical works from major classical composers to the correct composer's name. A data labeller has been built to extract the metadata from the audio files and stores it as a csv file. A sample output of this csv is shown below
```csv
path	filename	title	composer	composition	composition_number	nickname	workno	key	movement
Beethoven\BEETHOVENTheFivePianoConcertos	01.ConcertoNo.1InCMajor-I.AllegroConBrio.mp3	Concerto No. 1 in C Major: I. Allegro con brio	Beethoven	Concerto	No. 1			 C Major	I. Allegro con brio
Beethoven\BEETHOVENTheFivePianoConcertos	02.ConcertoNo.1InCMajor-Ii.Largo.mp3	Concerto No. 1 in C Major: II. Largo	Beethoven	Concerto	No. 1			 C Major	II. Largo
Beethoven\BEETHOVENTheFivePianoConcertos	03.ConcertoNo.1InCMajor-Iii.Rondo-AllegroScherzando.mp3	Concerto No. 1 in C Major: III. Rondo - Allegro scherzando	Beethoven	Concerto, Rondo	No. 1			 C Major	III. Rondo - Allegro scherzando
Beethoven\BEETHOVENTheFivePianoConcertos	04.ConcertoNo.2InB-flatMajor-I.AllegroConBrio.mp3	Concerto No. 2 in B-flat Major: I. Allegro con brio	Beethoven	Concerto	No. 2			 B-flat Major	I. Allegro con brio
Beethoven\BEETHOVENTheFivePianoConcertos	05.ConcertoNo.2InB-flatMajor-Ii.Adagio.mp3	Concerto No. 2 in B-flat Major: II. Adagio	Beethoven	Concerto	No. 2			 B-flat Major	II. Adagio
Beethoven\BEETHOVENTheFivePianoConcertos	06.ConcertoNo.2InB-flatMajor-Iii.RondomoltoAllegro.mp3	Concerto No. 2 in B-flat Major: III. Rondo (Molto allegro)	Beethoven	Concerto, Rondo	No. 2			 B-flat Major	III. Rondo (Molto allegro)
Beethoven\BEETHOVENTheFivePianoConcertos	07.ConcertoNo.3InCMinor-I.AllegroModerato.mp3	Concerto No. 3 in C Minor: I. Allegro moderato	Beethoven	Concerto	No. 3			 C Minor	I. Allegro moderato
Beethoven\BEETHOVENTheFivePianoConcertos	08.ConcertoNo.3InCMinor-Ii.AndanteConMoto.mp3	Concerto No. 3 in C Minor: II. Andante con moto	Beethoven	Concerto	No. 3			 C Minor	II. Andante con moto
Beethoven\BEETHOVENTheFivePianoConcertos	09.ConcertoNo.3InCMinor-Iii.Rondovivace.mp3	Concerto No. 3 in C Minor: III. Rondo (Vivace)	Beethoven	Concerto, Rondo	No. 3			 C Minor	III. Rondo (Vivace)
```

Next steps:
- Preprocess the data to reduce the number of features
- Build a Deep neural network to learn the features of the audio files and predict the composer's name by a probability

## Structure 
    .
    ├── data                    # Data files which includes raw and processed datasets. These will not be uploaded to GitHub
    |   ├── raw                 # Raw, unprocessed datasets that needs cleaning up and processing
    |   ├── processed           # Processed datasets that are ready for analysis
    ├── docs                    # Documentation files including journal articles
    ├── notebooks               # Jupyter notebooks for data scraping, EDA and model testing
    |   ├── FMA                 # All notebooks relating to the Free Music Archive (FMA) dataset
    |   ├── GTZAN               # All notebooks relating to the GTZAN dataset
    |   ├── Spotify             # All notebooks relating to Spotify's web scraped music datasets
    ├── src                     # Source code files including the data labeller
    ├── test                    # Automated tests for ML models
    ├── LICENSE
    └── README.md
