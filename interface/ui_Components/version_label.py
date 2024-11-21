import customtkinter as ctk

def create_version_label(input_frame):
    version_label = ctk.CTkLabel(input_frame, text="v1.2", font=("Helvetica", 8), fg_color="#D3D3D3")
    version_label.pack(side="bottom", anchor='w', padx=10, pady=5)