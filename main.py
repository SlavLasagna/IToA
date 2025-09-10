from backend import Backend
from ui.app import App

if __name__ == "__main__":
    backend = Backend()
    app = App(backend)
    app.mainloop()
