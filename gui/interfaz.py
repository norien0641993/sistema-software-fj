# =============================================================================
# gui/interfaz.py - Interfaz Gráfica con Configuración Centralizada
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os

from config import config  # Importar la configuración
from sistema import SistemaSoftwareFJ
from modelos import SistemaError, ClienteInvalidoError

class AplicacionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(config.TITULO_APP)  # Usar título desde config
        self.root.geometry(config.TAMANO_VENTANA)  # Usar tamaño desde config
        self.root.resizable(True, True)

        # Inicializar el sistema
        self.sistema = SistemaSoftwareFJ()

        # Configurar el estilo
        estilo = ttk.Style()
        estilo.theme_use('clam')

        # Crear las pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Pestañas
        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_servicios = ttk.Frame(self.notebook)
        self.tab_reservas = ttk.Frame(self.notebook)
        self.tab_logs = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_clientes, text="Clientes")
        self.notebook.add(self.tab_servicios, text="Servicios")
        self.notebook.add(self.tab_reservas, text="Reservas")
        self.notebook.add(self.tab_logs, text="Logs del Sistema")

        # Construir cada pestaña
        self._construir_tab_clientes()
        self._construir_tab_servicios()
        self._construir_tab_reservas()
        self._construir_tab_logs()

        # Cargar datos iniciales en las tablas
        self._actualizar_tabla_clientes()
        self._actualizar_tabla_servicios()
        self._actualizar_tabla_reservas()

    # ---- Pestaña Clientes ----
    def _construir_tab_clientes(self):
        frame = self.tab_clientes

        frame_form = ttk.LabelFrame(frame, text="Registrar Nuevo Cliente")
        frame_form.pack(fill='x', padx=10, pady=10)

        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_nombre = ttk.Entry(frame_form, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Email:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.entry_email = ttk.Entry(frame_form, width=30)
        self.entry_email.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Teléfono:").grid(row=0, column=4, padx=5, pady=5, sticky='w')
        self.entry_telefono = ttk.Entry(frame_form, width=20)
        self.entry_telefono.grid(row=0, column=5, padx=5, pady=5)

        btn_registrar = ttk.Button(frame_form, text="Registrar Cliente", command=self._registrar_cliente)
        btn_registrar.grid(row=0, column=6, padx=10, pady=5)

        frame_tabla = ttk.LabelFrame(frame, text="Lista de Clientes")
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=5)

        self.tree_clientes = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Email", "Teléfono"), show="headings")
        self.tree_clientes.heading("ID", text="ID")
        self.tree_clientes.heading("Nombre", text="Nombre")
        self.tree_clientes.heading("Email", text="Email")
        self.tree_clientes.heading("Teléfono", text="Teléfono")
        self.tree_clientes.column("ID", width=50)
        self.tree_clientes.column("Nombre", width=200)
        self.tree_clientes.column("Email", width=250)
        self.tree_clientes.column("Teléfono", width=150)
        self.tree_clientes.pack(fill='both', expand=True, padx=5, pady=5)

        scroll_y = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tree_clientes.yview)
        scroll_y.pack(side='right', fill='y')
        self.tree_clientes.configure(yscrollcommand=scroll_y.set)

    def _registrar_cliente(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        telefono = self.entry_telefono.get().strip()

        try:
            if not nombre:
                raise ClienteInvalidoError("El nombre no puede estar vacío.")
            cliente = self.sistema.registrar_cliente(nombre, email, telefono)
            messagebox.showinfo("Éxito", f"Cliente '{nombre}' registrado correctamente con ID: {cliente.id}")
            self._actualizar_tabla_clientes()
            self.entry_nombre.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_telefono.delete(0, tk.END)
        except SistemaError as e:
            messagebox.showerror("Error", f"Error al registrar cliente: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def _actualizar_tabla_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        for cliente in self.sistema.obtener_clientes():
            self.tree_clientes.insert("", tk.END, values=(cliente.id, cliente.nombre, cliente.email, cliente.telefono))

    # ---- Pestaña Servicios ----
    def _construir_tab_servicios(self):
        frame = self.tab_servicios

        frame_tabla = ttk.LabelFrame(frame, text="Servicios Disponibles")
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=10)

        self.tree_servicios = ttk.Treeview(
            frame_tabla, 
            columns=("ID", "Nombre", "Descripción", "Costo Base", "Disponible"), 
            show="headings"
        )
        self.tree_servicios.heading("ID", text="ID")
        self.tree_servicios.heading("Nombre", text="Nombre")
        self.tree_servicios.heading("Descripción", text="Descripción")
        self.tree_servicios.heading("Costo Base", text="Costo Base")
        self.tree_servicios.heading("Disponible", text="Disponible")
        self.tree_servicios.column("ID", width=50)
        self.tree_servicios.column("Nombre", width=180)
        self.tree_servicios.column("Descripción", width=350)
        self.tree_servicios.column("Costo Base", width=120)
        self.tree_servicios.column("Disponible", width=80)
        self.tree_servicios.pack(fill='both', expand=True, padx=5, pady=5)

        scroll_y = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tree_servicios.yview)
        scroll_y.pack(side='right', fill='y')
        self.tree_servicios.configure(yscrollcommand=scroll_y.set)

    def _actualizar_tabla_servicios(self):
        for item in self.tree_servicios.get_children():
            self.tree_servicios.delete(item)
        for servicio in self.sistema.obtener_servicios():
            disponible = "Sí" if servicio.disponible else "No"
            # Usar el formateador de configuración
            precio_formateado = config.formatear_precio(servicio._costo_base)
            self.tree_servicios.insert("", tk.END, values=(
                servicio.id, 
                servicio.nombre, 
                servicio._descripcion, 
                precio_formateado,  # Ahora con formato COP
                disponible
            ))

    # ---- Pestaña Reservas ----
    def _construir_tab_reservas(self):
        frame = self.tab_reservas

        frame_crear = ttk.LabelFrame(frame, text="Crear Nueva Reserva")
        frame_crear.pack(fill='x', padx=10, pady=10)

        ttk.Label(frame_crear, text="ID Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.spin_cliente = ttk.Spinbox(frame_crear, from_=0, to=100, width=8)
        self.spin_cliente.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_crear, text="ID Servicio:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.spin_servicio = ttk.Spinbox(frame_crear, from_=0, to=100, width=8)
        self.spin_servicio.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_crear, text="Duración:").grid(row=0, column=4, padx=5, pady=5, sticky='w')
        self.spin_duracion = ttk.Spinbox(frame_crear, from_=1, to=100, width=8)
        self.spin_duracion.grid(row=0, column=5, padx=5, pady=5)
        ttk.Label(frame_crear, text="(horas/días según servicio)").grid(row=0, column=6, padx=5, pady=5, sticky='w')

        btn_crear = ttk.Button(frame_crear, text="Crear Reserva", command=self._crear_reserva)
        btn_crear.grid(row=0, column=7, padx=10, pady=5)

        frame_acciones = ttk.LabelFrame(frame, text="Acciones sobre Reservas")
        frame_acciones.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_acciones, text="ID Reserva:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.spin_accion = ttk.Spinbox(frame_acciones, from_=0, to=100, width=8)
        self.spin_accion.grid(row=0, column=1, padx=5, pady=5)

        btn_cancelar = ttk.Button(frame_acciones, text="Cancelar Reserva", command=self._cancelar_reserva)
        btn_cancelar.grid(row=0, column=2, padx=5, pady=5)

        btn_procesar = ttk.Button(frame_acciones, text="Procesar Reserva", command=self._procesar_reserva)
        btn_procesar.grid(row=0, column=3, padx=5, pady=5)

        frame_tabla = ttk.LabelFrame(frame, text="Lista de Reservas")
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=5)

        self.tree_reservas = ttk.Treeview(
            frame_tabla, 
            columns=("ID", "Cliente", "Servicio", "Duración", "Estado", "Costo Total"), 
            show="headings"
        )
        self.tree_reservas.heading("ID", text="ID")
        self.tree_reservas.heading("Cliente", text="Cliente")
        self.tree_reservas.heading("Servicio", text="Servicio")
        self.tree_reservas.heading("Duración", text="Duración")
        self.tree_reservas.heading("Estado", text="Estado")
        self.tree_reservas.heading("Costo Total", text="Costo Total")
        self.tree_reservas.column("ID", width=50)
        self.tree_reservas.column("Cliente", width=150)
        self.tree_reservas.column("Servicio", width=150)
        self.tree_reservas.column("Duración", width=80)
        self.tree_reservas.column("Estado", width=100)
        self.tree_reservas.column("Costo Total", width=120)
        self.tree_reservas.pack(fill='both', expand=True, padx=5, pady=5)

        scroll_y = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tree_reservas.yview)
        scroll_y.pack(side='right', fill='y')
        self.tree_reservas.configure(yscrollcommand=scroll_y.set)

    def _crear_reserva(self):
        try:
            id_cliente = int(self.spin_cliente.get())
            id_servicio = int(self.spin_servicio.get())
            duracion = int(self.spin_duracion.get())

            if duracion <= 0:
                raise ValueError("La duración debe ser positiva.")

            reserva = self.sistema.crear_reserva(id_cliente, id_servicio, duracion)
            # Usar el formateador de configuración
            precio_formateado = config.formatear_precio(reserva.costo_total)
            messagebox.showinfo("Éxito", 
                f"Reserva creada exitosamente.\n"
                f"ID: {reserva.id}\n"
                f"Estado: {reserva.estado}\n"
                f"Costo: {precio_formateado}")
            self._actualizar_tabla_reservas()
        except ValueError as e:
            messagebox.showerror("Error de entrada", f"Por favor, ingresa valores numéricos válidos.\n{e}")
        except SistemaError as e:
            messagebox.showerror("Error en el sistema", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def _cancelar_reserva(self):
        try:
            id_reserva = int(self.spin_accion.get())
            if self.sistema.cancelar_reserva(id_reserva):
                messagebox.showinfo("Éxito", f"Reserva {id_reserva} cancelada exitosamente.")
                self._actualizar_tabla_reservas()
        except ValueError:
            messagebox.showerror("Error de entrada", "Por favor, ingresa un ID de reserva válido.")
        except SistemaError as e:
            messagebox.showerror("Error en el sistema", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def _procesar_reserva(self):
        try:
            id_reserva = int(self.spin_accion.get())
            if self.sistema.procesar_reserva(id_reserva):
                messagebox.showinfo("Éxito", f"Reserva {id_reserva} procesada/completada exitosamente.")
                self._actualizar_tabla_reservas()
        except ValueError:
            messagebox.showerror("Error de entrada", "Por favor, ingresa un ID de reserva válido.")
        except SistemaError as e:
            messagebox.showerror("Error en el sistema", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def _actualizar_tabla_reservas(self):
        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)
        for reserva in self.sistema.obtener_reservas():
            # Usar el formateador de configuración
            precio_formateado = config.formatear_precio(reserva.costo_total)
            self.tree_reservas.insert("", tk.END, values=(
                reserva.id,
                reserva.cliente.nombre,
                reserva.servicio.nombre,
                reserva.duracion,
                reserva.estado,
                precio_formateado  # Ahora con formato COP
            ))

    # ---- Pestaña Logs ----
    def _construir_tab_logs(self):
        frame = self.tab_logs

        btn_refrescar = ttk.Button(frame, text="Refrescar Logs", command=self._actualizar_logs)
        btn_refrescar.pack(pady=10)

        self.txt_logs = scrolledtext.ScrolledText(
            frame, 
            wrap=tk.WORD, 
            font=config.FUENTE_LOGS  # Usar fuente desde config
        )
        self.txt_logs.pack(fill='both', expand=True, padx=10, pady=10)

        self._actualizar_logs()

    def _actualizar_logs(self):
        contenido = self.sistema._log.leer_logs()
        self.txt_logs.delete(1.0, tk.END)
        self.txt_logs.insert(tk.END, contenido)