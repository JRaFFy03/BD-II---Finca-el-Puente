# =================================================================
# PROYECTO FINAL: FINCA EL PUENTE
# ASIGNATURA: BASE DE DATOS II — PROFESOR BALTAZAR
# ARCHIVO: gui.py (VERSIÓN FINAL CON ASISTENTE IA Y GENERADOR QR)
# =================================================================

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from PIL import Image
import urllib.request
import urllib.parse
import io
import datetime
import webbrowser
import os
from conexion import obtener_conexion

ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("green")  

class AppGanado(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Finca El Puente — Sistema Inteligente de Gestión Ganadera")
        self.geometry("1200x720")
        self.configure(fg_color="#F4F6F4") # Fondo general sutil
        
        # Fuentes institucionales
        self.font_titulo = ctk.CTkFont(family="Segoe UI", size=22, weight="bold")
        self.font_sub = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        self.font_cuerpo = ctk.CTkFont(family="Helvetica", size=13)
        
        # Guardar binarios de QR temporalmente para descargas
        self.qr_temp_data = None
        self.qr_temp_codigo = None

        self.img_sidebar = None
        try:
            url_finca = "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?q=80&w=300&auto=format&fit=crop"
            req = urllib.request.Request(url_finca, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as u:
                raw_data = u.read()
            img_original = Image.open(io.BytesIO(raw_data))
            self.img_sidebar = ctk.CTkImage(light_image=img_original, dark_image=img_original, size=(220, 130))
        except Exception as e:
            print(f"Nota: Iniciando con menú de color sólido (Sin Internet para Banner): {e}")

        # GRID PRINCIPAL
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.menu_lateral = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1E4620")
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        
        if self.img_sidebar:
            self.lbl_banner = ctk.CTkLabel(self.menu_lateral, image=self.img_sidebar, text="")
            self.lbl_banner.pack(pady=(0, 15), fill="x")
        else:
            self.lbl_logo = ctk.CTkLabel(self.menu_lateral, text="🚜 Finca El Puente", font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color="white")
            self.lbl_logo.pack(pady=25)

        self.btn_dashboard = ctk.CTkButton(self.menu_lateral, text="🏡 Dashboard", fg_color="transparent", text_color="white", anchor="w", font=self.font_cuerpo, command=self.mostrar_dashboard)
        self.btn_dashboard.pack(fill="x", padx=15, pady=5)
        
        self.btn_ganado = ctk.CTkButton(self.menu_lateral, text="🐄 Control de Ganado", fg_color="transparent", text_color="white", anchor="w", font=self.font_cuerpo, command=self.mostrar_ganado)
        self.btn_ganado.pack(fill="x", padx=15, pady=5)
        
        self.btn_sanidad = ctk.CTkButton(self.menu_lateral, text="💉 Control Sanitario", fg_color="transparent", text_color="white", anchor="w", font=self.font_cuerpo, command=self.mostrar_sanidad)
        self.btn_sanidad.pack(fill="x", padx=15, pady=5)
        
        self.btn_alimentacion = ctk.CTkButton(self.menu_lateral, text="🌾 Alimentación", fg_color="transparent", text_color="white", anchor="w", font=self.font_cuerpo, command=self.mostrar_alimentacion)
        self.btn_alimentacion.pack(fill="x", padx=15, pady=5)
        
        self.btn_pesajes = ctk.CTkButton(self.menu_lateral, text="⚖️ Control de Pesajes", fg_color="transparent", text_color="white", anchor="w", font=self.font_cuerpo, command=self.mostrar_pesajes)
        self.btn_pesajes.pack(fill="x", padx=15, pady=5)
        
        self.btn_reportes = ctk.CTkButton(self.menu_lateral, text="📊 Reportes y Gráficos", fg_color="transparent", text_color="white", anchor="w", font=self.font_cuerpo, command=self.mostrar_reportes)
        self.btn_reportes.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(self.menu_lateral, text="UTP - Chiriquí 2026", text_color="#A5D6A7", font=ctk.CTkFont(size=10)).pack(side="bottom", pady=15)

        self.frame_derecho = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_derecho.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_derecho.grid_columnconfigure(0, weight=1)
        self.frame_derecho.grid_rowconfigure(1, weight=1)
        
        self.lbl_titulo_modulo = ctk.CTkLabel(self.frame_derecho, text="Cargando Sistema...", font=self.font_titulo, text_color="#1E4620")
        self.lbl_titulo_modulo.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 5))
        
        self.contenedor_principal = ctk.CTkFrame(self.frame_derecho, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E0E0")
        self.contenedor_principal.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.contenedor_principal.grid_columnconfigure(0, weight=1)
        self.contenedor_principal.grid_rowconfigure(0, weight=1)
        
        self.btn_chatbot_flotante = ctk.CTkButton(
            self, text="💬 Asistente IA", fg_color="#2E7D32", hover_color="#1B5E20", text_color="white",
            width=130, height=40, corner_radius=20, font=ctk.CTkFont(family="Helvetica", size=13, weight="bold"),
            command=self.abrir_ventana_chatbot
        )
        self.btn_chatbot_flotante.place(relx=0.98, rely=0.96, anchor="se")

        # Cargar Dashboard inicial
        self.mostrar_dashboard()

    def limpiar_contenedor(self):
        for widget in self.contenedor_principal.winfo_children():
            widget.destroy()

    def abrir_ventana_chatbot(self):
        ChatbotWindow(self)

    # =================================================================
    # MÓDULO 1: DASHBOARD
    # =================================================================
    def mostrar_dashboard(self):
        self.limpiar_contenedor()
        self.lbl_titulo_modulo.configure(text="Panel de Control General (Dashboard)")
        
        self.vista_actual = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.vista_actual.pack(padx=30, pady=30, fill="both", expand=True)
        
        lbl_saludo = ctk.CTkLabel(self.vista_actual, text="¡Bienvenido al Panel de Administración de Finca El Puente!", font=self.font_sub, text_color="#333333")
        lbl_saludo.pack(anchor="w", pady=(0, 20))
        
        self.card_total = ctk.CTkFrame(self.vista_actual, fg_color="#E8F5E9", corner_radius=12, border_width=1, border_color="#C8E6C9")
        self.card_total.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(self.card_total, text="Ejemplares Totales de Ganado", text_color="#2E7D32", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
        self.lbl_contador_ganado = ctk.CTkLabel(self.card_total, text="Cargando...", text_color="#1B5E20", font=ctk.CTkFont(size=36, weight="bold"))
        self.lbl_contador_ganado.pack(pady=(0, 15))
        
        self.cargar_contadores_dashboard()

    def cargar_contadores_dashboard(self):
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT COUNT(*) FROM ganado")
                total = cursor.fetchone()[0]
                self.lbl_contador_ganado.configure(text=f"{total} Animales Activos")
            except Exception as e:
                self.lbl_contador_ganado.configure(text="Error de Carga")
                print(f"Error en dashboard: {e}")
            finally:
                cursor.close()
                conn.close()

    # =================================================================
    # MÓDULO 2: CONTROL DE GANADO (CON INTEGRACIÓN QR MÓVIL)
    # =================================================================
    def mostrar_ganado(self):
        self.limpiar_contenedor()
        self.lbl_titulo_modulo.configure(text="Módulo 1: Control e Inventario de Ganado")
        
        self.vista_actual = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.vista_actual.grid(row=0, column=0, sticky="nsew", padx=20, pady=15)
        
        self.vista_actual.grid_columnconfigure(0, weight=0)
        self.vista_actual.grid_columnconfigure(1, weight=0)
        self.vista_actual.grid_columnconfigure(2, weight=1)
        
        # --- PANEL IZQUIERDO: FORMULARIO ---
        frame_inputs = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_inputs.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        ctk.CTkLabel(frame_inputs, text="Código del Animal:", font=self.font_cuerpo).grid(row=0, column=0, sticky="w", pady=2)
        self.ent_codigo = ctk.CTkEntry(frame_inputs, width=170)
        self.ent_codigo.grid(row=0, column=1, pady=2, padx=5)
        
        ctk.CTkLabel(frame_inputs, text="Nombre / Alias:", font=self.font_cuerpo).grid(row=1, column=0, sticky="w", pady=2)
        self.ent_nombre = ctk.CTkEntry(frame_inputs, width=170)
        self.ent_nombre.grid(row=1, column=1, pady=2, padx=5)
        
        ctk.CTkLabel(frame_inputs, text="Raza Ganadera:", font=self.font_cuerpo).grid(row=2, column=0, sticky="w", pady=2)
        self.cmb_raza = ctk.CTkComboBox(frame_inputs, values=["Brahman Gris", "Brahman Rojo", "Nelore", "Gyr", "Pardo Suizo"], width=170)
        self.cmb_raza.grid(row=2, column=1, pady=2, padx=5)
        
        ctk.CTkLabel(frame_inputs, text="Sexo:", font=self.font_cuerpo).grid(row=3, column=0, sticky="w", pady=2)
        self.cmb_sexo = ctk.CTkComboBox(frame_inputs, values=["Macho", "Hembra"], width=170)
        self.cmb_sexo.grid(row=3, column=1, pady=2, padx=5)
        
        ctk.CTkLabel(frame_inputs, text="F. Nacimiento (AAAA-MM-DD):", font=self.font_cuerpo).grid(row=4, column=0, sticky="w", pady=2)
        self.ent_fecha_nac = ctk.CTkEntry(frame_inputs, width=170)
        self.ent_fecha_nac.grid(row=4, column=1, pady=2, padx=5)
        self.ent_fecha_nac.insert(0, str(datetime.date.today()))
        
        ctk.CTkLabel(frame_inputs, text="Peso Inicial (Kg):", font=self.font_cuerpo).grid(row=5, column=0, sticky="w", pady=2)
        self.ent_peso_ini = ctk.CTkEntry(frame_inputs, width=170)
        self.ent_peso_ini.grid(row=5, column=1, pady=2, padx=5)
        
        ctk.CTkLabel(frame_inputs, text="Estado:", font=self.font_cuerpo).grid(row=6, column=0, sticky="w", pady=2)
        self.cmb_estado = ctk.CTkComboBox(frame_inputs, values=["Activo", "Vendido", "Enfermo", "Inactivo"], width=170)
        self.cmb_estado.grid(row=6, column=1, pady=2, padx=5)

        ctk.CTkLabel(frame_inputs, text="Código del Padre:", font=self.font_cuerpo).grid(row=7, column=0, sticky="w", pady=2)
        self.ent_padre = ctk.CTkEntry(frame_inputs, width=170)
        self.ent_padre.grid(row=7, column=1, pady=2, padx=5)

        ctk.CTkLabel(frame_inputs, text="Código de la Madre:", font=self.font_cuerpo).grid(row=8, column=0, sticky="w", pady=2)
        self.ent_madre = ctk.CTkEntry(frame_inputs, width=170)
        self.ent_madre.grid(row=8, column=1, pady=2, padx=5)

        ctk.CTkLabel(frame_inputs, text="Observaciones:", font=self.font_cuerpo).grid(row=9, column=0, sticky="w", pady=2)
        self.ent_observaciones = ctk.CTkEntry(frame_inputs, width=170)
        self.ent_observaciones.grid(row=9, column=1, pady=2, padx=5)
        
        frame_btn = ctk.CTkFrame(frame_inputs, fg_color="transparent")
        frame_btn.grid(row=10, column=0, columnspan=2, pady=10)
        
        ctk.CTkButton(frame_btn, text="💾 Registrar", width=80, fg_color="#1E4620", hover_color="#143016", command=self.guardar_ganado).grid(row=0, column=0, padx=3)
        ctk.CTkButton(frame_btn, text="🗑️ Eliminar", width=80, fg_color="#C62828", hover_color="#B71C1C", command=self.eliminar_ganado).grid(row=0, column=1, padx=3)

        # --- PANEL CENTRAL: VISUALIZADOR DE CÓDIGO QR ---
        self.frame_qr = ctk.CTkFrame(self.vista_actual, fg_color="#F9F9F9", width=180, corner_radius=10, border_width=1, border_color="#E0E0E0")
        self.frame_qr.grid(row=0, column=1, padx=15, pady=5, sticky="ns")
        
        ctk.CTkLabel(self.frame_qr, text="Identificación QR", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#1E4620").pack(pady=10)
        
        self.lbl_qr_visual = ctk.CTkLabel(self.frame_qr, text="Seleccione un\nanimal de la\ntabla para\ngenerar QR", text_color="#555555", width=140, height=140, fg_color="#FFFFFF", corner_radius=8)
        self.lbl_qr_visual.pack(pady=10, padx=15)
        
        self.btn_guardar_qr = ctk.CTkButton(self.frame_qr, text="📥 Descargar QR", width=130, fg_color="#2E7D32", hover_color="#1B5E20", state="disabled", command=self.descargar_qr_seleccionado)
        self.btn_guardar_qr.pack(pady=10)

        # --- PANEL DERECHO: TABLA TREEVIEW ---
        self.tabla_ganado = None
        self.crear_tabla_ganado_vista()
        self.cargar_datos_ganado()

    def crear_tabla_ganado_vista(self):
        frame_tabla = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_tabla.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        columnas = ("codigo", "nombre", "raza", "sexo", "peso", "estado")
        self.tabla_ganado = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=18)
        
        self.tabla_ganado.heading("codigo", text="Código")
        self.tabla_ganado.heading("nombre", text="Nombre")
        self.tabla_ganado.heading("raza", text="Raza")
        self.tabla_ganado.heading("sexo", text="Sexo")
        self.tabla_ganado.heading("peso", text="Peso (Kg)")
        self.tabla_ganado.heading("estado", text="Estado")
        
        self.tabla_ganado.column("codigo", width=80, anchor="center")
        self.tabla_ganado.column("nombre", width=100)
        self.tabla_ganado.column("raza", width=100)
        self.tabla_ganado.column("sexo", width=65, anchor="center")
        self.tabla_ganado.column("peso", width=75, anchor="e")
        self.tabla_ganado.column("estado", width=75, anchor="center")
        
        self.tabla_ganado.pack(fill="both", expand=True)
        self.tabla_ganado.bind("<<TreeviewSelect>>", self.on_seleccionar_animal)

    def on_seleccionar_animal(self, event):
        sel = self.tabla_ganado.selection()
        if not sel: return
        valores = self.tabla_ganado.item(sel[0])['values']
        cod_selec = valores[0]

        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT codigo, nombre, raza, sexo, fecha_nacimiento, peso_inicial, estado, padre, madre, observaciones FROM ganado WHERE codigo = ?", (cod_selec,))
                fila = cursor.fetchone()
                if fila:
                    self.ent_codigo.delete(0, 'end')
                    self.ent_codigo.insert(0, fila[0])
                    
                    self.ent_nombre.delete(0, 'end')
                    self.ent_nombre.insert(0, fila[1])
                    
                    self.cmb_raza.set(fila[2])
                    self.cmb_sexo.set(fila[3])
                    
                    self.ent_fecha_nac.delete(0, 'end')
                    self.ent_fecha_nac.insert(0, str(fila[4]))
                    
                    self.ent_peso_ini.delete(0, 'end')
                    self.ent_peso_ini.insert(0, f"{fila[5]:.2f}")
                    
                    self.cmb_estado.set(fila[6])
                    
                    self.ent_padre.delete(0, 'end')
                    self.ent_padre.insert(0, fila[7] if fila[7] else "")
                    
                    self.ent_madre.delete(0, 'end')
                    self.ent_madre.insert(0, fila[8] if fila[8] else "")
                    
                    self.ent_observaciones.delete(0, 'end')
                    self.ent_observaciones.insert(0, fila[9] if fila[9] else "")

                    # Generar QR dinámico
                    self.generar_qr_online(fila[0], fila[1], fila[2], fila[3], fila[5], fila[6])
            except Exception as e:
                print(f"Error al cargar selección: {e}")
            finally:
                cursor.close()
                conn.close()

    def generar_qr_online(self, codigo, nombre, raza, sexo, peso_inicial, estado):
        try:
            # Para cumplir con "consulta de información desde dispositivos móviles",
            # el QR codificará un enlace a la Ficha Móvil Oficial en la nube (GitHub Pages),
            # pasando los parámetros de forma segura para renderizar la tarjeta en el celular.
            url_ficha_movil = (
                f"https://jraffy03.github.io/BD-II---Finca-el-Puente/ficha.html?" # <-- CAMBIA ESTO
                f"id={urllib.parse.quote(str(codigo))}&"
                f"nombre={urllib.parse.quote(str(nombre))}&"
                f"raza={urllib.parse.quote(str(raza))}&"
                f"sexo={urllib.parse.quote(str(sexo))}&"
                f"estado={urllib.parse.quote(str(estado))}&"
                f"peso={urllib.parse.quote(f'{float(peso_inicial):.1f}')}"
            )
            
            datos_url_safe = urllib.parse.quote(url_ficha_movil)
            url_api = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={datos_url_safe}"
            
            req = urllib.request.Request(url_api, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                binario_imagen = response.read()
            
            img_original = Image.open(io.BytesIO(binario_imagen))
            self.img_qr = ctk.CTkImage(light_image=img_original, dark_image=img_original, size=(130, 130))
            self.lbl_qr_visual.configure(image=self.img_qr, text="")
            
            self.qr_temp_data = binario_imagen
            self.qr_temp_codigo = codigo
            self.btn_guardar_qr.configure(state="normal")
            
        except Exception as e:
            self.lbl_qr_visual.configure(image=None, text="Error QR:\nSin Internet")
            self.btn_guardar_qr.configure(state="disabled")
            print(f"Error al generar QR: {e}")

    def descargar_qr_seleccionado(self):
        if not self.qr_temp_data or not self.qr_temp_codigo:
            return
            
        from tkinter import filedialog
        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png")],
            title="Guardar Código QR de Identificación",
            initialfile=f"QR_Identificacion_{self.qr_temp_codigo}.png"
        )
        if not ruta_guardado:
            return
            
        try:
            with open(ruta_guardado, "wb") as f:
                f.write(self.qr_temp_data)
            messagebox.showinfo("Éxito", f"🎉 El código QR de consulta móvil para el animal {self.qr_temp_codigo} se descargó exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

    def cargar_datos_ganado(self):
        for i in self.tabla_ganado.get_children():
            self.tabla_ganado.delete(i)
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, nombre, raza, sexo, peso_inicial, estado FROM ganado")
            for fila in cursor.fetchall():
                self.tabla_ganado.insert("", "end", values=(fila[0], fila[1], fila[2], fila[3], f"{fila[4]:.2f}", fila[5]))
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
            messagebox.showwarning("Atención", "Por favor complete los campos obligatorios.")
            return
        
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO ganado (codigo, nombre, raza, sexo, fecha_nacimiento, peso_inicial, estado, padre, madre, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (cod, nom, raz, sex, fec, float(pes), est, pad, mad, obs))
                conn.commit()
                messagebox.showinfo("Éxito", "Ejemplar registrado exitosamente.")
                self.cargar_datos_ganado()
            except Exception as e:
                messagebox.showerror("Error SQL", f"No se pudo guardar: {e}")
            finally:
                cursor.close()
                conn.close()

    def eliminar_ganado(self):
        sel = self.tabla_ganado.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un animal de la tabla.")
            return
        cod = self.tabla_ganado.item(sel[0])['values'][0]
        
        if messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar al animal {cod}?"):
            conn = obtener_conexion()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM ganado WHERE codigo = ?", (cod,))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Animal eliminado.")
                    self.cargar_datos_ganado()
                except Exception as e:
                    messagebox.showerror("Error SQL", f"No se pudo borrar: {e}")
                finally:
                    cursor.close()
                    conn.close()

    # =================================================================
    # MÓDULO 3: CONTROL SANITARIO (VACUNAS)
    # =================================================================
    def mostrar_sanidad(self):
        self.limpiar_contenedor()
        self.lbl_titulo_modulo.configure(text="Módulo 2: Control Sanitario y Clínico")
        
        self.vista_actual = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.vista_actual.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        frame_inputs = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_inputs.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        ctk.CTkLabel(frame_inputs, text="Código del Animal:", font=self.font_cuerpo).grid(row=0, column=0, sticky="w", pady=4)
        self.ent_sani_cod = ctk.CTkEntry(frame_inputs, width=180)
        self.ent_sani_cod.grid(row=0, column=1, pady=4, padx=5)
        
        ctk.CTkLabel(frame_inputs, text="Tipo de Tratamiento:", font=self.font_cuerpo).grid(row=1, column=0, sticky="w", pady=4)
        self.cmb_sani_tipo = ctk.CTkComboBox(frame_inputs, values=["Vacuna", "Desparasitante", "Vitamina", "Tratamiento Médico"], width=180)
        self.cmb_sani_tipo.grid(row=1, column=1, pady=4, padx=5)
        
        ctk.CTkLabel(frame_inputs, text="Medicamento:", font=self.font_cuerpo).grid(row=2, column=0, sticky="w", pady=4)
        self.ent_sani_med = ctk.CTkEntry(frame_inputs, width=180)
        self.ent_sani_med.grid(row=2, column=1, pady=4, padx=5)
        
        ctk.CTkLabel(frame_inputs, text="Dosis Aplicada:", font=self.font_cuerpo).grid(row=3, column=0, sticky="w", pady=4)
        self.ent_sani_dosis = ctk.CTkEntry(frame_inputs, width=180)
        self.ent_sani_dosis.grid(row=3, column=1, pady=4, padx=5)
        
        ctk.CTkButton(frame_inputs, text="💉 Registrar Tratamiento", fg_color="#1E4620", hover_color="#143016", command=self.guardar_sanidad).grid(row=4, column=0, columnspan=2, pady=15)
        
        self.tabla_sanidad = None
        self.crear_tabla_sanidad_vista()
        self.cargar_datos_sanidad()

    def crear_tabla_sanidad_vista(self):
        frame_tabla = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_tabla.grid(row=0, column=1, padx=15, pady=10, sticky="nsew")
        
        columnas = ("id", "animal", "tipo", "med", "fecha")
        self.tabla_sanidad = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        self.tabla_sanidad.heading("id", text="ID")
        self.tabla_sanidad.heading("animal", text="Animal")
        self.tabla_sanidad.heading("tipo", text="Tipo")
        self.tabla_sanidad.heading("med", text="Medicamento")
        self.tabla_sanidad.heading("fecha", text="Fecha")
        
        self.tabla_sanidad.column("id", width=45)
        self.tabla_sanidad.column("animal", width=90)
        self.tabla_sanidad.column("tipo", width=100)
        self.tabla_sanidad.column("med", width=120)
        self.tabla_sanidad.column("fecha", width=90)
        self.tabla_sanidad.pack(fill="both", expand=True)

    def cargar_datos_sanidad(self):
        for i in self.tabla_sanidad.get_children():
            self.tabla_sanidad.delete(i)
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, codigo_animal, tipo_tratamiento, medicamento, fecha_aplicacion FROM sanidad")
            for fila in cursor.fetchall():
                self.tabla_sanidad.insert("", "end", values=fila)
            cursor.close()
            conn.close()

    def guardar_sanidad(self):
        ani = self.ent_sani_cod.get().strip()
        tip = self.cmb_sani_tipo.get()
        med = self.ent_sani_med.get().strip()
        dos = self.ent_sani_dosis.get().strip()
        fec = str(datetime.date.today())
        
        if not ani or not med or not dos:
            messagebox.showwarning("Campos vacíos", "Llene todos los datos del control de salud.")
            return
            
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO sanidad (codigo_animal, tipo_tratamiento, medicamento, fecha_aplicacion, dosis)
                    VALUES (?, ?, ?, ?, ?)""", (ani, tip, med, fec, dos))
                conn.commit()
                messagebox.showinfo("Listo", "Historial médico guardado con éxito.")
                self.cargar_datos_sanidad()
            except Exception as e:
                messagebox.showerror("Error Relacional", f"Verifique si el código de animal existe.\nDetalle: {e}")
            finally:
                cursor.close()
                conn.close()

    # =================================================================
    # MÓDULO 4: ALIMENTACIÓN
    # =================================================================
    def mostrar_alimentacion(self):
        self.limpiar_contenedor()
        self.lbl_titulo_modulo.configure(text="Módulo 3: Control de Alimentación y Raciones")
        
        self.vista_actual = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.vista_actual.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        frame_inputs = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_inputs.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        ctk.CTkLabel(frame_inputs, text="Código del Animal:", font=self.font_cuerpo).grid(row=0, column=0, sticky="w", pady=4)
        self.ent_alim_cod = ctk.CTkEntry(frame_inputs, width=180)
        self.ent_alim_cod.grid(row=0, column=1, pady=4, padx=5)
        
        ctk.CTkLabel(frame_inputs, text="Tipo de Alimento:", font=self.font_cuerpo).grid(row=1, column=0, sticky="w", pady=4)
        self.cmb_alim_tipo = ctk.CTkComboBox(frame_inputs, values=["Concentrado", "Silo de Maíz", "Pasto de Corte", "Melaza", "Sales Minerales"], width=180)
        self.cmb_alim_tipo.grid(row=1, column=1, pady=4, padx=5)
        
        ctk.CTkLabel(frame_inputs, text="Cantidad Suministrada (Kg):", font=self.font_cuerpo).grid(row=2, column=0, sticky="w", pady=4)
        self.ent_alim_cant = ctk.CTkEntry(frame_inputs, width=180)
        self.ent_alim_cant.grid(row=2, column=1, pady=4, padx=5)
        
        ctk.CTkButton(frame_inputs, text="🌾 Registrar Dieta", fg_color="#1E4620", hover_color="#143016", command=self.guardar_alimentacion).grid(row=3, column=0, columnspan=2, pady=15)
        
        self.tabla_alim = None
        self.crear_tabla_alim_vista()
        self.cargar_datos_alim()

    def crear_tabla_alim_vista(self):
        frame_tabla = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_tabla.grid(row=0, column=1, padx=15, pady=10, sticky="nsew")
        
        columnas = ("id", "animal", "tipo", "cant", "fecha")
        self.tabla_alim = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        self.tabla_alim.heading("id", text="ID")
        self.tabla_alim.heading("animal", text="Animal")
        self.tabla_alim.heading("tipo", text="Tipo Alimento")
        self.tabla_alim.heading("cant", text="Cantidad (Kg)")
        self.tabla_alim.heading("fecha", text="Fecha")
        
        self.tabla_alim.column("id", width=45)
        self.tabla_alim.column("animal", width=90)
        self.tabla_alim.column("tipo", width=120)
        self.tabla_alim.column("cant", width=100)
        self.tabla_alim.column("fecha", width=90)
        self.tabla_alim.pack(fill="both", expand=True)

    def cargar_datos_alim(self):
        for i in self.tabla_alim.get_children():
            self.tabla_alim.delete(i)
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, codigo_animal, tipo_alimento, cantidad_kg, fecha_registro FROM alimentacion")
            for fila in cursor.fetchall():
                self.tabla_alim.insert("", "end", values=(fila[0], fila[1], fila[2], f"{fila[3]:.2f}", fila[4]))
            cursor.close()
            conn.close()

    def guardar_alimentacion(self):
        ani = self.ent_alim_cod.get().strip()
        tip = self.cmb_alim_tipo.get()
        can = self.ent_alim_cant.get().strip()
        fec = str(datetime.date.today())
        
        if not ani or not can:
            messagebox.showwarning("Atención", "Ingrese el código y la cantidad en kilos.")
            return
            
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO alimentacion (codigo_animal, tipo_alimento, cantidad_kg, fecha_registro)
                    VALUES (?, ?, ?, ?)""", (ani, tip, float(can), fec))
                conn.commit()
                messagebox.showinfo("Éxito", "Asignación de alimento guardada.")
                self.cargar_datos_alim()
            except Exception as e:
                messagebox.showerror("Error Relacional", f"Código de animal no registrado en inventario.\nDetalle: {e}")
            finally:
                cursor.close()
                conn.close()

    # =================================================================
    # MÓDULO 5: CONTROL DE PESAJES
    # =================================================================
    def mostrar_pesajes(self):
        self.limpiar_contenedor()
        self.lbl_titulo_modulo.configure(text="Módulo 4: Historial y Evolución de Pesos")
        
        self.vista_actual = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.vista_actual.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        frame_inputs = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_inputs.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        ctk.CTkLabel(frame_inputs, text="Código del Animal:", font=self.font_cuerpo).grid(row=0, column=0, sticky="w", pady=4)
        self.ent_peso_cod = ctk.CTkEntry(frame_inputs, width=180)
        self.ent_peso_cod.grid(row=0, column=1, pady=4, padx=5)
        
        ctk.CTkLabel(frame_inputs, text="Peso Actual Registrado (Kg):", font=self.font_cuerpo).grid(row=1, column=0, sticky="w", pady=4)
        self.ent_peso_kg = ctk.CTkEntry(frame_inputs, width=180)
        self.ent_peso_kg.grid(row=1, column=1, pady=4, padx=5)
        
        ctk.CTkButton(frame_inputs, text="⚖️ Registrar Pesaje", fg_color="#1E4620", hover_color="#143016", command=self.guardar_pesaje).grid(row=2, column=0, columnspan=2, pady=15)
        
        self.tabla_pesajes = None
        self.crear_tabla_pesajes_vista()
        self.cargar_datos_pesajes()

    def crear_tabla_pesajes_vista(self):
        frame_tabla = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_tabla.grid(row=0, column=1, padx=15, pady=10, sticky="nsew")
        
        columnas = ("id", "animal", "peso", "fecha")
        self.tabla_pesajes = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        self.tabla_pesajes.heading("id", text="ID")
        self.tabla_pesajes.heading("animal", text="Animal")
        self.tabla_pesajes.heading("peso", text="Peso Evaluado (Kg)")
        self.tabla_pesajes.heading("fecha", text="Fecha de Pesaje")
        
        self.tabla_pesajes.column("id", width=50)
        self.tabla_pesajes.column("animal", width=100)
        self.tabla_pesajes.column("peso", width=120)
        self.tabla_pesajes.column("fecha", width=100)
        self.tabla_pesajes.pack(fill="both", expand=True)

    def cargar_datos_pesajes(self):
        for i in self.tabla_pesajes.get_children():
            self.tabla_pesajes.delete(i)
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, codigo_animal, peso_kg, fecha_pesaje FROM pesajes")
            for fila in cursor.fetchall():
                self.tabla_pesajes.insert("", "end", values=(fila[0], fila[1], f"{fila[2]:.2f}", fila[3]))
            cursor.close()
            conn.close()

    def guardar_pesaje(self):
        ani = self.ent_peso_cod.get().strip()
        pes = self.ent_peso_kg.get().strip()
        fec = str(datetime.date.today())
        
        if not ani or not pes:
            messagebox.showwarning("Atención", "Complete la báscula con el código y peso.")
            return
            
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO pesajes (codigo_animal, peso_kg, fecha_pesaje)
                    VALUES (?, ?, ?)""", (ani, float(pes), fec))
                conn.commit()
                messagebox.showinfo("Éxito", "Pesaje cronológico añadido.")
                self.cargar_datos_pesajes()
            except Exception as e:
                messagebox.showerror("Error Relacional", f"No se encontró el animal en la Finca.\nDetalle: {e}")
            finally:
                cursor.close()
                conn.close()

    # =================================================================
    # MÓDULO 6: REPORTE, GRÁFICOS Y EXPORTACIÓN COMPLETA (PDF/EXCEL)
    # =================================================================
    def mostrar_reportes(self):
        self.limpiar_contenedor()
        self.lbl_titulo_modulo.configure(text="Módulo 5: Reportes, Gráficos y Métricas Operativas")
        
        self.vista_actual = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.vista_actual.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # --- SUBMÓDULO: TARJETAS INFORMATIVAS ---
        frame_cards = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_cards.pack(fill="x", pady=5)
        
        self.card_sanidad = ctk.CTkFrame(frame_cards, fg_color="#FFF3E0", corner_radius=10)
        self.card_sanidad.pack(side="left", padx=10, expand=True, fill="both")
        ctk.CTkLabel(self.card_sanidad, text="Tratamientos Sanitarios", text_color="#E65100", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=8)
        self.lbl_stat_sanidad = ctk.CTkLabel(self.card_sanidad, text="0", text_color="#BF360C", font=ctk.CTkFont(size=22, weight="bold"))
        self.lbl_stat_sanidad.pack(pady=(0,8))

        self.card_alimento = ctk.CTkFrame(frame_cards, fg_color="#E8F5E9", corner_radius=10)
        self.card_alimento.pack(side="left", padx=10, expand=True, fill="both")
        ctk.CTkLabel(self.card_alimento, text="Total Alimento Suministrado", text_color="#2E7D32", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=8)
        self.lbl_stat_alimento = ctk.CTkLabel(self.card_alimento, text="0.00 Kg", text_color="#1B5E20", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_stat_alimento.pack(pady=(0,8))

        self.card_pesajes = ctk.CTkFrame(frame_cards, fg_color="#E1F5FE", corner_radius=10)
        self.card_pesajes.pack(side="left", padx=10, expand=True, fill="both")
        ctk.CTkLabel(self.card_pesajes, text="Peso Promedio General", text_color="#0288D1", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=8)
        self.lbl_stat_pesajes = ctk.CTkLabel(self.card_pesajes, text="0.00 Kg", text_color="#01579B", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_stat_pesajes.pack(pady=(0,8))

        # --- SUBMÓDULO: SECCIÓN GRÁFICA (ESTADÍSTICAS VISUALES) ---
        lbl_grafico_titulo = ctk.CTkLabel(self.vista_actual, text="📊 Análisis Comparativo del Negocio (Alimento vs Sanidad)", font=ctk.CTkFont(size=14, weight="bold"), text_color="#1E4620")
        lbl_grafico_titulo.pack(anchor="w", pady=(15, 5))

        self.canvas_grafico = ctk.CTkCanvas(self.vista_actual, height=180, bg="#F9F9F9", highlightthickness=1, highlightbackground="#E0E0E0")
        self.canvas_grafico.pack(fill="x", padx=10, pady=5)

        # --- SUBMÓDULO: ACCIONES Y EXPORTACIÓN ---
        frame_acciones = ctk.CTkFrame(self.vista_actual, fg_color="transparent")
        frame_acciones.pack(pady=15)

        self.btn_refresh_stats = ctk.CTkButton(frame_acciones, text="🔄 Recargar Métricas", fg_color="#1E4620", hover_color="#143016", width=150, command=self.calcular_reportes_db)
        self.btn_refresh_stats.grid(row=0, column=0, padx=8)

        self.btn_exportar_excel = ctk.CTkButton(frame_acciones, text="📊 Exportar a Excel", fg_color="#2E7D32", hover_color="#1B5E20", width=150, command=self.exportar_reporte_csv)
        self.btn_exportar_excel.grid(row=0, column=1, padx=8)

        self.btn_exportar_pdf = ctk.CTkButton(frame_acciones, text="📄 Generar Reporte PDF", fg_color="#C62828", hover_color="#B71C1C", width=150, command=self.exportar_reporte_pdf)
        self.btn_exportar_pdf.grid(row=0, column=2, padx=8)

        self.calcular_reportes_db()

    def calcular_reportes_db(self):
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT COUNT(*) FROM sanidad")
                total_sani = cursor.fetchone()[0] or 0
                self.lbl_stat_sanidad.configure(text=f"{total_sani} Registros")
                
                cursor.execute("SELECT SUM(cantidad_kg) FROM alimentacion")
                total_alim = cursor.fetchone()[0]
                total_alim_val = float(total_alim) if total_alim else 0.0
                self.lbl_stat_alimento.configure(text=f"{total_alim_val:.2f} Kg")
                
                cursor.execute("SELECT AVG(peso_kg) FROM pesajes")
                avg_peso = cursor.fetchone()[0]
                avg_peso_val = float(avg_peso) if avg_peso else 0.0
                self.lbl_stat_pesajes.configure(text=f"{avg_peso_val:.2f} Kg")
                
                self.dibujar_graficos_finca(total_alim_val, total_sani)
                
            except Exception as e:
                print(f"❌ Error al compilar métricas: {e}")
            finally:
                cursor.close()
                conn.close()

    def dibujar_graficos_finca(self, alimento, sanidad):
        self.canvas_grafico.delete("all")
        max_alimento = max(alimento, 10.0)
        max_sanidad = max(sanidad, 5)
        
        alto_barra_alim = int((alimento / max_alimento) * 110)
        alto_barra_sani = int((sanidad / max_sanidad) * 110)
        
        # Barra de Alimentación
        self.canvas_grafico.create_rectangle(150, 140 - alto_barra_alim, 250, 140, fill="#4CAF50", outline="#2E7D32", width=1)
        self.canvas_grafico.create_text(200, 155, text=f"Alimento: {alimento:.1f} Kg", font=("Arial", 10, "bold"), fill="#333333")
        
        # Barra de Control Médico
        self.canvas_grafico.create_rectangle(380, 140 - alto_barra_sani, 480, 140, fill="#FF9800", outline="#E65100", width=1)
        self.canvas_grafico.create_text(430, 155, text=f"Sanidad: {sanidad} Reg.", font=("Arial", 10, "bold"), fill="#333333")
        
        self.canvas_grafico.create_line(50, 140, 600, 140, fill="#999999", width=2)

    def exportar_reporte_csv(self):
        import csv
        from tkinter import filedialog
        
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("Archivos de Excel / CSV", "*.csv")],
            title="Guardar Reporte Excel", initialfile="Reporte_Estadistico_Finca.csv"
        )
        if not ruta_archivo: return

        conn = obtener_conexion()
        if not conn: return
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM sanidad")
            t_sani = cursor.fetchone()[0] or 0
            cursor.execute("SELECT SUM(cantidad_kg) FROM alimentacion")
            t_alim = float(cursor.fetchone()[0] or 0.0)
            cursor.execute("SELECT AVG(peso_kg) FROM pesajes")
            a_peso = float(cursor.fetchone()[0] or 0.0)

            with open(ruta_archivo, mode='w', newline='', encoding='utf-8-sig') as archivo:
                escritor = csv.writer(archivo, delimiter=';')
                
                escritor.writerow(["FINCA EL PUENTE - REPORTE DE METRICAS Y ESTADÍSTICAS"])
                escritor.writerow(["Indicador", "Valor Actual", "Representación Gráfica (Barras)"])
                escritor.writerow(["Total Alimento Suministrado", f"{t_alim:.2f} Kg", "█" * min(int(t_alim), 30)])
                escritor.writerow(["Controles Sanitarios", f"{t_sani} Reg.", "█" * min(t_sani * 2, 30)])
                escritor.writerow(["Peso Promedio General", f"{a_peso:.2f} Kg", "█" * min(int(a_peso / 20), 30)])
                escritor.writerow([])
                
                escritor.writerow(["--- INVENTARIO DE GANADO BRAHMAN ---"])
                escritor.writerow(["Código", "Nombre", "Raza", "Sexo", "F. Nacimiento", "Peso Inicial (Kg)", "Estado"])
                cursor.execute("SELECT codigo, nombre, raza, sexo, fecha_nacimiento, peso_inicial, estado FROM ganado")
                for fila in cursor.fetchall():
                    escritor.writerow([fila[0], fila[1], fila[2], fila[3], fila[4], f"{fila[5]:.2f}", fila[6]])
                    
            messagebox.showinfo("Reporte Completo", "🎉 ¡Reporte Excel con estadísticas numéricas generado exitosamente!")
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al guardar: {e}")
        finally:
            cursor.close()
            conn.close()

    def exportar_reporte_pdf(self):
        from tkinter import filedialog
        import webbrowser
        import os
        import datetime
        
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("Reporte Web Imprimible (PDF)", "*.html")],
            title="Generar Reporte Ejecutivo Oficial",
            initialfile="Reporte_Finca_El_Puente.html"
        )
        if not ruta_archivo: return

        conn = obtener_conexion()
        if not conn: return
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

            max_val = max(t_alim, t_sani * 10, 1)
            w_alim = (t_alim / max_val) * 100
            w_sani = ((t_sani * 10) / max_val) * 100

            with open(ruta_archivo, mode='w', encoding='utf-8') as html:
                html.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>Reporte Finca El Puente</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #333; }}
        .header {{ text-align: center; border-bottom: 3px solid #1E4620; padding-bottom: 10px; }}
        .meta {{ text-align: right; font-size: 12px; color: #666; margin-top: 5px; }}
        h2 {{ color: #1E4620; margin-top: 30px; }}
        .metricas {{ display: flex; justify-content: space-between; margin: 20px 0; }}
        .card {{ background: #f4fdf4; border: 1px solid #c8e6c9; padding: 15px; border-radius: 8px; width: 22%; text-align: center; }}
        .card h3 {{ margin: 0; font-size: 14px; color: #2e7d32; }}
        .card p {{ font-size: 20px; font-weight: bold; margin: 10px 0 0 0; color: #1b5e20; }}
        .chart-container {{ background: #f9f9f9; border: 1px solid #e0e0e0; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .bar-group {{ margin-bottom: 15px; }}
        .bar-label {{ font-weight: bold; font-size: 13px; margin-bottom: 5px; }}
        .bar-bg {{ background: #e0e0e0; border-radius: 4px; width: 100%; height: 25px; }}
        .bar-fill-alim {{ background: #4CAF50; height: 100%; border-radius: 4px; width: {w_alim}%; }}
        .bar-fill-sani {{ background: #FF9800; height: 100%; border-radius: 4px; width: {w_sani}%; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #1E4620; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class='header'>
        <h1>REPORTE OPERATIVO OFICIAL</h1>
        <h3>SISTEMA DE GESTIÓN GANADERA - FINCA EL PUENTE</h3>
        <div class='meta'>Generado el: {datetime.date.today().strftime('%d/%m/%Y')}</div>
    </div>

    <h2>1. Resumen de Estadísticas</h2>
    <div class='metricas'>
        <div class='card'><h3>Ganado Registrado</h3><p>{t_gana} Cabezas</p></div>
        <div class='card'><h3>Sanidad Aplicada</h3><p>{t_sani} Reg.</p></div>
        <div class='card'><h3>Alimento Total</h3><p>{t_alim:.2f} Kg</p></div>
        <div class='card'><h3>Peso Promedio</h3><p>{a_peso:.2f} Kg</p></div>
    </div>

    <h2>2. Gráficos Comparativos de Rendimiento</h2>
    <div class='chart-container'>
        <div class='bar-group'>
            <div class='bar-label'>Distribución de Alimentación ({t_alim:.2f} Kg Suministrados)</div>
            <div class='bar-bg'><div class='bar-fill-alim'></div></div>
        </div>
        <div class='bar-group'>
            <div class='bar-label'>Densidad de Controles Sanitarios ({t_sani} Eventos Médicos)</div>
            <div class='bar-bg'><div class='bar-fill-sani'></div></div>
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
        <tbody>""")
                
                cursor.execute("SELECT codigo, nombre, raza, sexo, estado FROM ganado")
                for fila in cursor.fetchall():
                    html.write(f"""
            <tr>
                <td>{fila[0]}</td>
                <td>{fila[1]}</td>
                <td>{fila[2]}</td>
                <td>{fila[3]}</td>
                <td><span style='font-weight:bold;'>{fila[4]}</span></td>
            </tr>""")
                    
                html.write("""
        </tbody>
    </table>
</body>
</html>""")
                
            messagebox.showinfo("Reporte Generado", "📄 ¡El Reporte Ejecutivo se ha estructurado con éxito! Se abrirá en tu navegador donde podrás guardarlo o imprimirlo directamente como un PDF limpio.")
            webbrowser.open(f"file://{os.path.abspath(ruta_archivo)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo compilar el reporte visual: {e}")
        finally:
            cursor.close()
            conn.close()


