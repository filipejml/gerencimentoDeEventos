import tkinter as tk
from tkinter import ttk, messagebox  

import services
import datetime
from datetime import datetime
from services.palestra_service import inserir_palestra as inserir_palestra_banco_de_dados
from services.evento_service import inserir_evento, recuperar_eventos, recuperar_salas_disponiveis_para_evento, recuperar_empresas, recuperar_eventos_por_empresa
from services.participante_service import inserir_participante_banco_de_dados, recuperar_participantes, recuperar_participantes_por_evento
from services.palestra_service import inserir_palestra, recuperar_palestras_por_evento, recuperar_palestras_por_palestrante, recuperar_palestrantes, recuperar_nomes_palestrantes
from services.sala_service import inserir_sala, recuperar_salas_por_horario, recuperar_salas
from services.participante_evento_service import associar_participante_evento

palestra_window = None

def main():
    root = tk.Tk()
    root.title("Sistema de Gerenciamento de Eventos")

    def inserir_evento():
        # Cria uma janela para inserir os detalhes do evento
        global nome_entry, data_entry, local_entry, empresa_entry, evento_window
        evento_window = tk.Toplevel(root)
        evento_window.title("Inserir Evento")

        # Função para mostrar os eventos cadastrados
        def mostrar_eventos_cadastrados():
            eventos_cadastrados = recuperar_eventos()
            if eventos_cadastrados:
                # Cria uma nova janela para mostrar os eventos
                eventos_window = tk.Toplevel(root)
                eventos_window.title("Eventos Cadastrados")

                # Cria uma Treeview para exibir os eventos
                tree = ttk.Treeview(eventos_window, columns=("ID", "Nome", "Data", "Local", "Empresa"), show="headings")
                tree.heading("ID", text="ID")
                tree.heading("Nome", text="Nome")
                tree.heading("Data", text="Data")
                tree.heading("Local", text="Local")
                tree.heading("Empresa", text="Empresa")

                # Preenche a Treeview com os eventos cadastrados
                for evento in eventos_cadastrados:
                    # Formata a data para dd-mm-aaaa
                    evento_id, nome, data, local, empresa = evento
                    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')
                    tree.insert("", tk.END, values=(evento_id, nome, data_formatada, local, empresa))

                tree.pack(expand=True, fill=tk.BOTH)

                # Adiciona um botão "OK" para fechar a janela
                tk.Button(eventos_window, text="OK", command=eventos_window.destroy).pack(pady=10)
            else:
                messagebox.showinfo("Info", "Nenhum evento cadastrado.")

        # Criação de rótulos e campos de entrada para os detalhes do evento
        # Rótulo e campo de entrada para Nome do Evento
        tk.Label(evento_window, text="Nome do Evento:").grid(row=0, column=0, padx=5, pady=5)
        nome_entry = tk.Entry(evento_window)
        nome_entry.grid(row=0, column=1, padx=5, pady=5)

        # Rótulo e campo de entrada para Data do Evento
        tk.Label(evento_window, text="Data do Evento (DD-MM-AAAA):").grid(row=1, column=0, padx=5, pady=5)
        data_entry = tk.Entry(evento_window)
        data_entry.grid(row=1, column=1, padx=5, pady=5)

        # Rótulo e campo de entrada para Local do Evento
        tk.Label(evento_window, text="Local do Evento:").grid(row=2, column=0, padx=5, pady=5)
        local_entry = tk.Entry(evento_window)
        local_entry.grid(row=2, column=1, padx=5, pady=5)

        # Rótulo e campo de entrada para Nome da Empresa Organizadora
        tk.Label(evento_window, text="Nome da Empresa Organizadora:").grid(row=3, column=0, padx=5, pady=5)
        empresa_entry = tk.Entry(evento_window)
        empresa_entry.grid(row=3, column=1, padx=5, pady=5)

        # Frame para conter os botões
        button_frame = tk.Frame(evento_window)
        button_frame.grid(row=4, columnspan=2, pady=10)  

        # Botão para mostrar os eventos cadastrados
        tk.Button(button_frame, text="Eventos Cadastrados", command=mostrar_eventos_cadastrados).pack(side=tk.LEFT, padx=5)

        # Botão para salvar o evento
        tk.Button(button_frame, text="Salvar", command=salvar_evento).pack(side=tk.LEFT, padx=5)

    def salvar_evento():
        nome = nome_entry.get()
        data = data_entry.get()
        local = local_entry.get()
        empresa = empresa_entry.get()

        # Validação da data
        try:
            data_formatada = datetime.strptime(data, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Por favor, insira a data no formato DD-MM-AAAA.")
            return

        id_evento = services.evento_service.inserir_evento(nome, data_formatada, local, empresa)
        messagebox.showinfo("Sucesso", f"Evento inserido com ID: {id_evento}")
        evento_window.destroy()

    def inserir_participante():
        global participante_window
        # Cria uma nova janela para inserir os detalhes do participante
        participante_window = tk.Toplevel(root)
        participante_window.title("Inserir Participante")

        # Função para salvar o participante
        def salvar_participante():
            # Obtém os valores dos campos de entrada
            nome = nome_entry.get()
            email = email_entry.get()
            empresa = empresa_entry.get()
            evento_id = evento_var.get().split(':')[0]  # Obtém o ID do evento selecionado

            # Insere o participante no banco de dados
            id_participante = inserir_participante_banco_de_dados(nome, email, empresa)  # Renomeado para evitar conflito
            # Associa o participante ao evento
            associar_participante_evento(evento_id, id_participante)

            messagebox.showinfo("Sucesso", f"Participante inserido com ID: {id_participante} e associado ao evento {evento_id}")
            participante_window.destroy()  # Fecha a janela após salvar o participante

        # Rótulo e campo de entrada para Nome do Participante
        tk.Label(participante_window, text="Nome do Participante:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        nome_entry = tk.Entry(participante_window)
        nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Rótulo e campo de entrada para Email do Participante
        tk.Label(participante_window, text="Email do Participante:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        email_entry = tk.Entry(participante_window)
        email_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Rótulo e campo de entrada para Empresa do Participante
        tk.Label(participante_window, text="Empresa do Participante:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        empresa_entry = tk.Entry(participante_window)
        empresa_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Menu suspenso para selecionar o evento
        tk.Label(participante_window, text="Selecione o Evento:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        evento_var = tk.StringVar()
        eventos = recuperar_eventos()
        evento_combobox = ttk.Combobox(participante_window, textvariable=evento_var)
        evento_combobox['values'] = [f"{evento[0]}: {evento[1]}" for evento in eventos]
        evento_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Botão para salvar o participante
        tk.Button(participante_window, text="Salvar", command=salvar_participante).grid(row=4, columnspan=2, pady=10)

    def inserir_palestra():
        global palestra_window
        # Cria uma nova janela para inserir os detalhes da palestra
        palestra_window = tk.Toplevel(root)
        palestra_window.title("Inserir Palestra")

        # Função para salvar a palestra
        def salvar_nova_palestra():
            evento_id = evento_var.get().split(':')[0]  # Obtém o ID do evento selecionado
            sala_id = sala_var.get().split(':')[0]  # Obtém o ID da sala selecionada
            titulo = titulo_entry.get()
            palestrante = palestrante_entry.get()
            horario = horario_entry.get()

            # Verifique se os campos obrigatórios estão preenchidos
            if not (evento_id and sala_id and titulo and palestrante and horario):
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return

            # Insira a palestra no banco de dados
            id_palestra = inserir_palestra_banco_de_dados(evento_id, sala_id, titulo, palestrante, horario)
            messagebox.showinfo("Sucesso", f"Palestra inserida com ID: {id_palestra}")
            palestra_window.destroy()  # Fecha a janela após salvar a palestra

        # Rótulo e campo de entrada para selecionar o Evento
        tk.Label(palestra_window, text="Selecione o Evento:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        evento_var = tk.StringVar()
        eventos = recuperar_eventos()
        evento_combobox = ttk.Combobox(palestra_window, textvariable=evento_var)
        evento_combobox['values'] = [f"{evento[0]}: {evento[1]}" for evento in eventos]
        evento_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Rótulo e campo de entrada para selecionar a Sala
        tk.Label(palestra_window, text="Selecione a Sala:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        sala_var = tk.StringVar()
        salas = recuperar_salas()
        sala_combobox = ttk.Combobox(palestra_window, textvariable=sala_var)
        sala_combobox['values'] = [f"{sala[0]}: {sala[1]}" for sala in salas]
        sala_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Rótulo e campo de entrada para Título da Palestra
        tk.Label(palestra_window, text="Título da Palestra:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        titulo_entry = tk.Entry(palestra_window)
        titulo_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Rótulo e campo de entrada para Nome do Palestrante
        tk.Label(palestra_window, text="Nome do Palestrante:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        palestrante_entry = tk.Entry(palestra_window)
        palestrante_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Rótulo e campo de entrada para Horário da Palestra
        tk.Label(palestra_window, text="Horário da Palestra (HH:MM):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        horario_entry = tk.Entry(palestra_window)
        horario_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Botão para salvar a palestra
        tk.Button(palestra_window, text="Salvar", command=salvar_nova_palestra).grid(row=5, columnspan=2, pady=10)

        
    def inserir_sala_gui():
        # Cria uma nova janela para inserir os detalhes da sala
        sala_window = tk.Toplevel(root)
        sala_window.title("Inserir Sala")

        # Função para salvar a sala
        def salvar_sala():
            # Obtém os valores dos campos de entrada
            nome_sala = nome_sala_entry.get()
            capacidade = capacidade_entry.get()
            empresa = empresa_entry.get()

            # Insere a sala no banco de dados
            id_sala = inserir_sala(nome_sala, capacidade, empresa)
            messagebox.showinfo("Sucesso", f"Sala inserida com ID: {id_sala}")
            sala_window.destroy()  # Fecha a janela após salvar a sala

        # Cria um Frame para agrupar os rótulos e campos de entrada
        frame = tk.Frame(sala_window)
        frame.pack(padx=10, pady=10)  # Adiciona espaçamento interno ao frame

        # Rótulos e campos de entrada dentro do Frame
        tk.Label(frame, text="Nome da Sala:").grid(row=0, column=0, sticky="e")
        nome_sala_entry = tk.Entry(frame)
        nome_sala_entry.grid(row=0, column=1)

        tk.Label(frame, text="Capacidade da Sala:").grid(row=1, column=0, sticky="e")
        capacidade_entry = tk.Entry(frame)
        capacidade_entry.grid(row=1, column=1)

        tk.Label(frame, text="Empresa Responsável pela Sala:").grid(row=2, column=0, sticky="e")
        empresa_entry = tk.Entry(frame)
        empresa_entry.grid(row=2, column=1)

        # Botão para visualizar as salas cadastradas
        def visualizar_salas_cadastradas():
            # Cria uma nova janela para exibir as salas cadastradas
            salas_window = tk.Toplevel(root)
            salas_window.title("Salas Cadastradas")

            # Cria uma tabela para exibir as salas
            table = ttk.Treeview(salas_window, columns=("Nome", "Capacidade", "Empresa"))
            table.heading("#0", text="ID")
            table.heading("Nome", text="Nome")
            table.heading("Capacidade", text="Capacidade")
            table.heading("Empresa", text="Empresa")

            # Recupera as salas cadastradas
            salas_cadastradas = recuperar_salas()
            
            # Preenche a tabela com as salas cadastradas
            for sala in salas_cadastradas:
                table.insert("", "end", text=sala[0], values=(sala[1], sala[2], sala[3]))

            # Define o layout da tabela
            table.pack(padx=10, pady=10)

            # Função para fechar a janela
            def fechar_janela():
                salas_window.destroy()

            # Botão OK para fechar a janela
            ok_button = tk.Button(salas_window, text="OK", command=fechar_janela)
            ok_button.pack(pady=10)

        # Botões para visualizar salas cadastradas e salvar a sala
        button_frame = tk.Frame(sala_window)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Visualizar Salas Cadastradas", command=visualizar_salas_cadastradas).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Salvar", command=salvar_sala).pack(side=tk.LEFT, padx=5)


    def listar_eventos():
        eventos = recuperar_eventos()

        eventos_window = tk.Toplevel()
        eventos_window.title("Lista de Eventos")

        # Criando a tabela
        tree = ttk.Treeview(eventos_window, columns=("ID", "Nome", "Data", "Local", "Empresa"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Data", text="Data")
        tree.heading("Local", text="Local")
        tree.heading("Empresa", text="Empresa")

        # Preenchendo a tabela com os eventos
        for evento in eventos:
            evento_id, nome, data, local, empresa = evento
            # Formata a data para dd-mm-aaaa
            data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')
            tree.insert("", tk.END, values=(evento_id, nome, data_formatada, local, empresa))

        tree.pack(expand=True, fill=tk.BOTH)

        # Adiciona um botão "OK" para fechar a janela
        tk.Button(eventos_window, text="OK", command=eventos_window.destroy).pack(pady=10)

    def listar_participantes_de_evento():
            # Função para solicitar o ID do evento e mostrar a lista de eventos
            def solicitar_id_evento():
                # Criar uma nova janela para solicitar o ID do evento
                evento_window = tk.Toplevel()
                evento_window.title("Digite o ID do Evento")

                # Frame para conter o Entry e o Button
                frame = tk.Frame(evento_window)
                frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

                # Label e Entry para digitar o ID do evento
                tk.Label(frame, text="ID do Evento:").grid(row=0, column=0, padx=(0, 5))
                evento_id_entry = tk.Entry(frame)
                evento_id_entry.grid(row=0, column=1)

                # Exibir a lista de eventos já cadastrados
                eventos = recuperar_eventos()
                tree = ttk.Treeview(evento_window, columns=("ID", "Nome", "Data", "Local", "Empresa"), show="headings")
                tree.heading("ID", text="ID")
                tree.heading("Nome", text="Nome")
                tree.heading("Data", text="Data")
                tree.heading("Local", text="Local")
                tree.heading("Empresa", text="Empresa")

                for i, evento in enumerate(eventos):
                    tree.insert("", "end", values=evento)

                tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

                # Função para recuperar e exibir os participantes do evento
                def recuperar_participantes():
                    evento_id = evento_id_entry.get()
                    participantes = recuperar_participantes_por_evento(evento_id)
                    if participantes:
                        # Exibir os participantes em uma nova janela
                        participantes_window = tk.Toplevel()
                        participantes_window.title("Participantes do Evento")

                        # Criar a tabela de participantes
                        participantes_tree = ttk.Treeview(participantes_window, columns=("ID", "Nome", "Email", "Empresa"), show="headings")
                        participantes_tree.heading("ID", text="ID")
                        participantes_tree.heading("Nome", text="Nome")
                        participantes_tree.heading("Email", text="Email")
                        participantes_tree.heading("Empresa", text="Empresa")

                        # Inserir os participantes na tabela
                        for participante in participantes:
                            participantes_tree.insert("", "end", values=participante)

                        participantes_tree.pack(expand=True, fill=tk.BOTH)

                        # Botão "OK" para fechar a janela
                        ok_button = tk.Button(participantes_window, text="OK", command=participantes_window.destroy)
                        ok_button.pack(pady=10)

                    else:
                        messagebox.showinfo("Info", "Nenhum participante encontrado para este evento.")
                    evento_window.destroy()

                # Botão para recuperar os participantes
                tk.Button(frame, text="Recuperar Participantes", command=recuperar_participantes).grid(row=1, column=1, columnspan=2, padx=(5, 0))

            solicitar_id_evento()  # Chamada para iniciar o processo de listagem de participantes

    def listar_palestras_por_evento():
        def solicitar_id_evento():
            evento_window = tk.Toplevel()
            evento_window.title("Escolha um Evento")

            tk.Label(evento_window, text="Escolha um Evento:").pack()
            
            eventos = recuperar_eventos()
            tree = ttk.Treeview(evento_window, columns=("ID", "Nome", "Data", "Local", "Empresa"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Nome", text="Nome")
            tree.heading("Data", text="Data")
            tree.heading("Local", text="Local")
            tree.heading("Empresa", text="Empresa")

            for evento in eventos:
                tree.insert("", tk.END, values=evento)

            tree.pack(expand=True, fill=tk.BOTH)

            def evento_selecionado(event):
                item = tree.selection()[0]
                evento_id = tree.item(item, "values")[0]
                recuperar_palestras(evento_id)

            tree.bind("<Double-1>", evento_selecionado)

        def recuperar_palestras(evento_id):
            palestras = recuperar_palestras_por_evento(evento_id)
            if palestras:
                palestras_window = tk.Toplevel()
                palestras_window.title("Palestras do Evento")

                tree = ttk.Treeview(palestras_window, columns=("ID", "Sala", "Título", "Palestrante", "Horário"), show="headings")
                tree.heading("ID", text="ID")
                tree.heading("Sala", text="Sala")
                tree.heading("Título", text="Título")
                tree.heading("Palestrante", text="Palestrante")
                tree.heading("Horário", text="Horário")

                for palestra in palestras:
                    tree.insert("", tk.END, values=palestra)

                tree.pack(expand=True, fill=tk.BOTH)
            else:
                messagebox.showinfo("Info", "Nenhuma palestra encontrada para este evento.")

        solicitar_id_evento()
        
    def listar_salas_disponiveis_para_horario():
        def solicitar_horario():
            horario_window = tk.Toplevel()
            horario_window.title("Digite o Horário")

            # Labels e Entries para Data e Horário
            data_label = tk.Label(horario_window, text="Data (dd-mm-aaaa):")
            data_label.pack(side='left', padx=5, pady=5)
            data_entry = tk.Entry(horario_window)
            data_entry.pack(side='left', padx=5, pady=5)

            horario_label = tk.Label(horario_window, text="Horário (HH:MM):")
            horario_label.pack(side='left', padx=5, pady=5)
            horario_entry = tk.Entry(horario_window)
            horario_entry.pack(side='left', padx=5, pady=5)

            def recuperar_salas():
                data = data_entry.get()
                horario = horario_entry.get()
                try:
                    # Converte a data para o formato aaaa-mm-dd
                    data_formatada = datetime.strptime(data, '%d-%m-%Y').strftime('%Y-%m-%d')
                    datetime.strptime(horario, '%H:%M')  # Verifica o formato do horário
                except ValueError:
                    messagebox.showerror("Erro", "Formato de data ou horário inválido.")
                    return

                # Junta a data e o horário no formato correto
                datetime_formatado = f"{data_formatada} {horario}"

                salas = recuperar_salas_por_horario(datetime_formatado)
                if salas:
                    salas_window = tk.Toplevel()
                    salas_window.title("Salas Disponíveis")

                    tree = ttk.Treeview(salas_window, columns=("ID", "Nome", "Capacidade", "Empresa"), show="headings")
                    tree.heading("ID", text="ID")
                    tree.heading("Nome", text="Nome")
                    tree.heading("Capacidade", text="Capacidade")
                    tree.heading("Empresa", text="Empresa")

                    for sala in salas:
                        tree.insert("", tk.END, values=sala)

                    tree.pack(expand=True, fill=tk.BOTH)
                    tk.Button(salas_window, text="OK", command=salas_window.destroy).pack(pady=10)  # Botão OK para fechar a janela
                else:
                    messagebox.showinfo("Info", "Nenhuma sala disponível para este horário.")
                horario_window.destroy()

            tk.Button(horario_window, text="Recuperar Salas", command=recuperar_salas).pack(pady=10)

        solicitar_horario()

    def listar_palestras_de_palestrante():
        def solicitar_id_palestrante():
            # Criar uma nova janela para solicitar o nome do palestrante
            palestrante_window = tk.Toplevel()
            palestrante_window.title("Digite o Nome do Palestrante")

            # Label e Entry para digitar o nome do palestrante
            tk.Label(palestrante_window, text="Nome do Palestrante:").grid(row=0, column=0, padx=10, pady=5)
            palestrante_id_entry = tk.Entry(palestrante_window)
            palestrante_id_entry.grid(row=0, column=1, padx=10, pady=5)

            # Exibir a lista de palestrantes já cadastrados
            palestrantes = recuperar_palestrantes()
            tree = ttk.Treeview(palestrante_window, columns=("ID", "Nome", "Email", "Empresa"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Nome", text="Nome")
            tree.heading("Email", text="Email")
            tree.heading("Empresa", text="Empresa")

            for palestrante in palestrantes:
                tree.insert("", "end", values=palestrante)

            tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            # Função para recuperar e exibir as palestras do palestrante
            def recuperar_palestras():
                palestrante_nome = palestrante_id_entry.get()
                palestras = recuperar_palestras_por_palestrante(palestrante_nome)
                if palestras:
                    # Exibir as palestras em uma nova janela
                    palestras_window = tk.Toplevel()
                    palestras_window.title("Palestras do Palestrante")

                    # Criar a tabela de palestras
                    palestras_tree = ttk.Treeview(palestras_window, columns=("ID", "Título", "Horário", "Local", "Empresa"), show="headings")
                    palestras_tree.heading("ID", text="ID")
                    palestras_tree.heading("Título", text="Título")
                    palestras_tree.heading("Horário", text="Horário")
                    palestras_tree.heading("Local", text="Local")
                    palestras_tree.heading("Empresa", text="Empresa")

                    # Inserir as palestras na tabela
                    for palestra in palestras:
                        palestras_tree.insert("", "end", values=(palestra[0], palestra[1], palestra[2], palestra[3], palestra[4]))

                    palestras_tree.pack(expand=True, fill=tk.BOTH)
                else:
                    messagebox.showinfo("Info", "Nenhuma palestra encontrada para este palestrante.")
                palestrante_window.destroy()

            # Botão para recuperar as palestras
            tk.Button(palestrante_window, text="Recuperar Palestras", command=recuperar_palestras).grid(row=2, column=0, columnspan=2, pady=(10, 0))

        solicitar_id_palestrante()  # Chamada para iniciar o processo de listagem de palestras

    def listar_eventos_por_empresa():
        def mostrar_empresas():
            empresas = recuperar_empresas()

            empresas_window = tk.Toplevel(root)
            empresas_window.title("Empresas Cadastradas")

            tk.Label(empresas_window, text="Empresas Cadastradas:").pack()

            # Mostrar lista de empresas cadastradas
            for empresa in empresas:
                tk.Label(empresas_window, text=empresa[0]).pack()

        def buscar_eventos():
            empresa = empresa_entry.get()
            if empresa.strip():  # Verifica se o campo de entrada não está vazio
                eventos = recuperar_eventos_por_empresa(empresa)

                eventos_window = tk.Toplevel(root)
                eventos_window.title(f"Eventos da Empresa: {empresa}")

                tree = ttk.Treeview(eventos_window, columns=("ID", "Nome", "Data", "Local", "Empresa"), show="headings")
                tree.heading("ID", text="ID")
                tree.heading("Nome", text="Nome")
                tree.heading("Data", text="Data")
                tree.heading("Local", text="Local")
                tree.heading("Empresa", text="Empresa")

                for evento in eventos:
                    tree.insert("", tk.END, values=evento)

                tree.pack(expand=True, fill=tk.BOTH)
            else:
                messagebox.showerror("Erro", "Por favor, insira o nome da empresa.")

        empresa_window = tk.Toplevel(root)
        empresa_window.title("Digite o Nome da Empresa")

        tk.Label(empresa_window, text="Nome da Empresa:").grid(row=0, column=0, padx=10, pady=5)
        empresa_entry = tk.Entry(empresa_window)
        empresa_entry.grid(row=0, column=1, padx=10, pady=5)

        # Frame para os botões
        button_frame = tk.Frame(empresa_window)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Botão para mostrar empresas cadastradas
        tk.Button(button_frame, text="Mostrar Empresas Cadastradas", command=mostrar_empresas).pack(side=tk.LEFT, padx=5)
        # Botão para buscar eventos
        tk.Button(button_frame, text="Buscar Eventos", command=buscar_eventos).pack(side=tk.LEFT, padx=5)

    def quit_program():
        if messagebox.askokcancel("Sair", "Você tem certeza que quer sair?"):
            root.destroy()

    # Botões do lado esquerdo
    tk.Button(root, text="Inserir Evento", command=inserir_evento, borderwidth=5, relief="ridge").grid(row=1, column=0, pady=10, padx=(10, 5), sticky="ew")
    tk.Button(root, text="Inserir Participante", command=inserir_participante, borderwidth=5, relief="ridge").grid(row=2, column=0, pady=10, padx=(10, 5), sticky="ew")
    tk.Button(root, text="Inserir Palestra", command=inserir_palestra, borderwidth=5, relief="ridge").grid(row=3, column=0, pady=10, padx=(10, 5), sticky="ew")
    tk.Button(root, text="Inserir Sala", command=inserir_sala_gui, borderwidth=5, relief="ridge").grid(row=4, column=0, pady=10, padx=(10, 5), sticky="ew")
    tk.Button(root, text="Listar Eventos", command=listar_eventos, borderwidth=5, relief="ridge").grid(row=5, column=0, pady=10, padx=(10, 5), sticky="ew")

    # Botões do lado direito
    tk.Button(root, text="Listar Participantes de um Evento", command=listar_participantes_de_evento, borderwidth=5, relief="ridge").grid(row=1, column=1, pady=10, padx=(5, 10), sticky="ew")
    tk.Button(root, text="Listar Palestras de um Evento", command=listar_palestras_por_evento, borderwidth=5, relief="ridge").grid(row=2, column=1, pady=10, padx=(5, 10), sticky="ew")
    tk.Button(root, text="Listar Salas Disponíveis para um Horário", command=listar_salas_disponiveis_para_horario, borderwidth=5, relief="ridge").grid(row=3, column=1, pady=10, padx=(5, 10), sticky="ew")
    tk.Button(root, text="Listar Palestras de um Palestrante", command=listar_palestras_de_palestrante, borderwidth=5, relief="ridge").grid(row=4, column=1, pady=10, padx=(5, 10), sticky="ew")
    tk.Button(root, text="Recuperar Eventos por Empresa", command=listar_eventos_por_empresa, borderwidth=5, relief="ridge").grid(row=5, column=1, pady=10, padx=(5, 10), sticky="ew")
    tk.Button(root, text="Sair", command=quit_program, borderwidth=5, relief="ridge").grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

    root.mainloop()

if __name__ == "__main__":
    main()
