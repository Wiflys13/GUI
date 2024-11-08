# orders_tab.py
import sys
project_root = 'C:/Users/HARMONI/Documents/HARMONI/HRM_BBDD'
sys.path.append(project_root)
from config.config import URL_LOCAL, URL_VPN
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import requests
import logging
from datetime import datetime, timezone


class OrdersTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.configure(bg_color="white")

        # Configurar la cuadrícula general
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)

        # Crear las áreas
        self.create_general_order_info()  # Área superior
        self.create_search_area()         # Área izquierda
        self.create_order_area()          # Área central
        
    def create_general_order_info(self):
        """Crea la parte superior con los datos generales del pedido."""
        general_info_frame = ctk.CTkFrame(self)
        general_info_frame.grid(row=0, column=0, columnspan=3, sticky="nswe", padx=10, pady=10)

        title_label = ctk.CTkLabel(general_info_frame, text="Datos Generales del Pedido", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        general_scrollable_frame = ctk.CTkScrollableFrame(general_info_frame)
        general_scrollable_frame.pack(fill="both", expand=True)

        fields = ["ID Pedido", "Nombre Pedido", "Cuenta", "WP", "Estado", "Tipo", "Descripción", "Cab Reference"]
        self.general_entries = {}

        # Definir opciones para los campos de tipo Combobox
        opciones_estado = ["", "Estado 1", "Estado 2", "Estado 3"]
        opciones_cuenta = ["", "Cuenta 1", "Cuenta 2", "Cuenta 3"]
        opciones_wp = ["", "WP 1", "WP 2", "WP 3"]
        opciones_tipo = ["", "Tipo 1", "Tipo 2", "Tipo 3"]

        for field in fields:
            frame = ctk.CTkFrame(general_scrollable_frame)
            frame.pack(fill="x", pady=5)

            label = ctk.CTkLabel(frame, text=field)
            label.pack(side="left", padx=5)

            if field == "Estado":
                combo = ttk.Combobox(frame, values=opciones_estado, state="readonly")
                combo.pack(side="left", fill="x", padx=5, expand=True)
                self.general_entries[field] = combo

            elif field == "Cuenta":
                combo = ttk.Combobox(frame, values=opciones_cuenta, state="readonly")
                combo.pack(side="left", fill="x", padx=5, expand=True)
                self.general_entries[field] = combo

            elif field == "WP":
                combo = ttk.Combobox(frame, values=opciones_wp, state="readonly")
                combo.pack(side="left", fill="x", padx=5, expand=True)
                self.general_entries[field] = combo

            elif field == "Tipo":
                combo = ttk.Combobox(frame, values=opciones_tipo, state="readonly")
                combo.pack(side="left", fill="x", padx=5, expand=True)
                self.general_entries[field] = combo

            else:
                entry = ctk.CTkEntry(frame, placeholder_text=f"Ingrese {field}")
                entry.pack(side="left", fill="x", padx=5, expand=True)
                self.general_entries[field] = entry

        button_frame = ctk.CTkFrame(general_info_frame)
        button_frame.pack(fill="x", pady=10)

        search_button = ctk.CTkButton(button_frame, text="Buscar", command=self.search_order)
        search_button.pack(side="left", padx=5)
        
        generate_button = ctk.CTkButton(button_frame, text="Generar", command=self.generate_order)
        generate_button.pack(side="left", padx=5)

        clear_button = ctk.CTkButton(button_frame, text="Limpiar Orders", command=self.clear_order_fields)
        clear_button.pack(side="left", padx=5)

    def search_order(self):
        """Busca un pedido por ID y muestra los detalles en un pop-up."""
        order_id = self.general_entries["ID Pedido"].get()
        order_id = order_id.upper()
        
        if not order_id:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un ID de pedido.")
            return

        url = f'{URL_VPN}/orders/{order_id}'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza un error si la respuesta fue un error
            
            order_data = response.json()
            logging.debug(f"Datos del pedido recibidos: {order_data}")  # Añadir debug aquí

            # Mostrar los datos en un pop-up
            self.show_order_details_in_popup(order_data)
        
        except requests.exceptions.HTTPError as err:
            messagebox.showerror("Error", f"No se pudo encontrar el pedido: {err}")
            
    def show_order_details_in_popup(self, order_data):
        """Muestra los detalles del pedido en una ventana emergente."""
        
        popup = ctk.CTkToplevel(self)
        popup.title("Detalles del Pedido")
        popup.geometry("600x400")
        popup.attributes("-topmost", True)

        details_frame = ctk.CTkFrame(popup)
        details_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Crear un Treeview para mostrar los detalles del pedido
        tree = ttk.Treeview(details_frame, show="headings")
        tree.pack(side="left", fill="both", expand=True)

        h_scrollbar = ttk.Scrollbar(details_frame, orient="horizontal", command=tree.xview)
        h_scrollbar.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=h_scrollbar.set)

        v_scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=tree.yview)
        v_scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=v_scrollbar.set)

        # Mostrar los detalles del pedido
        columns = list(order_data.keys())
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col.replace('_', ' ').title())
            tree.column(col, width=150, anchor='w')

        values = [order_data.get(col, "") for col in columns]
        tree.insert("", "end", iid=0, text="", values=values)

        def edit_order():
            """Edita el pedido seleccionado y llena los campos de Datos Generales del Pedido."""
            # Rellena los campos de Datos Generales de Pedido solo si hay datos disponibles
            if order_data.get('name'):
                self.general_entries["Nombre Pedido"].insert(0, order_data['name'])
            if order_data.get('description'):
                self.general_entries["Descripción"].insert(0, order_data['description'])
            if order_data.get('account'):
                self.general_entries["Cuenta"].insert(0, order_data['account'])
            if order_data.get('wp'):
                self.general_entries["WP"].insert(0, order_data['wp'])
            if order_data.get('status'):
                self.general_entries["Estado"].insert(0, order_data['status'])
            if order_data.get('order_type'):
                self.general_entries["Tipo"].insert(0, order_data['order_type'])
            if order_data.get('cab_reference'):
                self.general_entries["Cab Reference"].insert(0, order_data['cab_reference'])

            # Asegurarse de que todos los componentes se añadan a la tabla de 'Pedido Actual'
            components = order_data.get('components', [])
            for component in components:
                values = [
                    component.get('ci_identification', ''),
                    component.get('name', ''),
                    component.get('acronym', ''),
                    component.get('supplier', ''),
                    component.get('manufacturer', ''),
                    component.get('manufacturer_part_number', ''),
                    component.get('catalog_reference', ''),
                    component.get('cost_unit', 0.0),
                    component.get('quantity', 1)
                ]
                # Insertar cada componente en el árbol de la tabla de "Pedido Actual"
                self.orders_tree.insert("", "end", values=values)

            # Cerrar el pop-up al final de la edición
            popup.destroy()

        # Usa una lambda para pasar los argumentos correctamente
        edit_button = ctk.CTkButton(popup, text="Editar Pedido", command=edit_order)
        edit_button.pack(pady=10)

        close_button = ctk.CTkButton(popup, text="Cerrar", command=popup.destroy)
        close_button.pack(pady=5)

        
    def add_component_to_current_order(self, order_data):
        """Agrega los componentes del pedido actual al área de Pedido Actual."""
        components = order_data.get('components', [])
        
        if components:
            for component in components:
                values = [
                    component['ci_identification'],
                    component.get('name', ''),
                    component.get('acronym', ''),
                    component.get('supplier', ''),
                    component.get('manufacturer', ''),
                    component.get('manufacturer_part_number', ''),
                    component.get('catalog_reference', ''),
                    str(component.get('cost_unit', 0)),
                    str(component.get('quantity', 0))
                ]
                # Inserta los valores en el Treeview (tabla) de Pedido Actual
                self.orders_tree.insert("", "end", values=values)
            
            # Mensaje de éxito
            messagebox.showinfo("Éxito", "Componentes añadidos al pedido actual.")
        else:
            # Si no hay componentes, muestra una advertencia
            messagebox.showwarning("Advertencia", "No hay componentes en este pedido.")

    def generate_order(self):
        """Genera o actualiza un pedido con los componentes añadidos."""
        selected_items = self.orders_tree.get_children()
        components = []

        if selected_items:
            for item in selected_items:
                item_values = self.orders_tree.item(item, 'values')
                component_detail = {
                    "ci_identification": item_values[0],
                    "name": item_values[1],
                    "acronym": item_values[2],
                    "supplier": item_values[3],
                    "manufacturer": item_values[4],
                    "manufacturer_part_number": item_values[5],
                    "catalog_reference": item_values[6],
                    "cost_unit": float(item_values[7]) if item_values[7] else 0.0,
                    "quantity": int(item_values[8]) if item_values[8] else 1
                }
                components.append(component_detail)

            order_id = self.general_entries["ID Pedido"].get() or None  # Utilizar order_id si existe

            order_payload = {
                "order_id": order_id,
                "name": self.general_entries["Nombre Pedido"].get(),
                "account": self.general_entries["Cuenta"].get() or None,
                "wp": self.general_entries["WP"].get() or None,
                "total_amount": sum(comp["cost_unit"] * comp["quantity"] for comp in components),
                "state": self.general_entries["Estado"].get() or None,
                "order_type": self.general_entries["Tipo"].get() or None,
                "description": self.general_entries["Descripción"].get(),
                "cab_reference": self.general_entries["Cab Reference"].get(),
                "components": components
            }

            url = f'{URL_VPN}/orders/'
            try:
                response = requests.post(url, json=order_payload)
                response.raise_for_status()
                messagebox.showinfo("Éxito","El pedido ha sido creado o actualizado con éxito.")
            except requests.exceptions.HTTPError as err:
                print(f"Error: {err}")
                messagebox.showerror("Error", "No se pudo crear o actualizar el pedido.")
        else:
            messagebox.showwarning("Advertencia", "No hay componentes en el pedido actual.")


    def create_search_area(self):
        """Crea la sección izquierda con los campos de búsqueda."""
        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=1, column=0, sticky="nswe", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(search_frame, text="Búsqueda de Componentes", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        search_scrollable_frame = ctk.CTkScrollableFrame(search_frame)
        search_scrollable_frame.pack(fill="both", expand=True)

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
        for label_text, endpoint in self.fields.items():
            field_frame = ctk.CTkFrame(search_scrollable_frame)
            field_frame.pack(pady=5, fill="x")

            label = ctk.CTkLabel(field_frame, text=label_text)
            label.pack(side="left", padx=5, pady=5)

            entry = ctk.CTkEntry(field_frame, width=150, placeholder_text=f"Ingrese {label_text}")
            entry.pack(side="left", padx=5, pady=5)
            self.entries[endpoint] = entry

        search_button = ctk.CTkButton(search_frame, text="Buscar", command=self.perform_search)
        search_button.pack(pady=10)

    def create_order_area(self):
        """Crea la sección central para el pedido actual."""
        order_frame = ctk.CTkFrame(self)
        order_frame.grid(row=1, column=1, sticky="nswe", padx=10, pady=10)

        title_label = ctk.CTkLabel(order_frame, text="Pedido Actual", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        table_frame = ctk.CTkFrame(order_frame)
        table_frame.pack(fill="both", expand=True)

        self.orders_tree = ttk.Treeview(table_frame, show="headings", selectmode="browse")
        self.orders_tree.pack(side="left", fill="both", expand=True)

        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.orders_tree.yview)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.orders_tree.xview)
        h_scrollbar.pack(side="bottom", fill="x")
        self.orders_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        columns = ["CI Identification", "Name", "Acronym", "Supplier", "Manufacturer", "Manufacturer Part Number", 
                "Catalog Reference", "Cost Unit", "Quantity"]
        self.orders_tree["columns"] = columns
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=100, anchor='w', stretch=False)

        self.orders_tree.bind("<Double-1>", self.on_double_click)

        delete_button = ctk.CTkButton(order_frame, text="Eliminar", command=self.delete_order)
        delete_button.pack(side="right", padx=5)
        
        add_component_button = ctk.CTkButton(order_frame, text="Agregar a ComponentsDetail", command=self.add_to_components_detail)
        add_component_button.pack(side="left", padx=5)
        
        self.orders_tree.bind("<Delete>", self.delete_order)
        
    def add_to_components_detail(self):
        """Agrega todos los componentes de la tabla a ComponentsDetail."""
        selected_items = self.orders_tree.get_children()  # Obtiene todos los elementos
        added_successfully = True  # Variable para rastrear si se añaden todos los componentes

        if selected_items:
            for item in selected_items:
                item_values = self.orders_tree.item(item, 'values')
                
                # Asegúrate de que estos índices sean correctos según la estructura de tu tabla
                payload = {
                    "ci_identification": item_values[0],  # CI Identification
                    "name": item_values[1],                # Asumiendo que el nombre es el segundo elemento
                    "acronym": item_values[2],             # Asumiendo que el acrónimo es el tercer elemento
                    "supplier": item_values[3],            # Proveedor
                    "manufacturer": item_values[4],        # Fabricante
                    "manufacturer_part_number": item_values[5],  # Número de parte del fabricante
                    "catalog_reference": item_values[6],   # Referencia del catálogo
                    "cost_unit": float(item_values[7]) if item_values[7] else 0.0,  # Convertir a float
                    "quantity": int(item_values[8]) if item_values[8] else 0  # Convertir a int
                }
                
                # Enviar la solicitud a la API
                url = f'{URL_VPN}/ComponentDetail/'  # Cambia esta URL al endpoint correcto
                
                try:
                    response = requests.post(url, json=payload)
                    response.raise_for_status()  # Lanza un error si la respuesta fue un error
                except requests.exceptions.HTTPError as err:
                    print(f"Error al añadir el componente {item_values[0]}:", err)
                    added_successfully = False  # Cambiar a False si hay un error

        # Mostrar mensaje final según el resultado
        if added_successfully:
            messagebox.showinfo("Éxito", "Componentes añadidos con éxito.")
        else:
            messagebox.showerror("Error", "No se han podido añadir algunos componentes.")
        
    def delete_order(self, event=None):
        """Eliminar una fila de la tabla del área central."""
        selected_item = self.orders_tree.focus()
        if selected_item:
            self.orders_tree.delete(selected_item)
            messagebox.showinfo("Éxito", "Fila eliminada con éxito.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una fila para eliminar.")

    def perform_search(self):
        """Recopila los filtros de búsqueda y llama a la función de búsqueda."""
        search_filters = {}
        for endpoint, entry in self.entries.items():
            search_term = entry.get()
            if search_term:
                search_filters[endpoint] = search_term

        if search_filters:
            self.search_component(search_filters)
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un valor en al menos uno de los campos de búsqueda.")

    def search_component(self, search_filters):
        """Envía la búsqueda al servidor y maneja la respuesta."""
        try:
            url = f'{URL_VPN}/PBS/search'
            response = requests.post(url, json=search_filters)  # Aquí usas POST y envías el diccionario como JSON
            
            # Verifica si la respuesta fue exitosa
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP >= 400
            
            try:
                search_results = response.json()  # Intenta parsear la respuesta como JSON
                
                if search_results:
                    self.show_components_results_in_popup(search_results)
                else:
                    messagebox.showinfo("Sin Resultados", "No se encontraron resultados para la búsqueda.")
            
            except requests.exceptions.JSONDecodeError:
                messagebox.showerror("Error", f"La respuesta no es un JSON válido: {response.text}")
        
        except requests.exceptions.HTTPError as http_err:
            messagebox.showerror("Error", f"Error HTTP al buscar componentes: {http_err}")
        except requests.exceptions.RequestException as req_err:
            messagebox.showerror("Error", f"Error de conexión al servidor: {req_err}")

    def show_components_results_in_popup(self, data):
        """Muestra los resultados de búsqueda en una ventana emergente."""
        popup = ctk.CTkToplevel(self)
        popup.title("Resultados de Búsqueda")
        popup.geometry("800x600")

        popup.attributes("-topmost", True)
        popup.grab_set()  # Hace que la ventana sea modal

        tree_frame = ctk.CTkFrame(popup)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(tree_frame, show="headings")
        tree.pack(side="left", fill="both", expand=True)

        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        h_scrollbar.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=h_scrollbar.set)

        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        v_scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=v_scrollbar.set)

        if isinstance(data, list) and data:
            columns = list(data[0].keys())
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col.replace('_', ' ').title())
                tree.column(col, width=100, anchor='w')

            for index, item in enumerate(data):
                values = [item.get(col, "") for col in columns]
                tree.insert("", "end", iid=index, text="", values=values)
        else:
            tree["columns"] = ["No se encontraron resultados"]
            tree.heading("#0", text="")
            tree.insert("", "end", text="No se encontraron resultados")

        # Aquí se pasa `popup` al lambda
        add_button = ctk.CTkButton(popup, text="Añadir al Pedido", command=lambda: self.add_selected_to_order(tree, data, popup))
        add_button.pack(pady=10)


    def add_selected_to_order(self, tree, data, popup):
        """Agrega los componentes seleccionados del popup a la tabla de pedidos."""
        selected_items = tree.selection()
        if selected_items:
            for selected_item in selected_items:
                item_data = data[int(selected_item)]
                ci_identification = str(item_data["ci_identification"])  # Asegúrate de que sea un string

                # Verificar si el ci_identification ya existe en la tabla
                exists = False
                for child in self.orders_tree.get_children():
                    # Asegúrate de comparar como strings
                    if str(self.orders_tree.item(child)["values"][0]) == ci_identification:
                        exists = True
                        break

                # Si no existe, añadir el componente
                if not exists:
                    values = [ci_identification, item_data["name"], item_data["acronym"]]
                    self.orders_tree.insert("", "end", values=values + [""] * (len(self.orders_tree["columns"]) - 3))
                    
                    # Mostrar messagebox de éxito
                    messagebox.showinfo("Éxito", "Componentes añadidos al pedido.", parent=popup)
                else:
                    # Mostrar messagebox de advertencia
                    messagebox.showwarning("Advertencia", f"El componente con CI '{ci_identification}' ya está en el pedido.", parent=popup)
        else:
            # Mostrar messagebox de advertencia
            messagebox.showwarning("Advertencia", "Seleccione al menos un componente.", parent=popup)

        popup.grab_release()  # Libera el enfoque de la ventana modal


    def on_double_click(self, event):
        """Abrir ventana emergente para editar componente al hacer doble clic."""
        selected_item = self.orders_tree.focus()
        if selected_item:
            item_values = self.orders_tree.item(selected_item, "values")
            self.open_edit_popup(item_values, selected_item)

    def open_edit_popup(self, item_values, selected_item):
        """Abrir ventana emergente para editar los campos de un componente seleccionado."""
        popup = ctk.CTkToplevel(self)
        popup.title("Editar Componente")
        popup.geometry("500x400")

        popup_scrollable_frame = ctk.CTkScrollableFrame(popup)
        popup_scrollable_frame.pack(fill="both", expand=True)

        fields = ["Supplier", "Manufacturer", "Manufacturer Part Number", "Catalog Reference", "Cost Unit", "Quantity"]
        self.edit_entries = {}
        for index, field in enumerate(fields):
            frame = ctk.CTkFrame(popup_scrollable_frame)
            frame.pack(fill="x", pady=5)
            
            label = ctk.CTkLabel(frame, text=field)
            label.pack(side="left", padx=5)
            
            entry = ctk.CTkEntry(frame, placeholder_text=f"Ingrese {field}")
            entry.pack(side="left", fill="x", padx=5, expand=True)
            self.edit_entries[field] = entry
            if index < len(item_values) - 3:
                entry.insert(0, item_values[index + 3])

        save_button = ctk.CTkButton(popup, text="Guardar", command=lambda: self.save_changes(selected_item, item_values))
        save_button.pack(pady=10)

    def save_changes(self, selected_item, item_values):
        """Guardar los cambios realizados en el componente."""
        new_values = list(item_values[:3])
        for field in ["Supplier", "Manufacturer", "Manufacturer Part Number", "Catalog Reference", "Cost Unit", "Quantity"]:
            new_values.append(self.edit_entries[field].get())

        self.orders_tree.item(selected_item, values=new_values)
        messagebox.showinfo("Éxito", "Cambios guardados con éxito.")

    def clear_order_fields(self):
        """Limpia todos los campos de Datos Generales de Pedido y Pedido Actual, incluyendo los Combobox."""
        # Limpiar los campos de Datos Generales de Pedido
        for entry in self.general_entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set('')  # Vaciar el contenido del Combobox
            else:
                entry.delete(0, 'end')  # Vaciar el contenido de los campos de texto (CTkEntry)

        # Limpiar la tabla de Pedido Actual
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)  # Eliminar todas las filas
