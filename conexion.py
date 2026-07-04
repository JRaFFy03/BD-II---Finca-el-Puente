import pyodbc

def obtener_conexion():
    """
    Establece y retorna la conexión con la base de datos SQL Server.
    """
    # CONFIGURA TU SERVIDOR AQUÍ:
    # Si entras a SSMS con un punto (.) o con 'localhost', déjalo así.
    # Si tu servidor tiene un nombre con barra (ej. LAPTOP-123\SQLEXPRESS), ponlo aquí usando doble barra: 'LAPTOP-123\\SQLEXPRESS'
    nombre_servidor = 'localhost' 
    nombre_bd = 'FincaElPuente'
    
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={nombre_servidor};"
        f"DATABASE={nombre_bd};"
        f"Trusted_Connection=yes;"
    )
    
    try:
        conexion = pyodbc.connect(connection_string)
        return conexion
    except Exception as e:
        print(f"❌ Error crítico al conectar a SQL Server: {e}")
        return None