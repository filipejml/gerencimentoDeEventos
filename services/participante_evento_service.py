from database.queries import execute_query, fetch_all

def associar_participante_evento(evento_id, participante_id):
    execute_query(
        'INSERT INTO participante_evento (evento_id, participante_id) VALUES (?, ?)',
        (evento_id, participante_id)
    )

def recuperar_participantes_por_evento(evento_id):
    return fetch_all(
        'SELECT p.id, p.nome, p.email, p.empresa FROM participantes p '
        'INNER JOIN participante_evento pe ON p.id = pe.participante_id '
        'WHERE pe.evento_id = ?',
        (evento_id,)
    )
