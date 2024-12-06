import customtkinter as ctk


def create_main_frame(root):
    """Erstellt den Mainframe der Hinter über den ganzen Bildschirm"""
    main_frame = ctk.CTkFrame(root, corner_radius=0)
    main_frame.pack(fill="both", expand=True)
    return main_frame