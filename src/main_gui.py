#main_gui.py
import customtkinter as ctk
from tabs.pbs_tab import PBSTab
from tabs.components_tab import ComponentsTab
from tabs.orders_tab import OrdersTab
from tabs.documents_tab import DocumentsTab
from tabs.administration_tab import AdministrationTab
from tabs.dashboard import DashboardTab


# Constantes para los títulos de las pestañas
TAB_TITLES = ["PBS", "Components" ,"Orders", "Administración", "Documents", "Dashboard"]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Base de Datos de Harmoni - CAB")
        self.geometry("1600x800")

        self.create_ui()

    def create_ui(self):
        # Configuración de la cuadrícula
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Crear la cabecera
        self.header_frame = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.header_frame.grid_propagate(False)

        self.header_label = ctk.CTkLabel(self.header_frame, text="Base de Datos de Harmoni - CAB", font=("Arial", 24, "bold"))
        self.header_label.pack(pady=15)

        # Crear las pestañas
        self.tabview = ctk.CTkTabview(self, width=1600, height=800)
        self.tabview.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # Agregar las pestañas
        for title in TAB_TITLES:
            self.tabview.add(title)

        # Agregar el contenido a las pestañas
        self.tabs = {
            "PBS": PBSTab(self.tabview.tab("PBS")),
            "Components" : ComponentsTab(self.tabview.tab("Components")),
            "Orders": OrdersTab(self.tabview.tab("Orders")),
            "Administración": AdministrationTab(self.tabview.tab("Administración")),
            "Documents": DocumentsTab(self.tabview.tab("Documents")),
            "Dashboard": DashboardTab(self.tabview.tab("Dashboard"))
        }

        for tab in self.tabs.values():
            tab.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()