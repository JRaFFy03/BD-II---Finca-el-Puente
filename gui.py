# =================================================================
# PROYECTO FINAL: FINCA EL PUENTE
# ASIGNATURA: BASE DE DATOS II
# ARCHIVO: gui.py
# SISTEMA DE GESTIÓN GANADERA CON QR MÓVIL Y ASISTENTE IA
# =================================================================

import customtkinter as ctk
from tkinter import messagebox, ttk, filedialog
import tkinter as tk
from PIL import Image
import urllib.request
import urllib.parse
import io
import datetime
import webbrowser
import os
import csv
from conexion import obtener_conexion

# =================================================================
# CONFIGURACIÓN GENERAL DE CUSTOMTKINTER
# =================================================================
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

class AppGanado(ctk.CTk):
    def __init__(self):
        super().__init__()
        # =============================================================
        # PALETA DE COLORES INSTITUCIONAL
        # =============================================================
        self.COLOR_VERDE_OSCURO = "#1E4620"
        self.COLOR_VERDE_MEDIO = "#2E7D32"
        self.COLOR_VERDE_CLARO = "#E8F5E9"
        self.COLOR_VERDE_SUAVE = "#F1F8E9"
        self.COLOR_FONDO = "#F4F6F4"
        self.COLOR_BLANCO = "#FFFFFF"
        self.COLOR_TEXTO = "#263238"
        self.COLOR_GRIS = "#ECEFF1"
        self.COLOR_BORDE = "#DDE5DD"
        self.COLOR_ROJO = "#C62828"
        self.COLOR_NARANJA = "#EF6C00"
        self.COLOR_AZUL = "#1565C0"
        
        # =============================================================
        # CONFIGURACIÓN DE LA VENTANA PRINCIPAL
        # =============================================================
        self.title("Finca El Puente — Sistema Inteligente de Gestión Ganadera")
        self.geometry("1240x740")
        self.minsize(1100, 680)
        self.configure(fg_color=self.COLOR_FONDO)
        
        # =============================================================
        # CONFIGURACIÓN DE GITHUB PAGES PARA LA FICHA MÓVIL
        # IMPORTANTE: CAMBIADO A index.html PARA INTEGRAR AL NUEVO PORTAL
        # =============================================================
        self.github_user = "JRaFFy03"
        self.github_repo = "BD-II---Finca-el-Puente"
        self.url_base_movil = f"https://{self.github_user}.github.io/{self.github_repo}/index.html"
        
        # =============================================================
        # FUENTES DEL SISTEMA
        # =============================================================
        self.font_titulo = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.font_subtitulo = ctk.CTkFont(family="Segoe UI", size=17, weight="bold")
        self.font_cuerpo = ctk.CTkFont(family="Segoe UI", size=13)
        self.font_cuerpo_bold = ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        self.font_pequena = ctk.CTkFont(family="Segoe UI", size=11)
        
        # =============================================================
        # VARIABLES TEMPORALES PARA QR
        # =============================================================
        self.qr_temp_data = None
        self.qr_temp_codigo = None
        self.url_ultimo_qr = None
        self.img_qr = None
        
        # =============================================================
        # ESTILO DE TABLAS
        # =============================================================
        self.configurar_estilo_tablas()
        
        # =============================================================
        # IMAGEN DEL MENÚ LATERAL
        # =============================================================
        self.img_sidebar = None
        self.cargar_imagen_sidebar()
        
        # =============================================================
        # ESTRUCTURA GENERAL
        # =============================================================
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.crear_menu_lateral()
        self.crear_area_principal()
        self.crear_boton_chatbot()
        
        # Cargar vista inicial
        self.mostrar_dashboard()

    # =================================================================
    # CONFIGURACIONES VISUALES GENERALES
    # =================================================================
    def configurar_estilo_tablas(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#263238",
            rowheight=31,
            fieldbackground="#FFFFFF",
            font=("Segoe UI", 10),
            bordercolor="#E0E0E0",
            borderwidth=1
        )
        style.configure(
            "Treeview.Heading",
            background="#1E4620",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=6
        )
        style.map(
            "Treeview",
            background=[("selected", "#A5D6A7")],
            foreground=[("selected", "#1B5E20")]
        )

    def cargar_imagen_sidebar(self):
        try:
            url_finca = "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?q=80&w=400&auto=format&fit=crop"
            req = urllib.request.Request(url_finca, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as u:
                raw_data = u.read()
            img_original = Image.open(io.BytesIO(raw_data))
            self.img_sidebar = ctk.CTkImage(
                light_image=img_original,
                dark_image=img_original,
                size=(220, 120)
            )
        except Exception as e:
            print(f"Nota: No se pudo cargar la imagen del menú. Se usará diseño sólido. Detalle: {e}")
            self.img_sidebar = None

    def crear_menu_lateral(self):
        self.menu_lateral = ctk.CTkFrame(
            self,
            width=235,
            corner_radius=0,
            fg_color=self.COLOR_VERDE_OSCURO
        )
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        self.menu_lateral.grid_propagate(False)
        
        # Encabezado del menú
        ctk.CTkLabel(
            self.menu_lateral,
            text=" 🐄  Finca El Puente",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="white"
        ).pack(pady=(22, 4))
        
        ctk.CTkLabel(
            self.menu_lateral,
            text="Sistema Ganadero Inteligente",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#C8E6C9"
        ).pack(pady=(0, 14))
        
        if self.img_sidebar:
            self.lbl_banner = ctk.CTkLabel(
                self.menu_lateral,
                image=self.img_sidebar,
                text="",
                corner_radius=12
            )
            self.lbl_banner.pack(padx=12, pady=(0, 14))
            
        ctk.CTkFrame(
            self.menu_lateral,
            height=1,
            fg_color="#4CAF50"
        ).pack(fill="x", padx=18, pady=(0, 12))
        
        # Botones del menú
        self.botones_menu = {}
        self.btn_dashboard = self.crear_boton_menu(
            "dashboard",
            " 🏡  Dashboard",
            self.mostrar_dashboard
        )
        self.btn_ganado = self.crear_boton_menu(
            "ganado",
            " 🐄  Control de Ganado",
            self.mostrar_ganado
        )
        self.btn_sanidad = self.crear_boton_menu(
            "sanidad",
            " 💉  Control Sanitario",
            self.mostrar_sanidad
        )
        self.btn_alimentacion = self.crear_boton_menu(
            "alimentacion",
            " 🌾  Alimentación",
            self.mostrar_alimentacion
        )
        self.btn_pesajes = self.crear_boton_menu(
            "pesajes",
            " ⚖️  Control de Pesajes",
            self.mostrar_pesajes
        )
        self.btn_reportes = self.crear_boton_menu(
            "reportes",
            " 📊  Reportes y Gráficos",
            self.mostrar_reportes
        )
        
        # Información inferior
        frame_footer = ctk.CTkFrame(self.menu_lateral, fg_color="transparent")
        frame_footer.pack(side="bottom", fill="x", padx=15, pady=15)
        ctk.CTkLabel(
            frame_footer,
            text="UTP Chiriquí • 2026",
            text_color="#A5D6A7",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold")
        ).pack()
        ctk.CTkLabel(
            frame_footer,
            text="Base de Datos II",
            text_color="#C8E6C9",
            font=ctk.CTkFont(family="Segoe UI", size=10)
        ).pack()

    def crear_boton_menu(self, clave, texto, comando):
        boton = ctk.CTkButton(
            self.menu_lateral,
            text=texto,
            fg_color="transparent",
            hover_color="#2E7D32",
            text_color="white",
            anchor="w",
            height=40,
            corner_radius=13,
            font=self.font_cuerpo_bold,
            command=comando
        )
        boton.pack(fill="x", padx=15, pady=4)
        self.botones_menu[clave] = boton
        return boton

    def activar_menu(self, clave_activa):
        for clave, boton in self.botones_menu.items():
            if clave == clave_activa:
                boton.configure(fg_color="#2E7D32")
            else:
                boton.configure(fg_color="transparent")

    def crear_area_principal(self):
        self.frame_derecho = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_derecho.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_derecho.grid_columnconfigure(0, weight=1)
        self.frame_derecho.grid_rowconfigure(1, weight=1)
        self.lbl_titulo_modulo = ctk.CTkLabel(
            self.frame_derecho,
            text="Cargando Sistema...",
            font=self.font_titulo,
            text_color=self.COLOR_VERDE_OSCURO
        )
        self.lbl_titulo_modulo.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 5))
        self.contenedor_principal = ctk.CTkFrame(
            self.frame_derecho,
            fg_color=self.COLOR_BLANCO,
            corner_radius=20,
            border_width=1,
            border_color="#E0E0E0"
        )
        self.contenedor_principal.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.contenedor_principal.grid_columnconfigure(0, weight=1)
        self.contenedor_principal.grid_rowconfigure(0, weight=1)

    def crear_boton_chatbot(self):
        self.btn_chatbot_flotante = ctk.CTkButton(
            self,
            text=" 💬  Asistente IA",
            fg_color=self.COLOR_VERDE_MEDIO,
            hover_color="#1B5E20",
            text_color="white",
            width=145,
            height=42,
            corner_radius=22,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self.abrir_ventana_chatbot
        )
        self.btn_chatbot_flotante.place(relx=0.985, rely=0.965, anchor="se")

    def limpiar_contenedor(self):
        for widget in self.contenedor_principal.winfo_children():
            widget.destroy()

    def crear_titulo_seccion(self, parent, titulo, descripcion):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 18))
        ctk.CTkLabel(
            frame,
            text=titulo,
            font=self.font_subtitulo,
            text_color=self.COLOR_VERDE_OSCURO
        ).pack(anchor="w")
        ctk.CTkLabel(
            frame,
            text=descripcion,
            font=self.font_pequena,
            text_color="#607D8B"
        ).pack(anchor="w", pady=(2, 0))

    def abrir_ventana_chatbot(self):
        ChatbotWindow(self)

    # =================================================================
    # DASHBOARD
    # =================================================================
    def mostrar_dashboard(self):
        self.activar_menu("dashboard")
        self.limpiar_contenedor()
        self.lbl_titulo_modulo.configure(text="Panel de Control General")
        self.vista_actual = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.vista_actual.pack(padx=28, pady=25, fill="both", expand=True)
        
        # Hero principal
        hero = ctk.CTkFrame(
            self.vista_actual,
            fg_color=self.COLOR_VERDE_CLARO,
            corner_radius=22,
            border_width=1,
            border_color="#C8E6C9"
        )
        hero.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(
            hero,
            text=" 🐄  Bienvenido al sistema de administración de Finca El Puente",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=self.COLOR_VERDE_OSCURO
        ).pack(anchor="w", padx=24, pady=(20, 4))
        
        ctk.CTkLabel(
            hero,
            text="Gestiona inventario ganadero, controles sanitarios, alimentación, pesajes, reportes y fichas QR móviles desde un solo lugar.",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#455A64",
            wraplength=850,
            justify="left"
        ).pack(anchor="w", padx=24, pady=(0, 20))
        
        # Tarjetas principales
        frame_cards = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_cards.pack(fill="x", pady=5)
        self.card_total = self.crear_card_dashboard(
            frame_cards,
            " 🐄  Ganado registrado",
            "Cargando...",
            "#E8F5E9",
            "#1B5E20"
        )
        self.card_total.pack(side="left", padx=7, expand=True, fill="both")
        self.card_sanidad_dash = self.crear_card_dashboard(
            frame_cards,
            " 💉  Controles sanitarios",
            "Cargando...",
            "#FFF3E0",
            "#E65100"
        )
        self.card_sanidad_dash.pack(side="left", padx=7, expand=True, fill="both")
        self.card_alim_dash = self.crear_card_dashboard(
            frame_cards,
            " 🌾  Alimento total",
            "Cargando...",
            "#F1F8E9",
            "#33691E"
        )
        self.card_alim_dash.pack(side="left", padx=7, expand=True, fill="both")
        self.card_peso_dash = self.crear_card_dashboard(
            frame_cards,
            " ⚖️  Peso promedio",
            "Cargando...",
            "#E3F2FD",
            "#0D47A1"
        )
        self.card_peso_dash.pack(side="left", padx=7, expand=True, fill="both")
        
        # Panel inferior de accesos
        frame_accesos = ctk.CTkFrame(
            self.vista_actual,
            fg_color="#FAFAFA",
            corner_radius=18,
            border_width=1,
            border_color="#EEEEEE"
        )
        frame_accesos.pack(fill="both", expand=True, pady=(24, 0))
        ctk.CTkLabel(
            frame_accesos,
            text=" ⚡  Accesos rápidos",
            font=self.font_subtitulo,
            text_color=self.COLOR_VERDE_OSCURO
        ).pack(anchor="w", padx=22, pady=(18, 8))
        
        grid_accesos = ctk.CTkFrame(frame_accesos, fg_color="transparent")
        grid_accesos.pack(fill="x", padx=20, pady=(0, 20))
        
        self.crear_acceso_rapido(
            grid_accesos,
            "Registrar ganado",
            "Añade un nuevo animal al inventario.",
            " 🐄 ",
            self.mostrar_ganado
        ).grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        self.crear_acceso_rapido(
            grid_accesos,
            "Control sanitario",
            "Registra vacunas y tratamientos.",
            " 💉 ",
            self.mostrar_sanidad
        ).grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        self.crear_acceso_rapido(
            grid_accesos,
            "Ficha QR",
            "Selecciona un animal y genera su QR.",
            " 🧾 ",
            self.mostrar_ganado
        ).grid(row=0, column=2, padx=8, pady=8, sticky="nsew")
        self.crear_acceso_rapido(
            grid_accesos,
            "Reportes",
            "Consulta métricas y exportaciones.",
            " 📊 ",
            self.mostrar_reportes
        ).grid(row=0, column=3, padx=8, pady=8, sticky="nsew")
        
        for i in range(4):
            grid_accesos.grid_columnconfigure(i, weight=1)
        self.cargar_contadores_dashboard()

    def crear_card_dashboard(self, parent, titulo, valor, color_fondo, color_texto):
        card = ctk.CTkFrame(
            parent,
            fg_color=color_fondo,
            corner_radius=18,
            border_width=1,
            border_color="#DDE5DD"
        )
        ctk.CTkLabel(
            card,
            text=titulo,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=color_texto
        ).pack(anchor="w", padx=16, pady=(16, 5))
        lbl_valor = ctk.CTkLabel(
            card,
            text=valor,
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=color_texto
        )
        lbl_valor.pack(anchor="w", padx=16, pady=(0, 16))
        card.valor_label = lbl_valor
        return card

    def crear_acceso_rapido(self, parent, titulo, descripcion, icono, comando):
        card = ctk.CTkButton(
            parent,
            text=f"{icono}\n{titulo}\n{descripcion}",
            fg_color="white",
            hover_color="#E8F5E9",
            text_color=self.COLOR_TEXTO,
            corner_radius=18,
            height=110,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=comando
        )
        return card

    def cargar_contadores_dashboard(self):
        conn = obtener_conexion()
        if not conn:
            self.card_total.valor_label.configure(text="Sin conexión")
            self.card_sanidad_dash.valor_label.configure(text="Sin conexión")
            self.card_alim_dash.valor_label.configure(text="Sin conexión")
            self.card_peso_dash.valor_label.configure(text="Sin conexión")
            return
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM ganado")
            total_ganado = cursor.fetchone()[0] or 0
            cursor.execute("SELECT COUNT(*) FROM sanidad")
            total_sanidad = cursor.fetchone()[0] or 0
            cursor.execute("SELECT SUM(cantidad_kg) FROM alimentacion")
            total_alimento = float(cursor.fetchone()[0] or 0.0)
            cursor.execute("SELECT AVG(peso_kg) FROM pesajes")
            peso_promedio = float(cursor.fetchone()[0] or 0.0)
            
            self.card_total.valor_label.configure(text=f"{total_ganado} animales")
            self.card_sanidad_dash.valor_label.configure(text=f"{total_sanidad} registros")
            self.card_alim_dash.valor_label.configure(text=f"{total_alimento:.2f} kg")
            self.card_peso_dash.valor_label.configure(text=f"{peso_promedio:.2f} kg")
        except Exception as e:
            print(f"Error en dashboard: {e}")
            self.card_total.valor_label.configure(text="Error")
            self.card_sanidad_dash.valor_label.configure(text="Error")
            self.card_alim_dash.valor_label.configure(text="Error")
            self.card_peso_dash.valor_label.configure(text="Error")
        finally:
            cursor.close()
            conn.close()

    # =================================================================
    # CONTROL DE GANADO
    # =================================================================
    def mostrar_ganado(self):
        self.activar_menu("ganado")
        self.limpiar_contenedor()
        self.lbl_titulo_modulo.configure(text="Control e Inventario de Ganado")
        self.vista_actual = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.vista_actual.grid(row=0, column=0, sticky="nsew", padx=20, pady=15)
        self.vista_actual.grid_columnconfigure(0, weight=0)
        self.vista_actual.grid_columnconfigure(1, weight=0)
        self.vista_actual.grid_columnconfigure(2, weight=1)
        self.vista_actual.grid_rowconfigure(0, weight=1)
        
        # -------------------------------------------------------------
        # PANEL IZQUIERDO: FORMULARIO
        # -------------------------------------------------------------
        frame_inputs = ctk.CTkFrame(
            self.vista_actual,
            fg_color="#FAFAFA",
            corner_radius=18,
            border_width=1,
            border_color="#E0E0E0"
        )
        frame_inputs.grid(row=0, column=0, padx=(0, 12), pady=5, sticky="nw")
        ctk.CTkLabel(
            frame_inputs,
            text=" 🧾  Datos del animal",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=self.COLOR_VERDE_OSCURO
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(14, 10))
        
        self.crear_label(frame_inputs, "Código del Animal:", 1)
        self.ent_codigo = ctk.CTkEntry(frame_inputs, width=185, placeholder_text="Ej: A001")
        self.ent_codigo.grid(row=1, column=1, pady=3, padx=(5, 14))
        
        self.crear_label(frame_inputs, "Nombre / Alias:", 2)
        self.ent_nombre = ctk.CTkEntry(frame_inputs, width=185, placeholder_text="Ej: Hércules")
        self.ent_nombre.grid(row=2, column=1, pady=3, padx=(5, 14))
        
        self.crear_label(frame_inputs, "Raza Ganadera:", 3)
        self.cmb_raza = ctk.CTkComboBox(
            frame_inputs,
            values=["Brahman Gris", "Brahman Rojo", "Nelore", "Gyr", "Pardo Suizo"],
            width=185
        )
        self.cmb_raza.grid(row=3, column=1, pady=3, padx=(5, 14))
        
        self.crear_label(frame_inputs, "Sexo:", 4)
        self.cmb_sexo = ctk.CTkComboBox(frame_inputs, values=["Macho", "Hembra"], width=185)
        self.cmb_sexo.grid(row=4, column=1, pady=3, padx=(5, 14))
        
        self.crear_label(frame_inputs, "F. Nacimiento:", 5)
        self.ent_fecha_nac = ctk.CTkEntry(frame_inputs, width=185)
        self.ent_fecha_nac.grid(row=5, column=1, pady=3, padx=(5, 14))
        self.ent_fecha_nac.insert(0, str(datetime.date.today()))
        
        self.crear_label(frame_inputs, "Peso Inicial (Kg):", 6)
        self.ent_peso_ini = ctk.CTkEntry(frame_inputs, width=185, placeholder_text="Ej: 320")
        self.ent_peso_ini.grid(row=6, column=1, pady=3, padx=(5, 14))
        
        self.crear_label(frame_inputs, "Estado:", 7)
        self.cmb_estado = ctk.CTkComboBox(
            frame_inputs,
            values=["Activo", "Vendido", "Enfermo", "Inactivo"],
            width=185
        )
        self.cmb_estado.grid(row=7, column=1, pady=3, padx=(5, 14))
        self.cmb_estado.set("Activo")
        
        self.crear_label(frame_inputs, "Código del Padre:", 8)
        self.ent_padre = ctk.CTkEntry(frame_inputs, width=185, placeholder_text="Opcional")
        self.ent_padre.grid(row=8, column=1, pady=3, padx=(5, 14))
        
        self.crear_label(frame_inputs, "Código de la Madre:", 9)
        self.ent_madre = ctk.CTkEntry(frame_inputs, width=185, placeholder_text="Opcional")
        self.ent_madre.grid(row=9, column=1, pady=3, padx=(5, 14))
        
        self.crear_label(frame_inputs, "Observaciones:", 10)
        self.ent_observaciones = ctk.CTkEntry(frame_inputs, width=185, placeholder_text="Notas del ejemplar")
        self.ent_observaciones.grid(row=10, column=1, pady=3, padx=(5, 14))
        
        frame_btn = ctk.CTkFrame(frame_inputs, fg_color="transparent")
        frame_btn.grid(row=11, column=0, columnspan=2, pady=14)
        
        ctk.CTkButton(
            frame_btn,
            text=" 💾  Registrar",
            width=105,
            fg_color=self.COLOR_VERDE_OSCURO,
            hover_color="#143016",
            command=self.guardar_ganado
        ).grid(row=0, column=0, padx=4)
        
        ctk.CTkButton(
            frame_btn,
            text=" 🗑️  Eliminar",
            width=105,
            fg_color=self.COLOR_ROJO,
            hover_color="#B71C1C",
            command=self.eliminar_ganado
        ).grid(row=0, column=1, padx=4)
        
        # -------------------------------------------------------------
        # PANEL CENTRAL: QR
        # -------------------------------------------------------------
        self.frame_qr = ctk.CTkFrame(
            self.vista_actual,
            fg_color="#F9F9F9",
            width=190,
            corner_radius=18,
            border_width=1,
            border_color="#E0E0E0"
        )
        self.frame_qr.grid(row=0, column=1, padx=8, pady=5, sticky="ns")
        self.frame_qr.grid_propagate(False)
        
        ctk.CTkLabel(
            self.frame_qr,
            text=" 🧾  Ficha móvil QR",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.COLOR_VERDE_OSCURO
        ).pack(pady=(16, 4))
        
        ctk.CTkLabel(
            self.frame_qr,
            text="Escanea desde el celular para ver la ficha del animal.",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color="#607D8B",
            wraplength=150,
            justify="center"
        ).pack(pady=(0, 8))
        
        self.lbl_qr_visual = ctk.CTkLabel(
            self.frame_qr,
            text=" 🐄 \nSeleccione un animal\npara generar QR",
            text_color="#4B5563",
            width=150,
            height=150,
            fg_color="#FFFFFF",
            corner_radius=14,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.lbl_qr_visual.pack(pady=8, padx=15)
        
        self.btn_guardar_qr = ctk.CTkButton(
            self.frame_qr,
            text=" 📥  Descargar QR",
            width=145,
            fg_color=self.COLOR_VERDE_MEDIO,
            hover_color="#1B5E20",
            state="disabled",
            command=self.descargar_qr_seleccionado
        )
        self.btn_guardar_qr.pack(pady=(8, 5))
        
        self.btn_abrir_ficha = ctk.CTkButton(
            self.frame_qr,
            text=" 🌐  Ver ficha",
            width=145,
            fg_color=self.COLOR_AZUL,
            hover_color="#0D47A1",
            state="disabled",
            command=self.abrir_ficha_movil_seleccionada
        )
        self.btn_abrir_ficha.pack(pady=5)
        
        # -------------------------------------------------------------
        # PANEL DERECHO: TABLA
        # -------------------------------------------------------------
        self.tabla_ganado = None
        self.crear_tabla_ganado_vista()
        self.cargar_datos_ganado()

    def crear_label(self, parent, texto, fila):
        ctk.CTkLabel(
            parent,
            text=texto,
            font=self.font_cuerpo,
            text_color=self.COLOR_TEXTO
        ).grid(row=fila, column=0, sticky="w", padx=(14, 5), pady=3)

    def crear_tabla_ganado_vista(self):
        frame_tabla = ctk.CTkFrame(
            self.vista_actual,
            fg_color="#FAFAFA",
            corner_radius=18,
            border_width=1,
            border_color="#E0E0E0"
        )
        frame_tabla.grid(row=0, column=2, padx=(12, 0), pady=5, sticky="nsew")
        frame_tabla.grid_columnconfigure(0, weight=1)
        frame_tabla.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            frame_tabla,
            text=" 📋  Inventario registrado",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=self.COLOR_VERDE_OSCURO
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 8))
        
        columnas = ("codigo", "nombre", "raza", "sexo", "peso", "estado")
        self.tabla_ganado = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=18)
        self.tabla_ganado.heading("codigo", text="Código")
        self.tabla_ganado.heading("nombre", text="Nombre")
        self.tabla_ganado.heading("raza", text="Raza")
        self.tabla_ganado.heading("sexo", text="Sexo")
        self.tabla_ganado.heading("peso", text="Peso")
        self.tabla_ganado.heading("estado", text="Estado")
        
        self.tabla_ganado.column("codigo", width=85, anchor="center")
        self.tabla_ganado.column("nombre", width=120)
        self.tabla_ganado.column("raza", width=115)
        self.tabla_ganado.column("sexo", width=70, anchor="center")
        self.tabla_ganado.column("peso", width=85, anchor="e")
        self.tabla_ganado.column("estado", width=90, anchor="center")
        
        self.tabla_ganado.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        self.tabla_ganado.bind("<<TreeviewSelect>>", self.on_seleccionar_animal)

    def on_seleccionar_animal(self, event):
        sel = self.tabla_ganado.selection()
        if not sel:
            return
        valores = self.tabla_ganado.item(sel[0])["values"]
        cod_selec = valores[0]
        conn = obtener_conexion()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar con SQL Server.")
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT codigo, nombre, raza, sexo, fecha_nacimiento, peso_inicial, estado, padre, madre, observaciones
                FROM ganado
                WHERE codigo = ?
                """,
                (cod_selec,)
            )
            fila = cursor.fetchone()
            if fila:
                self.ent_codigo.delete(0, "end")
                self.ent_codigo.insert(0, fila[0])
                self.ent_nombre.delete(0, "end")
                self.ent_nombre.insert(0, fila[1])
                self.cmb_raza.set(fila[2])
                self.cmb_sexo.set(fila[3])
                self.ent_fecha_nac.delete(0, "end")
                self.ent_fecha_nac.insert(0, str(fila[4]))
                self.ent_peso_ini.delete(0, "end")
                self.ent_peso_ini.insert(0, f"{float(fila[5] or 0):.2f}")
                self.cmb_estado.set(fila[6])
                self.ent_padre.delete(0, "end")
                self.ent_padre.insert(0, fila[7] if fila[7] else "")
                self.ent_madre.delete(0, "end")
                self.ent_madre.insert(0, fila[8] if fila[8] else "")
                self.ent_observaciones.delete(0, "end")
                self.ent_observaciones.insert(0, fila[9] if fila[9] else "")
                
                self.generar_qr_online(
                    codigo=fila[0],
                    nombre=fila[1],
                    raza=fila[2],
                    sexo=fila[3],
                    peso=f"{float(fila[5] or 0):.2f}",
                    estado=fila[6],
                    observaciones=fila[9] if fila[9] else ""
                )
        except Exception as e:
            print(f"Error al cargar selección: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el animal seleccionado.\nDetalle: {e}")
        finally:
            cursor.close()
            conn.close()

    def generar_qr_online(self, codigo, nombre, raza, sexo, peso, estado, observaciones=""):
        try:
            params = urllib.parse.urlencode({
                "id": codigo,
                "nombre": nombre,
                "raza": raza,
                "sexo": sexo,
                "peso": peso,
                "estado": estado,
                "obs": observaciones
            })
            url_destino = f"{self.url_base_movil}?{params}"
            self.url_ultimo_qr = url_destino
            url_api = (
                "https://api.qrserver.com/v1/create-qr-code/"
                f"?size=180x180&data={urllib.parse.quote(url_destino)}"
            )
            req = urllib.request.Request(url_api, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                binario_imagen = response.read()
            img_original = Image.open(io.BytesIO(binario_imagen))
            self.img_qr = ctk.CTkImage(
                light_image=img_original,
                dark_image=img_original,
                size=(140, 140)
            )
            self.lbl_qr_visual.configure(image=self.img_qr, text="")
            self.qr_temp_data = binario_imagen
            self.qr_temp_codigo = codigo
            self.btn_guardar_qr.configure(state="normal")
            self.btn_abrir_ficha.configure(state="normal")
        except Exception as e:
            self.lbl_qr_visual.configure(
                image=None,
                text="⚠️ Error QR\nVerifique Internet"
            )
            self.btn_guardar_qr.configure(state="disabled")
            self.btn_abrir_ficha.configure(state="disabled")
            print(f"Error al generar QR: {e}")

    def abrir_ficha_movil_seleccionada(self):
        if self.url_ultimo_qr:
            webbrowser.open(self.url_ultimo_qr)
        else:
            messagebox.showwarning("Atención", "Primero seleccione un animal para generar la ficha.")

    def descargar_qr_seleccionado(self):
        if not self.qr_temp_data or not self.qr_temp_codigo:
            messagebox.showwarning("Atención", "Primero seleccione un animal.")
            return
        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png")],
            title="Guardar Código QR",
            initialfile=f"QR_FincaElPuente_{self.qr_temp_codigo}.png"
        )
        if not ruta_guardado:
            return
        try:
            with open(ruta_guardado, "wb") as f:
                f.write(self.qr_temp_data)
            messagebox.showinfo(
                "Éxito",
                "🎉 QR descargado con éxito.\nPuede imprimirlo y colocarlo en la ficha o etiqueta del animal."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al guardar el QR: {e}")

    def cargar_datos_ganado(self):
        for i in self.tabla_ganado.get_children():
            self.tabla_ganado.delete(i)
        conn = obtener_conexion()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT codigo, nombre, raza, sexo, peso_inicial, estado FROM ganado")
            for fila in cursor.fetchall():
                self.tabla_ganado.insert(
                    "",
                    "end",
                    values=(
                        fila[0],
                        fila[1],
                        fila[2],
                        fila[3],
                        f"{float(fila[4] or 0):.2f}",
                        fila[5]
                    )
                )
        except Exception as e:
            messagebox.showerror("Error SQL", f"No se pudo cargar el inventario.\nDetalle: {e}")
        finally:
            cursor.close()
            conn.close()

    def guardar_ganado(self):
        cod = self.ent_codigo.get().strip()
        nom = self.ent_nombre.get().strip()
        raz = self.cmb_raza.get()
        sex = self.cmb_sexo.get()
        fec = self.ent_fecha_nac.get().strip()
        pes = self.ent_peso_ini.get().strip()
        est = self.cmb_estado.get()
        pad = self.ent_padre.get().strip() or None
        mad = self.ent_madre.get().strip() or None
        obs = self.ent_observaciones.get().strip() or None
        if not cod or not nom or not pes:
            messagebox.showwarning(
                "Campos obligatorios",
                "Por favor complete al menos el código, nombre y peso del animal."
            )
            return
        try:
            peso_float = float(pes)
        except ValueError:
            messagebox.showwarning("Dato inválido", "El peso debe ser un número válido.")
            return
        conn = obtener_conexion()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar con SQL Server.")
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO ganado
                (codigo, nombre, raza, sexo, fecha_nacimiento, peso_inicial, estado, padre, madre, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (cod, nom, raz, sex, fec, peso_float, est, pad, mad, obs)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "✅ Ejemplar registrado exitosamente.")
            self.cargar_datos_ganado()
        except Exception as e:
            messagebox.showerror("Error SQL", f"No se pudo guardar el animal.\nDetalle: {e}")
        finally:
            cursor.close()
            conn.close()

    def eliminar_ganado(self):
        sel = self.tabla_ganado.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un animal de la tabla.")
            return
        cod = self.tabla_ganado.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirmar eliminación", f"¿Seguro que desea eliminar al animal {cod}?"):
            return
        conn = obtener_conexion()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar con SQL Server.")
            return
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM ganado WHERE codigo = ?", (cod,))
            conn.commit()
            messagebox.showinfo("Éxito", "🗑️ Animal eliminado correctamente.")
            self.cargar_datos_ganado()
            self.lbl_qr_visual.configure(
                image=None,
                text="🐄\nSeleccione un animal\npara generar QR"
            )
            self.btn_guardar_qr.configure(state="disabled")
            self.btn_abrir_ficha.configure(state="disabled")
            self.qr_temp_data = None
            self.qr_temp_codigo = None
            self.url_ultimo_qr = None
        except Exception as e:
            messagebox.showerror("Error SQL", f"No se pudo eliminar el animal.\nDetalle: {e}")
        finally:
            cursor.close()
            conn.close()

    # =================================================================
    # CONTROL SANITARIO
    # =================================================================
    def mostrar_sanidad(self):
        self.activar_menu("sanidad")
        self.limpiar_contenedor()
        self.lbl_titulo_modulo.configure(text="Control Sanitario y Clínico")
        self.vista_actual = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.vista_actual.grid(row=0, column=0, sticky="nsew", padx=24, pady=22)
        self.vista_actual.grid_columnconfigure(1, weight=1)
        self.vista_actual.grid_rowconfigure(0, weight=1)
        
        frame_inputs = ctk.CTkFrame(
            self.vista_actual,
            fg_color="#FFF8E1",
            corner_radius=18,
            border_width=1,
            border_color="#FFE0B2"
        )
        frame_inputs.grid(row=0, column=0, padx=(0, 18), pady=5, sticky="nw")
        ctk.CTkLabel(
            frame_inputs,
            text="💉 Registro sanitario",
            font=self.font_subtitulo,
            text_color="#E65100"
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16, 10))
        
        self.crear_label(frame_inputs, "Código del Animal:", 1)
        self.ent_sani_cod = ctk.CTkEntry(frame_inputs, width=190, placeholder_text="Ej: A001")
        self.ent_sani_cod.grid(row=1, column=1, pady=5, padx=(5, 16))
        
        self.crear_label(frame_inputs, "Tipo Tratamiento:", 2)
        self.cmb_sani_tipo = ctk.CTkComboBox(
            frame_inputs,
            values=["Vacuna", "Desparasitante", "Vitamina", "Tratamiento Médico"],
            width=190
        )
        self.cmb_sani_tipo.grid(row=2, column=1, pady=5, padx=(5, 16))
        
        self.crear_label(frame_inputs, "Medicamento:", 3)
        self.ent_sani_med = ctk.CTkEntry(frame_inputs, width=190, placeholder_text="Ej: Ivermectina")
        self.ent_sani_med.grid(row=3, column=1, pady=5, padx=(5, 16))
        
        self.crear_label(frame_inputs, "Dosis Aplicada:", 4)
        self.ent_sani_dosis = ctk.CTkEntry(frame_inputs, width=190, placeholder_text="Ej: 5 ml")
        self.ent_sani_dosis.grid(row=4, column=1, pady=5, padx=(5, 16))
        
        ctk.CTkButton(
            frame_inputs,
            text="💉 Registrar Tratamiento",
            fg_color="#E65100",
            hover_color="#BF360C",
            height=38,
            command=self.guardar_sanidad
        ).grid(row=5, column=0, columnspan=2, padx=16, pady=(16, 18), sticky="ew")
        
        self.tabla_sanidad = None
        self.crear_tabla_sanidad_vista()
        self.cargar_datos_sanidad()

    def crear_tabla_sanidad_vista(self):
        frame_tabla = ctk.CTkFrame(
            self.vista_actual,
            fg_color="#FAFAFA",
            corner_radius=18,
            border_width=1,
            border_color="#E0E0E0"
        )
        frame_tabla.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        frame_tabla.grid_columnconfigure(0, weight=1)
        frame_tabla.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            frame_tabla,
            text="📋 Historial sanitario",
            font=self.font_subtitulo,
            text_color=self.COLOR_VERDE_OSCURO
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 8))
        
        columnas = ("id", "animal", "tipo", "med", "fecha")
        self.tabla_sanidad = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        self.tabla_sanidad.heading("id", text="ID")
        self.tabla_sanidad.heading("animal", text="Animal")
        self.tabla_sanidad.heading("tipo", text="Tipo")
        self.tabla_sanidad.heading("med", text="Medicamento")
        self.tabla_sanidad.heading("fecha", text="Fecha")
        
        self.tabla_sanidad.column("id", width=50, anchor="center")
        self.tabla_sanidad.column("animal", width=90, anchor="center")
        self.tabla_sanidad.column("tipo", width=130)
        self.tabla_sanidad.column("med", width=160)
        self.tabla_sanidad.column("fecha", width=110, anchor="center")
        self.tabla_sanidad.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))

    def cargar_datos_sanidad(self):
        for i in self.tabla_sanidad.get_children():
            self.tabla_sanidad.delete(i)
        conn = obtener_conexion()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, codigo_animal, tipo_tratamiento, medicamento, fecha_aplicacion FROM sanidad")
            for fila in cursor.fetchall():
                self.tabla_sanidad.insert("", "end", values=fila)
        except Exception as e:
            messagebox.showerror("Error SQL", f"No se pudo cargar sanidad.\nDetalle: {e}")
        finally:
            cursor.close()
            conn.close()

    def guardar_sanidad(self):
        ani = self.ent_sani_cod.get().strip()
        tip = self.cmb_sani_tipo.get()
        med = self.ent_sani_med.get().strip()
        dos = self.ent_sani_dosis.get().strip()
        fec = str(datetime.date.today())
        if not ani or not med or not dos:
            messagebox.showwarning("Campos vacíos", "Complete el código, medicamento y dosis.")
            return
        conn = obtener_conexion()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar con SQL Server.")
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO sanidad
                (codigo_animal, tipo_tratamiento, medicamento, fecha_aplicacion, dosis)
                VALUES (?, ?, ?, ?, ?)
                """,
                (ani, tip, med, fec, dos)
            )
            conn.commit()
            messagebox.showinfo("Listo", "✅ Historial médico guardado con éxito.")
            self.cargar_datos_sanidad()
        except Exception as e:
            messagebox.showerror(
                "Error Relacional",
                f"Verifique si el código del animal existe.\nDetalle: {e}"
            )
        finally:
            cursor.close()
            conn.close()

    # =================================================================
    # ALIMENTACIÓN
    # =================================================================
    def mostrar_alimentacion(self):
        self.activar_menu("alimentacion")
        self.limpiar_contenedor()
        self.lbl_titulo_modulo.configure(text="Control de Alimentación y Raciones")
        self.vista_actual = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.vista_actual.grid(row=0, column=0, sticky="nsew", padx=24, pady=22)
        self.vista_actual.grid_columnconfigure(1, weight=1)
        self.vista_actual.grid_rowconfigure(0, weight=1)
        
        frame_inputs = ctk.CTkFrame(
            self.vista_actual,
            fg_color="#F1F8E9",
            corner_radius=18,
            border_width=1,
            border_color="#DCEDC8"
        )
        frame_inputs.grid(row=0, column=0, padx=(0, 18), pady=5, sticky="nw")
        ctk.CTkLabel(
            frame_inputs,
            text="🌾 Registro alimenticio",
            font=self.font_subtitulo,
            text_color="#33691E"
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16, 10))
        
        self.crear_label(frame_inputs, "Código del Animal:", 1)
        self.ent_alim_cod = ctk.CTkEntry(frame_inputs, width=190, placeholder_text="Ej: A001")
        self.ent_alim_cod.grid(row=1, column=1, pady=5, padx=(5, 16))
        
        self.crear_label(frame_inputs, "Tipo de Alimento:", 2)
        self.cmb_alim_tipo = ctk.CTkComboBox(
            frame_inputs,
            values=["Concentrado", "Silo de Maíz", "Pasto de Corte", "Melaza", "Sales Minerales"],
            width=190
        )
        self.cmb_alim_tipo.grid(row=2, column=1, pady=5, padx=(5, 16))
        
        self.crear_label(frame_inputs, "Cantidad (Kg):", 3)
        self.ent_alim_cant = ctk.CTkEntry(frame_inputs, width=190, placeholder_text="Ej: 12.5")
        self.ent_alim_cant.grid(row=3, column=1, pady=5, padx=(5, 16))
        
        ctk.CTkButton(
            frame_inputs,
            text="🌾 Registrar Dieta",
            fg_color="#33691E",
            hover_color="#1B5E20",
            height=38,
            command=self.guardar_alimentacion
        ).grid(row=4, column=0, columnspan=2, padx=16, pady=(16, 18), sticky="ew")
        
        self.tabla_alim = None
        self.crear_tabla_alim_vista()
        self.cargar_datos_alim()

    def crear_tabla_alim_vista(self):
        frame_tabla = ctk.CTkFrame(
            self.vista_actual,
            fg_color="#FAFAFA",
            corner_radius=18,
            border_width=1,
            border_color="#E0E0E0"
        )
        frame_tabla.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        frame_tabla.grid_columnconfigure(0, weight=1)
        frame_tabla.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            frame_tabla,
            text="📋 Historial de alimentación",
            font=self.font_subtitulo,
            text_color=self.COLOR_VERDE_OSCURO
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 8))
        
        columnas = ("id", "animal", "tipo", "cant", "fecha")
        self.tabla_alim = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        self.tabla_alim.heading("id", text="ID")
        self.tabla_alim.heading("animal", text="Animal")
        self.tabla_alim.heading("tipo", text="Tipo Alimento")
        self.tabla_alim.heading("cant", text="Cantidad")
        self.tabla_alim.heading("fecha", text="Fecha")
        
        self.tabla_alim.column("id", width=50, anchor="center")
        self.tabla_alim.column("animal", width=90, anchor="center")
        self.tabla_alim.column("tipo", width=150)
        self.tabla_alim.column("cant", width=110, anchor="e")
        self.tabla_alim.column("fecha", width=110, anchor="center")
        self.tabla_alim.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))

    def cargar_datos_alim(self):
        for i in self.tabla_alim.get_children():
            self.tabla_alim.delete(i)
        conn = obtener_conexion()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, codigo_animal, tipo_alimento, cantidad_kg, fecha_registro FROM alimentacion")
            for fila in cursor.fetchall():
                self.tabla_alim.insert(
                    "",
                    "end",
                    values=(fila[0], fila[1], fila[2], f"{float(fila[3] or 0):.2f} Kg", fila[4])
                )
        except Exception as e:
            messagebox.showerror("Error SQL", f"No se pudo cargar alimentación.\nDetalle: {e}")
        finally:
            cursor.close()
            conn.close()

    def guardar_alimentacion(self):
        ani = self.ent_alim_cod.get().strip()
        tip = self.cmb_alim_tipo.get()
        can = self.ent_alim_cant.get().strip()
        fec = str(datetime.date.today())
        if not ani or not can:
            messagebox.showwarning("Atención", "Ingrese el código del animal y la cantidad en kilos.")
            return
        try:
            cantidad_float = float(can)
        except ValueError:
            messagebox.showwarning("Dato inválido", "La cantidad debe ser un número válido.")
            return
        conn = obtener_conexion()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar con SQL Server.")
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO alimentacion
                (codigo_animal, tipo_alimento, cantidad_kg, fecha_registro)
                VALUES (?, ?, ?, ?)
                """,
                (ani, tip, cantidad_float, fec)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "✅ Asignación de alimento guardada.")
            self.cargar_datos_alim()
        except Exception as e:
            messagebox.showerror(
                "Error Relacional",
                f"Código de animal no registrado en inventario.\nDetalle: {e}"
            )
        finally:
            cursor.close()
            conn.close()

    # =================================================================
    # CONTROL DE PESAJES
    # =================================================================
    def mostrar_pesajes(self):
        self.activar_menu("pesajes")
        self.limpiar_contenedor()
        self.lbl_titulo_modulo.configure(text="Historial y Evolución de Pesos")
        self.vista_actual = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.vista_actual.grid(row=0, column=0, sticky="nsew", padx=24, pady=22)
        self.vista_actual.grid_columnconfigure(1, weight=1)
        self.vista_actual.grid_rowconfigure(0, weight=1)
        
        frame_inputs = ctk.CTkFrame(
            self.vista_actual,
            fg_color="#E3F2FD",
            corner_radius=18,
            border_width=1,
            border_color="#BBDEFB"
        )
        frame_inputs.grid(row=0, column=0, padx=(0, 18), pady=5, sticky="nw")
        ctk.CTkLabel(
            frame_inputs,
            text="⚖️ Registro de pesaje",
            font=self.font_subtitulo,
            text_color="#0D47A1"
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16, 10))
        
        self.crear_label(frame_inputs, "Código del Animal:", 1)
        self.ent_peso_cod = ctk.CTkEntry(frame_inputs, width=190, placeholder_text="Ej: A001")
        self.ent_peso_cod.grid(row=1, column=1, pady=5, padx=(5, 16))
        
        self.crear_label(frame_inputs, "Peso Actual (Kg):", 2)
        self.ent_peso_kg = ctk.CTkEntry(frame_inputs, width=190, placeholder_text="Ej: 350")
        self.ent_peso_kg.grid(row=2, column=1, pady=5, padx=(5, 16))
        
        ctk.CTkButton(
            frame_inputs,
            text="⚖️ Registrar Pesaje",
            fg_color="#1565C0",
            hover_color="#0D47A1",
            height=38,
            command=self.guardar_pesaje
        ).grid(row=3, column=0, columnspan=2, padx=16, pady=(16, 18), sticky="ew")
        
        self.tabla_pesajes = None
        self.crear_tabla_pesajes_vista()
        self.cargar_datos_pesajes()

    def crear_tabla_pesajes_vista(self):
        frame_tabla = ctk.CTkFrame(
            self.vista_actual,
            fg_color="#FAFAFA",
            corner_radius=18,
            border_width=1,
            border_color="#E0E0E0"
        )
        frame_tabla.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        frame_tabla.grid_columnconfigure(0, weight=1)
        frame_tabla.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            frame_tabla,
            text="📋 Historial de pesajes",
            font=self.font_subtitulo,
            text_color=self.COLOR_VERDE_OSCURO
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 8))
        
        columnas = ("id", "animal", "peso", "fecha")
        self.tabla_pesajes = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        self.tabla_pesajes.heading("id", text="ID")
        self.tabla_pesajes.heading("animal", text="Animal")
        self.tabla_pesajes.heading("peso", text="Peso Evaluado")
        self.tabla_pesajes.heading("fecha", text="Fecha")
        
        self.tabla_pesajes.column("id", width=50, anchor="center")
        self.tabla_pesajes.column("animal", width=100, anchor="center")
        self.tabla_pesajes.column("peso", width=130, anchor="e")
        self.tabla_pesajes.column("fecha", width=120, anchor="center")
        self.tabla_pesajes.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))

    def cargar_datos_pesajes(self):
        for i in self.tabla_pesajes.get_children():
            self.tabla_pesajes.delete(i)
        conn = obtener_conexion()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, codigo_animal, peso_kg, fecha_pesaje FROM pesajes")
            for fila in cursor.fetchall():
                self.tabla_pesajes.insert(
                    "",
                    "end",
                    values=(fila[0], fila[1], f"{float(fila[2] or 0):.2f} Kg", fila[3])
                )
        except Exception as e:
            messagebox.showerror("Error SQL", f"No se pudo cargar pesajes.\nDetalle: {e}")
        finally:
            cursor.close()
            conn.close()

    def guardar_pesaje(self):
        ani = self.ent_peso_cod.get().strip()
        pes = self.ent_peso_kg.get().strip()
        fec = str(datetime.date.today())
        if not ani or not pes:
            messagebox.showwarning("Atención", "Complete el código del animal y el peso.")
            return
        try:
            peso_float = float(pes)
        except ValueError:
            messagebox.showwarning("Dato inválido", "El peso debe ser un número válido.")
            return
        conn = obtener_conexion()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar con SQL Server.")
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO pesajes
                (codigo_animal, peso_kg, fecha_pesaje)
                VALUES (?, ?, ?)
                """,
                (ani, peso_float, fec)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "✅ Pesaje cronológico añadido.")
            self.cargar_datos_pesajes()
        except Exception as e:
            messagebox.showerror(
                "Error Relacional",
                f"No se encontró el animal en la finca.\nDetalle: {e}"
            )
        finally:
            cursor.close()
            conn.close()

    # =================================================================
    # REPORTES
    # =================================================================
    def mostrar_reportes(self):
        self.activar_menu("reportes")
        self.limpiar_contenedor()
        self.lbl_titulo_modulo.configure(text="Reportes, Gráficos y Métricas")
        self.vista_actual = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.vista_actual.pack(fill="both", expand=True, padx=24, pady=22)
        self.crear_titulo_seccion(
            self.vista_actual,
            "📊 Resumen operativo de la finca",
            "Consulta indicadores generales, genera reportes exportables y visualiza métricas de gestión."
        )
        
        frame_cards = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_cards.pack(fill="x", pady=5)
        self.card_sanidad = self.crear_card_dashboard(
            frame_cards,
            "💉 Tratamientos Sanitarios",
            "0",
            "#FFF3E0",
            "#E65100"
        )
        self.card_sanidad.pack(side="left", padx=8, expand=True, fill="both")
        
        self.card_alimento = self.crear_card_dashboard(
            frame_cards,
            "🌾 Total Alimento Suministrado",
            "0.00 Kg",
            "#E8F5E9",
            "#1B5E20"
        )
        self.card_alimento.pack(side="left", padx=8, expand=True, fill="both")
        
        self.card_pesajes = self.crear_card_dashboard(
            frame_cards,
            "⚖️ Peso Promedio General",
            "0.00 Kg",
            "#E3F2FD",
            "#0D47A1"
        )
        self.card_pesajes.pack(side="left", padx=8, expand=True, fill="both")
        
        self.card_ganado_rep = self.crear_card_dashboard(
            frame_cards,
            "🐄 Ganado Registrado",
            "0",
            "#F1F8E9",
            "#33691E"
        )
        self.card_ganado_rep.pack(side="left", padx=8, expand=True, fill="both")
        
        # Gráfico
        frame_grafico = ctk.CTkFrame(
            self.vista_actual,
            fg_color="#FAFAFA",
            corner_radius=18,
            border_width=1,
            border_color="#E0E0E0"
        )
        frame_grafico.pack(fill="x", pady=(22, 10))
        ctk.CTkLabel(
            frame_grafico,
            text="📈 Comparación visual de métricas",
            font=self.font_subtitulo,
            text_color=self.COLOR_VERDE_OSCURO
        ).pack(anchor="w", padx=18, pady=(16, 8))
        
        self.canvas_grafico = tk.Canvas(
            frame_grafico,
            height=190,
            bg="#FAFAFA",
            highlightthickness=0
        )
        self.canvas_grafico.pack(fill="x", padx=15, pady=(0, 15))
        
        # Acciones
        frame_acciones = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_acciones.pack(pady=15)
        
        ctk.CTkButton(
            frame_acciones,
            text="🔄 Recargar Métricas",
            fg_color=self.COLOR_VERDE_OSCURO,
            hover_color="#143016",
            width=160,
            height=38,
            command=self.calcular_reportes_db
        ).grid(row=0, column=0, padx=8)
        
        ctk.CTkButton(
            frame_acciones,
            text="📊 Exportar CSV",
            fg_color=self.COLOR_VERDE_MEDIO,
            hover_color="#1B5E20",
            width=160,
            height=38,
            command=self.exportar_reporte_csv
        ).grid(row=0, column=1, padx=8)
        
        ctk.CTkButton(
            frame_acciones,
            text="📄 Generar Reporte HTML/PDF",
            fg_color=self.COLOR_ROJO,
            hover_color="#B71C1C",
            width=190,
            height=38,
            command=self.exportar_reporte_pdf
        ).grid(row=0, column=2, padx=8)
        
        self.calcular_reportes_db()

    def calcular_reportes_db(self):
        conn = obtener_conexion()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM sanidad")
            total_sani = cursor.fetchone()[0] or 0
            cursor.execute("SELECT SUM(cantidad_kg) FROM alimentacion")
            total_alim = float(cursor.fetchone()[0] or 0.0)
            cursor.execute("SELECT AVG(peso_kg) FROM pesajes")
            avg_peso = float(cursor.fetchone()[0] or 0.0)
            cursor.execute("SELECT COUNT(*) FROM ganado")
            total_ganado = cursor.fetchone()[0] or 0
            
            self.card_sanidad.valor_label.configure(text=f"{total_sani} registros")
            self.card_alimento.valor_label.configure(text=f"{total_alim:.2f} Kg")
            self.card_pesajes.valor_label.configure(text=f"{avg_peso:.2f} Kg")
            self.card_ganado_rep.valor_label.configure(text=f"{total_ganado} animales")
            
            self.dibujar_graficos_finca(total_alim, total_sani, avg_peso, total_ganado)
        except Exception as e:
            print(f"Error al compilar métricas: {e}")
            messagebox.showerror("Error", f"No se pudieron calcular las métricas.\nDetalle: {e}")
        finally:
            cursor.close()
            conn.close()

    def dibujar_graficos_finca(self, alimento, sanidad, peso_promedio, ganado):
        self.canvas_grafico.delete("all")
        datos = [
            ("Alimento kg", alimento, "#4CAF50"),
            ("Sanidad", sanidad, "#FF9800"),
            ("Peso prom.", peso_promedio, "#2196F3"),
            ("Ganado", ganado, "#8BC34A")
        ]
        max_val = max([valor for _, valor, _ in datos] + [1])
        x_inicio = 80
        y_base = 150
        ancho_barra = 95
        espacio = 145
        altura_max = 105
        
        self.canvas_grafico.create_line(40, y_base, 720, y_base, fill="#B0BEC5", width=2)
        for i, (nombre, valor, color) in enumerate(datos):
            x1 = x_inicio + i * espacio
            x2 = x1 + ancho_barra
            alto = int((valor / max_val) * altura_max) if max_val else 0
            y1 = y_base - alto
            self.canvas_grafico.create_rectangle(x1, y1, x2, y_base, fill=color, outline="")
            self.canvas_grafico.create_text(
                x1 + ancho_barra / 2,
                y1 - 12,
                text=f"{valor:.1f}" if isinstance(valor, float) else str(valor),
                font=("Segoe UI", 10, "bold"),
                fill="#263238"
            )
            self.canvas_grafico.create_text(
                x1 + ancho_barra / 2,
                y_base + 18,
                text=nombre,
                font=("Segoe UI", 9, "bold"),
                fill="#455A64"
            )

    def exportar_reporte_csv(self):
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")],
            title="Guardar Reporte CSV",
            initialfile="Reporte_Estadistico_Finca.csv"
        )
        if not ruta_archivo:
            return
        conn = obtener_conexion()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar con SQL Server.")
            return
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM sanidad")
            t_sani = cursor.fetchone()[0] or 0
            cursor.execute("SELECT SUM(cantidad_kg) FROM alimentacion")
            t_alim = float(cursor.fetchone()[0] or 0.0)
            cursor.execute("SELECT AVG(peso_kg) FROM pesajes")
            a_peso = float(cursor.fetchone()[0] or 0.0)
            cursor.execute("SELECT COUNT(*) FROM ganado")
            t_ganado = cursor.fetchone()[0] or 0
            
            with open(ruta_archivo, mode="w", newline="", encoding="utf-8-sig") as archivo:
                escritor = csv.writer(archivo, delimiter=";")
                escritor.writerow(["FINCA EL PUENTE - REPORTE DE MÉTRICAS"])
                escritor.writerow(["Fecha de generación", datetime.date.today().strftime("%d/%m/%Y")])
                escritor.writerow([])
                escritor.writerow(["Indicador", "Valor Actual"])
                escritor.writerow(["Ganado Registrado", f"{t_ganado} animales"])
                escritor.writerow(["Controles Sanitarios", f"{t_sani} registros"])
                escritor.writerow(["Total Alimento Suministrado", f"{t_alim:.2f} Kg"])
                escritor.writerow(["Peso Promedio General", f"{a_peso:.2f} Kg"])
                escritor.writerow([])
                escritor.writerow(["--- INVENTARIO DE GANADO ---"])
                escritor.writerow(["Código", "Nombre", "Raza", "Sexo", "F. Nacimiento", "Peso Inicial", "Estado"])
                cursor.execute("SELECT codigo, nombre, raza, sexo, fecha_nacimiento, peso_inicial, estado FROM ganado")
                for fila in cursor.fetchall():
                    escritor.writerow([
                        fila[0],
                        fila[1],
                        fila[2],
                        fila[3],
                        fila[4],
                        f"{float(fila[5] or 0):.2f}",
                        fila[6]
                    ])
            messagebox.showinfo("Reporte generado", "🎉 Reporte CSV generado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al guardar el reporte.\nDetalle: {e}")
        finally:
            cursor.close()
            conn.close()

    def exportar_reporte_pdf(self):
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("Reporte Web Imprimible", "*.html")],
            title="Generar Reporte Ejecutivo Oficial",
            initialfile="Reporte_Finca_El_Puente.html"
        )
        if not ruta_archivo:
            return
        conn = obtener_conexion()
        if not conn:
            messagebox.showerror("Error", "No se pudo conectar con SQL Server.")
            return
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM sanidad")
            t_sani = cursor.fetchone()[0] or 0
            cursor.execute("SELECT SUM(cantidad_kg) FROM alimentacion")
            t_alim = float(cursor.fetchone()[0] or 0.0)
            cursor.execute("SELECT AVG(peso_kg) FROM pesajes")
            a_peso = float(cursor.fetchone()[0] or 0.0)
            cursor.execute("SELECT COUNT(*) FROM ganado")
            t_gana = cursor.fetchone()[0] or 0
            max_val = max(t_alim, t_sani * 10, a_peso, t_gana, 1)
            w_alim = (t_alim / max_val) * 100
            w_sani = ((t_sani * 10) / max_val) * 100
            w_peso = (a_peso / max_val) * 100
            w_gana = (t_gana / max_val) * 100
            
            with open(ruta_archivo, mode="w", encoding="utf-8") as html:
                html.write(f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Reporte Finca El Puente</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 40px;
            color: #263238;
            background: #f4f6f4;
        }}
        .documento {{
            background: white;
            padding: 35px;
            border-radius: 18px;
            box-shadow: 0 8px 28px rgba(0,0,0,.08);
        }}
        .header {{
            text-align: center;
            border-bottom: 4px solid #1E4620;
            padding-bottom: 18px;
        }}
        .header h1 {{
            color: #1E4620;
            margin-bottom: 5px;
        }}
        .meta {{
            text-align: right;
            font-size: 12px;
            color: #607D8B;
            margin-top: 10px;
        }}
        h2 {{
            color: #1E4620;
            margin-top: 30px;
        }}
        .metricas {{
            display: flex;
            gap: 12px;
            margin: 20px 0;
        }}
        .card {{
            background: #f4fdf4;
            border: 1px solid #c8e6c9;
            padding: 16px;
            border-radius: 12px;
            width: 25%;
            text-align: center;
        }}
        .card h3 {{
            margin: 0;
            font-size: 13px;
            color: #2E7D32;
        }}
        .card p {{
            font-size: 21px;
            font-weight: bold;
            margin: 10px 0 0 0;
            color: #1B5E20;
        }}
        .chart-container {{
            background: #FAFAFA;
            border: 1px solid #E0E0E0;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
        }}
        .bar-group {{
            margin-bottom: 16px;
        }}
        .bar-label {{
            font-weight: bold;
            font-size: 13px;
            margin-bottom: 6px;
        }}
        .bar-bg {{
            background: #E0E0E0;
            border-radius: 8px;
            width: 100%;
            height: 26px;
            overflow: hidden;
        }}
        .bar {{
            height: 100%;
            border-radius: 8px;
        }}
        .alim {{ background: #4CAF50; width: {w_alim}%; }}
        .sani {{ background: #FF9800; width: {w_sani}%; }}
        .peso {{ background: #2196F3; width: {w_peso}%; }}
        .gana {{ background: #8BC34A; width: {w_gana}%; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            background: white;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
            font-size: 13px;
        }}
        th {{
            background-color: #1E4620;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f7f7f7;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            font-size: 11px;
            color: #607D8B;
        }}
    </style>
</head>
<body>
    <div class="documento">
        <div class="header">
            <h1>REPORTE OPERATIVO OFICIAL</h1>
            <h3>SISTEMA DE GESTIÓN GANADERA - FINCA EL PUENTE</h3>
            <div class="meta">Generado el: {datetime.date.today().strftime('%d/%m/%Y')}</div>
        </div>
        <h2>1. Resumen de Estadísticas</h2>
        <div class="metricas">
            <div class="card"><h3>Ganado Registrado</h3><p>{t_gana}</p></div>
            <div class="card"><h3>Sanidad Aplicada</h3><p>{t_sani}</p></div>
            <div class="card"><h3>Alimento Total</h3><p>{t_alim:.2f} Kg</p></div>
            <div class="card"><h3>Peso Promedio</h3><p>{a_peso:.2f} Kg</p></div>
        </div>
        <h2>2. Gráficos Comparativos</h2>
        <div class="chart-container">
            <div class="bar-group">
                <div class="bar-label">Alimentación total: {t_alim:.2f} Kg</div>
                <div class="bar-bg"><div class="bar alim"></div></div>
            </div>
            <div class="bar-group">
                <div class="bar-label">Controles sanitarios: {t_sani} registros</div>
                <div class="bar-bg"><div class="bar sani"></div></div>
            </div>
            <div class="bar-group">
                <div class="bar-label">Peso promedio: {a_peso:.2f} Kg</div>
                <div class="bar-bg"><div class="bar peso"></div></div>
            </div>
            <div class="bar-group">
                <div class="bar-label">Ganado registrado: {t_gana} animales</div>
                <div class="bar-bg"><div class="bar gana"></div></div>
            </div>
        </div>
        <h2>3. Inventario Analítico de Animales</h2>
        <table>
            <thead>
                <tr>
                    <th>Código</th>
                    <th>Nombre</th>
                    <th>Raza</th>
                    <th>Sexo</th>
                    <th>Estado</th>
                </tr>
            </thead>
            <tbody>
""")
                cursor.execute("SELECT codigo, nombre, raza, sexo, estado FROM ganado")
                for fila in cursor.fetchall():
                    html.write(f"""
                <tr>
                    <td>{fila[0]}</td>
                    <td>{fila[1]}</td>
                    <td>{fila[2]}</td>
                    <td>{fila[3]}</td>
                    <td><strong>{fila[4]}</strong></td>
                </tr>
""")
                html.write("""
            </tbody>
        </table>
        <div class="footer">
            © 2026 Finca El Puente • UTP Chiriquí • Sistema de Base de Datos II
        </div>
    </div>
</body>
</html>
""")
            messagebox.showinfo(
                "Reporte Generado",
                "El reporte se generó con éxito.\nSe abrirá en tu navegador para imprimir o guardar como PDF."
            )
            webbrowser.open(f"file://{os.path.abspath(ruta_archivo)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo compilar el reporte.\nDetalle: {e}")
        finally:
            cursor.close()
            conn.close()

# =================================================================
# CHATBOT / ASISTENTE IA
# =================================================================
class ChatbotWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Asistente Virtual IA — Finca El Puente")
        self.geometry("500x640")
        self.configure(fg_color="#F4F6F4")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        
        self.header = ctk.CTkFrame(self, fg_color="#1E4620", height=65, corner_radius=0)
        self.header.pack(fill="x", side="top")
        
        self.lbl_titulo_chat = ctk.CTkLabel(
            self.header,
            text="🤖 Asistente Virtual Ganadero",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        )
        self.lbl_titulo_chat.pack(pady=10, padx=16, side="left")
        
        self.lbl_estado = ctk.CTkLabel(
            self.header,
            text="● SQL Server",
            text_color="#81C784",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")
        )
        self.lbl_estado.pack(pady=15, padx=16, side="right")
        
        self.historial_mensajes = ctk.CTkScrollableFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=16,
            border_width=1,
            border_color="#E0E0E0"
        )
        self.historial_mensajes.pack(fill="both", expand=True, padx=16, pady=16)
        
        self.frame_entrada = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_entrada.pack(fill="x", side="bottom", padx=16, pady=(0, 16))
        
        self.ent_consulta = ctk.CTkEntry(
            self.frame_entrada,
            placeholder_text="Pregunta por un animal, peso o vacuna...",
            fg_color="white",
            border_color="#B0BEC5",
            height=42,
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.ent_consulta.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.ent_consulta.bind("<Return>", lambda event: self.enviar_consulta())
        
        self.btn_enviar = ctk.CTkButton(
            self.frame_entrada,
            text="Enviar  🚀",
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            width=95,
            height=42,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self.enviar_consulta
        )
        self.btn_enviar.pack(side="right")
        
        self.agregar_burbuja_texto(
            "¡Hola! Soy el Asistente Inteligente de Finca El Puente 🐄\n\n"
            "Puedo ayudarte con consultas como:\n"
            "• Estadísticas generales de la finca.\n"
            "• Datos de un animal por código o nombre.\n"
            "• Información sobre sanidad y vacunas.\n"
            "• Consejos básicos de alimentación ganadera.",
            es_asistente=True
        )

    def enviar_consulta(self):
        consulta = self.ent_consulta.get().strip()
        if not consulta:
            
            return
        self.agregar_burbuja_texto(consulta, es_asistente=False)
        self.ent_consulta.delete(0, "end")
        self.procesar_ia_ganadera(consulta)

    def agregar_burbuja_texto(self, texto, es_asistente=True):
        contenedor = ctk.CTkFrame(self.historial_mensajes, fg_color="transparent")
        contenedor.pack(fill="x", pady=6)

        if es_asistente:
            color_fondo = "#ECEFF1"
            color_texto = "#263238"
            lado_alineado = "left"
        else:
            color_fondo = "#E8F5E9"
            color_texto = "#1B5E20"
            lado_alineado = "right"

        burbuja = ctk.CTkFrame(contenedor, fg_color=color_fondo, corner_radius=14)
        burbuja.pack(side=lado_alineado, padx=10, ipady=7, ipadx=11)

        lbl = ctk.CTkLabel(
            burbuja,
            text=texto,
            text_color=color_texto,
            wraplength=330,
            justify="left",
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        lbl.pack()

        try:
            self.historial_mensajes._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass

    def procesar_ia_ganadera(self, consulta):
        consulta_min = consulta.lower()

        conn = obtener_conexion()
        if not conn:
            self.agregar_burbuja_texto("⚠️ No logré conectar con SQL Server.", es_asistente=True)
            return
        
        cursor = conn.cursor()
        try:
            if any(x in consulta_min for x in ["estadística", "estadistica", "general", "finca", "resumen", "total", "indicador", "promedio"]):
                cursor.execute("SELECT COUNT(*) FROM ganado")
                total_ganado = cursor.fetchone()[0] or 0

                cursor.execute("SELECT SUM(cantidad_kg) FROM alimentacion")
                total_alimento = float(cursor.fetchone()[0] or 0.0)

                cursor.execute("SELECT AVG(peso_kg) FROM pesajes")
                peso_promedio = float(cursor.fetchone()[0] or 0.0)

                respuesta = (
                    f"📊 Reporte Estadístico Automatizado\n\n"
                    f"Actualmente en la Finca El Puente tenemos:\n"
                    f"• {total_ganado} cabezas de ganado registradas.\n"
                    f"• {total_alimento:.2f} Kg de alimento acumulado.\n"
                    f"• Peso promedio general: {peso_promedio:.2f} Kg."
                )
                self.agregar_burbuja_texto(respuesta, es_asistente=True)
                return
                
            palabras = consulta.split()
            ejemplar_encontrado = None

            for palabra in palabras:
                palabra_limpia = palabra.replace("?", "").replace(",", "").replace(".", "").strip()

                cursor.execute(
                    """
                    SELECT codigo, nombre, raza, sexo, peso_inicial, estado, observaciones
                    FROM ganado
                    WHERE codigo = ? OR nombre LIKE ?
                    """,
                    (palabra_limpia, f"%{palabra_limpia}%")
                )

                fila = cursor.fetchone()
                if fila:
                    ejemplar_encontrado = fila
                    break

            if ejemplar_encontrado:
                cod, nom, raz, sex, peso_i, est, obs = ejemplar_encontrado
                obs = obs or "Sin notas adicionales registradas."

                cursor.execute("SELECT COUNT(*) FROM sanidad WHERE codigo_animal = ?", (cod,))
                cont_sani = cursor.fetchone()[0] or 0

                cursor.execute("SELECT SUM(cantidad_kg) FROM alimentacion WHERE codigo_animal = ?", (cod,))
                cont_alim = float(cursor.fetchone()[0] or 0.0)

                respuesta = (
                    f"🐄 Hoja de Datos — {nom} ({cod})\n\n"
                    f"• Raza: {raz}\n"
                    f"• Sexo: {sex}\n"
                    f"• Estado: {est}\n"
                    f"• Peso inicial: {float(peso_i or 0):.2f} Kg\n"
                    f"• Controles médicos: {cont_sani}\n"
                    f"• Alimentación acumulada: {cont_alim:.2f} Kg\n"
                    f"• Observaciones: {obs}"
                )
                self.agregar_burbuja_texto(respuesta, es_asistente=True)
                return
                
            if any(x in consulta_min for x in ["vacuna", "enfermo", "sanidad", "tratamiento", "médico", "medico", "salud", "inyección", "inyeccion"]):
                cursor.execute("SELECT COUNT(*) FROM sanidad")
                total_tratamientos = cursor.fetchone()[0] or 0

                respuesta = (
                    f"💉 Asistencia Clínica Veterinaria\n\n"
                    f"El sistema registra {total_tratamientos} tratamientos aplicados.\n"
                    f"Recuerde mantener actualizado el historial sanitario para facilitar el seguimiento del animal."
                )
                self.agregar_burbuja_texto(respuesta, es_asistente=True)
                return
                
            if any(x in consulta_min for x in ["consejo", "brahman", "pasto", "alimentar", "silo", "melaza", "calor", "agua"]):
                respuesta = (
                    f"🌾 Recomendación Ganadera\n\n"
                    f"• Mantenga agua fresca disponible durante todo el día.\n"
                    f"• En épocas secas, complemente el pastoreo con sales minerales y melaza.\n"
                    f"• Registre la alimentación para controlar mejor los costos y el rendimiento."
                )
                self.agregar_burbuja_texto(respuesta, es_asistente=True)
                return
                
            if any(x in consulta_min for x in ["hola", "buenas", "saludo", "hey", "asistente"]):
                self.agregar_burbuja_texto(
                    "¡Hola! Un placer saludarte. Estoy listo para procesar tus consultas relacionales sobre la Finca El Puente.",
                    es_asistente=True
                )
                return
                
            self.agregar_burbuja_texto(
                f"No encontré información específica sobre: '{consulta}'.\n"
                f"Prueba preguntando por un código de animal, un nombre, estadísticas o sanidad.",
                es_asistente=True
            )

        except Exception as e:
            self.agregar_burbuja_texto(f"❌ Error al consultar la información: {e}", es_asistente=True)
        finally:
            cursor.close()
            conn.close()

# =================================================================
# PUNTO DE ENTRADA PRINCIPAL INTEGRADO
# =================================================================
if __name__ == "__main__":
    app = AppGanado()
    app.mainloop()
