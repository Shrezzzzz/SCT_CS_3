# SCT_CS_3 — PassGuard: Password Strength Checker

A GUI-based password strength analysis tool built with Python and CustomTkinter, developed as Task 03 of the SkillCraft Technology Cyber Security Internship.

## Features

- Real-time password strength evaluation as you type
- 5-segment colour-coded strength meter (Red → Orange → Yellow → Green)
- Security requirements checklist for length, uppercase, lowercase, digit, and special characters
- Show/Hide toggle to reveal or mask the password
- Copy password to clipboard functionality
- One-click reset to clear the input and start over

## Project Structure

```
SCT_CS_3/
├── app.py              # Main application (single file)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Getting Started

### Prerequisites

- Python 3.8+ (with `tkinter` — included by default on Windows & macOS; on Linux install `python3-tk`)

### Installation

```bash
# Clone or navigate into the project
cd SCT_CS_3

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

> **Linux note:** If you get a `tkinter` error, install it with:
> ```bash
> sudo apt install python3-tk   # Debian/Ubuntu/Kali
> ```

## Cross-Platform Compatibility

- **Windows 10 / 11:** Works out of the box
- **Ubuntu / Kali Linux:** Works (install `python3-tk` if missing)
- **macOS (Intel & Apple Silicon):** Works out of the box

No OS-specific paths or APIs are used. Only standard Python libraries + CustomTkinter.

## Tech Stack

- **Language:** Python 3
- **UI Framework:** CustomTkinter
- **Standard Library:** `re`, `string`

## License

This project is provided for educational purposes as part of SkillCraft Technology internship tasks.
