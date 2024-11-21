import customtkinter as ctk

def create_input_frame(main_frame):
    input_frame = ctk.CTkFrame(main_frame, fg_color="#787575", width=10, corner_radius=0)
    input_frame.pack(side="left", fill="y")
    return input_frame