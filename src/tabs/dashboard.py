# # dashboard.py
import customtkinter as ctk
import webview

class DashboardTab(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.metabase_url = "http://192.168.11.121:3001/dashboard/2-components"

        # Botón para abrir el dashboard en una ventana nueva
        self.open_dashboard_button = ctk.CTkButton(self, text="Abrir Dashboard", command=self.open_dashboard)
        self.open_dashboard_button.pack(pady=20)

    def open_dashboard(self):
        # Crear la ventana del dashboard
        webview.create_window("Dashboard de Metabase", self.metabase_url, width=1200, height=800)
        webview.start()

if __name__ == "__main__":
    root = ctk.CTk()
    app = DashboardTab(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()



# ###### NOTAS PARA V.2:

# ### Hacer Dashboard con PLOTLY