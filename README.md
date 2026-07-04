# Finca El Puente — Sistema Inteligente de Gestión Ganadera

Este proyecto es una aplicación de escritorio diseñada para automatizar y optimizar el control de inventario, salud, alimentación y pesaje del ganado en la Finca El Puente. Desarrollado como proyecto final para la asignatura de **Base de Datos II**.

## 🚀 Características Principales
- **Dashboard en Tiempo Real:** Muestra indicadores clave como el total de cabezas de ganado registradas.
- **Módulos Completos:** Gestión de Ganado, Control Sanitario (Vacunas/Tratamientos), Historial de Alimentación y Control de Pesajes.
- **Base de Datos Robusta:** Conexión directa a SQL Server con validaciones de integridad referencial.
- **Interfaz Moderna:** Diseñada con componentes personalizados y un entorno visual limpio.

---

## 🛠️ Requisitos e Instalación

### 1. Clonar o Descargar el Proyecto
Asegúrese de tener todos los archivos en su directorio local:
- `main.py` (Punto de entrada de la aplicación)
- `gui.py` (Componentes de la interfaz gráfica)
- `conexion.py` (Módulo de conexión a la base de Datos)
- `script.sql` (Script de la Base de Datos)

### 2. Instalar Dependencias de Python
Abra la terminal en la ruta del proyecto y ejecute los siguientes comandos para instalar las librerías necesarias:
```bash
pip install customtkinter pyodbc