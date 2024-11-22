import customtkinter as ctk

def create_version_label(input_frame):
    version_label = ctk.CTkLabel(input_frame, text="v1.2", font=("Helvetica", 8), text_color="#000000", width=300)
    version_label.pack(side="bottom", anchor='w', padx=10, pady=5)