import customtkinter as ctk
from PIL import Image, ImageTk

def add_steelfox_logo(title_canvas):
    try:
        image_path = "interface/ui_components/Logo.png"
        logo_image = Image.open(image_path)
        logo_image.thumbnail((70, 70), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        image_label = ctk.CTkLabel(title_canvas, image=logo_photo, text="")
        image_label.image = logo_photo
        image_label.pack(side="left", padx=10, pady=10)
    except Exception as e:
        print(f"Fehler beim Laden des Bildes: {e}")