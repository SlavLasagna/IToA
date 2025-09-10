from ascii_converter import ASCIIConverter
from ui.app import App

if __name__ == "__main__":
    converter = ASCIIConverter()
    app = App(converter)
    app.mainloop()
