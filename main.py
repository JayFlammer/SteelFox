import customtkinter as ctk
from interface_main import SteelFoxApp

if __name__ == "__main__":
    # Erstelle ein CustomTkinter-Fenster
    root = ctk.CTk()

    # Initialisiere die App mit dem CTk-Fenster
    app = SteelFoxApp(root)

    # Starte die Haupt-Event-Schleife
    root.mainloop()


