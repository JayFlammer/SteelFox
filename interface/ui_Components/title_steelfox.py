import customtkinter as ctk

def add_steelfox_text(title_canvas):
    logo_label = ctk.CTkLabel(title_canvas, text="SteelFox", font=("Helvetica", 24, "bold"), text_color="#FF8C00")
    logo_label.pack(side="left", padx=10, pady=10)