# Python Tkinter Typing Test

A Python Tkinter-based typing test app with timed input, raw/net WPM & CPM metrics, accuracy tracking, and a dynamic UI with restart functionality.

## Features
- Timed typing test
- Raw WPM, Net WPM
- CPM (characters per minute)
- Accuracy tracking
- Restart / retake flow
- Simple Tkinter UI

## Getting started

### Prerequisites
- Python 3.8+ (recommended)
- Tkinter (ships with most Python installations)

### Run locally
```bash
git clone https://github.com/Arnav-AP/python-tkinter-typing-test.git
cd python-tkinter-typing-test
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

python main.py
```

> If your entry file is not `main.py`, run the correct script (for example `app.py`).

## How it works (metrics)
- **Raw WPM**: total words typed / minutes
- **Net WPM**: raw WPM adjusted for errors
- **CPM**: total characters typed / minutes
- **Accuracy**: correct characters / total characters * 100

## Project structure
This repo is 100% Python.

Common files you may find:
- `main.py` (or similar): app entry point
- Tkinter UI + typing-test logic modules

## Contributing
PRs are welcome.
1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Open a pull request

## License
Add a license file (MIT/Apache-2.0/etc.) if you want others to reuse your code with clear terms.