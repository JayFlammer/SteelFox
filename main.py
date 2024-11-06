import tkinter as tk
from interface_folder.interface_widgets import create_widgets

def main():
    root = tk.Tk()
    root.title("IFC Datenmanager")
    app = tk.Frame(root)
    app.root = root
    create_widgets(app)
    root.mainloop()

if __name__ == "__main__":
    print("Programm gestartet")  # Diesen Print-Befehl hinzufügen
    main()
