import mysql.connector
import os
import time


class App:
    def __init__(self):
        # Instanciar conexao à base de dados
        self.connection = mysql.connector.connect(
            host="localhost", user="root", password="password", database="ex2"
        )

        self.cursor = self.connection.cursor()

    def _adicionar_aluno(self):
        # Limpar consola
        os.system("cls")
        nome = input("Insira o nome do aluno: ")
        endereco = input("Insira o endereço do aluno: ")
        # Não faço ideia do que seja "garantia"...
        garantia = input("Insira a garantia do aluno: ")
        # Executar stored procedure
        self.cursor.callproc("adicionar_aluno", args=[nome, endereco, garantia])
        # Commit para guardar alteracoes
        self.connection.commit()

    def _atualizar_aluno(self):
        # Limpar consola
        os.system("cls")
        numero = input("Qual o número do aluno a atualizar?")

        nome_new = input("Qual o novo nome?")
        endereco_new = input("Qual o novo endereço?")
        garantia_new = input("Qual a nova garantia?")

        # Chamar procedimento
        self.cursor.callproc(
            "atualizar_aluno", args=[numero, nome_new, endereco_new, garantia_new]
        )
        # Commit para guardar alteracoes
        self.connection.commit()

    def _apagar_aluno(self):
        # Limpar consola
        os.system("cls")

        numero = input("Qual o número do aluno a apagar?")

        # Chamar procedimento
        self.cursor.callproc("apagar_aluno", args=[numero])
        # Commit para guardar alteracoes
        self.connection.commit()

    def _listar_livros(self):
        # Limpar consola
        os.system("cls")
        self.cursor.execute("SELECT * FROM Livro")
        q = self.cursor.fetchall()

        print(q)
        input("Pressione alguma tecla para continuar")

    def _adicionar_livro(self):
        # Limpar consola
        os.system("cls")

        titulo = input("Insira o titulo do livro: ")
        autor = input("Insira o autor do livro: ")
        editor = input("Insira o editor do livro: ")

        # Chamar procedimento
        self.cursor.callproc("adicionar_livro", args=[titulo, autor, editor])
        # Commit para guardar alteracoes
        self.connection.commit()

    def _atualizar_livro(self):
        # limpar consola
        os.system("cls")

        numero = input("Qual o número do livro a atualizar?")

        titulo_new = input("Qual o novo titulo?")
        autor_new = input("Qual o novo autor?")
        editor_new = input("Qual o novo editor?")

        # Chamar procedimento
        self.cursor.callproc(
            "atualizar_livro", args=[numero, titulo_new, autor_new, editor_new]
        )
        # Commit para guardar alteracoes
        self.connection.commit()

    def _apagar_livro(self):
        # Limpar consola
        os.system("cls")

        numero = input("Qual o número do livro a apagar?")

        # Chamar procedimento
        self.cursor.callproc("apagar_livro", args=[numero])
        # Commit para guardar alteracoes
        self.connection.commit()

    def _listar_alunos(self):
        # Limpar consola
        os.system("cls")
        self.cursor.execute("SELECT * FROM Aluno")
        q = self.cursor.fetchall()

        print(q)
        input("Pressione alguma tecla para continuar")

    def _adicionar_emprestimo(self):
        # Limpar consola
        os.system("cls")

        aluno = input("Insira o número do aluno: ")
        livro = input("Insira o número do livro: ")

        self.cursor.callproc("adicionar_emprestimo", args=[aluno, livro])
        self.connection.commit()

    def _devolver_livro(self):
        # Limpar consola
        os.system("cls")

        aluno = input("Insira o número do aluno: ")
        livro = input("Insira o número do livro: ")
        data_requisicao = input("Insira a data de requisicao: ")

        # Chamar procedimento
        self.cursor.callproc("devolver_livro", args=[aluno, livro, data_requisicao])
        self.connection.commit()

    def _relatorio_livros_nao_entregues(self):
        # Limpar consola
        os.system("cls")

        opt = input("Pretende que o relatório seja especifico de um aluno? (y/n)")

        # Se opt for sim, perguntamos o aluno e passamos na chamada de procedimento
        if opt == "y":
            aluno = input("Insira o número de aluno: ")
            self.cursor.callproc("relatorio_livros_nao_entregues", args=[aluno])

        else:
            # Se não chamamos o procedimento sem passar o aluno
            # O que irá dar um relatorio de todos os livros nao entregues
            self.cursor.callproc("relatorio_livros_nao_entregues", args=[None])

        print("Livros não entregues:")

        for result in self.cursor.stored_results():
            print(result.fetchone())

        input("Pressione alguma tecla para continuar...")

    def run(self):
        while True:

            # limpar consola
            os.system("cls")

            # Apresentar menu
            print("MENU:")
            print("Alunos:")
            print("\t1 - Listar alunos")
            print("\t2 - Adicionar aluno")
            print("\t3 - Atualizar aluno")
            print("\t4 - Apagar aluno")

            print("Livros:")
            print("\t5 - Listar livros")
            print("\t6 - Adicionar livro")
            print("\t7 - Atualizar livro")
            print("\t8 - Apagar livro")

            print("Empréstimos:")
            print("\t9 - Fazer empréstimo")
            print("\t10 - Entregar livro")
            print("\t11 - Relatório de livros não entregues")

            print("q - Sair")

            opt = input("Opção: ")

            # Se for 'q' fechar app
            if opt == "q":
                break
            elif opt == "1":
                self._listar_alunos()

            elif opt == "2":
                self._adicionar_aluno()

            elif opt == "3":
                self._atualizar_aluno()

            elif opt == "4":
                self._apagar_aluno()

            elif opt == "5":
                self._listar_livros()

            elif opt == "6":
                self._adicionar_livro()

            elif opt == "7":
                self._atualizar_livro()

            elif opt == "8":
                self._apagar_livro()

            elif opt == "9":
                self._adicionar_emprestimo()

            elif opt == "10":
                self._devolver_livro()

            elif opt == "11":
                self._relatorio_livros_nao_entregues()
        # Fechar conexoes
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    App().run()
