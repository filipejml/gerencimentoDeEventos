
from database.queries import execute_query, fetch_all

def inserir_evento(nome, data, local, empresa):
    return execute_query(
        'INSERT INTO eventos (nome, data, local, empresa) VALUES (?, ?, ?, ?)',
        (nome, data, local, empresa)
    )

def recuperar_eventos():
    return fetch_all('SELECT id, nome, data, local, empresa FROM eventos')

def recuperar_eventos_por_empresa(empresa):
    return fetch_all('SELECT id, nome, data, local FROM eventos WHERE empresa = ?', (empresa,))

def recuperar_salas_disponiveis_para_evento(evento_id):
    return fetch_all('SELECT id, nome, capacidade, empresa FROM salas WHERE id NOT IN (SELECT sala_id FROM palestras WHERE evento_id = ?)', (evento_id,))

def recuperar_empresas():
    return fetch_all('SELECT DISTINCT empresa FROM eventos')
