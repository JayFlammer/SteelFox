import customtkinter as ctk
from PIL import Image

def add_halter_logo(title_canvas):
    try:
        halter_logo_path = "interface/canvas/logo-hier-stehen.png"

        # Bild mit PIL laden
        halter_logo_image = Image.open(halter_logo_path)

        # Maximale Abmessungen
        max_width, max_height = 93.75, 90

        # Seitenverhältnis beibehalten
        original_width, original_height = halter_logo_image.size
        aspect_ratio = original_width / original_height

        if original_width > original_height:
            # Breite dominiert, Höhe anpassen
            width = max_width
            height = int(max_width / aspect_ratio)
        else:
            # Höhe dominiert, Breite anpassen
            height = max_height
            width = int(max_height * aspect_ratio)

        # CTkImage erstellen mit den neuen Abmessungen
        halter_logo_ctk_image = ctk.CTkImage(light_image=halter_logo_image, dark_image=halter_logo_image, size=(width, height))
        
        # CTkLabel erstellen und CTkImage verwenden
        halter_image_label = ctk.CTkLabel(title_canvas, image=halter_logo_ctk_image, text="")
        halter_image_label.pack(side="right", padx=20, pady=10)

    except Exception as e:
        print(f"Fehler beim Laden des Halter Bildes: {e}")
