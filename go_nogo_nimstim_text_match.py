"""
Emotion label-picture matching Go/No-Go task using NimStim-style facial expression stimuli.

Updated design:
- Go trials: the emotion word above the face MATCHES the facial expression.
  Participant should press SPACE as quickly as possible.
- No-Go trials: the emotion word above the face DOES NOT MATCH the facial expression.
  Participant should withhold response / press nothing.

Default structure:
- 50 trials total
- 40 Go/match trials
- 10 No-Go/mismatch trials
- Each trial:
    1. fixation cross: 500 ms
    2. emotion label + face image: 750 ms
    3. blank interval: 500 ms

How to adapt:
- Put your selected NimStim images in the same folder as this script,
  or change STIMULUS_DIR to the folder where your images are stored.
- The script assumes filenames like "Happy Female.png", "Angry Male.png", etc.
"""

from pathlib import Path
import random
import pandas as pd

from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim
from psychopy.core import Clock, quit, wait
from psychopy.event import Mouse
from psychopy.hardware.keyboard import Keyboard


# -----------------------------
# Task settings
# -----------------------------
N_TRIALS = 50
N_GO = 40
N_NOGO = 10

FIXATION_DURATION = 0.5
STIMULUS_DURATION = 0.75
ITI_DURATION = 0.5

# The possible labels shown above the face.
EMOTION_LABELS = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]

# Use the folder where your NimStim images are stored.
# If the images are in the same folder as this script, use Path(__file__).parent
STIMULUS_DIR = Path(__file__).parent
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Selected stimuli. Add/remove filenames as needed.
STIMULI = [
    "Angry Female.png",
    "Disgust Female.png",
    "Happy Female.png",
    "Neutral Female.png",
    "Sad Female.png",
    "Fear Female.png",
    "Surprise Female.png",
    "Angry Male.png",
    "Disgust Male.png",
    "Happy Male.png",
    "Neutral Male.png",
    "Sad Male.png",
    "Fear Male.png",
    "Surprise Male.png",
]


# -----------------------------
# Helper functions
# -----------------------------
def parse_stimulus_metadata(filename: str) -> dict:
    """Extract emotion and gender from filenames such as 'Happy Female.png'."""
    stem = Path(filename).stem.lower()
    parts = stem.split()

    emotion = parts[0]
    if emotion == "surprised":
        emotion = "surprise"
    if emotion == "fearful":
        emotion = "fear"

    gender = "unknown"
    if "female" in parts:
        gender = "female"
    elif "male" in parts:
        gender = "male"

    return {
        "filename": filename,
        "emotion": emotion,
        "gender": gender,
        "path": STIMULUS_DIR / filename,
    }


def check_stimulus_files(stimuli_df: pd.DataFrame):
    missing = [str(p) for p in stimuli_df["path"] if not Path(p).exists()]
    if missing:
        missing_text = "\n".join(missing)
        raise FileNotFoundError(
            "The following image files could not be found.\n"
            "Make sure STIMULUS_DIR points to the correct folder and filenames match exactly:\n\n"
            f"{missing_text}"
        )


