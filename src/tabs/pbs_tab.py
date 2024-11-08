#PBS_tab.py
from config.config import URL_VPN
import pandas as pd
import customtkinter as ctk
import requests
from tkinter import messagebox, ttk
from tkinter import filedialog

class PBSTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.configure(bg_color="white")  # Configuración del fondo del marco

        # Configuración de la cuadrícula para la disposición de los widgets
        self.grid_columnconfigure(0, weight=1)  # Barra lateral
        self.grid_columnconfigure(1, weight=2)  # Contenedor de búsqueda
        self.grid_columnconfigure(2, weight=4)  # Contenedor de resultados
        self.grid_rowconfigure(0, weight=0)     # Espacio para la cabecera
        self.grid_rowconfigure(1, weight=1)     # Contenedor de búsqueda

        # Creación de la barra lateral de opciones
        self.create_sidebar()

        # Contenedor de búsqueda con scrollbar
        self.create_search_frame()

    def create_sidebar(self):
        """Crea y configura la barra lateral con botones de acción."""
        self.left_sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.left_sidebar_frame.grid(row=1, column=0, sticky="nswe")
        self.left_sidebar_frame.grid_propagate(False)

        # Título de la barra lateral
        self.logo_label = ctk.CTkLabel(self.left_sidebar_frame, text="Opciones", font=("Arial", 18, "bold"))
        self.logo_label.pack(pady=(20, 10))

        # Botones de acción
        self.insert_button = ctk.CTkButton(self.left_sidebar_frame, text="Insertar", command=self.insert_data)
        self.insert_button.pack(pady=10)

        self.update_button = ctk.CTkButton(self.left_sidebar_frame, text="Actualizar", command=self.update_data)
        self.update_button.pack(pady=10)

        self.search_button = ctk.CTkButton(self.left_sidebar_frame, text="Buscar", command=self.perform_search)
        self.search_button.pack(pady=10)

        self.search_all_button = ctk.CTkButton(self.left_sidebar_frame, text="Buscar todos", command=self.search_all)
        self.search_all_button.pack(pady=10)

    def create_search_frame(self):
        """Crea y configura el marco de búsqueda con campos de entrada."""
        self.search_frame = ctk.CTkFrame(self, corner_radius=0)
        self.search_frame.grid(row=1, column=1, sticky="nswe")
        self.search_frame.grid_propagate(False)

        # Scrollable Frame dentro del contenedor de búsqueda
        self.scrollable_search_frame = ctk.CTkScrollableFrame(self.search_frame)
        self.scrollable_search_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Definición de campos de búsqueda
        self.fields = {
            "CI Identification": "ci_identification",
            "Name": "name",
            "Acronym": "acronym",
            "System": "system",
            "Subsystem": "subsystem",
            "Module": "module",
            "Unit": "unit",
            "Assembly": "assembly",
            "Subassembly": "subassembly",
            "Component": "component"
        }

        self.entries = {}
        self.field_labels = []

        # Creación de entradas para los campos de búsqueda
        for label_text, endpoint in self.fields.items():
            field_frame = ctk.CTkFrame(self.scrollable_search_frame)
            field_frame.pack(pady=5, fill="x")

            # Etiqueta y campo de entrada
            label = ctk.CTkLabel(field_frame, text=label_text)
            label.pack(side="left", padx=5, pady=5)

            entry = ctk.CTkEntry(field_frame, width=150, placeholder_text=f"Ingrese {label_text}")
            entry.pack(side="left", padx=5, pady=5)
            self.entries[endpoint] = entry
            self.field_labels.append(label_text)

    def perform_search(self):
        """Recopila los filtros de búsqueda y llama a la función de búsqueda."""
        search_filters = {}
        for endpoint, entry in self.entries.items():
            search_term = entry.get()
            if search_term:
                search_filters[endpoint] = search_term  # Añade solo los campos con valor

        # Verifica si al menos un campo tiene un valor
        if search_filters:
            self.search_component(search_filters)
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un valor en al menos uno de los campos de búsqueda.")
            
    def search_all(self):
        """Obtener todos los componentes"""
        try:
            url = f'{URL_VPN}/PBS/search'
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                if result:
                    self.show_results_in_popup(result)
                else:
                    messagebox.showinfo("Sin Resultados", "No se encontraron resultados para la búsqueda.")
            else:
                messagebox.showerror("Error", f"Error en la búsqueda: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_component(self, search_filters):
        """Envía la búsqueda al servidor y maneja la respuesta."""
        try:
            url = f'{URL_VPN}/PBS/search'
            response = requests.post(url, json=search_filters)  # Aquí usas POST y envías el diccionario como JSON
            if response.status_code == 200:
                result = response.json()
                if result:
                    self.show_results_in_popup(result)
                else:
                    messagebox.showinfo("Sin Resultados", "No se encontraron resultados para la búsqueda.")
            else:
                messagebox.showerror("Error", f"Error en la búsqueda: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_results_in_popup(self, data):
        """Muestra los resultados de búsqueda en una ventana emergente."""
        # Crear el popup
        popup = ctk.CTkToplevel(self)
        popup.title("Resultados de Búsqueda")
        popup.geometry("800x600")
        
        # Asegúrate de que el popup siempre esté encima
        popup.attributes("-topmost", True)

        # Crear un frame para el Treeview y su scrollbar horizontal
        tree_frame = ctk.CTkFrame(popup)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Configurar el Treeview
        tree = ttk.Treeview(tree_frame, show="headings")
        tree.pack(side="left", fill="both", expand=True)

        # Barra de desplazamiento horizontal
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        h_scrollbar.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=h_scrollbar.set)

        # Barra de desplazamiento vertical
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        v_scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=v_scrollbar.set)

        # Mostrar los resultados en una tabla
        if isinstance(data, list) and data:
            columns = list(data[0].keys())
            tree["columns"] = columns
            tree.heading("#0", text="ID")
            for col in columns:
                tree.heading(col, text=col.replace('_', ' ').title())
                tree.column(col, width=100, anchor='w')  # Ajustar el ancho y alineación

            # Insertar datos en el Treeview
            for index, item in enumerate(data):
                values = [item.get(col, "") for col in columns]
                tree.insert("", "end", iid=index, text=index+1, values=values)
        else:
            tree["columns"] = ["No se encontraron resultados"]
            tree.heading("#0", text="")
            tree.insert("", "end", text="No se encontraron resultados")

        # Botón de descarga CSV
        download_button = ctk.CTkButton(popup, text="Descargar CSV", command=lambda: self.download_csv(popup, tree))
        download_button.pack(pady=10)

        # Configurar el popup para que siempre esté encima
        popup.lift()  # Eleva el popup sobre otras ventanas
        popup.focus_force()  # Fuerza el foco en el popup

    def download_csv(self, popup, tree):
        """Descarga los resultados mostrados en el Treeview como un archivo CSV."""
        try:
            # Lleva el popup de resultados al frente para asegurarse de que no se minimice
            popup.lift()
            popup.attributes("-topmost", True)
            popup.attributes("-topmost", False)  # Restaurar el estado original

            # Abrir un cuadro de diálogo para elegir la ubicación y el nombre del archivo CSV
            file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if not file_path:
                return  # Salir si el usuario cancela el diálogo

            # Extraer los datos del Treeview
            data = []
            headers = [col for col in tree["columns"]]

            for item in tree.get_children():
                values = tree.item(item, 'values')
                # Convertir valores None a NaN
                row = [value if value is not None else pd.NA for value in values]
                data.append(row)

            # Crear un DataFrame de pandas
            df = pd.DataFrame(data, columns=headers)

            # Escribir el DataFrame en un archivo CSV
            df.to_csv(file_path, index=False, encoding='utf-8')

            # Mostrar mensaje de éxito después de que el cuadro de diálogo de descarga se cierre
            popup.after(100, lambda: messagebox.showinfo("Éxito", "Archivo CSV descargado correctamente."))
        except Exception as e:
            # Mostrar mensaje de error después de que el cuadro de diálogo de descarga se cierre
            popup.after(100, lambda: messagebox.showerror("Error", f"Error al guardar el archivo CSV: {str(e)}"))

    # Métodos dummy para los botones Insertar y Actualizar
    def insert_data(self):
        """Función de inserción (aún no implementada)."""
        messagebox.showinfo("Insertar", "Función Insertar aún no implementada")

    def update_data(self):
        """Función de actualización (aún no implementada)."""
        messagebox.showinfo("Actualizar", "Función Actualizar aún no implementada")
