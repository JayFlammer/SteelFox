import tkinter as tk
from interface_widgets import create_widgets

class IFCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IFC Datenmanager")
        create_widgets(self)

if __name__ == "__main__":
    root = tk.Tk()
    app = IFCApp(root)
    root.mainloop()