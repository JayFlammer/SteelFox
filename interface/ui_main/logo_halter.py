import customtkinter as ctk
from PIL import Image, ImageTk

def add_halter_logo(title_canvas):
    try:
        halter_logo_path = "interface/ui_components/Halter_Logo_Weiss_RGB.png"
        halter_logo_image = Image.open(halter_logo_path)
        max_width, max_height = 93.75, 90
        halter_logo_image.thumbnail((max_width, max_height), Image.LANCZOS)
        halter_logo_photo = ImageTk.PhotoImage(halter_logo_image)
        halter_image_label = ctk.CTkLabel(title_canvas, image=halter_logo_photo, text="")
        halter_image_label.image = halter_logo_photo
        halter_image_label.pack(side="right", padx=20, pady=10)
    except Exception as e:
        print(f"Fehler beim Laden des Halter Bildes: {e}")