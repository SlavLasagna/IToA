import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageGrab

from backend import Backend, ImageProcessingError
from ui.file_selector import FileSelector
from ui.size_selector import SizeSelector
from ui.char_selector import CharSelector
from ui.status_bar import StatusBar
from ui.result_viewer import ResultViewer


class App(tk.Tk):
    def __init__(self, backend: Backend):
        super().__init__()
        self.backend = backend
        self.TITLE = "IToA - Image To ASCII Converter"

        # Main window config
        self.title(self.TITLE)
        self.geometry("640x480")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Welcome to IToA, the image to ASCII converter!").pack(pady=5)

        container = tk.Frame(self)
        container.pack(pady=5, expand=True)

        # File selection
        file_frame = tk.Frame(container)
        file_frame.pack(pady=5)
        self.file_selector = FileSelector(file_frame,
                                          on_file_selected=self._on_file_selected,
                                          on_clipboard_selected=self._on_clipboard_selected)
        self.file_selector.pack(fill="x")

        # Size selector
        self.size_selector = SizeSelector(container)
        self.size_selector.pack(pady=15)

        # Characters
        self.char_selector = CharSelector(container)
        self.char_selector.pack(pady=5)

        # Inverted option
        self.inverted_var = tk.BooleanVar()
        tk.Checkbutton(
            container,
            text="Inverted colors (black on white for light apps)",
            variable=self.inverted_var
        ).pack(pady=5)

        # Status bar
        self.status_bar = StatusBar(self)
        self.status_bar.pack(pady=10)

        # Action buttons
        buttons = tk.Frame(self)
        buttons.pack(pady=10, fill="x")
        tk.Button(buttons, text="Quit", command=self.on_exit).pack(padx=10, side=tk.LEFT)
        tk.Button(buttons, text="Display", command=self.on_display).pack(padx=10, side=tk.RIGHT)
        tk.Button(buttons, text="Copy", command=self.on_copy).pack(padx=10, side=tk.RIGHT)

    def _on_file_selected(self, filepath):
        try:
            self.backend.load_file(filepath)
            self.file_selector.set_text(f"Selected file: {filepath}", color="green")
            self.size_selector.set_size(self.backend.image.size)
            self.size_selector.lock()
            self.status_bar.set_success("Image loaded.")
        except ImageProcessingError as e:
            self.status_bar.set_error(str(e))
            self.file_selector.set_text("Failed to load file", color="red")

    def _on_clipboard_selected(self, image):
        try:
            self.backend.load_clipboard(image)
            self.file_selector.set_text("Copied image from clipboard", color="green")
            self.size_selector.set_size(self.backend.image.size)
            self.size_selector.lock()
            self.status_bar.set_success("Image loaded from clipboard.")
        except ImageProcessingError as e:
            self.status_bar.set_error(str(e))
            self.file_selector.set_text("Failed to load clipboard image", color="red")

    def on_copy(self):
        try:
            size = self.size_selector.get_size()
            chars = self.char_selector.get_characters()
            inverted = self.inverted_var.get()
            ascii_art = self.backend.to_ascii(size, chars, inverted)
            self.clipboard_clear()
            self.clipboard_append(ascii_art)
            self.status_bar.set_success("ASCII copied to clipboard.")
        except Exception as e:
            self.status_bar.set_error(f"Conversion failed: {e}")

    def on_display(self):
        try:
            size = self.size_selector.get_size()
            chars = self.char_selector.get_characters()
            inverted = self.inverted_var.get()
            ascii_art = self.backend.to_ascii(size, chars, inverted)
            font_size = max(1, int(1024 / size[1]))
            ResultViewer(self, ascii_art, self.TITLE, font_size)
            self.status_bar.set_success("ASCII displayed.")
        except Exception as e:
            self.status_bar.set_error(f"Conversion failed: {e}")

    def on_exit(self):
        self.destroy()
        exit(0)
