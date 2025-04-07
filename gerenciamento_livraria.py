# import sqlite3
import mysql.connector as conector
import random
from datetime import datetime
import csv

# Classes (Filhas) do sistema de gerenciamento de pedidos capaz de armazenar informações sobre livros, clientes e pedidos.

# TAREFA: 
# Sua tarefa é desenvolver um script em Python que se conecte a um banco de dados SQLite, crie as tabelas necessárias, 
# insira dados iniciais utilizando parâmetros nomeados e demonstre a seleção de dados relacionados usando JOIN, para obter informações completas sobre os pedidos, 
# incluindo detalhes dos livros e clientes.

class BancoDeDadosSqlite: # Classe responsável por criar e manipular o banco de dados SQLite.
    def __init__(self):
           self.conn = None # Inicialize a conexão como None
           self.cur = None  # Inicialize o cursor como None
           self.connect_to_db("Livraria_online")
           self.create_table("Livraria_online", "Livro", "Cliente", "Pedido")
            
    def connect_to_db(self, db):
           try:
               self.conn = conector.connect(
                   host="localhost",
                   user="root",
                   password="886744@Jo",
                   database=db
               )
               self.cur = self.conn.cursor()
               print(f"Conexão com o banco de dados '{db}' estabelecida com sucesso.")
               print("Conexão com o Banco de Dados aberta com sucesso!")
               return self.conn
           except conector.Error as e:
               print(f"Erro ao conectar com o banco de dados '{db}': {e}")
               self.con = None
               self.cur = None
               print(f"\nFalha ao se conectar ao Banco de Dados [CAUSA]: {e}") 
    
    def fechar_conexao(self):
        if self.cur: # Verifique se o cursor existe antes de tentar fechá-lo
            self.cur.close()
            print("\nCursor fechado.")
            
           # Encapsula o fechamento de conexões ao banco de dados.
        if self.conn: 
            # Verifica se a conexão existe
            # Verifique se a conexão existe antes de tentar fechá-la
               try:
                   if self.conn is not None:
                       # Confirme se a conexão ainda está ativa
                       self.conn.close() # Em seguida, feche a conexão
                       print("\nConexão ao banco de dados fechada!")
                   self.cur = None
                   self.con = None
               except conector.Error as e:
                   print("\nErro ao tentar fechar a conexão:", e)
                   return {"\nConexão [STATUS]": self.conn, "\nCursor [STATUS]": self.cur}
                   
    def create_table(self, db, table_name_1, table_name_2, table_name_3):
            try:
                # Abertura de conexão e aquisição de cursor
                self.conn = conector.connect(
                    host="localhost",
                    user="root",
                    password="886744@Jo",
                    database=db
                )
                self.cur = self.conn.cursor()
                # Execução de um comando: SELECT... CREATE ...
                comando_create_table_1 = '''CREATE TABLE IF NOT EXISTS ''' + table_name_1 + '''(
                                id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                titulo VARCHAR(150) NOT NULL,
                                autor VARCHAR(150) NOT NULL,
                                preco FLOAT NOT NULL
                                );'''
                comando_create_table_2 = '''CREATE TABLE IF NOT EXISTS ''' + table_name_2 + '''(
                     id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
                     nome VARCHAR(150) NOT NULL,
                     email VARCHAR(150) NOT NULL,
                     telefone VARCHAR(150) NOT NULL
                    );'''
                comando_create_table_3 = '''CREATE TABLE IF NOT EXISTS ''' + table_name_3 + '''(
                    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    cliente_id INTEGER NOT NULL,
                    livro_id INTEGER NOT NULL,
                    quantidade INTEGER,
                    data_pedido DATE NOT NULL,
                    FOREIGN KEY (cliente_id) REFERENCES Cliente(id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (livro_id) REFERENCES Livro(id) ON DELETE CASCADE ON UPDATE CASCADE
                    );'''
                self.cur.execute(comando_create_table_1)
                self.cur.execute(comando_create_table_2)
                self.cur.execute(comando_create_table_3)
                self.conn.commit()
                data_time = datetime.now()
                dt = data_time.strftime("%d/%m/%Y %H:%M:%S")
                print(f"\nTable {table_name_1} created at {dt}")
                print(f"Table {table_name_2} created at {dt}")
                print(f"Table {table_name_3} created at {dt}")
                print(f"\nTabelas criadas com sucesso! Primeira tabela criada foi a tabela de '{table_name_1}', a segunda table criada foi a tabela de '{table_name_2}' e, por fim, a última tabela criada foi a tabela de '{table_name_3}'.\n")
            except conector.Error as e:
                print(f"\nErro ao criar tabelas: {e}")
    
    def inserir_dados(self, livro, cliente, pedido):
        """Insere dados no banco de dados."""
        self.cur = self.conn.cursor()
        livros = [livro]
        clientes = [cliente]
        pedidos = [pedido]
        try:
            inserir_livros = 'INSERT INTO livro (id, titulo, autor, preco) VALUES (%s, %s, %s, %s)'
            for livro in livros:
                self.cur.execute(inserir_livros, (livro.id, livro.titulo, livro.autor, livro.preco))

            inserir_clientes = 'INSERT INTO cliente (id, nome, email, telefone) VALUES (%s, %s, %s, %s)'
            for cliente in clientes:
                self.cur.execute(inserir_clientes, (cliente.id, cliente.nome, cliente.email, cliente.telefone))

            inserir_pedidos = 'INSERT INTO pedido (cliente_id, livro_id, quantidade, data_pedido) VALUES (%s, %s, %s, %s)'
            for pedido in pedidos:
                self.cur.execute(inserir_pedidos, (pedido.cliente_id, pedido.livro_id, pedido.quantidade, pedido.data_pedido))

            self.conn.commit()
            print("\nDados inseridos com sucesso!")
            
            data_hora_atual = datetime.now()
            data_cadastro = data_hora_atual.strftime("%Y-%m-%d")
            hora_cadastro = data_hora_atual.strftime("%H:%M:%S")
            print(f"\nDados inseridos com sucesso! Data de cadastro: {data_cadastro}, Hora de cadastro: {hora_cadastro}.\n")
            
            data_time = datetime.now()
            dt = data_time.strftime("%d/%m/%Y %H:%M:%S")
            print(f"\nOs dados foram inseridos no banco de dados no dia e hora: {dt}.\n")
            
        except conector.Error as e:
                print(f"\nErro ao INSERIR DADOS nas tabelas: {e}")
        finally:
                self.fechar_conexao() 
            
    def exibir_dados_inserirdos(self):
        """Exibe dados do banco de dados."""
        query_1_SELECT = '''SELECT * FROM livro'''
        query_2_SELECT = '''SELECT * FROM cliente'''
        query_3_SELECT = '''SELECT * FROM pedido'''
        
        self.cur.execute(query_1_SELECT)
        livros = self.cur.fetchall()
        self.cur.execute(query_2_SELECT)
        clientes = self.cur.fetchall()
        self.cur.execute(query_3_SELECT)
        pedidos = self.cur.fetchall()
        
        for livros in livros:
            print(f"\nTitulo: {livros[1]}, Autor: {livros[2]}, Preço: {livros[3]}")
        for clientes in clientes:
            print(f"\nNome: {clientes[1]}, Email: {clientes[2]}, Telefone: {clientes[3]}")
        for pedidos in pedidos:
            print(f"\nCliente ID: {pedidos[1]}, Livro ID: {pedidos[2]}, Quantidade: {pedidos[3]}, Data Pedido: {pedidos[4]}")
        data_time = datetime.now()
        dt = data_time.strftime("%d/%m/%Y %H:%M:%S")
        print(f"\nData e Hora das consultas: {dt}\n")
            
    def exibir_dados(self):
        """Exibe dados do banco de dados."""
        self.cur = self.conn.cursor()
        query_SELECT = '''SELECT p.id, c.nome, l.titulo, p.quantidade, p.data_pedido
        FROM pedido p
        INNER JOIN cliente c ON p.cliente_id = c.id
        INNER JOIN livro l ON p.livro_id = l.id;'''
        self.cur.execute(query_SELECT)
        pedidos = self.cur.fetchall()
        print("\nPedidos:\n")
        for pedido in pedidos:
            print(f"ID: {pedido[0]}, Nome: {pedido[1]}, Titulo: {pedido[2]}, Quantidade: {pedido[3]}, Data Pedido: {pedido[4]}")
            data_time = datetime.now()
            dt = data_time.strftime('%d/%m/%Y %H:%M:%S')
            print(f"\nData e Hora das consultas: {dt}\n")
            
    def atualizar_dados(self, table, id, coluna, valor):
        """Atualiza dados do banco de dados."""
        self.cur = self.conn.cursor()
        query_UPDATE = '''UPDATE {} SET {} = %s WHERE id = %s'''.format(table, coluna)
        try:
            self.cur.execute(query_UPDATE, (valor, id))
            self.conn.commit()
            print("Dados atualizados com sucesso!")
            data_time = datetime.now()
            dt = data_time.strftime('%d/%m/%Y %H:%M:%S')
            print(f"\nData e Hora da Atualização: {dt}\n")
            if self.cur.rowcount > 0:
                return dt
            else:
                return None
        except conector.Error as e:
            self.conn.rollback()
            print(f"Erro ao atualizar dados: {e}")
            self.cur = None
            
    def excluir_dados(self, id):
        """Exclui dados do banco de dados."""
        self.cur = self.conn.cursor()
        query_DELETE = '''DELETE FROM pedido WHERE id = %s'''
        try:
            self.cur.execute(query_DELETE, (id,))
            self.conn.commit()
            print("\nDados excluídos com sucesso!\n")
            data_time = datetime.now()
            dt = data_time.strftime('%d/%m/%Y %H:%M:%S')
            print(f"\nData e Hora da Exclusão: {dt}\n")
            if self.cur.rowcount > 0:
                return dt
            else:
                return None
        except conector.Error as e:
            self.conn.rollback()
            print(f"Erro ao excluir dados: {e}")
            self.cur = None
    
    def salvar_dados_csv(self):
        """Salva dados do banco de dados em um arquivo CSV."""
        self.cur = self.conn.cursor()
        query_SELECT = '''SELECT p.id, c.nome, l.titulo, p.quantidade, p.data_pedido
        FROM pedido p
        INNER JOIN cliente c ON p.cliente_id = c.id
        INNER JOIN livro l ON p.livro_id = l.id;'''
        self.cur.execute(query_SELECT)
        pedidos = self.cur.fetchall()
        # Criando o arquivo .csv da tabela Pedidos:
        with open('pedidos.csv', 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Nome', 'Titulo', 'Quantidade', 'Data Pedido']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for pedido in pedidos:
                writer.writerow({
                    'ID': pedido[0],
                    'Nome': pedido[1],
                    'Titulo': pedido[2],
                    'Quantidade': pedido[3],
                    'Data Pedido': pedido[4]
                })
            data_time = datetime.now()
            dt = data_time.strftime('%d/%m/%Y %H:%M:%S')
            print(f"\nData e Hora da Criação do Relatório: {dt}\n")
            print("\nDados salvos com sucesso no arquivo CSV!\n")
        with open('pedidos.csv', 'r') as file:
            try:
                print(file.read())
                self.cur = None
            except Exception as e:
                print(f"Erro ao salvar dados no arquivo CSV: {e}")
                self.cur = None
        self.cur = None
                
# Classes princiapis do sistema de gerenciamento de livros e de pedidos                                
class Livro(BancoDeDadosSqlite):
    def __init__(self, id, titulo, autor, preco):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.preco = preco
        try:
            self.conn = conector.connect(
                host="localhost",
                user="root",
                password="886744@Jo",
                database="Livraria_online"
               )
            self.cur = self.conn.cursor()
        except conector.Error as e:
            print(f"Erro ao conectar com o banco de dados 'Livraria_online': {e}")
            
    def cadastrar_livro(self, livro):
        """Cadastra um livro no banco de dados."""
        try:
            self.cur = self.conn.cursor()
            query_INSERT = '''INSERT INTO livro (id, titulo, autor, preco) VALUES (%s, %s, %s, %s);'''
            self.cur.execute(query_INSERT, (livro.id, livro.titulo, livro.autor, livro.preco))
            self.conn.commit()
            print("Livro cadastrado com sucesso!")
        except conector.Error as e:
            self.conn.rollback()
            print(f"Erro ao cadastrar livro: {e}")
        finally:
            self.cur = None
    def buscar_livro(self, id):
            """Busca um livro no banco de dados pelo seu ID."""
            self.cur = self.conn.cursor()
            query_SELECT = '''SELECT * FROM livro WHERE id = ''' + str(id)
            self.cur.execute(query_SELECT)
            livro = self.cur.fetchone()
            self.cur = None
            return livro
    def buscar_todos_livros(self):
            """Busca todos os livros no banco de dados."""
            self.cur = self.conn.cursor()
            query_SELECT = '''SELECT * FROM livro;'''
            self.cur.execute(query_SELECT)
            livros = self.cur.fetchall()
            self.cur = None
            return livros
            
    def consultar_livros(self):
        """Exibe dados do banco de dados."""
        query_SELECT = '''SELECT * FROM livro'''
        self.cur.execute(query_SELECT)
        livros = self.cur.fetchall()
        print("\nLivros:\n")
        for livro in livros:
            print(f"ID: {livro[0]}, Titulo: {livro[1]}, Autor: {livro[2]}, Preco: {livro[3]}")
            
class Cliente(BancoDeDadosSqlite):
    def __init__(self, id, nome, email, telefone):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        try:
            self.conn = conector.connect(
                host="localhost",
                user="root",
                password="886744@Jo",
                database="Livraria_online"
               )
            self.cur = self.conn.cursor()
        except conector.Error as e:
            print(f"Erro ao conectar com o banco de dados 'Livraria_online': {e}")
            
    def cadastrar_cliente(self, cliente):
        """Cadastra um cliente no banco de dados."""
        try:
            self.cur = self.conn.cursor()
            query_INSERT = '''INSERT INTO cliente (id, nome, email, telefone) VALUES (%s, %s, %s, %s);'''
            self.cur.execute(query_INSERT, (cliente.id, cliente.nome, cliente.email, cliente.telefone))
            self.conn.commit()
            print("Cliente cadastrado com sucesso!")
            data_time = datetime.now()
            dt = data_time.strftime('%d/%m/%Y %H:%M:%S')
            print(f"\nData e Hora do Cadastro: {dt}\n")
        except conector.Error as e:
            self.conn.rollback()
            print(f"Erro ao cadastrar cliente: {e}")
        finally:
            self.cur = None
    def buscar_cliente(self, id):
            """Busca um cliente no banco de dados pelo seu ID."""
            self.cur = self.conn.cursor()
            query_SELECT = '''SELECT * FROM cliente WHERE id = ''' + str(id)
            self.cur.execute(query_SELECT)
            cliente = self.cur.fetchone()
            self.cur = None
            return cliente
    def buscar_todos_clientes(self):
        """Busca todos os clientes no banco de dados."""
        self.cur = self.conn.cursor()
        query_SELECT = '''SELECT * FROM cliente;'''
        self.cur.execute(query_SELECT)
        clientes = self.cur.fetchall()
        self.cur = None
        return clientes
    
    def consultar_clientes(self):
        """Exibe dados do banco de dados."""
        query_SELECT = '''SELECT * FROM cliente'''
        self.cur.execute(query_SELECT)
        clientes = self.cur.fetchall()
        print("\nClientes:\n")
        for cliente in clientes:
            print(f"ID: {cliente[0]}, nome: {cliente[1]}, email: {cliente[2]}, telefone: {cliente[3]}")
                
class Pedido(BancoDeDadosSqlite):
    def __init__(self, cliente_id, livro_id, quantidade, data_pedido):
        self.cliente_id = cliente_id
        self.livro_id = livro_id
        self.quantidade = quantidade
        self.data_pedido = data_pedido 
        try:
            self.conn = conector.connect(
                host="localhost",
                user="root",
                password="886744@Jo",
                database="Livraria_online"
               )
            self.cur = self.conn.cursor()
        except conector.Error as e:
            print(f"Erro ao conectar com o banco de dados 'Livraria_online': {e}")
            
    def cadastrar_pedido(self, pedido):
        """Cadastra um pedido no banco de dados."""
        try:
            self.cur = self.conn.cursor()
            query_INSERT = '''INSERT INTO pedido (cliente_id, livro_id, quantidade, data_pedido)
            VALUES (%s, %s, %s, %s);'''
            self.cur.execute(query_INSERT, (pedido.cliente_id, pedido.livro_id, pedido.quantidade, pedido.data_pedido))
            self.conn.commit()
            print("Pedido cadastrado com sucesso!")
            data_time = datetime.now()
            dt = data_time.strftime('%d/%m/%Y %H:%M:%S')
            print(f"\nData e Hora do Cadastro: {dt}\n")
        except conector.Error as e:
            self.conn.rollback()
            print(f"Erro ao cadastrar pedido: {e}")
        finally:
            self.cur = None
        
    def buscar_pedido(self, id):
            """Busca um pedido no banco de dados pelo seu ID."""
            self.cur = self.conn.cursor()
            query_SELECT = '''SELECT * FROM pedido WHERE id = ''' + str(id)
            self.cur.execute(query_SELECT)
            pedido = self.cur.fetchone()
            self.cur = None
            return pedido
        
    def buscar_todos_pedidos(self):
            """Busca todos os pedidos no banco de dados."""
            self.cur = self.conn.cursor()
            query_SELECT = '''SELECT * FROM pedido;'''
            self.cur.execute(query_SELECT)
            pedidos = self.cur.fetchall()
            self.cur = None
            return pedidos
        
    def consultar_pedidos(self):
        """Exibe dados do banco de dados."""
        query_SELECT = '''SELECT * FROM pedido'''
        self.cur.execute(query_SELECT)
        pedidos = self.cur.fetchall()
        print("\nPedidos:\n")
        for pedido in pedidos:
            print(pedido)
            print(f"\nID: {pedido[0]}, Cliente ID: {pedido[1]}, Livro ID: {pedido[2]}, Quantidade: {pedido[3]}, Data Pedido: {pedido[4]}\n")
                
# Monatando o script principal do programa de gerenciamento de livrros e pedidos em uma livraria on-line
if __name__ == "__main__":
    livro = Livro(0, "", "", 0.00) # Variáveis globais
    cliente = Cliente(0, "", "", "")
    pedido = Pedido(0, 0, 0, "")
    print("\nSistema de Gerenciamento de Livraria Online\n")
    print("\n Sistema de registro de livros e pedidos\n")
    data_time = datetime.now()
    dt = data_time.strftime('%d/%m/%Y %H:%M:%S')
    print(f"\nData e Hora da Execução do programa: {dt}\n")
    # Cadastrando livros, clientes e pedidos
    print("\n1 - Cadastrar Livro")
    print("2 - Cadastrar Cliente")
    print("3 - Cadastrar Pedido")
    print("4 - Exibir Dados")
    print("5 - Sair do Sistema")
    print("\n")
    while True:
        opcao = input("Escolha uma opção: ") # Cadastro de novos livros
        if opcao == "1":
            try:
                id = int(input("Digite o ID do livro (somente números interiros): "))
            except TypeError:
                print("Erro: ID do livro deve ser um número inteiro")
                break
            try:
                titulo = input("Digite o Titulo do Livro: ")
                autor = input("Digite o Autor do Livro: ")
                preco = float(input("Digite o Preco do Livro: "))
                livro = Livro(id, titulo, autor, preco)
                livro.cadastrar_livro(livro)
                print("\nLivro cadastrado com sucesso!\n")
            except ValueError:
                print("Erro: ID e preço devem ser números inteiros e reais.")
                break
            try:
                print("\nDeseja pesquisar por um livro?\n")
                print("1 - Sim")
                print("2 - Não")
                opcao_pesquisa = input("\nEscolha uma opção: ")
                if opcao_pesquisa == "1":
                    id_pesquisa = int(input("Digite o ID do livro que deseja pesquisar: "))
                    print(livro.buscar_livro(id_pesquisa))
                else:
                    print("Deseja ver todos os livros cadastrados?\n")
                    print("1 - Sim")
                    print("2 - Não")
                    try:
                        opcao_ver_livros = input("\nEscolha uma opção:")
                        if opcao_ver_livros == "1":
                            print(livro.buscar_todos_livros())
                        elif opcao_ver_livros == "2":
                            print("Saindo do sistema de gerenciamento de livros...")
                            print("Deseja continuar cadastrando livros?")
                            print("1 - Sim")
                            print("2 - Não")
                            try:
                                opcao_continuar = input("\nEscolha uma opção:")
                                if opcao_continuar == "1":
                                    continue
                                elif opcao_continuar == "2":
                                    print("Saindo do sistema de gerenciamento de livros...")
                                    break
                            except ValueError:
                                print("Erro: Opção inválida. Saindo do sistema de gerenciamento")
                                break
                            break
                        else:
                            print("Opção inválida. Por favor, tente novamente.")
                    except ValueError:
                        print("Opção inválida. Por favor, tente novamente.")
            except ValueError:
                print("Erro: ID deve ser um número inteiro")
                break
            
            #Livro(1, 'Python para Iniciantes', 'John Doe', 39.99),
            # Livro(2, 'Algoritmos e Estruturas de Dados', 'Jane Smith', 49.99),
            # Livro(3, 'Inteligência Artificial', 'Alan Turing', 59.99)
            
        elif opcao == "2": # Cadastro de novos clientes
            try:
                id = int(input("Digite o ID do cliente (somente números interiros): "))
            except TypeError:
                print("Erro: ID do cliente deve ser um número inteiro")
                break
            try:
                nome = input("Digite o Nome do Cliente: ")
                email = input("Digite o Email do Cliente: ")
                telefone = input("Digite o Telefone do Cliente: ")
                cliente = Cliente(id, nome, email, telefone)
                cliente.cadastrar_cliente(cliente)
                print("\nCliente cadastrado com sucesso!\n")
                try:
                    print("\nDeseja pesquisar por um cliente?\n")
                    print("1 - Sim")
                    print("2 - Não")
                    opcao_pesquisa = input("\nEscolha uma opção:")
                    if opcao_pesquisa == "1":
                        id_pesquisa = int(input("Digite o ID do cliente que deseja pesquisar: "))
                        print(cliente.buscar_cliente(id_pesquisa))
                    else:
                        print("Deseja ver todos os clientes cadastrados?\n")
                        print("1 - Sim")
                        print("2 - Não")
                    try:
                        opcao_ver_clientes = input("\nEscolha uma opção: ")
                        if opcao_ver_clientes == "1":
                            print(cliente.buscar_todos_clientes())
                        elif opcao_ver_livros == "2":
                            print("Saindo do sistema de gerenciamento de livros...")
                            print("Deseja continuar cadastrando livros?")
                            print("1 - Sim")
                            print("2 - Não")
                            try:
                                opcao_continuar = input("\nEscolha uma opção:")
                                if opcao_continuar == "1":
                                    continue
                                elif opcao_continuar == "2":
                                    print("Saindo do sistema de gerenciamento de livros...")
                                    break
                            except ValueError:
                                print("Erro: Opção inválida. Saindo do sistema de gerenciamento")
                                break
                            break
                        else:
                            print("Opção inválida. Por favor, tente novamente.")
                    except ValueError:
                        print("Opção inválida. Por favor, tente novamente.")
                except ValueError:
                    print("Erro: ID deve ser um número inteiro")
                    break
            except ValueError:
                    print("Erro: ID, preço e quantidade devem ser números inteiros")
            
            # Cliente(1, 'Alice', 'alice@example.com', '1234567890'),
            # Cliente(2, 'Bob', 'bob@example.com', '9876543210'),
            # Cliente(3, 'Charlie', 'charlie@example.com', '995678309')
            
        elif opcao == "3": # Cadastro de novos pedidos
            try:
                cliente_id = int(input("Digite o ID do Cliente (somente números interiros): "))
                livro_id = int(input("Digite o ID do Livro (somente números inteiros): "))
            except TypeError:
                print("Erro: ID do cliente e do livro devem ser um número inteiro")
                break
            try:
                quantidade = int(input("Digite a Quantidade do Livro: "))
            except TypeError:
                print("Erro: Quantidade deve ser um número inteiro")
                break
            data_pedido = datetime.now().strftime('%Y-%m-%d')
            try:
                pedido = Pedido(cliente_id, livro_id, quantidade, data_pedido)
                pedido.cadastrar_pedido(pedido)
                print("\nPedido cadastrado com sucesso!\n")
            except ValueError:
                print("Erro: ID do cliente, ID do livro e a quantidade devem ser números inteiros")
                break
            try:
                    print("\nDeseja pesquisar por um pedido? \n")
                    print("1 - Sim")
                    print("2 - Não")
                    opcao_pesquisa = input("\nEscolha uma opção: ")
                    if opcao_pesquisa == "1":
                        id_pesquisa = int(input("Digite o ID do pedido que deseja pesquisar: "))
                        print(pedido.buscar_pedido(id_pesquisa))
                    else:
                        print("Deseja ver todos os pedidos cadastrados? \n")
                        print("1 - Sim")
                        print("2 - Não")
                    try:
                        opcao_ver_pedidos = input("\nEscolha uma opção: ")
                        if opcao_ver_pedidos == "1":
                            print(pedido.buscar_todos_pedidos())
                        elif opcao_ver_livros == "2":
                            print("Saindo do sistema de gerenciamento de livros...")
                            print("Deseja continuar cadastrando livros? ")
                            print("1 - Sim")
                            print("2 - Não")
                            try:
                                opcao_continuar = input("\nEscolha uma opção: ")
                                if opcao_continuar == "1":
                                    continue
                                elif opcao_continuar == "2":
                                    print("Saindo do sistema de gerenciamento de livros...")
                                    break
                            except ValueError:
                                print("Erro: Opção inválida. Saindo do sistema de gerenciamento")
                                break
                            break
                        else:
                            print("Opção inválida. Por favor, tente novamente.")
                    except ValueError:
                        print("Opção inválida. Por favor, tente novamente.")
            except ValueError:
                print("Erro: ID deve ser um número inteiro")
                break
           
            # Pedido(1, 1, 2, '2023-06-15'),
            # Pedido(2, 2, 1, '2023-06-16'),
            # Pedido(3, 3, 3, '2023-06-17')
               
        elif opcao == "4":
            print("\n Dados Cadastrados: \n")
            print("Livros Cadastrados: ")
            print(livro.consultar_livros())
            print("\n Clientes Cadastrados: ")
            print(cliente.consultar_clientes())
            print("\n Pedidos Cadastrados: ")
            print(pedido.consultar_pedidos())
            
        elif opcao == "5":
            print("\n Obrigado por usar o sistema de gerenciamento de livraria online! \n")
            break
        else:
            print("\n Opção Inválida! Você escolheu uma opção que não existe. Por favor, tente novamente. \n")
            print("\n Obrigado por usar o sistema de gerenciamento de livraria online! \n")
            break
        
    banco = BancoDeDadosSqlite()
    banco.exibir_dados_inserirdos()
    banco.exibir_dados()
    
    banco.salvar_dados_csv()
    
    # banco.atualizar_dados("livro", 2, "titulo", "Algoritmos e Estruturas de Dados")
    banco.exibir_dados_inserirdos()
    
    # banco.excluir_dados(1)
    # banco.exibir_dados_inserirdos()
    
    # banco.exibir_dados()
    
    # Fechar a conexão com o banco de dados
    banco.fechar_conexao()    