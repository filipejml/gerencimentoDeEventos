from .db_connection import get_connection

def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            data DATE NOT NULL, 
            local VARCHAR(100) NOT NULL,
            empresa VARCHAR(100)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            empresa VARCHAR(100) NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS palestras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evento_id INTEGER NOT NULL,
            sala_id INTEGER,
            titulo VARCHAR(100) NOT NULL,
            palestrante VARCHAR(100) NOT NULL,
            horario DATE NOT NULL,
            FOREIGN KEY (evento_id) REFERENCES eventos (id),
            FOREIGN KEY (sala_id) REFERENCES salas (id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS salas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            capacidade INTEGER NOT NULL,
            empresa VARCHAR(100)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS participante_evento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evento_id INTEGER NOT NULL,
            participante_id INTEGER NOT NULL,
            FOREIGN KEY (evento_id) REFERENCES eventos (id),
            FOREIGN KEY (participante_id) REFERENCES participantes (id)
        )
        ''')

        conn.commit()
