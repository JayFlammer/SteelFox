import customtkinter as ctk

def create_result_frame(main_frame):
    result_frame = ctk.CTkFrame(main_frame, fg_color="#000000", corner_radius=0)
    result_frame.pack(side="left", fill="both", expand=True)
    info_label = ctk.CTkLabel(result_frame, text="Lade bitte alle benötigten Dateien hoch um die Auswertung starten zu können", font=("Helvetica", 12), text_color="#ffffff")
    info_label.place(relx=0.5, rely=0.5, anchor='center')
    return result_frame