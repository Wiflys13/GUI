import customtkinter as ctk
import requests
from tkinter import messagebox

class ComponentsTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = ctk.CTkLabel(self, text="Components", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)
        # Añadir más widgets y funcionalidades según sea necesario

    # Agregar métodos similares a los de ComponentsTab según sea necesario