from PIL import Image

class ImageProcessingError(Exception):
    """Custom exception for image processing errors."""
    pass


class Backend:
    FONT_RATIO = 0.44

    def __init__(self):
        self.image = None

    def load_file(self, filepath: str) -> None:
        """Load image from a file."""
        try:
            self.image = Image.open(filepath)
        except Exception as e:
            raise ImageProcessingError(f"Could not open file: {filepath}") from e

    def load_clipboard(self, image: Image.Image) -> None:
        """Load image from clipboard (expects a PIL.Image object)."""
        if image is None:
            raise ImageProcessingError("No image found in clipboard")
        self.image = image

    def to_ascii(self, size: tuple[int, int], characters: str, inverted: bool) -> str:
        """Convert the current image to ASCII art."""
        if self.image is None:
            raise ImageProcessingError("No image loaded")

        if not isinstance(size, tuple) or len(size) != 2:
            raise ValueError("Size must be a tuple of two integers (width, height)")
        if not characters or not isinstance(characters, str):
            raise ValueError("Characters must be a non-empty string")

        width, height = size[0], int(size[1] * self.FONT_RATIO)
        image = self.image.resize((width, height)).convert("L")

        if inverted:
            characters = characters[::-1]
        length = len(characters) - 1

        data = image.getdata()
        ascii_str = ""
        for y in range(height):
            for x in range(width):
                pixel = data[y * width + x]
                ascii_str += characters[(pixel * length) // 255]
            ascii_str += "\n"

        return ascii_str
