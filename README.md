[README.md](https://github.com/user-attachments/files/27611412/README.md)
# Emotion Match Go/No-Go Task

This repository contains a PsychoPy-based psychology experiment for an emotion label–picture matching Go/No-Go task using NimStim-style facial expression stimuli.

## Project Aim

The aim of this experiment is to measure response inhibition in an emotional face-processing context. On each trial, participants see an emotion word displayed above a facial expression image. They are instructed to press the spacebar as quickly as possible when the emotion word matches the facial expression, and to withhold their response when the word does not match the facial expression.

This design adapts the Go/No-Go paradigm to an emotion recognition context. It allows trial-level measurement of reaction time, accuracy, hits, misses, false alarms, and correct rejections.

## Task Design

The experiment contains 50 trials:

- 40 Go trials: the emotion word matches the facial expression.
- 10 No-Go trials: the emotion word does not match the facial expression.

Each trial follows this timing structure:

1. Fixation cross: 500 ms
2. Emotion label + face image: 750 ms
3. Blank intertrial interval: 500 ms

Participants respond using the spacebar.

## Go/No-Go Logic

| Trial type | Emotion word and face | Correct response | Outcome if correct |
|---|---|---|---|
| Go | Match | Press SPACE | Hit |
| No-Go | Mismatch | Press nothing | Correct rejection |

Incorrect responses are coded as:

- Miss: no response on a Go trial
- False alarm: spacebar press on a No-Go trial

## Files

```text
emotion-match-gonogo/
├── go_nogo_nimstim_text_match.py   # Main PsychoPy experiment script
├── README.md                       # Project explanation and running instructions
├── requirements.txt                # Required Python packages
├── .gitignore                      # Files/folders ignored by Git
├── stimuli/                        # Place NimStim image files here if you modify STIMULUS_DIR
└── data/                           # Output CSV files are saved here
```

## Dependencies

This task requires Python and the following packages:

```bash
pip install psychopy pandas
```

The task was written for PsychoPy and uses:

- `psychopy.visual`
- `psychopy.core`
- `psychopy.gui`
- `psychopy.hardware.keyboard`
- `pandas`
- `pathlib`
- `random`

## How to Run the Experiment

1. Install PsychoPy and required packages.

```bash
pip install psychopy pandas
```

2. Put the selected emotion face images in the same folder as the script, or update this line in the script:

```python
STIMULUS_DIR = Path(__file__).parent
```

3. Make sure the image filenames match the filenames listed in the `STIMULI` list exactly.

Example:

```python
STIMULI = [
    "Angry Female.png",
    "Happy Female.png",
    "Neutral Male.png",
]
```

4. Run the script:

```bash
python go_nogo_nimstim_text_match.py
```

5. Enter participant information in the pop-up dialog.

6. Follow the on-screen instructions.

7. The output file will be saved automatically in the `data` folder.

Example output filename:

```text
data/P001_emotion_match_gonogo.csv
```

## Output Data Columns

The script saves one row per trial. The output CSV includes:

| Column | Meaning |
|---|---|
| `participant_nr` | Participant ID entered at the start |
| `age` | Participant age |
| `trial_number` | Trial order |
| `filename` | Image filename |
| `image_emotion` | Emotion shown in the face image |
| `displayed_label` | Emotion word displayed above the image |
| `gender` | Actor gender parsed from filename |
| `condition` | Go or No-Go |
| `match_status` | Match or mismatch |
| `correct_response` | Expected response |
| `response_key` | Participant response |
| `rt` | Reaction time for first spacebar press |
| `accuracy` | 1 = correct, 0 = incorrect |
| `outcome` | Hit, miss, false alarm, or correct rejection |

## Notes on Stimuli

This script assumes the use of NimStim-style facial expression images, with filenames that contain both the emotion and actor gender. Example filenames include:

```text
Happy Female.png
Angry Male.png
Fear Female.png
Neutral Male.png
```

The actual NimStim image files are not included in this repository unless permitted by the dataset’s usage terms. Users should obtain the stimuli through the appropriate official access route and place the selected images in the correct folder before running the task.

## Code Design

The script is divided into clear sections:

1. Task settings
2. Stimulus metadata parsing
3. File checking
4. Trial-list generation
5. PsychoPy setup
6. Experiment loop
7. Data saving

The function `check_stimulus_files()` checks whether all listed image files exist before the experiment begins. This prevents the experiment from crashing midway due to missing or misspelled image filenames.

The function `make_trial_list()` creates the Go and No-Go trials. Go trials use matching emotion labels, while No-Go trials randomly select an incorrect emotion label for each face.

## Possible Extensions

Future versions could add:

- More trials for EEG/ERP analysis
- Practice accuracy feedback
- Counterbalanced blocks by target emotion
- Trial-level jittered timing
- Separate analysis script for reaction time and accuracy
- Visualization of hit rate, false alarm rate, and mean RT

## Ethical and Practical Notes

This task uses emotional facial expression stimuli, so participants should be informed that they will view human faces displaying different emotions. Any formal data collection should follow relevant institutional ethics procedures, especially if used with children or clinical populations.