def make_trial_list(stimuli_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create 40 Go/match trials and 10 No-Go/mismatch trials.

    Go/match:
        displayed_label == image emotion
        correct response = SPACE

    No-Go/mismatch:
        displayed_label != image emotion
        correct response = no key
    """
    if len(stimuli_df) == 0:
        raise ValueError("No stimuli found.")

    go_trials = stimuli_df.sample(n=N_GO, replace=True).copy()
    go_trials["condition"] = "go"
    go_trials["match_status"] = "match"
    go_trials["displayed_label"] = go_trials["emotion"]
    go_trials["correct_response"] = "space"

    nogo_trials = stimuli_df.sample(n=N_NOGO, replace=True).copy()
    nogo_trials["condition"] = "nogo"
    nogo_trials["match_status"] = "mismatch"

    mismatch_labels = []
    for emotion in nogo_trials["emotion"]:
        possible_wrong_labels = [label for label in EMOTION_LABELS if label != emotion]
        mismatch_labels.append(random.choice(possible_wrong_labels))

    nogo_trials["displayed_label"] = mismatch_labels
    nogo_trials["correct_response"] = "none"

    trials = pd.concat([go_trials, nogo_trials], ignore_index=True)
    trials = trials.sample(frac=1).reset_index(drop=True)
    trials.insert(0, "trial_number", range(1, len(trials) + 1))
    return trials


def wait_for_space_or_escape(kb, win):
    kb.clearEvents()
    while True:
        keys = kb.getKeys(["space", "escape"], waitRelease=False)
        if keys:
            if keys[0].name == "escape":
                win.close()
                quit()
            return


def draw_and_wait(win, stim, duration: float):
    stim.draw()
    win.flip()
    wait(duration)


# -----------------------------
# Experiment info
# -----------------------------
exp_info = {
    "participant_nr": "",
    "age": "",
}

dlg = DlgFromDict(exp_info, title="Emotion Match Go/No-Go Task")
if not dlg.OK:
    quit()

participant = exp_info["participant_nr"].strip() or "anonymous"
age = exp_info["age"].strip()


# -----------------------------
# Prepare stimuli and trials
# -----------------------------
stimuli_df = pd.DataFrame([parse_stimulus_metadata(f) for f in STIMULI])
check_stimulus_files(stimuli_df)
trial_list = make_trial_list(stimuli_df)


# -----------------------------
# PsychoPy setup
# -----------------------------
win = Window(size=(1200, 800), fullscr=False, color="black", units="height")
mouse = Mouse(visible=False)
kb = Keyboard()

fixation = TextStim(win, text="+", color="white", height=0.08)
blank = TextStim(win, text="", color="white")

instructions = TextStim(
    win,
    text=(
        "You will see an emotion word above a face.\n\n"
        "Press SPACE as quickly as possible when the word MATCHES the facial expression.\n\n"
        "Do NOT press anything when the word does NOT match the facial expression.\n\n"
        "Try to respond quickly and accurately.\n\n"
        "Press SPACE to begin."
    ),
    color="white",
    height=0.035,
    wrapWidth=1.2,
)

end_text = TextStim(
    win,
    text="The task is finished. Thank you!\n\nPress SPACE to exit.",
    color="white",
    height=0.04,
    wrapWidth=1.2,
)


# -----------------------------
# Run task
# -----------------------------
instructions.draw()
win.flip()
wait_for_space_or_escape(kb, win)

results = []

for _, trial in trial_list.iterrows():
    # Fixation
    draw_and_wait(win, fixation, FIXATION_DURATION)

    # Stimuli: label above face
    image = ImageStim(
        win,
        image=str(trial["path"]),
        pos=(0, -0.08),
        size=(0.55, 0.55),
    )

    label = TextStim(
        win,
        text=str(trial["displayed_label"]).upper(),
        color="white",
        height=0.055,
        pos=(0, 0.32),
    )

    kb.clearEvents()
    stimulus_clock = Clock()
    response_key = None
    rt = None

    while stimulus_clock.getTime() < STIMULUS_DURATION:
        label.draw()
        image.draw()
        win.flip()

        keys = kb.getKeys(["space", "escape"], waitRelease=False)
        if keys and response_key is None:
            first_key = keys[0]
            if first_key.name == "escape":
                win.close()
                quit()
            response_key = first_key.name
            rt = first_key.rt

    # Blank screen / ITI
    blank.draw()
    win.flip()
    wait(ITI_DURATION)

    # Score accuracy
    made_response = response_key == "space"
    if trial["condition"] == "go":
        accuracy = int(made_response)
        outcome = "hit" if made_response else "miss"
    else:
        accuracy = int(not made_response)
        outcome = "false_alarm" if made_response else "correct_rejection"

    results.append({
        "participant_nr": participant,
        "age": age,
        "trial_number": int(trial["trial_number"]),
        "filename": trial["filename"],
        "image_emotion": trial["emotion"],
        "displayed_label": trial["displayed_label"],
        "gender": trial["gender"],
        "condition": trial["condition"],
        "match_status": trial["match_status"],
        "correct_response": trial["correct_response"],
        "response_key": response_key if response_key is not None else "none",
        "rt": rt if rt is not None else "NA",
        "accuracy": accuracy,
        "outcome": outcome,
    })


# -----------------------------
# Save data
# -----------------------------
results_df = pd.DataFrame(results)
output_file = DATA_DIR / f"{participant}_emotion_match_gonogo.csv"
results_df.to_csv(output_file, index=False)

end_text.draw()
win.flip()
wait_for_space_or_escape(kb, win)

win.close()
quit()
