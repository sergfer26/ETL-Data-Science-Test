import sqlite3


def create_schema():
    """Create the database schema."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Tabla visitor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitor (
            email TEXT PRIMARY KEY,
            fechaPrimeraVisita DATE,
            fechaUltimaVisita DATE,
            visitasTotales INTEGER DEFAULT 0,
            visitasAnioActual INTEGER DEFAULT 0,
            visitasMesActual INTEGER DEFAULT 0,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla statistics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            jyv TEXT,
            Badmail TEXT,
            Baja TEXT,
            fecha_envio DATETIME,
            fecha_open DATETIME,
            Opens INTEGER DEFAULT 0,
            Opens_virales INTEGER DEFAULT 0,
            fecha_click DATETIME,
            Clicks INTEGER DEFAULT 0,
            Clicks_virales INTEGER DEFAULT 0,
            Links TEXT,
            IPs TEXT,
            Navegadores TEXT,
            Plataformas TEXT,
            fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            archivo_origen TEXT
        )
    ''')
    
    # Tabla errors
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            archivo TEXT,
            linea INTEGER,
            registro TEXT,
            error_descripcion TEXT,
            fecha_error TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de control ETL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS etl_control (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            archivo TEXT UNIQUE,
            fecha_descarga DATETIME,
            fecha_procesamiento DATETIME,
            registros_totales INTEGER,
            registros_exitosos INTEGER,
            registros_error INTEGER,
            estado TEXT,
            hash_archivo TEXT
        )
    ''')
    
    conn.commit()
    conn.close()