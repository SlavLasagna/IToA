import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab


class FileSelector(tk.Frame):
    """
    Widget that provides:
     - 'Choose an image' button -> calls on_file_selected(filepath)
     - 'Copy from clipboard' button -> calls on_clipboard_selected(PIL.Image)
     - small label showing the current status / selected file
    """

    def __init__(self, parent, on_file_selected=None, on_clipboard_selected=None):
        super().__init__(parent)
        self.on_file_selected = on_file_selected
        self.on_clipboard_selected = on_clipboard_selected

        self._build()

    def _build(self):
        # Buttons
        file_button = tk.Button(self, text="Choose an image", command=self._choose_file)
        file_button.pack(side=tk.LEFT, padx=5)

        clipboard_button = tk.Button(self, text="Copy from clipboard", command=self._from_clipboard)
        clipboard_button.pack(side=tk.LEFT, padx=5)

        # Status / file label
        self.file_label = tk.Label(self, text="", fg="green")
        self.file_label.pack(side=tk.RIGHT, padx=5)

    def _choose_file(self):
        filepath = filedialog.askopenfilename()
        # If user cancelled, filepath may be empty string
        if not filepath:
            return
        # Update label (optimistic)
        self.set_text(f"Selected file: {filepath}", color="green")
        if callable(self.on_file_selected):
            try:
                self.on_file_selected(filepath)
            except Exception:
                # Let the parent widget handle errors (it may update the label)
                pass

    def _from_clipboard(self):
        image = ImageGrab.grabclipboard()
        if image is None:
            self.set_text("No image in clipboard", color="red")
            return
        self.set_text("Copied image from clipboard", color="green")
        if callable(self.on_clipboard_selected):
            try:
                self.on_clipboard_selected(image)
            except Exception:
                # Let the parent handle exceptions
                pass

    def set_text(self, text: str, color: str = "green"):
        """Convenience method to update the internal label."""
        self.file_label.config(text=text, fg=color)
