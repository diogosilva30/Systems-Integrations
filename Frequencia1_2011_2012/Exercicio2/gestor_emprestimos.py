from gestor_base import GestorBase
import os


class GestorEmprestimos(GestorBase):
    """
    Classe que faz a gestão dos empréstimos
    """

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
            print("Gestor de empréstimos:")
            print("\t1 - Fazer empréstimo")
            print("\t2 - Entregar livro")
            print("\t3 - Relatório de livros não entregues")

            print("q - Sair")

            opt = input("Opção: ")

            # Se for 'q' fechar app
            if opt == "q":
                break
            elif opt == "1":
                self._adicionar_emprestimo()

            elif opt == "2":
                self._devolver_livro()

            elif opt == "3":
                self._relatorio_livros_nao_entregues()

        # Fechar conexoes
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    """
    Entrypoint do script
    """
    # Instanciamos um gestor de emprestimos com as credenciais corretas
    # deste serviço e corremos o gestor
    GestorEmprestimos("gestor_emprestimos", "password").run()
