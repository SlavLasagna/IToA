# IToA - Image To ASCII Converter

IToA (Image To ASCII) is a simple Python application that converts images into ASCII art.  
It comes with a graphical interface built using Tkinter and Pillow (PIL), allowing you to load images, adjust the output size, choose characters, and copy the result to the clipboard.

---

## Features

- **Load images** from:
  - A file (`.png`, `.jpg`, etc.)
  - The system clipboard (if an image is copied)
- **Adjust output size** with width and height spinboxes
  - Lock/unlock aspect ratio
- **Character sets**:
  - Predefined sets (e.g. `░▒▓█`, ` .,:;=#`)
  - Custom character string
- **Inverted colors option** (useful for light vs dark backgrounds)
- **View result**:
  - Display ASCII art in a scrollable new window
  - Copy ASCII art to clipboard
- **Error handling** with simple popup messages

---

## Requirements

- Python **3.10+** (earlier versions may also work)
- Dependencies:
  - [Pillow](https://pypi.org/project/pillow/) `pip install pillow`
  - [Tkinter](https://docs.python.org/fr/3.13/library/tkinter.html) `pip install tkinter` (usually comes preinstalled with Python)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/SlavLasagna/IToA.git
```

Install dependencies:
```bash
cd IToA
pip install pillow
pip install tkinter
```

---

## Usage

Run the program:
```bash
python app.py
```

### Steps:

1. Choose an image file, or copy an image to clipboard and use the "Copy from clipboard" button.
2. Adjust width and height (or lock ratio).
3. Select a character set (or enter custom characters).
4. Optionally toggle "Inverted colors".
5. Convert:
   - Display ASCII art in a new window. 
   - Or copy ASCII art directly to clipboard.

---

## Example

Image input: [GitHub Logo](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbqj9Ii13d6hx5a9kyLnC5A8A96LDSaSZv_w&s)

Settings:
- Size = 64 x 64 px
- Characters = ` ░▒▓█`
- Not inverted (white on black)

Output ASCII :
```
████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████
███████████████████████▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓███████████████████████
███████████████████▓▒▒░                  ░▒▒▓███████████████████
████████████████▓▒░                          ░▒▓████████████████
█████████████▓▒░                                ░▒▓█████████████
████████████▒░                                    ░▒████████████
██████████▓░      ░▓▓▓▓▒░   ░░░░░░░░   ░▒▓▓▓▓░      ░▓██████████
█████████▓        ▒██████▓▓▓████████▓▓▓██████▒        ▓█████████
████████▓         ░▓▓██████████████████████▓█░         ▓████████
███████▓░        ░▓▓▓████████████████████████▓░        ░▓███████
███████▓        ░▓█████████████████████████████░        ▓███████
███████▒        ▒█▓████████████████████████████▒        ▒███████
███████▒        ▒██████████████████████████████▒        ▒███████
███████▒         ▓████████████████████████████▓░        ▒███████
███████▓         ░▓██████████████████████████▓░         ▓███████
████████▒          ▒▓██████████████████████▓▒          ▒████████
███████▓█▒    ░▒░    ░░▒▒▓▓▓▓███████▓▓▓▒▒░░           ▒█▓███████
██████████▒    ░▓▓▒       ░▓████████▓░               ▒██████████
███████████▓░    ▒█▓▒░░░░▒▓██████████▓             ░▓███████████
████████████▓▒░   ░▒▓▓▓▓▓▓▓▓█████████▓░          ░▒▓████████████
██████████████▓▓░         ▓██████████▓         ░▓▓██████████████
█████████████████▓▓▒░     ▓██████████▓     ░▒▓▓█████████████████
█████████████████████▓▓▒▒▒▓▓█████████▓▒▒▒▓▓█████████████████████
████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████
```

---

## Project Structure

```
IToA/
├── backend.py
├── main.py
└── ui/
    ├── app.py
    ├── char_selector.py
    ├── file_selector.py
    ├── result_viewer.py
    ├── size_selector.py
    └── status_bar.py
```

---

## Roadmap

☑ Factorize code (split backend logic and UI) <br>
☐ Add export options (saving to text file or bitmap) <br>
☐ Package as a standalone executable

---

## License


This project is licensed under the GNU General Public License v3.0 (GPL-3.0) - see the [LICENSE](LICENSE) file for details.