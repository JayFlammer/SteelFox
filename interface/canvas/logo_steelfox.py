import customtkinter as ctk
from PIL import Image

def add_steelfox_logo(title_canvas):
    try:
        image_path = "interface/canvas/Logo.png"
        
        # Bild mit PIL laden
        logo_image = Image.open(image_path)
        
        # CTkImage erstellen und Größe setzen
        max_width, max_height = 70, 70
        logo_ctk_image = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(max_width, max_height))
        
        # CTkLabel erstellen und CTkImage verwenden
        image_label = ctk.CTkLabel(title_canvas, image=logo_ctk_image, text="")
        image_label.pack(side="left", padx=10, pady=10)

    except Exception as e:
        print(f"Fehler beim Laden des Bildes: {e}")
