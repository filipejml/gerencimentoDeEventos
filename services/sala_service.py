from database.queries import execute_query, fetch_all

def inserir_sala(nome, capacidade, empresa):
    return execute_query(
        'INSERT INTO salas (nome, capacidade, empresa) VALUES (?, ?, ?)',
        (nome, capacidade, empresa)
    )

def recuperar_salas():
    return fetch_all('SELECT * FROM salas')
    
def recuperar_salas_por_horario(horario):
    return fetch_all(
        '''
        SELECT salas.id, salas.nome, salas.capacidade, salas.empresa
        FROM salas
        LEFT JOIN palestras ON salas.id = palestras.sala_id AND palestras.horario = ?
        WHERE palestras.id IS NULL
        ''',
        (horario,)
    )

def recuperar_salas_disponiveis_para_evento(evento_id):
    return fetch_all(
        '''
        SELECT id, nome, capacidade, empresa
        FROM salas
        WHERE id NOT IN (
            SELECT sala_id FROM palestras WHERE evento_id = ?
        )
        ''',
        (evento_id,)
    )