# =================================================================
# 🤖 CLASE EXTRA: VENTANA CONVERSACIONAL DEL CHATBOT CON IA
# =================================================================
class ChatbotWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Asistente Virtual IA — Finca El Puente")
        self.geometry("480x620")
        self.configure(fg_color="#F4F6F4")
        self.resizable(False, False)
        
        # Mantener siempre al frente
        self.attributes("-topmost", True)
        
        # --- CABECERA DEL CHATBOT ---
        self.header = ctk.CTkFrame(self, fg_color="#1E4620", height=60, corner_radius=0)
        self.header.pack(fill="x", side="top")
        
        self.lbl_titulo_chat = ctk.CTkLabel(
            self.header, text="🤖 Asistente Virtual Ganadero", text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold")
        )
        self.lbl_titulo_chat.pack(pady=8, padx=15, side="left")
        
        self.lbl_estado = ctk.CTkLabel(
            self.header, text="● Conectado a SQL Server", text_color="#81C784",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold")
        )
        self.lbl_estado.pack(pady=12, padx=15, side="right")
        
        # --- ÁREA DE MENSAJES (SCROLLABLE) ---
        self.historial_mensajes = ctk.CTkScrollableFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E0E0E0")
        self.historial_mensajes.pack(fill="both", expand=True, padx=15, pady=15)
        
        # --- BARRA DE ENTRADA DE TEXTO ---
        self.frame_entrada = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_entrada.pack(fill="x", side="bottom", padx=15, pady=(0, 15))
        
        self.ent_consulta = ctk.CTkEntry(
            self.frame_entrada, placeholder_text="Pregunta por un animal, peso o vacuna (Ej: Hércules)...",
            fg_color="white", border_color="#B0BEC5", height=40, font=ctk.CTkFont(family="Helvetica", size=12)
        )
        self.ent_consulta.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.ent_consulta.bind("<Return>", lambda event: self.enviar_consulta())
        
        self.btn_enviar = ctk.CTkButton(
            self.frame_entrada, text="Consultar 🚀", fg_color="#2E7D32", hover_color="#1B5E20",
            width=90, height=40, font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            command=self.enviar_consulta
        )
        self.btn_enviar.pack(side="right")
        
        # Mensaje de bienvenida inicial de la IA
        self.agregar_burbuja_texto(
            "¡Hola! Soy tu Asistente Inteligente de Finca El Puente. ¿En qué puedo ayudarte hoy?\n\n"
            "💡 Sugerencias:\n"
            "• ¿Cómo está el animal Hércules?\n"
            "• Dame las estadísticas generales de la finca.\n"
            "• ¿Qué vacunas se han aplicado hoy?\n"
            "• Dame un consejo para alimentar ganado.",
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
            
        burbuja = ctk.CTkFrame(contenedor, fg_color=color_fondo, corner_radius=12)
        burbuja.pack(side=lado_alineado, padx=10, ipady=6, ipadx=10)
        
        lbl = ctk.CTkLabel(
            burbuja, text=texto, text_color=color_texto, wraplength=310, justify="left",
            font=ctk.CTkFont(family="Helvetica", size=12)
        )
        lbl.pack()
        
        self.historial_mensajes._parent_canvas.yview_moveto(1.0)

    def procesar_ia_ganadera(self, consulta):
        consulta_min = consulta.lower()
        
        conn = obtener_conexion()
        if not conn:
            self.agregar_burbuja_texto("⚠️ Error de Red: No logré conectar con la base de datos SQL Server.", es_asistente=True)
            return
            
        cursor = conn.cursor()
        try:
            # CASO A: ESTADÍSTICAS GENERALES DE LA FINCA
            if any(x in consulta_min for x in ["estadística", "general", "finca", "resumen", "total", "indicador", "promedio"]):
                cursor.execute("SELECT COUNT(*) FROM ganado")
                total_ganado = cursor.fetchone()[0] or 0
                
                cursor.execute("SELECT SUM(cantidad_kg) FROM alimentacion")
                total_alimento = float(cursor.fetchone()[0] or 0.0)
                
                cursor.execute("SELECT AVG(peso_kg) FROM pesajes")
                peso_promedio = float(cursor.fetchone()[0] or 0.0)
                
                respuesta = (
                    f"📊 *Reporte Estadístico Automatizado (IA)*\n\n"
                    f"Actualmente en la Finca El Puente tenemos registrados:\n"
                    f"• {total_ganado} cabezas de ganado en inventario.\n"
                    f"• {total_alimento:.2f} Kg de alimento suministrado acumulado.\n"
                    f"• Peso promedio general de pesajes: {peso_promedio:.2f} Kg.\n\n"
                    f"¿Te gustaría que indague sobre el historial clínico de algún ejemplar en específico?"
                )
                self.agregar_burbuja_texto(respuesta, es_asistente=True)
                return

            # CASO B: DETECTAR CONSULTA DE ANIMAL ESPECÍFICO (Nombre o Código)
            palabras = consulta.split()
            ejemplar_encontrado = None
            
            for palabra in palabras:
                palabra_limpia = palabra.replace("?", "").replace(",", "").replace(".", "").strip()
                cursor.execute(
                    "SELECT codigo, nombre, raza, sexo, peso_inicial, estado, observaciones FROM ganado WHERE codigo = ? OR nombre LIKE ?",
                    (palabra_limpia, f"%{palabra_limpia}%")
                )
                fila = cursor.fetchone()
                if fila:
                    ejemplar_encontrado = fila
                    break
                    
            if ejemplar_encontrado:
                cod, nom, raz, sex, peso_i, est, obs = ejemplar_encontrado
                obs = obs or "Sin notas clínicas adicionales en el expediente."
                
                cursor.execute("SELECT COUNT(*) FROM sanidad WHERE codigo_animal = ?", (cod,))
                cont_sani = cursor.fetchone()[0] or 0
                
                cursor.execute("SELECT SUM(cantidad_kg) FROM alimentacion WHERE codigo_animal = ?", (cod,))
                cont_alim = float(cursor.fetchone()[0] or 0.0)
                
                respuesta = (
                    f"🐄 *Hoja de Datos Inteligente — {nom}* ({cod})\n\n"
                    f"• Raza registrada: {raz} — Sexo: {sex}\n"
                    f"• Estado Operativo: {est}\n"
                    f"• Peso al ingresar: {peso_i:.2f} Kg\n"
                    f"• Controles Médicos: {cont_sani} registros aplicados.\n"
                    f"• Ración Alimentaria total: {cont_alim:.2f} Kg.\n"
                    f"• Notas de campo: {obs}\n\n"
                    f"Los datos proceden directamente de las tablas relacionales de la base de datos."
                )
                self.agregar_burbuja_texto(respuesta, es_asistente=True)
                return

            # CASO C: RECOMENDACIONES DE SALUD / VACUNAS
            if any(x in consulta_min for x in ["vacuna", "enfermo", "sanidad", "tratamiento", "médico", "salud", "inyección"]):
                cursor.execute("SELECT COUNT(*) FROM sanidad")
                total_tratamientos = cursor.fetchone()[0] or 0
                respuesta = (
                    f"💉 *Asistencia Clínica Veterinaria*\n\n"
                    f"El sistema registra un total de {total_tratamientos} tratamientos aplicados en finca.\n"
                    f"Recuerde que para la cría de ganado Brahman en Chiriquí, se sugiere vacunar contra Rabia Paralítica y el carbón bacteridiano al menos una vez al año.\n\n"
                    f"¿Desea consultar el historial de algún animal específico? Escriba su nombre."
                )
                self.agregar_burbuja_texto(respuesta, es_asistente=True)
                return

            # CASO D: CONSEJOS GENERALES DE GANADERÍA (AGRO-IA)
            if any(x in consulta_min for x in ["consejo", "brahman", "pasto", "alimentar", "silo", "melaza", "calor"]):
                respuesta = (
                    f"🌾 *Recomendación Agrícola de la IA*\n\n"
                    f"• *Manejo del Calor:* El ganado Brahman tolera bien el sol, pero es vital tener árboles de sombra y agua fresca disponible.\n"
                    f"• *Dieta Balanceada:* Complemente el pastoreo directo con mezclas de melaza y sales minerales en épocas secas para proteger el peso corporal.\n"
                    f"• *Registro:* Mantener el pesaje al día es la única forma confiable de medir si el ganado está asimilando bien el alimento."
                )
                self.agregar_burbuja_texto(respuesta, es_asistente=True)
                return

            # CASO E: SALUDO
            if any(x in consulta_min for x in ["hola", "buen", "saludo", "tal", "asistente", "hey"]):
                self.agregar_burbuja_texto("¡Hola! Un placer saludarte. Estoy listo para procesar tus consultas relacionales sobre la Finca El Puente. ¿Qué animal deseas buscar hoy?", es_asistente=True)
                return

            # CASO F: RESPUESTA DE FALLBACK
            respuesta_fallback = (
                f"Entiendo tu consulta sobre '{consulta}'. Como tu asistente IA de Finca El Puente, "
                f"te comento que actualmente no tengo cargada información explícita sobre ese término. "
                f"Intenta escribiendo el nombre de algún ejemplar registrado (como 'Hércules') "
                f"o solicita estadísticas generales."
            )
            self.agregar_burbuja_texto(respuesta_fallback, es_asistente=True)

        except Exception as e:
            self.agregar_burbuja_texto(f"❌ Error al consultar la IA: {e}", es_asistente=True)
        finally:
            cursor.close()
            conn.close()