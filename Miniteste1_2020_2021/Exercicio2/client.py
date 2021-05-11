"""
Modulo que contêm a pequena aplicacao para a gestão de individuos
na tabela MYTABLE

Base de dados utilizada:
    - MySQL

Dependências Externas necessárias para correr este script:
    - Connector Python MySQL: `pip install mysql-connector-python` # https://pypi.org/project/mysql-connector-python/
"""
import mysql.connector
import os


class App:
    def __init__(self, user, password):
        """
        Construtor Base de todos os gestores.
        É instanciada uma conexão à base de dados MySQL com as credenciais fornecidas.
        """
        # Instanciar conexao à base de dados
        self.connection = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database="mt1",
        )
        self.cursor = self.connection.cursor()

    def _adicionar_utilizador(self):
        # Limpar consola
        os.system("cls")

        id = input("Insira o id do utilizador: ")
        nome = input("Insira o nome do utilizador: ")
        peso = input("Insira o peso do utilizador: ")

        # Chamar procedimento
        self.cursor.callproc("adicionar", args=[id, nome, peso])
        # Commit para guardar alteracoes
        self.connection.commit()

    def _atualizar_utilizador(self):
        # limpar consola
        os.system("cls")

        id = input("Insira o id do utilizador a atualizar: ")

        nome_new = input("Insira o novo nome do utilizador: ")
        peso_new = input("Insira o novo peso do utilizador: ")

        # Chamar procedimento
        self.cursor.callproc("atualizar", args=[id, nome_new, peso_new])
        # Commit para guardar alteracoes
        self.connection.commit()

    def _apagar_utilizador(self):
        # Limpar consola
        os.system("cls")

        id = input("Insira o id do utilizador a apagar: ")

        # Chamar procedimento
        self.cursor.callproc("remover", args=[id])
        # Commit para guardar alteracoes
        self.connection.commit()

    def run(self):

        while True:

            # limpar consola
            os.system("cls")

            # Apresentar menu
            print("Gestor de utilizadores:")
            print("\t1 - Adicionar utilizador")
            print("\t2 - Atualizar utilizador")
            print("\t3 - Apagar utilizador")

            print("q - Sair")

            opt = input("Opção: ")

            # Se for 'q' fechar app
            if opt == "q":
                break
            elif opt == "1":
                self._adicionar_utilizador()

            elif opt == "2":
                self._atualizar_utilizador()

            elif opt == "3":
                self._apagar_utilizador()

        # Fechar conexoes
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    """
    Entrypoint do script. O gestor é iniciado (com as suas credenciais),
    e é executado.
    """
    App(user="gestor_mytable", password="password").run()
