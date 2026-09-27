# 🔒 PassGuard — Password Strength Checker

A polished, cross-platform desktop cybersecurity utility that evaluates password strength in real time.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

---

## ✨ Features

| Feature | Description |
|---|---|
| **Real-time analysis** | Strength updates instantly as you type |
| **Show/Hide toggle** | 👁 button reveals or masks the password |
| **Strength meter** | Colour-coded progress bar (Red → Orange → Yellow → Green) |
| **Requirements checklist** | ✔ / ✖ for length, uppercase, lowercase, digit, special character |
| **Suggestions** | Actionable tips when the password is weak |
| **Clear / Reset** | One-click reset to start over |

## 🎨 Design

- Clean **Apple-inspired light theme**
- White card on soft-gray background
- Rounded corners, subtle borders
- **Inter** typography (falls back to system sans-serif)
- Responsive centered dashboard layout

## 🔐 Strength Levels

| Score | Label | Colour |
|-------|------------|---------|
| 0–1 | Very Weak | 🔴 Red |
| 2 | Weak | 🟠 Orange |
| 3 | Moderate | 🟡 Yellow |
| 4 | Strong | 🟢 Green |
| 5 | Very Strong | 🩵 Teal |

## 📁 Project Structure

```
SCT_CS_3/
├── app.py              # Main application (single file)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** (with `tkinter` — included by default on Windows & macOS; on Linux install `python3-tk`)

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

## 🖥️ Cross-Platform Compatibility

| OS | Status |
|---|---|
| Windows 10 / 11 | ✅ Works out of the box |
| Ubuntu / Kali Linux | ✅ Works (install `python3-tk` if missing) |
| macOS (Intel & Apple Silicon) | ✅ Works out of the box |

No OS-specific paths or APIs are used. Only standard Python libraries + CustomTkinter.

## 🛠️ Tech Stack

- **Language:** Python 3
- **UI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **Standard Library:** `re`, `string`

## 📄 License

This project is provided for educational purposes as part of SkillCraft Technology internship tasks.
