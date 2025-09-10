from math import ceil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
from PIL import Image
from PIL import ImageGrab

class Backend:
    def __init__(self):
        self.image = None
        self.FONT_RATIO = 0.44

    def handle_file(self, filepath):
        try:
            self.image = Image.open(filepath)
            return True
        except Exception:
            messagebox.showerror(title="IToA - Image To ASCII Converter", message="There was an error processing your image.")
            return False

    def check_input_constraints(self, size, characters, inverted):
        if not isinstance(size, tuple):
            raise TypeError('Size must be a tuple')
        if len(size) != 2:
            raise Exception('Size must contain two elements')
        if not isinstance(size[0], int) or size[0] < 1:
            raise Exception('Invalid desired image width')
        if not isinstance(size[1], int) or size[1] < 1:
            raise Exception('Invalid desired image height')
        if not isinstance(characters, str) or len(characters) < 1:
            raise TypeError("Characters must be a string")
        if not isinstance(inverted, bool):
            raise TypeError("Inverted must be a boolean")

    def convert(self, size: tuple | float, characters: str, inverted: bool) -> str:
        self.check_input_constraints(size, characters, inverted)
        width, height = size[0], size[1] * self.FONT_RATIO
        image = self.image.resize((int(width), int(height)))
        if inverted:
            characters = characters[::-1]
        length = len(characters) - 1
        data = image.convert('L').getdata()
        width, height = image.size
        result = ""
        for y in range(height):
            for x in range(width):
                pixel = data[y * width + x]
                result += characters[((pixel * length) // 255)]
            result += "\n"
        return result

class App(tk.Tk):
    def __init__(self, backend: Backend):
        super().__init__()
        self.backend = backend

        # Class vars/consts
        self.TITLE = "IToA - Image To ASCII Converter"
        self.size_ratio = 1
        self.size_ratio_lock = False
        self.size_spinbox_mutex = True

        # Main window config
        self.title(self.TITLE)
        self.geometry("640x480")

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Top text
        top_text = tk.Label(self, text="Welcome to IToA, the image to ASCII converter!")
        top_text.pack(pady=5)

        container = tk.Frame(self)
        container.pack(pady=5, expand=True)

        # File selection widget
        self.file_container = tk.Frame(container)
        self.file_container.pack(pady=5)

        file_button = tk.Button(self.file_container, text="Choose an image", command=self.open_file_dialog)
        file_button.pack(side=tk.LEFT,padx=5)

        copy_from_clipboard_button = tk.Button(self.file_container, text="Copy from clipboard", command=self.open_from_clipboard)
        copy_from_clipboard_button.pack(side=tk.LEFT,padx=5)

        self.file_label = tk.Label(self.file_container, text="", fg="green")
        self.file_label.pack(side=tk.RIGHT,padx=5)

        # Size selection container
        size_container = tk.Frame(container)
        size_container.pack(pady=15)

        # Width selection spinbox
        width_label = tk.Label(size_container, text="Width:")
        width_label.pack(side=tk.LEFT, padx=5)

        self.width_var = tk.IntVar(value=1)
        self.width_var.trace_add("write", self.on_width_spin_change)
        self.width_spinbox = ttk.Spinbox(size_container, from_=1, to=1024, textvariable=self.width_var)
        self.width_spinbox.pack(side=tk.LEFT, padx=(5,15))

        # Height selection spinbox
        height_label = tk.Label(size_container, text="Height:")
        height_label.pack(side=tk.LEFT,padx=(15,5))

        self.height_var = tk.IntVar(value=1)
        self.height_var.trace_add("write", self.on_height_spin_change)
        self.height_spinbox = ttk.Spinbox(size_container, from_=1, to=1024, textvariable=self.height_var)
        self.height_spinbox.pack(side=tk.LEFT,padx=5)

        self.size_ratio_lock_button = tk.Button(size_container, text="Lock ratio", command=self.toggle_size_ratio_lock)
        self.size_ratio_lock_button.pack(side=tk.RIGHT, padx=15)

        # Character list entry
        characters_container = tk.Frame(container)
        characters_container.pack(pady=5)

        characters_label = tk.Label(characters_container, text="Characters:")
        characters_label.pack(side=tk.LEFT, padx=5)

        self.characters_combo = ttk.Combobox(characters_container, values=[" ░▒▓█"," .,:;/#","Custom..."], font=("Courier New", 12))
        self.characters_combo.current(0)
        self.characters_combo.pack(side=tk.LEFT, padx=5)

        # Checkbox
        self.checkbox_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(
            container,
            text="Inverted colors (inverted means black on white, for light modes apps)",
            variable=self.checkbox_var
        )
        self.checkbox.pack(pady=5)

        # Result info labels
        result_info_container = tk.Frame(self)
        result_info_container.pack(pady=10)

        self.success_label = tk.Label(result_info_container, fg="green")
        self.success_label.pack(pady=5)

        self.error_label = tk.Label(result_info_container, fg="red")
        self.error_label.pack(pady=5)

        # Submit & quit buttons
        buttons_container = tk.Frame(self)
        buttons_container.pack(pady=10, fill="x")

        quit_button = tk.Button(buttons_container, text="Quit", command=self.on_exit)
        quit_button.pack(padx=10, side=tk.LEFT)

        result_container = tk.Frame(buttons_container)
        result_container.pack(padx=10, side=tk.RIGHT)

        submit_button = tk.Button(result_container, text="Display to new window", command=self.on_submit)
        submit_button.pack(padx=10, side=tk.LEFT)

        copy_to_clipboard_button = tk.Button(result_container, text="Copy to clipboard", command=self.copy_then_submit)
        copy_to_clipboard_button.pack(padx=10, side=tk.LEFT)

    def lock_size_ratio(self):
        self.size_ratio_lock = True
        self.size_ratio_lock_button.config(text="Unlock ratio")
        self.size_ratio = self.width_var.get() / self.height_var.get()

    def unlock_size_ratio(self):
        self.size_ratio_lock = False
        self.size_ratio_lock_button.config(text="Lock ratio")

    def toggle_size_ratio_lock(self):
        if not self.size_ratio_lock and (self.width_var.get() or self.height_var.get()):
            self.lock_size_ratio()
        else:
            self.unlock_size_ratio()

    def on_width_spin_change(self, *args):
        if self.size_ratio_lock and self.size_spinbox_mutex:
            width = self.width_var.get()
            self.size_spinbox_mutex = False
            self.height_var.set(ceil(width / self.size_ratio))
            self.size_spinbox_mutex = True

    def on_height_spin_change(self, *args):
        if self.size_ratio_lock and self.size_spinbox_mutex:
            height = self.height_var.get()
            self.size_spinbox_mutex = False
            self.width_var.set(ceil(height * self.size_ratio))
            self.size_spinbox_mutex = True

    def open_file_dialog(self):
        self.unlock_size_ratio()
        filepath = filedialog.askopenfilename()
        result = self.backend.handle_file(filepath)
        if result:
            self.file_label.config(text="Selected file: {}".format(filepath))
            self.error_label.config(text="")
            size = self.backend.image.size
            self.width_var.set(size[0])
            self.height_var.set(size[1])
            self.lock_size_ratio()

    def open_from_clipboard(self):
        self.unlock_size_ratio()
        self.error_label.config(text="")
        self.success_label.config(text="")
        try:
            self.backend.image = ImageGrab.grabclipboard()
            self.file_label.config(text="Copied image from clipboard")
            self.error_label.config(text="")
            size = self.backend.image.size
            self.width_var.set(size[0])
            self.height_var.set(size[1])
            self.lock_size_ratio()
        except Exception as error:
            print(error)
            self.error_label.config(text="Unable to copy image from clipboard, please try again.")

    def copy_then_submit(self):
        self.error_label.config(text="")
        self.success_label.config(text="")
        size = (self.width_var.get(), self.height_var.get())
        characters = self.characters_combo.get()
        inverted = self.checkbox_var.get()
        if characters == "Custom...":
            tmp = None
            while tmp is None:
                tmp = simpledialog.askstring(
                    self.TITLE,
                    "Enter a list of characters, going downwards in luminosity (for example: \" .,:;=#\"). " +
                    "Do not include any extra punctuation.")
            characters = tmp
        try:
            result = self.backend.convert(size, characters, inverted)
            self.clipboard_clear()
            self.clipboard_append(result)
            self.update()
            self.success_label.config(text="Successfully converted and copied ASCII image to clipboard.")
            self.unlock_size_ratio()
        except Exception:
            self.error_label.config(text="Could not convert image and copy to clipboard, please try again.")

    def on_submit(self):
        self.error_label.config(text="")
        self.success_label.config(text="")
        size = (self.width_var.get(), self.height_var.get())
        characters = self.characters_combo.get()
        inverted = self.checkbox_var.get()
        if characters == "Custom...":
            tmp = None
            while tmp is None:
                tmp = simpledialog.askstring(
                    self.TITLE,
                    "Enter a list of characters, going downwards in luminosity (for example: \" .,:;=#\"). " +
                    "Do not include any extra punctuation.")
            characters = tmp
        try:
            result = self.backend.convert(size, characters, inverted)
            font_size = max(1, int(1024/size[1]))

            top = tk.Toplevel(self)
            top.title(self.TITLE)
            top.geometry(str(self.winfo_screenwidth())+"x"+str(self.winfo_screenheight()))

            text_area = scrolledtext.ScrolledText(top, wrap=tk.WORD, font=("Courier New", font_size))
            text_area.pack(expand=True, fill="both")
            text_area.insert(tk.END, result)
            text_area.config(state=tk.DISABLED)
            self.success_label.config(text="Successfully converted ASCII image.")
        except Exception as error:
            self.error_label.config(text="Could not convert image and display it, please try again.")

    def on_exit(self):
        self.destroy()
        exit(0)

if __name__ == "__main__":
    backend = Backend()
    app = App(backend)
    app.mainloop()
