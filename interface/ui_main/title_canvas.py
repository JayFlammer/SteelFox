import customtkinter as ctk

def create_title_canvas(main_frame):
    """Erstellt den Titelstreifen"""
    title_canvas = ctk.CTkCanvas(main_frame, bg="#C9B1BD", height=100, highlightthickness=0)
    title_canvas.pack(side="top", fill="x")
    return title_canvas