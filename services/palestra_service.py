from database.queries import execute_query, fetch_all

def inserir_palestra(evento_id, sala_id, titulo, palestrante, horario):
    return execute_query(
        'INSERT INTO palestras (evento_id, sala_id, titulo, palestrante, horario) VALUES (?, ?, ?, ?, ?)',
        (evento_id, sala_id, titulo, palestrante, horario)
    )

def recuperar_palestras_por_evento(evento_id):
    return fetch_all(
        '''
        SELECT palestras.id, salas.nome AS nome_sala, palestras.titulo, palestras.palestrante, palestras.horario
        FROM palestras
        JOIN salas ON palestras.sala_id = salas.id
        WHERE palestras.evento_id = ?
        ''',
        (evento_id,)
    )



def recuperar_palestras_por_palestrante(palestrante):
    return fetch_all(
        'SELECT * FROM palestras WHERE palestrante = ?',
        (palestrante,)
    )

def recuperar_palestrantes():
    return fetch_all(
        'SELECT DISTINCT palestrante FROM palestras'
    )

def recuperar_nomes_palestrantes():
    # Recupera apenas os nomes dos palestrantes
    palestras = fetch_all('SELECT DISTINCT palestrante FROM palestras')
    nomes_palestrantes = [palestra[0] for palestra in palestras]  # Extrai os nomes dos palestrantes
    return nomes_palestrantes