from database.queries import execute_query, fetch_all

def inserir_participante_banco_de_dados(nome, email, empresa):
    return execute_query(
        'INSERT INTO participantes (nome, email, empresa) VALUES (?, ?, ?)',
        (nome, email, empresa)
    )

def recuperar_participantes():
    return fetch_all('SELECT * FROM participantes')

def recuperar_participantes_por_evento(evento_id):
    return fetch_all(
        '''
        SELECT participantes.id, participantes.nome, participantes.email, participantes.empresa
        FROM participantes
        JOIN participante_evento ON participantes.id = participante_evento.participante_id
        WHERE participante_evento.evento_id = ?
        ''',
        (evento_id,)
    )
