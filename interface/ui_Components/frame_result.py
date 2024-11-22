import customtkinter as ctk

def create_result_frame(main_frame):
    result_frame = ctk.CTkFrame(main_frame, fg_color="#000000", corner_radius=0)
    result_frame.pack(side="left", fill="both", expand=True)
    return result_frame